# ADR 0001: Multi-Server MCP Tool Layer with Strict Privilege Separation

## Status
Accepted

## Context
A freelancer copilot requires access to three distinct functional domains:
1. Confidential freelancer identity (CV, private past client reviews, case studies).
2. Public marketplace operations (scouting jobs, submitting proposals, reading client history).
3. Workspace productivity (calendar slot holds, email drafting).

Monolithic agent tooling risks security cross-contamination: an untrusted marketplace job description containing a prompt injection could attempt to trick the agent into deleting calendar holds or exfiltrating client reviews.

## Decision
We adopt the **Model Context Protocol (MCP)** specification via FastMCP:
1. Divide tooling into three independent servers:
   - `Portfolio MCP Server`: Read-only access to persona assets.
   - `Marketplace MCP Server`: Stateful operations with dry-run flags, idempotency keys, and token-bucket rate limits.
   - `Workspace MCP Server`: Scheduling and calendar holds.
2. Implement `MultiServerMCPClient` in the agent layer with strict per-node tool allowlists. For instance, the `Risk Assessor` node only has access to marketplace read tools, while `Compliance` only has access to validation tools.

## Consequences
- **Positive**: Strict least-privilege security boundaries; independent testing and packaging; standalone deployment readiness via `uvx`.
- **Negative**: Marginal IPC overhead across stdio pipes, mitigated by local fast process initialization.

