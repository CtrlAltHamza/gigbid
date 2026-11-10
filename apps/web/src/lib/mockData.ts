import { Job, Proposal, MessageThread, AgentRun, MemoryRule, AnalyticsSummary } from '../types';

export const INITIAL_JOBS: Job[] = [
  {
    id: "job-ai-101",
    title: "Production RAG Pipeline with Hybrid Search & Re-ranking for Healthcare Data",
    client: "HealthTech Innovations (US, $45k spent, 4.9★)",
    platform: "Upwork",
    budget_type: "fixed",
    budget_min: 3500,
    budget_max: 4500,
    fit_score: 96,
    risk_level: "safe",
    scam_score: 0.02,
    red_flags: [],
    status: "auto_drafted",
    description: "Looking for a Senior AI/LLM Engineer to architect and implement an enterprise-grade RAG pipeline. We need hybrid search combining BM25 keyword matching and dense embeddings, cross-encoder re-ranking, and dynamic claim verification against HIPAA-compliant medical EHR corpus.",
    deliverables: [
      "Hybrid search retriever with reciprocal rank fusion (RRF)",
      "Cross-encoder re-ranking pipeline",
      "Fact-checking & atomic claim verification module",
      "Production FastAPI inference service with Docker & eval suite"
    ],
    scope: "Architecture, implementation, latency optimization (<250ms p95), and automated evaluation suite.",
    skills: ["Python", "LangChain/LangGraph", "FastAPI", "Vector Search", "Qdrant", "Cross-Encoder"],
    pricing_rationale: "Fixed milestone bid at $4,000 based on $80/hr × 50 estimated hours. High client rating and enterprise scope justify upper-quartile rate.",
    requirement_matches: [
      {
        requirement: "Hybrid BM25 + Dense Retriever with RRF",
        matched_skill: "Information Retrieval & Hybrid Search",
        evidence_id: "CS-AI-01",
        evidence_title: "Sub-100ms Multimodal Hybrid RAG for FinTech Compliance",
        excerpt: "Engineered hybrid BM25 + dense vector search pipeline with custom reciprocal rank fusion yielding +28% Recall@5 over baseline.",
        score: 0.94
      },
      {
        requirement: "Atomic claim verification & hallucination guardrails",
        matched_skill: "NLI Claim Entailment & Evaluation",
        evidence_id: "CS-AI-04",
        evidence_title: "Automated Evidence Verifier & Calibrated LLM Judge",
        excerpt: "Implemented decontextualized atomic claim splitting and NLI entailment scoring reaching 92% hallucination suppression.",
        score: 0.91
      }
    ],
    created_at: "10 mins ago",
    connects_cost: 16
  },
  {
    id: "job-ai-102",
    title: "URGENT: Crypto Trading Telegram Bot — Send WhatsApp deposit to start immediately",
    client: "Anonymous User (Unverified, $0 spent, 0★)",
    platform: "Upwork",
    budget_type: "fixed",
    budget_min: 8000,
    budget_max: 12000,
    fit_score: 41,
    risk_level: "scam",
    scam_score: 0.98,
    scam_reasoning: "High-confidence off-platform payment phishing detected. Job mentions contact via external WhatsApp (+1-555-SCAM) and demands advance deposit outside platform escrow.",
    red_flags: [
      "Demands off-platform communication via WhatsApp",
      "Requests upfront payment or deposit",
      "Unverified payment method and zero historical hiring on platform",
      "Suspiciously inflated budget for trivial bot request"
    ],
    status: "scam_blocked",
    description: "Looking for fast bot developer. Contact our manager on WhatsApp at +1-987-654-3210 for requirements and pay $50 deposit to receive repo credentials. High payout guaranteed within 24h.",
    deliverables: ["Contact manager on Telegram/WhatsApp", "Deposit initial security fee"],
    scope: "Phishing / Off-platform contract violation.",
    skills: ["Python", "Telegram Bot"],
    pricing_rationale: "N/A — Blocked by Compliance & Scam Defense node.",
    requirement_matches: [],
    created_at: "25 mins ago",
    connects_cost: 16
  },
  {
    id: "job-ai-103",
    title: "Multi-Agent System for Autonomous Market Research with LangGraph",
    client: "Apex Strategic Advisors (UK, $120k spent, 5.0★)",
    platform: "Upwork",
    budget_type: "hourly",
    budget_min: 75,
    budget_max: 95,
    hourly_rate: 85,
    fit_score: 93,
    risk_level: "safe",
    scam_score: 0.04,
    red_flags: [],
    status: "auto_drafted",
    description: "Seeking an expert in LangGraph and Agentic Workflows to design a 5-node agent pipeline that crawls filings, extracts KPIs, evaluates competitive positioning, and drafts executive briefing decks.",
    deliverables: [
      "LangGraph stateful workflow with checkpointing and human-in-the-loop interrupts",
      "Model Context Protocol (MCP) tool integration",
      "Structured output validation with Pydantic v2"
    ],
    scope: "Design, prompt engineering, multi-server MCP client, unit & integration test coverage.",
    skills: ["LangGraph", "Python", "MCP", "FastAPI", "AsyncIO"],
    pricing_rationale: "Targeting $85/hr (client bracket $75–$95/hr) for estimated 20-30 hrs/week ongoing retainer.",
    requirement_matches: [
      {
        requirement: "LangGraph stateful orchestration with interrupts",
        matched_skill: "Multi-Agent Architecture",
        evidence_id: "CS-AI-02",
        evidence_title: "Fault-Tolerant Multi-Agent Financial Extraction Graph",
        excerpt: "Built 8-agent LangGraph workflow with parallel fan-out, bounded critique loops, and SQLite checkpointing.",
        score: 0.95
      }
    ],
    created_at: "1 hour ago",
    connects_cost: 16
  },
  {
    id: "job-ai-104",
    title: "Fine-tune Small Language Models (Qwen / Llama) with LoRA on Custom Support Tickets",
    client: "ScaleOps Global (Canada, $60k spent, 4.8★)",
    platform: "Upwork",
    budget_type: "fixed",
    budget_min: 2500,
    budget_max: 3000,
    fit_score: 88,
    risk_level: "medium",
    scam_score: 0.18,
    red_flags: ["Ambiguous evaluation metrics for model performance"],
    status: "clarification_needed",
    description: "We have 15,000 multi-turn customer support chats. We need to fine-tune a compact open-source model (7B/8B) using Unsloth/PEFT for zero-shot categorization and automated reply suggestion.",
    deliverables: [
      "Data preprocessing and token length distribution analysis",
      "LoRA / QLoRA training script with wandb logging",
      "GGUF/vLLM quantized deployment package"
    ],
    scope: "Dataset preparation, fine-tuning run, benchmark against baseline gpt-4o-mini.",
    skills: ["PyTorch", "HuggingFace", "PEFT", "LoRA", "Unsloth", "vLLM"],
    pricing_rationale: "Fixed price $2,800. Needs clarification on GPU hardware availability and eval benchmarks before auto-submitting.",
    requirement_matches: [
      {
        requirement: "LoRA / QLoRA fine-tuning and quantization",
        matched_skill: "Model Optimization & Quantization",
        evidence_id: "CS-AI-05",
        evidence_title: "Edge LLM Distillation and 4-bit Quantization Pipeline",
        excerpt: "Distilled 70B model into 8B Llama using QLoRA, cutting latency by 64% while maintaining 94.2% task accuracy.",
        score: 0.89
      }
    ],
    created_at: "2 hours ago",
    connects_cost: 16
  }
];

