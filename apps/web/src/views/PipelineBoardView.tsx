import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { 
  Kanban, 
  DollarSign, 
  User, 
  ArrowRight, 
  Clock, 
  Filter, 
  CheckCircle, 
  ChevronRight,
  MoreVertical
} from 'lucide-react';
import { Proposal } from '../types';

type PipelineStage = 'drafted' | 'submitted' | 'viewed' | 'replied' | 'interview' | 'hired' | 'lost';

const STAGES: { id: PipelineStage; label: string; color: string; badge: string }[] = [
  { id: 'drafted', label: 'Drafted', color: 'border-slate-700 bg-slate-900/50', badge: 'bg-slate-700 text-slate-300' },
  { id: 'submitted', label: 'Submitted', color: 'border-blue-900/60 bg-blue-950/20', badge: 'bg-blue-500/20 text-blue-300' },
  { id: 'viewed', label: 'Viewed', color: 'border-purple-900/60 bg-purple-950/20', badge: 'bg-purple-500/20 text-purple-300' },
  { id: 'replied', label: 'Replied', color: 'border-indigo-900/60 bg-indigo-950/20', badge: 'bg-indigo-500/20 text-indigo-300' },
  { id: 'interview', label: 'Interview', color: 'border-amber-900/60 bg-amber-950/20', badge: 'bg-amber-500/20 text-amber-300' },
  { id: 'hired', label: 'Hired (Won)', color: 'border-emerald-900/60 bg-emerald-950/20', badge: 'bg-emerald-500/20 text-emerald-300' },
  { id: 'lost', label: 'Lost / Closed', color: 'border-rose-900/60 bg-rose-950/20', badge: 'bg-rose-500/20 text-rose-300' },
];

