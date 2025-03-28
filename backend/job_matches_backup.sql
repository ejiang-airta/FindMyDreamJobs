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
    match_score_initial double precision DEFAULT 40 NOT NULL,
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
-- Name: job_matches id; Type: DEFAULT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.job_matches ALTER COLUMN id SET DEFAULT nextval('public.job_matches_id_seq'::regclass);


--
-- Data for Name: job_matches; Type: TABLE DATA; Schema: public; Owner: job_user
--

COPY public.job_matches (id, user_id, job_id, resume_id, created_at, matched_skills, missing_skills, calculated_at, ats_score_initial, ats_score_final, match_score_initial, match_score_final) FROM stdin;
2	1	1	4	2025-03-24 17:46:22.540848	\N	\N	\N	\N	\N	40	\N
7	1	1	7	2025-03-25 11:31:13.244147	\N	\N	\N	\N	\N	40	\N
9	1	1	7	2025-03-25 12:31:05.9694	\N	\N	\N	\N	\N	40	\N
11	1	1	10	2025-03-26 11:51:59.672436		fastapi,python,sql	2025-03-26 17:13:21.378113	85	\N	40	\N
6	1	1	6	2025-03-25 11:31:08.890594	\N	\N	2025-03-26 17:17:32.657834	75	\N	40	\N
10	1	1	6	2025-03-25 12:31:11.476208	\N	\N	2025-03-26 17:17:33.69651	75	\N	40	\N
4	1	1	7	2025-03-25 11:30:54.47121	\N	\N	2025-03-26 19:12:43.916303	80	\N	40	\N
8	1	1	8	2025-03-25 11:31:16.58674	\N	\N	2025-03-26 19:12:47.133351	40	\N	40	\N
1	1	1	4	2025-03-24 17:35:46.38618	\N	\N	2025-03-26 19:13:41.381646	40	\N	40	\N
3	1	1	5	2025-03-24 18:05:49.27198	\N	\N	2025-03-26 19:13:44.882803	70	\N	40	\N
5	1	1	5	2025-03-25 11:31:03.650432	\N	\N	2025-03-26 19:17:18.96094	70	\N	40	\N
\.


--
-- Name: job_matches_id_seq; Type: SEQUENCE SET; Schema: public; Owner: job_user
--

SELECT pg_catalog.setval('public.job_matches_id_seq', 16, true);


--
-- Name: job_matches job_matches_pkey; Type: CONSTRAINT; Schema: public; Owner: job_user
--

ALTER TABLE ONLY public.job_matches
    ADD CONSTRAINT job_matches_pkey PRIMARY KEY (id);


--
-- Name: ix_job_matches_id; Type: INDEX; Schema: public; Owner: job_user
--

CREATE INDEX ix_job_matches_id ON public.job_matches USING btree (id);


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
-- PostgreSQL database dump complete
--

