import random, json, binascii, time
from PeerPack import DBManager
class PeerModule:
    def __init__(self, sock, file_hash):#, last_index, file_path):
        self.sock = sock
        self.file_hash = file_hash
        self.db = DBManager.DBManager()
        self.file_path, self.last_index = self.db.get_file_data(self.file_hash)

    def choice_block(self, send_block_list):
        send_list = []
        try:
            for i in range(10):
                block_num = random.choice(send_block_list)
                send_list.append(block_num)
                send_block_list.remove(block_num)
        except Exception as e:
            print(e)
        return send_list

    def create_dict(self, head, body, foot=None):
        msg_dict = {
            'HEAD': head,
            'BODY': body
        }
        if foot is not None:
            msg_dict['FOOT'] = foot
        return msg_dict

    def decode_msg(self, msg):
        msg = msg.decode('utf-8')
        file_dict = json.loads(msg)
        block_num = -1
        if file_dict['HEAD'] == 'BLOCK':
            block_num = file_dict['FOOT']
        return file_dict['HEAD'], file_dict['BODY'], block_num

    def get_status(self):
        block_list = self.db.get_blocks(self.file_hash)

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

    def send_msg(self, msg):
        print('Send'+str(msg))
        msg = json.dumps(msg)
        msg = msg.encode('utf-8')
        self.sock.send(msg)

    def get_msg(self, buf_size=20000):
        msg = self.sock.recv(buf_size)
        print('Receive' + str(msg) + str(msg.__sizeof__()))
        return msg

    def get_needed_blocks(self):
        block_list = self.db.get_blocks(self.file_hash)
        request_list = []
        for i in range(self.last_index):
            if not block_list.__contains__(i + 1):
                request_list.append(i + 1)
        return request_list

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
            byte_data = fm.read_block_data(self.file_path, send_block_list[i])
            hex_data = binascii.hexlify(byte_data)
            str_data = hex_data.decode('utf-8')
            block_dict = self.create_dict('BLOCK', str_data, int(send_block_list[i]))
            self.send_msg(block_dict)


        finish_dict = self.create_dict('FINISH', 'FINISH')
        self.send_msg(finish_dict)

