# ADR 0004: Three-Tier Memory Architecture with Self-Correcting Rule Promotion

## Status
Accepted

## Context
Freelancers possess nuanced, personalized bidding preferences (e.g., minimum hourly rates, preferred tone, technical frameworks to highlight, terms to avoid). If an AI copilot operates solely on static prompt templates, users are forced to repeatedly correct the same issues. Conversely, naive appending of conversation history into prompts results in prompt bloat, context dilution, and potential contradiction.

## Decision
We implement a three-tier memory architecture with deterministic promotion rules:
1. **Working Memory (State Graph)**: Ephemeral state tracking current job specification, parallel reports, handoffs, and execution traces. Cleared upon run completion.
2. **Style & User Preference Memory**: Fast-lookup key-value store for user stylistic overrides (e.g., concise vs. detailed greetings, preferred signature).
3. **Durable Heuristic Memory Store**:
   - When a proposal is rejected by the user with feedback, the system distills the feedback into a structured negative rule.
   - When a proposal receives an interview invite or is marked "Won", successful framing patterns are extracted as positive rules.
   - Rules are promoted with a confidence score and category (`pricing`, `tone`, `compliance`, `portfolio`).
   - The user can inspect, test, and delete any rule from the Web UI Settings tab.
   - Top-ranked rules are dynamically injected into the `Writer` and `Critic` system prompts.

## Consequences
- **Positive**: Continuous, transparent self-improvement; user maintains full auditability and veto power over learned rules; no prompt bloat.
- **Negative**: Requires structured distillation prompts to extract clean, generalized rules from raw rejection comments.
