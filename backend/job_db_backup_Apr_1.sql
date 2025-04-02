--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Postgres.app)
-- Dumped by pg_dump version 17.4 (Postgres.app)

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: job_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO job_user;

--
-- Name: applications; Type: TABLE; Schema: public; Owner: job_user
--

CREATE TABLE public.applications (
    id integer NOT NULL,
    user_id integer NOT NULL,
    job_id integer NOT NULL,
    resume_id integer NOT NULL,
    application_url character varying,
    application_status character varying,
    applied_date timestamp without time zone NOT NULL,
    updated_at timestamp without time zone
);


ALTER TABLE public.applications OWNER TO job_user;

--
-- Name: applications_id_seq; Type: SEQUENCE; Schema: public; Owner: job_user
--

CREATE SEQUENCE public.applications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.applications_id_seq OWNER TO job_user;

--
-- Name: applications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: job_user
--

ALTER SEQUENCE public.applications_id_seq OWNED BY public.applications.id;


--
-- Name: job_matches; Type: TABLE; Schema: public; Owner: job_user
--

CREATE TABLE public.job_matches (
    id integer NOT NULL,
    user_id integer NOT NULL,
    job_id integer NOT NULL,
    resume_id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    matched_skills text,
    missing_skills text,
    calculated_at timestamp without time zone,
    ats_score_initial double precision,
    ats_score_final double precision,
    match_score_initial double precision NOT NULL,
    match_score_final double precision NOT NULL
);


ALTER TABLE public.job_matches OWNER TO job_user;

--
-- Name: job_matches_id_seq; Type: SEQUENCE; Schema: public; Owner: job_user
--

CREATE SEQUENCE public.job_matches_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.job_matches_id_seq OWNER TO job_user;

--
-- Name: job_matches_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: job_user
--

ALTER SEQUENCE public.job_matches_id_seq OWNED BY public.job_matches.id;


--
-- Name: jobs; Type: TABLE; Schema: public; Owner: job_user
--

CREATE TABLE public.jobs (
    id integer NOT NULL,
    job_title character varying NOT NULL,
    company_name character varying NOT NULL,
    location character varying,
    job_description text NOT NULL,
    job_url character varying,
    extracted_skills text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone
);


ALTER TABLE public.jobs OWNER TO job_user;

--
-- Name: jobs_id_seq; Type: SEQUENCE; Schema: public; Owner: job_user
--

CREATE SEQUENCE public.jobs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.jobs_id_seq OWNER TO job_user;

--
-- Name: jobs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: job_user
--

ALTER SEQUENCE public.jobs_id_seq OWNED BY public.jobs.id;


--
-- Name: resumes; Type: TABLE; Schema: public; Owner: job_user
--

CREATE TABLE public.resumes (
    id integer NOT NULL,
    user_id integer NOT NULL,
    file_path character varying,
    parsed_text text,
    created_at timestamp without time zone NOT NULL,
    optimized_text text,
    is_ai_generated boolean,
    is_user_approved boolean,
    updated_at timestamp without time zone,
    ats_score_initial double precision,
    ats_score_final double precision
);


ALTER TABLE public.resumes OWNER TO job_user;

--
-- Name: resumes_id_seq; Type: SEQUENCE; Schema: public; Owner: job_user
--

CREATE SEQUENCE public.resumes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.resumes_id_seq OWNER TO job_user;

--
-- Name: resumes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: job_user
--

ALTER SEQUENCE public.resumes_id_seq OWNED BY public.resumes.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: job_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    full_name character varying,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO job_user;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: job_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO job_user;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: job_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: applications id; Type: DEFAULT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.applications ALTER COLUMN id SET DEFAULT nextval('public.applications_id_seq'::regclass);


--
-- Name: job_matches id; Type: DEFAULT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.job_matches ALTER COLUMN id SET DEFAULT nextval('public.job_matches_id_seq'::regclass);


--
-- Name: jobs id; Type: DEFAULT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.jobs ALTER COLUMN id SET DEFAULT nextval('public.jobs_id_seq'::regclass);


