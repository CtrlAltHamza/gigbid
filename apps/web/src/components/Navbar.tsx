import React from 'react';
import { useApp } from '../context/AppContext';
import { ShieldAlert, Zap, AlertTriangle, CheckCircle, Info, RefreshCw, Cpu } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { settings, notification, setNotification, toggleDegradedMode, triggerScoutAction } = useApp();

  const personaLabels: Record<string, string> = {
    ai_engineer: 'AI & LLM Engineer',
    fullstack_dev: 'Full-Stack Developer',
    data_analyst: 'Data Analyst & BI',
  };

  return (
    <header className="bg-slate-900 border-b border-slate-800 px-6 py-3 sticky top-0 z-40 flex items-center justify-between">
      {/* Brand */}
      <div className="flex items-center space-x-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 text-white font-black tracking-wider text-lg">
          GB
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <span className="font-extrabold text-lg tracking-tight text-white">GigBid</span>
            <span className="text-[10px] font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-1.5 py-0.5 rounded uppercase tracking-wider">
              Copilot v2.4
            </span>
          </div>
          <p className="text-xs text-slate-400">Autonomous Freelance Operating System</p>
        </div>
      </div>

      {/* Center Status Banner (Degraded Mode & Scout) */}
      <div className="flex items-center space-x-3">
        {settings.degraded_mode_simulated ? (
          <div className="flex items-center space-x-2 bg-amber-500/10 border border-amber-500/30 text-amber-300 px-3 py-1.5 rounded-lg text-xs font-medium animate-pulse">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <span>Degraded Mode Active: GigSim Simulator Fallback</span>
            <button 
              onClick={toggleDegradedMode} 
              className="ml-2 underline text-amber-200 hover:text-white"
            >
              Restore Live
            </button>
          </div>
        ) : (
          <div className="flex items-center space-x-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 px-3 py-1.5 rounded-lg text-xs font-medium">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
            <span>Upwork Live Adapter Connected</span>
            <button 
              onClick={toggleDegradedMode} 
              className="ml-2 text-[10px] bg-slate-800 text-slate-300 hover:text-white px-1.5 py-0.5 rounded border border-slate-700"
            >
              Simulate Failure
            </button>
          </div>
        )}

        <button
          onClick={triggerScoutAction}
          className="flex items-center space-x-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3 py-1.5 rounded-lg text-xs font-medium transition shadow-sm"
          title="Trigger Scout agent to scan marketplace"
        >
          <RefreshCw className="w-3.5 h-3.5 text-indigo-400" />
          <span>Scout Marketplace</span>
        </button>
      </div>

      {/* Right Stats & Persona */}
      <div className="flex items-center space-x-4">
        {/* Connects Balance */}
        <div className="flex items-center space-x-2 bg-slate-950/80 border border-slate-800 px-3 py-1.5 rounded-lg">
          <Zap className="w-4 h-4 text-amber-400 fill-amber-400/30" />
          <div className="text-right">
            <div className="text-xs font-bold text-amber-400">{settings.connects_balance}</div>
            <div className="text-[10px] text-slate-400 uppercase tracking-wider">Connects</div>
          </div>
        </div>

        {/* Persona Pill */}
        <div className="flex items-center space-x-2 bg-slate-800/80 border border-slate-700 px-3 py-1.5 rounded-lg">
          <Cpu className="w-4 h-4 text-indigo-400" />
          <div>
            <div className="text-xs font-semibold text-slate-200">{personaLabels[settings.persona]}</div>
            <div className="text-[10px] text-slate-400">
              {settings.autonomy_level === 'draft_and_ask' ? 'Human-in-Loop' : settings.autonomy_level === 'full_auto' ? 'Full Autonomy' : 'Scout Only'}
            </div>
          </div>
        </div>
      </div>

      {/* Global Notification Toast */}
      {notification && (
        <div className="fixed bottom-6 right-6 z-50 max-w-md p-4 rounded-xl shadow-2xl border flex items-start space-x-3 transition-all animate-bounce bg-slate-900 border-indigo-500/40 text-slate-100">
          {notification.type === 'success' && <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />}
          {notification.type === 'warning' && <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />}
          {notification.type === 'error' && <ShieldAlert className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />}
          {notification.type === 'info' && <Info className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />}
          <div className="flex-1">
            <p className="text-sm font-medium text-slate-200">{notification.message}</p>
          </div>
          <button 
            onClick={() => setNotification(null)}
            className="text-slate-400 hover:text-white text-xs font-bold"
          >
            ✕
          </button>
        </div>
      )}
    </header>
  );
};

