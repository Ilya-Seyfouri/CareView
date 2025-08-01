--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 16.9

-- Started on 2025-07-31 19:09:30

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
-- TOC entry 219 (class 1259 OID 16918)
-- Name: assignments; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.assignments (
    user_email character varying NOT NULL,
    client_id character varying NOT NULL
);


ALTER TABLE public.assignments OWNER TO admin;

--
-- TOC entry 218 (class 1259 OID 16910)
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
-- TOC entry 217 (class 1259 OID 16909)
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
-- TOC entry 216 (class 1259 OID 16901)
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
-- TOC entry 220 (class 1259 OID 16935)
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
    notes text,
    completed_at character varying
);


ALTER TABLE public.schedules OWNER TO admin;

--
-- TOC entry 215 (class 1259 OID 16893)
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
-- TOC entry 221 (class 1259 OID 16953)
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
    mood json,
    last_updated_by character varying,
    last_updated_at timestamp without time zone
);


ALTER TABLE public.visit_logs OWNER TO admin;

--
-- TOC entry 4755 (class 2604 OID 16913)
-- Name: audit_logs id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.audit_logs ALTER COLUMN id SET DEFAULT nextval('public.audit_logs_id_seq'::regclass);


--
-- TOC entry 4924 (class 0 OID 16918)
-- Dependencies: 219
-- Data for Name: assignments; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.assignments (user_email, client_id) FROM stdin;
emily.watson@carehome.com	CL001
emily.watson@carehome.com	CL002
emily.watson@carehome.com	CL003
michael.johnson@carehome.com	CL004
michael.johnson@carehome.com	CL005
lisa.chen@carehome.com	CL006
lisa.chen@carehome.com	CL007
lisa.chen@carehome.com	CL008
james.brown@carehome.com	CL009
james.brown@carehome.com	CL010
anna.williams@carehome.com	CL001
anna.williams@carehome.com	CL005
carer@demo.com	CL002
john.smith@family.com	CL001
mary.jones@family.com	CL002
peter.wilson@family.com	CL003
susan.davis@family.com	CL004
family@demo.com	CL001
carer@demo.com	CL001
carer@demo.com	CL003
\.


--
-- TOC entry 4923 (class 0 OID 16910)
-- Dependencies: 218
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.audit_logs (id, user_email, action, entity_type, entity_id, "timestamp") FROM stdin;
1	admin@carehome.com	login	user	admin@carehome.com	2025-07-29 20:58:03.894353
2	manager@carehome.com	created	client	CL001	2025-07-31 14:58:03.894353
3	manager@carehome.com	created	schedule	SCH001	2025-07-31 04:58:03.894353
4	emily.watson@carehome.com	login	user	emily.watson@carehome.com	2025-07-30 17:58:03.894353
5	emily.watson@carehome.com	created	visit_log	VL001	2025-07-29 10:58:03.894353
6	emily.watson@carehome.com	updated	schedule_status	SCH001	2025-07-30 15:58:03.894353
7	manager@carehome.com	assigned	carer_client	emily.watson@carehome.com-CL001	2025-07-28 19:58:03.894353
8	admin@carehome.com	created	manager	headmanager@carehome.com	2025-07-30 17:58:03.894353
9	lisa.chen@carehome.com	login	user	lisa.chen@carehome.com	2025-07-30 10:58:03.894353
10	michael.johnson@carehome.com	completed	schedule	SCH002	2025-07-31 02:58:03.894353
11	family@demo.com	viewed	client	CL001	2025-07-30 00:58:03.894353
12	manager@carehome.com	updated	client	CL002	2025-07-29 09:58:03.894353
13	manager@demo.com	created	schedule	SCH1C267C51	2025-07-31 17:12:38.758154
14	manager@demo.com	created	visit_log	VL4E62DDF1	2025-07-31 17:14:22.30698
15	carer@demo.com	created	visit_log	VLB4A08DAD	2025-07-31 17:15:33.882452
16	manager@demo.com	created	schedule	SCHA3B87900	2025-07-31 17:18:38.109592
\.