--
-- Name: resumes id; Type: DEFAULT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.resumes ALTER COLUMN id SET DEFAULT nextval('public.resumes_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: job_user
--

COPY public.alembic_version (version_num) FROM stdin;
f17abfe9c725
\.


--
-- Data for Name: applications; Type: TABLE DATA; Schema: public; Owner: job_user
--

COPY public.applications (id, user_id, job_id, resume_id, application_url, application_status, applied_date, updated_at) FROM stdin;
\.


--
-- Data for Name: job_matches; Type: TABLE DATA; Schema: public; Owner: job_user
--

COPY public.job_matches (id, user_id, job_id, resume_id, created_at, matched_skills, missing_skills, calculated_at, ats_score_initial, ats_score_final, match_score_initial, match_score_final) FROM stdin;
\.


--
-- Data for Name: jobs; Type: TABLE DATA; Schema: public; Owner: job_user
--

COPY public.jobs (id, job_title, company_name, location, job_description, job_url, extracted_skills, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: resumes; Type: TABLE DATA; Schema: public; Owner: job_user
--

COPY public.resumes (id, user_id, file_path, parsed_text, created_at, optimized_text, is_ai_generated, is_user_approved, updated_at, ats_score_initial, ats_score_final) FROM stdin;
2	1	uploads/resumes/70a39ff4-fb44-4fa6-a16d-55d120d299bb_Jiang-Eugene-Critique-Updated-Mar-31.docx	Eugene Jiang\nVancouver, BC V3E 0M3 | 604-368-6508 | eugene.jiang@gmail.com | www.linkedin.com/in/eugenejiang\n\nDirector of Software Quality Assurance\n\nVisionary engineering leader scaling high-performing teams, delivering customer-facing applications, and driving technical excellence. Specialize in Agile development, DevOps, and cloud-based applications across SaaS, e-Commerce, Fintech, and Analytics, leveraging data-driven decision-making to optimize engineering practices. Define and execute engineering roadmaps aligned with business objectives and product vision, fostering innovation while mentoring engineers into senior leadership roles. Committed to technical advancement, earning two patents in AI-driven automation and analytics. Collaborate with Product, Design, Customer Success, and Business teams to drive seamless, customer-centric development. Cultivate open culture of growth, aligned product engineering strategy with business goals, and enhanced performance, scalability, and user experience for high-availability SaaS applications.\n\nEngineering Roadmaps | Talent Development | Agile | DevOps | CI/CD | AI/ML\n\nProfessional Experience \n\nWorkday | Vancouver, BC\nDirector of Software Engineer in Test (SDET)\t\t07/2022 – present\nLead high-performing SDET and software engineering teams of 40+ members, focusing on customer-facing testing analytics applications and test infrastructure.\nDefined and standardized product release and feature sign-off processes, reducing customer-reported issues by ~20% YoY through collaboration with quality, product, development, and customer support teams.\nLed engineering transformation for developer productivity, implementing next gen pre-commit solutions (NGPCQ) that improved efficiency by 50% and prevented 6% defective code from merging.\nScaled team from 23 to 40+, mentoring talent and developing multiple engineers into managerial and senior leadership roles.\nEstablished customer-focused, continuous improvement culture by aligning engineering initiatives with business and product strategy by engaging various stakeholders to do production issue analysis and identify area of improvements.\nSpearheaded AI-driven initiatives, including AI Chatbot and Automatic Failure Analysis. Led architecture design and review, supervised the implementation which integrated with NGPCQ achieved efficiency gain.\n\nPayBePhone | Vancouver, BC\nHead of Quality Assurance (QA)\t\t04/2021 – 02/2022\nLed product quality standards and processes, driving testing requirements for performance and security test practices, automation framework, and development process. Implemented Static Code Analysis, code coverage, and CI/CD pipeline using PyTest, SonarQube, GitLab, and AWS to enhance code quality and streamline development workflows.\nDrove production site reliability, improving uptime toward 99.9% availability through cross-team collaboration with Cloud Platform, Architect, Infrastructure, DevOps, Security, PMO, DBA, Development to setup a taskforce, strategy, roadmap, and execution plan which resulted 86% environment issue reduction after the first 5 months. \nImplemented enhanced production deployment process with Jira/Slack integration, increasing developer productivity by 15% time savings.\n\nCheckPay Technologies | Vancouver, BC\nChief Technology Officer (CTO)\t\t08/2020 – 04/2021\nOwned HelloChat app requirements, design, development, quality, build, and release. Managed Development, Product Management, UI/UX, IT Service, and DevOps teams to drive seamless execution and delivery.\nLed successful HelloChat v2 launch on iOS and Android using React Native, doubling user adoption doubled within first 2 months after v2 roll-out.  \n\nCheckPay Technologies | Chief Technology Officer (CTO)\t\tcontinued\nDirected CD pipeline implementation with CircleCI in real-time API services release.\nLed mobile architectural changes on client-side caching using Realm DB with 10x performance gain.  \n\nChief Operating Officer (COO)\t\t07/2019 – 08/2020\nOversaw company IT operations, design, sales, and marketing. Managed marketing, sales, product management, UI/UX, and IT service teams to drive business growth and operational efficiency.\nGrew company marketing distribution network by 300%.  \nLed marketing, design, and feature requirements of company flagship product HelloChat and achieved userbase growth of 589% within first 4 months since its debut.  \n\nSAP SuccessFactors | Vancouver, BC\nSenior Director of Engineering\t\t04/2014 – 08/2020\nDeveloped SAF (SuccessFactors Automation Framework) team vision, strategy, and roadmap to support automation for API, Mobile, and GUI. Led large-scale project management, including scheduling, planning, resource allocation, and budgeting.\nLed company digital transformation as Project Lead, adopting DevOps practices to revamp software development process towards CICD to achieve 10x more daily builds. \nSpearheaded Next Gen SAF integration development into CD Pipeline, achieving 4x faster in automation test execution with 75% less resource consumption.  \nPatented Results Analysis Engine (RAE) algorithm optimization with AI/ML from metadata service provider, reducing 51% duplicated service tickets in Jira.\n\nAdditional experience:\nDirector of Quality Assurance | SAP SuccessFactors\n\nEducation / Certifications\n\nUniversity of Saskatchewan | Saskatoon, Saskatchewan\nMaster of Science (M.S.) in Mechanical Engineering\n\nZhejiang University | Hangzhou, Zhejiang, China\nBachelor of Engineering in Thermo Science & Technology\n\nCertified Scrum Master | Scrum Alliance	2025-04-01 19:35:07.963576	\N	f	f	2025-04-01 19:35:07.965082	\N	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: job_user
--

COPY public.users (id, email, hashed_password, full_name, created_at, updated_at) FROM stdin;
1	eugene.jiang@gmail.com			2025-04-01 19:32:47.605949	2025-04-01 19:32:47.605954
\.


--
-- Name: applications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: job_user
--

SELECT pg_catalog.setval('public.applications_id_seq', 1, false);


--
-- Name: job_matches_id_seq; Type: SEQUENCE SET; Schema: public; Owner: job_user
--

SELECT pg_catalog.setval('public.job_matches_id_seq', 16, true);


--
-- Name: jobs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: job_user
--

SELECT pg_catalog.setval('public.jobs_id_seq', 1, false);


--
-- Name: resumes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: job_user
--

SELECT pg_catalog.setval('public.resumes_id_seq', 2, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: job_user
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY (id);


--
-- Name: job_matches job_matches_pkey; Type: CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.job_matches
    ADD CONSTRAINT job_matches_pkey PRIMARY KEY (id);


--
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);


--
-- Name: resumes resumes_pkey; Type: CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.resumes
    ADD CONSTRAINT resumes_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_applications_id; Type: INDEX; Schema: public; Owner: job_user
--

CREATE INDEX ix_applications_id ON public.applications USING btree (id);


--
-- Name: ix_job_matches_id; Type: INDEX; Schema: public; Owner: job_user
--

CREATE INDEX ix_job_matches_id ON public.job_matches USING btree (id);


--
-- Name: ix_jobs_id; Type: INDEX; Schema: public; Owner: job_user
--

CREATE INDEX ix_jobs_id ON public.jobs USING btree (id);


--
-- Name: ix_resumes_id; Type: INDEX; Schema: public; Owner: job_user
--

CREATE INDEX ix_resumes_id ON public.resumes USING btree (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: job_user
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: job_user
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: applications applications_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: applications applications_resume_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_resume_id_fkey FOREIGN KEY (resume_id) REFERENCES public.resumes(id);


--
-- Name: applications applications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: job_matches job_matches_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.job_matches
    ADD CONSTRAINT job_matches_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_matches job_matches_resume_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.job_matches
    ADD CONSTRAINT job_matches_resume_id_fkey FOREIGN KEY (resume_id) REFERENCES public.resumes(id);


--
-- Name: job_matches job_matches_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.job_matches
    ADD CONSTRAINT job_matches_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: resumes resumes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.resumes
    ADD CONSTRAINT resumes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

