import socket, threading, json, binascii
from PeerPack.Model import BlockVO
import random

class ClientPeer(threading.Thread):
    def __init__(self, peer):
        threading.Thread.__init__(self)
        self.peer = peer
        self.client_socket = self.connect_to_peer()
        from PeerPack import db
        self.file_path, self.last_index = db.get_file_data(self.peer.file_hash)

    def connect_to_peer(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.peer.ip, self.peer.port))
        return client_socket

    def run(self):
        peer_dict = self.create_dict('PEER', self.peer.file_hash)
        self.send_msg(peer_dict)
        status, body = self.get_status()
        if status != 'COMPLETE_PHASE':
            self.recv_msg()

    def send_status(self, status, body):
        request_dict = self.create_dict(status, body)
        self.send_msg(request_dict)

    def get_status(self):
        from PeerPack import db
        block_list = db.get_blocks(self.peer.file_hash)

        block_ratio = block_list.__len__() / self.last_index
        body = 'EMPTY'
        status = ''
        if block_ratio == 0:
            status = 'BOOTSTRAP_PHASE'
        elif block_ratio < 0.9:
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
        print(msg)

    def recv_msg(self, buf_size=10000):
        from PeerPack import fm, db

        while True:
            msg = self.client_socket.recv(buf_size)
            print(msg)
            head, body, block_num = self.decode_msg(msg)

            my_block_list = db.get_blocks(self.peer.file_hash)

            if head == 'BLOCK':
                #block_num = msg['FOOT']
                byte_data = binascii.unhexlify(body.encode('utf-8'))
                block = BlockVO.BlockVO(file_hash=self.peer.file_hash, file_path=self.file_path, block_num=block_num,
                                        block_data=byte_data)

                fm.insert_block(block)

                msg_dict = self.create_dict('ASK', 'ASK')
                self.send_msg(msg_dict)

            elif head == 'REQ':
                self.send_block(my_block_list, body)
                msg_dict = self.create_dict('QUIT', 'QUIT')
                self.send_msg(msg_dict)
                break
            elif head == 'QUIT':
                msg_dict = self.create_dict('QUIT', 'QUIT')
                self.send_msg(msg_dict)

                fm.request_write_blocks()

                quit_flag = self.request_to_dht()
                if quit_flag is True:
                    break
            else:
                status, body = self.get_status()
                self.send_status(status, body)

    def request_to_dht(self):
        from PeerPack import core

        quit_flag = True
        status = self.get_status()
        if status != 'COMPLETE_PHASE':
            core.server.connect_to_dht(msg='get_peers', file_hash=self.peer.file_hash)
            quit_flag = False
        else:
            core.server.connect_to_dht(msg='add_peer', file_hash=self.peer.file_hash)
        return quit_flag

    def send_block(self, my_block_list, request_block_list):
        send_block_list = []

        for i in range(request_block_list.__len__()):
            if my_block_list.__contains__(request_block_list[i]):
                send_block_list.append(request_block_list[i])
        send_block_list = self.choice_block(send_block_list)

        for i in range(send_block_list.__len__()):
            from PeerPack import fm
            byte_data = fm.read_block_data(self.file_path, send_block_list[i])
            hex_data = binascii.hexlify(byte_data)
            str_data = hex_data.decode('utf-8')
            block_dict = self.create_dict('BLOCK', str_data, send_block_list[i])
            self.send_msg(block_dict)

    def choice_block(self, request_block_list):
        request_list = []
        try:
            for i in range(10):
                data = request_block_list.pop(random.choice(request_block_list))
                request_list.append(data)
        except Exception as e:
            print(e)
        return request_list

    def decode_msg(self, msg):
        msg = msg.decode('utf-8')
        file_dict = json.loads(msg)
        block_num = -1
        if file_dict['HEAD'] == 'BLOCK':
            block_num = file_dict['FOOT']
        return file_dict['HEAD'], file_dict['BODY'], block_num

    def create_dict(self, head, body, foot=None):
        msg_dict = {
            'HEAD': head,
            'BODY': body
        }
        if foot is not None:
            msg_dict['FOOT'] = foot
        return msg_dict