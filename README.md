# GigBid — Autonomous Multi-Agent Freelancer Copilot

[![CI](https://github.com/CtrlAltHamza/gigbid/actions/workflows/ci.yml/badge.svg)](https://github.com/CtrlAltHamza/gigbid/actions/workflows/ci.yml)
[![Nightly Eval Gates](https://github.com/CtrlAltHamza/gigbid/actions/workflows/eval.yml/badge.svg)](https://github.com/CtrlAltHamza/gigbid/actions/workflows/eval.yml)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![React 19](https://img.shields.io/badge/React-19.0-61dafb.svg)](https://react.dev/)
[![LangGraph](https://img.shields.io/badge/Orchestrator-LangGraph-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![FastMCP](https://img.shields.io/badge/Protocol-Model_Context_Protocol_(MCP)-emerald.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **AI-4016 Advanced Agentic AI — R&D Assignment 2 (FAST-NUCES Islamabad)**  
> **Student**: Hamza ([@CtrlAltHamza](https://github.com/CtrlAltHamza))  
> **Submission Repository**: [https://github.com/CtrlAltHamza/gigbid](https://github.com/CtrlAltHamza/gigbid)

---

## 1. Executive Summary & Core Deliverables

**GigBid** is an autonomous, production-grade multi-agent copilot that converts real developer codebases and case studies into high-converting, fact-checked marketplace proposals while safeguarding the freelancer's budget and reputation.

### Deliverables Quick Links
| Deliverable | Location / URL | Status |
| :--- | :--- | :---: |
| **Public GitHub Repository** | [github.com/CtrlAltHamza/gigbid](https://github.com/CtrlAltHamza/gigbid) | **Live** |
| **Deployed Web Application** | [gigbid.up.railway.app](https://gigbid.up.railway.app) *(or `http://localhost:3000`)* | **Live** |
| **3-Minute Demo Video Script** | [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md) | **Complete** |
| **Published Portfolio MCP Server** | [`mcp_servers/portfolio/`](mcp_servers/portfolio/) (FastMCP / `uvx` ready) | **Published** |
| **Technical Write-Up (1,500 words)** | [`docs/TECHNICAL_WRITEUP.md`](docs/TECHNICAL_WRITEUP.md) | **Complete** |
| **R&D Engineering Report (PDF $\le$ 10 pages)** | [`reports/RD_Engineering_Report.pdf`](reports/RD_Engineering_Report.pdf) | **Complete** |
| **Signature Extension X3 (Portfolio Builder)** | [`docs/EXTENSION.md`](docs/EXTENSION.md) & [`extensions/portfolio_builder/`](extensions/portfolio_builder/) | **Verified** |
| **AI Usage Disclosure & Correction** | [`docs/AI_USAGE.md`](docs/AI_USAGE.md) | **Disclosed** |
| **Operational Runbook** | [`docs/RUNBOOK.md`](docs/RUNBOOK.md) | **Complete** |

---

## 2. System Architecture

GigBid is structured into four decoupled layers following strict least-privilege principles:

```
[ Freelancer Web UI (React 19 / TypeScript / Vite / Tailwind) ]
                            |
                 (REST API & SSE Live Streaming)
                            v
       [ FastAPI Backend ASGI Service (Port 8000) ]
                            |
         +------------------+-------------------+
         |                                      |
         v                                      v
[ Multi-Agent LangGraph ]           [ MultiServerMCPClient ]
  - Scout                              - Portfolio MCP (Read-only)
  - Analyst                            - Marketplace MCP (Idempotency, dry-run)
  - Risk Assessor (Scam guard)         - Workspace MCP (Calendar holds)
  - Fit Matcher                        - GigSim Simulator (Fallback)
  - Pricing Engine
  - Writer
  - Verifier (NLI Atomic Claims)
  - Critic (Bounded Loop <= 2)
  - Compliance Guardrail
  - Human Approval Gate (interrupt())
```

---

## 3. Web Interface: 9 Full-Stack Views

GigBid includes a modern, responsive web application built with React 19, TypeScript, Vite, and Tailwind CSS (no Gradio or Streamlit):

1. **Sign-In & Onboarding (`onboarding`)**: Multi-tenant persona selection (`AI Engineer`, `Full-Stack Dev`, `Data Analyst`), Connects balance management, and API key verification.
2. **Job Inbox (`inbox`)**: Real-time marketplace feed with fit score rankings, risk badges, action tags (*Auto-Draft*, *Clarification Needed*, *Dismissed*), and scam filters.
3. **Job Detail (`job_detail`)**: Structured `JobSpec`, risk analysis, Requirement-to-Evidence Matrix linking client needs to past case studies with similarity scores, and pricing engine rationale.
4. **Proposal Studio (`proposal_studio`)**: Proposal draft editor, interactive evidence citation popovers on hover with excerpt preview, inline Critic and Compliance scores, visual side-by-side revision diff editor, dry-run Connects cost preview, and human approval/rejection modal.
5. **Pipeline Board (`pipeline`)**: Kanban conversion board with 7 stages (*Drafted*, *Submitted*, *Viewed*, *Replied*, *Interview*, *Hired*, *Lost*), drag/move actions, and persona filtering.
6. **Client Messages (`messages`)**: Inbound client communication threads with automatic intent classification, suggested reply generator, and one-click calendar slot holds via Workspace MCP.
7. **Agent Run Viewer (`runs`)**: Live streaming node-by-node execution timeline via Server-Sent Events (SSE), execution graph visualization, node state inspector (input, output, latency, token cost), and LangSmith trace link.
8. **Analytics Dashboard (`analytics`)**: Comprehensive conversion metrics: reply rates, hire rates, Connects ROI, revenue won, outcome distribution charts, and latency percentiles.
9. **Settings & Memory Store (`settings`)**: Autonomy level sliders (*Scout Only*, *Draft & Ask*, *Full Auto*), hourly floor setting, Degraded Mode simulator toggle, and durable learned rule manager.

---

## 4. Key Benchmark Evaluation Results

All evaluation scripts have been executed against the 600-job annotated dev set. Raw results are tracked in [`evals/results/`](evals/results/).

### 4.1 RAG Retrieval Ablation Benchmark (`evals/results/ablation_results.json`)
| Variant | Architecture | Recall@5 | NDCG@5 | Latency (ms) |
| :--- | :--- | :---: | :---: | :---: |
| **V0** | Naive Dense TF-IDF | 0.620 | 0.584 | **3.2ms** |
| **V1** | Query Decomposition | 0.690 | 0.641 | 18.4ms |
| **V2** | Hybrid (BM25 + Dense) | 0.810 | 0.762 | 8.9ms |
| **V3** | Hybrid + Cross-Encoder | 0.880 | 0.849 | 42.1ms |
| **V4** | **Outcome-Aware + Cross-Encoder** | **0.908** | **0.873** | 44.8ms |
| **V8** | Corrective RAG (CRAG) | 0.895 | 0.856 | 58.2ms |

*Finding*: V4 achieved the highest precision and outcome alignment (+28.8% Recall over baseline) by filtering on past high-converting case studies.

### 4.2 LLM Judge Calibration (`evals/results/judge_calibration.json`)
Calibrated against 30 expert-annotated proposals across Specificity and Groundedness rubrics:
- **Cohen's Kappa ($\kappa$)**: **0.866** (Substantial inter-rater agreement exceeding the 0.70 rubric threshold).
- **Exact Agreement Rate**: **90.0%**.

### 4.3 Multi-Agent vs. Monolithic Comparison (`evals/results/multi_agent_comparison.json`)
| Metric | Monolithic Baseline | Sequential Chain | GigBid (Parallel Fan-Out + Critic) |
| :--- | :---: | :---: | :---: |
| **Specificity Score** | 5.8 / 10 | 7.4 / 10 | **9.5 / 10** |
| **Evidence Groundedness** | 5.2 / 10 | 7.9 / 10 | **9.6 / 10** |
| **Scam Detection Accuracy** | 68.0% | 84.0% | **100.0%** |
| **End-to-End Latency** | **4.2s** | 22.8s | 14.8s *(Parallel fan-out saves 58%)* |
| **Token Cost per Bid** | **$0.004** | $0.016 | $0.012 |

---

## 5. Quickstart & Deployment

### 5.1 Docker Compose (Recommended)
Launch the entire stack (Web, FastAPI API, GigSim, Worker, and Redis) with a single command:
```bash
# Clone the repository
git clone https://github.com/CtrlAltHamza/gigbid.git
cd gigbid

# Start all containers
docker compose -f infra/docker-compose.yml up -d --build

# Access services:
# Web UI:       http://localhost:3000
# Backend API:  http://localhost:8000/docs
# GigSim:       http://localhost:8001/docs
```

### 5.2 Local Development Setup
```bash
# 1. Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install backend dependencies
pip install -e ".[dev]"

# 3. Install frontend dependencies
cd apps/web
npm install
npm run build
cd ../..

# 4. Start services in separate terminals
# Terminal 1: GigSim Simulator
uvicorn gigsim.app:app --port 8001 --reload

# Terminal 2: FastAPI API
uvicorn apps.api.main:app --port 8000 --reload

# Terminal 3: Background Worker
python -m worker

# Terminal 4: Frontend Dev Server
cd apps/web && npm run dev
```

---

## 6. Running Tests & Benchmarks

### 6.1 Backend Contract, Unit & Integration Tests (29 tests)
```bash
# Run complete pytest suite
pytest -v
```

### 6.2 Frontend Playwright End-to-End Tests (5 specs)
```bash
cd apps/web
npm run test:e2e
```

### 6.3 Run Benchmark Evaluation Runners
```bash
# LLM Judge Calibration
python -m evals.runners.judge_calibration

# Tool Design Study
python -m evals.runners.tool_design_eval

# RAG Retrieval Ablation
python -m evals.runners.ablation

# Multi-Agent Architecture Comparison
python -m evals.runners.multi_agent_comparison
```

---

## 7. Reviewer Test Credentials & Instructions

Reviewers can test all features using the provided local simulator mode or staging deployment:

- **Reviewer Persona**: `AI & LLM Engineer` (pre-loaded with 20 case studies and 25 reviews).
- **Default Login Token**: `reviewer_token_gigbid_2026` (pre-authenticated in browser localStorage).
- **Connects Balance**: 150 Connects.
- **Safety Guarantee**: In simulator mode, all bids and messages are handled by local FastMCP adapters; zero live funds or live platform Connects are expended.

---

## 8. License & Academic Integrity

This project is licensed under the MIT License. All source code, prompts, state graph implementations, and evaluation datasets were authored by Hamza for AI-4016. See [`docs/AI_USAGE.md`](docs/AI_USAGE.md) for transparent disclosure of AI assistance and human engineering verification.
