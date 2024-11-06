import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2

# Conexão com o banco de dados
conn = psycopg2.connect(host='localhost', port='5432', database='Mercado', user='postgres', password='91257590')

def close_connection():
    conn.close()

# Funções de cadastro e manipulação de dados
def cadastrar_cliente():
    sql = "INSERT INTO CLIENTE (COD, NOME, TELEFONE, TOTAL_COMPRAS) VALUES (%s, %s, %s, %s);"
    cod = entry_cliente_cod.get()
    nome = entry_cliente_nome.get()
    telefone = entry_cliente_telefone.get()
    total_compras = 0  # Inicializando com 0
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (cod, nome, telefone, total_compras))
            conn.commit()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            limpar_campos_cliente()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar o cliente: {e}")

def limpar_campos_cliente():
    entry_cliente_cod.delete(0, tk.END)
    entry_cliente_nome.delete(0, tk.END)
    entry_cliente_telefone.delete(0, tk.END)

def cadastrar_produto():
    sql = "INSERT INTO PRODUTO (COD, NOME, VALOR_UN, QTD_ESTQ) VALUES (%s, %s, %s, %s);"
    cod = entry_produto_cod.get()
    nome = entry_produto_nome.get()
    valor_unitario = float(entry_produto_valor.get())
    quantidade_estoque = int(entry_produto_qtd.get())
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (cod, nome, valor_unitario, quantidade_estoque))
            conn.commit()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            limpar_campos_produto()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar o produto: {e}")

def limpar_campos_produto():
    entry_produto_cod.delete(0, tk.END)
    entry_produto_nome.delete(0, tk.END)
    entry_produto_valor.delete(0, tk.END)
    entry_produto_qtd.delete(0, tk.END)

def limpar_campos_venda():
    entry_venda_cliente_cod.delete(0, tk.END)
    entry_venda_data.delete(0, tk.END)
    entry_venda_pagamento.delete(0, tk.END)
    lista_produtos.clear()
    for row in tree.get_children():
        tree.delete(row)

def atualizar_estoque():
    produto_cod = entry_estoque_cod.get()
    nova_quantidade = int(entry_estoque_qtd.get())
    
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE PRODUTO SET QTD_ESTQ = %s WHERE COD = %s;", (nova_quantidade, produto_cod))
            conn.commit()
            messagebox.showinfo("Sucesso", "Estoque atualizado com sucesso!")
            limpar_campos_estoque()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao atualizar o estoque: {e}")

def limpar_campos_estoque():
    entry_estoque_cod.delete(0, tk.END)
    entry_estoque_qtd.delete(0, tk.END)

# Interface gráfica
def criar_abas():
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)

    aba_cliente = ttk.Frame(notebook)
    aba_produto = ttk.Frame(notebook)
    aba_venda = ttk.Frame(notebook)
    aba_estoque = ttk.Frame(notebook)
    aba_relatorios = ttk.Frame(notebook)

    notebook.add(aba_cliente, text="Clientes")
    notebook.add(aba_produto, text="Produtos")
    notebook.add(aba_venda, text="Vendas")
    notebook.add(aba_estoque, text="Estoque")
    notebook.add(aba_relatorios, text="Relatórios")

    interface_cliente(aba_cliente)
    interface_produto(aba_produto)
    interface_venda(aba_venda)
    
    # Aqui você incluiria as funções interface_produto, interface_venda, etc.

def interface_cliente(aba):
    tk.Label(aba, text="Cadastro de Clientes", font=("Arial", 12, "bold")).grid(row=0, columnspan=2, pady=(0, 10))

    tk.Label(aba, text="Código:").grid(row=1, column=0, sticky="e")
    global entry_cliente_cod
    entry_cliente_cod = ttk.Entry(aba)
    entry_cliente_cod.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(aba, text="Nome:").grid(row=2, column=0, sticky="e")
    global entry_cliente_nome
    entry_cliente_nome = ttk.Entry(aba)
    entry_cliente_nome.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(aba, text="Telefone:").grid(row=3, column=0, sticky="e")
    global entry_cliente_telefone
    entry_cliente_telefone = ttk.Entry(aba)
    entry_cliente_telefone.grid(row=3, column=1, padx=5, pady=5)

    ttk.Button(aba, text="Cadastrar Cliente", command=cadastrar_cliente).grid(row=4, columnspan=2, pady=10)

def interface_produto(aba):
    tk.Label(aba, text="Cadastro de Produtos", font=("Arial", 12, "bold")).grid(row=0, columnspan=2, pady=(0, 10))

    tk.Label(aba, text="Código:").grid(row=1, column=0, sticky="e")
    global entry_produto_cod
    entry_produto_cod = ttk.Entry(aba)
    entry_produto_cod.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(aba, text="Nome:").grid(row=2, column=0, sticky="e")
    global entry_produto_nome
    entry_produto_nome = ttk.Entry(aba)
    entry_produto_nome.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(aba, text="Valor Unitário:").grid(row=3, column=0, sticky="e")
    global entry_produto_valor
    entry_produto_valor = ttk.Entry(aba)
    entry_produto_valor.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(aba, text="Quantidade em Estoque:").grid(row=4, column=0, sticky="e")
    global entry_produto_qtd
    entry_produto_qtd = ttk.Entry(aba)
    entry_produto_qtd.grid(row=4, column=1, padx=5, pady=5)

    ttk.Button(aba, text="Cadastrar Produto", command=cadastrar_produto).grid(row=5, columnspan=2, pady=10)

