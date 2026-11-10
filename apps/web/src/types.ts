export type PersonaType = 'ai_engineer' | 'fullstack_dev' | 'data_analyst';

export type AutonomyLevel = 'scout_only' | 'draft_and_ask' | 'full_auto';

export type JobStatus = 'new' | 'auto_drafted' | 'dismissed' | 'clarification_needed' | 'scam_blocked';

export type RiskLevel = 'safe' | 'medium' | 'suspicious' | 'scam';

export interface EvidenceItem {
  id: string;
  source: string;
  title: string;
  excerpt: string;
  metrics: string[];
  similarity_score: number;
}

export interface RequirementMatch {
  requirement: string;
  matched_skill: string;
  evidence_id: string;
  evidence_title: string;
  excerpt: string;
  score: number;
}

export interface Job {
  id: string;
  title: string;
  client: string;
  platform: string;
  budget_type: 'fixed' | 'hourly';
  budget_min: number;
  budget_max: number;
  hourly_rate?: number;
  fit_score: number;
  risk_level: RiskLevel;
  scam_score: number;
  scam_reasoning?: string;
  red_flags: string[];
  status: JobStatus;
  description: string;
  deliverables: string[];
  scope: string;
  skills: string[];
  pricing_rationale: string;
  requirement_matches: RequirementMatch[];
  created_at: string;
  connects_cost: number;
}

export interface CriticReview {
  specificity_score: number;
  evidence_groundedness_score: number;
  client_alignment_score: number;
  overall_score: number;
  comments: string[];
  suggestions: string[];
}

export interface ComplianceCheck {
  passed: boolean;
  violations: string[];
  no_off_platform_contact: boolean;
  no_unpaid_free_work: boolean;
  no_credential_sharing: boolean;
}

export interface Proposal {
  id: string;
  job_id: string;
  job_title: string;
  client: string;
  persona: PersonaType;
  draft_content: string;
  initial_draft?: string;
  revised_draft?: string;
  bid_amount: number;
  estimated_hours: number;
  turnaround_days: number;
  critic_review: CriticReview;
  compliance_check: ComplianceCheck;
  cited_evidence: EvidenceItem[];
  status: 'drafted' | 'submitted' | 'viewed' | 'replied' | 'interview' | 'hired' | 'lost';
  connects_used: number;
  created_at: string;
  updated_at: string;
  feedback?: string;
}

export interface MessageThread {
  id: string;
  job_id: string;
  job_title: string;
  client_name: string;
  client_avatar?: string;
  intent: 'interview_invite' | 'scope_question' | 'price_negotiation' | 'scam_offplatform';
  unread: boolean;
  messages: {
    id: string;
    sender: 'client' | 'agent' | 'user';
    text: string;
    timestamp: string;
  }[];
  suggested_reply: string;
  available_slots?: string[];
  booked_slot?: string;
}

export interface AgentNodeRun {
  node_name: string;
  status: 'pending' | 'running' | 'completed' | 'interrupted' | 'failed';
  started_at: string;
  completed_at?: string;
  latency_ms?: number;
  input_summary?: Record<string, any>;
  output_summary?: Record<string, any>;
  tokens_used?: number;
  cost_usd?: number;
}

export interface AgentRun {
  run_id: string;
  job_id: string;
  job_title: string;
  started_at: string;
  status: 'running' | 'completed' | 'interrupted' | 'failed';
  nodes: AgentNodeRun[];
  current_node?: string;
  trace_id: string;
}

export interface MemoryRule {
  id: string;
  source_proposal_id: string;
  rule_text: string;
  confidence: number;
  created_at: string;
  category: 'pricing' | 'tone' | 'compliance' | 'portfolio';
}

export interface UserSettings {
  persona: PersonaType;
  autonomy_level: AutonomyLevel;
  hourly_rate_floor: number;
  max_daily_connects: number;
  connects_balance: number;
  degraded_mode_simulated: boolean;
  min_client_rating: number;
  auto_submit_confidence_threshold: number;
}

export interface AnalyticsSummary {
  proposals_sent: number;
  won_count: number;
  replied_count: number;
  interview_count: number;
  hired_count: number;
  reply_rate: number;
  hire_rate: number;
  connects_spent: number;
  connects_roi: number;
  total_revenue_usd: number;
  avg_latency_seconds: number;
  avg_cost_per_bid_usd: number;
  outcomes_breakdown: Record<string, number>;
}

