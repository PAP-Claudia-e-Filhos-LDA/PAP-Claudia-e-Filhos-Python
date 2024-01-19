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
from tkinter import ttk, Text, WORD, END, INSERT, filedialog, simpledialog, messagebox
import os

'''Notas:
#FD9C3A -> Laranja 
#17191F -> Cinzento Escuro
#2E3133 -> Cinzento Claro

#TENTAR FAZER FUNÇÃO QUE ORDENE OS ITENS DA TREEVIEW'''
class Funcs:
    def conecta_bd(self):  # faz conexao á base de dados
        self.conn = sqlite3.connect("../BD/Rissois.db")
        self.cursor = self.conn.cursor()
    def desconecta_bd(self):  # desliga a conexao á base de dados
        self.conn.commit()
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
        lista = self.cursor.execute("SELECT id_produto, nome_produto, preco || ' €' AS preco,desc, caminho_imagem, CASE WHEN ativo = 1 THEN 'Sim' ELSE 'Não' END AS ativo FROM Produtos ORDER BY id_produto;")
        for i in lista:
            self.produtos_lista.insert("", "end", values=i)
            self.produtos_lista.update()
        self.desconecta_bd()
    def on_double_click(self, event):# Quando se faz doublee click as entrys preenchem automaticamente com os produtos em que o double click foi feito
        item = self.produtos_lista.selection()[0]
        values = self.produtos_lista.item(item, "values")

        self.Textbox_Produtos.delete(0, tk.END)
        self.Textbox_Produtos.insert(0, values[1])
        self.Textbox_Preco.delete(0, tk.END)
        self.Textbox_Preco.insert(0, values[2][:-1])
        self.TextBox_Descrição.delete(1.0, tk.END)
        self.TextBox_Descrição.insert(tk.END, values[3])

        caminho = values[4]

        try:
            if hasattr(self, 'logo') and hasattr(self,'nova_imagem'):
                self.nova_imagem.config(text="Alterar Imagem")
                self.logo.destroy()

            ImagemProduto = ImageTk.PhotoImage(Image.open(caminho).resize((250, 135)))
            self.logo = Label(self.bodyFrame4_Produtos, image=ImagemProduto, bg='#2E3133', bd=1)
            self.logo.image = ImagemProduto
            self.logo.place(x=15, y=275)
        except FileNotFoundError:
            if hasattr(self, 'logo') and hasattr(self,'nova_imagem'):
                self.logo.destroy()
            print("Erro: Imagem não Encontrada")
            self.nova_imagem = Button(self.bodyFrame4_Produtos, text="Adicione uma imagem", command=self.inserir_imagem ,bg='#2E3133', font=("", 10, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=20)
            self.nova_imagem.place(x=79, y=240)
    def Limpar(self):# função que quando se da um click com o botao direito na Treeview ela pergunta se quer apagar
            resposta = messagebox.askyesno("Confirmação", "Limpar todas as Entrys?")
            if resposta:
                self.Textbox_Produtos.delete(0, END)
                self.Textbox_Preco.delete(0, END)
                self.TextBox_Descrição.delete(1.0, END)
                self.nova_imagem.config(text="Adicione uma imagem")
                FundoImagem = ImageTk.PhotoImage(Image.open('../Imagens/semImagem.png').resize((250, 135)))
                self.logo.image = FundoImagem
    def on_right_click(self, event):
        self.conecta_bd()
        item = self.produtos_lista.selection()[0] if self.produtos_lista.selection() else None
        if item:
            item = self.produtos_lista.selection()[0]
            values = self.produtos_lista.item(item, "values")
            item_id = values[0]
            ativo = values[5]
            if ativo == "Sim":
                resposta = messagebox.askyesno("Confirmação", "Queres desativar este produto?")
            else:
                resposta = messagebox.askyesno("Confirmação", "Queres ativar este produto?")

            if resposta:
                if ativo == "Sim":
                    resultado = self.cursor.execute("UPDATE Produtos SET ativo = 0 WHERE id_produto = ?;", (item_id,))
                else:
                    resultado = self.cursor.execute("UPDATE Produtos SET ativo = 1 WHERE id_produto = ?;", (item_id,))
                self.desconecta_bd()
                self.lista_produtos()
        self.produtos_lista.update()
    def inserir_imagem(self):#guarda as imagens que foram uploadadas numa pasta com um nome especifico para serem tratadas pela,base de dados

        try:# verifica se esta alguma coisa selecionada. Se tiver vai fazer o id desse produto se nao vai continuar a partir do ultimo numero
            item = self.produtos_lista.selection()[0]
            values = self.produtos_lista.item(item, "values")
            item = values[0]
        except IndexError:
            num_produtos = self.contar_Produtos() + 1
            item = num_produtos

        self.caminho_nova_imagem = filedialog.askopenfilename(initialdir="/", title="Selecione uma imagem", filetypes=(
            ("Arquivos de Imagem", "*.png;*.jpg;*.jpeg;*.gif"), ("Todos os arquivos", "*.*")))
        if self.caminho_nova_imagem:
            imagem = Image.open(self.caminho_nova_imagem).resize((250, 135))
            imagem_produto = ImageTk.PhotoImage(imagem)

            if hasattr(self, 'logo') and hasattr(self, 'nova_imagem'):
                self.logo.destroy()

            self.logo = Label(self.bodyFrame4_Produtos, image=imagem_produto, bg='#2E3133', bd=1)
            self.logo.image = imagem_produto
            self.logo.place(x=15, y=275)
    def adicionar_produto(self):# função que vai adicionar os produtos/alterar um produto já existente
        self.conecta_bd()
        try:# verifica se esta alguma coisa selecionada. Se tiver vai fazer o id desse produto se nao vai continuar a partir do ultimo numero
            selcionado = self.produtos_lista.selection()
            item = self.produtos_lista.selection()[0]
            values = self.produtos_lista.item(item, "values")
            item = values[0]
        except IndexError:
            num_produtos = self.contar_Produtos()
            item = num_produtos

        nome = self.Textbox_Produtos.get()
        if nome.strip() == "":  #este if serve para saber se a variavel foi preenchida ou nao
            try: #se essa mesma variavel nao foi preenchida vai buscar á base de dados a anteriror para o registo nao ficar em branco
                result = self.cursor.execute("SELECT nome_produto FROM Produtos WHERE id_produto=?", (item,)).fetchone()
                if result:
                    nome = result[0]
            except Exception:
                print("Ocorreu um erro com o nome, tente novamente.")

        preco = self.Textbox_Preco.get()
        if preco.strip() == "":
            try:
                result = self.cursor.execute("SELECT preco FROM Produtos WHERE id_produto=?", (item,)).fetchone()
                if result:
                    preco = result[0]
            except Exception:
                print("Ocorreu um erro com o preco, tente novamente.")

        desc = self.TextBox_Descrição.get("1.0", "end-1c")
        if desc.strip() == "":
            try:
                result = self.cursor.execute("SELECT `desc` FROM Produtos WHERE id_produto=?", (item,)).fetchone()
                if result:
                    desc = result[0]
            except Exception:
                print("Ocorreu um erro com a descrição, tente novamente.")

        try:
            imagem = Image.open(self.caminho_nova_imagem).resize((250, 135))
            imagem.save(os.path.join("../imagens/", f"imagem_produto_{item}.png"))
            imagem = "../imagens/" + f"imagem_produto_{item}.png"
        except Exception:
            try:
                result = self.cursor.execute("SELECT caminho_imagem FROM Produtos WHERE id_produto=?",(item,)).fetchone()
                if result:
                    imagem = result[0]
            except Exception:
                print("Ocorreu um erro com a imagem, tente novamente.")

        if selcionado:
            self.conecta_bd()
            self.cursor.execute("UPDATE Produtos SET nome_produto=?, preco=?, `desc`=?, caminho_imagem=? WHERE id_produto=?",(nome, preco, desc, imagem, item))
            self.desconecta_bd()
        else:
            self.conecta_bd()
            self.cursor.execute("INSERT INTO Produtos (nome_produto, preco, `desc`, caminho_imagem, ativo) VALUES (?, ?,?,?,?)",(nome, preco, desc, imagem, 1))
            self.desconecta_bd()
            self.N_produtosFrame3_Produtos.config(text=int(self.contar_Produtos()))
        self.lista_produtos()
        self.produtos_lista.update()
        if hasattr(self, 'logo') and hasattr(self, 'nova_imagem'):
            self.logo.destroy()
            self.nova_imagem.config(text="Adicione uma imagem ")

class Dashboard(Funcs):
    def __init__(self, window):
        # janela principal
        self.window = window
        self.window.title("Rissois")
        self.window.geometry("1366x768")
        self.window.state("zoomed")
        self.window.configure(background="#17191F")

        # Icon da app
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.window.iconbitmap(r'../imagens/favicon.ico')

        ##############################################################################################################################################
        ##################################################### Barra Lateral ###########################################################################
        ##############################################################################################################################################

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
        ## Btn Inicio
        self.dashboard_text = Button(self.sidebar, text='Inicio', bg='#2E3133', font=("", 12, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=10,command=lambda: self.frameInicio.lift())
        self.dashboard_text.place(x=30, y=325)

        ## Btn Encomendas
        self.manager_text = Button(self.sidebar, text='Encomendas', bg='#2E3133', font=("", 12, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=10)
        self.manager_text.place(x=160, y=325)

        ## Btn Produtos
        self.settings_text = Button(self.sidebar, text='Produtos', bg='#2E3133', font=("", 12, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=10,command=lambda: self.frameProdutos.lift())
        self.settings_text.place(x=30, y=375)

        ## Btn Clientes
        self.manager_text = Button(self.sidebar, text='Clientes', bg='#2E3133', font=("", 12, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=10)
        self.manager_text.place(x=160, y=375)

        ## Btn Lucro
        self.settings_text = Button(self.sidebar, text='Lucro', bg='#2E3133', font=("", 12, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=10)
        self.settings_text.place(x=30, y=425)

        ## Btn Sair
        self.exit_text = Button(self.sidebar, text='Exit', bg='#2E3133', font=("", 12, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=10, command=self.window.quit)
        self.exit_text.place(x=160, y=425)

        ##############################################################################################################################################
        ##################################################### FRAME Inicio ##########################################################################
        ##############################################################################################################################################

        #Frame Inicio (O primeiro de quando se abre o programa)
        self.frameInicio = Frame(self.window, bg="#17191F")
        self.frameInicio.place(x=300, y=0, width=1366, height=768)

        ## Label Dashboard
        self.heading_Inicio = Label(self.frameInicio, text="Dashboard", font=("", 13, "bold"), fg='white', bg='#17191F')
        self.heading_Inicio.place(x=25, y=50)

        ##Linha
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
        self.bodyFrame1_Produtos.place(x=28, y=90, width=660, height=650)

        ### Treeview que mostra todos os Produtos na base de dados
        self.produtos_lista =tkinter.ttk.Treeview(self.bodyFrame1_Produtos, columns=("col1", "col2", "col3","col4","col5","col6"))
        self.produtos_lista.heading("#0", text="")
        self.produtos_lista.heading("#1", text="Produto", anchor='w')
        self.produtos_lista.heading("#2", text="Nome", anchor='w')
        self.produtos_lista.heading("#3", text="Preço", anchor='w')
        self.produtos_lista.heading("#4", text="Descrição", anchor='w')
        self.produtos_lista.heading("#5", text="Imagem", anchor='w')
        self.produtos_lista.heading("#6", text="Ativo", anchor='w')
        self.produtos_lista.column("#0", width=5, stretch=NO)
        self.produtos_lista.column("#1", width=100, stretch=NO)
        self.produtos_lista.column("#2", width=130, stretch=NO)
        self.produtos_lista.column("#3", width=76, stretch=NO)
        self.produtos_lista.column("#4", width=150, stretch=NO)
        self.produtos_lista.column("#5", width=75, stretch=NO)
        self.produtos_lista.column("#6", width=120, stretch=NO)
        self.produtos_lista.place(relx=-0.009, rely=0, relwidth=1.001, relheight=1.05)
        self.produtos_lista.bind("<Double-1>", self.on_double_click)
        self.produtos_lista.bind("<Button-3>", self.on_right_click)

        ### Sroll Bar
        self.sroll = Scrollbar(self.bodyFrame1_Produtos, orient="vertical")
        self.sroll.configure(command=self.produtos_lista.yview)
        self.produtos_lista.configure(yscroll=self.sroll.set)
        self.sroll.place(relx=0.94, rely=0.04, relwidth=0.051, relheight=0.96)
        self.lista_produtos()

        ### Decorar a Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.map('Treeview',background=[('selected', '#FD9C3A'), ('!selected', '#2E3133')],foreground=[('selected', 'black'), ('!selected', 'white')],)
        style.map('Treeview.Heading',foreground=[('selected', 'white')])
        style.configure('Treeview.Heading', background="#FD9C3A")
        style.configure('Treeview',rowheight=35)

        ## Frame 2 (Quantidade de Produtos)
        self.bodyFrame3_Produtos = Frame(self.frameProdutos, bg="#2E3133")
        self.bodyFrame3_Produtos.place(x=730, y=90, width=310, height=150)

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
        self.N_produtosFrame3_Produtos.place(x=115, y=65)

        ## Frame 4 (Adicionar Produto)
        self.bodyFrame4_Produtos = Frame(self.frameProdutos, bg="#2E3133")
        self.bodyFrame4_Produtos.place(x=730, y=285, width=310 , height=455)

        ### Label a dizer Alterar Produtos
        self.LabelAlterarProduto = Label(self.bodyFrame4_Produtos, bg="#2E3133", text="Alteral Produtos", font=("", 15, "bold"),fg='white')
        self.LabelAlterarProduto.place(x=25, y=25)

        ### Linha
        self.lineFrame4_Produtos = Label(self.bodyFrame4_Produtos, text="______________________",font=("", 10, "bold"), fg='#FD9C3A', bg='#2E3133')
        self.lineFrame4_Produtos.place(x=25, y=0)

        ### Imagen de um certo para aceitar
        CertoImage = ImageTk.PhotoImage(Image.open('../imagens/aceitar.png'))
        self.aceitar = Label(self.bodyFrame4_Produtos, image=CertoImage, bg='#2E3133')
        self.aceitar.image = CertoImage
        self.aceitar.place(x=260, y=25)
        self.aceitar.bind("<Button-1>", lambda event: self.adicionar_produto())

        ### Imagen de uma vassoura para limpar as entrys
        VassouraImage = ImageTk.PhotoImage(Image.open('../imagens/limpar.png'))
        self.limpar = Label(self.bodyFrame4_Produtos, image=VassouraImage, bg='#2E3133')
        self.limpar.image = VassouraImage
        self.limpar.place(x=225, y=25)
        self.limpar.bind("<Button-1>", lambda event: self.Limpar())

        ### Nome do Produto
        self.nomeProduto = Label(self.bodyFrame4_Produtos, text="Nome do Produto ", font=("", 10, "bold"), fg='white', bg='#2E3133')
        self.nomeProduto.place(x=15, y=75)
        self.labelProduto = Label(self.bodyFrame4_Produtos, text=": ", font=("", 10, "bold"), fg='#FD9C3A', bg='#2E3133')
        self.labelProduto.place(x=130, y=75)
        self.Textbox_Produtos = Entry(self.bodyFrame4_Produtos,bg='#2E3133',fg='white')
        self.Textbox_Produtos.place(x=140, y=75,width=100 , height=25)

        ### Preço
        self.Preço_Produto = Label(self.bodyFrame4_Produtos, text="Preço ", font=("", 10, "bold"), fg='white', bg='#2E3133')
        self.Preço_Produto.place(x=15, y=105)
        self.LabelPreço = Label(self.bodyFrame4_Produtos, text=": ", font=("", 10, "bold"), fg='#FD9C3A', bg='#2E3133')
        self.LabelPreço.place(x=57, y=105)
        self.Textbox_Preco = Entry(self.bodyFrame4_Produtos,bg='#2E3133',fg='white')
        self.Textbox_Preco.place(x=70, y=105,width=45 , height=25)
        self.LabelEuro = Label(self.bodyFrame4_Produtos, text="€ ", font=("", 10, "bold"), fg='#FD9C3A', bg='#2E3133')
        self.LabelEuro.place(x=117,y=105)

        ###Descrição
        self.LabelDescrição = Label(self.bodyFrame4_Produtos, text="Descrição ", font=("", 10, "bold"), fg='white', bg='#2E3133')
        self.LabelDescrição.place(x=15,y=137)
        self.LabelDescriçãoPontos = Label(self.bodyFrame4_Produtos, text=": ", font=("", 10, "bold"), fg='#FD9C3A', bg='#2E3133')
        self.LabelDescriçãoPontos.place(x=80,y=137)
        self.TextBox_Descrição = Text(self.bodyFrame4_Produtos, bg='#2E3133', fg='white')
        self.TextBox_Descrição.place(x=90, y=135, width=150, height=100)

        ### Produto
        self.LabelImagem= Label(self.bodyFrame4_Produtos,text="Imagem ", font=("", 10, "bold"), fg='white', bg='#2E3133')
        self.LabelImagem.place(x=15,y=240)
        self.LabelImagemPontos = Label(self.bodyFrame4_Produtos,text=": ", font=("", 10, "bold"), fg='#FD9C3A', bg='#2E3133')
        self.LabelImagemPontos.place(x=70,y=240)

        ### Botão para Adicionar Imagem / Alterar Imagem
        self.nova_imagem = Button(self.bodyFrame4_Produtos, text="Adicione uma imagem", command=lambda : self.inserir_imagem() ,bg='#2E3133', font=("", 10, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=20)
        self.nova_imagem.place(x=79, y=240)

        ### Try que serve para abrir o programa sem imagem, e quando tiver imagem vai aparecer acho(?)
        try:
            ImagemProduto = ImageTk.PhotoImage(Image.open('../imagens/semImagem.png').resize((250, 135)))
            self.logo = Label(self.bodyFrame4_Produtos, image=ImagemProduto, bg='#2E3133',bd=1)
            self.logo.image = ImagemProduto
            self.logo.place(x=15, y=275)
        except FileNotFoundError:
            print("Erro:'Imagem não Encontrada'")
            self.nova_imagem = Button(self.bodyFrame4_Produtos, text="Adicione uma imagem", command=lambda : self.inserir_imagem() ,bg='#2E3133', font=("", 10, "bold"), fg='white',cursor='hand2', activebackground='#FD9C3A', bd=5, width=20)
            self.nova_imagem.place(x=79, y=240)

        #Puxar a janela do inicio para cima quando o programa abrir
        self.frameInicio.lift()

def win():
    window = Tk()
    Dashboard(window)
    window.mainloop()

if __name__ == "__main__":
    win()   
