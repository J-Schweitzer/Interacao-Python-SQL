import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2

# Conexão com o banco de dados
conn = psycopg2.connect(host='localhost', port='5432', database='Mercado', user='postgres', password='---')

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
            
            #Limpando dados cliente
            entry_cliente_cod.delete(0, tk.END)
            entry_cliente_nome.delete(0, tk.END)
            entry_cliente_telefone.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar o cliente: {e}")

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
    combobox_pagamento.delete(0, tk.END)
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
    interface_estoque(aba_estoque)
    interface_relatorios(aba_relatorios)

    
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
    def atualizar_parcelas(event):
        """Habilita ou desabilita a seleção de parcelas dependendo do tipo de pagamento."""
        if combobox_pagamento.get() == "Credito":
            combobox_parcelas.configure(state="readonly")
            combobox_parcelas.set("1")  # Define o padrão para 1 parcela
            atualizar_valor_parcela()  # Atualiza o valor da parcela
        else:
            combobox_parcelas.configure(state="disabled")
            combobox_parcelas.set("")
            label_valor_parcela.configure(text="Valor da Parcela: -")

    def atualizar_valor_parcela(event=None):
        """Atualiza o valor da parcela com base no total da venda e nas parcelas selecionadas."""
        if combobox_pagamento.get() == "Credito":
            try:
                total_venda = calcular_total_venda()
                num_parcelas = int(combobox_parcelas.get())
                valor_parcela = total_venda / num_parcelas
                label_valor_parcela.configure(text=f"Valor da Parcela: R$ {valor_parcela:.2f}")
            except (ValueError, ZeroDivisionError):
                label_valor_parcela.configure(text="Valor da Parcela: -")
        else:
            label_valor_parcela.configure(text="Valor da Parcela: -")

    def calcular_total_venda():
        """Calcula o total da venda com base nos produtos adicionados."""
        return sum(item[4] for item in lista_produtos)  # item[4] é o 'total' de cada produto na tupla


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
    tk.Label(aba, text="Tipo de Pagamento:").grid(row=3, column=0, sticky="e")
    global combobox_pagamento
    combobox_pagamento = ttk.Combobox(aba, values=["Debito", "Credito"], state="readonly")
    combobox_pagamento.grid(row=3, column=1, padx=5, pady=5)
    combobox_pagamento.set("Debito")  # Define um valor padrão
    combobox_pagamento.bind("<<ComboboxSelected>>", atualizar_parcelas)

    # Quantidade de parcelas (inicialmente desabilitado)
    tk.Label(aba, text="Quantidade de Parcelas:").grid(row=4, column=0, sticky="e")
    global combobox_parcelas
    combobox_parcelas = ttk.Combobox(aba, values=[str(i) for i in range(1, 13)], state="disabled")
    combobox_parcelas.grid(row=4, column=1, padx=5, pady=5)
    combobox_parcelas.bind("<<ComboboxSelected>>", atualizar_valor_parcela)

    # Label para mostrar o valor da parcela
    global label_valor_parcela
    label_valor_parcela = tk.Label(aba, text="Valor da Parcela: -", font=("Arial", 10))
    label_valor_parcela.grid(row=5, columnspan=2, pady=5)

    # Produtos da venda
    tk.Label(aba, text="Produtos (código e quantidade):").grid(row=6, column=0, sticky="e")
    global entry_venda_produtos
    entry_venda_produtos = ttk.Entry(aba)
    entry_venda_produtos.grid(row=6, column=1, padx=5, pady=5)

    ttk.Button(aba, text="Adicionar Produto", command=adicionar_produto_venda).grid(row=7, column=0, pady=10)
    ttk.Button(aba, text="Registrar Venda", command=registrar_venda).grid(row=7, column=1, pady=10)

    # Árvore para listar produtos
    global tree
    tree = ttk.Treeview(aba, columns=("Código", "Nome", "Quantidade", "Preço Unitário", "Total"), show="headings")
    tree.grid(row=8, columnspan=2, pady=10)

    tree.heading("Código", text="Código")
    tree.heading("Nome", text="Nome")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Preço Unitário", text="Preço Unitário")
    tree.heading("Total", text="Total")

    # Lista para armazenar os produtos da venda
    global lista_produtos
    lista_produtos = []

def interface_estoque(aba):
    tk.Label(aba, text="Atualização de Estoque", font=("Arial", 12, "bold")).grid(row=0, columnspan=2, pady=(0, 10))

    tk.Label(aba, text="Código do Produto:").grid(row=1, column=0, sticky="e")
    global entry_estoque_cod
    entry_estoque_cod = ttk.Entry(aba)
    entry_estoque_cod.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(aba, text="Nova Quantidade:").grid(row=2, column=0, sticky="e")
    global entry_estoque_qtd
    entry_estoque_qtd = ttk.Entry(aba)
    entry_estoque_qtd.grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(aba, text="Atualizar Estoque", command=atualizar_estoque).grid(row=3, columnspan=2, pady=10)