--
-- TOC entry 4921 (class 0 OID 16901)
-- Dependencies: 216
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.clients (id, name, age, room, date_of_birth, support_needs) FROM stdin;
CL001	Robert Wilson	78	101A	1946-03-15	Advanced dementia care. Requires assistance with all daily activities. Enjoys music therapy and gentle hand massage. Family visits regularly on weekends. Prefers routine and familiar faces.
CL002	Margaret Thompson	82	102B	1942-07-22	Moderate dementia with sundowning. Independent with eating but needs encouragement. Loves looking at family photos and listening to 1960s music. Can become agitated in the evenings.
CL003	James Patterson	75	103A	1949-11-08	Type 2 diabetes requiring 4x daily blood glucose monitoring. Insulin dependent. Mobility issues with left leg. Enjoys reading newspapers and discussing current events.
CL004	Dorothy Davis	79	104B	1945-09-12	Post-stroke rehabilitation. Right-side weakness requiring mobility assistance. Speech therapy exercises twice weekly. Passionate about gardening and bird watching.
CL005	William Miller	81	105A	1943-01-30	Congestive heart failure. Requires daily weight monitoring and fluid restriction. Oxygen therapy at night. Former teacher who enjoys chess and helping other residents.
CL006	Elizabeth Brown	77	106B	1947-06-18	Parkinson's disease with tremors and balance issues. Requires assistance with fine motor tasks. Medication timing is critical. Loves classical music and poetry readings.
CL007	Thomas Anderson	84	107A	1940-12-03	Mild cognitive impairment. Generally independent but needs reminders for medications. Former engineer who enjoys building puzzles and mechanical projects.
CL008	Helen Carter	76	108B	1948-04-25	Chronic pain management from arthritis. Uses wheelchair for longer distances. Very social and organizes resident activities. Requires pain medication management.
CL009	George Williams	80	109A	1944-08-14	Recent hip replacement recovery. Physical therapy 3x weekly. Former military officer who appreciates routine and order. Enjoys war documentaries and memoirs.
CL010	Betty Taylor	83	110B	1941-02-08	Advanced macular degeneration - legally blind. Requires assistance with navigation and reading. Exceptional hearing and memory. Loves audiobooks and music.
\.