export const INITIAL_PROPOSALS: Proposal[] = [
  {
    id: "prop-ai-101",
    job_id: "job-ai-101",
    job_title: "Production RAG Pipeline with Hybrid Search & Re-ranking for Healthcare Data",
    client: "HealthTech Innovations",
    persona: "ai_engineer",
    draft_content: `Hi HealthTech Innovations Team,

Your requirement for a HIPAA-grade hybrid RAG system with sub-250ms p95 latency maps directly to production architectures I have deployed. 

In a recent enterprise engagement ([CS-AI-01: FinTech Compliance RAG]), I engineered a dual-retriever hybrid pipeline pairing BM25Okapi keyword lexical matching with dense cosine embeddings and reciprocal rank fusion (RRF). That system achieved a +28% bump in Recall@5 over dense-only retrieval while keeping p95 latency under 110ms on a 500k document corpus.

Here is how I will architect your healthcare pipeline:
1. Retrieval Engine: Qdrant dense vector store with BAAI/bge-m3 embeddings combined with BM25 Okapi lexical scoring via rank-bm25, unified with Reciprocal Rank Fusion (k=60).
2. Re-Ranking & Precision: Cross-encoder (bge-reranker-large) applied over the top 25 candidate chunks, compressing to the top 5 most relevant passages.
3. Factuality & Guardrails: Decontextualized atomic claim splitting and NLI entailment scoring ([CS-AI-04]) to catch hallucinations before LLM generation reaches clinical users.
4. Infrastructure: Containerized FastAPI async endpoints with OpenTelemetry tracing and comprehensive PyTest evals.

I can deliver the end-to-end working pipeline with automated evals in 14 days. I would be glad to share an architecture walkthrough.

Best regards,
Hamza — Senior AI Systems Engineer`,
    initial_draft: `Hi, I saw your post looking for a RAG pipeline with hybrid search. I have worked on RAG pipelines before using LangChain and Qdrant. I can help build your BM25 and cross-encoder search. Let me know if you would like to discuss!`,
    revised_draft: `Hi HealthTech Innovations Team,

Your requirement for a HIPAA-grade hybrid RAG system with sub-250ms p95 latency maps directly to production architectures I have deployed. 

In a recent enterprise engagement ([CS-AI-01: FinTech Compliance RAG]), I engineered a dual-retriever hybrid pipeline pairing BM25Okapi keyword lexical matching with dense cosine embeddings and reciprocal rank fusion (RRF). That system achieved a +28% bump in Recall@5 over dense-only retrieval while keeping p95 latency under 110ms on a 500k document corpus.

Here is how I will architect your healthcare pipeline:
1. Retrieval Engine: Qdrant dense vector store with BAAI/bge-m3 embeddings combined with BM25 Okapi lexical scoring via rank-bm25, unified with Reciprocal Rank Fusion (k=60).
2. Re-Ranking & Precision: Cross-encoder (bge-reranker-large) applied over the top 25 candidate chunks, compressing to the top 5 most relevant passages.
3. Factuality & Guardrails: Decontextualized atomic claim splitting and NLI entailment scoring ([CS-AI-04]) to catch hallucinations before LLM generation reaches clinical users.
4. Infrastructure: Containerized FastAPI async endpoints with OpenTelemetry tracing and comprehensive PyTest evals.

I can deliver the end-to-end working pipeline with automated evals in 14 days. I would be glad to share an architecture walkthrough.

Best regards,
Hamza — Senior AI Systems Engineer`,
    bid_amount: 4000,
    estimated_hours: 50,
    turnaround_days: 14,
    critic_review: {
      specificity_score: 9.4,
      evidence_groundedness_score: 9.6,
      client_alignment_score: 9.5,
      overall_score: 9.5,
      comments: [
        "Strong opening sentence addressing specific latency (<250ms) and HIPAA constraints.",
        "Grounding citations [CS-AI-01] and [CS-AI-04] are concrete with quantitative metrics (+28% recall, <110ms latency).",
        "Clear 4-step architectural roadmap matches all required deliverables."
      ],
      suggestions: [
        "Include brief note on containerization or local deployment readiness."
      ]
    },
    compliance_check: {
      passed: true,
      violations: [],
      no_off_platform_contact: true,
      no_unpaid_free_work: true,
      no_credential_sharing: true
    },
    cited_evidence: [
      {
        id: "CS-AI-01",
        source: "data/personas/ai_engineer/case_studies/cs_01_hybrid_rag.md",
        title: "Sub-100ms Multimodal Hybrid RAG for FinTech Compliance",
        excerpt: "Engineered hybrid BM25 + dense vector search pipeline with custom reciprocal rank fusion yielding +28% Recall@5 over baseline.",
        metrics: ["+28% Recall@5", "<110ms p95 latency", "500k chunks indexed"],
        similarity_score: 0.94
      },
      {
        id: "CS-AI-04",
        source: "data/personas/ai_engineer/case_studies/cs_04_eval_verifier.md",
        title: "Automated Evidence Verifier & Calibrated LLM Judge",
        excerpt: "Implemented decontextualized atomic claim splitting and NLI entailment scoring reaching 92% hallucination suppression.",
        metrics: ["92% hallucination suppression", "Kappa 0.866 calibration", "45ms verifier overhead"],
        similarity_score: 0.91
      }
    ],
    status: "drafted",
    connects_used: 16,
    created_at: "Just now",
    updated_at: "Just now"
  }
];

