import threading
import socket, json
from PeerPack.Connection import PeerSocket, ClientPeer, ServerPeer
from PeerPack.Model import PeerVO


class ServerThread(threading.Thread):

    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.peers_list = []
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
            if head == 'DHT':
                # Open ClientPeer, Peer Data we got from DHT should be {file_hash:'ip:port'}
                peer_list = self.get_peers(body)
                self.request_to_peer(peer_list)
            elif head == 'PEER':
                # Open Server Peer
                peer = ServerPeer.ServerPeer(client_socket, body)
                peer.start()
            else:
                print('Error')
            # Receive {file_hash:peer_list} from DHT(Master Peer)

            # Start PeerSocket Thread to transfer File Block

    def request_to_peer(self, peer_list):
        for peer in peer_list:
            client_peer = ClientPeer.ClientPeer(peer)
            client_peer.start()
        self.peers_list += peer_list

    def get_peers(self, peer_dict):
        peer_list = []
        for key in peer_dict:
            address_list = peer_dict[key]
            for address in address_list:
                address_arr = address.split(':')
                # IP, PORT, File Hash
                peer = PeerVO.PeerVO(address_arr[0], address_arr[1], key)
                peer_list.append(peer)
        return peer_list

    def recv_msg(self, client_socket, buf_size=8192):
        msg = client_socket.recv(buf_size)
        msg = msg.decode('utf-8')
        msg_dict = json.loads(msg)
        return msg_dict['HEAD'], msg_dict['BODY']