--
-- TOC entry 4925 (class 0 OID 16935)
-- Dependencies: 220
-- Data for Name: schedules; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.schedules (id, carer_email, client_id, date, start_time, end_time, shift_type, status, notes, completed_at) FROM stdin;
SCHDB51536E	emily.watson@carehome.com	CL001	2025-07-24	09:00	10:30	morning	completed	Morning dementia care completed successfully	\N
SCH7A7616F9	michael.johnson@carehome.com	CL004	2025-07-24	14:00	15:30	afternoon	completed	Post-stroke physiotherapy and mobility exercises	\N
SCH825E0317	emily.watson@carehome.com	CL001	2025-07-25	09:00	10:30	morning	completed	Morning dementia care completed successfully	\N
SCHBA8804FB	michael.johnson@carehome.com	CL004	2025-07-25	14:00	15:30	afternoon	completed	Post-stroke physiotherapy and mobility exercises	\N
SCHAA446A01	emily.watson@carehome.com	CL001	2025-07-26	09:00	10:30	morning	completed	Morning dementia care completed successfully	\N
SCHA8CB3C1B	michael.johnson@carehome.com	CL004	2025-07-26	14:00	15:30	afternoon	completed	Post-stroke physiotherapy and mobility exercises	\N
SCH4C969D09	emily.watson@carehome.com	CL001	2025-07-27	09:00	10:30	morning	completed	Morning dementia care completed successfully	\N
SCHDAFDCDBE	michael.johnson@carehome.com	CL004	2025-07-27	14:00	15:30	afternoon	completed	Post-stroke physiotherapy and mobility exercises	\N
SCHDAF0CF0E	emily.watson@carehome.com	CL001	2025-07-28	09:00	10:30	morning	completed	Morning dementia care completed successfully	\N
SCHA8B37A11	michael.johnson@carehome.com	CL004	2025-07-28	14:00	15:30	afternoon	completed	Post-stroke physiotherapy and mobility exercises	\N
SCH2441ECA5	emily.watson@carehome.com	CL001	2025-07-29	09:00	10:30	morning	completed	Morning dementia care completed successfully	\N
SCH27918224	michael.johnson@carehome.com	CL004	2025-07-29	14:00	15:30	afternoon	completed	Post-stroke physiotherapy and mobility exercises	\N
SCH79BCBCA7	emily.watson@carehome.com	CL001	2025-07-30	09:00	10:30	morning	completed	Morning dementia care completed successfully	\N
SCH0DCE82E0	michael.johnson@carehome.com	CL004	2025-07-30	14:00	15:30	afternoon	completed	Post-stroke physiotherapy and mobility exercises	\N
SCHAF7C52A2	emily.watson@carehome.com	CL001	2025-07-31	08:30	10:00	morning	completed	Morning routine and medication administration	\N
SCH7C130977	lisa.chen@carehome.com	CL006	2025-07-31	11:00	12:30	morning	in_progress	Parkinson's care and tremor management	\N
SCH6D5096D5	james.brown@carehome.com	CL009	2025-07-31	15:00	16:30	afternoon	scheduled	Hip replacement recovery exercises	\N
SCH5B4A491F	lisa.chen@carehome.com	CL005	2025-08-01	19:00	15:30	evening	scheduled	Routine care visit scheduled	\N
SCH73AE8D1D	lisa.chen@carehome.com	CL001	2025-08-02	09:00	10:30	afternoon	scheduled	Routine care visit scheduled	\N
SCHDA2BE814	michael.johnson@carehome.com	CL002	2025-08-03	09:00	20:30	morning	scheduled	Routine care visit scheduled	\N
SCH94415081	michael.johnson@carehome.com	CL004	2025-08-04	09:00	20:30	evening	scheduled	Routine care visit scheduled	\N
SCH1E9B5352	michael.johnson@carehome.com	CL003	2025-08-05	14:00	15:30	evening	scheduled	Routine care visit scheduled	\N
SCH46D1595E	emily.watson@carehome.com	CL001	2025-08-06	19:00	15:30	morning	scheduled	Routine care visit scheduled	\N
SCH953E560C	michael.johnson@carehome.com	CL002	2025-08-07	19:00	15:30	afternoon	scheduled	Routine care visit scheduled	\N
SCH257F0D05	carer@demo.com	CL001	2025-07-31	19:00	20:00	evening	completed	Evening care and bedtime routine	2025-07-31 18:16:31
SCHA3B87900	carer@demo.com	CL001	2025-07-31	20:00	23:00	Medication Assistance	scheduled		\N
\.


