# GigBid Operational Runbook & Production Incident Playbook

**System Name**: GigBid — Multi-Agent Freelancer Copilot  
**Author**: Hamza ([@CtrlAltHamza](https://github.com/CtrlAltHamza))  
**Target Environment**: Production (Docker Compose / Cloud Container / Hybrid)  
**Last Updated**: November 2026

---

## 1. System Topology & Architecture

```
[ Freelancer / Browser (Port 3000) ]
                 |
                 v  (Reverse Proxy / SSE Buffering Off)
        [ Nginx Web Container ]
                 |
                 v  (/api/* Proxy)
        [ FastAPI Backend Service (Port 8000) ]
        /        |               \             \
       v         v                v             v
[Portfolio MCP] [Marketplace MCP] [Workspace MCP] [PostgreSQL / SQLite]
                  /            \
                 v              v
        [GigSim Simulator]  [Upwork Live Adapter]
           (Port 8001)         (OAuth2 / REST)
```

### Components
1. **Frontend (`web`)**: Vite + React 19 + TypeScript + Tailwind CSS with SPA fallback.
2. **Backend API (`api`)**: FastAPI async ASGI server providing REST and SSE endpoints.
3. **Multi-Agent Orchestrator (`agent`)**: LangGraph state graph with parallel fan-out, Bounded Critic loop ($\le 2$ cycles), and human-in-the-loop `interrupt()`.
4. **Tool Layer (`mcp_servers`)**:
   - `Portfolio MCP`: FastMCP server exposing CV, case studies, repos, and reviews.
   - `Marketplace MCP`: FastMCP server with idempotency keys, dry-run mode, and audit logging.
   - `Workspace MCP`: FastMCP server managing calendar slot holds and proposal drafts.
5. **Simulator (`gigsim`)**: Deterministic marketplace simulator with 60 open jobs, 30 clients, and 1,500 historical jobs.
6. **Background Worker (`worker`)**: Async periodic scheduler for marketplace scouting, client message polling, and pipeline synchronization.

---

## 2. Bootstrapping & Deployment

### Quick Start with Docker Compose
```bash
# 1. Clone repository
git clone https://github.com/CtrlAltHamza/gigbid.git
cd gigbid

# 2. Configure environment
cp .env.example .env

# 3. Launch full stack
docker compose -f infra/docker-compose.yml up -d --build

# 4. Verify service health
docker compose -f infra/docker-compose.yml ps
```

### Local Development Startup
```bash
# Terminal 1: GigSim Simulator
uvicorn gigsim.app:app --port 8001 --reload

# Terminal 2: FastAPI Backend
uvicorn apps.api.main:app --port 8000 --reload

# Terminal 3: Background Worker
python -m worker

# Terminal 4: Frontend Development Server
cd apps/web && npm run dev
```

---

## 3. Marketplace Rate Limiting & Quota Management

Upwork GraphQL and REST endpoints enforce strict rate limits:
- **Scout search**: 40 requests / minute.
- **Proposal submission**: 10 submissions / hour.
- **Client messaging**: 60 messages / minute.

### Enforcement Strategy
- **Token Bucket Limiter**: Implemented in `mcp_servers/marketplace/server.py`.
- **Jittered Exponential Backoff**: When HTTP 429 is encountered, requests are retried with formula:
  $$T_{\text{wait}} = \min(60, 2^{\text{attempt}} \times 1.5 + \text{random}(0, 1))$$
- **Maximum Retries**: Bounded to 3 attempts. Upon third failure, degraded mode is activated.

---

## 4. Degraded Mode & Fault Tolerance

If the live marketplace adapter fails (network partition, Upwork maintenance, or quota exhaustion):
1. **Automatic Detection**: `agent/mcp_client.py` catches `MarketplaceConnectionError` or HTTP 429/503.
2. **Seamless Fallback**: MultiServerMCPClient switches the active marketplace adapter from `UpworkLiveAdapter` to `GigSimAdapter`.
3. **Operator Notification**: The API emits an SSE warning event, triggering the amber Degraded Mode banner on all connected web clients.
4. **Zero Downtime**: Job scouting, requirement-to-evidence matching, and draft authoring continue uninterrupted against local synthetic seed data.
5. **Self-Healing**: A background healthcheck probes Upwork `/api/v3/status` every 60 seconds. Once 3 consecutive health probes succeed, the client automatically restores live mode.

---

## 5. Security & Incident Response Playbooks

### Incident A: Prompt Injection Attempt Detected
*Symptom*: Risk Assessor reports injection pattern or `scan_for_injection` returns `True`.
1. Job is immediately tagged with status `scam_blocked`.
2. Drafting action is locked.
3. Incident logged to `logs/audit_log.jsonl` with hash of suspicious content.
4. No Connects are expended.

### Incident B: Connects Budget Depletion Alert
*Symptom*: User hits max daily Connects limit (default: 40 connects/day).
1. `human_approval` node blocks submission even if confidence exceeds threshold.
2. Toast warning displayed in web interface: `"Daily Connects ceiling reached"`.
3. To override: Navigate to **Settings & Memory**, adjust slider or approve manually.

### Incident C: Corrupted Memory Store Heuristics
*Symptom*: Agent applies an overfitted or conflicting rule to drafts.
1. Navigate to **Settings & Memory** $\rightarrow$ **Learned Heuristics in Memory Store**.
2. Locate the rule by ID or keyword.
3. Click the **Trash** icon to revoke and purge from SQLite memory store.
4. The rule is immediately expunged from the dynamic prompt context.

---

## 6. Secrets & Cryptographic Key Management

- **API Keys**: Stored in `.env` (never committed to git).
- **Session Tokens**: Encrypted using Fernet symmetric encryption (`cryptography.fernet`) with `SECRET_KEY`.
- **Key Rotation Procedure**:
  ```bash
  python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
  ```
  Update `GIGBID_ENCRYPTION_KEY` in environment and restart backend service.
