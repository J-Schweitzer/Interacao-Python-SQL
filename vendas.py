import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2

# Conexão com o banco de dados
conn = psycopg2.connect(host='localhost', port='5432', database='Mercado', user='postgres', password='91257590')

def close_connection():
    conn.close()

# Função para cadastrar cliente
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

# Função para cadastrar produto
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

# Função para registrar venda
def registrar_venda():
    cliente_cod = entry_venda_cliente_cod.get()
    data = entry_venda_data.get()
    tipo_pagamento = entry_venda_pagamento.get().lower()
    
    total = 0.0
    itens = []
    
    for i in range(len(lista_produtos)):
        quantidade = lista_produtos[i][1]
        produto_cod = lista_produtos[i][0]
        
        # Busca o preço e o estoque do produto
        with conn.cursor() as cur:
            cur.execute("SELECT VALOR_UN, QTD_ESTQ FROM PRODUTO WHERE COD = %s;", (produto_cod,))
            resultado = cur.fetchone()
            if resultado is None:
                messagebox.showerror("Erro", f"Produto {produto_cod} não encontrado.")
                return

            valor_unitario, quantidade_estoque = resultado
            if quantidade > quantidade_estoque:
                messagebox.showerror("Erro", f"Quantidade insuficiente em estoque para o produto {produto_cod}.")
                return

            total += float(valor_unitario * quantidade)
            itens.append((produto_cod, quantidade, valor_unitario))

            # Atualizar o estoque do produto
            cur.execute("UPDATE PRODUTO SET QTD_ESTQ = QTD_ESTQ - %s WHERE COD = %s;", (quantidade, produto_cod))

    # Registrar a venda na tabela VENDA
    with conn.cursor() as cur:
        cur.execute("INSERT INTO VENDA (CLIENTE_COD, DATA, TIPO_PAGAMENTO, TOTAL) VALUES (%s, %s, %s, %s);",
                    (cliente_cod, data, tipo_pagamento, total))
        conn.commit()

    # Atualizar o total de compras do cliente
    with conn.cursor() as cur:
        cur.execute("UPDATE CLIENTE SET TOTAL_COMPRAS = TOTAL_COMPRAS + %s WHERE COD = %s;", (total, cliente_cod))
        conn.commit()

    messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
    limpar_campos_venda()

def limpar_campos_venda():
    entry_venda_cliente_cod.delete(0, tk.END)
    entry_venda_data.delete(0, tk.END)
    entry_venda_pagamento.delete(0, tk.END)
    lista_produtos.clear()
    for row in tree.get_children():
        tree.delete(row)

# Função para atualizar estoque
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

# Função para consultar cliente
def consultar_cliente():
    cliente_cod = entry_consulta_cliente_cod.get()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT NOME, COD, TELEFONE, TOTAL_COMPRAS FROM CLIENTE WHERE COD = %s;", (cliente_cod,))
            cliente = cur.fetchone()
            if cliente:
                nome, cod, telefone, total_compras = cliente
                messagebox.showinfo("Cliente Encontrado", f"Nome: {nome}\nCódigo: {cod}\nTelefone: {telefone}\nTotal de Compras: R${total_compras:.2f}")
            else:
                messagebox.showinfo("Erro", "Cliente não encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao consultar o cliente: {e}")

# Função para relatar clientes
def relatorio_clientes():
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM CLIENTE;")
            clientes = cur.fetchall()
            relatorio = "Clientes cadastrados:\n" + "\n".join([str(cliente) for cliente in clientes])
            messagebox.showinfo("Relatório de Clientes", relatorio)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o relatório: {e}")

# Função para relatar total de vendas
def relatorio_total_vendas():
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT SUM(TOTAL) FROM VENDA;")
            total_vendas = cur.fetchone()[0] or 0.0
            messagebox.showinfo("Total de Vendas", f"Total de vendas do empreendimento: R${total_vendas:.2f}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o relatório: {e}")

# Função para relatar vendas por cliente
def relatorio_vendas_por_cliente():
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT CLIENTE_COD, SUM(TOTAL) FROM VENDA GROUP BY CLIENTE_COD;")
            vendas_por_cliente = cur.fetchall()
            relatorio = "Total de vendas por cliente:\n" + "\n".join([f"Cliente {cliente_cod}: R${total:.2f}" for cliente_cod, total in vendas_por_cliente])
            messagebox.showinfo("Relatório de Vendas por Cliente", relatorio)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o relatório: {e}")

# Criar a janela principal
root = tk.Tk()
root.title("Sistema de Vendas")

# Frame para cadastro de clientes
frame_cliente = tk.Frame(root)
frame_cliente.pack(pady=10)

tk.Label(frame_cliente, text="Cadastro de Clientes").grid(row=0, columnspan=2)