--
-- TOC entry 4920 (class 0 OID 16893)
-- Dependencies: 215
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users (email, password_hash, role, name, phone, department, family_id) FROM stdin;
admin@carehome.com	$2b$12$EQ3Z.8SoP8LdQqAOZB0K3uJo1P.1DMVVB.PhXTel0fm93gcmXgqeG	admin	System Administrator	\N	\N	\N
manager@carehome.com	$2b$12$MnYQ84Kd/fIs80JJreWyW.Pe5puAI1YfW6lmVq/yInzZ3H/q.vp9e	manager	Sarah Harrison	\N	Care Management	\N
headmanager@carehome.com	$2b$12$Pgc2mgRIEOighinWbMbDYuuuZl4yxue1oFX7vMFyMr6AyiEZ4i7IC	manager	David Thompson	\N	Operations	\N
nightmanager@carehome.com	$2b$12$dCy.LiaBk7TdN7Wy8gwq2O7kDzY4yJLoBsBJo24pZowweUo2jQyjq	manager	Rachel Green	\N	Night Operations	\N
emily.watson@carehome.com	$2b$12$1QxdIMjTkrFz7LM3kkK/UO3S6H81VWldX9n87MwyhVCfN0DvAM.T2	carer	Emily Watson	01234 567 890	\N	\N
michael.johnson@carehome.com	$2b$12$XCd7HA2HLK4CQ/f4vgM0oex1WzKhtmkVD7FeD77VT5RDSc/Jqtjh2	carer	Michael Johnson	01234 567 891	\N	\N
lisa.chen@carehome.com	$2b$12$w8NPDlBQbUpzTwHZMgH9nOM0XuOpLTma/sDsCeuduWQw1p5eH2ccO	carer	Lisa Chen	01234 567 892	\N	\N
james.brown@carehome.com	$2b$12$grIJuWAiq7mI4Pymjm.Wvutd3ZPxd5iXEi0Id5S6S8or4Qa1ogGbS	carer	James Brown	01234 567 893	\N	\N
anna.williams@carehome.com	$2b$12$KXh5jZQ.aA9pkcz16tkjNunVtVfgEoNy3r2Q63dmDNvacGEeYdnuW	carer	Anna Williams	01234 567 894	\N	\N
john.smith@family.com	$2b$12$zJU2NKH.kLj7eW9lt.GtdedZI9KTE9K./5DpuLfppLHGFpIy1JhyG	family	John Smith	07700 123 456	\N	FAM001
mary.jones@family.com	$2b$12$PWsO3Zoy8FmGTKaLUeQOleICjRWMjyKstcvA5ZhNMnwLkEmsfMJHe	family	Mary Jones	07700 123 457	\N	FAM002
peter.wilson@family.com	$2b$12$wwtcwcjvz.55q3zEpt5KN.CM9Lq0hDmE0TLlV6NZ76.lm9YRyy/0C	family	Peter Wilson	07700 123 458	\N	FAM003
susan.davis@family.com	$2b$12$H9W0ToVysiPRIRREjlULwuQjkv/DncG09U3mT6QCYeG9P7i0tUoeO	family	Susan Davis	07700 123 459	\N	FAM004
admin@demo.com	$2b$12$sm0ndzYTQ0Wub6phrmWIouk.yjWtMZUTwKhgAcTiAdnAVpWe3SRTG	admin	Demo Admin	\N	\N	\N
manager@demo.com	$2b$12$/9cF5iGpxcEk3f.wEjE8XOFdIy4wizuAylZVijxoHlkn95uYvwvO2	manager	Demo Manager	\N	Demo Department	\N
carer@demo.com	$2b$12$mbFbD.HU3UATUit0YDHAz.TqovA/owzdkdWLgxqERh769TAgq6ex6	carer	Demo Carer	01234 567 999	\N	\N
family@demo.com	$2b$12$MRgW4dvLCsiFyPaFdYelNemhEIkvm3Sz55B/H50P07eBy9ZYI4NPa	family	Demo Family	07700 123 9993	\N	FAM999
\.


