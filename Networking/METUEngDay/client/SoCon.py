import socket 



class client():
    def __init__(self,server_ip,port) -> None:
        self.Server_IP = server_ip
        self.server_port = port
        self.ip_v4 = socket.AF_INET
        self.tcp = socket.SOCK_STREAM
    def connect_server(self)->None:
        self.clinetSocket = socket.socket(self.ip_v4,self.tcp)
        print("socket is created")
        self.clinetSocket.connect((self.Server_IP,self.server_port))
    def send_msg(self,msg)->None:
        self.clinetSocket.send(msg.encode())
    def recieve_msg(self)->None:
        data = self.clinetSocket.recv(4096).decode()
        return data
    def destroy(self):
        self.clinetSocket.close()



class server():
    def __init__(self,port) -> None:
        self.Server_Hostname = socket.gethostname()
        self.Server_IP = socket.gethostbyname(self.Server_Hostname)
        self.port = port 
        self.ip_v4 = socket.AF_INET
        self.tcp = socket.SOCK_STREAM
    def network_dive(self)-> None:
        self.serverSocket = socket.socket(self.ip_v4,self.tcp)
        self.serverSocket.bind((self.Server_IP,self.port))
        self.serverSocket.listen()
    def accept_client(self)->None:
        self.client , self.address = self.serverSocket.accept()
        print(f"adress: {self.address} is connected")
        return [{self.address:self.client},self.address]
    def send_msg(self, client, msg) ->None:
        client.send(msg.encode()),
    def recieve_msg(self,client)->None:
        data = client.recv(1024)
        print(data.decode())
        return data.decode()
    def destroy(self):
        self.serverSocket.close()





