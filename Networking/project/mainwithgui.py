import os 
import tkinter as tk
from tkinter import ttk
import socket as soc 
import threading as thread 


class userInterface():
    def __init__(self) -> None:
        self.GUIobeject = tk.Tk()
        self.GUIobeject.geometry("400x800")
        self.Server_Hostname = soc.gethostname()
        self.Server_IP = soc.gethostbyname(self.Server_Hostname)
        self.ip_v4 = soc.AF_INET
        self.tcp = soc.SOCK_STREAM
        self.numberConnected = 0    
        self.command = []
    def acceptor(self):
        self.client , self.address =self.serverSocket.accept()
        self.history.insert(tk.END,f"{self.address} is connected succesfully\n")
        a=thread.Thread(target=self.clientReader)
        a.start()
    def clientReader(self):
            client = self.client
            address = self.address
            while True:
                try:
                    client.send(b"ping")
                except:
                    print("client is closed")
                    break
                data = client.recv(1024)
                self.messageBox.insert(tk.END,(f"from {address} :" + data.decode()+"\n"))
                if data.decode().lower() == "quit" or data.decode().lower() == "kill":
                    break
    def acceptorRunner(self):
        a=thread.Thread(target=self.acceptor)
        a.start()
    def network_dive(self)-> None:
        self.serverSocket = soc.socket(self.ip_v4,self.tcp)
        self.serverSocket.bind((self.entry1.get(),int(self.entry2.get())))
        self.serverSocket.listen(10)
        self.history.insert(tk.END,"The socket Object is created succesfully.\n")
    def built(self):
        Button1 = tk.Button(self.GUIobeject,text="Accept",command=self.acceptorRunner,height=2,width=8)
        Button1.place(x=200,y=50)
        Button2 = tk.Button(self.GUIobeject,text="Create",command=self.network_dive,height=2,width=8)
        Button2.place(x=10,y=10)
        self.IP = tk.StringVar()
        self.port = tk.StringVar()
        label1 = tk.Label(self.GUIobeject,text="Message Box").place(y=120,x=180)
        label2 = tk.Label(self.GUIobeject,text="History").place(y=520,x=180)
        self.entry1 = tk.Entry(self.GUIobeject,textvariable=self.IP)
        self.entry1.insert(tk.END,"IP")
        self.entry1.place(x=100,y=10)
        self.entry2 = tk.Entry(self.GUIobeject,textvariable=self.port)
        self.entry2.insert(tk.END,"port")
        self.entry2.place(x=250,y=10)
        self.history = tk.Text(self.GUIobeject, height = 15, width = 42)
        self.history.place(x=30,y=550)
        self.messageBox = tk.Text(self.GUIobeject, height = 22, width = 42)
        self.messageBox.place(x=30,y=150)
    def destroy(self):
        self.GUIobeject.mainloop()



if __name__ == "__main__":
    GUI = userInterface()
    GUI.built()
    GUI.destroy()