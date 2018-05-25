import requests

class Connect2Tracker:

    def __init__(self):
        ip = "http://127.0.0.1"
        port = "6000"
        self.baseURL = ip + ":" + port

    def get_peer_list(self):
        resp = requests.get(self.baseURL+'/peerList')


        '''
        resp = requests.post('http://www.mywebsite.com/user')
        resp = requests.put('http://www.mywebsite.com/user/put')
        resp = requests.delete('http://www.mywebsite.com/user/delete')

        userdata = {"firstname": "John", "lastname": "Doe", "password": "jdoe123"}
        resp = requests.post('http://www.mywebsite.com/user', data=userdata)
        '''