import psycopg2

conn = psycopg2.connect(host='localhost',port='5432', database='Mercado',user='postgres',
password='91257590')

cur = conn.cursor()

def cadastrar_cliente():
    sql = "INSERT INTO CLIENTE (COD, NOME, TELEFONE, TOTAL_COMPRAS) VALUES (%s, %s, %s, %s);"
    cod = input("Informe o código do cliente: ")
    nome = input("Informe o nome do cliente: ")
    telefone = input("Informe o telefone do cliente: ")
    total_compras = 0  # Inicializando com 0
    cur.execute(sql, (cod, nome, telefone, total_compras))
    conn.commit()
    print("Cliente cadastrado com sucesso!")

def cadastrar_produto():
    sql = "INSERT INTO PRODUTO (COD, NOME, VALOR_UN, QTD_ESTQ) VALUES (%s, %s, %s, %s);"
    cod = input("Informe o código do produto: ")
    nome = input("Informe o nome do produto: ")
    valor_unitario = float(input("Informe o valor unitário do produto: "))
    quantidade_estoque = int(input("Informe a quantidade no estoque: "))
    cur.execute(sql, (cod, nome, valor_unitario, quantidade_estoque))
    conn.commit()
    print("Produto cadastrado com sucesso!")

def registrar_venda():
    cliente_cod = input("Informe o código do cliente: ")
    data = input("Informe a data da venda (YYYY-MM-DD): ")
    tipo_pagamento = input("Informe o tipo de pagamento (DINHEIRO, DEBITO, CREDITO): ").lower()
    total = 0.0
    itens = []

    while True:
        produto_cod = input("Informe o código do produto (ou 0 para finalizar): ")
        if produto_cod == '0':
            break
        quantidade = int(input("Informe a quantidade: "))
        
        # Busca o preço e o estoque do produto
        cur.execute("SELECT VALOR_UN, QTD_ESTQ FROM PRODUTO WHERE COD = %s;", (produto_cod,))
        resultado = cur.fetchone()
        if resultado is None:
            print("Produto não encontrado.")
            continue

        valor_unitario, quantidade_estoque = resultado
        if quantidade > quantidade_estoque:
            print("Quantidade insuficiente em estoque.")
            continue
        
        # Convertendo valor_unitario para float antes da operação
        total += float(valor_unitario * quantidade)
        itens.append((produto_cod, quantidade, valor_unitario))

        # Atualizar o estoque do produto
        cur.execute("UPDATE PRODUTO SET QTD_ESTQ = QTD_ESTQ - %s WHERE COD = %s;", (quantidade, produto_cod))

    # Registrar a venda na tabela VENDA
    cur.execute("INSERT INTO VENDA (CLIENTE_COD, DATA, TIPO_PAGAMENTO, TOTAL) VALUES (%s, %s, %s, %s) RETURNING ID;", 
                (cliente_cod, data, tipo_pagamento, total))
    venda_id = cur.fetchone()[0]

    # Registrar os itens da venda na tabela ITEM_VENDA
    for produto_cod, quantidade, valor_unitario in itens:
        cur.execute("INSERT INTO ITEM_VENDA (VENDA_ID, PRODUTO_COD, QUANTIDADE, VALOR_UNITARIO) VALUES (%s, %s, %s, %s);",
                    (venda_id, produto_cod, quantidade, valor_unitario))

    # Atualizar o total de compras do cliente
    cur.execute("UPDATE CLIENTE SET TOTAL_COMPRAS = TOTAL_COMPRAS + %s WHERE COD = %s;", (total, cliente_cod))
    
    # Confirmar todas as operações
    conn.commit()
    print("Venda registrada com sucesso!")

def atualizar_estoque():
    produto_cod = input("Informe o código do produto: ")
    nova_quantidade = int(input("Informe a nova quantidade no estoque: "))
    cur.execute("UPDATE PRODUTO SET QTD_ESTQ = %s WHERE COD = %s;", (nova_quantidade, produto_cod))
    conn.commit()
    print("Estoque atualizado com sucesso!")


def consultar_cliente():
    cliente_cod = input("Informe o código do cliente: ")
    cur.execute("SELECT NOME, COD, TELEFONE, TOTAL_COMPRAS FROM CLIENTE WHERE COD = %s;", (cliente_cod,))
    cliente = cur.fetchone()
    if cliente:
        nome, cod, telefone, total_compras = cliente
        print(f"Nome: {nome}\nCódigo: {cod}\nTelefone: {telefone}\nTotal de Compras: R${total_compras:.2f}")
    else:
        print("Cliente não encontrado.")

def relatorio_clientes():
    cur.execute("SELECT * FROM CLIENTE;")
    clientes = cur.fetchall()
    print("Clientes cadastrados:")
    for cliente in clientes:
        print(cliente)

def relatorio_total_vendas():
    cur.execute("SELECT SUM(TOTAL) FROM VENDA;")
    total_vendas = cur.fetchone()[0] or 0.0
    print(f"Total de vendas do empreendimento: R${total_vendas:.2f}")

def relatorio_vendas_por_cliente():
    cur.execute("SELECT CLIENTE_COD, SUM(TOTAL) FROM VENDA GROUP BY CLIENTE_COD;")
    vendas_por_cliente = cur.fetchall()
    print("Total de vendas por cliente:")
    for cliente_cod, total in vendas_por_cliente:
        print(f"Cliente {cliente_cod}: R${total:.2f}")

def main():
    while True:
        print("\n--- MENU ---")
        print("1. Cadastro de clientes")
        print("2. Cadastro de produtos")
        print("3. Cadastrar venda dos produtos para o cliente")
        print("4. Atualizar estoque")
        print("5. Informações do Cliente")
        print("6. Relatório - Todos os clientes cadastrados")
        print("7. Relatório - Total de vendas do empreendimento")
        print("8. Relatório - Total de vendas por cliente")
        print("9. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            cadastrar_cliente()
        elif opcao == '2':
            cadastrar_produto()
        elif opcao == '3':
            registrar_venda()
        elif opcao == '4':
            atualizar_estoque()
        elif opcao == '5':
            consultar_cliente()
        elif opcao == '6':
            relatorio_clientes()
        elif opcao == '7':
            relatorio_total_vendas()
        elif opcao == '8':
            relatorio_vendas_por_cliente()
        elif opcao == '9':
            break
        else:
            print("Opção inválida. Tente novamente.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()