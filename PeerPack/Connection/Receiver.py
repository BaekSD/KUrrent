import threading
import socket, json
from PeerPack.Connection import ClientPeer, ServerPeer
from PeerPack.Model import PeerVO


class ServerThread(threading.Thread):

    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.peers_list = []
        self.ip = ip
        self.port = port
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))

    def wait_for_client(self):
        client_socket, addr = self.server_socket.accept()
        return client_socket

    def run(self):
        self.server_socket.listen(5)
        while True:
            # Wait For Peers
            client_socket = self.wait_for_client()
            head, body = self.recv_msg(client_socket)
            print(head, body)
            if head == 'DHT':
                # Open ClientPeer, Peer Data we got from DHT should be {file_hash:'ip:port'}
                peer_list = self.get_peers(body)
                self.request_to_peer(peer_list)
            elif head == 'PEER':
                # Open Server Peer
                peer = ServerPeer.ServerPeer(client_socket, body, self.lock)
                peer.start()
            else:
                print('Error')
            # Receive {file_hash:peer_list} from DHT(Master Peer)


    def request_to_peer(self, peer_list):
        for peer in peer_list:
            client_peer = ClientPeer.ClientPeer(peer, self.lock)
            client_peer.start()
        self.peers_list += peer_list

    def get_peers(self, raw_peer_list):
        peer_list = []
        for key in raw_peer_list:
            file_hash = hex(int(key))[2:]
            for i in range(raw_peer_list[key].__len__()):
                address_arr = raw_peer_list[key][i].split(':')
                # IP, PORT, File Hash

                peer = PeerVO.PeerVO(ip=address_arr[0], port=int(address_arr[1]), file_hash=file_hash)
                peer_list.append(peer)
        return peer_list

    def recv_msg(self, client_socket, buf_size=8192):
        msg = client_socket.recv(buf_size)
        msg = msg.decode('utf-8')
        msg_dict = json.loads(msg)
        return msg_dict['HEAD'], msg_dict['BODY']

    def connect_to_dht(self, request, file_hash, master_ip, master_port):
        msg = request + ',' + file_hash + ',' + str(self.ip) + ',' + str(self.port)
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((master_ip, int(master_port)))
            client_socket.send(msg.encode())
        except Exception as e:
            print(e)
