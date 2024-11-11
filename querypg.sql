CREATE TABLE cliente (
    cod INT PRIMARY KEY,
    nome VARCHAR(50),
    telefone VARCHAR(20),
    total_compras DECIMAL(10,2) DEFAULT 0
);

CREATE TABLE produto (
    cod INT PRIMARY KEY,
    nome VARCHAR(50),
    valor_un DECIMAL(10,2),
    qtd_estq INT
);

CREATE TABLE venda (
    id SERIAL PRIMARY KEY,
    cliente_cod INT,
    data DATE,
    tipo_pagamento VARCHAR(10) CHECK (tipo_pagamento IN ('dinheiro', 'debito', 'credito')),
    total DECIMAL(10, 2),
    FOREIGN KEY (cliente_cod) REFERENCES cliente(cod)
);

CREATE TABLE item_venda (
    venda_id INT,
    produto_cod INT,
    quantidade INT,
    valor_unitario DECIMAL(10, 2),
    FOREIGN KEY (venda_id) REFERENCES venda(id),
    FOREIGN KEY (produto_cod) REFERENCES produto(cod)
);

insert into cliente values (
	1,
	'Luan',
	'67 991561505'
);

insert into cliente values (
	2,
	'Jorge',
	'67 97458475'
);

insert into produto values (
	1,
	'Arroz 5Kg',
	45.00,
	87
);

insert into produto values (
	2,
	'Feijao 1kg',
	21.00,
	41
);
