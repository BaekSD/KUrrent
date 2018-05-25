import requests
from collections import namedtuple

class Connect2Tracker:

    def __init__(self):
        ip = "http://127.0.0.1"
        port = "6000"
        self.baseURL = ip + ":" + port

    def get_peer_list(self):
        resp = requests.get(self.baseURL+'/peerList')
        data = resp.json()
        user = namedtuple("User", data.keys())(*data.values())

        '''
        http://dgkim5360.tistory.com/entry/python-requests
        
        
        resp = requests.post('http://www.mywebsite.com/user')
        resp = requests.put('http://www.mywebsite.com/user/put')
        resp = requests.delete('http://www.mywebsite.com/user/delete')

        res.json() # json response일 경우 딕셔너리 타입으로 바로 변환

        userdata = {"firstname": "John", "lastname": "Doe", "password": "jdoe123"}
        resp = requests.post('http://www.mywebsite.com/user', data=userdata)
        '''