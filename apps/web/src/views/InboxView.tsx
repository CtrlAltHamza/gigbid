import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { 
  ShieldAlert, 
  ShieldCheck, 
  AlertTriangle, 
  Zap, 
  ArrowRight, 
  Filter, 
  Search, 
  CheckCircle2, 
  XCircle, 
  Clock 
} from 'lucide-react';
import { Job, RiskLevel } from '../types';

export const InboxView: React.FC = () => {
  const { jobs, selectJobForDetail, openProposalStudio, proposals } = useApp();
  const [filterRisk, setFilterRisk] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [minFitScore, setMinFitScore] = useState<number>(0);

  const filteredJobs = jobs.filter(job => {
    if (filterRisk !== 'all' && job.risk_level !== filterRisk) return false;
    if (job.fit_score < minFitScore) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return (
        job.title.toLowerCase().includes(q) ||
        job.description.toLowerCase().includes(q) ||
        job.client.toLowerCase().includes(q) ||
        job.skills.some(s => s.toLowerCase().includes(q))
      );
    }
    return true;
  });

  const getRiskBadge = (risk: RiskLevel, score: number) => {
    switch (risk) {
      case 'safe':
        return (
          <span className="inline-flex items-center space-x-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full text-xs font-medium">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Safe (Scam: {(score * 100).toFixed(0)}%)</span>
          </span>
        );
      case 'medium':
        return (
          <span className="inline-flex items-center space-x-1 bg-amber-500/10 text-amber-400 border border-amber-500/30 px-2 py-0.5 rounded-full text-xs font-medium">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>Medium Risk</span>
          </span>
        );
      case 'scam':
        return (
          <span className="inline-flex items-center space-x-1 bg-rose-500/20 text-rose-300 border border-rose-500/40 px-2.5 py-0.5 rounded-full text-xs font-bold animate-pulse">
            <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
            <span>SCAM DETECTED ({(score * 100).toFixed(0)}%)</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center space-x-1 bg-slate-700 text-slate-300 px-2 py-0.5 rounded-full text-xs">
            <span>Suspicious</span>
          </span>
        );
    }
  };

  const getActionTag = (job: Job) => {
    if (job.status === 'scam_blocked') {
      return (
        <span className="bg-rose-950 text-rose-400 border border-rose-800 px-2.5 py-1 rounded-md text-xs font-semibold flex items-center space-x-1">
          <XCircle className="w-3.5 h-3.5" />
          <span>BLOCKED — Off-Platform Fraud</span>
        </span>
      );
    }
    if (job.status === 'auto_drafted') {
      return (
        <span className="bg-indigo-950/80 text-indigo-300 border border-indigo-700/60 px-2.5 py-1 rounded-md text-xs font-semibold flex items-center space-x-1">
          <CheckCircle2 className="w-3.5 h-3.5 text-indigo-400" />
          <span>Auto-Draft Ready</span>
        </span>
      );
    }
    if (job.status === 'clarification_needed') {
      return (
        <span className="bg-amber-950/80 text-amber-300 border border-amber-700/60 px-2.5 py-1 rounded-md text-xs font-semibold flex items-center space-x-1">
          <Clock className="w-3.5 h-3.5 text-amber-400" />
          <span>Clarification Needed</span>
        </span>
      );
    }
    return (
      <span className="bg-slate-800 text-slate-400 px-2.5 py-1 rounded-md text-xs">
        Dismissed
      </span>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Marketplace Job Inbox</h1>
          <p className="text-sm text-slate-400">
            Real-time feed filtered and prioritized by Multi-Agent Fit Matcher & Risk Assessor.
          </p>
        </div>

        {/* Filter bar */}
        <div className="flex flex-wrap items-center gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search jobs, skills, clients..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 w-60"
            />
          </div>

          {/* Risk Filter */}
          <div className="flex items-center space-x-1 bg-slate-900 border border-slate-800 p-1 rounded-lg text-xs">
            <Filter className="w-3.5 h-3.5 text-slate-400 ml-1.5" />
            <button
              onClick={() => setFilterRisk('all')}
              className={`px-2 py-1 rounded ${filterRisk === 'all' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'}`}
            >
              All
            </button>
            <button
              onClick={() => setFilterRisk('safe')}
              className={`px-2 py-1 rounded ${filterRisk === 'safe' ? 'bg-emerald-600 text-white' : 'text-slate-400 hover:text-white'}`}
            >
              Safe
            </button>
            <button
              onClick={() => setFilterRisk('medium')}
              className={`px-2 py-1 rounded ${filterRisk === 'medium' ? 'bg-amber-600 text-white' : 'text-slate-400 hover:text-white'}`}
            >
              Medium
            </button>
            <button
              onClick={() => setFilterRisk('scam')}
              className={`px-2 py-1 rounded ${filterRisk === 'scam' ? 'bg-rose-600 text-white' : 'text-slate-400 hover:text-white'}`}
            >
              Scams
            </button>
          </div>

          {/* Min Fit Slider */}
          <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg text-xs">
            <span className="text-slate-400">Min Fit: {minFitScore}%</span>
            <input
              type="range"
              min="0"
              max="90"
              step="10"
              value={minFitScore}
              onChange={(e) => setMinFitScore(Number(e.target.value))}
              className="w-20 accent-indigo-500"
            />
          </div>
        </div>
      </div>

      {/* Jobs List */}
      <div className="space-y-4">
        {filteredJobs.length === 0 ? (
          <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-12 text-center text-slate-400">
            <p className="text-base font-semibold">No jobs match your filter criteria.</p>
            <p className="text-xs mt-1">Try resetting the risk filter or lowering minimum fit threshold.</p>
          </div>
        ) : (
          filteredJobs.map((job) => {
            const hasProposal = proposals.find(p => p.job_id === job.id);
            const isScam = job.risk_level === 'scam';

            return (
              <div
                key={job.id}
                className={`bg-slate-900/80 border rounded-2xl p-6 transition-all hover:border-slate-700 shadow-xl ${
                  isScam 
                    ? 'border-rose-900/60 bg-gradient-to-r from-rose-950/20 via-slate-900/80 to-slate-900/80' 
                    : 'border-slate-800 hover:shadow-indigo-500/5'
                }`}
              >
                <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                  {/* Left Column: Title, Metadata, Badges */}
                  <div className="flex-1 space-y-2.5">
                    <div className="flex flex-wrap items-center gap-2">
                      {getActionTag(job)}
                      {getRiskBadge(job.risk_level, job.scam_score)}
                      <span className="text-xs text-slate-400 font-medium">
                        • {job.platform} • {job.created_at}
                      </span>
                    </div>

                    <h2 
                      onClick={() => selectJobForDetail(job.id)}
                      className="text-lg font-bold text-white hover:text-indigo-400 cursor-pointer transition flex items-center space-x-2"
                    >
                      <span>{job.title}</span>
                    </h2>

                    <p className="text-xs text-slate-300 font-medium">{job.client}</p>

                    <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                      {job.description}
                    </p>

                    {/* Scam Explanatory Box if flagged */}
                    {isScam && job.scam_reasoning && (
                      <div className="p-3 rounded-xl bg-rose-950/40 border border-rose-800/80 text-rose-300 text-xs space-y-1">
                        <div className="font-bold flex items-center space-x-1.5 text-rose-200">
                          <ShieldAlert className="w-4 h-4 text-rose-400" />
                          <span>Scam Guardrail Triggered:</span>
                        </div>
                        <p className="text-slate-300">{job.scam_reasoning}</p>
                        <ul className="list-disc list-inside text-rose-300/80 text-[11px] pt-1">
                          {job.red_flags.map((flag, idx) => (
                            <li key={idx}>{flag}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Skills pills */}
                    <div className="flex flex-wrap gap-1.5 pt-1">
                      {job.skills.map((skill, idx) => (
                        <span
                          key={idx}
                          className="bg-slate-800/80 text-slate-300 border border-slate-700/60 text-[11px] px-2 py-0.5 rounded-md"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Right Column: Fit Score, Budget, Actions */}
                  <div className="flex flex-col items-end justify-between self-stretch shrink-0 min-w-[210px] space-y-4">
                    {/* Fit Score & Budget */}
                    <div className="text-right space-y-1">
                      <div className="flex items-center justify-end space-x-2">
                        <span className="text-xs text-slate-400">Match Fit:</span>
                        <span className={`text-base font-extrabold ${job.fit_score >= 85 ? 'text-emerald-400' : job.fit_score >= 60 ? 'text-amber-400' : 'text-slate-400'}`}>
                          {job.fit_score}%
                        </span>
                      </div>
                      <div className="text-sm font-black text-white">
                        {job.budget_type === 'fixed'
                          ? `$${job.budget_min.toLocaleString()} – $${job.budget_max.toLocaleString()} Fixed`
                          : `$${job.hourly_rate || job.budget_min}/hr Hourly`}
                      </div>
                      <div className="text-[11px] text-amber-400/90 flex items-center justify-end space-x-1">
                        <Zap className="w-3 h-3 fill-amber-400/40" />
                        <span>Requires {job.connects_cost} Connects</span>
                      </div>
                    </div>

                    {/* Action buttons */}
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => selectJobForDetail(job.id)}
                        className="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs px-3 py-2 rounded-xl font-medium border border-slate-700 transition"
                      >
                        Inspect Job
                      </button>

                      {isScam ? (
                        <button
                          disabled
                          className="bg-slate-800 text-slate-500 text-xs px-3 py-2 rounded-xl font-medium cursor-not-allowed border border-slate-800"
                          title="Drafting disabled by Scam Guardrail"
                        >
                          Draft Blocked
                        </button>
                      ) : hasProposal ? (
                        <button
                          onClick={() => openProposalStudio(hasProposal.id)}
                          className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs px-3.5 py-2 rounded-xl font-bold transition flex items-center space-x-1.5 shadow-lg shadow-indigo-600/30"
                        >
                          <span>Review Draft</span>
                          <ArrowRight className="w-3.5 h-3.5" />
                        </button>
                      ) : (
                        <button
                          onClick={() => selectJobForDetail(job.id)}
                          className="bg-indigo-600/20 hover:bg-indigo-600 text-indigo-300 hover:text-white text-xs px-3 py-2 rounded-xl font-medium border border-indigo-500/30 transition flex items-center space-x-1"
                        >
                          <span>Generate Draft</span>
                          <ArrowRight className="w-3.5 h-3.5" />
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