def interface_venda(aba):
    tk.Label(aba, text="Registro de Vendas", font=("Arial", 12, "bold")).grid(row=0, columnspan=2, pady=(0, 10))

    # Código do cliente
    tk.Label(aba, text="Código do Cliente:").grid(row=1, column=0, sticky="e")
    global entry_venda_cliente_cod
    entry_venda_cliente_cod = ttk.Entry(aba)
    entry_venda_cliente_cod.grid(row=1, column=1, padx=5, pady=5)

    # Data da venda
    tk.Label(aba, text="Data da Venda (YYYY-MM-DD):").grid(row=2, column=0, sticky="e")
    global entry_venda_data
    entry_venda_data = ttk.Entry(aba)
    entry_venda_data.grid(row=2, column=1, padx=5, pady=5)

    # Tipo de pagamento
    tk.Label(aba, text="Tipo de Pagamento (à vista, cartão, etc.):").grid(row=3, column=0, sticky="e")
    global entry_venda_pagamento
    entry_venda_pagamento = ttk.Entry(aba)
    entry_venda_pagamento.grid(row=3, column=1, padx=5, pady=5)

    # Produtos da venda
    tk.Label(aba, text="Produtos (código e quantidade):").grid(row=4, column=0, sticky="e")
    global entry_venda_produtos
    entry_venda_produtos = ttk.Entry(aba)
    entry_venda_produtos.grid(row=4, column=1, padx=5, pady=5)

    ttk.Button(aba, text="Adicionar Produto", command=adicionar_produto_venda).grid(row=5, column=0, pady=10)
    ttk.Button(aba, text="Registrar Venda", command=registrar_venda).grid(row=5, column=1, pady=10)

    # Árvore para listar produtos
    global tree
    tree = ttk.Treeview(aba, columns=("Código", "Nome", "Quantidade", "Preço Unitário", "Total"), show="headings")
    tree.grid(row=6, columnspan=2, pady=10)

    tree.heading("Código", text="Código")
    tree.heading("Nome", text="Nome")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Preço Unitário", text="Preço Unitário")
    tree.heading("Total", text="Total")

    # Lista para armazenar os produtos da venda
    global lista_produtos
    lista_produtos = []

def adicionar_produto_venda():
    produto_info = entry_venda_produtos.get().split(",")
    
    if len(produto_info) != 2:
        messagebox.showerror("Erro", "Insira o código e a quantidade corretamente separados por vírgula.")
        return
    
    produto_cod = produto_info[0].strip()
    quantidade = int(produto_info[1].strip())
    
    # Buscar as informações do produto no banco
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT NOME, VALOR_UN FROM PRODUTO WHERE COD = %s;", (produto_cod,))
            produto = cur.fetchone()
            if produto is None:
                messagebox.showerror("Erro", f"Produto com código {produto_cod} não encontrado.")
                return
            
            nome, valor_unitario = produto
            total = valor_unitario * quantidade
            
            lista_produtos.append((produto_cod, quantidade, nome, valor_unitario, total))

            # Adicionar o produto na árvore de visualização
            tree.insert("", "end", values=(produto_cod, nome, quantidade, f"R${valor_unitario:.2f}", f"R${total:.2f}"))
            entry_venda_produtos.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar o produto: {e}")

def registrar_venda():
    cliente_cod = entry_venda_cliente_cod.get()
    data = entry_venda_data.get()
    tipo_pagamento = entry_venda_pagamento.get().lower()
    
    total = 0.0
    for produto_cod, quantidade, nome, valor_unitario, total_produto in lista_produtos:
        total += total_produto
    
    try:
        with conn.cursor() as cur:
            # Registrar a venda
            cur.execute("INSERT INTO VENDA (CLIENTE_COD, DATA, TIPO_PAGAMENTO, TOTAL) VALUES (%s, %s, %s, %s);",
                        (cliente_cod, data, tipo_pagamento, total))
            conn.commit()

            # Atualizar o estoque
            for produto_cod, quantidade, _, _, _ in lista_produtos:
                cur.execute("UPDATE PRODUTO SET QTD_ESTQ = QTD_ESTQ - %s WHERE COD = %s;", (quantidade, produto_cod))
            
            # Atualizar o total de compras do cliente
            cur.execute("UPDATE CLIENTE SET TOTAL_COMPRAS = TOTAL_COMPRAS + %s WHERE COD = %s;", (total, cliente_cod))
            conn.commit()

        messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
        limpar_campos_venda()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao registrar a venda: {e}")

def limpar_campos_venda():
    entry_venda_cliente_cod.delete(0, tk.END)
    entry_venda_data.delete(0, tk.END)
    entry_venda_pagamento.delete(0, tk.END)
    lista_produtos.clear()
    
    for row in tree.get_children():
        tree.delete(row)

# Criar a janela principal
root = tk.Tk()
root.title("Sistema de Vendas")
root.geometry("600x500")
root.protocol("WM_DELETE_WINDOW", lambda: (close_connection(), root.destroy()))

criar_abas()
root.mainloop()