export const PipelineBoardView: React.FC = () => {
  const { proposals, openProposalStudio } = useApp();
  const [filterPersona, setFilterPersona] = useState<string>('all');

  // Local state for moving cards around in pipeline
  const [pipelineProposals, setPipelineProposals] = useState<Proposal[]>([
    ...proposals,
    {
      id: "prop-ai-099",
      job_id: "job-ai-099",
      job_title: "FastAPI + Qdrant Semantic Search Service",
      client: "BioData Core",
      persona: "ai_engineer",
      draft_content: "Delivered sub-50ms vector query service...",
      bid_amount: 3200,
      estimated_hours: 40,
      turnaround_days: 10,
      critic_review: { specificity_score: 9, evidence_groundedness_score: 9.2, client_alignment_score: 9.1, overall_score: 9.1, comments: [], suggestions: [] },
      compliance_check: { passed: true, violations: [], no_off_platform_contact: true, no_unpaid_free_work: true, no_credential_sharing: true },
      cited_evidence: [],
      status: "replied",
      connects_used: 16,
      created_at: "Yesterday",
      updated_at: "Yesterday"
    },
    {
      id: "prop-ai-098",
      job_id: "job-ai-098",
      job_title: "Enterprise Agentic Workflow with LangGraph Checkpoints",
      client: "FinLeap Capital",
      persona: "ai_engineer",
      draft_content: "Architected multi-agent graph with PostgreSQL persistence...",
      bid_amount: 5500,
      estimated_hours: 60,
      turnaround_days: 21,
      critic_review: { specificity_score: 9.5, evidence_groundedness_score: 9.8, client_alignment_score: 9.6, overall_score: 9.6, comments: [], suggestions: [] },
      compliance_check: { passed: true, violations: [], no_off_platform_contact: true, no_unpaid_free_work: true, no_credential_sharing: true },
      cited_evidence: [],
      status: "interview",
      connects_used: 16,
      created_at: "3 days ago",
      updated_at: "Today"
    },
    {
      id: "prop-ai-095",
      job_id: "job-ai-095",
      job_title: "LLM Hallucination Reduction System with NLI",
      client: "NovaGen AI",
      persona: "ai_engineer",
      draft_content: "Implemented atomic claim verifier...",
      bid_amount: 4800,
      estimated_hours: 50,
      turnaround_days: 14,
      critic_review: { specificity_score: 9.6, evidence_groundedness_score: 9.7, client_alignment_score: 9.5, overall_score: 9.6, comments: [], suggestions: [] },
      compliance_check: { passed: true, violations: [], no_off_platform_contact: true, no_unpaid_free_work: true, no_credential_sharing: true },
      cited_evidence: [],
      status: "hired",
      connects_used: 16,
      created_at: "1 week ago",
      updated_at: "2 days ago"
    }
  ]);

  const moveStage = (proposalId: string, direction: 'next' | 'prev') => {
    setPipelineProposals(prev => prev.map(p => {
      if (p.id === proposalId) {
        const currentIndex = STAGES.findIndex(s => s.id === p.status);
        const newIndex = direction === 'next' 
          ? Math.min(STAGES.length - 1, currentIndex + 1)
          : Math.max(0, currentIndex - 1);
        return { ...p, status: STAGES[newIndex].id };
      }
      return p;
    }));
  };

  const filteredProposals = pipelineProposals.filter(p => {
    if (filterPersona !== 'all' && p.persona !== filterPersona) return false;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header & Filter */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Proposal Pipeline Kanban</h1>
          <p className="text-sm text-slate-400">
            Track and progress client bids across the proposal conversion lifecycle.
          </p>
        </div>

        {/* Filter Persona */}
        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 p-1.5 rounded-xl text-xs">
          <Filter className="w-3.5 h-3.5 text-slate-400 ml-1" />
          <span className="text-slate-400">Persona:</span>
          <select
            value={filterPersona}
            onChange={(e) => setFilterPersona(e.target.value)}
            className="bg-slate-950 text-slate-200 border border-slate-800 rounded px-2 py-1 text-xs focus:outline-none focus:border-indigo-500"
          >
            <option value="all">All Personas</option>
            <option value="ai_engineer">AI Engineer</option>
            <option value="fullstack_dev">Fullstack Dev</option>
            <option value="data_analyst">Data Analyst</option>
          </select>
        </div>
      </div>

      {/* Kanban Board Container (Horizontal Scroll) */}
      <div className="flex space-x-4 overflow-x-auto pb-6 pt-1">
        {STAGES.map((stage) => {
          const cardsInStage = filteredProposals.filter(p => p.status === stage.id);
          const stageTotal = cardsInStage.reduce((acc, c) => acc + c.bid_amount, 0);

          return (
            <div
              key={stage.id}
              className={`w-72 shrink-0 border rounded-2xl p-4 flex flex-col space-y-3 ${stage.color} min-h-[580px] shadow-lg`}
            >
              {/* Column Header */}
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-bold text-white uppercase tracking-wider">{stage.label}</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${stage.badge}`}>
                    {cardsInStage.length}
                  </span>
                </div>
                <span className="text-[11px] font-mono font-semibold text-slate-400">
                  ${stageTotal.toLocaleString()}
                </span>
              </div>

              {/* Cards list */}
              <div className="space-y-3 flex-1 overflow-y-auto">
                {cardsInStage.length === 0 ? (
                  <div className="h-32 border border-dashed border-slate-800 rounded-xl flex items-center justify-center text-[11px] text-slate-400">
                    No proposals
                  </div>
                ) : (
                  cardsInStage.map((card) => (
                    <div
                      key={card.id}
                      className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-xl p-3.5 space-y-2.5 shadow-md transition group"
                    >
                      <div className="flex items-center justify-between text-[11px]">
                        <span className="font-mono text-indigo-400 font-semibold">{card.id}</span>
                        <span className="text-slate-400">{card.created_at}</span>
                      </div>

                      <h4 
                        onClick={() => openProposalStudio(card.id)}
                        className="text-xs font-bold text-white hover:text-indigo-400 cursor-pointer line-clamp-2 leading-snug"
                      >
                        {card.job_title}
                      </h4>

                      <div className="text-[11px] text-slate-400 flex items-center space-x-1">
                        <User className="w-3 h-3 text-slate-500" />
                        <span className="truncate">{card.client}</span>
                      </div>

                      <div className="flex items-center justify-between border-t border-slate-800/80 pt-2 text-xs">
                        <span className="font-extrabold text-emerald-400 font-mono">
                          ${card.bid_amount.toLocaleString()}
                        </span>

                        {/* Move stage controls */}
                        <div className="flex items-center space-x-1 opacity-80 group-hover:opacity-100 transition">
                          <button
                            onClick={() => moveStage(card.id, 'prev')}
                            title="Move back"
                            className="bg-slate-800 hover:bg-slate-700 text-slate-300 px-1.5 py-0.5 rounded text-[10px]"
                          >
                            ◀
                          </button>
                          <button
                            onClick={() => moveStage(card.id, 'next')}
                            title="Advance stage"
                            className="bg-indigo-600 hover:bg-indigo-500 text-white px-1.5 py-0.5 rounded text-[10px]"
                          >
                            ▶
                          </button>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
