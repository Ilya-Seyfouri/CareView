--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 16.9

-- Started on 2025-07-19 11:55:46

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

DROP DATABASE IF EXISTS careview;
--
-- TOC entry 4932 (class 1262 OID 16498)
-- Name: careview; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE careview WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United Kingdom.1252';


ALTER DATABASE careview OWNER TO admin;

\connect careview

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

--
-- TOC entry 5 (class 2615 OID 16671)
-- Name: public; Type: SCHEMA; Schema: -; Owner: admin
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO admin;

--
-- TOC entry 4933 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON SCHEMA public IS '';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 219 (class 1259 OID 16697)
-- Name: assignments; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.assignments (
    user_email character varying NOT NULL,
    client_id character varying NOT NULL
);


ALTER TABLE public.assignments OWNER TO admin;

--
-- TOC entry 218 (class 1259 OID 16689)
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.audit_logs (
    id integer NOT NULL,
    user_email character varying NOT NULL,
    action character varying NOT NULL,
    entity_type character varying NOT NULL,
    entity_id character varying NOT NULL,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.audit_logs OWNER TO admin;

--
-- TOC entry 217 (class 1259 OID 16688)
-- Name: audit_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.audit_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.audit_logs_id_seq OWNER TO admin;

--
-- TOC entry 4935 (class 0 OID 0)
-- Dependencies: 217
-- Name: audit_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.audit_logs_id_seq OWNED BY public.audit_logs.id;


--
-- TOC entry 216 (class 1259 OID 16680)
-- Name: clients; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.clients (
    id character varying NOT NULL,
    name character varying NOT NULL,
    age integer NOT NULL,
    room character varying NOT NULL,
    date_of_birth character varying NOT NULL,
    support_needs text NOT NULL
);


ALTER TABLE public.clients OWNER TO admin;

--
-- TOC entry 220 (class 1259 OID 16714)
-- Name: schedules; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.schedules (
    id character varying NOT NULL,
    carer_email character varying NOT NULL,
    client_id character varying NOT NULL,
    date character varying NOT NULL,
    start_time character varying NOT NULL,
    end_time character varying NOT NULL,
    shift_type character varying NOT NULL,
    status character varying NOT NULL,
    notes text
);


ALTER TABLE public.schedules OWNER TO admin;

--
-- TOC entry 215 (class 1259 OID 16672)
-- Name: users; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users (
    email character varying NOT NULL,
    password_hash character varying NOT NULL,
    role character varying NOT NULL,
    name character varying,
    phone character varying,
    department character varying,
    family_id character varying
);


ALTER TABLE public.users OWNER TO admin;

--
-- TOC entry 221 (class 1259 OID 16732)
-- Name: visit_logs; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.visit_logs (
    id character varying NOT NULL,
    client_id character varying NOT NULL,
    carer_name character varying NOT NULL,
    carer_number character varying,
    date timestamp without time zone NOT NULL,
    personal_care_completed boolean NOT NULL,
    care_reminders_provided text NOT NULL,
    toilet boolean NOT NULL,
    changed_clothes boolean NOT NULL,
    ate_food text NOT NULL,
    notes text NOT NULL,
    mood json
);


ALTER TABLE public.visit_logs OWNER TO admin;

--
-- TOC entry 4755 (class 2604 OID 16692)
-- Name: audit_logs id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.audit_logs ALTER COLUMN id SET DEFAULT nextval('public.audit_logs_id_seq'::regclass);


--
-- TOC entry 4924 (class 0 OID 16697)
-- Dependencies: 219
-- Data for Name: assignments; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.assignments (user_email, client_id) FROM stdin;
sarah.jones@carehome.com	C001
sarah.jones@carehome.com	C002
mike.wilson@carehome.com	C003
mike.wilson@carehome.com	C004
emma.brown@carehome.com	C005
emma.brown@carehome.com	C006
alex.taylor@carehome.com	C007
lisa.white@carehome.com	C008
mary.johnson@gmail.com	C001
david.davis@outlook.com	C002
linda.thompson@yahoo.com	C003
susan.miller@gmail.com	C004
james.wilson@hotmail.com	C005
\.


--
-- TOC entry 4923 (class 0 OID 16689)
-- Dependencies: 218
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.audit_logs (id, user_email, action, entity_type, entity_id, "timestamp") FROM stdin;
\.


--
-- TOC entry 4921 (class 0 OID 16680)
-- Dependencies: 216
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.clients (id, name, age, room, date_of_birth, support_needs) FROM stdin;
C002	Margaret Davis	82	102B	1942-07-22	Memory support, mobility assistance, fall prevention. Needs supervision and gentle encouragement for daily activities.
C003	William Thompson	75	103A	1949-11-08	Respiratory support, mobility assistance, emotional support. Requires breathing support equipment and limited mobility assistance.
C004	Dorothy Miller	88	201C	1936-01-30	Memory support, mobility assistance, personal care. Requires full assistance with personal care and gentle reassurance.
C005	Charles Wilson	71	202A	1953-09-12	Movement support, swallowing assistance. Requires modified diet and movement support care.
C006	Betty Anderson	79	203B	1945-05-18	Recovery support, left side weakness, communication assistance. Movement therapy ongoing.
C007	Frank Martinez	84	204A	1940-12-03	Kidney support care, dietary assistance, vision support. Special care routine 3x weekly.
C008	Helen Garcia	76	205C	1948-04-25	Recovery support, anxiety management, comfort care. Comfort management care plan in place.
C001	Robert Johnson	21	101A	1946-03-15	Personal care assistance, mobility support, medication reminders. Requires assistance with daily activities and personal care routines.
\.


--
-- TOC entry 4925 (class 0 OID 16714)
-- Dependencies: 220
-- Data for Name: schedules; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.schedules (id, carer_email, client_id, date, start_time, end_time, shift_type, status, notes) FROM stdin;
SCH8877832D	mike.wilson@carehome.com	C003	2025-07-18	09:00	12:00	morning	in_progress	Respiratory support session ongoing
SCH2E274040	emma.brown@carehome.com	C005	2025-07-18	14:00	17:00	afternoon	scheduled	Movement therapy and personal care
SCH0CAD6DEA	alex.taylor@carehome.com	C007	2025-07-18	16:00	19:00	evening	scheduled	Evening care and medication support
SCH97C595D4	sarah.jones@carehome.com	C002	2025-07-19	08:30	11:30	morning	scheduled	Memory support and mobility assistance
SCHAA753CB8	lisa.white@carehome.com	C008	2025-07-19	10:00	13:00	morning	scheduled	Anxiety management and comfort care
SCH08F13D1D	susan.miller@gmail.com	C001	stringstri	strin	strin	string	scheduled	string
SCHCD347F51	alex.taylor@carehome.com	C001	stringstri	strin	strin	string	scheduled	string
SCHB70DAE40	alex.taylor@carehome.com	C001	stringstri	strin	strin	string	scheduled	string
SCHE8E5B92E	david.davis@outlook.com	C001	stringstri	strin	strin	string	scheduled	string
\.


--
-- TOC entry 4920 (class 0 OID 16672)
-- Dependencies: 215
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users (email, password_hash, role, name, phone, department, family_id) FROM stdin;
admin@carehome.com	$2b$12$ux.Cp6UdfAyLggZOUvFJd.X6MJFkeLi4dbPsJTUmeXFIB63Z4xVvi	admin	\N	\N	\N	\N
nurse.supervisor@carehome.com	$2b$12$vsJ.WfbSz/wK9d1dz0pBZO4n1VG.Zc/fkhN9croBcyWDefCSeMS2u	manager	Jennifer Taylor	\N	Nursing Supervisor	\N
admin.head@carehome.com	$2b$12$7XbXaY3/.u1wX8LTnAvLROeVDuZQU599NJ50wQ5KIRlFKMl0lb4uG	manager	Robert Chen	\N	Administration	\N
sarah.jones@carehome.com	$2b$12$Q/47N9VVcMTC1KW25Zqzb.mDx8uE7mQyEnMpuNAuQl8vlc2M9A8O.	carer	Sarah Jones	447987654321	\N	\N
mike.wilson@carehome.com	$2b$12$53Yb3ZQuE.Fzzq7V1royEussbSmTm9T/UmIDGjjXku8JvqPpke62q	carer	Mike Wilson	447555123456	\N	\N
emma.brown@carehome.com	$2b$12$C41V8Ipuo.Q9F1vyU8fQY.keFvOkUpBZ0UDYDIMTYBhIYZnWKsfcC	carer	Emma Brown	447666789123	\N	\N
alex.taylor@carehome.com	$2b$12$AE4KwyWu4buEOWPVcIis2Or41Wp9cGycqPBT0.8FwpnoFzFOwxL2.	carer	Alex Taylor	447123987654	\N	\N
lisa.white@carehome.com	$2b$12$ss.9B11WZI0/hainl5GdNuANb1ma4mJIPajZNbORoTNkjv1.tKmq.	carer	Lisa White	447888999000	\N	\N
mary.johnson@gmail.com	$2b$12$welLtvlquTGjNWBD17wZ3.sLQm6zstsPcxVUwt6RcTs.hPyRs.6VG	family	Mary Johnson	447111222333	\N	F001
david.davis@outlook.com	$2b$12$J5zNozUwv9Q.yFWzGYezIeu522.Kr6JLYaHMozVpyn69lItUgy9Ra	family	David Davis	447444555666	\N	F002
susan.miller@gmail.com	$2b$12$MysoKLlidr1UjHA6oLoLVOGyYX0tT09zns/MjZPvKiCbYkKq7C.8W	family	Susan Miller	447222333444	\N	F004
james.wilson@hotmail.com	$2b$12$bbRqJ1J21BjsADy2ejjRhepANDzcsfK0Py8nlycBfeJelREa8SLRu	family	James Wilson Jr	447555666777	\N	F005
linda.thompson@yahoo.com	$2b$12$9u.Flx6h377qsjRuhbJsKORTnOyK4TgTwmGQG.wklObwEa10bF1Ma	family	string	447777888999	\N	F003
dr.smith@carehome.com	$2b$12$jZbQ0Mh.RempOPl8CFY5r.h210jqc1V4zENShKSfuKIZ/HnZOU0YG	manager	string	\N	Medical Director	\N
\.


--
-- TOC entry 4926 (class 0 OID 16732)
-- Dependencies: 221
-- Data for Name: visit_logs; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.visit_logs (id, client_id, carer_name, carer_number, date, personal_care_completed, care_reminders_provided, toilet, changed_clothes, ate_food, notes, mood) FROM stdin;
VL8C7608A4	C001	Sarah Jones	447987654321	2025-07-18 13:20:21.507291	t	Morning medication reminders provided as requested, all care preferences followed	t	t	Enjoyed full breakfast, dietary preferences accommodated	Client in good spirits today. All care routines completed successfully. Mobility exercises done.	["happy", "cooperative"]
VL7610F64F	C002	Sarah Jones	447987654321	2025-07-18 13:20:21.507426	t	Memory support provided, daily routine reinforced	t	t	Assisted with lunch, ate well with encouragement	Better orientation today. Client remembered carer's name and enjoyed conversation about her past.	["alert", "nostalgic"]
VLC3E4A331	C003	Mike Wilson	447555123456	2025-07-18 13:20:21.507503	f	Breathing support equipment checked and functioning well	t	t	Small portions due to breathing comfort, appetite maintained	Respiratory therapy session completed. Client positioned comfortably. Movement exercises adapted for breathing.	["determined", "comfortable"]
VL9FC296E7	C006	string	string	2025-07-18 13:42:41.22	t	string	t	t	string	string	[]
VLD46F72EF	C006	string	string	2025-07-18 13:42:41.22	t	string	t	t	string	string	[]
\.


--
-- TOC entry 4936 (class 0 OID 0)
-- Dependencies: 217
-- Name: audit_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.audit_logs_id_seq', 1, false);


--
-- TOC entry 4765 (class 2606 OID 16703)
-- Name: assignments assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_pkey PRIMARY KEY (user_email, client_id);


--
-- TOC entry 4763 (class 2606 OID 16696)
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- TOC entry 4760 (class 2606 OID 16686)
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (id);


--
-- TOC entry 4768 (class 2606 OID 16720)
-- Name: schedules schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_pkey PRIMARY KEY (id);


--
-- TOC entry 4758 (class 2606 OID 16678)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (email);


--
-- TOC entry 4771 (class 2606 OID 16738)
-- Name: visit_logs visit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.visit_logs
    ADD CONSTRAINT visit_logs_pkey PRIMARY KEY (id);


--
-- TOC entry 4761 (class 1259 OID 16687)
-- Name: ix_clients_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_clients_id ON public.clients USING btree (id);


--
-- TOC entry 4766 (class 1259 OID 16731)
-- Name: ix_schedules_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_schedules_id ON public.schedules USING btree (id);


--
-- TOC entry 4756 (class 1259 OID 16679)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 4769 (class 1259 OID 16744)
-- Name: ix_visit_logs_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_visit_logs_id ON public.visit_logs USING btree (id);


--
-- TOC entry 4772 (class 2606 OID 16709)
-- Name: assignments assignments_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id) ON DELETE CASCADE;


--
-- TOC entry 4773 (class 2606 OID 16704)
-- Name: assignments assignments_user_email_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_user_email_fkey FOREIGN KEY (user_email) REFERENCES public.users(email) ON DELETE CASCADE;


--
-- TOC entry 4774 (class 2606 OID 16721)
-- Name: schedules schedules_carer_email_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_carer_email_fkey FOREIGN KEY (carer_email) REFERENCES public.users(email);


--
-- TOC entry 4775 (class 2606 OID 16726)
-- Name: schedules schedules_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id);


--
-- TOC entry 4776 (class 2606 OID 16739)
-- Name: visit_logs visit_logs_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.visit_logs
    ADD CONSTRAINT visit_logs_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id);


--
-- TOC entry 4934 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: admin
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2025-07-19 11:55:47

--
-- PostgreSQL database dump complete
--

