import threading, json
import binascii, time
from PeerPack.Model import BlockVO
from PeerPack.Connection.PeerModule import PeerModule as peer_module


class ServerPeer(threading.Thread, peer_module):
    def __init__(self, client_socket, file_hash):
        threading.Thread.__init__(self)
        peer_module.__init__(self, sock=client_socket, file_hash=file_hash)

    def run(self):
        conn_dict = self.create_dict('CONN', 'SUCCESS')
        self.send_msg(conn_dict)
        self.recv_msg()
        print('============================ Close Peer =========================')

    def recv_msg(self):
        from PeerPack import fm, db, core
        while True:
            try:
                msg = self.get_msg(20000)
                print('Receive' + str(msg))

                head, body, block_num = self.decode_msg(msg)

                my_block_list = db.get_blocks(self.file_hash)

                if head == 'BOOTSTRAP_PHASE':
                    self.send_block(my_block_list)
                elif head == 'DOWNLOAD_PHASE':
                    self.send_block(my_block_list, body)
                elif head == 'LAST_PHASE':
                    self.send_block(my_block_list, body)
                elif head == 'COMPLETE_PHASE':
                    break
                elif head == 'ASK':
                    phase, request_block = self.get_status()
                    if phase != 'COMPLETE_PHASE':
                        msg_dict = self.create_dict('REQ', request_block)
                    else:
                        msg_dict = self.create_dict('QUIT', 'QUIT')
                        core.server.connect_to_dht(request='add_peer', file_hash=self.file_hash)

                    self.send_msg(msg_dict)

                elif head == 'BLOCK':
                    block_num = msg['FOOT']
                    byte_data = binascii.unhexlify(body.encode('utf-8'))
                    block = BlockVO.BlockVO(file_hash=self.file_hash, file_path=self.file_path, block_num=block_num,
                                            block_data=byte_data)
                    fm.insert_block(block)
                elif head == 'QUIT':
                    fm.request_write_blocks()
                    break
            except Exception as e:
                print(e)
                break

