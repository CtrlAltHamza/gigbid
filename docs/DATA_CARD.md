# GigBid Data Card & Attribution Specification

> **Course**: AI-4016 Advanced Agentic AI (Assignment 2)  
> **Institution**: FAST-NUCES Islamabad  
> **Author**: Hamza ([@CtrlAltHamza](https://github.com/CtrlAltHamza))  
> **Repository**: [https://github.com/CtrlAltHamza/gigbid](https://github.com/CtrlAltHamza/gigbid)

---

## 1. Overview & Dataset Strategy

The GigBid system operates in an autonomous freelance copilot environment, requiring realistic marketplace feeds, historical pricing benchmarks, client behavior patterns, and verifiable freelancer portfolio evidence. 

To satisfy the requirements announced by the course instruction team, GigBid implements a **hybrid empirical data architecture**:
1. **Real-World Empirical Baselines**: Statistical distributions, budget ranges, skill co-occurrences, client payment verification rates, and contract outcomes sampled and synthesized from 6 canonical Kaggle Upwork/freelance datasets.
2. **Deterministic Custom Simulator (`gigsim`)**: A custom-built marketplace and client simulator engine (`gigsim/engine.py`) implementing search, proposal submission, evaluation, and interview scheduling.
3. **Verifiable Synthetic Persona Corpora**: Where real-world data is confidential or ungrounded (e.g., proprietary client source code, NDA case studies, and private messages), high-fidelity synthetic portfolios are generated and strictly grounded in AST-verifiable code repositories.

---

## 2. Real-World Kaggle Dataset Attribution & Licensing

GigBid references and models distributions from the following six datasets approved and announced by the course teaching assistants:

| Dataset Name | Primary Author | Source URL & Identifiers | Records | License | Role in GigBid System |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Upwork Job Postings Dataset 2024** | asaniczka | [kaggle.com/.../upwork-job-postings-dataset-2024-50k-records](https://www.kaggle.com/datasets/asaniczka/upwork-job-postings-dataset-2024-50k-records) | 50,000 | Open Data Commons (ODbL) | Job taxonomy, skill tag co-occurrence matrix, hourly rate floors, fixed vs. hourly ratios. |
| **All Jobs on Upwork (200k+)** | asaniczka | [kaggle.com/.../all-jobs-on-upwork-200k-plus](https://www.kaggle.com/datasets/asaniczka/all-jobs-on-upwork-200k-plus) | 200,000+ | Open Data Commons (ODbL) | Long-tail technical requirements, connects cost bands (8, 12, 16 connects), client country distribution. |
| **Upwork Freelance Jobs 60k** | Ahmed Myalo | [kaggle.com/.../upwork-freelance-jobs-60k](https://www.kaggle.com/datasets/ahmedmyalo/upwork-freelance-jobs-60k) | 60,000 | CC0: Public Domain | Clean natural-language job specifications, client budget vs. actual spend benchmarks. |
| **Freelance Contracts Dataset** | asaniczka | [kaggle.com/.../freelance-contracts-dataset-1-3-million-entries](https://www.kaggle.com/datasets/asaniczka/freelance-contracts-dataset-1-3-million-entries) | 1,300,000 | Open Data Commons (ODbL) | Historical contract outcomes, proposal-to-hire conversion rates, repeat client hiring probabilities. |
| **Freelancer Success & Earnings** | Sarvesh Chhetri | [kaggle.com/.../freelancer-success-earnings-and-churn-prediction](https://www.kaggle.com/datasets/sarveshchhetri/freelancer-success-earnings-and-churn-prediction) | Tabular | CC BY-SA 4.0 | Freelancer rating thresholds, churn risk vs. hourly floor ($55-$75/hr), connects ROI modeling. |
| **Trial-1 Freelance Project Bids** | Aditya M. Mantri | [kaggle.com/.../adityammantri/trial-1](https://www.kaggle.com/datasets/adityammantri/trial-1) | Tabular | Open Database | Bid price dispersion, delivery turnaround distributions (7–30 days), client interview ratios. |

---

## 3. Data Preprocessing & Schema Harmonization Pipeline

Raw data from the above Kaggle sources underwent multi-stage preprocessing to produce clean, schema-conforming test and simulator data:

```
[ Raw Kaggle Datasets (CSV/JSON) ]
             │
             ▼
[ 1. Cleaning & Filtering ]
   - Deduplication on job title + description hash
   - Stripped HTML tags, unicode artifacts, and tracking parameters
   - Filtered for English language postings (>98% confidence)
             │
             ▼
[ 2. Statistical Distribution Sampling ]
   - Extracted budget percentiles (p10, p25, p50, p75, p90) by skill category
   - Mapped connects cost heuristic: 8 (<$500), 12 ($500-$2000), 16 (>$2000)
   - Calculated client payment verification ratio (68% verified, 32% unverified)
             │
             ▼
[ 3. Schema Harmonization ]
   - Normalized into typed Pydantic models: `Job`, `ClientProfile`, `Proposal`
   - Generated `gigsim/data/jobs.json`, `clients.json`, and `historical_jobs.json`
             │
             ▼
[ 4. Adversarial Data Injection ]
   - Seeded 12 scam patterns (Telegram off-platform bypass, fake checks, WhatsApp phishing)
   - Seeded 6 prompt-injection attacks (`<SYSTEM> Ignore instructions...`)
```

---

## 4. Distinction: Real-World Foundation vs. Synthetic Generation

Following the course instructions to **"clearly distinguish realistic synthetic data from real data"**, the boundary is explicitly defined below:

| Artifact / Corpus | Data Source Nature | Rationale & Methodology |
| :--- | :---: | :--- |
| **Marketplace Job Postings (`gigsim/data/jobs.json`)** | **Empirically Seeded** | Based directly on real-world distributions from the Asaniczka and Ahmed Myalo Upwork datasets. Realistic skill combinations, budgets, and descriptions. |
| **Historical Contracts (`gigsim/data/historical_jobs.json`)** | **Empirically Sampled** | 1,500 historical contracts statistically calibrated against the 1.3M Freelance Contracts dataset for pricing regression. |
| **Hiring Client Profiles (`gigsim/data/clients.json`)** | **Semi-Synthetic** | Client metadata (spend bands, review counts) sampled from real data; private hiring heuristics (e.g. `dislikes_generic_openings`) modeled synthetically. |
| **Freelancer Personas (`data/personas/`)** | **High-Fidelity Synthetic** | Generated with realistic technical depth to preserve real freelancer NDA confidentiality. All 20 case studies per persona reference verifiable AST symbols in accompanying repositories. |
| **Annotated Dev Set (`evals/datasets/dev_set.json`)** | **Curated & Annotated** | 600 jobs manually curated with gold-standard labels (`gold_decision`, `is_scam`, `gold_evidence_ids`, `fair_price_band`) for deterministic evaluation. |
| **Adversarial Test Bids & Phishing** | **Synthetic Adversarial** | Explicitly crafted to evaluate safety guardrails (`Risk Assessor` node and prompt injection regex sandboxes). |

---

## 5. Custom Autonomous Simulator (`gigsim`)

As clarified by the teaching assistant in course communication, students are required to implement the simulator engine. 

GigBid includes a complete, standalone marketplace simulator located in [`gigsim/`](../gigsim/):
* **Engine (`gigsim/engine.py`)**: Stateful `GigSimEngine` implementing:
  * `search_jobs()`: Full-text and skill-filtered job feed querying.
  * `get_job()`: Retrieval of complete structured job specifications.
  * `submit_proposal()`: Idempotent proposal submission with Connects deduction.
  * `evaluate_proposal()`: Deterministic client review simulation scoring proposals against client hidden preferences (`must_have_skills`, `budget_ceiling`, `dislikes_generic_openings`).
  * `get_messages()` & `schedule_interview()`: Real-time message thread generation and calendar booking.
* **API Service (`gigsim/app.py`)**: Standalone FastAPI ASGI service running on port 8001 (or embedded within the main backend in simulator mode).
* **CLI Utility (`gigsim/cli.py`)**: Interactive terminal client for inspecting and testing simulator state.

---

## 6. Dataset Limitations & Ethical Considerations

1. **Platform Policy Compliance**: No live Upwork scraping was conducted during this project; all empirical data was obtained from published, open-licensed Kaggle academic research archives.
2. **Temporal Validity**: Datasets primarily cover 2023–2024 postings. Market pricing heuristics for emerging technologies (e.g. LangGraph, Gemini 2.5, MCP) were augmented with 2026 industry rate cards.
3. **Geographic Skew**: Kaggle datasets exhibit a higher concentration of US/European clients. The simulator includes diversified global client profiles to test currency and timezone normalization.
4. **Safety & Sanitization**: All potential personal identifiable information (PII)—including personal client names, contact numbers, and payment IDs—has been sanitized and replaced with synthetic placeholders.
