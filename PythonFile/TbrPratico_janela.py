from tkinter import *
import tkinter as tkk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class Func:

    def conecta_bd(self): #faz conexao á base de dados
        self.conn = sqlite3.connect("../BD/Rissois.db")
        self.cursor = self.conn.cursor()
    def desconecta_bd(self):#desliga a conexao á base de dados
        self.conn.close()
    def contar_clientes(self):#função pra contar o numero de clientes pra por automatico quando se adciona um novo cliente
        self.conecta_bd()
        resultado = self.cursor.execute("SELECT COUNT(*) FROM Clientes").fetchone()
        self.desconecta_bd()
        return resultado[0]
    def contar_Produtos(self): #função para contar o numero de produtos pra por automatico quando se adciona
        self.conecta_bd()
        resultado = self.cursor.execute("SELECT COUNT(*) FROM Produtos").fetchone()
        self.desconecta_bd()
        return resultado[0]
    def buscar_produtos(self):#cria um dicionario com os nomes dos produtos para por em radiobuttons para depois escolher
        self.conecta_bd()
        produtos  = self.cursor.execute("SELECT nome_produto FROM Produtos").fetchall()
        self.desconecta_bd()
        return [produto[0] for produto in produtos]
    def inserir_cliente(self):#comando para inserir um novo cliente na base de dados
        nome = self.tx_nome_cliente.get()
        contacto = self.tx_Contacto.get()
        self.conecta_bd()
        self.cursor.execute("INSERT INTO Clientes (nome_cliente, contacto) VALUES (?, ?)", (nome, contacto))
        self.conn.commit()
        self.desconecta_bd()
        messagebox.showinfo('Sucesso', 'Cliente inserido com sucesso')
    def inserir_produto(self):#comando para inserir um novo produto na base de dados
        nome = self.tx_nome_cliente.get()
        preco = self.tx_preco.get()
        self.conecta_bd()
        self.cursor.execute("INSERT INTO Produtos (nome_produto, preco) VALUES (?, ?)", (nome, preco))
        self.conn.commit()
        self.desconecta_bd()
        messagebox.showinfo('Sucesso', 'Produto inserido com sucesso')
    def inserir_encomenda(self, nome_cliente, quantidades):#faz inserir uma nova encomenda na base de dados (liga o encomenda_id com o cliente_id)
        self.conecta_bd()
        fritos_congelados = self.obter_checkbox_status()[::2] #o array de fritos congelados estava duplicado por isso tirei todos os dados duplicados com aquele comando
        resultado_encomendas = self.cursor.execute("SELECT COUNT(DISTINCT id_Encomendas) AS total_encomendas FROM Encomendas;").fetchone()

        if resultado_encomendas:
            id_encomenda = resultado_encomendas[0] + 1

            self.cursor.execute('SELECT id_clientes FROM Clientes WHERE nome_cliente = ?', (nome_cliente,))
            resultado_cliente = self.cursor.fetchone()

            if resultado_cliente:
                id_cliente = resultado_cliente[0]
                self.cursor.execute("INSERT INTO Encomendas VALUES (?, ?)", (id_encomenda, id_cliente))
                self.conn.commit()
                messagebox.showinfo('Sucesso', 'Encomenda inserida com sucesso')
            else:
                messagebox.showerror('Erro', 'Cliente ' +nome_cliente+ 'não encontrado.')
        else:
            messagebox.showerror('Erro', 'Erro ao obter o número total de encomendas')

        for i, quantidade in enumerate(quantidades):
            if int(quantidade) > 0:
                self.inserir_linha_encomenda(id_encomenda, id_cliente, i + 1, quantidade,fritos_congelados[i])
        self.desconecta_bd()
    def inserir_linha_encomenda(self, id_encomenda, id_cliente, id_produto, quantidade,fritos_congelados):#insere na tabela principal da base de dados usa o mesmo id_encomenda para adicionar varios produtos
        self.conecta_bd()
        data_encomenda = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            """INSERT INTO Linha_de_Encomenda (Encomendas_id_Encomendas, Produtos_id_produto, congelados, data_encomenda, quantidade) VALUES (?, ?, ?, ?, ?);""",
            (id_encomenda, id_produto, fritos_congelados, data_encomenda, quantidade))
        self.conn.commit()
        self.select_list()
        self.desconecta_bd()
    def lista_clientes(self):#faz o select que vai mostrar os clientes e as suas informações
        self.clientes_lista.delete(*self.clientes_lista.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("select id_clientes, nome_cliente, contacto from Clientes order by id_clientes")
        for i in lista:
            self.clientes_lista.insert("", "end", values=i)
            self.clientes_lista.update()
        self.desconecta_bd()
    def lista_produtos(self):#faz o select que vai mostrar os produtos e as suas informações
        self.produtos_lista.delete(*self.produtos_lista.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("select id_produto, nome_produto, preco from Produtos order by id_produto")
        for i in lista:
            self.produtos_lista.insert("", "end", values=i)
            self.produtos_lista.update()
        self.desconecta_bd()
    def select_list(self): #select que mostra a linha de encomendas com alguns extras para facilitar a leitura
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(
            """SELECT
                E.id_Encomendas AS id_encomenda,
                C.nome_cliente,
                P.nome_produto,
                CASE
                    WHEN P.nome_produto LIKE '%Rissol%' THEN
                        CASE
                            WHEN LE.congelados = 1 THEN 'Frito'
                            WHEN LE.congelados = 0 THEN 'Congelado'
                        END
                    WHEN P.nome_produto IN ('Trouxas de Frango', 'Croquetes') THEN
                        CASE
                            WHEN LE.congelados = 1 THEN 'Frito'
                            WHEN LE.congelados = 0 THEN 'Congelado'
                        END
                    ELSE '-------------'
                END AS estado,
                LE.data_encomenda,
                LE.quantidade,
                (LE.quantidade * CAST(P.preco AS DECIMAL)) || ' €' AS total_a_pagar
            FROM
                Encomendas E
                JOIN Clientes C ON E.id_clientes = C.id_clientes
                JOIN Linha_de_Encomenda LE ON E.id_Encomendas = LE.Encomendas_id_Encomendas
                JOIN Produtos P ON LE.Produtos_id_produto = P.id_produto
            ORDER BY id_encomenda DESC;""")

        for row in lista.fetchall():
            self.listaCli.insert("", "end", values=row)
        self.listaCli.update()
        self.desconecta_bd()
    def bucar_nomes_clientes(self):#select que vai buscar os nomes dos clientes todos para quando estou a fazer uma encomenda saber que clientes existem
        self.conecta_bd()
        clientes = self.cursor.execute("SELECT nome_cliente FROM Clientes order by nome_cliente asc").fetchall()
        self.desconecta_bd()
        return [cliente[0] for cliente in clientes]
    def obter_quantidades(self):
        quantidades = []
        for entry in self.quantidade_entries:
            quantidade = entry.get()
            quantidades.append(quantidade if quantidade else 0)
        return quantidades
    def obter_nome_produto(self):
        nomes_produtos = []
        self.conecta_bd()
        self.cursor.execute("SELECT nome_produto FROM Produtos")
        resultados = self.cursor.fetchall()
        for resultado in resultados:
            nomes_produtos.append(resultado[0])
            self.desconecta_bd()
        return nomes_produtos
    def obter_checkbox_status(self):#verifica as checkboxes que estao selecionadas (Por alguma razao os dados duplicam por isso eu cortei o array de dois em dois para os dados ficarem usaveis)
        checkbox_status = []
        for check_var in self.check_var_list:
            status = check_var.get()
            if status == 1:
                checkbox_status.append(1)
            else:
                checkbox_status.append(0)
        fritos_congelados = checkbox_status[::2]
        return checkbox_status
    def onDoubleClick_clientes(self, event):#Double click para buscar os dados dos clientes que estão na trewview
        selected_item = self.clientes_lista.selection()
        for item_id in selected_item:
            col1, col2, col3 = self.clientes_lista.item(item_id, 'values')
            self.tx_n_cliente.delete(0, END)
            self.tx_n_cliente.insert(END, col1)
            self.tx_nome_cliente.delete(0, END)
            self.tx_nome_cliente.insert(END, col2)
            self.tx_Contacto.delete(0, END)
            self.tx_Contacto.insert(END, col3)
    def onDoubleClick_produtos(self, event):#Double click para buscar os dados dos produtos que estão na trewview
        selected_item = self.produtos_lista.selection()
        for item_id in selected_item:
            col1, col2, col3 = self.produtos_lista.item(item_id, 'values')
            self.tx_produto.delete(0, END)
            self.tx_produto.insert(END, col1)
            self.tx_nome_produto.delete(0, END)
            self.tx_nome_produto.insert(END, col2)
            self.tx_Preço.delete(0, END)
            self.tx_Preço.insert(END, col3)
    def onDoubleClick_encomendas(self, event):
        selected_item = self.encomenda_lista.selection()
        for item_id in selected_item:
            col1, col2, col3, _, col5 = self.encomenda_lista.item(item_id, 'values')
            self.combo_produto.set(col2)
            self.cbtn_fritos_congelados.deselect()
            if col3 == 'Frito':
                self.cbtn_fritos_congelados.select()
            self.txt_quantidade.delete(0, END)
            self.txt_quantidade.insert(END, col5)
    def procurar_por_id_clients(self):#procura um cliente pelo ID e preenche o resto dos campos automaticamente
        id = int(self.tx_n_cliente.get())
        self.conecta_bd()
        strr = 'SELECT * FROM Clientes WHERE id_clientes = ?'
        self.cursor.execute(strr, (id,))
        result = self.cursor.fetchone()
        if result:
            self.tx_n_cliente.delete(0, END)
            self.tx_n_cliente.insert(0, result[0])
            self.tx_nome_cliente.delete(0, END)
            self.tx_nome_cliente.insert(0, result[1])
            self.tx_Contacto.delete(0, END)
            self.tx_Contacto.insert(0, result[2])
        else:
            messagebox.showerror('Erro', 'Cliente com ID ' +id+' não encontrado', parent=self.root)
        self.desconecta_bd()
    def procurar_por_id_produto(self):#procura um produto pelo ID e preenche o resto dos campos automaticamente
        id = int(self.tx_produto.get())
        self.conecta_bd()
        strr = 'SELECT * FROM Produtos WHERE id_produto = ?'
        self.cursor.execute(strr, (id,))
        result = self.cursor.fetchone()
        if result:
            self.tx_produto.delete(0, END)
            self.tx_produto.insert(0, result[0])
            self.tx_nome_produto.delete(0, END)
            self.tx_nome_produto.insert(0, result[1])
            self.tx_Preço.delete(0, END)
            self.tx_Preço.insert(0, result[2])
        else:
            messagebox.showerror('Erro', 'Produto com ID ' +id+ 'não encontrado', parent=self.root)
        self.desconecta_bd()
    def procurar_encomenda(self):
        self.encomenda_lista.delete(*self.encomenda_lista.get_children())
        self.conecta_bd()
        id = int(self.tx_n_cliente.get())
        lista = self.cursor.execute('''SELECT
    LE.Encomendas_id_Encomendas,
    P.nome_produto,
    CASE
        WHEN P.nome_produto LIKE '%Rissol%' THEN
            CASE
                WHEN LE.congelados = 1 THEN 'Frito'
                WHEN LE.congelados = 0 THEN 'Congelado'
            END
        WHEN P.nome_produto IN ('Trouxas de Frango', 'Croquetes') THEN
            CASE
                WHEN LE.congelados = 1 THEN 'Frito'
                WHEN LE.congelados = 0 THEN 'Congelado'
            END
        ELSE '----------'
    END AS congelado_frito,
    LE.data_encomenda,
    LE.quantidade
FROM
    Linha_de_Encomenda LE
JOIN
    Produtos P ON LE.Produtos_id_produto = P.id_produto
WHERE
    LE.Encomendas_id_Encomendas = ?; ''',(id,) )
        for i in lista:
            self.encomenda_lista.insert("", "end", values=i)
            self.encomenda_lista.update()
        self.conecta_bd()
        self.cursor.execute('''SELECT C.nome_cliente
                    FROM Linha_de_Encomenda LE
                    JOIN Produtos P ON LE.Produtos_id_produto = P.id_produto
                    JOIN Encomendas E ON LE.Encomendas_id_Encomendas = E.id_Encomendas
                    JOIN Clientes C ON E.id_clientes = C.id_clientes
                    WHERE LE.Encomendas_id_Encomendas = ?
                    GROUP by C.nome_cliente''',(id,) )

        verificar_nome_cliente = self.cursor.fetchone()

        if verificar_nome_cliente:
            nome_cliente = verificar_nome_cliente[0]
            self.lbl_nome_cliente.config(text='Cliente ' + str(nome_cliente))
        else:
            self.lbl_nome_cliente.config(text='Cliente não encontrado')

        self.desconecta_bd()
    def confirmar_modificacao_clientes(self):#confirma a modificação de um cliente
        id_cliente = self.tx_n_cliente.get()
        novo_nome = self.tx_nome_cliente.get()
        novo_contato = self.tx_Contacto.get()
        if not id_cliente:
            messagebox.showerror('Erro', 'Por favor, insira o ID do cliente', parent=self.lista_clientes_window)
            return
        self.conecta_bd()
        self.cursor.execute('SELECT * FROM Clientes WHERE id_clientes = ?', (id_cliente,))
        resultado = self.cursor.fetchone()
        if resultado:
            self.cursor.execute('UPDATE Clientes SET nome_cliente = ?, contacto = ? WHERE id_clientes = ?',
                                (novo_nome, novo_contato, id_cliente))
            self.conn.commit()
            messagebox.showinfo('Sucesso', 'Registo modificado com sucesso', parent=self.lista_clientes_window)
            self.lista_clientes()
        else:
            messagebox.showerror('Erro', f'Cliente com ID ' +id_cliente+ 'não encontrado', parent=self.lista_clientes_window)
        self.desconecta_bd()
    def confirmar_modificacao_produtos(self):#confirma a modificação de um produto
        id_produto = self.tx_produto.get()
        novo_nome = self.tx_nome_produto.get()
        novo_preco = self.tx_Preço.get()
        if not id_produto:
            messagebox.showerror('Erro', 'Por favor, insira o ID do Produto', parent=self.lista_produtos_window)
            return
        self.conecta_bd()
        self.cursor.execute('SELECT * FROM Produtos WHERE id_produto = ?', (id_produto,))
        resultado = self.cursor.fetchone()
        if resultado:
            self.cursor.execute('UPDATE Produtos SET nome_produto = ?, preco = ? WHERE id_produto = ?',
                                (novo_nome, novo_preco, id_produto))
            self.conn.commit()
            messagebox.showinfo('Sucesso', 'Registo modificado com sucesso', parent=self.lista_produtos_window)
            self.lista_produtos()
        else:
            messagebox.showerror('Erro', 'Cliente com ID' +id_produto+' não encontrado', parent=self.lista_clientes_window)
        self.desconecta_bd()
    def confirmar_nova_encomenda(self ):#função que vai buscar as quantidades e , vai buscra se estao fritos ou nao e manda para outra função que confirma a encomenda
        self.conecta_bd()
        item_selecionado = self.combo_cliente.get()
        quantidades= self.obter_quantidades()
        self.inserir_encomenda(item_selecionado,quantidades)
        self.desconecta_bd()
    def apagar_linha_encomenda(self):
        self.conecta_bd()
        id_cliente = int(self.tx_n_cliente.get())
        nome_produto = self.combo_produto.get()
        self.cursor.execute('''SELECT id_produto FROM Produtos WHERE nome_produto = ?''', (nome_produto,))
        resultado = self.cursor.fetchone()
        if resultado:
            id_produto = resultado[0]
            self.cursor.execute(
                "DELETE FROM Linha_de_Encomenda WHERE Encomendas_id_Encomendas = ? AND Produtos_id_produto = ?",
                (id_cliente, id_produto))
            self.conn.commit()
            self.desconecta_bd()
            messagebox.showinfo('Sucesso', 'Encomenda apagada com sucesso')
            self.encomenda_lista.update()
            self.procurar_encomenda()
            self.select_list()
        else:
            messagebox.showerror('Erro', 'Produto não encontrado na base de dados')
    def adicionar_linha_encomenda(self):
        self.conecta_bd()
        nome_produto = self.combo_produto.get()
        id_produto = self.cursor.execute("SELECT id_produto FROM Produtos WHERE nome_produto = ?", (nome_produto,))
        id_produto = id_produto.fetchone()[0]
        id = int(self.tx_n_cliente.get())
        data = self.cursor.execute('''SELECT data_encomenda FROM Linha_de_Encomenda
                                        WHERE Encomendas_id_Encomendas = ?
                                        GROUP BY Encomendas_id_Encomendas''', (id,)).fetchone()[0]
        quantidade = int(self.txt_quantidade.get())
        self.cursor.execute('''insert into Linha_de_Encomenda VALUES (?,?,?,?,?);''',
                            (id, id_produto, 0, data, quantidade))
        self.conn.commit()
        self.desconecta_bd()
        self.procurar_encomenda()
        self.select_list()

class application(Func):
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.select_list()
        self.root.mainloop()
    def tela(self):#tela principal da aplicação
        self.root.title("Rissois Lda.")
        self.root.configure(background="light blue")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        self.root.maxsize(width=1000, height=600)
        self.root.minsize(width=1000, height=600)
    def frames_da_tela(self):#os dois frames da tela principal que vão ter as funções principais
        self.frame_1 = Frame(self.root, bd=4, bg="lightblue", highlightbackground="black", highlightthickness=2)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.1)
        self.frame_2 = Frame(self.root, bd=4, bg="lightblue", highlightbackground="black", highlightthickness=2)
        self.frame_2.place(relx=0.02, rely=0.15, relwidth=0.96, relheight=0.80)
    def widgets_frame1(self):#os butoes que aparecem na tela principal
        self.bt_novo_cliente = Button(self.frame_1, text="Novo Cliente", bd=2, bg="yellow", fg="black",
                                    font=("comic Sans", 8, "bold"), command=self.janela_mais_clientes)
        self.bt_novo_cliente.place(relx=0.01, rely=0.1, relwidth=0.15, relheight=0.8)

        self.bt_lista_cliente = Button(self.frame_1, text="Lista Clientes", bd=2, bg="yellow", fg="black",
                                    font=("comic Sans", 8, "bold"),command=self.janela_lista_clientes)
        self.bt_lista_cliente.place(relx=0.68, rely=0.1, relwidth=0.15, relheight=0.8)

        self.bt_lista_produtos = Button(self.frame_1, text="Lista Produtos", bd=2, bg="yellow", fg="black",
                                    font=("comic Sans", 8, "bold"),command=self.janela_lista_produtos)
        self.bt_lista_produtos.place(relx=0.84, rely=0.1, relwidth=0.15, relheight=0.8)

        self.bt_novo_produto = Button(self.frame_1, text="Novo Produto", bd=2, bg="yellow", fg="black",
                                    font=("comic Sans", 8, "bold"), command=self.janela_novo_produto)
        self.bt_novo_produto.place(relx=0.17, rely=0.1, relwidth=0.15, relheight=0.80)

        self.bt_nova_encomendas = Button(self.frame_1, text="Nova encomenda", bd=2, bg="yellow", fg="black",
                                    font=("comic Sans", 8, "bold"), command=self.janela_nova_encomenda)
        self.bt_nova_encomendas.place(relx=0.33, rely=0.1, relwidth=0.15, relheight=0.80)

        self.bt_lista_encomendas = Button(self.frame_1, text="Lista encomenda", bd=2, bg="yellow", fg="black",
                                    font=("comic Sans", 8, "bold"),command=self.janela_lista_encomendas)
        self.bt_lista_encomendas.place(relx=0.52, rely=0.1, relwidth=0.15, relheight=0.80)
    def lista_frame2(self):# a treeview que aparece na tela principal com o select que  mostra a linha de encomendas
        self.listaCli = ttk.Treeview(self.frame_2, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Encomenda")
        self.listaCli.heading("#2", text="Cliente")
        self.listaCli.heading("#3", text="Produto")
        self.listaCli.heading("#4", text="Congelado/Frito")
        self.listaCli.heading("#5", text="Data")
        self.listaCli.heading("#6", text="Quantidade")
        self.listaCli.heading("#7", text="Total")

        self.listaCli.column("#0", width=1, stretch=NO)
        self.listaCli.column("#1", width=125, stretch=NO)
        self.listaCli.column("#2", width=125, stretch=NO)
        self.listaCli.column("#3", width=125, stretch=NO)
        self.listaCli.column("#4", width=125, stretch=NO)
        self.listaCli.column("#5", width=125, stretch=NO)
        self.listaCli.column("#6", width=125, stretch=NO,anchor="center")
        self.listaCli.column("#7", width=125, stretch=NO,anchor="center")
        self.listaCli.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.95)

        self.sroll = Scrollbar(self.frame_2, orient="vertical")
        self.sroll.configure(command=self.listaCli.yview)
        self.listaCli.configure(yscroll=self.sroll.set)
        self.sroll.place(relx=0.93, rely=0.011, relwidth=0.06, relheight=0.945)
    def janela_lista_clientes(self):  # cria uma janela para mostrar os clientes
        self.lista_clientes_window = Toplevel(self.root)
        self.lista_clientes_window.grab_set()
        self.lista_clientes_window.geometry('600x400')
        self.lista_clientes_window.title('Lista de Clientes')
        self.lista_clientes_window.configure(background="light blue")

        self.lista_clientes_window.maxsize(width=600, height=400)
        self.lista_clientes_window.minsize(width=600, height=400)

        self.clientes_lista = ttk.Treeview(self.lista_clientes_window, columns=("col1", "col2", "col3",))
        self.clientes_lista.heading("#0", text="")
        self.clientes_lista.heading("#1", text="ID")
        self.clientes_lista.heading("#2", text="Cliente")
        self.clientes_lista.heading("#3", text="Contacto")

        self.clientes_lista.column("#0", width=1, stretch=NO)
        self.clientes_lista.column("#1", width=100, stretch=NO)
        self.clientes_lista.column("#2", width=100, stretch=NO)
        self.clientes_lista.column("#3", width=100, stretch=NO)

        self.clientes_lista.place(relx=0.01, rely=0.01, relwidth=0.5, relheight=0.95)

        self.sroll = Scrollbar(self.lista_clientes_window, orient="vertical")
        self.sroll.configure(command=self.clientes_lista.yview)
        self.clientes_lista.configure(yscroll=self.sroll.set)
        self.sroll.place(relx=0.49, rely=0.012, relwidth=0.03, relheight=0.945)

        self.lista_clientes()

        self.Cancelar = Button(self.lista_clientes_window, text="Confirmar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"), command=self.confirmar_modificacao_clientes)
        self.Cancelar.place(relx=0.60, rely=0.8)

        self.Cancelar = Button(self.lista_clientes_window, text="Cancelar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"),command=self.lista_clientes_window.destroy)
        self.Cancelar.place(relx=0.75, rely=0.8)

        self.Procurar = Button(self.lista_clientes_window, text="Procurar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"), command=self.procurar_por_id_clients)
        self.Procurar.place(relx=0.8, rely=0.2)

        self.lb_Tit = Label(self.lista_clientes_window, text="Modificar Cliente", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_Tit.place(relx=0.6, rely=0)

        self.lb_n_cliente = Label(self.lista_clientes_window, text="Cliente: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_n_cliente.place(relx=0.52, rely=0.2)
        self.tx_n_cliente = Entry(self.lista_clientes_window)
        self.tx_n_cliente.place(relx=0.66, rely=0.197, relwidth=0.05, relheight=0.077)

        self.lb_Nome_cliente = Label(self.lista_clientes_window, text="Nome: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_Nome_cliente.place(relx=0.52, rely=0.40)
        self.tx_nome_cliente = Entry(self.lista_clientes_window)
        self.tx_nome_cliente.place(relx=0.64, rely=0.397, relwidth=0.248, relheight=0.077)

        self.lb_Contacto = Label(self.lista_clientes_window, text="Contacto: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_Contacto.place(relx=0.52, rely=0.6)
        self.tx_Contacto = Entry(self.lista_clientes_window)
        self.tx_Contacto.place(relx=0.69,  rely=0.597, relwidth=0.248, relheight=0.079)


        self.clientes_lista.bind("<Double-1>", self.onDoubleClick_clientes)
    def janela_lista_produtos(self):  # cria uma janela para mostrar os produtos
        self.lista_produtos_window = Toplevel(self.root)
        self.lista_produtos_window.grab_set()
        self.lista_produtos_window.geometry('600x400')
        self.lista_produtos_window.title('Lista de Produtos')
        self.lista_produtos_window.configure(background="light blue")

        self.lista_produtos_window.maxsize(width=600, height=400)
        self.lista_produtos_window.minsize(width=600, height=400)

        self.produtos_lista = ttk.Treeview(self.lista_produtos_window, columns=("col1", "col2", "col3",))
        self.produtos_lista.heading("#0", text="")
        self.produtos_lista.heading("#1", text="Produto")
        self.produtos_lista.heading("#2", text="Nome")
        self.produtos_lista.heading("#3", text="Preço")

        self.produtos_lista.column("#0", width=1, stretch=NO)
        self.produtos_lista.column("#1", width=100, stretch=NO)
        self.produtos_lista.column("#2", width=100, stretch=NO)
        self.produtos_lista.column("#3", width=100, stretch=NO)

        self.produtos_lista.place(relx=0.01, rely=0.01, relwidth=0.5, relheight=0.95)

        self.sroll = Scrollbar(self.lista_produtos_window, orient="vertical")
        self.sroll.configure(command=self.produtos_lista.yview)
        self.produtos_lista.configure(yscroll=self.sroll.set)
        self.sroll.place(relx=0.49, rely=0.012, relwidth=0.03, relheight=0.945)

        self.lista_produtos()

        self.Confirmar = Button(self.lista_produtos_window, text="Confirmar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"), command=self.confirmar_modificacao_produtos)
        self.Confirmar.place(relx=0.60, rely=0.8)

        self.Cancelar = Button(self.lista_produtos_window, text="Cancelar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"),command=self.lista_produtos_window.destroy)
        self.Cancelar.place(relx=0.75, rely=0.8)

        self.Procurar = Button(self.lista_produtos_window, text="Procurar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"), command=self.procurar_por_id_produto)
        self.Procurar.place(relx=0.8, rely=0.2)

        self.lb_Tit = Label(self.lista_produtos_window, text="Modificar Produto", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_Tit.place(relx=0.6, rely=0)

        self.lb_produto = Label(self.lista_produtos_window, text="Produto: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_produto.place(relx=0.52, rely=0.2)
        self.tx_produto = Entry(self.lista_produtos_window)
        self.tx_produto.place(relx=0.68, rely=0.197, relwidth=0.05, relheight=0.077)

        self.lb_Nome_produto = Label(self.lista_produtos_window, text="Nome: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_Nome_produto.place(relx=0.52, rely=0.40)
        self.tx_nome_produto = Entry(self.lista_produtos_window)
        self.tx_nome_produto.place(relx=0.64, rely=0.397, relwidth=0.248, relheight=0.077)

        self.lb_Preço = Label(self.lista_produtos_window, text="Preço: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_Preço.place(relx=0.52, rely=0.6)
        self.tx_Preço = Entry(self.lista_produtos_window)
        self.tx_Preço.place(relx=0.644,  rely=0.597, relwidth=0.148, relheight=0.079)

        self.produtos_lista.bind("<Double-1>", self.onDoubleClick_produtos)
    def janela_mais_clientes(self):#cria a janela de novos clientes
        num_clientes = self.contar_clientes()
        self.mais_clientes = Toplevel(self.root)
        self.mais_clientes.grab_set()
        self.mais_clientes.geometry('400x250')
        self.mais_clientes.title('Mais Clientes')
        self.mais_clientes.configure(background="light blue")

        self.mais_clientes.maxsize(width=400, height=250)
        self.mais_clientes.minsize(width=400, height=250)

        self.lb_Tit = Label(self.mais_clientes, text="Adicionar novo Cliente", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_Tit.place(relx=0.225, rely=0)

        self.lb_n_cliente = Label(self.mais_clientes, text="Cliente Nº: " + str(num_clientes + 1), fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_n_cliente.place(relx=0, rely=0.2)

        self.lb_Nome_cliente = Label(self.mais_clientes, text="Nome: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_Nome_cliente.place(relx=0, rely=0.40)
        self.tx_nome_cliente = Entry(self.mais_clientes)
        self.tx_nome_cliente.place(relx=0.185, rely=0.4, relwidth=0.35, relheight=0.118)

        self.lb_Contacto = Label(self.mais_clientes, text="Contacto: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_Contacto.place(relx=0, rely=0.6)
        self.tx_Contacto = Entry(self.mais_clientes)
        self.tx_Contacto.place(relx=0.26, rely=0.6, relwidth=0.35, relheight=0.118)

        self.Confirmar = Button(self.mais_clientes, text="Confirmar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"), command=self.inserir_cliente)
        self.Confirmar.place(relx=0.3, rely=0.8)
        self.Cancelar = Button(self.mais_clientes, text="Cancelar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"),command=self.mais_clientes.destroy)
        self.Cancelar.place(relx=0.55, rely=0.8)
    def janela_novo_produto(self):#cria a janela de novos produtos
        num_produto = self.contar_Produtos()
        self.novo_produto = Toplevel(self.root)
        self.novo_produto.grab_set()
        self.novo_produto.geometry('400x250')
        self.novo_produto.title('Novo Produto')
        self.novo_produto.configure(background="light blue")

        self.novo_produto.maxsize(width=400, height=250)
        self.novo_produto.minsize(width=400, height=250)

        self.lb_Tit = Label(self.novo_produto, text="Adicionar novo Produto", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_Tit.place(relx=0.225, rely=0)

        self.lb_n_cliente = Label(self.novo_produto, text="Cliente Nº: " + str(num_produto + 1), fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_n_cliente.place(relx=0, rely=0.2)

        self.lb_Nome_cliente = Label(self.novo_produto, text="Nome: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_Nome_cliente.place(relx=0, rely=0.40)
        self.tx_nome_cliente = Entry(self.novo_produto)
        self.tx_nome_cliente.place(relx=0.185, rely=0.4, relwidth=0.35, relheight=0.118)

        self.lb_preco = Label(self.novo_produto, text="Preço: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_preco.place(relx=0, rely=0.6)
        self.tx_preco = Entry(self.novo_produto)
        self.tx_preco.place(relx=0.17, rely=0.6, relwidth=0.35, relheight=0.118)

        self.Confirmar = Button(self.novo_produto, text="Confirmar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"), command=self.inserir_produto)
        self.Confirmar.place(relx=0.3, rely=0.8)
        self.Cancelar = Button(self.novo_produto, text="Cancelar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"),command=self.novo_produto.destroy)
        self.Cancelar.place(relx=0.55, rely=0.8)
    def janela_nova_encomenda(self):#cria a janela de novas encomendas
        nomes_clientes = self.bucar_nomes_clientes()
        produtos = self.buscar_produtos()
        self.nova_encomenda = Toplevel(self.root)
        self.nova_encomenda.grab_set()
        self.nova_encomenda.geometry('400x550')
        self.nova_encomenda.title('Nova Encomenda')
        self.nova_encomenda.configure(background="light blue")

        self.nova_encomenda.maxsize(width=400, height=550)
        self.nova_encomenda.minsize(width=400, height=550)

        self.lb_Tit = Label(self.nova_encomenda, text="Adicionar nova Encomenda", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_Tit.place(relx=0.2, rely=0)

        self.lb_n_cliente = Label(self.nova_encomenda, text="Cliente: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_n_cliente.place(relx=0, rely=0.1)

        self.Confirmar = Button(self.nova_encomenda, text="Confirmar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"),command=self.confirmar_nova_encomenda)
        self.Confirmar.place(relx=0.3, rely=0.75)
        self.Cancelar = Button(self.nova_encomenda, text="Cancelar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"),command=self.nova_encomenda.destroy)
        self.Cancelar.place(relx=0.55, rely=0.75)

        self.combo_cliente = ttk.Combobox(self.nova_encomenda, values=nomes_clientes, state="readonly")
        self.combo_cliente.place(relx=0.2, rely=0.1, relwidth=0.35, relheight=0.058)

        self.canvas_produtos = Canvas(self.nova_encomenda, bg="light blue", width=1, height=1, background='white')
        self.canvas_produtos.place(relx=0.2, rely=0.2, relwidth=0.45, relheight=0.50)

        self.frame_checkbuttons = Frame(self.canvas_produtos)
        self.frame_checkbuttons.place(relx=0.1, rely=0.2, relwidth=0.95, relheight=0.50)
        self.canvas_produtos.create_window((20, 20), window=self.frame_checkbuttons, anchor="nw")

        #estas duas variaveis e o For foram feitas pelo ChatGPT pois eu nao sabia como fazer um ciclo automatico que fazia checkboxs e entrys para cada uma delas, obrigado pela compreensão
        self.check_var_list = []
        self.quantidade_entries = []

        for i, produto_nome in enumerate(produtos):
            check_var = IntVar()
            check_button = Checkbutton(self.frame_checkbuttons, text=produto_nome, variable=check_var)
            check_button.grid(row=i, column=0, sticky="w")

            quantidade_entry = Entry(self.frame_checkbuttons, width=5)
            quantidade_entry.grid(row=i, column=1, padx=(5, 0))

            self.quantidade_entries.append(quantidade_entry)

            self.check_var_list.append(check_var)
            self.check_var_list.append(check_var)

            self.frame_checkbuttons.update_idletasks()

        self.canvas_produtos.config(scrollregion=self.canvas_produtos.bbox("all"))
        self.scroll_canvas = Scrollbar(self.nova_encomenda, orient="vertical", command=self.canvas_produtos.yview)
        self.scroll_canvas.place(relx=0.65, rely=0.2, relwidth=0.06, relheight=0.50)
        self.canvas_produtos.configure(yscrollcommand=self.scroll_canvas.set)
    def janela_lista_encomendas(self):
        nomes_produtos = self.obter_nome_produto()
        self.lista_encomendas = Toplevel(self.root)
        self.lista_encomendas.grab_set()
        self.lista_encomendas.geometry('1000x1000')
        self.lista_encomendas.title('Lista de Encomendas')
        self.lista_encomendas.configure(background="light blue")

        self.lista_encomendas.maxsize(width=600, height=400)
        self.lista_encomendas.minsize(width=600, height=400)

        self.encomenda_lista = ttk.Treeview(self.lista_encomendas, columns=("col1", "col2", "col3","col4", "col5"))
        self.encomenda_lista.heading("#0", text="")
        self.encomenda_lista.heading("#1", text="ID")
        self.encomenda_lista.heading("#2", text="Produto")
        self.encomenda_lista.heading("#3", text="Congelados/Fritos")
        self.encomenda_lista.heading("#4", text="Data")
        self.encomenda_lista.heading("#5", text="Quantidades")

        self.encomenda_lista.column("#0", width=1, stretch=NO)
        self.encomenda_lista.column("#1", width=100, stretch=NO)
        self.encomenda_lista.column("#2", width=100, stretch=NO)
        self.encomenda_lista.column("#3", width=100, stretch=NO)
        self.encomenda_lista.column("#4", width=100, stretch=NO)
        self.encomenda_lista.column("#5", width=100, stretch=NO)

        self.encomenda_lista.place(relx=0.01, rely=0.01, relwidth=0.5, relheight=0.95)

        self.verical_srollbar = Scrollbar(self.lista_encomendas, orient="vertical")
        self.verical_srollbar.configure(command=self.encomenda_lista.yview)
        self.encomenda_lista.configure(yscroll=self.verical_srollbar.set)
        self.verical_srollbar.place(relx=0.49, rely=0.012, relwidth=0.03, relheight=0.945)

        self.horizontal_scrollbar = Scrollbar(self.lista_encomendas, orient=HORIZONTAL)
        self.horizontal_scrollbar.configure(command=self.encomenda_lista.xview)
        self.encomenda_lista.configure(xscroll=self.horizontal_scrollbar.set)
        self.horizontal_scrollbar.place(relx=0.01, rely=0.915, relwidth=0.49)

        self.Apagar = Button(self.lista_encomendas, text="Apagar", bd=2, bg="yellow", fg="black",
                            font=("comic Sans", 10, "bold"), command=self.apagar_linha_encomenda)
        self.Apagar.place(relx=0.76, rely=0.7)

        self.Adicionar = Button(self.lista_encomendas, text="Adicionar", bd=2, bg="yellow", fg="black",
                            font=("comic Sans", 10, "bold"), command=self.adicionar_linha_encomenda)
        self.Adicionar.place(relx=0.58, rely=0.7)

        self.Cancelar = Button(self.lista_encomendas, text="Cancelar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"), command=self.lista_encomendas.destroy)
        self.Cancelar.place(relx=0.685, rely=0.8)

        self.Procurar = Button(self.lista_encomendas, text="Procurar", bd=2, bg="yellow", fg="black",
                                font=("comic Sans", 10, "bold"),command= self.procurar_encomenda)
        self.Procurar.place(relx=0.85, rely=0.2)

        self.lb_Tit = Label(self.lista_encomendas, text="Modificar Encomenda", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_Tit.place(relx=0.6, rely=0)

        self.lbl_nome_cliente = Label(self.lista_encomendas, text="Cliente: ", fg="black",
                                  font=("comic Sans", 15, "bold"))
        self.lbl_nome_cliente.place(relx=0.52, rely=0.1)

        self.lb_n_cliente = Label(self.lista_encomendas, text="Encomenda: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lb_n_cliente.place(relx=0.52, rely=0.2)
        self.tx_n_cliente = Entry(self.lista_encomendas)
        self.tx_n_cliente.place(relx=0.735, rely=0.197, relwidth=0.05, relheight=0.077)

        self.lbl_Produto = Label(self.lista_encomendas, text="Produto: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lbl_Produto.place(relx=0.52, rely=0.3)

        self.combo_produto = ttk.Combobox(self.lista_encomendas, values=nomes_produtos, state="readonly")
        self.combo_produto.place(relx=0.679, rely=0.3, relwidth=0.3, relheight=0.076)

        self.lbl_fritos_congelados = Label(self.lista_encomendas, text="Fritos/Congelados: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lbl_fritos_congelados.place(relx=0.52, rely=0.4)

        self.cbtn_fritos_congelados = Checkbutton(self.lista_encomendas)
        self.cbtn_fritos_congelados.place(relx=0.85, rely=0.4, relwidth=0.1, relheight=0.076)

        self.lbl_quantidade = Label(self.lista_encomendas, text="Quantidade: ", fg="black",
                                font=("comic Sans", 15, "bold"))
        self.lbl_quantidade.place(relx=0.52, rely=0.5)
        self.txt_quantidade = Entry(self.lista_encomendas, width="5")
        self.txt_quantidade.place(relx=0.7299, rely=0.5, relwidth=0.1, relheight=0.076)

        self.lista_encomendas.bind("<Double-1>", self.onDoubleClick_encomendas)
application()
