import threading
import socket
import json
from PeerPack.Model import PeerSocket

class ServerThread(threading.Thread):

    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))

    def wait_for_client(self):
        self.server_socket.listen(5)
        client_socket, addr = self.server_socket.accept()
        peer_socket = PeerSocket.PeerSocket(client_socket)
        return peer_socket

    def run(self):
        while True:
            peer_socket = self.wait_for_client()
            peer_socket.start()