from tkinter import *
from PIL import Image, ImageTk
from datetime import *
import time
import ctypes
class Dashboard:
    def __init__(self, window):
        #janela principal
        self.window = window
        self.window.title("Rissois")
        self.window.geometry("1366x768")
        self.window.state("zoomed")
        self.window.configure(background="#232323")

            # Icon
        myappid='mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.window.iconbitmap(r'../imagens/favicon.ico')

        #Barra Lateral
        self.sidebar = Frame(self.window, bg="#2E3133")
        self.sidebar.place(x=0,y=0,width=300,height=1900)

            #Empresa Imagem
        EmpresaLogo = ImageTk.PhotoImage(Image.open('../imagens/profile.png'))
        self.logo = Label(self.sidebar,image=EmpresaLogo,bg='#FFB366')
        self.logo.image = EmpresaLogo
        self.logo.place(x=70,y=80)

            #Empresa Nome
        self.EmpresaNome = Label(self.sidebar,text='Claúdia e Filhos, Lda',bg='#2E3133', font=("", 15, "bold"),fg='white')
        self.EmpresaNome.place(x=45,y=240)

            #Opções

                #Dashboard
        self.dashboard_text = Button(self.sidebar,text='Dashboard',bg='#2E3133', font=("", 12, "bold"),fg='white',cursor='hand2', activebackground='#FFB366',bd=5,width=10)
        self.dashboard_text.place(x=30,y=325)

                #Manager
        self.manager_text = Button(self.sidebar,text='Manage',bg='#2E3133', font=("", 12, "bold"),fg='white',cursor='hand2', activebackground='#FFB366',bd=5,width=10)
        self.manager_text.place(x=160,y=325)

                #Settings
        self.settings_text = Button(self.sidebar,text='Settings',bg='#2E3133', font=("", 12, "bold"),fg='white',cursor='hand2', activebackground='#FFB366',bd=5,width=10)
        self.settings_text.place(x=30,y=375)

                #Sair
        self.exit_text = Button(self.sidebar,text='Exit',bg='#2E3133', font=("", 12, "bold"),fg='white',cursor='hand2', activebackground='#FFB366',bd=5,width=10,command=self.window.destroy)
        self.exit_text.place(x=160,y=375)


        #Corpo

            #Label Dashboard
        self.heading = Label(self.window,text="Dashboard" , font=("",13,"bold"),fg='white',bg='#232323')
        self.heading.place(x=325,y=50)

        self.line = Label(self.window, text="____________", font=("", 10, "bold"), fg='#ffb366', bg='#232323')
        self.line.place(x=325, y=25)

            #Frame 1 do body (Total por Mês)
        self.bodyFrame1= Frame(self.window,bg="#2E3133")
        self.bodyFrame1.place(x=328,y=90,width=1010,height=350)

            #Frame 2 do body (Clientes)
        self.bodyFrame2= Frame(self.window,bg="#2E3133")
        self.bodyFrame2.place(x=328,y=475,width=310,height=220)

                #Label a dizer Clientes
        self.labelFrame2=Label(self.bodyFrame2,bg="#2E3133",text="Clientes", font=("",20,"bold"),fg='white')
        self.labelFrame2.place(x=75,y=25)

                #Linha
        self.lineFrame2 = Label(self.bodyFrame2, text="__________________", font=("", 15, "bold"), fg='#ffb366', bg='#2E3133')
        self.lineFrame2.place(x=25, y=0)
                #Imagem
        ClientesImage = ImageTk.PhotoImage(Image.open('../imagens/clientes.png'))
        self.logo = Label(self.bodyFrame2, image=ClientesImage, bg='#2E3133')
        self.logo.image = ClientesImage
        self.logo.place(x=235, y=5)
        

            #Frame 3 do body (Produtos)
        self.bodyFrame3= Frame(self.window,bg="#2E3133")
        self.bodyFrame3.place(x=680,y=475,width=310,height=220)

            #Frame 4 do body (Encomendas?)
        self.bodyFrame4= Frame(self.window,bg="#2E3133")
        self.bodyFrame4.place(x=1030,y=475,width=310,height=220)

def win():
    window = Tk()
    Dashboard(window)
    window.mainloop()

if __name__ == "__main__":
    win()
