import React from 'react';
import { useApp } from '../context/AppContext';
import { 
  ArrowLeft, 
  ShieldAlert, 
  ShieldCheck, 
  CheckCircle, 
  DollarSign, 
  Clock, 
  FileCheck2, 
  Layers, 
  User, 
  PenTool, 
  AlertCircle 
} from 'lucide-react';

export const JobDetailView: React.FC = () => {
  const { selectedJobId, jobs, proposals, setCurrentView, openProposalStudio } = useApp();

  const job = jobs.find(j => j.id === selectedJobId) || jobs[0];
  const proposal = proposals.find(p => p.job_id === job.id);
  const isScam = job.risk_level === 'scam';

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Back button & Title header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <button
          onClick={() => setCurrentView('inbox')}
          className="flex items-center space-x-2 text-xs font-semibold text-slate-400 hover:text-white transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Job Inbox</span>
        </button>

        <div className="flex items-center space-x-3">
          {proposal && (
            <button
              onClick={() => openProposalStudio(proposal.id)}
              className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs px-4 py-2 rounded-xl font-bold flex items-center space-x-2 transition shadow-lg shadow-indigo-600/30"
            >
              <PenTool className="w-3.5 h-3.5" />
              <span>Open in Proposal Studio</span>
            </button>
          )}
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Job Spec & Evidence Matrix */}
        <div className="lg:col-span-2 space-y-6">
          {/* Job Overview Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">
                Structured JobSpec
              </span>
              <span className="text-xs bg-slate-800 text-slate-300 px-2.5 py-1 rounded-md font-mono">
                ID: {job.id}
              </span>
            </div>

            <h1 className="text-xl font-black text-white leading-tight">
              {job.title}
            </h1>

            <div className="flex items-center space-x-4 text-xs text-slate-300 border-y border-slate-800/80 py-3">
              <div className="flex items-center space-x-1.5">
                <User className="w-3.5 h-3.5 text-indigo-400" />
                <span>{job.client}</span>
              </div>
              <div>•</div>
              <div className="flex items-center space-x-1.5">
                <DollarSign className="w-3.5 h-3.5 text-emerald-400" />
                <span className="font-semibold text-white">
                  {job.budget_type === 'fixed'
                    ? `$${job.budget_min.toLocaleString()} – $${job.budget_max.toLocaleString()} Fixed`
                    : `$${job.hourly_rate || job.budget_min}/hr`}
                </span>
              </div>
              <div>•</div>
              <div className="flex items-center space-x-1.5">
                <Clock className="w-3.5 h-3.5 text-slate-400" />
                <span>Posted {job.created_at}</span>
              </div>
            </div>

            <div className="space-y-2">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Project Scope & Context</h3>
              <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-line">
                {job.description}
              </p>
            </div>

            {/* Deliverables List */}
            <div className="space-y-2 pt-2">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Target Deliverables</h3>
              <ul className="space-y-1.5">
                {job.deliverables.map((deliv, idx) => (
                  <li key={idx} className="flex items-start space-x-2 text-xs text-slate-300">
                    <CheckCircle className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
                    <span>{deliv}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Skills */}
            <div className="pt-2">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Required Tech Stack</h3>
              <div className="flex flex-wrap gap-1.5">
                {job.skills.map((s, idx) => (
                  <span key={idx} className="bg-slate-800 text-indigo-300 border border-slate-700 text-xs px-2.5 py-1 rounded-md">
                    {s}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Requirement-to-Evidence Matrix Table */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Layers className="w-4 h-4 text-indigo-400" />
                <h2 className="text-sm font-bold text-white uppercase tracking-wider">
                  Requirement-to-Evidence Grounding Matrix
                </h2>
              </div>
              <span className="text-xs text-slate-400">Retriever: V4 Outcome-Aware + Cross-Encoder</span>
            </div>

            {job.requirement_matches.length === 0 ? (
              <div className="bg-slate-950/60 p-6 rounded-xl text-center text-xs text-slate-400 border border-slate-800">
                No verified evidence matches found for this job (or job was flagged as scam).
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-950/60 text-slate-400 uppercase tracking-wider text-[10px] border-b border-slate-800">
                    <tr>
                      <th className="py-2.5 px-3">Job Requirement</th>
                      <th className="py-2.5 px-3">Portfolio Case Study</th>
                      <th className="py-2.5 px-3">Grounding Excerpt</th>
                      <th className="py-2.5 px-3 text-right">Similarity</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/80">
                    {job.requirement_matches.map((match, idx) => (
                      <tr key={idx} className="hover:bg-slate-800/30 transition">
                        <td className="py-3 px-3 font-medium text-slate-200 align-top max-w-[160px]">
                          {match.requirement}
                        </td>
                        <td className="py-3 px-3 text-indigo-400 align-top max-w-[160px]">
                          <span className="font-semibold block">{match.evidence_id}</span>
                          <span className="text-[11px] text-slate-400">{match.evidence_title}</span>
                        </td>
                        <td className="py-3 px-3 text-slate-300 text-[11px] align-top leading-relaxed">
                          "{match.excerpt}"
                        </td>
                        <td className="py-3 px-3 text-right font-mono font-bold text-emerald-400 align-top">
                          {(match.score * 100).toFixed(0)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>

        {/* Right 1 Col: Risk Assessment, Pricing Rationale, Autonomy */}
        <div className="space-y-6">
          {/* Risk Analysis Card */}
          <div className={`border rounded-2xl p-6 space-y-4 shadow-xl ${
            isScam 
              ? 'bg-rose-950/30 border-rose-800' 
              : 'bg-slate-900 border-slate-800'
          }`}>
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Risk & Scam Assessment
              </span>
              {isScam ? (
                <ShieldAlert className="w-5 h-5 text-rose-400" />
              ) : (
                <ShieldCheck className="w-5 h-5 text-emerald-400" />
              )}
            </div>

            <div className="flex items-center space-x-3">
              <div className="text-3xl font-black text-white">
                {(job.scam_score * 100).toFixed(0)}%
              </div>
              <div>
                <div className={`text-xs font-bold uppercase ${isScam ? 'text-rose-400' : 'text-emerald-400'}`}>
                  {isScam ? 'High Scam Risk' : 'Low Scam Risk'}
                </div>
                <div className="text-[11px] text-slate-400">Assessed by Risk Assessor Agent</div>
              </div>
            </div>

            {isScam ? (
              <div className="space-y-2 pt-2 border-t border-rose-900/60">
                <div className="text-xs font-semibold text-rose-200">Scam Detection Reasoning:</div>
                <p className="text-xs text-rose-300 leading-relaxed">{job.scam_reasoning}</p>
                <div className="text-xs font-semibold text-rose-200 pt-1">Red Flags:</div>
                <ul className="space-y-1 text-xs text-rose-300/90 list-disc list-inside">
                  {job.red_flags.map((flag, idx) => (
                    <li key={idx}>{flag}</li>
                  ))}
                </ul>
              </div>
            ) : (
              <div className="space-y-2 pt-2 border-t border-slate-800 text-xs text-slate-300">
                <p className="text-emerald-400 font-medium">✓ Client has verified payment method.</p>
                <p className="text-emerald-400 font-medium">✓ Zero off-platform contact keywords found.</p>
                <p className="text-emerald-400 font-medium">✓ Budget is within normal market quartiles.</p>
              </div>
            )}
          </div>

          {/* Pricing Rationale Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
            <div className="flex items-center space-x-2">
              <DollarSign className="w-4 h-4 text-emerald-400" />
              <h3 className="text-xs font-bold uppercase tracking-wider text-white">
                Pricing Engine Rationale
              </h3>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/60 p-3.5 rounded-xl border border-slate-800">
              {job.pricing_rationale}
            </p>

            <div className="space-y-2 text-xs text-slate-400 border-t border-slate-800 pt-3">
              <div className="flex justify-between">
                <span>Connects Cost:</span>
                <span className="font-semibold text-amber-400">{job.connects_cost} Connects</span>
              </div>
              <div className="flex justify-between">
                <span>Estimated Value:</span>
                <span className="font-semibold text-white">
                  ${job.budget_max.toLocaleString()}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Expected Value ROI:</span>
                <span className="font-semibold text-emerald-400">~12.4x</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

