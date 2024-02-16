--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: assets_family; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.assets_family (
    id integer NOT NULL,
    description character varying(100),
    aloca_bens character(3),
    movimenta_bens character(3)
);


ALTER TABLE public.assets_family OWNER TO postgres;

--
-- Name: asset_family_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.asset_family_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.asset_family_id_seq OWNER TO postgres;

--
-- Name: asset_family_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.asset_family_id_seq OWNED BY public.assets_family.id;


--
-- Name: assets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.assets (
    id integer NOT NULL,
    model_type character varying(20),
    description_model_type character varying(100),
    description character varying(100),
    manufacturer character varying(100),
    unit_model character varying(100),
    unit_series character varying(100),
    add_description character varying(100),
    supplier character varying(100),
    purchase_value numeric(10,2),
    purchase_date date,
    motor_manufacturer character varying(100),
    motor_model character varying(100),
    tank character varying(10),
    alt_larg_comp character varying(20),
    chain character varying(100),
    avg character varying(100),
    weight character varying(10),
    current_pos_counter character varying(5),
    accumulated_counter character varying(5),
    limit_counter character varying(5),
    avg_variation_counter character varying(5),
    last_date_counter date
);


ALTER TABLE public.assets OWNER TO postgres;

--
-- Name: assets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.assets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.assets_id_seq OWNER TO postgres;

--
-- Name: assets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.assets_id_seq OWNED BY public.assets.id;


--
-- Name: clients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clients (
    id integer NOT NULL,
    company character varying(100) NOT NULL,
    corporate_name character varying(100) NOT NULL,
    number_store smallint NOT NULL,
    person_type character varying(15) NOT NULL,
    company_address character varying(100) NOT NULL,
    client_type character varying(100) NOT NULL,
    cpf_cnpj character varying(20) NOT NULL,
    state_registration character varying(20) NOT NULL,
    registration_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    contact_name character varying(100) NOT NULL,
    phone character varying(15) NOT NULL,
    email character varying(100) NOT NULL,
    billing_address character varying(100) NOT NULL
);


ALTER TABLE public.clients OWNER TO postgres;

--
-- Name: clients_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clients_id_seq OWNER TO postgres;

--
-- Name: clients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clients_id_seq OWNED BY public.clients.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer NOT NULL,
    description character varying(100),
    type character varying(100),
    storage character varying(100),
    price numeric(10,2),
    weigth numeric(10,4),
    add_description character varying(100),
    product_code character varying(15)
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: proposal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.proposal (
    id integer NOT NULL,
    client_id integer,
    status character varying(100),
    delivery_date date,
    withdrawal_date date,
    start_date date,
    end_date date,
    period_days character varying(4),
    delivery_address character varying(100),
    validity character varying(10),
    value character varying(100)
);


ALTER TABLE public.proposal OWNER TO postgres;

--
-- Name: proposal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.proposal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.proposal_id_seq OWNER TO postgres;

--
-- Name: proposal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.proposal_id_seq OWNED BY public.proposal.id;


--
-- Name: proposal_product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.proposal_product (
    proposal_id integer NOT NULL,
    product_id integer NOT NULL
);


ALTER TABLE public.proposal_product OWNER TO postgres;

--
-- Name: proposal_product_proposal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.proposal_product_proposal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.proposal_product_proposal_id_seq OWNER TO postgres;

--
-- Name: proposal_product_proposal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.proposal_product_proposal_id_seq OWNED BY public.proposal_product.proposal_id;


--
-- Name: proposal_refund; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.proposal_refund (
    proposal_id integer NOT NULL,
    refund_id integer NOT NULL
);


ALTER TABLE public.proposal_refund OWNER TO postgres;

--
-- Name: proposal_refund_proposal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.proposal_refund_proposal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.proposal_refund_proposal_id_seq OWNER TO postgres;

--
-- Name: proposal_refund_proposal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.proposal_refund_proposal_id_seq OWNED BY public.proposal_refund.proposal_id;


--
-- Name: refund; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.refund (
    cod smallint NOT NULL,
    descript character varying(100)
);


ALTER TABLE public.refund OWNER TO postgres;

--
-- Name: assets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assets ALTER COLUMN id SET DEFAULT nextval('public.assets_id_seq'::regclass);


--
-- Name: assets_family id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assets_family ALTER COLUMN id SET DEFAULT nextval('public.asset_family_id_seq'::regclass);


