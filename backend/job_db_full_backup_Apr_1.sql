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
    extracted_skills text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    user_id integer NOT NULL,
    job_link character varying,
    required_experience character varying
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
b64a9fea6cb3
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

COPY public.jobs (id, job_title, company_name, location, job_description, extracted_skills, created_at, updated_at, user_id, job_link, required_experience) FROM stdin;
2	backend engineer	Unknown Company	\N	Looking for a backend engineer with 3+ years of experience in Python and FastAPI.	{Python,FastAPI}	2025-04-02 12:10:16.522695	2025-04-02 12:10:16.5227	1	N/A	3+ years
3	Unknown Title	is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.	\N	About the job\nClio is more than just a tech company–we are a global leader that is transforming the legal experience for all by bettering the lives of legal professionals while increasing access to justice.\n\nSummary:\n\nAs the VP of Engineering, you will play a critical role in shaping Clio's technical and strategic direction. Working closely with your peers in the leadership team, you will directly own and drive the Fintech and International domains, with opportunities to expand your influence into additional areas as the company scales. This role requires a dynamic leader with a proven track record in building high-performing engineering teams, delivering innovative technology solutions, and aligning engineering execution with business objectives. All Engineering roles at Clio require handson ability. While your day-to-day won’t be coding, you will need to be deeply technical.\n\nAs a key member of Clio’s senior leadership team, reporting directly to the CTO, the Vice President will be responsible for aligning engineering efforts with Clio's broader vision and goals while leading and scaling a diverse team of 100+ engineers to deliver great products that will shape the future of the legal industry.\n\nWhat You’ll Work On:\n\nTechnical & Product Leadership\n\nDefine and execute the technical strategy for Payments and International expansion, ensuring scalability, security, and compliance in global markets.\nCollaborate with Product Management and Design to develop and execute a robust product roadmap that aligns with customer needs and business objectives.\nStay ahead of industry trends in payments technology and international infrastructure, positioning the company as a leader in these domains.\n\nTeam & Organizational Development\n\nScale, mentor, and lead a high-performing engineering team, ensuring a culture of innovation, accountability, and excellence.\nFoster a strong engineering leadership team that can drive execution while enabling career growth and leadership development across the organization.\nPromote best practices in engineering, architecture, and operational excellence to enhance system reliability and development velocity.\n\nStrategic Execution & Cross-Functional Collaboration\n\nTranslate company vision into an actionable engineering strategy, working closely with executive leadership.\nPartner with stakeholders across finance, legal, compliance, and international operations to navigate the complexities of global payments and expansion.\nChampion the engineering function within the broader organization, ensuring clear communication, alignment, and cross-functional success.\n\nScaling & Innovation\n\nDrive architectural improvements and technological innovations that support the company’s long-term growth, particularly in global payment infrastructure and international market expansion.\nAlign engineering efforts with customer needs, market demands, and regulatory requirements through automation and scalable solutions.\nLead initiatives around operational efficiency, automation, and system scalability to support international growth and regulatory requirements.\n\nWhat you May Have: \n\n10+ years of engineering leadership experience in payments, fintech, or international technology expansion, with a background as a CTO, VP, or a similar role.\nProven success in scaling engineering teams and delivering complex, customer-facing platforms at a global level.\nDeep understanding of payment processing, compliance frameworks, global infrastructure, and financial technology.\nStrong strategic mindset with the ability to balance long-term vision with short-term execution.\nExperience leading multiple managers and directors, with direct oversight of senior leaders and coordinating action across teams.\nExceptional collaboration skills, with the ability to influence and align multiple stakeholders across the organization.\nPassion for building high-impact teams, mentoring leaders, and driving engineering excellence.\n\nBonus Points: \n\nExperience in B2B SaaS and hypergrowth environments, scaling engineering organizations to support rapid expansion\nUnderstanding of the engineering challenges, operational rigor, and PCI compliance requirements necessary for IPO readiness and navigating the public company transition.	{}	2025-04-02 12:10:38.759706	2025-04-02 12:10:38.75971	1	https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4186426938	10+ years
4	Unknown Title	Unknown Company	\N	Clio \nLooking for a Director of Engineering with 10+ years of experience in Python, AWS and FastAPI.	{Python,FastAPI,AWS}	2025-04-02 12:21:23.138548	2025-04-02 12:21:23.138553	1	N/A	10+ years
5	Unknown Title	Unknown Company	\N	Amazon is looking for a Director of Engineering with 12+ years of experience in DevOps, CI/CD, Python, AWS and FastAPI.	{Python,FastAPI,AWS}	2025-04-02 12:22:42.930636	2025-04-02 12:22:42.930639	1	N/A	12+ years
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

SELECT pg_catalog.setval('public.jobs_id_seq', 5, true);


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

