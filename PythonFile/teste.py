import tkinter.ttk
from tkinter import *
from PIL import Image, ImageTk
from datetime import *
import time
import ctypes
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

'''Notas:
#FD9C3A -> Laranja 
#17191F -> Cinzento Escuro
#2E3133 -> Cinzento Claro'''
class Funcs:
    def conecta_bd(self):  # faz conexao á base de dados
        self.conn = sqlite3.connect("../BD/Rissois.db")
        self.cursor = self.conn.cursor()
    def desconecta_bd(self):  # desliga a conexao á base de dados
        self.conn.close()
    def contar_clientes(self):  # função pra contar o numero de clientes
        self.conecta_bd()
        resultado = self.cursor.execute("SELECT COUNT(*) FROM Clientes").fetchone()
        self.desconecta_bd()
        return resultado[0]
    def contar_Produtos(self): #função para contar o numero de produtos
        self.conecta_bd()
        resultado = self.cursor.execute("SELECT COUNT(*) FROM Produtos").fetchone()
        self.desconecta_bd()
        return resultado[0]
    def contar_lucro(self):# função que vai buscar o lucro por mes
        self.conecta_bd()
        resultado = self.cursor.execute("""SELECT strftime('%Y-%m', LE."data_encomenda") AS month, SUM(P."preco" * LE."quantidade") AS total_amount FROM "Linha_de_Encomenda" AS LE JOIN "Produtos" AS P ON LE."Produtos_id_produto" = P."id_produto" GROUP BY month ORDER BY month""").fetchall()
        self.desconecta_bd()
        return resultado
    def contar_Encomendas(self):  # função para contar o numero de encomendas
        self.conecta_bd()
        resultado = self.cursor.execute("SELECT COUNT(*) FROM Encomendas").fetchone()
        self.desconecta_bd()
        return resultado[0]
    def lista_produtos(self):#faz o select que vai mostrar os produtos e as suas informações
        self.produtos_lista.delete(*self.produtos_lista.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("select id_produto, nome_produto, preco from Produtos order by id_produto")
        for i in lista:
            self.produtos_lista.insert("", "end", values=i)
            self.produtos_lista.update()
        self.desconecta_bd()

    def ordenarProdutos_Id(self):
        self.produtos_lista.delete(*self.produtos_lista.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("Select * from Produtos Order by id_produto DESC")
        for i in lista:
            self.produtos_lista.insert("", "end", values=i)
            self.produtos_lista.update()
        self.desconecta_bd()

class Dashboard(Funcs):
    def __init__(self, window):

        # janela principal
        self.window = window
        self.window.title("Rissois")
        self.window.geometry("1366x768")
        self.window.state("zoomed")
        self.window.configure(background="#17191F")

        #Frame Inicio (O primeiro de quando se abre o programa)
        self.frameInicio = Frame(self.window, bg="#17191F")
        self.frameInicio.place(x=300, y=0, width=1366, height=768)

        ##############################################################################################################################################
        ##################################################### Barra Lateral ###########################################################################
        ##############################################################################################################################################
        ## Icon
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.window.iconbitmap(r'../imagens/favicon.ico')

        # Barra Lateral
        self.sidebar = Frame(self.window, bg="#2E3133")
        self.sidebar.place(x=0, y=0, width=300, height=1900)

        ## Empresa Imagem
        EmpresaLogo = ImageTk.PhotoImage(Image.open('../imagens/profile.png'))
        self.logo = Label(self.sidebar, image=EmpresaLogo, bg='#FD9C3A')
        self.logo.image = EmpresaLogo
        self.logo.place(x=70, y=80)

        ## Empresa Nome
        self.EmpresaNome = Label(self.sidebar, text='Claúdia e Filhos, Lda', bg='#2E3133', font=("", 15, "bold"),fg='white')
        self.EmpresaNome.place(x=45, y=240)

        # Opções
        ## Inicio
        self.dashboard_text = Button(self.sidebar, text='Inicio', bg='#2E3133', font=("", 12, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=10,command=lambda: self.frameInicio.lift())
        self.dashboard_text.place(x=30, y=325)

        ## Encomendas
        self.manager_text = Button(self.sidebar, text='Encomendas', bg='#2E3133', font=("", 12, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=10)
        self.manager_text.place(x=160, y=325)

        ## Produtos
        self.settings_text = Button(self.sidebar, text='Produtos', bg='#2E3133', font=("", 12, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=10,command=lambda: self.frameProdutos.lift())
        self.settings_text.place(x=30, y=375)

        ## Clientes
        self.manager_text = Button(self.sidebar, text='Clientes', bg='#2E3133', font=("", 12, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=10)
        self.manager_text.place(x=160, y=375)

        ## Lucro
        self.settings_text = Button(self.sidebar, text='Lucro', bg='#2E3133', font=("", 12, "bold"), fg='white',
                                    cursor='hand2', activebackground='#FD9C3A', bd=5, width=10)
        self.settings_text.place(x=30, y=425)

        ## Sair
        self.exit_text = Button(self.sidebar, text='Exit', bg='#2E3133', font=("", 12, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=10, command=self.window.quit)
        self.exit_text.place(x=160, y=425)

        ##############################################################################################################################################
        ##################################################### FRAME Inicio ##########################################################################
        ##############################################################################################################################################

        ## Label Dashboard
        self.heading_Inicio = Label(self.frameInicio, text="Dashboard", font=("", 13, "bold"), fg='white', bg='#17191F')
        self.heading_Inicio.place(x=25, y=50)

        self.line_Inicio = Label(self.frameInicio, text="____________", font=("", 10, "bold"), fg='#FD9C3A', bg='#17191F')
        self.line_Inicio.place(x=25, y=25)

        ## Frame 1 do body (Grafico)
        self.bodyFrame1_Inicio = Frame(self.frameInicio, bg="#2E3133")
        self.bodyFrame1_Inicio.place(x=28, y=90, width=1010, height=350)

        ### Grafico
        #### Configs do Grafico
        fig, ax = plt.subplots(figsize=(8, 4), tight_layout=True, facecolor='#2E3133')
        ax.set_facecolor('#2E3133')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')

        #### Valores do Grafico
        lucros = self.contar_lucro()
        mes, total = zip(*lucros)

        #### Cores da escala
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        for text in ax.get_xticklabels() + ax.get_yticklabels():
            text.set_color('white')

        #### Cores dos eixos
        ax.bar(mes, total, color='#FD9C3A',)
        ax.set_xlabel('Mês', color='white')
        ax.set_ylabel('Total ', color='white')
        ax.set_title('Total por Mês', color='white')

        #### Escreve os meses
        ax.set_xticks(range(len(mes)))
        ax.set_xticklabels(mes, rotation=45, ha='right')

        #### Por o Grafico no BodyFrame1
        canvas = FigureCanvasTkAgg(fig, master=self.bodyFrame1_Inicio)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        for text in ax.get_xticklabels() + ax.get_yticklabels():
            text.set_color('white')


        ## Frame 2 do body (Clientes)
        self.bodyFrame2_Inicio = Frame(self.frameInicio, bg="#2E3133")
        self.bodyFrame2_Inicio.place(x=28, y=475, width=310, height=220)

        ### Label a dizer Clientes
        self.labelFrame2_Inicio = Label(self.bodyFrame2_Inicio, bg="#2E3133", text="Clientes", font=("", 15, "bold"), fg='white')
        self.labelFrame2_Inicio.place(x=60, y=25)

        ### Linha
        self.lineFrame2_Inicio = Label(self.bodyFrame2_Inicio, text="_________", font=("", 10, "bold"), fg='#FD9C3A',bg='#2E3133')
        self.lineFrame2_Inicio.place(x=60, y=5)

        ### Imagem
        ClientesImage = ImageTk.PhotoImage(Image.open('../imagens/clientes.png'))
        self.logo = Label(self.bodyFrame2_Inicio, image=ClientesImage, bg='#2E3133')
        self.logo.image = ClientesImage
        self.logo.place(x=25, y=21)

        ###Numero de CLientes
        numClientes = self.contar_clientes()
        self.N_clientesFrame2_Inicio = Label(self.bodyFrame2_Inicio, bg="#2E3133", text=str(numClientes), font=("", 50, "bold"), fg='white')
        self.N_clientesFrame2_Inicio.place(x=115, y=70)

        ## Frame 3 do body (Produtos)
        self.bodyFrame3_Inicio = Frame(self.frameInicio, bg="#2E3133", cursor='hand2')
        self.bodyFrame3_Inicio.place(x=380, y=475, width=310, height=220)
        self.bodyFrame3_Inicio.bind("<Button-1>", lambda event: self.frameProdutos.lift())


        ### Label a dizer Produtos
        self.labelFrame3_Inicio = Label(self.bodyFrame3_Inicio, bg="#2E3133", text="Produtos", font=("", 15, "bold"), fg='white')
        self.labelFrame3_Inicio.place(x=60, y=25)

        ### Linha
        self.lineFrame3_Inicio = Label(self.bodyFrame3_Inicio, text="_________", font=("", 10, "bold"), fg='#FD9C3A',bg='#2E3133')
        self.lineFrame3_Inicio.place(x=60, y=5)

        ### Imagem
        ProdutosImage = ImageTk.PhotoImage(Image.open('../imagens/shopping-cart.png'))
        self.logo = Label(self.bodyFrame3_Inicio, image=ProdutosImage, bg='#2E3133')
        self.logo.image = ProdutosImage
        self.logo.place(x=25, y=21)

        ###Numero de Produtos
        numProdutos = self.contar_Produtos()
        self.N_produtosFrame3_Inicio = Label(self.bodyFrame3_Inicio, bg="#2E3133", text=str(numProdutos), font=("", 50, "bold"), fg='white')
        self.N_produtosFrame3_Inicio.place(x=115, y=70)

        ## Frame 4 do body (Encomendas)
        self.bodyFrame4_Inicio = Frame(self.frameInicio, bg="#2E3133")
        self.bodyFrame4_Inicio.place(x=730, y=475, width=310, height=220)

        ### Label a dizer Encomendas
        self.labelFrame4_Inicio = Label(self.bodyFrame4_Inicio, bg="#2E3133", text="Encomendas", font=("", 15, "bold"), fg='white')
        self.labelFrame4_Inicio.place(x=60, y=25)

        ### Linha
        self.lineFrame4_Inicio = Label(self.bodyFrame4_Inicio, text="_______________", font=("", 10, "bold"), fg='#FD9C3A',bg='#2E3133')
        self.lineFrame4_Inicio.place(x=60, y=5)

        ### Imagem
        EncomendasImage = ImageTk.PhotoImage(Image.open('../imagens/encomenda.png'))
        self.logo = Label(self.bodyFrame4_Inicio, image=EncomendasImage, bg='#2E3133')
        self.logo.image = EncomendasImage
        self.logo.place(x=25, y=21)

        ###Numero de Encomendas
        numEncomendas = self.contar_Encomendas()
        self.N_encomendasFrame4_Inicio = Label(self.bodyFrame4_Inicio, bg="#2E3133", text=str(numEncomendas), font=("", 50, "bold"),fg='white')
        self.N_encomendasFrame4_Inicio.place(x=115, y=70)


        ##############################################################################################################################################
        ##################################################### FRAME Produtos #########################################################################
        ##############################################################################################################################################

        ##Frame Produtos
        self.frameProdutos = Frame(self.window, bg="#17191F")
        self.frameProdutos.place(x=300, y=0, width=1366, height=768)

        # Corpo

        ## Label Dashboard
        self.heading_Produtos = Label(self.frameProdutos, text="Produtos", font=("", 13, "bold"), fg='white', bg='#17191F')
        self.heading_Produtos.place(x=25, y=50)

        self.line_Produtos = Label(self.frameProdutos, text="____________", font=("", 10, "bold"), fg='#FD9C3A', bg='#17191F')
        self.line_Produtos.place(x=25, y=25)

        ## Frame 1 da listagem de Produtos
        self.bodyFrame1_Produtos = Frame(self.frameProdutos, bg="#2E3133")
        self.bodyFrame1_Produtos.place(x=28, y=90, width=310, height=650)

        ### Treeview que mostra todos os Produtos na base de dados
        self.produtos_lista =tkinter.ttk.Treeview(self.bodyFrame1_Produtos, columns=("col1", "col2", "col3",))
        self.produtos_lista.heading("#0", text="")
        self.produtos_lista.heading("#1", text="Produto", anchor='w',command=lambda: self.ordenarProdutos_Id())
        self.produtos_lista.heading("#2", text="Nome", anchor='w')
        self.produtos_lista.heading("#3", text="Preço", anchor='w')
        self.produtos_lista.column("#0", width=1, stretch=NO)
        self.produtos_lista.column("#1", width=100, stretch=NO)
        self.produtos_lista.column("#2", width=130, stretch=NO)
        self.produtos_lista.column("#3", width=76, stretch=NO)
        self.produtos_lista.place(relx=-0.009, rely=0, relwidth=1.001, relheight=1.05)

        ### Sroll Bar
        self.sroll = Scrollbar(self.bodyFrame1_Produtos, orient="vertical")
        self.sroll.configure(command=self.produtos_lista.yview)
        self.produtos_lista.configure(yscroll=self.sroll.set)
        self.sroll.place(relx=0.937, rely=0.04, relwidth=0.051, relheight=0.96)
        self.lista_produtos()

        ### Decorar a Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.map('Treeview',background=[('selected', '#FD9C3A'), ('!selected', '#2E3133')],foreground=[('selected', 'black'), ('!selected', 'white')],)
        style.map('Treeview.Heading',foreground=[('selected', 'black')])
        style.configure('Treeview.Heading', background="#FD9C3A")
        style.configure('Treeview',rowheight=35)

        ## Frame 2 Adicionar Produtos
        self.bodyFrame2_Produtos = Frame(self.frameProdutos, bg="#2E3133")
        self.bodyFrame2_Produtos.place(x=380, y=90, width=310, height=650)


        ## Frame 3 (Quantidade de Produtos)
        self.bodyFrame3_Produtos = Frame(self.frameProdutos, bg="#2E3133")
        self.bodyFrame3_Produtos.place(x=730, y=90, width=310, height=175)

        ### Label a dizer Produtos
        self.labelFrame3_Produtos = Label(self.bodyFrame3_Produtos, bg="#2E3133", text="Total de Produtos:", font=("", 15, "bold"),fg='white')
        self.labelFrame3_Produtos.place(x=60, y=25)

        ### Linha
        self.lineFrame3_Produtos = Label(self.bodyFrame3_Produtos, text="________________________", font=("", 10, "bold"), fg='#FD9C3A',bg='#2E3133')
        self.lineFrame3_Produtos.place(x=60, y=0)

        ### Imagem
        ProdutosImage = ImageTk.PhotoImage(Image.open('../imagens/shopping-cart.png'))
        self.logo = Label(self.bodyFrame3_Produtos, image=ProdutosImage, bg='#2E3133')
        self.logo.image = ProdutosImage
        self.logo.place(x=20, y=16)

        ###Numero de Produtos
        numProdutos = self.contar_Produtos()
        self.N_produtosFrame3_Produtos = Label(self.bodyFrame3_Produtos, bg="#2E3133", text=str(numProdutos),font=("", 50, "bold"), fg='white')
        self.N_produtosFrame3_Produtos.place(x=115, y=70)



        ## Frame 4 Grafico redondo
        self.bodyFrame4_Produtos = Frame(self.frameProdutos, bg="#2E3133")
        self.bodyFrame4_Produtos.place(x=730, y=310, width=310 , height=430)


















        self.frameInicio.lift()
def win():
    window = Tk()
    Dashboard(window)
    window.mainloop()

if __name__ == "__main__":
    win()