--
-- TOC entry 4926 (class 0 OID 16953)
-- Dependencies: 221
-- Data for Name: visit_logs; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.visit_logs (id, client_id, carer_name, carer_number, date, personal_care_completed, care_reminders_provided, toilet, changed_clothes, ate_food, notes, mood, last_updated_by, last_updated_at) FROM stdin;
VL0387A5AA	CL001	Emily Watson	01234 567 890	2025-07-31 12:58:03.889785	t	Administered morning medications including donepezil. Gentle encouragement with breakfast routine.	t	t	Full breakfast consumed - porridge with honey, tea with 2 sugars. Ate well today.	Robert was in excellent spirits. Recognized me immediately and asked about my weekend. Mobility stable, no falls. Family photo session helped with reminiscence.	["happy", "alert", "cooperative"]	\N	\N
VLADD95819	CL001	Emily Watson	01234 567 890	2025-07-30 16:58:03.889785	t	Administered morning medications including donepezil. Gentle encouragement with breakfast routine.	t	t	Full breakfast consumed - porridge with honey, tea with 2 sugars. Ate well today.	Robert was in excellent spirits. Recognized me immediately and asked about my weekend. Mobility stable, no falls. Family photo session helped with reminiscence.	["happy", "alert", "cooperative"]	\N	\N
VL3A6B2663	CL001	Emily Watson	01234 567 890	2025-07-29 15:58:03.889785	t	Administered morning medications including donepezil. Gentle encouragement with breakfast routine.	t	t	Full breakfast consumed - porridge with honey, tea with 2 sugars. Ate well today.	Robert was in excellent spirits. Recognized me immediately and asked about my weekend. Mobility stable, no falls. Family photo session helped with reminiscence.	["happy", "alert", "cooperative"]	\N	\N
VLCB840877	CL002	Emily Watson	01234 567 890	2025-07-31 10:58:03.889785	t	Gentle encouragement needed with personal hygiene. Music therapy during care routine.	t	t	Partial breakfast - encouraged to finish orange juice. Prefers finger foods.	Margaret showed some confusion this morning but responded well to familiar songs from the 1960s. Agitation reduced when shown family photos.	["confused", "calmer after music", "responsive to photos"]	\N	\N
VL7EA1AF3A	CL002	Emily Watson	01234 567 890	2025-07-30 14:58:03.889785	t	Gentle encouragement needed with personal hygiene. Music therapy during care routine.	t	t	Partial breakfast - encouraged to finish orange juice. Prefers finger foods.	Margaret showed some confusion this morning but responded well to familiar songs from the 1960s. Agitation reduced when shown family photos.	["confused", "calmer after music", "responsive to photos"]	\N	\N
VL13509B37	CL002	Emily Watson	01234 567 890	2025-07-29 15:58:03.889785	t	Gentle encouragement needed with personal hygiene. Music therapy during care routine.	t	t	Partial breakfast - encouraged to finish orange juice. Prefers finger foods.	Margaret showed some confusion this morning but responded well to familiar songs from the 1960s. Agitation reduced when shown family photos.	["confused", "calmer after music", "responsive to photos"]	\N	\N
VL733A8432	CL003	Michael Johnson	01234 567 891	2025-07-31 14:58:03.889785	t	Blood glucose check: 8.2 mmol/L (target range). Insulin administered as prescribed.	t	f	Diabetic breakfast - controlled carbohydrates. Discussed newspaper headlines during meal.	James is managing his diabetes well. Enjoyed discussion about local football results. Left leg mobility slightly improved from yesterday.	["cheerful", "engaged", "independent"]	\N	\N
VL89923287	CL003	Michael Johnson	01234 567 891	2025-07-30 12:58:03.889785	t	Blood glucose check: 8.2 mmol/L (target range). Insulin administered as prescribed.	t	f	Diabetic breakfast - controlled carbohydrates. Discussed newspaper headlines during meal.	James is managing his diabetes well. Enjoyed discussion about local football results. Left leg mobility slightly improved from yesterday.	["cheerful", "engaged", "independent"]	\N	\N
VL56F87274	CL003	Michael Johnson	01234 567 891	2025-07-29 09:58:03.889785	t	Blood glucose check: 8.2 mmol/L (target range). Insulin administered as prescribed.	t	f	Diabetic breakfast - controlled carbohydrates. Discussed newspaper headlines during meal.	James is managing his diabetes well. Enjoyed discussion about local football results. Left leg mobility slightly improved from yesterday.	["cheerful", "engaged", "independent"]	\N	\N
VL51136321	CL004	Michael Johnson	01234 567 891	2025-07-31 12:58:03.889785	t	Speech exercises completed - pronunciation improving. Right arm strengthening exercises.	t	t	Soft diet breakfast, needs encouragement with swallowing. Thickened fluids as per speech therapy.	Dorothy completed all physiotherapy exercises today. Speech clarity improved. Excited about garden visit this afternoon - spotted new birds from window.	["determined", "optimistic", "excited about gardening"]	\N	\N
VL52697767	CL004	Michael Johnson	01234 567 891	2025-07-30 16:58:03.889785	t	Speech exercises completed - pronunciation improving. Right arm strengthening exercises.	t	t	Soft diet breakfast, needs encouragement with swallowing. Thickened fluids as per speech therapy.	Dorothy completed all physiotherapy exercises today. Speech clarity improved. Excited about garden visit this afternoon - spotted new birds from window.	["determined", "optimistic", "excited about gardening"]	\N	\N
VL58ADF8BC	CL005	Lisa Chen	01234 567 892	2025-07-31 11:58:03.889785	t	Daily weight check: stable. Fluid restriction discussed. Heart medication administered.	t	t	Low-sodium breakfast. Monitored fluid intake carefully.	William's breathing comfortable today. No ankle swelling observed. Helped new resident settle in - natural mentor personality shining through.	["stable", "helpful", "mentor-like"]	\N	\N
VLB4A08DAD	CL001	carer@demo.com	01234 567 999	2025-07-31 17:15:00	t	f3rewdc,	f	f	f3r xef2wds	3fgbhewnd shnfewmd s	["Cooperative"]	\N	\N
\.