def interface_relatorios(aba):
    tk.Label(aba, text="Relatórios", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

    # Botões para carregar diferentes relatórios
    ttk.Button(aba, text="Relatório de Clientes", command=exibir_relatorio_clientes).grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(aba, text="Relatório de Produtos", command=exibir_relatorio_produtos).grid(row=1, column=1, padx=5, pady=5)

    # Treeview para exibir o relatório
    global tree_relatorio
    tree_relatorio = ttk.Treeview(aba, columns=("col1", "col2", "col3", "col4"), show="headings")
    tree_relatorio.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

    # Configuração das colunas (exemplo genérico)
    tree_relatorio.heading("col1", text="Coluna 1")
    tree_relatorio.heading("col2", text="Coluna 2")
    tree_relatorio.heading("col3", text="Coluna 3")
    tree_relatorio.heading("col4", text="Coluna 4")

def exibir_relatorio_clientes():
    # Configura a Treeview para exibir os dados dos clientes
    for col in tree_relatorio["columns"]:
        tree_relatorio.heading(col, text=col)
    tree_relatorio.heading("col1", text="Código")
    tree_relatorio.heading("col2", text="Nome")
    tree_relatorio.heading("col3", text="Telefone")
    tree_relatorio.heading("col4", text="Total Compras")

    # Limpar dados antigos
    for row in tree_relatorio.get_children():
        tree_relatorio.delete(row)
    
    # Consultar dados do banco
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COD, NOME, TELEFONE, TOTAL_COMPRAS FROM CLIENTE ORDER BY COD;")
            clientes = cur.fetchall()
            for cliente in clientes:
                tree_relatorio.insert("", "end", values=cliente)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao carregar o relatório de clientes: {e}")

def exibir_relatorio_produtos():
    # Configura a Treeview para exibir os dados dos produtos
    for col in tree_relatorio["columns"]:
        tree_relatorio.heading(col, text=col)
    tree_relatorio.heading("col1", text="Código")
    tree_relatorio.heading("col2", text="Nome")
    tree_relatorio.heading("col3", text="Valor Unitário")
    tree_relatorio.heading("col4", text="Quantidade em Estoque")

    # Limpar dados antigos
    for row in tree_relatorio.get_children():
        tree_relatorio.delete(row)
    
    # Consultar dados do banco
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COD, NOME, VALOR_UN, QTD_ESTQ FROM PRODUTO ORDER BY COD;")
            produtos = cur.fetchall()
            for produto in produtos:
                tree_relatorio.insert("", "end", values=produto)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao carregar o relatório de produtos: {e}")

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
    tipo_pagamento = combobox_pagamento.get().lower()

    total = 0.0
    produtos_para_atualizar_estoque = []

    # Verificar se o estoque é suficiente e calcular o total da venda
    for produto_cod, quantidade, nome, valor_unitario, total_produto in lista_produtos:
        total += float(total_produto)
        
        try:
            with conn.cursor() as cur:
                # Verificar se há estoque suficiente para o produto
                cur.execute("SELECT QTD_ESTQ FROM PRODUTO WHERE COD = %s;", (produto_cod,))
                estoque_atual = cur.fetchone()
                if estoque_atual is None:
                    messagebox.showerror("Erro", f"Produto {produto_cod} não encontrado.")
                    return

                estoque_atual = estoque_atual[0]
                if estoque_atual < quantidade:
                    messagebox.showerror("Erro", f"Estoque insuficiente para o produto {produto_cod}.")
                    return

                # Se o estoque for suficiente, preparar a atualização do estoque
                produtos_para_atualizar_estoque.append((produto_cod, quantidade))

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao verificar o estoque: {e}")
            return

    # Registrar a venda
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO VENDA (CLIENTE_COD, DATA, TIPO_PAGAMENTO, TOTAL) VALUES (%s, %s, %s, %s);",
                        (cliente_cod, data, tipo_pagamento, total))
            conn.commit()

            # Atualizar o estoque e o total de compras do cliente
            for produto_cod, quantidade in produtos_para_atualizar_estoque:
                cur.execute("UPDATE PRODUTO SET QTD_ESTQ = QTD_ESTQ - %s WHERE COD = %s;", (quantidade, produto_cod))
                
            cur.execute("UPDATE CLIENTE SET TOTAL_COMPRAS = TOTAL_COMPRAS + %s WHERE COD = %s;", (total, cliente_cod))
            conn.commit()

        messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
        limpar_campos_venda()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao registrar a venda: {e}")

def limpar_campos_venda():
    entry_venda_cliente_cod.delete(0, tk.END)
    entry_venda_data.delete(0, tk.END)
    combobox_pagamento.delete(0, tk.END)
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
