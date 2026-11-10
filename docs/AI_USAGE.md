# AI Usage Disclosure & Engineering Verification Log

**Student Name**: Hamza  
**GitHub Profile**: [@CtrlAltHamza](https://github.com/CtrlAltHamza)  
**Repository**: [https://github.com/CtrlAltHamza/gigbid](https://github.com/CtrlAltHamza/gigbid)  
**Course**: AI-4016 Advanced Agentic AI (R&D Assignment 2, FAST-NUCES Islamabad)

---

## 1. AI Coding Assistants & Models Used

Throughout the design, implementation, evaluation, and documentation of the **GigBid Multi-Agent Freelancer Copilot**, the following AI tools and foundation models were utilized:
1. **Antigravity IDE & Pairing Agent**: Google Gemini 2.5 Pro / Claude 3.7 Sonnet hybrid agent for architecture planning, refactoring, and code generation.
2. **Evaluation Foundation Models**:
   - `gemini-2.5-pro`: Utilized as the primary calibrated LLM Judge for proposal specificity and groundedness scoring.
   - `gemini-2.5-flash`: Utilized for high-throughput Scout filtering, regex parsing, and atomic claim generation.
   - `bge-reranker-large` / Cross-Encoder: In-memory scoring for RAG ablation experiments.

---

## 2. Granular Task Breakdown

| Subsystem / Task | Files Affected | Extent of AI Assistance | Human Verification & Engineering Intervention |
| :--- | :--- | :--- | :--- |
| **MCP Tool Layer (Part A)** | `mcp_servers/portfolio/`, `marketplace/`, `workspace/` | Initial FastMCP server boilerplate and tool schemas generated. | Added strict Pydantic v2 metadata validation, audit log persistence, token bucket rate limiter, and dry-run flag logic. |
| **Advanced RAG Engine (Part B)** | `rag/variants/`, `rag/index/`, `rag/verify.py` | Scaffolding for BM25 and TF-IDF cosine vector search. | Implemented reciprocal rank fusion (RRF), calibrated LLM judge inter-rater reliability protocol ($\kappa = 0.866$), and NLI atomic claim verification. |
| **Multi-Agent Orchestration (Part C)** | `agent/graphs/`, `agent/nodes/`, `agent/state.py` | StateGraph node stubs and prompt drafting. | Diagnosed and fixed parallel reducer state collision (`InvalidUpdateError`), implemented bounded 2-cycle critique loop, and SQLite interrupt checkpointing. |
| **Web Application (Part D)** | `apps/web/src/`, `apps/api/` | React component layout and Tailwind styling assistance. | Configured FastAPI SSE streaming proxy with buffering disabled, interactive citation hover popovers, and 5 Playwright E2E test specs. |
| **Production Worker & Security (Part E)** | `worker/`, `agent/security/`, `infra/` | Dockerfile drafting and regex pattern generation. | Fixed variable-width look-behind error in regex compiler, added SQLite task idempotency store, and docker-compose healthchecks. |
| **Signature Extension X3 (Part F)** | `extensions/portfolio_builder/` | Initial parser outline. | Built complete Python AST traversal engine (`ast.parse`) to detect hallucinated classes and reject them prior to case study synthesis. |

---

## 3. Detailed Failure Case: Incorrect AI Suggestion & Correction

### The Bug / Incorrect Suggestion
During the implementation of parallel fan-out in the LangGraph Bid Graph (`scout -> [analyst, risk_assessor, fit_matcher]`), the AI assistant initially generated graph nodes where all three parallel nodes returned updates to the top-level state dictionary without reducer wrappers:
```python
# INCORRECT AI SUGGESTION
class GigBidState(TypedDict):
    step_count: int
    execution_trace: List[str]
    job_spec: Dict[str, Any]
    risk_report: Dict[str, Any]
    fit_report: Dict[str, Any]
```
When LangGraph executed all three nodes concurrently during the same superstep, it raised:
```
InvalidUpdateError: At key 'step_count': Can receive only one value per step. Received 3 updates.
```

### The Root Cause Analysis
In LangGraph, when nodes execute in parallel within the same superstep, any state key that receives updates from multiple nodes MUST have an associative, commutative reducer (such as `operator.add`). Without a reducer, LangGraph cannot deterministically resolve concurrent writes to the same primitive scalar.

### The Engineering Correction
We refactored `agent/state.py` to annotate concurrently updated fields with `operator.add`, while ensuring that parallel nodes only mutate their dedicated sub-keys:
```python
# CORRECTED IMPLEMENTATION
from typing import Annotated
import operator

class GigBidState(TypedDict):
    step_count: Annotated[int, operator.add]
    execution_trace: Annotated[List[str], operator.add]
    errors: Annotated[List[str], operator.add]
    # Distinct dedicated keys for parallel branches:
    risk_report: Dict[str, Any]
    fit_report: Dict[str, Any]
```
In addition, each parallel node was adjusted to return `{"step_count": 1}` so that the reducer smoothly aggregated the total superstep operations. All unit tests (`test_bid_graph.py`) passed immediately following this correction.

---

## 4. Academic Integrity & Responsibility Statement

I acknowledge full intellectual ownership and technical responsibility for all source code, evaluation datasets, architectural documentation, and deliverables committed in this repository. All AI interactions served as an engineering amplifier, with every generated function, prompt, and test case inspected, executed, verified, and debugged locally.
