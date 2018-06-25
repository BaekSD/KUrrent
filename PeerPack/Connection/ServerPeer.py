import socket, threading, json
import random

class ServerPeer(threading.Thread):

    def __init__(self, client_socket, file_hash, lock):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.file_hash = file_hash
        self.lock = lock
        from PeerPack import db
        self.file_path, self.last_index = db.get_file_data(self.file_hash)

    def run(self):
        self.recv_msg()

    def create_dict(self, head, body, foot=None):
        msg_dict = {
            'HEAD': head,
            'BODY': body
        }
        if foot is not None:
            msg_dict['FOOT'] = foot
        return msg_dict

    def get_needed_blocks(self):
        from PeerPack import db
        block_list = db.get_blocks('test')
        request_list = []
        for i in range(self.last_index):
            if not block_list.__contains__(i + 1):
                request_list.append(i + 1)
        return request_list

    def send_msg(self, msg):
        msg = json.dumps(msg)
        msg = msg.encode('utf-8')
        self.client_socket.send(msg)

    def recv_msg(self, buf_size=10000):
        from PeerPack import db

        while True:
            msg = self.client_socket.recv(buf_size)
            head, body = self.decode_msg(msg)

            my_block_list = db.get_blocks(self.file_hash)

            if head is 'BOOTSTRAP_PHASE':
                self.send_block(my_block_list)
            elif head is 'DOWNLOAD_PHASE':
                self.send_block(my_block_list, body)
            elif head is 'LAST_PHASE':
                self.send_block(my_block_list, body)
            elif head is 'COMPLETE_PHASE':
                break
            elif head is 'ASK':
                phase, request_block = self.get_status()
                if phase is not 'COMPLETE_PHASE':
                    msg_dict = self.create_dict('QUIT', 'QUIT')
                else:
                    msg_dict = self.create_dict('REQ', request_block)
                self.send_msg(msg_dict)

            elif head is 'BLOCK':
                block_num = msg['FOOT']
                from PeerPack import fm, db

                fm.write_block_data(self.file_path, block_num)
                db.put_block_info(self.file_hash, block_num)

            elif head is 'QUIT':
                break

    def get_status(self):
        from PeerPack import db
        block_list = db.get_blocks(self.file_hash)

        block_ratio = block_list.__len__() / self.last_index
        body = 'EMPTY'
        status = ''

        if block_ratio < 0.9:
            status = 'DOWNLOAD_PHASE'
            body = self.get_needed_blocks()
        elif block_ratio < 1:
            status = 'LAST_PHASE'
            body = self.get_needed_blocks()
        elif block_ratio == 1:
            status = 'COMPLETE_PHASE'
        else:
            print('Send Status Error')
        return status, body

    def send_block(self, my_block_list, request_block_list=None):
        send_block_list = []

        if request_block_list is not None:
            for i in range(request_block_list.__len__()):
                if my_block_list.__contains__(request_block_list[i]):
                    send_block_list.append(request_block_list[i])
            send_block_list = self.choice_block(send_block_list)
        # When Client is BootStrap Phase
        else:
            send_block_list = self.choice_block(my_block_list)

        for i in range(send_block_list.__len__()):
            from PeerPack import fm
            block_dict = self.create_dict('BLOCK', fm.read_block_data(self.file_path, send_block_list[i]), send_block_list[i])
            self.send_msg(block_dict)

    def choice_block(self, send_block_list):
        send_list = []
        try:
            for i in range(10):
                data = send_block_list.pop(random.choice(send_block_list))
                send_list.append(data)
        except Exception as e:
            print(e)
        return send_list

    def decode_msg(self, msg):
        msg = msg.decode('utf-8')
        file_dict = json.loads(msg)
        return file_dict['HEAD'], file_dict['BODY']
