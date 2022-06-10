import socket as soc
import os 
import threading as thr





class communcation():
    def __init__(self) -> None:
    # In this function, the communcation protocol and the constant parameter will be defined.
        # The following parameters are hostname, ip address, address family for communcation and communcation protocol respectively.
        self.localHostname = soc.gethostname()
        self.localIP = soc.gethostbyname(self.localHostname)
        self.addressFamily = soc.AF_INET
        self.protocol = soc.SOCK_STREAM
        self.localPort = 80
        # This is parameter to destroy server acceptor.
        self.loopAcceptorIndicator = 1
            
        self.clientConnected = {}
    def serverInitializer(self,port)->None:
    # In this function, the server object will be created and published.
        self.localPort = port
        try:
            # Socket object creation 
            self.serverSocket = soc.socket(self.addressFamily,self.protocol)
            # Diving network
            self.serverSocket.bind((self.localIP,self.localPort))
            self.serverSocket.listen(10)
            # If the function work succesfully, the list below is returned.
            return [1,"The server is created succesfully."] 
        except:
            # Not, this 
            return[0,"The server cannot be created."]
    def serverAcceptor(self):
    # In this function is acceptor function. In other words, the server accept each client which try to connect.
        # Accept client 
        try:
            client , address = self.serverSocket.accept()
            self.clientConnected[address[0]] = [client,address[0],address[1],[]]
        # If client is connected succesfully, the array below is returned.
            return [1,f"The client {address} with port {address[2]} is connected succesfully."]
        except:
            return[0,"The server socket can be broken"]
    def loopAcceptor(self):
    # This is function to create infinite acceptor. In other words, this is fucntion to accept multiple clients
        while True:
            if self.loopAcceptorIndicator == 0:
                break
        self.serverAcceptor()
        return
    def loopAcceptorThread(self):
    # This is fucntion to parellel executing. In other words, the accept fucntion is waiting until client connection. To continue program with acceptor, the thread method is used. 
        self.loopfunction = thr.Thread(target=self.loopAcceptor)
        self.loopfunction.start()
    def loopAcceptorExist(self):
    # This is function to check the loop function alive.
        return self.loopfunction.is_alive()
    def clientReader(self,IP):
        clientobject = self.clientConnected[IP][0]
        while True:
            try:
                clientobject.send(b"ping")
            except:
                return [0,f"The client {IP} is disconnected"]
            data = clientobject.recv(1024)
            command = data.decode()
            if command == "Quit".lower():
                break
        return [1, f"The client {IP} is disconnected"]
    def clientReaderThread(self,ip):    
    # This is fucntion to parellel executing. 
        self.clientfunction = thr.Thread(target=self.clientReader,args=(ip,))
        self.clientfunction.start()
    def loopAcceptorExist(self):
    # This is function to check the loop function alive.
        return self.clientfunction.is_alive()


