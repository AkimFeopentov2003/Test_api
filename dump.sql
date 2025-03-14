--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12 (Debian 15.12-1.pgdg120+1)
-- Dumped by pg_dump version 17.2 (Ubuntu 17.2-1.pgdg24.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: rolls; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rolls (
    id integer NOT NULL,
    length double precision NOT NULL,
    weight double precision NOT NULL,
    added_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    removed_at timestamp without time zone
);


ALTER TABLE public.rolls OWNER TO postgres;

--
-- Name: rolls_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rolls_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rolls_id_seq OWNER TO postgres;

--
-- Name: rolls_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rolls_id_seq OWNED BY public.rolls.id;


--
-- Name: rolls id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rolls ALTER COLUMN id SET DEFAULT nextval('public.rolls_id_seq'::regclass);


--
-- Data for Name: rolls; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rolls (id, length, weight, added_at, removed_at) FROM stdin;
20	1	2.4	2025-03-12 15:13:11.22285	\N
21	1	2.4	2025-03-12 15:13:11.381608	\N
22	1	2.4	2025-03-12 15:13:11.544048	\N
17	1	3.5	2025-03-12 15:11:36.739866	2025-03-12 15:22:30.967275
18	1	2.4	2025-03-12 15:12:59.51418	2025-03-12 15:28:28.831534
19	1	2.4	2025-03-12 15:13:04.153373	2025-03-13 08:53:29.212268
23	5	9.8	2025-03-13 09:14:45.06259	\N
24	6	2.8	2025-03-13 09:14:52.360956	\N
25	7	1.8	2025-03-13 09:14:59.526786	\N
26	9.7	23.9	2025-03-13 09:15:10.599933	\N
\.


--
-- Name: rolls_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rolls_id_seq', 26, true);


--
-- Name: rolls rolls_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rolls
    ADD CONSTRAINT rolls_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

