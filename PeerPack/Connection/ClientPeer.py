import socket, threading, json, binascii
from PeerPack.Model import BlockVO
from PeerPack.Connection.PeerModule import PeerModule as peer_module


class ClientPeer(threading.Thread, peer_module):
    def __init__(self, peer):
        threading.Thread.__init__(self)
        self.client_socket = self.connect_to_peer(peer)
        peer_module.__init__(self, sock=self.client_socket, file_hash=peer.file_hash)  #

    def connect_to_peer(self, peer):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(None)
        client_socket.connect((peer.ip, peer.port))
        return client_socket

    def run(self):
        peer_dict = self.create_dict('PEER', self.file_hash)
        self.send_msg(peer_dict)
        status, body = self.get_status()
        if status != 'COMPLETE_PHASE':
            self.recv_msg()
        else:
            msg_dict = self.create_dict('QUIT', 'QUIT')
            self.send_msg(msg_dict)

    def send_status(self, status, body):
        request_dict = self.create_dict(status, body)
        self.send_msg(request_dict)

    def recv_msg(self):
        from PeerPack import fm, db

        while True:
            try:
                msg = self.get_msg(20000)
                head, body, block_num = self.decode_msg(msg)

                my_block_list = db.get_blocks(self.file_hash)

                if head == 'BLOCK':
                    # block_num = msg['FOOT']
                    byte_data = binascii.unhexlify(body.encode('utf-8'))
                    block = BlockVO.BlockVO(file_hash=self.file_hash, file_path=self.file_path, block_num=block_num,
                                            block_data=byte_data)
                    fm.insert_block(block)

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
                elif head == 'FINISH':
                    msg_dict = self.create_dict('ASK', 'ASK')
                    self.send_msg(msg_dict)
                else:
                    status, body = self.get_status()
                    self.send_status(status, body)
            except Exception as e:
                print('error' + str(e))
                break

    def request_to_dht(self):
        from PeerPack import core

        quit_flag = True
        status, body = self.get_status()
        if status != 'COMPLETE_PHASE':
            core.server.connect_to_dht(request='get_peers', file_hash=self.file_hash)
            quit_flag = False
        else:
            core.server.connect_to_dht(request='add_peer', file_hash=self.file_hash)
        return quit_flag
