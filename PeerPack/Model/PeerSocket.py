import socket, threading

class PeerSocket:

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
