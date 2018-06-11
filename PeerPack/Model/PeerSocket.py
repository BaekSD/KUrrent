import hashlib

file_list = []

class PeerSocket:

    def get_file(self, ip, port, hash):
        self.ip = ip
        self.port = port
        self.hash = hash

    def trans_file(self, ip, port, hash):
        for x in file_list:
            pass
        pass
