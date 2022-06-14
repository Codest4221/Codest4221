from pydoc import cli
import tkinter as tk
from tkinter import ttk
import cv2 as cv
import socket as con
import os 
import sys
import threading as thr
from PIL import ImageTk, Image
import datetime
import mediapipe as mp
import struct
import customtkinter as ctk
import numpy as np
import socket as soc
import pickle

class VoiceA():


    def __init__(self) -> None:
        self.codest = cv.imread("codest.png",1)
        #self.codest = cv.cvtColor(self.codest,cv.COLOR_BGR2RGBA)
        self.localHostname = soc.gethostname()
        self.localIP = soc.gethostbyname(self.localHostname)
        self.addressFamily = soc.AF_INET
        self.protocol = soc.SOCK_STREAM
        self.encodelist =  [int(cv.IMWRITE_JPEG_QUALITY), 90]
        self.localPort = 80
        self.GUIobeject = tk.Tk()
        self.GUIobeject.attributes('-fullscreen', True)
        self.cameraLivesValue = 1
        self.mainimage = None
        self.client = None
        self.clientIP = None
        self.clientPort = None
        self.imgsaved = None
        self.i = 30
        self.NumberOfSavedImage = 0
    def cameraLives(self):
        self.cameraLivesValue = 0
    def serverAcceptor(self):
    # In this function is acceptor function. In other words, the server accept each client which try to connect.
        # Accept client 
        try:
            client , address = self.serverSocket.accept()
            self.client = client
            self.clientIP = address[0]
            self.clientPort = address[1]
        # If client is connected succesfully, the array below is returned.
            self.history.insert(tk.END,f"The client {address[0]} with port {address[1]} is connected succesfully.\n")
            return 1
        except:
            self.history.insert(tk.END,"The server socket can be broken\n")
            return 0
    def loopAcceptorThread(self):
    # This is fucntion to parellel executing. In other words, the accept fucntion is waiting until client connection. To continue program with acceptor, the thread method is used. 
        self.loopfunction = thr.Thread(target=self.serverAcceptor)
        self.loopfunction.start()
    def build(self):
        self.entry1 = tk.Entry(self.GUIobeject,textvariable=self.localIP)
        self.entry1.insert(tk.END,"IP")
        self.entry1.place(x=400,y=800)
        self.entry2 = tk.Entry(self.GUIobeject,textvariable=self.localPort)
        self.entry2.insert(tk.END,"port")
        self.entry2.place(x=550,y=800)
        self.history = tk.Text(self.GUIobeject, height = 10, width = 60)
        self.history.place(x=400,y=620)
        Button1 = tk.Button(self.GUIobeject,text="Close App",command=self.GUIobeject.destroy,height=2,width=10)
        Button1.place(x=1400,y=50)
        Button7 = tk.Button(self.GUIobeject,text="Initiliaze",command=self.serverInitializer,height=1,width=10)
        Button7.place(x=700,y=800)
        Button8 = tk.Button(self.GUIobeject,text="Accept",command=self.loopAcceptorThread,height=1,width=10)
        Button8.place(x=800,y=800)
        Button2 = tk.Button(self.GUIobeject,text="Close Camera",command=self.cameraLives,height=2,width=10)
        Button2.place(x=150,y=650)
        Button3 = tk.Button(self.GUIobeject,text="Take Photo",command=self.saver,height=2,width=10)
        Button3.place(x=50,y=650)
        Button4 = tk.Button(self.GUIobeject,text="Open Camera",command=self.cameraOpener,height=2,width=10)
        Button4.place(x=250,y=650)
        Button5 = tk.Button(self.GUIobeject,text="Send",command=self.sender,height=2,width=10)
        Button5.place(x=1200,y=50)
        Button5 = tk.Button(self.GUIobeject,text="Delete",command=self.deleter,height=2,width=10)
        Button5.place(x=1300,y=50)
        Button6 = tk.Button(self.GUIobeject,text="show",command=self.shower,height=2,width=10)
        Button6.place(x=1100,y=50)
        self.treeview = ttk.Treeview(self.GUIobeject,columns=(1, 2, 3), show='headings', height=35)
        self.treeview.place(y=100,x=900)
        self.treeview.heading(1, text='PhotoID')
        self.treeview.heading(2, text='Date')
        self.treeview.heading(3, text='Photo Type')
        verscrlbar = ttk.Scrollbar(self.GUIobeject, orient ="vertical",command = self.treeview.yview)
        verscrlbar.place(x=1500,y=400)
        self.label1 = tk.Label(self.GUIobeject,text="CODEST TEAM")
        self.label1.place(y=20,x=100)
        self.label2 = tk.Label(self.GUIobeject,bd=15)
        self.label2.place(y=100,x=40)
        cv.waitKey(1000)
    def deleter(self):
        self.treeview.delete(self.treeview.selection()[0])
    def sender(self):
        image = self.treeview.item(self.treeview.selection())["values"][0]
        img = cv.imread(image,1)
        result, frame = cv.imencode('.jpg', img, self.encodelist)
        data = pickle.dumps(frame, 0)
        size = len(data)
        self.client.sendall(struct.pack(">L", size) + data)
    def serverInitializer(self)->None:
    # In this function, the server object will be created and published.
        self.localPort = int(self.entry2.get())
        self.localIP = self.entry1.get()
        try:
            # Socket object creation 
            self.serverSocket = soc.socket(self.addressFamily,self.protocol)
            # Diving network
            
            self.serverSocket.bind((self.localIP,self.localPort))
            self.serverSocket.listen(10)
            # If the function work succesfully, the list below is returned.
            self.history.insert(tk.END,"The server is created succesfully.\n") 
            return 1
        except:
            # Not, this
            self.history.insert(tk.END,"The server cannot be created.\n") 
            return 0
    def shower(self):
        image = self.treeview.item(self.treeview.selection())["values"][0]
        image = cv.imread(image)
        cv.imshow("Window",image)
        cv.waitKey(0)
    def handCapturer(self):
        cv.waitKey(10000)
        mpHands = mp.solutions.hands
        hands = mpHands.Hands()
        point = {}
        pointlist = []
        oldarea = 0
        while self.cap.isOpened():
            if self.i != -1:
                self.i = self.i -1
            success, image = self.cap.read()
            imageRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            results = hands.process(imageRGB)
            # checking whether a hand is detected
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks: # working with each hand
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        if id == 20 or id == 16 or id == 12 or id == 8 or id == 4 or id == 0 :
                            point[id] = [cx,cy]
                            pointlist.append((cx,cy))
            if len(pointlist) != 0:
                area = cv.contourArea(np.array(pointlist))
                if area < oldarea/10:
                    self.i = 30
                oldarea = area
            if self.i == 0:
                self.saver()
                self.i = self.i -1
            point = {}
            pointlist = []
            if self.cameraLivesValue == 0:
                break
    def saver(self):
        imagename = "Images/Codest-"+"IMGID  "+ str(self.NumberOfSavedImage)+ ".png"
        self.imgsaved.save(imagename)
        self.NumberOfSavedImage = self.NumberOfSavedImage + 1
        self.treeview.insert(parent='', text='',index="end" ,values=(imagename,datetime.datetime.now(),imagename.split()[1]))
        self.treeview.update()
    def updater(self):
        pass
    def camera(self):
        self.cameraLivesValue = 1
        self.cap = cv.VideoCapture(cv.CAP_DSHOW)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            frame[-self.codest.shape[0]:,-self.codest.shape[1]:] = self.codest 
            cv.putText(frame,str(self.i),(50,50),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
            cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            self.imgsaved = img
            imgtk = ImageTk.PhotoImage(image=img)
            self.label2.configure(image=imgtk)
            self.label2.update
            self.mainimage = imgtk
            if self.cameraLivesValue == 0:
                break
        self.cap.release()    
    def destroy(self):
        self.GUIobeject.mainloop()
    def cameraOpener(self):
        cameraFunction = thr.Thread(target=self.camera)
        cameraFunction.start()
        #updatefeature = thr.Thread(target=self.updater)
        #updatefeature.start()
        handcapture = thr.Thread(target=self.handCapturer)
        handcapture.start()






if __name__ == "__main__":
    app = VoiceA()
    app.build()
    app.destroy()