export const INITIAL_MESSAGES: MessageThread[] = [
  {
    id: "thread-01",
    job_id: "job-ai-101",
    job_title: "Production RAG Pipeline with Hybrid Search",
    client_name: "Dr. Eleanor Vance (HealthTech)",
    intent: "interview_invite",
    unread: true,
    messages: [
      {
        id: "msg-01",
        sender: "client",
        text: "Hi Hamza, your proposal on the hybrid RAG architecture and atomic claim verification is exactly what we need. Could you hop on a 20-minute intro call tomorrow to discuss HIPAA audit logging and timeline?",
        timestamp: "Today at 2:15 PM"
      }
    ],
    suggested_reply: "Hi Dr. Vance, thank you for reaching out! I would be delighted to connect. I have put a hold on my calendar for our 20-minute intro call. Looking forward to walking you through the HIPAA audit logging pipeline.",
    available_slots: [
      "Tomorrow, 2:00 PM – 2:30 PM EST",
      "Tomorrow, 4:30 PM – 5:00 PM EST",
      "Thursday, 11:00 AM – 11:30 AM EST"
    ],
    booked_slot: undefined
  },
  {
    id: "thread-02",
    job_id: "job-ai-103",
    job_title: "Multi-Agent System for Autonomous Market Research",
    client_name: "Marcus Sterling (Apex Strategic)",
    intent: "scope_question",
    unread: false,
    messages: [
      {
        id: "msg-02",
        sender: "client",
        text: "Thanks for submitting Hamza. How do you plan to handle rate limits if SEC EDGAR filings throttle our crawler agent?",
        timestamp: "Yesterday at 6:40 PM"
      },
      {
        id: "msg-03",
        sender: "agent",
        text: "Hi Marcus, we handle SEC rate limits (10 req/sec) using an async token bucket rate limiter with exponential jittered backoff and local disk cache. If a 429 response is received, the crawler pauses and safely checkpoints state.",
        timestamp: "Yesterday at 7:02 PM"
      }
    ],
    suggested_reply: "I can also provide a small demo test runner verifying our SEC rate-limit backoff logic if you'd like to inspect it before kicking off.",
  }
];

