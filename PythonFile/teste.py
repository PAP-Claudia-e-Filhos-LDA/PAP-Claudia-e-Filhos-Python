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
        self.window.configure(background="lightblue")

            #icon da janela
        icon = PhotoImage(file="../imagens/profile.png")
        self.window.iconphoto(True, icon)

        #Cabecalho
        self.header = Frame(self.window, bg ="#009df4")
        self.header.place(x=300,y=0,width=1070,height=60)

            #botão de sair
        self.logout_text =Button(self.window,text="Sair", bg="#32cf8e" , font =("" , 13 ,"bold"),bd=0, fg='white', cursor = 'hand2' , activebackground='#32cf8e', command=self.window.destroy)
        self.logout_text.place(x=1315,y=15)

def win():
    window = Tk()
    Dashboard(window)
    window.mainloop()

if __name__ == "__main__":
    win()
