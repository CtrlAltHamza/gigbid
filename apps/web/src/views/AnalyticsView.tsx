import React from 'react';
import { useApp } from '../context/AppContext';
import { 
  BarChart3, 
  TrendingUp, 
  Zap, 
  Award, 
  Clock, 
  DollarSign, 
  CheckCircle2, 
  Percent, 
  PieChart 
} from 'lucide-react';

export const AnalyticsView: React.FC = () => {
  const { analytics } = useApp();

  const outcomeColors: Record<string, string> = {
    Won: 'bg-emerald-500',
    Replied: 'bg-indigo-500',
    Ignored: 'bg-slate-600',
    Lost: 'bg-rose-500',
  };

  const totalOutcomes = Object.values(analytics.outcomes_breakdown).reduce((a, b) => a + b, 0);

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-black text-white tracking-tight">Performance & Financial Analytics</h1>
        <p className="text-sm text-slate-400">
          Conversion funnels, Connects return-on-investment (ROI), latency percentiles, and multi-agent inference overhead.
        </p>
      </div>

      {/* Top 4 KPI Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-2 shadow-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Client Reply Rate</span>
            <TrendingUp className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-3xl font-black text-white font-mono">
            {analytics.reply_rate}%
          </div>
          <div className="text-[11px] text-emerald-400 font-medium">
            +31.4% vs. manual freelance baseline
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-2 shadow-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Hire (Win) Rate</span>
            <Award className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-black text-emerald-400 font-mono">
            {analytics.hire_rate}%
          </div>
          <div className="text-[11px] text-slate-400">
            {analytics.hired_count} client contracts won
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-2 shadow-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Connects ROI</span>
            <Zap className="w-4 h-4 text-amber-400 fill-amber-400/30" />
          </div>
          <div className="text-3xl font-black text-amber-400 font-mono">
            {analytics.connects_roi}x
          </div>
          <div className="text-[11px] text-slate-400">
            ${(analytics.total_revenue_usd / analytics.connects_spent).toFixed(1)} earned / connect spent
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-2 shadow-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Total Revenue Won</span>
            <DollarSign className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-black text-white font-mono">
            ${analytics.total_revenue_usd.toLocaleString()}
          </div>
          <div className="text-[11px] text-slate-400">
            Across {analytics.proposals_sent} submitted bids
          </div>
        </div>
      </div>

      {/* 2 Columns: Conversion Funnel & System Latency / Cost */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Outcome Breakdown Chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5 shadow-xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <PieChart className="w-4 h-4 text-indigo-400" />
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                Proposal Outcome Conversion Distribution
              </h3>
            </div>
            <span className="text-xs text-slate-400 font-mono">{totalOutcomes} Total</span>
          </div>

          {/* Bar Segment */}
          <div className="h-6 w-full rounded-xl overflow-hidden flex bg-slate-950">
            {Object.entries(analytics.outcomes_breakdown).map(([outcome, count]) => {
              const pct = (count / totalOutcomes) * 100;
              return (
                <div
                  key={outcome}
                  className={`${outcomeColors[outcome] || 'bg-slate-600'} transition-all`}
                  style={{ width: `${pct}%` }}
                  title={`${outcome}: ${count} (${pct.toFixed(1)}%)`}
                />
              );
            })}
          </div>

          {/* Legend */}
          <div className="grid grid-cols-2 gap-3 text-xs">
            {Object.entries(analytics.outcomes_breakdown).map(([outcome, count]) => {
              const pct = (count / totalOutcomes) * 100;
              return (
                <div key={outcome} className="flex items-center justify-between p-2.5 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="flex items-center space-x-2">
                    <span className={`w-3 h-3 rounded-full ${outcomeColors[outcome] || 'bg-slate-600'}`} />
                    <span className="font-semibold text-slate-200">{outcome}</span>
                  </div>
                  <span className="text-slate-400 font-mono">{count} ({pct.toFixed(0)}%)</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Multi-Agent Latency & Cost Metrics */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5 shadow-xl">
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4 text-indigo-400" />
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">
              Inference Telemetry & Speed
            </h3>
          </div>

          <div className="space-y-4 text-xs">
            <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
              <div>
                <div className="font-bold text-white text-sm">Average Pipeline Latency</div>
                <div className="text-[11px] text-slate-400">Total time for 9 agent nodes + critique</div>
              </div>
              <span className="text-lg font-bold text-indigo-400 font-mono">
                {analytics.avg_latency_seconds}s
              </span>
            </div>

            <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
              <div>
                <div className="font-bold text-white text-sm">Average Token Cost Per Bid</div>
                <div className="text-[11px] text-slate-400">Gemini 2.5 Pro & Flash multi-agent calls</div>
              </div>
              <span className="text-lg font-bold text-emerald-400 font-mono">
                ${analytics.avg_cost_per_bid_usd.toFixed(4)}
              </span>
            </div>

            <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
              <div>
                <div className="font-bold text-white text-sm">NLI Verifier Overhead</div>
                <div className="text-[11px] text-slate-400">Atomic claim verification pass</div>
              </div>
              <span className="text-lg font-bold text-slate-200 font-mono">
                45ms / claim
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

