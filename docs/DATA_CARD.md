# GigBid Data Card

## 1. Overview & Purpose
This data card documents the datasets and corpora used in GigBid for retrieval-augmented generation (RAG), agent decision evaluation, and marketplace simulation (FAST-NUCES AI-4016).

## 2. Dataset Inventory

### A. Freelancer Persona Corpora (`data/personas/`)
Three distinct professional personas providing realistic, messy ground-truth portfolio evidence:
- **`ai_engineer` (Alex Rivera)**: Lead AI/ML Engineer
  - 1 Curriculum Vitae (`cv.md`)
  - 20 Production Case Studies (`case_studies/cs-ai-01.md` through `cs-ai-20.md`) covering tabular ML, RAG, time-series, computer vision, and LLM guardrails.
  - 5 Git repositories with `README.md` and executable `main.py` code.
  - 25 Client reviews with industry, rating, and testimonial text.
  - 150 Past proposals labelled `won` (45), `replied` (50), or `ignored` (55).
- **`fullstack_dev` (Sarah Chen)**: Senior Full-Stack Web Developer
  - 1 CV, 20 Case Studies (Next.js, FastAPI, WebSockets, Supabase, Stripe billing).
  - 5 Repositories with code and architecture documentation.
  - 25 Client reviews, 150 labelled past proposals.
- **`data_analyst` (Marcus Vance)**: Principal Data Analyst & BI Specialist
  - 1 CV, 20 Case Studies (dbt, Snowflake, PostgreSQL optimization, cohort retention, Tableau).
  - 5 Repositories with SQL/Python pipelines.
  - 25 Client reviews, 150 labelled past proposals.

### B. GigSim Seed Data (`gigsim/data/`)
- **`jobs.json`**: 60 active jobs spanning machine learning, full-stack, data analytics, low-budget filters, scam posts (`unpaid_work`, `off_platform_contact`), and planted prompt-injection attacks.
- **`clients.json`**: 30 hiring clients with verified payment flags, total spend, rating, and hidden evaluation preferences (`must_have_skills`, `budget_ceiling`, `dislikes_generic_openings`).
- **`historical_jobs.json`**: 1,500 historical jobs used for pricing regression, floor calibration, and Connects ROI calculation.

### C. Development Evaluation Set (`evals/datasets/dev_set.json`)
- 600 total jobs (200 per persona) with gold annotations:
  - `gold_decision`: "bid" or "skip"
  - `is_scam`: boolean with scam taxonomy
  - `planted_injection`: boolean indicator
  - `gold_evidence_ids`: ground-truth portfolio evidence required to prove competence
  - `fair_price_band`: `{"min": ..., "max": ...}`

## 3. Data Integrity & Safety Guardrails
- **Confidentiality**: All personas, client histories, and jobs are synthetically generated and safe for public GitHub repository hosting.
- **No Hidden Test Leakage**: The dev evaluation set is strictly separated; the hidden evaluation test set never enters this repository.
- **Prompt Injection Delimiters**: Posts containing adversarial prompt injection attacks are tested in evaluation suites to verify that agent instructions cannot be hijacked.
- **PII Scrubbing**: Emails, phone numbers, and payment details are masked across all logs and traces.
