import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { 
  Settings, 
  Sliders, 
  Trash2, 
  ShieldCheck, 
  BrainCircuit, 
  Zap, 
  AlertTriangle, 
  CheckCircle2, 
  RefreshCw,
  Plus
} from 'lucide-react';
import { AutonomyLevel, MemoryRule } from '../types';

export const SettingsView: React.FC = () => {
  const { settings, updateSettingsAction, rules, deleteMemoryRuleAction, toggleDegradedMode } = useApp();

  const [hourlyFloor, setHourlyFloor] = useState<number>(settings.hourly_rate_floor);
  const [dailyConnects, setDailyConnects] = useState<number>(settings.max_daily_connects);
  const [autonomy, setAutonomy] = useState<AutonomyLevel>(settings.autonomy_level);

  const handleSaveSettings = async () => {
    await updateSettingsAction({
      hourly_rate_floor: hourlyFloor,
      max_daily_connects: dailyConnects,
      autonomy_level: autonomy,
    });
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-black text-white tracking-tight">System Settings & Memory Store</h1>
        <p className="text-sm text-slate-400">
          Configure agent autonomy boundaries, financial safety guardrails, and manage learned user heuristics in the Memory Store.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Autonomy & Financial Guardrails */}
        <div className="space-y-6">
          {/* Autonomy Level */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
            <div className="flex items-center space-x-2">
              <Sliders className="w-4 h-4 text-indigo-400" />
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                Agent Autonomy Mode
              </h3>
            </div>

            <div className="space-y-3">
              <label
                onClick={() => setAutonomy('scout_only')}
                className={`p-3.5 rounded-xl border block cursor-pointer transition ${
                  autonomy === 'scout_only'
                    ? 'bg-indigo-950/60 border-indigo-500 text-white'
                    : 'bg-slate-950/40 border-slate-800 text-slate-300 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs">Level 1: Scout Only</span>
                  {autonomy === 'scout_only' && <CheckCircle2 className="w-4 h-4 text-indigo-400" />}
                </div>
                <p className="text-[11px] text-slate-400 mt-1">
                  Agent searches and filters marketplace opportunities. No proposals or bids are ever drafted.
                </p>
              </label>

              <label
                onClick={() => setAutonomy('draft_and_ask')}
                className={`p-3.5 rounded-xl border block cursor-pointer transition ${
                  autonomy === 'draft_and_ask'
                    ? 'bg-indigo-950/60 border-indigo-500 text-white'
                    : 'bg-slate-950/40 border-slate-800 text-slate-300 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs">Level 2: Draft & Ask (Human-in-the-Loop)</span>
                  {autonomy === 'draft_and_ask' && <CheckCircle2 className="w-4 h-4 text-indigo-400" />}
                </div>
                <p className="text-[11px] text-slate-400 mt-1">
                  Full multi-agent pipeline drafts, grounds, and critiques bids. Execution suspends at <code className="text-indigo-300">interrupt()</code> awaiting human approval before submitting.
                </p>
              </label>

              <label
                onClick={() => setAutonomy('full_auto')}
                className={`p-3.5 rounded-xl border block cursor-pointer transition ${
                  autonomy === 'full_auto'
                    ? 'bg-indigo-950/60 border-indigo-500 text-white'
                    : 'bg-slate-950/40 border-slate-800 text-slate-300 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs">Level 3: Full Auto (Confidence &gt; 95%)</span>
                  {autonomy === 'full_auto' && <CheckCircle2 className="w-4 h-4 text-indigo-400" />}
                </div>
                <p className="text-[11px] text-slate-400 mt-1">
                  Autonomous proposal dispatch for bids meeting ultra-high confidence, capped strictly by daily Connects ceiling.
                </p>
              </label>
            </div>
          </div>

          {/* Rate & Connects Safety Boundaries */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                Financial Guardrails
              </h3>
            </div>

            <div className="space-y-4 text-xs">
              <div>
                <div className="flex justify-between mb-1.5">
                  <span className="text-slate-300 font-semibold">Hourly Rate Floor ($/hr):</span>
                  <span className="font-bold text-indigo-400 font-mono">${hourlyFloor}/hr</span>
                </div>
                <input
                  type="range"
                  min="40"
                  max="150"
                  step="5"
                  value={hourlyFloor}
                  onChange={(e) => setHourlyFloor(Number(e.target.value))}
                  className="w-full accent-indigo-500"
                />
                <p className="text-[10px] text-slate-400 mt-1">Agent will automatically discard or negotiate up any jobs paying below this rate.</p>
              </div>

              <div>
                <div className="flex justify-between mb-1.5">
                  <span className="text-slate-300 font-semibold">Max Daily Connects Budget:</span>
                  <span className="font-bold text-amber-400 font-mono">{dailyConnects} Connects/day</span>
                </div>
                <input
                  type="range"
                  min="16"
                  max="100"
                  step="8"
                  value={dailyConnects}
                  onChange={(e) => setDailyConnects(Number(e.target.value))}
                  className="w-full accent-amber-500"
                />
                <p className="text-[10px] text-slate-400 mt-1">Hard killswitch ceiling preventing accidental Connects depletion.</p>
              </div>
            </div>

            <button
              onClick={handleSaveSettings}
              className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-2 rounded-xl text-xs transition shadow-lg shadow-indigo-600/30"
            >
              Save Financial Guardrails
            </button>
          </div>

          {/* Degraded Mode Simulation Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3 shadow-xl">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <AlertTriangle className="w-4 h-4 text-amber-400" />
                <h3 className="text-xs font-bold uppercase tracking-wider text-white">
                  Degraded Mode Simulator
                </h3>
              </div>
              <button
                onClick={toggleDegradedMode}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
                  settings.degraded_mode_simulated
                    ? 'bg-amber-500 text-slate-950 font-bold'
                    : 'bg-slate-800 text-slate-300 hover:text-white'
                }`}
              >
                {settings.degraded_mode_simulated ? 'Fallback Active' : 'Simulate Upwork Outage'}
              </button>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              When enabled, the MultiServerMCPClient catches marketplace connection dropouts or 429 rate limits, and dynamically falls back to the deterministic local GigSim simulator without crashing.
            </p>
          </div>
        </div>

        {/* Right Column: Long-Term Memory Store Inspector */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div className="flex items-center space-x-2">
              <BrainCircuit className="w-4 h-4 text-indigo-400" />
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                Learned Heuristics in Memory Store
              </h3>
            </div>
            <span className="text-xs text-indigo-400 font-mono font-semibold">
              {rules.length} Rules Active
            </span>
          </div>

          <p className="text-xs text-slate-400">
            Rules distilled by the Memory Store when proposals are rejected with feedback or won with high client engagement. Rules are injected dynamically into Writer & Critic prompts.
          </p>

          <div className="space-y-3">
            {rules.length === 0 ? (
              <div className="p-8 text-center text-xs text-slate-400 border border-dashed border-slate-800 rounded-xl">
                No learned rules currently in Memory Store.
              </div>
            ) : (
              rules.map((rule) => (
                <div
                  key={rule.id}
                  className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 space-y-2 group hover:border-slate-700 transition"
                >
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-mono text-[11px] text-indigo-400 font-semibold">{rule.id}</span>
                    <div className="flex items-center space-x-2">
                      <span className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded uppercase font-bold">
                        {rule.category}
                      </span>
                      <button
                        onClick={() => deleteMemoryRuleAction(rule.id)}
                        className="text-slate-500 hover:text-rose-400 transition"
                        title="Delete rule"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>

                  <p className="text-xs text-slate-200 leading-relaxed font-sans">
                    "{rule.rule_text}"
                  </p>

                  <div className="flex items-center justify-between text-[10px] text-slate-400 border-t border-slate-800/60 pt-2">
                    <span>Source: {rule.source_proposal_id}</span>
                    <span className="text-emerald-400 font-semibold">Confidence: {(rule.confidence * 100).toFixed(0)}%</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

