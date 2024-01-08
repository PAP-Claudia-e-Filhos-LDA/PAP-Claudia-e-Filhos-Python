from tkinter import *
from PIL import Image, ImageTk
from datetime import *
import time

class Dashboard:
    def __init__(self, window):
        #janela principal
        self.window = window
        self.window.title("Rissois")
        self.window.geometry("1366x768")
        self.window.state("zoomed")
        self.window.configure(background="#232323")

            #icon da janela
        icon = PhotoImage(file="../imagens/profile.png")
        self.window.iconphoto(True, icon)

        #Barra Lateral
        self.sidebar = Frame(self.window, bg="#2E3133")
        self.sidebar.place(x=0,y=0,width=300,height=1900)

        #Corpo
        self.heading = Label(self.window,text="Dashboard" , font=("",13,"bold"),fg='white',bg='#232323')
        self.heading.place(x=325,y=50)

        self.line = Label(self.window, text="____________", font=("", 10, "bold"), fg='#ffb366', bg='#232323')
        self.line.place(x=325, y=25)

            #Frame 1 do body
        self.bodyFrame1= Frame(self.window,bg="#2E3133")
        self.bodyFrame1.place(x=328,y=110,width=1010,height=350)

            #Frame 2 do body
        self.bodyFrame2= Frame(self.window,bg="#2E3133")
        self.bodyFrame2.place(x=328,y=495,width=310,height=200)

            #Frame 3 do body
        self.bodyFrame3= Frame(self.window,bg="#2E3133")
        self.bodyFrame3.place(x=680,y=495,width=310,height=200)

            #Frame 2 do body
        self.bodyFrame4= Frame(self.window,bg="#2E3133")
        self.bodyFrame4.place(x=1030,y=495,width=310,height=200)

def win():
    window = Tk()
    Dashboard(window)
    window.mainloop()

if __name__ == "__main__":
    win()
