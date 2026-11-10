# GigBid MCP Tool Inventory

Every capability in GigBid is exposed strictly as a Model Context Protocol (MCP) tool with typed Pydantic schemas, declared input/output constraints, idempotency enforcement, and client-level access control allowlists.

## Tool Registry

| Tool Name | Server | Access Type | Annotations | Authentication & Security | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `search_evidence` | Portfolio | Read-only | `readOnlyHint=true`, `destructiveHint=false`, `idempotentHint=true` | In-memory / Bearer Token | Search verified portfolio case studies, repositories, and past proposals by requirement or skill. |
| `get_case_study` | Portfolio | Read-only | `readOnlyHint=true`, `destructiveHint=false`, `idempotentHint=true` | In-memory / Bearer Token | Retrieve complete text, architecture, and outcomes of a verified case study by evidence ID. |
| `list_skills` | Portfolio | Read-only | `readOnlyHint=true`, `destructiveHint=false`, `idempotentHint=true` | In-memory / Bearer Token | List all verified skills and technical competencies backed by evidence in the freelancer profile. |
| `search_jobs` | Marketplace | Read-only | `readOnlyHint=true`, `destructiveHint=false`, `idempotentHint=true` | Bearer Token / Per-user Rate Limiter | Search active jobs with query keywords, category, and budget range filters. |
| `get_job` | Marketplace | Read-only | `readOnlyHint=true`, `destructiveHint=false`, `idempotentHint=true` | Bearer Token / Per-user Rate Limiter | Retrieve complete job specification, screening questions, Connects cost, and warning flags. |
| `get_client_history` | Marketplace | Read-only | `readOnlyHint=true`, `destructiveHint=false`, `idempotentHint=true` | Bearer Token / Per-user Rate Limiter | Retrieve client hiring history, total spend, rating, and payment verification status. |
| `get_connects_balance` | Marketplace | Read-only | `readOnlyHint=true`, `destructiveHint=false`, `idempotentHint=true` | Bearer Token / Per-user Rate Limiter | Check current account Connects balance. |
| `list_messages` | Marketplace | Read-only | `readOnlyHint=true`, `destructiveHint=false`, `idempotentHint=true` | Bearer Token / Per-user Rate Limiter | List conversation messages and client replies in a thread. |
| `create_proposal_draft` | Marketplace | Write | `readOnlyHint=false`, `destructiveHint=false`, `idempotentHint=true` | Bearer Token / Idempotency Key / Audit Log | Create an internal proposal draft for a job before user review. Idempotent and non-destructive. |
| `submit_proposal` | Marketplace | Write | `readOnlyHint=false`, `destructiveHint=true`, `idempotentHint=true` | Bearer Token / Idempotency Key / Audit Log | Submit an approved proposal to the marketplace. Destructive (spends Connects). Supports `dry_run` preview. |
| `send_message` | Marketplace | Write | `readOnlyHint=false`, `destructiveHint=true`, `idempotentHint=true` | Bearer Token / Idempotency Key / Audit Log | Send a message or interview availability to a client thread. Destructive and idempotent. |
| `get_calendar_availability` | Workspace | Read-only | `readOnlyHint=true`, `destructiveHint=false`, `idempotentHint=true` | OAuth2 / Local Mock | Find upcoming free interview slots in the freelancer's calendar. |
| `create_interview_hold` | Workspace | Write | `readOnlyHint=false`, `destructiveHint=false`, `idempotentHint=true` | OAuth2 / Local Mock | Place a tentative interview hold on the calendar for a client conversation. |
| `create_email_draft` | Workspace | Write | `readOnlyHint=false`, `destructiveHint=false`, `idempotentHint=true` | OAuth2 / Local Mock | Create an email draft in Gmail / workspace client for client correspondence. |
| `ingest_repo_artifacts` | GitHub (3rd party) | Read-only | `readOnlyHint=true`, `destructiveHint=false`, `idempotentHint=true` | GitHub Fine-grained PAT | Ingests public repositories, code snippets, and README files into verified portfolio case studies. |

## Third-Party MCP Servers Trust Rationale

1. **Official Upwork MCP Server (`https://mcp.upwork.com/mcp`)**:  
   *Trust Rationale*: Built, signed, and maintained directly by Upwork Engineering with OAuth 2.1 authentication and platform rate limits; trusted because it guarantees platform terms compliance, never exposes session credentials, and enforces human-in-the-loop confirmation on the platform for all contract/payment writes.
2. **GitHub MCP Server (`github.com/modelcontextprotocol/servers/tree/main/src/github`)**:  
   *Trust Rationale*: Officially sanctioned by the Model Context Protocol core repository; scoped with read-only personal access tokens (PAT) for developer portfolio repositories, ensuring no write or administrative permissions on the user's GitHub account.

## Client Discipline & Agent Tool Allowlists
To prevent tool pollution and hallucinations, each LangGraph agent role receives an explicit subset of tools:
- **Scout**: `search_jobs`, `get_job`
- **Job Analyst**: Pure reasoning (no external MCP tools)
- **Risk Assessor**: `get_client_history`, `get_job`
- **Fit Matcher**: `search_evidence`, `get_case_study`, `list_skills`
- **Pricing Strategist**: `get_client_history`, `get_connects_balance`
- **Proposal Writer**: `search_evidence`, `get_case_study`
- **Critic**: `search_evidence`, `get_case_study`
- **Compliance Guard**: Pure policy pack validation (no MCP tools)
- **Client Liaison**: `list_messages`, `send_message`, `get_calendar_availability`, `create_interview_hold`, `create_email_draft`
