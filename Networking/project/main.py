import socket 
import os
import threading as thread
from time import sleep 



class communication():
    def __init__(self) -> None:
        #The protocol and parameter of system.
        print("****** CODEST ******\nWelcome...\nThis application support communicaiton based on pv4 and the port determined by users must be valid for TCP\n\n")
        self.Server_Hostname = socket.gethostname()
        self.Server_IP = socket.gethostbyname(self.Server_Hostname)
        self.ip_v4 = socket.AF_INET
        self.tcp = socket.SOCK_STREAM
        self.numberConnected = 0    
        self.command = []
        self.currentCommand = "Goon"
    def devicesConfig(self):
        print(f"Hostname:{self.Server_Hostname}")
        print(f"IP:{self.Server_IP}")
    def TakePort(self):
        self.startPort = input("The value of port is recomended 6000-7000\nThe start port value:")
        print("port value is taken")
    def mainAcceptor(self,database):
        print("server started")
        self.socketObject = socket.socket(self.ip_v4,self.tcp)
        self.socketObject.bind((self.Server_IP,int(self.startPort)))
        self.socketObject.listen(10)
        while True:
            sleep(2)
            if "kill" in self.currentCommand.lower():
                break
            print("waiting for client")
            self.client , self.address =self.socketObject.accept()
            if "kill" in self.currentCommand.lower():
                break
            self.numberConnected += 1
            database.append({self.address[0]:[self.client,self.address]})
            a=thread.Thread(target=self.clientReader, args=(self.currentCommand,))
            a.start()
        self.socketObject.close()
    def clientReader(self,command):
        client = self.client
        address = self.address
        while True:
            try:
                client.send(b"ping")
            except:
                print("client is closed")
                break
            data = client.recv(1024)
            command = data.decode()
            self.currentCommand = command
            self.command.append({str(address):data.decode()})
            print(f"from {address} :" + data.decode())
            if data.decode().lower() == "quit" or data.decode().lower() == "kill":
                break
        








class DeviceSet():
    def __init__(self) -> None:
        # This arrat is for keeping the information of devices. The structure of array is list:[Dictionary:{IP:SocketObject},...]
        self.Devices = []
    def delete(self,deviceIP):
        if len(self.Devices) == 0:
            print("The devices is connected currently is not existed...")
        else:
            # Delete Code Here.
            pass












if __name__ =="__main__":
    #test procedure
    database = DeviceSet()
    server = communication()
    server.devicesConfig()
    server.TakePort()
    server.mainAcceptor(database.Devices)
    print(server.command)
