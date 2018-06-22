import socket, threading
import json
from PeerPack import db
from . import FileManager

class PeerSocket(threading.Thread):
    def __init__(self, peer):
        threading.Thread.__init__(self)
        self.peer = peer
        self.list1 = []
        self.lock = threading.Lock()

    def connect_to_peer(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.peer.ip, self.peer.port))
        return client_socket

    def run(self):
        self.client_socket = self.connect_to_peer()

        recv_th = threading.Thread(target=self.recv_block)
        recv_th.daemon = False
        recv_th.start()

        while True:
            # Send File Blocks in here
            pass

    def send_block(self, msg):
        msg = json.dumps(msg)
        msg = msg.encode('utf-8')
        self.client_socket.send(msg)

    def recv_block(self, buf_size=8192):

        while True:
            msg = self.client_socket.recv(buf_size)
            file_hash, block_num, file_block = self.decode_block(msg)

            if block_num < 0:
                break
            else:
                # We Have To Do Here
                file_manager = FileManager.FileManager(block_num, file_block)
                self.lock.aquire()
                file_manager.save_file()
                db.put_block_info(file_hash, block_num)
                self.lock.release()
                pass

    def decode_block(self, msg):
        msg = msg.decode('utf-8')
        file_dict = json.loads(msg)

        file_hash = file_dict.get('file_hash')
        block_num = file_dict.get('block_num')
        file_block = file_dict.get('file_block')
        return file_hash, block_num, file_block
    '''

    def __init__(self, ip='127.0.0.1', port=7777, core=None):
        self.ip = ip
        self.port = port
        self.core = core
        self.sock_th = threading.Thread(target=self.run_a_sock)
        self.sock_th.daemon = True
        self.sock_th.start()
        self.comm_th = threading.Thread(target=self.run_request)
        self.comm_th.daemon = True
        self.comm_th.start()
    '''
    def request_have(self, ip, port, hash, file_name, piece_num):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.send("have".encode())
            s.send(hash.encode())
            s.send(file_name.endcode())
            s.send(piece_num.encode())
            result = s.recv(1024).decode()
            return bool(result)

    def request_piece(self, ip, port, hash, file_name, piece_num):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.send("piece".encode())
            s.send(hash.encode())
            s.send(file_name.endcode())
            s.send(piece_num.encode())
            piece = s.recv(1024)
            return piece

    def request_keep_alive(self, ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.send("keep_alive".encode())
            hi = s.recv(1024)
            if hi:
                return True
            else:
                return False

    def response_have(self, conn):
        hash = conn.recv(1024).decode()
        file_name = conn.recv(1024).decode()
        piece_num = conn.recv(1024).decode()

        result = self.core.piece_exist(hash, file_name, piece_num)
        conn.send(str(result).encode())
        conn.close()

    def response_piece(self, conn):
        hash = conn.recv(1024).decode()
        file_name = conn.recv(1024).decode()
        piece_num = conn.recv(1024).decode()

        piece = self.core.get_piece(hash, file_name, piece_num)
        conn.send(piece)
        conn.close()

    def response_keep_alive(self, conn):
        # check that the peer is online
        conn.send("hi".encode())
        conn.close()

    def run_a_sock(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.port))
            s.listen(5)
            while True:
                conn, addr = s.accept()
                msg = conn.recv(1024).decode()
                if msg == "have":
                    th = threading.Thread(target=self.response_have, args=conn)
                    th.daemon = True
                    th.start()
                elif msg == "piece":
                    th = threading.Thread(target=self.response_piece, args=conn)
                    th.daemon = True
                    th.start()
                elif msg == "keep_alive":
                    th = threading.Thread(target=self.response_keep_alive, args=conn)
                    th.daemon = True
                    th.start()
                else:
                    conn.close()

    def run_request(self):
        while True:
            todo = self.core.get_todolist()
            for i in todo:
                # get todolist from core
                # and to the process
                pass