export const INITIAL_RUNS: AgentRun[] = [
  {
    run_id: "run-9842",
    job_id: "job-ai-101",
    job_title: "Production RAG Pipeline with Hybrid Search",
    started_at: "2 minutes ago",
    status: "interrupted",
    trace_id: "tr-gigbid-8891-langsmith",
    current_node: "human_approval",
    nodes: [
      {
        node_name: "scout",
        status: "completed",
        started_at: "14:10:01",
        completed_at: "14:10:03",
        latency_ms: 1840,
        tokens_used: 120,
        cost_usd: 0.0003,
        output_summary: { matches_found: 4, top_match: "job-ai-101", filter: "fit_score >= 80" }
      },
      {
        node_name: "analyst",
        status: "completed",
        started_at: "14:10:03",
        completed_at: "14:10:05",
        latency_ms: 2100,
        tokens_used: 480,
        cost_usd: 0.0012,
        output_summary: { deliverables_count: 4, budget_tier: "enterprise", complexity: "high" }
      },
      {
        node_name: "risk_assessor",
        status: "completed",
        started_at: "14:10:03",
        completed_at: "14:10:04",
        latency_ms: 1620,
        tokens_used: 350,
        cost_usd: 0.0008,
        output_summary: { scam_score: 0.02, risk_level: "safe", red_flags_count: 0 }
      },
      {
        node_name: "fit_matcher",
        status: "completed",
        started_at: "14:10:03",
        completed_at: "14:10:05",
        latency_ms: 2010,
        tokens_used: 510,
        cost_usd: 0.0013,
        output_summary: { fit_score: 96, matched_case_studies: ["CS-AI-01", "CS-AI-04"] }
      },
      {
        node_name: "pricing",
        status: "completed",
        started_at: "14:10:05",
        completed_at: "14:10:06",
        latency_ms: 1100,
        tokens_used: 280,
        cost_usd: 0.0007,
        output_summary: { recommended_bid: 4000, model: "fixed", est_hours: 50, rate: 80 }
      },
      {
        node_name: "writer",
        status: "completed",
        started_at: "14:10:06",
        completed_at: "14:10:09",
        latency_ms: 2950,
        tokens_used: 820,
        cost_usd: 0.0025,
        output_summary: { draft_words: 245, citations_embedded: 2 }
      },
      {
        node_name: "verifier",
        status: "completed",
        started_at: "14:10:09",
        completed_at: "14:10:10",
        latency_ms: 1350,
        tokens_used: 390,
        cost_usd: 0.0010,
        output_summary: { atomic_claims: 6, supported_claims: 6, entailment_score: 0.95 }
      },
      {
        node_name: "critic",
        status: "completed",
        started_at: "14:10:10",
        completed_at: "14:10:12",
        latency_ms: 2200,
        tokens_used: 610,
        cost_usd: 0.0018,
        output_summary: { overall_score: 9.5, loops_completed: 1, action: "pass_to_compliance" }
      },
      {
        node_name: "compliance",
        status: "completed",
        started_at: "14:10:12",
        completed_at: "14:10:13",
        latency_ms: 980,
        tokens_used: 240,
        cost_usd: 0.0006,
        output_summary: { off_platform_contact: false, free_work: false, approved: true }
      },
      {
        node_name: "human_approval",
        status: "interrupted",
        started_at: "14:10:13",
        output_summary: { state: "awaiting_human_decision", requires_connects: 16 }
      }
    ]
  }
];

