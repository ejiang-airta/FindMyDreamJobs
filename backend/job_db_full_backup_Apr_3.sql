--
-- PostgreSQL database dump
--

-- Dumped from database version 14.17 (Homebrew)
-- Dumped by pg_dump version 14.17 (Homebrew)

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


ALTER TABLE public.applications_id_seq OWNER TO job_user;

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
    match_score_final double precision
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


ALTER TABLE public.job_matches_id_seq OWNER TO job_user;

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
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    user_id integer NOT NULL,
    job_link character varying,
    required_experience character varying,
    extracted_skills jsonb
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


ALTER TABLE public.jobs_id_seq OWNER TO job_user;

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


ALTER TABLE public.resumes_id_seq OWNER TO job_user;

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


ALTER TABLE public.users_id_seq OWNER TO job_user;

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
a0148ad7c7ca
\.


--
-- Data for Name: applications; Type: TABLE DATA; Schema: public; Owner: job_user
--

COPY public.applications (id, user_id, job_id, resume_id, application_url, application_status, applied_date, updated_at) FROM stdin;
2	1	5	4	https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4186426938	rejected	2025-04-02 12:38:21.209651	2025-04-02 12:39:03.587377
1	1	5	4	https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4186426938	rejected	2025-04-02 12:37:25.457907	2025-04-02 12:39:30.459113
\.


--
-- Data for Name: job_matches; Type: TABLE DATA; Schema: public; Owner: job_user
--

COPY public.job_matches (id, user_id, job_id, resume_id, created_at, matched_skills, missing_skills, calculated_at, ats_score_initial, ats_score_final, match_score_initial, match_score_final) FROM stdin;
18	1	5	3	2025-04-02 12:23:25.614366	aws	python,fastapi	2025-04-02 12:23:25.614389	\N	\N	33.33	\N
17	1	2	3	2025-04-02 12:18:43.096498		python,fastapi	2025-04-02 12:34:37.954347	\N	96	0	0
\.


--
-- Data for Name: jobs; Type: TABLE DATA; Schema: public; Owner: job_user
--