--
-- Name: clients id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients ALTER COLUMN id SET DEFAULT nextval('public.clients_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: proposal id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal ALTER COLUMN id SET DEFAULT nextval('public.proposal_id_seq'::regclass);


--
-- Name: proposal_product proposal_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal_product ALTER COLUMN proposal_id SET DEFAULT nextval('public.proposal_product_proposal_id_seq'::regclass);


--
-- Name: proposal_refund proposal_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal_refund ALTER COLUMN proposal_id SET DEFAULT nextval('public.proposal_refund_proposal_id_seq'::regclass);


--
-- Data for Name: assets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assets (id, model_type, description_model_type, description, manufacturer, unit_model, unit_series, add_description, supplier, purchase_value, purchase_date, motor_manufacturer, motor_model, tank, alt_larg_comp, chain, avg, weight, current_pos_counter, accumulated_counter, limit_counter, avg_variation_counter, last_date_counter) FROM stdin;
\.


--
-- Data for Name: assets_family; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assets_family (id, description, aloca_bens, movimenta_bens) FROM stdin;
\.


--
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clients (id, company, corporate_name, number_store, person_type, company_address, client_type, cpf_cnpj, state_registration, registration_date, contact_name, phone, email, billing_address) FROM stdin;
2	geraforca	geraforca	1	juridica	est capuava	cons final	000012212121121	054545121655	2023-12-14 16:29:31.339912	henrique	40404040	henrique@gf	estr capuava
3	Faculdade Estácio	estacio	1	juridica	est capuava	cons final	000012212121121	12102051510545	2023-12-14 16:42:46.12628	henrique	11970637362	henrique@gf	
4	teste1	teste1 ltda	1	legal	est capuava	cons_final	659465584846	4845655988	2023-12-14 17:49:00.84534	henrique	8484865989	teste@teste	estr capuava
5	teste2	teste2 ltda	1	Juridica	est capuava	Cons. Final	5555544464	054545121655	2023-12-14 17:51:25.105121	henrique	11970637362	teste2@teste	estr capuava
7	teste4	teste4 ltda	1	Juridica	est capuava	Cons. Final	45459898895621	4845655988	2023-12-15 10:30:09.698857	henrique	8484865989	teste4@teste	
9	Henrique	Henrique LTDA	1	Fisica	rua maua	Cons. Final	46133289856	1111111111	2023-12-18 16:26:38.759643	henrique	970637362	santos_silvaaa@hotmail.com	rua maua
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (id, description, type, storage, price, weigth, add_description, product_code) FROM stdin;
1	GRUPO GERADOR SILENCIADO DE 350 KVA	PA - Produto Acabado	ESTOQUE DE GERADORES	130800.00	4000.0000	TRIFASICO. ESTACIONARIO. DIESEL	0810350000
2	GRUPO GERADOR SILENCIADO DE 450 KVA	PA - Produto Acabado	ESTOQUE DE GERADORES	130000.00	5000.0000	TRIFASICO. ESTACIONARIO. DIESEL	0810450000
\.


--
-- Data for Name: proposal; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.proposal (id, client_id, status, delivery_date, withdrawal_date, start_date, end_date, period_days, delivery_address, validity, value) FROM stdin;
\.


--
-- Data for Name: proposal_product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.proposal_product (proposal_id, product_id) FROM stdin;
\.


--
-- Data for Name: proposal_refund; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.proposal_refund (proposal_id, refund_id) FROM stdin;
\.


--
-- Data for Name: refund; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.refund (cod, descript) FROM stdin;
1	RESSARCIMENTO DE DESPESAS DE LOCACAO - TRANSPORTE
2	RESSARCIMENTO DE DESPESAS DE LOCACAO - OPERADOR
3	RESSARCIMENTO DE DESPESAS DE LOCACAO - MANUTENCAO
4	RESSARCIMENTO DE DESPESAS DE LOCACAO - OLEO DIESEL
5	RESSARCIMENTO DE DESPESAS DE LOCACAO - OUTROS
\.


--
-- Name: asset_family_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.asset_family_id_seq', 1, false);


--
-- Name: assets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assets_id_seq', 1, false);


--
-- Name: clients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clients_id_seq', 9, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 2, true);


--
-- Name: proposal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.proposal_id_seq', 1, false);


--
-- Name: proposal_product_proposal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.proposal_product_proposal_id_seq', 1, false);


--
-- Name: proposal_refund_proposal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.proposal_refund_proposal_id_seq', 1, false);


--
-- Name: assets_family asset_family_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assets_family
    ADD CONSTRAINT asset_family_pkey PRIMARY KEY (id);


--
-- Name: assets assets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assets
    ADD CONSTRAINT assets_pkey PRIMARY KEY (id);


--
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (id);


--
-- Name: products pk_id_products; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT pk_id_products PRIMARY KEY (id);


--
-- Name: proposal proposal_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal
    ADD CONSTRAINT proposal_pkey PRIMARY KEY (id);


--
-- Name: proposal_product proposal_product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal_product
    ADD CONSTRAINT proposal_product_pkey PRIMARY KEY (proposal_id, product_id);


--
-- Name: proposal_refund proposal_refund_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal_refund
    ADD CONSTRAINT proposal_refund_pkey PRIMARY KEY (proposal_id, refund_id);


--
-- Name: refund refund_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refund
    ADD CONSTRAINT refund_pkey PRIMARY KEY (cod);


--
-- Name: proposal proposal_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal
    ADD CONSTRAINT proposal_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id);


--
-- Name: proposal_product proposal_product_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal_product
    ADD CONSTRAINT proposal_product_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: proposal_product proposal_product_proposal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal_product
    ADD CONSTRAINT proposal_product_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.proposal(id);


--
-- Name: proposal_refund proposal_refund_proposal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal_refund
    ADD CONSTRAINT proposal_refund_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.proposal(id);


--
-- Name: proposal_refund proposal_refund_refund_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal_refund
    ADD CONSTRAINT proposal_refund_refund_id_fkey FOREIGN KEY (refund_id) REFERENCES public.refund(cod);


--
-- PostgreSQL database dump complete
--

