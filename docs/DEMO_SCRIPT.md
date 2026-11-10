# GigBid: 3-Minute Demo Video Script & Production Storyboard

**Title**: GigBid — Autonomous Multi-Agent Freelancer Copilot  
**Presenter**: Hamza ([@CtrlAltHamza](https://github.com/CtrlAltHamza))  
**Target Duration**: Exactly 180 seconds (3:00)  
**Resolution**: 1080p 60fps, Dark Theme UI  
**Live URL**: `http://localhost:3000` (or deployed staging URL)

---

## Storyboard Timeline & Voiceover Script

### [0:00 - 0:25] Scene 1: The Problem & Onboarding Profile Setup
- **Visual Cue**: Open browser on `http://localhost:3000`. Landing on the **Onboarding & Profile** view. Three persona cards visible (`AI Engineer`, `Full-Stack Dev`, `Data Analyst`).
- **Screen Action**: Click `AI & LLM Engineer` persona card. Show that 20 case studies and hourly floor ($75/hr) are loaded. Click *"Launch Copilot Workspace"*.
- **Voiceover**:
  > *"Every freelance software engineer knows the struggle: Upwork Connects cost real money, clients ignore generic template proposals, and winning bids requires responding within 15 minutes with deep technical proof. Welcome to GigBid—an autonomous multi-agent copilot that turns your actual GitHub repositories and case studies into high-converting, verified proposals. Let's begin by selecting our AI Engineer persona and launching the workspace."*

---

### [0:25 - 0:55] Scene 2: Job Inbox & Real-Time Scam Defense
- **Visual Cue**: Transition to **Job Inbox**. Ranked list of marketplace postings is displayed with match fit badges, risk scores, and platform tags.
- **Screen Action**: 
  1. Hover over the top-ranked job: *"Production RAG Pipeline with Hybrid Search"* (Fit: 96%, Risk: Safe).
  2. Scroll down to show the red flagged job: *"URGENT: Crypto Trading Telegram Bot — Send WhatsApp deposit"*. Point out the `SCAM DETECTED (98%)` badge and `BLOCKED — Off-Platform Fraud` tag.
  3. Show that the *Generate Draft* button is disabled with a tooltip explaining the WhatsApp off-platform violation.
- **Voiceover**:
  > *"Our Scout agent continuously monitors the marketplace, ranking opportunities using our multi-agent fit matcher. Notice how our Risk Assessor immediately flagged and blocked this crypto bot posting. The client demanded an upfront deposit via WhatsApp—an immediate violation of platform escrow. GigBid automatically locks the drafting pipeline, preventing accidental Connects waste."*

---

### [0:55 - 1:25] Scene 3: Job Detail & Requirement-to-Evidence Grounding Matrix
- **Visual Cue**: Click *"Inspect Job"* on the Healthcare RAG opportunity to open **Job Detail View**.
- **Screen Action**:
  1. Scroll through the structured `JobSpec`: Deliverables, Tech Stack, Budget ($4,000 Fixed), and Pricing Engine rationale.
  2. Highlight the **Requirement-to-Evidence Grounding Matrix**: show the table linking client requirements to past case studies (`CS-AI-01: Sub-100ms Multimodal Hybrid RAG`) with similarity scores (94%).
  3. Click the top-right button: *"Open in Proposal Studio"*.
- **Voiceover**:
  > *"Opening the job detail reveals the structured JobSpec extracted by our Analyst node. Beneath it lies the heart of our grounding system: the Requirement-to-Evidence Matrix. Instead of guessing, GigBid’s hybrid BM25 and dense retriever maps each client requirement to our AST-verified portfolio case studies, complete with similarity metrics. Let’s jump into Proposal Studio."*

---

### [1:25 - 1:55] Scene 4: Proposal Studio — Grounding Hover, Inline Critic & Human Approval
- **Visual Cue**: Arrive at **Proposal Studio**. Left: Proposal editor. Right: Critic rubric scores and dry-run Connects preview.
- **Screen Action**:
  1. Hover over the citation badge `[CS-AI-01]` in the proposal text. An interactive tooltip popover appears with the verified excerpt and metrics (`+28% Recall@5`, `<110ms latency`).
  2. Toggle *"Compare Revisions"*: show side-by-side visual diff between the generic initial draft and the grounded Critic-revised proposal.
  3. Point out the Critic score (9.5/10) and Compliance checks (all PASSED).
  4. Show Connects balance (150). Click *"Approve & Submit"*. Watch Connects balance deduct to 134, and status badge update to *"Submitted"*.
- **Voiceover**:
  > *"In Proposal Studio, every factual claim is grounded. Hovering over citation [CS-AI-01] reveals the exact case study excerpt and latency benchmarks. Clicking 'Compare Revisions' displays the visual diff after two bounded critique cycles. Our Compliance guardrail certifies zero off-platform contact. LangGraph suspended execution at a human interrupt gate; once I click 'Approve & Submit', 16 Connects are deducted, and the bid is dispatched."*

---

### [1:55 - 2:20] Scene 5: Pipeline Kanban & Client Messages with Workspace MCP
- **Visual Cue**: Switch to **Pipeline Board**, then click **Client Messages**.
- **Screen Action**:
  1. On the Kanban board, show proposal cards moving from *Submitted* to *Interview*.
  2. Switch to *Client Messages*. Open thread with *"Dr. Eleanor Vance (HealthTech)"*. Point out the `Interview Invite` intent tag.
  3. In the message timeline, display the **Workspace MCP Calendar Hold Availability** widget.
  4. Click *"Slot 1: Tomorrow, 2:00 PM EST"*. Show the status change to *"Hold Confirmed"* and calendar invite dispatched.
- **Voiceover**:
  > *"On the Pipeline board, we track contract progression. In Client Messages, when Dr. Vance reaches out for an intro call, our Conversation Graph classifies the intent as an Interview Invite. Powered by our Workspace MCP server, GigBid checks our calendar availability and provides one-click slot holds without leaving the app."*

---

### [2:20 - 2:45] Scene 6: Live Agent Run Viewer & Memory Store Heuristics
- **Visual Cue**: Navigate to **Agent Runs**, then **Settings & Memory**.
- **Screen Action**:
  1. On *Agent Run Viewer*, show the live LangGraph execution DAG (`Scout -> Analyst -> [Parallel Fan-Out] -> Pricing -> Writer -> Verifier -> Critic -> Compliance -> Human Approval`).
  2. Click the `critic` node to inspect latency (2.2s), token usage (610 tokens), and output payload. Show the LangSmith trace link.
  3. Navigate to *Settings & Memory*. Show the learned heuristics table. Show the rule: *"Never bid below $75/hr floor for AI Engineer persona"*. Click the trash icon to demonstrate immediate rule revocation.
- **Voiceover**:
  > *"For full operational transparency, the Agent Run Viewer streams each LangGraph superstep in real-time via Server-Sent Events. We can inspect input/output payloads, latencies, and token costs for every single agent. In Settings, our Memory Store allows freelancers to inspect, test, or revoke learned rules distilled from past feedback."*

---

### [2:45 - 3:00] Scene 7: Summary & Closing
- **Visual Cue**: Switch to **Analytics ROI Dashboard**, showing $32,400 won, 57.1% reply rate, and 48.2× Connects ROI.
- **Screen Action**: Pan across the conversion distribution chart and system speed metrics.
- **Voiceover**:
  > *"With Model Context Protocol privilege separation, atomic claim verification, and LangGraph human-in-the-loop control, GigBid transforms freelance engineering into an intelligent, high-ROI business. All source code, Docker configs, and evaluations are open on GitHub. Thank you!"*

---

## Production Recording Checklist
- [x] Backend running on `http://localhost:8000` with mock seed data loaded.
- [x] Frontend compiled and running on `http://localhost:3000`.
- [x] Clean browser profile with dark mode enabled.
- [x] Audio track: Noise-suppressed condenser mic with clear articulation.
- [x] Export format: MP4 1080p H.264 with AAC audio, duration exactly 3 minutes.
