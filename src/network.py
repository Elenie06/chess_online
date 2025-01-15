import socket
import pickle

#gère la connection entre le serveur et le client

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.18.41.148"
        self.port = 5555
        self.address = (self.server, self.port)
        self.player = self.connect()

    def get_p(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data) :
        try :
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4096*16))
        except socket.error as err :
            print(err)
