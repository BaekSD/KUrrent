from Thread import ClientThread, ServerThread


class Peer:

    def __init__(self):
        self.port = 8099
        self.host = "127.0.0.1"
        self.baseURL = "http://127.0.0.1:5000"

    def wait_client(self):
        server_thread = ServerThread.ServerThread(self.host, self.port)
        server_thread.start()

    def access_server(self):
        client_thread = ClientThread.ClientThread(self.host, self.port)
        client_thread.start()

