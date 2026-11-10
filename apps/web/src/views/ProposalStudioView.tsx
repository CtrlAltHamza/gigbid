import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { 
  ArrowLeft, 
  Send, 
  X, 
  CheckCircle2, 
  AlertCircle, 
  Sparkles, 
  GitCompare, 
  Zap, 
  ShieldCheck, 
  MessageSquarePlus, 
  ExternalLink,
  ThumbsUp,
  ThumbsDown
} from 'lucide-react';
import { Proposal } from '../types';

export const ProposalStudioView: React.FC = () => {
  const { selectedProposalId, proposals, submitProposalAction, rejectProposalAction, setCurrentView, settings } = useApp();

  const proposal: Proposal = proposals.find(p => p.id === selectedProposalId) || proposals[0];

  const [draftText, setDraftText] = useState<string>(proposal.draft_content);
  const [showDiff, setShowDiff] = useState<boolean>(false);
  const [showRejectModal, setShowRejectModal] = useState<boolean>(false);
  const [rejectFeedback, setRejectFeedback] = useState<string>('Never quote hourly rates under $75/hr and avoid promising unpaid exploratory sprints.');
  const [hoveredCitation, setHoveredCitation] = useState<string | null>(null);

  if (!proposal) {
    return (
      <div className="p-12 text-center text-slate-400">
        <p>No proposal currently selected.</p>
        <button onClick={() => setCurrentView('inbox')} className="mt-3 text-indigo-400 underline">
          Go to Job Inbox
        </button>
      </div>
    );
  }

  const handleApprove = async () => {
    await submitProposalAction(proposal.id, draftText);
  };

  const handleReject = async () => {
    if (!rejectFeedback.trim()) return;
    await rejectProposalAction(proposal.id, rejectFeedback);
    setShowRejectModal(false);
  };

  const isSubmitted = proposal.status !== 'drafted';

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setCurrentView('inbox')}
            className="flex items-center space-x-1 text-xs font-semibold text-slate-400 hover:text-white transition"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Inbox</span>
          </button>
          <span className="text-slate-600">|</span>
          <span className="text-xs bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 px-2 py-0.5 rounded font-mono">
            {proposal.id}
          </span>
          <h1 className="text-lg font-bold text-white tracking-tight truncate max-w-md">
            {proposal.job_title}
          </h1>
        </div>

        {/* Action Controls */}
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setShowDiff(!showDiff)}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-medium border transition ${
              showDiff 
                ? 'bg-indigo-600 text-white border-indigo-500' 
                : 'bg-slate-800 text-slate-300 border-slate-700 hover:text-white'
            }`}
          >
            <GitCompare className="w-3.5 h-3.5" />
            <span>{showDiff ? 'Hide Diff' : 'Compare Revisions'}</span>
          </button>

          {!isSubmitted && (
            <>
              <button
                onClick={() => setShowRejectModal(true)}
                className="bg-slate-800 hover:bg-rose-950/60 text-slate-300 hover:text-rose-300 border border-slate-700 hover:border-rose-800/80 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition flex items-center space-x-1.5"
              >
                <ThumbsDown className="w-3.5 h-3.5" />
                <span>Reject & Teach</span>
              </button>

              <button
                onClick={handleApprove}
                className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-1.5 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 shadow-lg shadow-emerald-600/30"
              >
                <ThumbsUp className="w-3.5 h-3.5" />
                <span>Approve & Submit</span>
              </button>
            </>
          )}

          {isSubmitted && (
            <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 px-3 py-1.5 rounded-xl text-xs font-bold flex items-center space-x-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span className="capitalize">{proposal.status}</span>
            </span>
          )}
        </div>
      </div>

      {/* Main Studio Body: 2 Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column (2 cols): Proposal Editor & Grounding Citations */}
        <div className="lg:col-span-2 space-y-6">
          {/* Diff View Banner */}
          {showDiff && (
            <div className="bg-slate-900 border border-indigo-500/30 rounded-2xl p-5 space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-indigo-300 uppercase tracking-wider flex items-center space-x-1.5">
                  <GitCompare className="w-4 h-4 text-indigo-400" />
                  <span>Revision Diff: Initial Draft vs. Critic-Revised Draft</span>
                </span>
                <span className="text-slate-400 text-[11px]">2 Critic iterations completed</span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div className="bg-rose-950/20 border border-rose-900/40 p-3 rounded-xl text-rose-200">
                  <div className="font-bold text-rose-300 mb-1 text-[11px] uppercase tracking-wider">
                    Initial Draft (Before Critic)
                  </div>
                  <p className="line-through opacity-75 font-mono text-[11px] leading-relaxed">
                    {proposal.initial_draft || "Generic template: Hi, I saw your post looking for a RAG pipeline..."}
                  </p>
                </div>
                <div className="bg-emerald-950/20 border border-emerald-900/40 p-3 rounded-xl text-emerald-200">
                  <div className="font-bold text-emerald-300 mb-1 text-[11px] uppercase tracking-wider">
                    Revised Proposal (Grounding + Critic Loop)
                  </div>
                  <p className="font-mono text-[11px] leading-relaxed">
                    {proposal.revised_draft || proposal.draft_content}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Draft Text Editor */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl relative">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                Proposal Content (Editable)
              </span>
              <span className="text-xs text-slate-500">
                Word Count: {draftText.trim().split(/\s+/).length} words
              </span>
            </div>

            <textarea
              rows={16}
              disabled={isSubmitted}
              value={draftText}
              onChange={(e) => setDraftText(e.target.value)}
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl p-4 text-xs font-mono text-slate-200 focus:outline-none focus:border-indigo-500 leading-relaxed resize-y disabled:opacity-80"
              placeholder="Draft your proposal here..."
            />

            {/* Evidence Citation Popover Trigger bar */}
            <div className="border-t border-slate-800/80 pt-3">
              <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center space-x-1.5">
                <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                <span>Hover to Preview Grounding Evidence Citations:</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {proposal.cited_evidence.map((ev) => (
                  <div
                    key={ev.id}
                    onMouseEnter={() => setHoveredCitation(ev.id)}
                    onMouseLeave={() => setHoveredCitation(null)}
                    className="relative"
                  >
                    <button className="bg-indigo-950/60 hover:bg-indigo-900/80 text-indigo-300 border border-indigo-700/60 text-xs px-2.5 py-1 rounded-lg font-mono font-medium flex items-center space-x-1 transition">
                      <span>[{ev.id}]</span>
                      <span className="text-slate-400 text-[10px] truncate max-w-[120px]">{ev.title}</span>
                    </button>

                    {/* Popover Tooltip */}
                    {hoveredCitation === ev.id && (
                      <div className="absolute bottom-full left-0 mb-2 w-80 bg-slate-900 border border-indigo-500/50 rounded-xl p-3.5 shadow-2xl z-30 text-xs space-y-2 pointer-events-none animate-in fade-in zoom-in-95">
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-indigo-300 font-mono">[{ev.id}]</span>
                          <span className="text-[10px] text-emerald-400 font-semibold">Similarity: {(ev.similarity_score * 100).toFixed(0)}%</span>
                        </div>
                        <div className="font-medium text-white text-[11px]">{ev.title}</div>
                        <p className="text-slate-300 text-[11px] italic leading-relaxed bg-slate-950/60 p-2 rounded border border-slate-800">
                          "{ev.excerpt}"
                        </p>
                        <div className="flex flex-wrap gap-1">
                          {ev.metrics.map((m, idx) => (
                            <span key={idx} className="bg-slate-800 text-slate-300 text-[9px] px-1.5 py-0.5 rounded">
                              {m}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right Column (1 col): Critic Scores, Compliance & Cost Preview */}
        <div className="space-y-6">
          {/* Critic Rubric Evaluation */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Critic Agent Rubric
              </span>
              <span className="text-sm font-extrabold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                {proposal.critic_review.overall_score.toFixed(1)} / 10
              </span>
            </div>

            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Specificity:</span>
                  <span className="font-bold text-white">{proposal.critic_review.specificity_score} / 10</span>
                </div>
                <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${proposal.critic_review.specificity_score * 10}%` }} />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Evidence Groundedness:</span>
                  <span className="font-bold text-white">{proposal.critic_review.evidence_groundedness_score} / 10</span>
                </div>
                <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${proposal.critic_review.evidence_groundedness_score * 10}%` }} />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Client Alignment:</span>
                  <span className="font-bold text-white">{proposal.critic_review.client_alignment_score} / 10</span>
                </div>
                <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-violet-500 rounded-full" style={{ width: `${proposal.critic_review.client_alignment_score * 10}%` }} />
                </div>
              </div>
            </div>

            <div className="border-t border-slate-800 pt-3 space-y-2 text-xs">
              <div className="font-semibold text-slate-300">Critic Feedback:</div>
              <ul className="space-y-1.5 text-slate-400 text-[11px]">
                {proposal.critic_review.comments.map((c, idx) => (
                  <li key={idx} className="flex items-start space-x-1.5">
                    <span className="text-emerald-400">•</span>
                    <span>{c}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Compliance Guardrails */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3 shadow-xl">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <h3 className="text-xs font-bold uppercase tracking-wider text-white">
                Compliance Guardrails
              </h3>
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between text-emerald-400 bg-emerald-950/20 p-2 rounded-lg border border-emerald-900/40">
                <span>No Off-Platform Contact:</span>
                <span className="font-bold">PASSED</span>
              </div>
              <div className="flex items-center justify-between text-emerald-400 bg-emerald-950/20 p-2 rounded-lg border border-emerald-900/40">
                <span>No Unpaid Free Work:</span>
                <span className="font-bold">PASSED</span>
              </div>
              <div className="flex items-center justify-between text-emerald-400 bg-emerald-950/20 p-2 rounded-lg border border-emerald-900/40">
                <span>No Credential Sharing:</span>
                <span className="font-bold">PASSED</span>
              </div>
            </div>
          </div>

          {/* Dry-Run Connects Cost & ROI Preview */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3 shadow-xl">
            <div className="flex items-center space-x-2">
              <Zap className="w-4 h-4 text-amber-400 fill-amber-400/40" />
              <h3 className="text-xs font-bold uppercase tracking-wider text-white">
                Dry-Run Connects Preview
              </h3>
            </div>

            <div className="space-y-2 text-xs text-slate-300">
              <div className="flex justify-between">
                <span>Connects Required:</span>
                <span className="font-bold text-amber-400">{proposal.connects_used} Connects</span>
              </div>
              <div className="flex justify-between">
                <span>Current Balance:</span>
                <span className="font-bold text-white">{settings.connects_balance} Connects</span>
              </div>
              <div className="flex justify-between">
                <span>Balance After Submit:</span>
                <span className="font-bold text-emerald-400">
                  {settings.connects_balance - (isSubmitted ? 0 : proposal.connects_used)} Connects
                </span>
              </div>
              <div className="flex justify-between border-t border-slate-800 pt-2">
                <span>Target Bid Amount:</span>
                <span className="font-extrabold text-white">${proposal.bid_amount.toLocaleString()}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Reject & Teach Modal */}
      {showRejectModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <MessageSquarePlus className="w-5 h-5 text-indigo-400" />
                <h3 className="font-bold text-white text-base">Reject & Promote to Long-Term Memory</h3>
              </div>
              <button onClick={() => setShowRejectModal(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-300">
              Provide specific feedback on why this proposal draft was rejected. The agent will distill this into a durable memory rule so future drafts adhere to your preference.
            </p>

            <textarea
              rows={4}
              value={rejectFeedback}
              onChange={(e) => setRejectFeedback(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-200 focus:outline-none focus:border-indigo-500 font-mono"
              placeholder="e.g. Never mention fixed price under $500, always mention Ray and PyTorch..."
            />

            <div className="flex items-center justify-end space-x-3 pt-2">
              <button
                onClick={() => setShowRejectModal(false)}
                className="px-4 py-2 text-xs font-semibold text-slate-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={handleReject}
                className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-xl text-xs font-bold transition shadow-lg shadow-indigo-600/30"
              >
                Promote Rule & Reject
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