export const INITIAL_RULES: MemoryRule[] = [
  {
    id: "rule-mem-01",
    source_proposal_id: "prop-ai-089",
    rule_text: "Always emphasize sub-100ms latency benchmarks and test coverage when client mentions enterprise or production scale.",
    confidence: 0.92,
    created_at: "Yesterday",
    category: "tone"
  },
  {
    id: "rule-mem-02",
    source_proposal_id: "prop-ai-072",
    rule_text: "Never bid below $75/hr floor for AI Engineer persona even if client budget suggests $50-$60 range.",
    confidence: 0.98,
    created_at: "3 days ago",
    category: "pricing"
  },
  {
    id: "rule-mem-03",
    source_proposal_id: "prop-ai-061",
    rule_text: "Quote fixed milestone breakdown with 3 to 4 distinct deliverables rather than a monolithic single deliverable.",
    confidence: 0.88,
    created_at: "5 days ago",
    category: "portfolio"
  }
];

export const INITIAL_ANALYTICS: AnalyticsSummary = {
  proposals_sent: 42,
  won_count: 14,
  replied_count: 24,
  interview_count: 18,
  hired_count: 12,
  reply_rate: 57.1,
  hire_rate: 28.6,
  connects_spent: 672,
  connects_roi: 48.2,
  total_revenue_usd: 32400,
  avg_latency_seconds: 14.8,
  avg_cost_per_bid_usd: 0.012,
  outcomes_breakdown: {
    "Won": 14,
    "Replied": 10,
    "Ignored": 12,
    "Lost": 6
  }
};