COPY public.jobs (id, job_title, company_name, location, job_description, created_at, updated_at, user_id, job_link, required_experience, extracted_skills) FROM stdin;
2	backend engineer	Unknown Company	\N	Looking for a backend engineer with 3+ years of experience in Python and FastAPI.	2025-04-02 12:10:16.522695	2025-04-02 12:10:16.5227	1	N/A	3+ years	\N
3	Unknown Title	is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.	\N	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.	2025-04-02 12:10:38.759706	2025-04-02 12:10:38.75971	1	https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4186426938	10+ years	\N
4	Unknown Title	Unknown Company	\N	Clio \nLooking for a Director of Engineering with 10+ years of experience in Python, AWS and FastAPI.	2025-04-02 12:21:23.138548	2025-04-02 12:21:23.138553	1	N/A	10+ years	\N
5	Unknown Title	Unknown Company	\N	Amazon is looking for a Director of Engineering with 12+ years of experience in DevOps, CI/CD, Python, AWS and FastAPI.	2025-04-02 12:22:42.930636	2025-04-02 12:22:42.930639	1	N/A	12+ years	\N
6	a Director	Amazon	\N	Amazon is looking for a Director of Engineering with 12+ years of experience in DevOps, CI/CD, Python, AWS and FastAPI.	2025-04-02 14:10:57.127879	2025-04-02 14:10:57.127883	1	N/A	12+ years	\N
7	the VP	the VP of Engineering	\N	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.\nIn this case, Clio is company name, VP of Engineering is the title, and the fuction return "Unknown Title" and interestingly it return company name as "is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice."	2025-04-02 14:12:47.876497	2025-04-02 14:12:47.876501	1	N/A	10+ years	\N
8	VP	Fintech	\N	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.\nIn this case, Clio is company name, VP of Engineering is the title, and the fuction return "Unknown Title" and interestingly it return company name as "is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice."	2025-04-02 14:25:57.42643	2025-04-02 14:25:57.426434	1	N/A	10+ years	\N
9	Director	Amazon	\N	Amazon is looking for a Director of Engineering with 12+ years of experience in DevOps, CI/CD, Python, AWS and FastAPI.	2025-04-02 14:26:39.218506	2025-04-02 14:26:39.218512	1	N/A	12+ years	\N
10	VP	Fintech	\N	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.	2025-04-02 14:28:15.479114	2025-04-02 14:28:15.479134	1	N/A	10+ years	\N
11	backend engineer	Checkpay Technology	\N	A fintech startup, Checkpay Technology, is ooking for a backend engineer with 3+ years of experience in Python and FastAPI.	2025-04-02 14:29:15.667001	2025-04-02 14:29:15.667005	1	N/A	3+ years	\N
12	Backend Engineer	Checkpay Technology	\N	A fintech startup, Checkpay Technology, is ooking for a backend engineer with 3+ years of experience in Python and FastAPI.	2025-04-02 15:04:27.838337	2025-04-02 15:04:27.83834	1	N/A	3+ years	\N
13	Director of Engineering	Amazon	\N	Amazon is looking for a Director of Engineering with 12+ years of experience in DevOps, CI/CD, Python, AWS	2025-04-02 15:05:01.559921	2025-04-02 15:05:01.559925	1	N/A	12+ years	\N
14	VP of Engineering	Fintech	\N	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.	2025-04-02 15:05:26.45504	2025-04-02 15:05:26.455044	1	N/A	10+ years	\N
15	VP of Engineering	Clio	\N	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.	2025-04-02 15:09:40.245252	2025-04-02 15:09:40.245257	1	N/A	10+ years	\N
16	VP of Engineering	Clio	Unspecified	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.	2025-04-02 15:25:22.072878	2025-04-02 15:25:22.072881	1	N/A	10+ years	\N
17	Director of Engineering	Amazon	Unspecified	Amazon is looking for a Director of Engineering in Vancouver Canada with 12+ years of experience in DevOps, CI/CD, Python, AWS and FastAPI.	2025-04-02 15:26:42.094806	2025-04-02 15:26:42.09481	1	N/A	12+ years	\N
18	Director of Engineering	Amazon	Vancouver Canada	Amazon is looking for a Director of Engineering in Vancouver Canada with 12+ years of experience in DevOps, CI/CD, Python, AWS and FastAPI.	2025-04-02 15:36:32.587296	2025-04-02 15:36:32.587301	1	N/A	12+ years	\N
19	VP of Engineering	Clio	Unspecified	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.	2025-04-02 15:36:50.796599	2025-04-02 15:36:50.796604	1	N/A	10+ years	\N
20	Unknown Title	N/A	Unspecified	N/A	2025-04-02 15:37:28.940241	2025-04-02 15:37:28.940249	1	https://www.linkedin.com/jobs/view/4186426938	Unspecified	\N
21	VP of Engineering	Clio	Unspecified	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.	2025-04-02 15:38:51.123361	2025-04-02 15:38:51.123364	1	N/A	10+ years	\N
22	VP of Engineering	Clio	Vancouver	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering located in Vancouver, BC, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.\n\n	2025-04-02 15:42:37.173554	2025-04-02 15:42:37.173558	1	N/A	10+ years	\N
23	Unknown Title	N/A	Unspecified	N/A	2025-04-02 16:14:44.11496	2025-04-02 16:14:44.114965	1	https://www.linkedin.com/jobs/view/4186426938/	Unspecified	\N
24	VP of Engineering	Clio	Unspecified	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.	2025-04-02 16:21:00.669908	2025-04-02 16:21:00.669913	1	N/A	10+ years	\N
25	VP of Engineering	Clio	Vancouver	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering located in Vancouver, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.	2025-04-02 16:21:29.871788	2025-04-02 16:21:29.871792	1	N/A	10+ years	\N
26	VP of Engineering	Clio	Unspecified	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.	2025-04-02 17:09:33.205588	2025-04-02 17:09:33.205592	1	N/A	10+ years	\N
27	Unknown Title	N/A	Unspecified	N/A	2025-04-02 17:28:45.21903	2025-04-02 17:28:45.219034	1	https://www.jobleads.com/job/e4bfb128232ee8ea9c7ee08ab3dffdf91	Unspecified	\N
28	Unknown Title	Experts	AI	\n        We’re unlocking community knowledge in a new way. Experts add insights directly into each article, started with the help of AI.\n      	2025-04-02 19:27:49.471209	2025-04-02 19:27:49.471213	1	https://www.linkedin.com/jobs/view/4186426938/	Unspecified	\N
29	Unknown Title	Google	Coquitlam	jobs - Google Search  Google×Please click here if you are not redirected within a few seconds.    AllImagesNewsVideos Maps Shopping Books Search tools    Any timeAny timePast hourPast 24 hoursPast weekPast monthPast yearAll resultsAll resultsVerbatimjobs in Coquitlam, BC - Indeedca.indeed.com › l-coquitlam,-bc-jobsSearch 15922 jobs now available in Coquitlam, BC on Indeed.com, the world's largest job site.Career Opportunities | Coquitlam, BCwww.coquitlam.ca › Career-OpportunitiesWe offer exciting municipal careers in human resources, planning and development, parks and recreation, engineering, corporate and strategic initiatives as ...Jobs in Coquitlam | Hiring Now - BCjobs.cawww.bcjobs.ca › coquitlam-jobsSearching for jobs in Coquitlam? BCjobs.ca provides a comprehensive listing of jobs available in Coquitlam as well as career advices & interview tips.Jobs & Careers | City of Surreywww.surrey.ca › about-surrey › jobs-careersView our job opportunities. We are looking for talented professionals and innovators who are ready to help us build a world-class city.Find Jobs | WorkBCwww.workbc.ca › search-and-prepare-job › find-jobsSearch for and apply to jobs in British Columbia using the WorkBC Job Board.Account · Industry Job Boards · Job Search TipsPeople also askWhat jobs can I get at 14 in BC?Which jobs in Canada are in demand?How many employees does the city of Coquitlam have?Part Time jobs in Coquitlam, Bc - Indeedca.indeed.com › q-part-time-l-coquitlam,-bc-jobsSearch 4903 Part Time jobs now available in Coquitlam, BC on Indeed.com, the world's largest job site.Work for the City of Vancouver — Do your best work herevancouver.ca › your-government › apply-for-a-job-redirectCreate a candidate profile to apply for a job at the City of Vancouver. If you're a City, VPL, or VFRS employee, review and apply for an internal job posting.Review all job openings · View jobs for current employees · All job openingsCareer Search Results | CivicJobs.cacivicjobs.ca › jobsFound 10 Jobs ; Solid Waste Program Specialist · Coquitlam, BC 2 days ago ; Police File Reviewer · Coquitlam, BC 6 days ago ; Registration Clerk/ Receptionist.93 Jobs in Coquitlam, British Columbia | Randstad Canadawww.randstad.ca › jobs › british-columbia › coquitlamBrowse 93 jobs in Coquitlam, British Columbia. Choose from temporary and permanent jobs that'll help you reach your career goals.WorkBC Centre - Coquitlamwww.workbc.ca › workbc-centres › workbc-centre-coquitlam-0Search the job board and explore resources to help you in your job search. ... Recent Jobs. Explore recent job postings. hairstylist. Choigaeul Hair Salon.People also search forCoquitlamBurnabyPort CoquitlamPort Moodyjobs near vancouver, bcCity of Coquitlam jobsJobs CoquitlamPort Moody jobsCity of Port Moody jobsPort Coquitlam jobsIndeed jobs CoquitlamSD43 jobs  Next >  Coquitlam, British ColumbiaFrom your IP address - Learn moreSign inSettingsPrivacyTermsDark theme: Off 	2025-04-02 19:39:15.774134	2025-04-02 19:39:15.774138	1	https://www.google.com/search?q=jobs&gl=canada&hl=en&udm=8#vhid=vt%3D20/docid%3Dh8DwBMPCeQ-o-wLPAAAAAA%3D%3D&vssid=jobs-detail-viewer"	Unspecified	\N
30	Unknown Title	If	Indonesia	If running a startup is like playing a video game, then “game over” happens when the company runs out of cash. Founders often focus on battling the big, visible monsters like the competition beast, the market-size dragon, or the marketing ghoul.But too often, they miss the silent killer: financial mismanagement. According to recent studies, 16% of startups fail due to cash flow problems and other financial management issues.So, how can a founder bring order to the chaos of spending and scaling? One way, I argue, is by leveraging the financial services that fintech platforms offer.Where traditional banks fall shortFor some startup founders, traditional banks can be rigid and don’t always fulfill their needs. Critics cite lengthy onboarding processes, clunky user interfaces, and manual workflows as downsides.I believe for startups, this is more than just frustrating – it’s a growth killer. Instead of focusing on scaling their business, founders are stuck dealing with slow processes and outdated systems.See also: Indonesia’s banks are taking over BNPL. Can fintech firms survive?Fintech platforms like Aspire, Airwallex, and Brex, which provide financial tools for startups, could be one solution	2025-04-02 19:40:11.131372	2025-04-02 19:40:11.131376	1	https://simplify.jobs/p/6870f1fe-2cc8-4a78-b7fd-eaa5142f14ad/Engineering-Manager?utm_source=job_post&utm_medium=copy_link&utm_campaign=organic_share	Unspecified	\N
31	Unknown Title	If	Indonesia	If running a startup is like playing a video game, then “game over” happens when the company runs out of cash. Founders often focus on battling the big, visible monsters like the competition beast, the market-size dragon, or the marketing ghoul.But too often, they miss the silent killer: financial mismanagement. According to recent studies, 16% of startups fail due to cash flow problems and other financial management issues.So, how can a founder bring order to the chaos of spending and scaling? One way, I argue, is by leveraging the financial services that fintech platforms offer.Where traditional banks fall shortFor some startup founders, traditional banks can be rigid and don’t always fulfill their needs. Critics cite lengthy onboarding processes, clunky user interfaces, and manual workflows as downsides.I believe for startups, this is more than just frustrating – it’s a growth killer. Instead of focusing on scaling their business, founders are stuck dealing with slow processes and outdated systems.See also: Indonesia’s banks are taking over BNPL. Can fintech firms survive?Fintech platforms like Aspire, Airwallex, and Brex, which provide financial tools for startups, could be one solution	2025-04-02 19:40:13.693348	2025-04-02 19:40:13.693353	1	https://simplify.jobs/p/6870f1fe-2cc8-4a78-b7fd-eaa5142f14ad/Engineering-Manager?utm_source=job_post&utm_medium=copy_link&utm_campaign=organic_share	Unspecified	\N
32	Unknown Title	Google	Unspecified	Google SearchPlease click here if you are not redirected within a few seconds.If you're having trouble accessing Google Search, pleaseclick here, or sendfeedback.	2025-04-02 19:44:40.347887	2025-04-02 19:44:40.347891	1	https://www.google.com/search?q=jobs&gl=canada&hl=en&udm=8&jbr=sep:0#vhid=vt%3D20/docid%3DTxSEIOb0AbuZQQ5eAAAAAA%3D%3D&vssid=jobs-detail-viewer	Unspecified	\N
33	Director of Engineering	Amazon	Vancouver Canada	Amazon is looking for a Director of Engineering in Vancouver Canada with 12+ years of experience in DevOps, CI/CD, Python, AWS and FastAPI.	2025-04-02 20:09:11.845232	2025-04-02 20:09:11.845238	1	N/A	12+ years	\N
34	Director of Engineering	Amazon	Vancouver Canada	Amazon is looking for a Director of Engineering in Vancouver Canada with 12+ years of experience in DevOps, CI/CD, Python, AWS and FastAPI.\nover 8+ years of managing a DevOps team, and be able to innovate with new DevOps model to migrate to AWS cloud.\nOver 5+ years of Python hands-on development experience using REST APIs	2025-04-03 12:00:50.819867	2025-04-03 12:00:50.819873	1	N/A	12+ years	[{"skill": "Python", "frequency": 1}, {"skill": "FastAPI", "frequency": 1}, {"skill": "AWS", "frequency": 1}, {"skill": "CI/CD", "frequency": 1}, {"skill": "DevOps", "frequency": 1}]
\.


