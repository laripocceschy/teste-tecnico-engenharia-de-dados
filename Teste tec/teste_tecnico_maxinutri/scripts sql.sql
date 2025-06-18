-- Table: public.dim_cliente

-- DROP TABLE IF EXISTS public.dim_cliente;

CREATE TABLE IF NOT EXISTS public.dim_cliente
(
    customer_id text COLLATE pg_catalog."default",
    cidade text COLLATE pg_catalog."default",
    estado text COLLATE pg_catalog."default",
    cep_prefixo bigint
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.dim_cliente
    OWNER to admin;


-- Table: public.dim_pedido

-- DROP TABLE IF EXISTS public.dim_pedido;

CREATE TABLE IF NOT EXISTS public.dim_pedido
(
    order_id text COLLATE pg_catalog."default",
    status_pedido text COLLATE pg_catalog."default",
    data_compra timestamp without time zone,
    data_aprovacao timestamp without time zone,
    data_envio_transportadora timestamp without time zone,
    data_entrega_cliente timestamp without time zone,
    data_entrega_estimada timestamp without time zone
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.dim_pedido
    OWNER to admin;

-- Table: public.dim_produto

-- DROP TABLE IF EXISTS public.dim_produto;

CREATE TABLE IF NOT EXISTS public.dim_produto
(
    product_id text COLLATE pg_catalog."default",
    categoria text COLLATE pg_catalog."default",
    fotos_qtd double precision,
    peso_g double precision,
    comprimento_cm double precision,
    altura_cm double precision,
    largura_cm double precision
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.dim_produto
    OWNER to admin;

-- Table: public.fato_avaliacoes

-- DROP TABLE IF EXISTS public.fato_avaliacoes;

CREATE TABLE IF NOT EXISTS public.fato_avaliacoes
(
    order_id text COLLATE pg_catalog."default",
    nota_avaliacao double precision,
    titulo_avaliacao text COLLATE pg_catalog."default",
    texto_avaliacao text COLLATE pg_catalog."default",
    data_avaliacao timestamp without time zone,
    data_resposta timestamp without time zone
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.fato_avaliacoes
    OWNER to admin;

-- Table: public.fato_vendas

-- DROP TABLE IF EXISTS public.fato_vendas;

CREATE TABLE IF NOT EXISTS public.fato_vendas
(
    order_id text COLLATE pg_catalog."default",
    customer_id text COLLATE pg_catalog."default",
    product_id text COLLATE pg_catalog."default",
    price double precision,
    frete double precision,
    data_entrega timestamp without time zone
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.fato_vendas
    OWNER to admin;