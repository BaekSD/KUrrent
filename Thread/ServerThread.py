import threading
import socket


class ServerThread(threading.Thread):

    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((ip, port))
        self.wait_for_client()

    def wait_for_client(self):
        self.serverSocket.listen(1)
        self.client_socket, self.addr = self.serverSocket.accept()
        print('ServerThread wait_client Complete')