tk.Label(frame_cliente, text="Código:").grid(row=1, column=0)
entry_cliente_cod = tk.Entry(frame_cliente)
entry_cliente_cod.grid(row=1, column=1)

tk.Label(frame_cliente, text="Nome:").grid(row=2, column=0)
entry_cliente_nome = tk.Entry(frame_cliente)
entry_cliente_nome.grid(row=2, column=1)

tk.Label(frame_cliente, text="Telefone:").grid(row=3, column=0)
entry_cliente_telefone = tk.Entry(frame_cliente)
entry_cliente_telefone.grid(row=3, column=1)

tk.Button(frame_cliente, text="Cadastrar Cliente", command=cadastrar_cliente).grid(row=4, columnspan=2)

# Frame para cadastro de produtos
frame_produto = tk.Frame(root)
frame_produto.pack(pady=10)

tk.Label(frame_produto, text="Cadastro de Produtos").grid(row=0, columnspan=2)

tk.Label(frame_produto, text="Código:").grid(row=1, column=0)
entry_produto_cod = tk.Entry(frame_produto)
entry_produto_cod.grid(row=1, column=1)

tk.Label(frame_produto, text="Nome:").grid(row=2, column=0)
entry_produto_nome = tk.Entry(frame_produto)
entry_produto_nome.grid(row=2, column=1)

tk.Label(frame_produto, text="Valor Unitário:").grid(row=3, column=0)
entry_produto_valor = tk.Entry(frame_produto)
entry_produto_valor.grid(row=3, column=1)

tk.Label(frame_produto, text="Quantidade em Estoque:").grid(row=4, column=0)
entry_produto_qtd = tk.Entry(frame_produto)
entry_produto_qtd.grid(row=4, column=1)

tk.Button(frame_produto, text="Cadastrar Produto", command=cadastrar_produto).grid(row=5, columnspan=2)

# Frame para registrar vendas
frame_venda = tk.Frame(root)
frame_venda.pack(pady=10)

tk.Label(frame_venda, text="Registrar Venda").grid(row=0, columnspan=2)

tk.Label(frame_venda, text="Código do Cliente:").grid(row=1, column=0)
entry_venda_cliente_cod = tk.Entry(frame_venda)
entry_venda_cliente_cod.grid(row=1, column=1)

tk.Label(frame_venda, text="Data (YYYY-MM-DD):").grid(row=2, column=0)
entry_venda_data = tk.Entry(frame_venda)
entry_venda_data.grid(row=2, column=1)

tk.Label(frame_venda, text="Tipo de Pagamento:").grid(row=3, column=0)
entry_venda_pagamento = tk.Entry(frame_venda)
entry_venda_pagamento.grid(row=3, column=1)

tk.Button(frame_venda, text="Registrar Venda", command=registrar_venda).grid(row=4, columnspan=2)

# Frame para atualizar estoque
frame_estoque = tk.Frame(root)
frame_estoque.pack(pady=10)

tk.Label(frame_estoque, text="Atualizar Estoque").grid(row=0, columnspan=2)

tk.Label(frame_estoque, text="Código do Produto:").grid(row=1, column=0)
entry_estoque_cod = tk.Entry(frame_estoque)
entry_estoque_cod.grid(row=1, column=1)

tk.Label(frame_estoque, text="Nova Quantidade:").grid(row=2, column=0)
entry_estoque_qtd = tk.Entry(frame_estoque)
entry_estoque_qtd.grid(row=2, column=1)

tk.Button(frame_estoque, text="Atualizar Estoque", command=atualizar_estoque).grid(row=3, columnspan=2)

# Frame para consulta de clientes
frame_consulta = tk.Frame(root)
frame_consulta.pack(pady=10)

tk.Label(frame_consulta, text="Consultar Cliente").grid(row=0, columnspan=2)

tk.Label(frame_consulta, text="Código do Cliente:").grid(row=1, column=0)
entry_consulta_cliente_cod = tk.Entry(frame_consulta)
entry_consulta_cliente_cod.grid(row=1, column=1)

tk.Button(frame_consulta, text="Consultar", command=consultar_cliente).grid(row=2, columnspan=2)

# Frame para relatórios
frame_relatorios = tk.Frame(root)
frame_relatorios.pack(pady=10)

tk.Label(frame_relatorios, text="Relatórios").grid(row=0, columnspan=2)

tk.Button(frame_relatorios, text="Relatório de Clientes", command=relatorio_clientes).grid(row=1, column=0)
tk.Button(frame_relatorios, text="Total de Vendas", command=relatorio_total_vendas).grid(row=1, column=1)
tk.Button(frame_relatorios, text="Vendas por Cliente", command=relatorio_vendas_por_cliente).grid(row=2, columnspan=2)

# Fechar a conexão ao final
root.protocol("WM_DELETE_WINDOW", lambda: (close_connection(), root.destroy()))

# Rodar a aplicação
root.mainloop()
