import tkinter as tk
import customtkinter
from tkinter import filedialog
from pytube import YouTube
from PIL import Image,ImageTk
from urllib.request import urlopen
from pip import main
import ctypes
import datetime
import threading

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) #ekran cozunurlugunu aliyorum
width = screensize[0]
height = screensize[1]


class App(customtkinter.CTk):
    def __init__(self):
        """
        Programın tüm widgetleri ve widgetlerin yerleri burada tanımlanıyor.

        Tek bir frame kullandim ve hepsini ayni grid sistemine atadim

        """
        super().__init__()

        self.geometry(f"{int(width*0.6)}x{int(height*0.34)}") #uygulama boyutunun sabit olmasi icin
        self.title("Youtube Downloader")

        topFrame = customtkinter.CTkFrame(master=self)
        topFrame.grid(row=0,column=0)

        topFrame.grid_rowconfigure(9) #layout 10x10
        topFrame.grid_columnconfigure(9)

        self.optionsLabel = customtkinter.CTkLabel(master=topFrame,text="Options",height=35)
        self.optionsLabel.grid(row=0,column=0,columnspan=3)

        self.emptyLabel = customtkinter.CTkLabel(master=topFrame,text="")
        self.emptyLabel.grid(row=1)

        self.filePathLabel = customtkinter.CTkLabel(master=topFrame,text = "Filepath")
        self.filePathLabel.grid(row=2,column=0,columnspan=3)

        self.filePathText = tk.Entry(master=topFrame,disabledforeground = "silver",width = 70,state="normal",disabledbackground="#333333")
        self.filePathText.grid(row=3,column=0,columnspan=2)
        self.filePathText.insert(0,"Filepath for downloaded videos"); self.filePathText.config(state="disabled")

        filePathButton = customtkinter.CTkButton(master=topFrame,text="Set File Path",command=self.selectFilePath)
        filePathButton.grid(row=3,column=2)

        self.resValue= tk.IntVar(value=0) #Radiobuttonlarin ortak olmasi icin ayni degere atama

        customtkinter.CTkLabel(master=topFrame,text="").grid(row=1,rowspan=1,column=3,columnspan=2)
        customtkinter.CTkLabel(master=topFrame,text="URL",height=42).grid(row=0,column=3,columnspan=2)


        self.urlText = tk.Entry(master=topFrame,bg = "#333333",fg = "silver",width = 97)
        self.urlText.grid(row=2,column=3,columnspan=2)
        searchButton = customtkinter.CTkButton(master=topFrame,text="Select Video",command=self.selectVideo).grid(row=3,column=3)

        self.videoLabel = customtkinter.CTkLabel(master=topFrame,text="")
        self.videoLabel.grid(row=4,column=3,columnspan=2)
        self.emptyLabel=customtkinter.CTkLabel(master=topFrame,text="Video Quality").grid(row=5,column=3,columnspan=2)
        """
        Su anda yalnizca video indirme secenekleri var yakin zamanda mp3 seceneklerini de ekleyecegim
        """
        self.p144RadioButton = customtkinter.CTkRadioButton(value=17,command=self.getVideoSize,master=topFrame,text="144p         ",state="disabled",variable = self.resValue)
        self.p144RadioButton.grid(row=6,column=3,columnspan=2)

        self.p240RadioButton = customtkinter.CTkRadioButton(value=133,command=self.getVideoSize,master=topFrame,text="240p         ",state="disabled",variable = self.resValue)
        self.p240RadioButton.grid(row=7,column=3,columnspan=2)

        self.p360RadioButton = customtkinter.CTkRadioButton(master=topFrame,command=self.getVideoSize,value=18,text="360p         ",state="disabled",variable = self.resValue)
        self.p360RadioButton.grid(row=8,column=3,columnspan=2)

        self.p480RadioButton = customtkinter.CTkRadioButton(master=topFrame,command=self.getVideoSize,value=135,text="480p         ",state="disabled",variable = self.resValue)
        self.p480RadioButton.grid(row=9,column=3,columnspan=2)

        self.p72030RadioButton = customtkinter.CTkRadioButton(master=topFrame,command=self.getVideoSize,value=22,text="720p/30f  ",state="disabled",variable = self.resValue)
        self.p72030RadioButton.grid(row=10,column=3,columnspan=2)

        self.p72060RadioButton = customtkinter.CTkRadioButton(master=topFrame,command=self.getVideoSize,value=298,text="720p/60f  ",state="disabled",variable = self.resValue)
        self.p72060RadioButton.grid(row=11,column=3,columnspan=2)

        self.p1080RadioButton = customtkinter.CTkRadioButton(master=topFrame,command=self.getVideoSize,value=299,text="1080p/60f",state="disabled",variable = self.resValue)
        self.p1080RadioButton.grid(row=12,column=3,columnspan=2)

        self.downloadButton = customtkinter.CTkButton(master=topFrame,text="Download Video",state="disabled",command=self.downloadVideo)
        self.downloadButton.grid(row=3,column=4)

        self.downloadProgressBar = customtkinter.CTkProgressBar(master=topFrame,width=400)
        self.downloadProgressBar.set(0)
        self.downloadProgressBar.grid(row=7,column=0,columnspan=2)
        self.downloadLabel = customtkinter.CTkLabel(master=topFrame,text="0MB/0MB")
        self.downloadLabel.grid(row=7,column=2)

    def selectFilePath(self):
        """
        Butona atanan komut:
        Kullanicidan videolari indirecegi klasoru secmesini istiyor ve bunu bir string degerine atiyor
        """
        self.filename = filedialog.askdirectory()
        self.filePathText.config(state = "normal")
        self.filePathText.delete(0,"end")
        self.filePathText.insert(0, self.filename)
        self.filePathText.config(state="disabled")

    def selectVideo(self):
        """
        URL kismina yazilan urlden "pytube" modulu ile videoyu bulmak ve video cozunurluk degerlerine gore gerekli radiobuttonlari acmak icin kullaniliyor
        """
        urlpaste = self.urlText.get()
        self.ytvideo = YouTube(urlpaste, on_progress_callback=self.progress_func) #urlpaste video url'si, on_progress_callback ise indirme sirasinda fonksiyon calistirmaya yariyor
        videoTitle = self.ytvideo.title
        videoLength = self.ytvideo.length
        a = datetime.timedelta(seconds=videoLength) #video uzunlugunu saniyeden HH:MM:SS cinsine cevirme
        self.videoLabel.configure(text=f"Video Title= {videoTitle}\n \nVideo Length= {a}")

        self.p144RadioButton.configure(state="disabled") #once tum radiobuttonlari devre disi birakiyorum
        self.p240RadioButton.configure(state="disabled") #boylece yeni video eklendiginde yeni cozunurluge gore ayar yapilabilir
        self.p360RadioButton.configure(state="disabled")
        self.p480RadioButton.configure(state="disabled")
        self.p72030RadioButton.configure(state="disabled")
        self.p72060RadioButton.configure(state="disabled")
        self.p1080RadioButton.configure(state="disabled")


        self.downloadButton.configure(state="normal") #indirme butonunu aktiflestirme
        """
        modul tum cozunurlukleri bir listeye atiyor
        bu listeyi okuyup gerekli radiobuttonlari aciyorum
        """
        for i in self.ytvideo.streams:
            if i.itag == 17:
                self.p144RadioButton.configure(state="normal")
            elif i.itag == 133:
                self.p240RadioButton.configure(state="normal")
            elif i.itag == 18:
                self.p360RadioButton.configure(state="normal")
            elif i.itag == 135:
                self.p480RadioButton.configure(state="normal")
            elif i.itag == 22:
                self.p72030RadioButton.configure(state="normal")
            elif i.itag == 298:
                self.p72060RadioButton.configure(state="normal")
            elif i.itag == 299:
                self.p1080RadioButton.configure(state="normal")

    def downloadVideo(self): #secilen cozunurlukte videoyu indirme
        x = threading.Thread(target=self.threadDownloadVideo)
        x.start() #thread kullanmamin sebebi kullanilmazsa video inerken baska bir islem yapmak mumkun olmuyor

    def threadDownloadVideo(self):  #radiobutton degerini okuyup videoyu indirme
        self.itagValue = self.resValue.get()
        self.filePath = self.filename
        self.stream = self.ytvideo.streams.get_by_itag(self.resValue.get())
        self.stream.download(output_path=self.filePath)

    def getVideoSize(self):  #videonun boyutunu almak ve bunu mb cinsinden yazmak icin
        self.itagValue2 = self.resValue.get()
        self.stream2 = self.ytvideo.streams.get_by_itag(self.itagValue2)
        self.videoFileSize = self.stream2.filesize
        self.mbFileSize = "{:.2f}".format(self.videoFileSize/(1024*1024))
        self.downloadLabel.configure(text=f"0MB/{self.mbFileSize}MB")
        self.downloadProgressBar.set(0)

    def progress_func(self,stream, chunk, bytes_remaining):
        """
        Videoyu indirirken ne kadarının indirildiğini ve ne kadar kaldığını göstermeye yarayan fonksiyon
        """
        self.downloadedPart = ("{:.2f}".format((self.stream.filesize-bytes_remaining)/(1024*1024))) # kaç byte indirildi ve bunu 2 decimal'li floata cevirme
        self.barProgress = float(self.downloadedPart) / float(self.mbFileSize) #Progress bar'a 0-1 arası deger girmek icin oran hesabı
        self.downloadProgressBar.set(self.barProgress) #Progress bar deger atama
        self.downloadLabel.configure(text= f"{self.downloadedPart}MB / {self.mbFileSize}MB ") #Progress bar yanındaki label'de yazılı kalan mb hesabı




app = App()
app.mainloop()