--
-- TOC entry 4936 (class 0 OID 0)
-- Dependencies: 217
-- Name: audit_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.audit_logs_id_seq', 16, true);


--
-- TOC entry 4765 (class 2606 OID 16924)
-- Name: assignments assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_pkey PRIMARY KEY (user_email, client_id);


--
-- TOC entry 4763 (class 2606 OID 16917)
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- TOC entry 4760 (class 2606 OID 16907)
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (id);


--
-- TOC entry 4768 (class 2606 OID 16941)
-- Name: schedules schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_pkey PRIMARY KEY (id);


--
-- TOC entry 4758 (class 2606 OID 16899)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (email);


--
-- TOC entry 4771 (class 2606 OID 16959)
-- Name: visit_logs visit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.visit_logs
    ADD CONSTRAINT visit_logs_pkey PRIMARY KEY (id);


--
-- TOC entry 4761 (class 1259 OID 16908)
-- Name: ix_clients_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_clients_id ON public.clients USING btree (id);


--
-- TOC entry 4766 (class 1259 OID 16952)
-- Name: ix_schedules_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_schedules_id ON public.schedules USING btree (id);


--
-- TOC entry 4756 (class 1259 OID 16900)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 4769 (class 1259 OID 16965)
-- Name: ix_visit_logs_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_visit_logs_id ON public.visit_logs USING btree (id);


--
-- TOC entry 4772 (class 2606 OID 16930)
-- Name: assignments assignments_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id) ON DELETE CASCADE;


--
-- TOC entry 4773 (class 2606 OID 16925)
-- Name: assignments assignments_user_email_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_user_email_fkey FOREIGN KEY (user_email) REFERENCES public.users(email) ON DELETE CASCADE;


--
-- TOC entry 4774 (class 2606 OID 16942)
-- Name: schedules schedules_carer_email_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_carer_email_fkey FOREIGN KEY (carer_email) REFERENCES public.users(email);


--
-- TOC entry 4775 (class 2606 OID 16947)
-- Name: schedules schedules_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id);


--
-- TOC entry 4776 (class 2606 OID 16960)
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


-- Completed on 2025-07-31 19:09:30

--
-- PostgreSQL database dump complete
--

