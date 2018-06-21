import threading
import socket

class ClientThread(threading.Thread):

    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.connect_to_server(ip, port)

    def connect_to_server(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        print('ClientThread connect complete')

