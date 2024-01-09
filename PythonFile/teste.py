from tkinter import *
from PIL import Image, ImageTk
from datetime import *
import time
import ctypes
import sqlite3
import matplotlib.pyplot as plt

class Funcs:
    def conecta_bd(self):  # faz conexao á base de dados
        self.conn = sqlite3.connect("../BD/Rissois.db")
        self.cursor = self.conn.cursor()
    def desconecta_bd(self):  # desliga a conexao á base de dados
        self.conn.close()
    def contar_clientes(self):  # função pra contar o numero de clientes pra por automatico quando se adciona um novo cliente
        self.conecta_bd()
        resultado = self.cursor.execute("SELECT COUNT(*) FROM Clientes").fetchone()
        self.desconecta_bd()
        return resultado[0]

    def contar_Produtos(self): #função para contar o numero de produtos pra por automatico quando se adciona
        self.conecta_bd()
        resultado = self.cursor.execute("SELECT COUNT(*) FROM Produtos").fetchone()
        self.desconecta_bd()
        return resultado[0]
class Dashboard(Funcs):
    def __init__(self, window):
        # janela principal
        self.window = window
        self.window.title("Rissois")
        self.window.geometry("1366x768")
        self.window.state("zoomed")
        self.window.configure(background="#232323")

        # Icon
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.window.iconbitmap(r'../imagens/favicon.ico')

        # Barra Lateral
        self.sidebar = Frame(self.window, bg="#2E3133")
        self.sidebar.place(x=0, y=0, width=300, height=1900)

        # Empresa Imagem
        EmpresaLogo = ImageTk.PhotoImage(Image.open('../imagens/profile.png'))
        self.logo = Label(self.sidebar, image=EmpresaLogo, bg='#FFB366')
        self.logo.image = EmpresaLogo
        self.logo.place(x=70, y=80)

        # Empresa Nome
        self.EmpresaNome = Label(self.sidebar, text='Claúdia e Filhos, Lda', bg='#2E3133', font=("", 15, "bold"),
                                 fg='white')
        self.EmpresaNome.place(x=45, y=240)

        # Opções

        # Dashboard
        self.dashboard_text = Button(self.sidebar, text='Dashboard', bg='#2E3133', font=("", 12, "bold"), fg='white',
                                     cursor='hand2', activebackground='#FFB366', bd=5, width=10)
        self.dashboard_text.place(x=30, y=325)

        # Manager
        self.manager_text = Button(self.sidebar, text='Manage', bg='#2E3133', font=("", 12, "bold"), fg='white',
                                   cursor='hand2', activebackground='#FFB366', bd=5, width=10)
        self.manager_text.place(x=160, y=325)

        # Settings
        self.settings_text = Button(self.sidebar, text='Settings', bg='#2E3133', font=("", 12, "bold"), fg='white',
                                    cursor='hand2', activebackground='#FFB366', bd=5, width=10)
        self.settings_text.place(x=30, y=375)

        # Sair
        self.exit_text = Button(self.sidebar, text='Exit', bg='#2E3133', font=("", 12, "bold"), fg='white',
                                cursor='hand2', activebackground='#FFB366', bd=5, width=10, command=self.window.destroy)
        self.exit_text.place(x=160, y=375)

        # Corpo

        # Label Dashboard
        self.heading = Label(self.window, text="Dashboard", font=("", 13, "bold"), fg='white', bg='#232323')
        self.heading.place(x=325, y=50)

        self.line = Label(self.window, text="____________", font=("", 10, "bold"), fg='#ffb366', bg='#232323')
        self.line.place(x=325, y=25)

        # Frame 1 do body (Total por Mês)
        self.bodyFrame1 = Frame(self.window, bg="#2E3133")
        self.bodyFrame1.place(x=328, y=90, width=1010, height=350)

        # Frame 2 do body (Clientes)
        self.bodyFrame2 = Frame(self.window, bg="#2E3133")
        self.bodyFrame2.place(x=328, y=475, width=310, height=220)

        # Label a dizer Clientes
        self.labelFrame2 = Label(self.bodyFrame2, bg="#2E3133", text="Clientes", font=("Poppins", 15, "bold"), fg='white')
        self.labelFrame2.place(x=60, y=25)

        # Linha
        self.lineFrame2 = Label(self.bodyFrame2, text="  ________", font=("Poppins", 10, "bold"), fg='#ffb366',
                                bg='#2E3133')
        self.lineFrame2.place(x=60, y=5)

        # Imagem
        ClientesImage = ImageTk.PhotoImage(Image.open('../imagens/clientes.png'))
        self.logo = Label(self.bodyFrame2, image=ClientesImage, bg='#2E3133')
        self.logo.image = ClientesImage
        self.logo.place(x=25, y=21)

        #Numero de CLientes
        numClientes = self.contar_clientes()
        self.N_clientesFrame2 = Label(self.bodyFrame2, bg="#2E3133", text=str(numClientes), font=("", 50, "bold"), fg='white')
        self.N_clientesFrame2.place(x=115, y=95)


        # Frame 3 do body (Produtos)
        self.bodyFrame3 = Frame(self.window, bg="#2E3133")
        self.bodyFrame3.place(x=680, y=475, width=310, height=220)

        # Label a dizer Produtos
        self.labelFrame3 = Label(self.bodyFrame3, bg="#2E3133", text="Produtos", font=("", 15, "bold"), fg='white')
        self.labelFrame3.place(x=25, y=25)

        # Linha
        self.lineFrame3 = Label(self.bodyFrame3, text="______", font=("", 10, "bold"), fg='#ffb366',
                                bg='#2E3133')
        self.lineFrame3.place(x=25, y=0)

        # Imagem
        ProdutosImage = ImageTk.PhotoImage(Image.open('../imagens/shopping-cart.png'))
        self.logo = Label(self.bodyFrame3, image=ProdutosImage, bg='#2E3133')
        self.logo.image = ProdutosImage
        self.logo.place(x=235, y=5)



        #Numero de Produtos
        numProdutos = self.contar_Produtos()
        self.N_clientesFrame2 = Label(self.bodyFrame3, bg="#2E3133", text=str(numProdutos), font=("", 50, "bold"), fg='white')
        self.N_clientesFrame2.place(x=115, y=95)

        # Frame 4 do body (Encomendas?)
        self.bodyFrame4 = Frame(self.window, bg="#2E3133")
        self.bodyFrame4.place(x=1030, y=475, width=310, height=220)



def win():
    window = Tk()
    Dashboard(window)
    window.mainloop()


if __name__ == "__main__":
    win()
