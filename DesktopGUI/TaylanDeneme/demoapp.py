import tkinter as tk
import customtkinter
import ctypes

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
width = screensize[0]
height = screensize[1]


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry(f"{int(width*0.405)}x{int(height*0.615)}")
        self.title("Demo App")

        topFrame = customtkinter.CTkFrame(master=self)
        topFrame.grid(row=0,column=0)

        self.topEntryLeft = customtkinter.CTkEntry(master=topFrame,width=330)
        self.topEntryLeft.grid(row=0,column=0,padx=20,pady=60)

        self.topEntryRight = customtkinter.CTkEntry(master=topFrame,width=330)
        self.topEntryRight.grid(row=0,column=1,padx=20,pady=60)

        self.leftButton = customtkinter.CTkButton(master=topFrame,text="Button 1")
        self.leftButton.grid(row=1,column=0,padx=20,pady=50)

        self.rightButton = customtkinter.CTkButton(master=topFrame,text="Button 2")
        self.rightButton.grid(row=1,column=1,padx=20,pady=50)

        self.leftTextBox = tk.Text(master=topFrame,bg="#333333",width=48,fg="silver")
        self.leftTextBox.grid(row=2,column=0)

        self.rightTextBox = tk.Text(master=topFrame,bg="#333333",width=48,fg="silver")
        self.rightTextBox.grid(row=2,column=1)


app = App()
app.mainloop()
