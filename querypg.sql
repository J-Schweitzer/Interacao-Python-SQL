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

insert into cliente values (
	3,
	'Alex',
	'67 992457481'
);

insert into cliente values (
	4,
	'Mariana',
	'67 988245678'
);

insert into cliente values (
	5,
	'Carlos',
	'67 988745678'
);

insert into cliente values (
	6,
	'Roberta',
	'67 991234567'
);

insert into cliente values (
	7,
	'Fernanda',
	'67 997654321'
);

insert into cliente values (
	8,
	'Paulo',
	'67 996745231'
);

insert into cliente values (
	9,
	'Lucia',
	'67 992345678'
);

insert into cliente values (
	10,
	'Felipe',
	'67 991876543'
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
insert into produto values (
	3,
	'Macarrao Espaguete 500g',
	5.99,
	120
);

insert into produto values (
	4,
	'Óleo de Soja 900ml',
	6.49,
	150
);

insert into produto values (
	5,
	'Leite UHT 1L',
	4.30,
	200
);

insert into produto values (
	6,
	'Papel Higiênico 12 Unidades',
	18.90,
	50
);

insert into produto values (
	7,
	'Detergente Líquido 500ml',
	2.99,
	80
);

insert into produto values (
	8,
	'Sabão em Pó 1kg',
	7.45,
	60
);

insert into produto values (
	9,
	'Biscoito Maizena 400g',
	3.80,
	150
);

insert into produto values (
	10,
	'Feijão Preto 1kg',
	7.20,
	120
);

insert into produto values (
	11,
	'Macarrão Instantâneo 85g',
	1.80,
	250
);

insert into produto values (
	12,
	'Abacaxi',
	5.00,
	30
);
