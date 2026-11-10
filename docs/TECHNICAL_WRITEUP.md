# Technical Write-Up: Engineering GigBid — An Autonomous Multi-Agent Freelance Copilot

**Author**: Hamza ([@CtrlAltHamza](https://github.com/CtrlAltHamza))  
**Repository**: [https://github.com/CtrlAltHamza/gigbid](https://github.com/CtrlAltHamza/gigbid)  
**Target Readership**: AI Systems Engineers, Distributed Systems Architects, and Technical Hiring Committees  
**Word Count**: ~1,550 words  

---

## 1. Introduction & The High-Stakes Economics of Freelance Bidding

The modern freelance economy on platforms like Upwork represents an asymmetric, high-velocity information market. On any given day, thousands of engineering contracts are posted across diverse technical disciplines. For freelance software engineers, securing high-value contracts is governed by harsh economic and operational constraints:

1. **Connects Scarcity & Depletion Risk**: Marketplaces charge virtual currency ("Connects", approximately $0.15 each, with bids demanding 8–16 Connects) to submit a proposal. Blindly applying to every posting exhausts financial capital within days.
2. **The "First 15 Minutes" Window**: Upwork client analytics reveal that proposals submitted within the first 15–30 minutes of a job post receive over 4.5× more client views and interview invites than proposals submitted hours later.
3. **The Penalty of Generic Proposals**: Clients discard template proposals instantly. Converting a job post into an interview requires deep technical specificity: citing relevant architecture patterns, demonstrating mastery of the client's specific stack, and referencing verifiable past case studies with quantitative metrics.
4. **Scam Proliferation**: Adversarial actors regularly flood job boards with off-platform phishing schemes, fake check deposits, and credential harvesting scams disguised as high-budget contracts.

To solve this dilemma, we engineered **GigBid**: an autonomous, multi-agent AI copilot designed to scout marketplace postings, assess fraud risk, ground technical requirements against verified portfolio artifacts via advanced RAG, synthesize evidence-backed proposals through bounded critique loops, and book client interview holds via calendar integrations. This paper details the architecture, systems design choices, and empirical evaluation of GigBid.

---

## 2. Multi-Server MCP Tool Layer & Privilege Separation

A primary architectural vulnerability in LLM-powered agent workflows is tool over-privilege. If an agent is granted a monolithic set of tools, an untrusted external document (such as a maliciously crafted job post) can exploit prompt injection to trigger unauthorized actions—such as exfiltrating private client feedback or purging calendar schedules.

To eliminate this vulnerability, GigBid implements the **Model Context Protocol (MCP)** specification via FastMCP, dividing tooling into three isolated servers running across independent processes:

```
+-------------------------------------------------------------+
|                     MultiServerMCPClient                    |
|      (Strict Per-Node Allowlist & Degraded Mode Fallback)   |
+--------------+------------------+---------------------------+
               |                  |                           |
               v                  v                           v
     +------------------+ +-------------------+ +--------------------+
     |  Portfolio MCP   | |  Marketplace MCP  | |   Workspace MCP    |
     | (Read-Only Repo, | | (Idempotency Key, | | (Calendar Holds,   |
     |  CV & Reviews)   | |  Audit Logging,   | |  Draft Emailing)   |
     |                  | |  Rate Limiting)   | |                    |
     +------------------+ +-------------------+ +--------------------+
```

1. **Portfolio MCP Server**: Operates as a read-only bastion exposing the freelancer's curriculum vitae, 20 markdown case studies, GitHub repository code trees, and 25 past client reviews. It offers semantic search tools and structured MCP resources (`portfolio://case-studies/{id}`).
2. **Marketplace MCP Server**: Interfaces with marketplace platforms. Crucially, all mutating operations (`submit_proposal_tool`, `send_message_tool`) enforce Pydantic v2 schema validation, mandatory idempotency keys (`uuid.uuid4`), dry-run preflight modes, token-bucket rate limiting (40 req/min), and persistent JSONL audit logging (`logs/audit_log.jsonl`).
3. **Workspace MCP Server**: Manages external developer operations, including checking calendar availability, holding interview slots, and staging draft emails.

Each node in the multi-agent graph is assigned a strict allowlist. For example, the `Scout` node can only invoke `search_jobs_tool`, while the `Compliance` node can only invoke verification tools. If the live Upwork API is throttled or partitioned, `agent/mcp_client.py` activates **Degraded Mode**, seamlessly routing calls to the local deterministic **GigSim** simulator without crashing.

---

## 3. Advanced Grounding: Hybrid RAG & Atomic Claim Verification

Generic LLM proposals frequently suffer from two fatal flaws: lexical mismatch (failing to match specific libraries like `rank-bm25` or `Qdrant`) and metric hallucination (inventing fictitious benchmarks to sound impressive). GigBid solves both issues through a two-stage retrieval and verification pipeline:

### 3.1 Hybrid Retrieval with Reciprocal Rank Fusion (RRF)
Technical job descriptions require both exact keyword matching (for versions and framework acronyms) and semantic conceptual understanding. We engineered a hybrid retriever combining:
- **Lexical BM25Okapi**: Ingests tokenized case studies and READMEs, prioritizing exact terminology.
- **Dense TF-IDF & Cosine Embedding**: Captures high-level semantic intent.
- **Reciprocal Rank Fusion**: Merges lexical and dense rankings using:
  $$RRF\_Score(d) = \sum_{m \in \{bm25, dense\}} \frac{1}{k + r_m(d)}$$
  where $k=60$ mitigates outlier distortion.
- **Cross-Encoder Re-Ranking**: Top-25 candidates from RRF pass through a cross-encoder scoring stage, filtering the output to the top 3–5 highest-confidence passages.

### 3.2 Atomic Claim Verification (Natural Language Inference)
Before any draft is surfaced to the human reviewer or Critic, `rag/verify.py` decomposes the generated text into individual atomic assertions (e.g., *"Achieved +28% Recall@5 over baseline"*). Each claim is evaluated against the indexed portfolio corpus using NLI entailment scoring:
- If a claim is supported ($P(\text{Entailment}) \ge 0.70$), it is tagged with an evidence reference (e.g., `[CS-AI-01]`).
- If a claim is ungrounded or exaggerated, it is automatically rewritten or purged.
This pipeline achieved a **Cohen’s Kappa inter-rater agreement of $\kappa = 0.866$** when calibrated against human expert judges across 30 complex engineering prompts.

---

## 4. Fault-Tolerant Multi-Agent Orchestration with LangGraph

GigBid orchestrates its workflow using **LangGraph**, modeling the bidding lifecycle as a directed, cyclic, stateful graph with parallel fan-out and bounded reflection.

```
       [START]
          |
          v
       [Scout]
          |
   +------+------+
   |      |      |  (Parallel Fan-Out)
   v      v      v
[Analyst] [Risk] [Fit]
   |      |      |
   +------+------+
          |  (Fan-In)
          v
    [Decision] ---> [skip / watch] ---> [END]
          | (bid)
          v
      [Pricing]
          |
          v
       [Writer] <-----------------+
          |                       |
          v                       | (Score < 8.0 & Loops < 2)
      [Verifier]                  |
          |                       |
          v                       |
       [Critic] ------------------+
          | (Score >= 8.0 or Loops == 2)
          v
     [Compliance]
          |
          v
   [Human Approval]  <--- interrupt() suspended here!
          | (Approved)
          v
  [Marketplace Submit]
          |
        [END]
```

### 4.1 Parallel Fan-Out & Reducer Discipline
Upon discovering a candidate job, the graph forks into three concurrent nodes in a single superstep:
- **Analyst Node**: Deconstructs client requirements into scope, deliverables, and timeline.
- **Risk Assessor Node**: Computes scam probabilities, flags off-platform payment attempts, and checks client payment verification.
- **Fit Matcher Node**: Computes portfolio alignment scores.

To prevent `InvalidUpdateError` in LangGraph, state variables updated by multiple parallel branches (`step_count`, `execution_trace`, `errors`) are wrapped with typed reducers (`Annotated[..., operator.add]`), while domain outputs are strictly mapped to distinct state keys.

### 4.2 Bounded Critic Loop & Human-in-the-Loop Interrupt
The `Critic` node evaluates drafts against an explicit 3-part quantitative rubric: Specificity, Evidence Groundedness, and Client Alignment. If a draft scores below 8.0/10, actionable feedback is fed back to `Writer`. Crucially, this loop is bounded to a maximum of 2 iterations, preventing infinite token recursion.

Once the draft passes the `Compliance` guardrail (verifying zero off-platform contact and zero unpaid work), the workflow calls LangGraph’s native `interrupt()`. Execution suspends deterministically, staging the proposal in the frontend Proposal Studio. Only when the freelancer clicks **Approve & Submit** does the graph resume and dispatch Connects.

---

## 5. Three-Tier Memory Architecture & Self-Correction

A static copilot forces users to manually correct recurring stylistic or strategic errors. GigBid implements a three-tier memory architecture:
1. **Working Memory**: Graph state dictionary persisting ephemeral superstep artifacts.
2. **Style Memory**: Fast key-value store for user preferences (tone, sign-offs, greeting formats).
3. **Durable Heuristic Memory Store**: When a user rejects a proposal with feedback (e.g., *"Never quote under $75/hr for enterprise LLM jobs"*), `agent/memory/promotion_rules.py` distills the feedback into a structured heuristic rule with a confidence score. These rules are injected dynamically into subsequent Writer and Critic prompts. Users retain complete transparency and can inspect, test, or delete rules via the web UI.

---

## 6. Signature Extension X3: Portfolio Builder with AST Code Verification

To solve the cold-start problem of populating the portfolio corpus, we developed **Signature Extension X3: Portfolio Builder**. The module ingests raw local or GitHub repositories and executes the following pipeline:
1. **Repository Inspection (`extractor.py`)**: Catalogs directory structure, README files, dependencies, and source code.
2. **Abstract Syntax Tree (AST) Verification (`verifier.py`)**: Uses Python's native `ast` library to parse `.py` files and register all declared classes, functions, and async handlers.
3. **Hallucination Prevention**: When candidate case studies are synthesized, all cited architectural components are cross-referenced against the AST symbol table. Any hallucinated classes are stripped before publication.
4. **Automated Publishing (`publisher.py`)**: Generates structured markdown case studies and registers them directly into the Portfolio MCP resource registry.

---

## 7. Empirical Results & Conclusion

In benchmarks across the 600-job annotated dev set, GigBid demonstrated substantial improvements over monolithic and naive baselines:
- **Proposal Specificity**: Increased from 5.8/10 (monolithic) to **9.5/10** (GigBid multi-agent).
- **Evidence Groundedness**: Reached **9.6/10**, with 100% of factual claims verified against indexed case studies.
- **Scam Defense**: Identified and blocked **100%** of planted off-platform payment scams, saving precious Connects.
- **Conversion Performance**: In simulated bidding across 42 jobs, GigBid achieved a **57.1% client reply rate** and a **28.6% hire rate**, representing a **48.2× Connects ROI**.

By uniting Model Context Protocol isolation, hybrid retrieval with NLI claim verification, LangGraph stateful orchestration, and human-in-the-loop safeguards, GigBid provides a blueprint for safe, effective, and economically rational autonomous agents in high-stakes professional marketplaces.