--
-- Data for Name: resumes; Type: TABLE DATA; Schema: public; Owner: job_user
--

COPY public.resumes (id, user_id, file_path, parsed_text, created_at, optimized_text, is_ai_generated, is_user_approved, updated_at, ats_score_initial, ats_score_final) FROM stdin;
4	1	uploads/resumes/55e27226-c3da-4107-a323-59c06e9aab81_Resume-Eugene-Jiang-updated-Feb-5-2025.docx	Eugene Jiang \neugene.jiang@gmail.com 604-368-6508 linkedin.com/in/eugenejiang Vancouver,BC,V3E 0M3 \nSummary \nVisionary engineering leader with a proven track record of scaling high-performing teams, delivering customer-facing applications, and driving technical excellence. \nExpertise in Agile development, DevOps, cloud-based applications, and data-driven decision-making across SaaS, e-Commerce, Fintech, and Analytics. \nPassionate about fostering innovation, optimizing engineering practices, building, coaching and growing strong teams with an open culture, and aligning product engineering strategy with business goals. \nHolder of two patents in AI-driven automation and analytics.\n\nExperience \nDirector of Software Development Engineer in Test (SDET)\nWorkday | Vancouver, Canada | 07/2022 - present \nLed multiple high-performing SDET and software engineering teams (40+ members), focusing on customer-facing analytics applications and test infrastructure.\nDefined and standardized product release and feature sign-off processes, and collaborated with PM/Dev/Customer Support teams to tackle the production issues resulted in ~20% YoY customer-reported issues reduction.\nLed the engineering transformation for developer productivity, implementing Next Gen Pre-Commit solutions that improved efficiency by 50% and prevented 6% defective code from merging.\nScaled team from 23 to 40+ while mentoring talent - grown multiple engineers to managerial and senior leadership roles.\nEstablished a customer-focused, continuous improvement culture, aligning engineering initiatives with business and product strategy.\nSpearheaded the AI-driven initiatives such as AIChatbot, Automatic Failure Analysis.\nHead Of Quality\nPayByPhone | Vancouver, Canada | 04/2021 - 02/2022 \n- Led PayByPhone product quality standard and processes and drive testing requirements including performance & security test practices, automation framework, and development process with Static Code Analysis, code coverage, and CICD pipeline using PyTest, SonarQube, GitLab and AWS. \n- Owner of Production site reliability and drive uptime improvement towards 99.9% availability, worked cross-team with Platform Infrastructure/DevOps, Cloud Platform, Architect, Security, PMO, DBA, Development and QA to setup a taskforce, strategy, roadmap, and execution plan which resulted 86% environment issue reduction after the first 5 months. \n- Implemented the new and enhanced production deployment process with Jira/Slack integration which improved developer productivity by 15% time saving. \nChief Technology Officer \nCheckPay Technologies Ltd (Fintech Startup)  | Vancouver, Canada |  08/2020 - 04/ 2021 \n- Owned  HelloChat, app requirements, design, development, quality, build and release. \n- Managed Development, Product Management, UIUX, IT Service and DevOps teams. \n- Led successful launch of HelloChat v2 on iOS and Android using React Native with user adoption doubled within first two months after v2 roll-out. \n- Directed the implementation of the CD pipeline with CircleCI in real-time release of API services. \n- Led the mobile architectural changes on client-side caching using Realm DB with 10x performance gain. \n\nChief Operating Officer \nCheckPay Technologies Ltd  (Fintech Startup)  | Vancouver, Canada |  07/2019 - 08/2020 \n- Responsible for the company IT operation, design, sales, and marketing. \n- Managed Marketing, Sales, Product Management, UIUX, and IT Service teams. \n- Grown company marketing distribution network by 300%. \n- Led the marketing, design, and feature requirements of the company flagship product HelloChat and achieved user base growth of 589% within the first 4 months since its debut. \n \t\nSenior Director of Engineering \nSAP SuccessFactors  | Vancouver, Canada | 04/2014 - 04/2019 \n- Built SAF (SuccessFactors Automation Framework) team long term vision, strategy, and roadmap to satisfy automation needs for API, Mobile and GUI. \n- Extensive large-scale Project Management in schedule management, project planning, resource management and budget; Led the company digital transformation as Project Lead adopting DevOps practices to revamped software development process towards CICD achieved 10x more daily builds. - Spearheaded development of Next Gen SAF integration into CD Pipeline and achieved 4x faster in automation test execution with 75% less resource consumption. \n- Product Owner of patented RAE (Results Analysis Engine) algorithm optimization with AI/ML from metadata service provider and reduced 51% duplicated service ticket in Jira. \n\nDirector Of Quality Assurance \nSAP SuccessFactors  | Shanghai, China | 01/2011 - 03/2014 \n- Built and managed SAP SuccessFactors (SF) Global Automation (SAF) team for testing SF suite of products processing 670M daily transactions at peak to serve 120M million users in 200 countries. \n- Managed, recruited, and grown SAF team into a high performing automation testing team of 65 people in 5 geographic locations with less than 2% attrition 3 years in a row (2012-2015). - Coach, mentor and grown 2 developers to Architect and 3 IC to senior dev manager. - Built team culture and core values, committed, and delivered project roadmap items on time with high quality exceeding expectations. \n- Chaired the architectural design and implementation of end-to-end automation solution (SAF v1) with Selenium achieved 96% adoption, 150% YOY growth and improved code coverage by 31%. \n- Built relationship and collaborated with all stakeholders to standardize the development process with SAF achieved 23% YOY reduction on production regression issue. \n- Got 2 patents granted with RAE and ACE (Automatic componentization engine). \nSenior Quality Assurance Manager \neBay | Shanghai, China | 03/2009 - 12/2010\n- Owned eBay quality engineering standard, process, framework, and tools development. \n- Managed 6 teams with 3 managers, 33 developers, testers, automation engineers, release managers, product manager, and project managers. \n- Invented and coached development of eCAF (eBay Componentized Automation Framework) serving all eBay automation needs and reduced 90% initial automation effort. \n- Led development effort of eBay next gen tools such as: Data Creation Tool (DCT), Reporting Portal, Monitoring Hub, project management tool with DCT availability at six 9s. \n- Standardized development and quality process with software development life cycle (SDLC) that includes discovery, code review, unit testing, Static Code Analysis (SCA). \nDevelopment Manager \nSAP BusinessObjects | Shanghai, China | 07/2006 - 03/2009 \n- Led Developer Mission team to bundle Crystal Reports SDK with Microsoft Visual Studio .NET and successfully achieved stricter quality requirements from Microsoft within budget. \n- Drove Shanghai Development Center (SDC) to define software development processes that achieved operational excellence through innovative early bug detection (EBD) system. \n- Led design and implementation of UI Automation tool, Smart UI (SUI) and achieved 3 times faster test execution and 10 times more platform coverage which cut down the full regression time from one month in handful platform to 10 days with 126 environments. \n- Chaired productivity and quality improvement initiatives as SDC Site Lead and successfully improved quality and efficiency with Code Review, SCA, Continuous Integration (CI), Unit Test, Code Coverage and achieved 30% regression issue reduction. \nQuality Assurance Manager \nSAP BusinessObjects | Vancouver, Canada | 06/2003 - 12/2006 \n- Established QA processes, strategies, and built teams from scratch to 30+ people within 6 months and successfully coached and mentored the teams to take more ownership. \n- Coordinated cross site testing efforts with other SAP teams located in different geographic locations including Canada, US, France, UK, and India. \nFeature Test Developer \nSAP BusinessObjects | Vancouver, Canada | 06/2001 - 06/2003 \n- Owned entire Crystal Reports SDK testing including test planning, test prioritization, test design, test framework and automation development. \n- Architected, designed, and coded Crystal Reports Designer Component (RDC) automation framework with VB, C#, ASP.NET, ODBC, SQL Server, Oracle, Access, OLEDB, ADO, Perl script. \n- Developed a Web-based RDC Info System using ASP.Net, VB script, Java script and HTML. \n- Developed Crystal Reports Formula Language Test Application using VB, SQL server, and Perl script, and CR.NET. \nEducation\nUniversity of Saskatchewan \nMaster of Science, Mechanical Engineering \nZhejiang University \nBachelor of Engineering, Thermo Science & Technology\n\n\nLicenses & Certifications \nCertified Scrum Master - Scrum Alliance	2025-04-02 12:11:26.155898	\N	f	f	2025-04-02 12:11:26.157633	\N	\N
3	1	uploads/resumes/eeb74e5b-755c-44b7-80cd-251e9da0d1c6_Jiang-Eugene-Critique-Updated-Mar-31.docx	Eugene Jiang\nVancouver, BC V3E 0M3 | 604-368-6508 | eugene.jiang@gmail.com | www.linkedin.com/in/eugenejiang\n\nDirector of Software Quality Assurance\n\nVisionary engineering leader scaling high-performing teams, delivering customer-facing applications, and driving technical excellence. Specialize in Agile development, DevOps, and cloud-based applications across SaaS, e-Commerce, Fintech, and Analytics, leveraging data-driven decision-making to optimize engineering practices. Define and execute engineering roadmaps aligned with business objectives and product vision, fostering innovation while mentoring engineers into senior leadership roles. Committed to technical advancement, earning two patents in AI-driven automation and analytics. Collaborate with Product, Design, Customer Success, and Business teams to drive seamless, customer-centric development. Cultivate open culture of growth, aligned product engineering strategy with business goals, and enhanced performance, scalability, and user experience for high-availability SaaS applications.\n\nEngineering Roadmaps | Talent Development | Agile | DevOps | CI/CD | AI/ML\n\nProfessional Experience \n\nWorkday | Vancouver, BC\nDirector of Software Engineer in Test (SDET)\t\t07/2022 – present\nLead high-performing SDET and software engineering teams of 40+ members, focusing on customer-facing testing analytics applications and test infrastructure.\nDefined and standardized product release and feature sign-off processes, reducing customer-reported issues by ~20% YoY through collaboration with quality, product, development, and customer support teams.\nLed engineering transformation for developer productivity, implementing next gen pre-commit solutions (NGPCQ) that improved efficiency by 50% and prevented 6% defective code from merging.\nScaled team from 23 to 40+, mentoring talent and developing multiple engineers into managerial and senior leadership roles.\nEstablished customer-focused, continuous improvement culture by aligning engineering initiatives with business and product strategy by engaging various stakeholders to do production issue analysis and identify area of improvements.\nSpearheaded AI-driven initiatives, including AI Chatbot and Automatic Failure Analysis. Led architecture design and review, supervised the implementation which integrated with NGPCQ achieved efficiency gain.\n\nPayBePhone | Vancouver, BC\nHead of Quality Assurance (QA)\t\t04/2021 – 02/2022\nLed product quality standards and processes, driving testing requirements for performance and security test practices, automation framework, and development process. Implemented Static Code Analysis, code coverage, and CI/CD pipeline using PyTest, SonarQube, GitLab, and AWS to enhance code quality and streamline development workflows.\nDrove production site reliability, improving uptime toward 99.9% availability through cross-team collaboration with Cloud Platform, Architect, Infrastructure, DevOps, Security, PMO, DBA, Development to setup a taskforce, strategy, roadmap, and execution plan which resulted 86% environment issue reduction after the first 5 months. \nImplemented enhanced production deployment process with Jira/Slack integration, increasing developer productivity by 15% time savings.\n\nCheckPay Technologies | Vancouver, BC\nChief Technology Officer (CTO)\t\t08/2020 – 04/2021\nOwned HelloChat app requirements, design, development, quality, build, and release. Managed Development, Product Management, UI/UX, IT Service, and DevOps teams to drive seamless execution and delivery.\nLed successful HelloChat v2 launch on iOS and Android using React Native, doubling user adoption doubled within first 2 months after v2 roll-out.  \n\nCheckPay Technologies | Chief Technology Officer (CTO)\t\tcontinued\nDirected CD pipeline implementation with CircleCI in real-time API services release.\nLed mobile architectural changes on client-side caching using Realm DB with 10x performance gain.  \n\nChief Operating Officer (COO)\t\t07/2019 – 08/2020\nOversaw company IT operations, design, sales, and marketing. Managed marketing, sales, product management, UI/UX, and IT service teams to drive business growth and operational efficiency.\nGrew company marketing distribution network by 300%.  \nLed marketing, design, and feature requirements of company flagship product HelloChat and achieved userbase growth of 589% within first 4 months since its debut.  \n\nSAP SuccessFactors | Vancouver, BC\nSenior Director of Engineering\t\t04/2014 – 08/2020\nDeveloped SAF (SuccessFactors Automation Framework) team vision, strategy, and roadmap to support automation for API, Mobile, and GUI. Led large-scale project management, including scheduling, planning, resource allocation, and budgeting.\nLed company digital transformation as Project Lead, adopting DevOps practices to revamp software development process towards CICD to achieve 10x more daily builds. \nSpearheaded Next Gen SAF integration development into CD Pipeline, achieving 4x faster in automation test execution with 75% less resource consumption.  \nPatented Results Analysis Engine (RAE) algorithm optimization with AI/ML from metadata service provider, reducing 51% duplicated service tickets in Jira.\n\nAdditional experience:\nDirector of Quality Assurance | SAP SuccessFactors\n\nEducation / Certifications\n\nUniversity of Saskatchewan | Saskatoon, Saskatchewan\nMaster of Science (M.S.) in Mechanical Engineering\n\nZhejiang University | Hangzhou, Zhejiang, China\nBachelor of Engineering in Thermo Science & Technology\n\nCertified Scrum Master | Scrum Alliance	2025-04-02 10:04:45.913585	Eugene Jiang\nVancouver, BC V3E 0M3 | 604-368-6508 | eugene.jiang@gmail.com | www.linkedin.com/in/eugenejiang\n\nDirector of Software Quality Assurance\n\nVisionary engineering leader scaling high-performing teams, delivering customer-facing applications, and driving technical excellence. Specialize in Agile development, DevOps, and cloud-based applications across SaaS, e-Commerce, Fintech, and Analytics, leveraging data-driven decision-making to optimize engineering practices. Define and execute engineering roadmaps aligned with business objectives and product vision, fostering innovation while mentoring engineers into senior leadership roles. Committed to technical advancement, earning two patents in AI-driven automation and analytics. Collaborate with Product, Design, Customer Success, and Business teams to drive seamless, customer-centric development. Cultivate open culture of growth, aligned product engineering strategy with business goals, and enhanced performance, scalability, and user experience for high-availability SaaS applications.\n\nEngineering Roadmaps | Talent Development | Agile | DevOps | CI/CD | AI/ML\n\nProfessional Experience \n\nWorkday | Vancouver, BC\nDirector of Software Engineer in Test (SDET)\t\t07/2022 – present\nLead high-performing SDET and software engineering teams of 40+ members, focusing on customer-facing testing analytics applications and test infrastructure.\nDefined and standardized product release and feature sign-off processes, reducing customer-reported issues by ~20% YoY through collaboration with quality, product, development, and customer support teams.\nLed engineering transformation for developer productivity, implementing next gen pre-commit solutions (NGPCQ) that improved efficiency by 50% and prevented 6% defective code from merging.\nScaled team from 23 to 40+, mentoring talent and developing multiple engineers into managerial and senior leadership roles.\nEstablished customer-focused, continuous improvement culture by aligning engineering initiatives with business and product strategy by engaging various stakeholders to do production issue analysis and identify area of improvements.\nSpearheaded AI-driven initiatives, including AI Chatbot and Automatic Failure Analysis. Led architecture design and review, supervised the implementation which integrated with NGPCQ achieved efficiency gain.\n\nPayBePhone | Vancouver, BC\nHead of Quality Assurance (QA)\t\t04/2021 – 02/2022\nLed product quality standards and processes, driving testing requirements for performance and security test practices, automation framework, and development process. Implemented Static Code Analysis, code coverage, and CI/CD pipeline using PyTest, SonarQube, GitLab, and AWS to enhance code quality and streamline development workflows.\nDrove production site reliability, improving uptime toward 99.9% availability through cross-team collaboration with Cloud Platform, Architect, Infrastructure, DevOps, Security, PMO, DBA, Development to setup a taskforce, strategy, roadmap, and execution plan which resulted 86% environment issue reduction after the first 5 months. \nImplemented enhanced production deployment process with Jira/Slack integration, increasing developer productivity by 15% time savings.\n\nCheckPay Technologies | Vancouver, BC\nChief Technology Officer (CTO)\t\t08/2020 – 04/2021\nOwned HelloChat app requirements, design, development, quality, build, and release. Managed Development, Product Management, UI/UX, IT Service, and DevOps teams to drive seamless execution and delivery.\nLed successful HelloChat v2 launch on iOS and Android using React Native, doubling user adoption doubled within first 2 months after v2 roll-out.  \n\nCheckPay Technologies | Chief Technology Officer (CTO)\t\tcontinued\nDirected CD pipeline implementation with CircleCI in real-time API services release.\nLed mobile architectural changes on client-side caching using Realm DB with 10x performance gain.  \n\nChief Operating Officer (COO)\t\t07/2019 – 08/2020\nOversaw company IT operations, design, sales, and marketing. Managed marketing, sales, product management, UI/UX, and IT service teams to drive business growth and operational efficiency.\nGrew company marketing distribution network by 300%.  \nLed marketing, design, and feature requirements of company flagship product HelloChat and achieved userbase growth of 589% within first 4 months since its debut.  \n\nSAP SuccessFactors | Vancouver, BC\nSenior Director of Engineering\t\t04/2014 – 08/2020\nDeveloped SAF (SuccessFactors Automation Framework) team vision, strategy, and roadmap to support automation for API, Mobile, and GUI. Led large-scale project management, including scheduling, planning, resource allocation, and budgeting.\nLed company digital transformation as Project Lead, adopting DevOps practices to revamp software development process towards CICD to achieve 10x more daily builds. \nSpearheaded Next Gen SAF integration development into CD Pipeline, achieving 4x faster in automation test execution with 75% less resource consumption.  \nPatented Results Analysis Engine (RAE) algorithm optimization with AI/ML from metadata service provider, reducing 51% duplicated service tickets in Jira.\n\nAdditional experience:\nDirector of Quality Assurance | SAP SuccessFactors\n\nEducation / Certifications\n\nUniversity of Saskatchewan | Saskatoon, Saskatchewan\nMaster of Science (M.S.) in Mechanical Engineering\n\nZhejiang University | Hangzhou, Zhejiang, China\nBachelor of Engineering in Thermo Science & Technology\n\nCertified Scrum Master | Scrum Alliance\n\n===========================\n🔍 AI-Optimized Resume Section\n===========================\n\nAs highlighted in the job description, the following skills are critical for\nsuccess in this role. The applicant has provided justification for emphasizing\nthese skills during resume optimization: AWS\n\n⚡ Highlighted Skills:\n- Python\n\n===========================	t	t	2025-04-02 12:34:49.7997	\N	96
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

SELECT pg_catalog.setval('public.applications_id_seq', 2, true);


--
-- Name: job_matches_id_seq; Type: SEQUENCE SET; Schema: public; Owner: job_user
--

SELECT pg_catalog.setval('public.job_matches_id_seq', 18, true);


--
-- Name: jobs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: job_user
--

SELECT pg_catalog.setval('public.jobs_id_seq', 34, true);


--
-- Name: resumes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: job_user
--

SELECT pg_catalog.setval('public.resumes_id_seq', 4, true);


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
-- Name: jobs jobs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: resumes resumes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.resumes
    ADD CONSTRAINT resumes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

