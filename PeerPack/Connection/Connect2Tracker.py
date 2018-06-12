import requests
from collections import namedtuple

class Connect2Tracker:

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = "8090"
        self.baseURL = self.ip + ":" + self.port

    def get_peer_list(self):
        resp = requests.get(self.baseURL+'/peerList')
        data = resp.json()
        user = namedtuple("User", data.keys())(*data.values())

    def add_request(self, tracker, file_hash):
        domain = tracker + "/download_request"
        peer_dict = {
            'ip': self.ip,
            'port': self.port,
            'hash':file_hash
        }
        res = requests.post(url=domain, data=peer_dict)
        data = res.json()
        client_ip = data.get('ip')

    def add_seeder_request(self, tracker, file_hash):
        domain = tracker + "/add_seeder_request"
        peer_dict = {
            'ip': self.ip,
            'port': self.port,
            'hash': file_hash
        }
        res = requests.post(url=domain, data=peer_dict)
        data = res.json()
        client_ip = data.get('ip')

        '''
        http://dgkim5360.tistory.com/entry/python-requests
        
        
        resp = requests.post('http://www.mywebsite.com/user')
        resp = requests.put('http://www.mywebsite.com/user/put')
        resp = requests.delete('http://www.mywebsite.com/user/delete')

        res.json() # json response일 경우 딕셔너리 타입으로 바로 변환

        userdata = {"firstname": "John", "lastname": "Doe", "password": "jdoe123"}
        resp = requests.post('http://www.mywebsite.com/user', data=userdata)
        '''