import React from 'react';
import { useApp, AppView } from '../context/AppContext';
import { 
  Inbox, 
  FileText, 
  PenTool, 
  Kanban, 
  MessageSquare, 
  PlayCircle, 
  BarChart3, 
  Settings, 
  UserCheck 
} from 'lucide-react';

interface NavItem {
  id: AppView;
  label: string;
  icon: React.ElementType;
  badge?: number | string;
  badgeColor?: string;
}

export const Sidebar: React.FC = () => {
  const { currentView, setCurrentView, jobs, proposals, messages, runs } = useApp();

  const pendingApprovalsCount = proposals.filter(p => p.status === 'drafted').length;
  const unreadMessagesCount = messages.filter(m => m.unread).length;
  const runningRunsCount = runs.filter(r => r.status === 'running' || r.status === 'interrupted').length;

  const navItems: NavItem[] = [
    { id: 'inbox', label: 'Job Inbox', icon: Inbox, badge: jobs.length, badgeColor: 'bg-indigo-500/20 text-indigo-300' },
    { id: 'job_detail', label: 'Job Detail', icon: FileText },
    { 
      id: 'proposal_studio', 
      label: 'Proposal Studio', 
      icon: PenTool, 
      badge: pendingApprovalsCount > 0 ? `${pendingApprovalsCount} Draft` : undefined,
      badgeColor: 'bg-amber-500/20 text-amber-300' 
    },
    { id: 'pipeline', label: 'Pipeline Board', icon: Kanban },
    { 
      id: 'messages', 
      label: 'Client Messages', 
      icon: MessageSquare, 
      badge: unreadMessagesCount > 0 ? unreadMessagesCount : undefined,
      badgeColor: 'bg-emerald-500/20 text-emerald-300' 
    },
    { 
      id: 'runs', 
      label: 'Agent Runs', 
      icon: PlayCircle, 
      badge: runningRunsCount > 0 ? 'Live' : undefined,
      badgeColor: 'bg-purple-500/20 text-purple-300' 
    },
    { id: 'analytics', label: 'Analytics ROI', icon: BarChart3 },
    { id: 'settings', label: 'Settings & Memory', icon: Settings },
    { id: 'onboarding', label: 'Onboarding & Profile', icon: UserCheck },
  ];

  return (
    <aside className="w-64 bg-slate-900/60 border-r border-slate-800 flex flex-col shrink-0 min-h-[calc(100vh-61px)]">
      <div className="p-4 space-y-1">
        <p className="px-3 text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2">
          Workspace Navigation
        </p>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                  : 'text-slate-300 hover:bg-slate-800/80 hover:text-white'
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span
                  className={`text-xs px-2 py-0.5 rounded-full font-semibold ${
                    isActive ? 'bg-white/20 text-white' : item.badgeColor
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Footer Info Box */}
      <div className="mt-auto p-4 border-t border-slate-800/80 m-3 rounded-xl bg-slate-950/40 text-xs text-slate-400 space-y-2">
        <div className="flex items-center justify-between text-[11px] text-slate-400 font-semibold">
          <span>MCP SERVERS</span>
          <span className="text-emerald-400">3 Online</span>
        </div>
        <div className="space-y-1 text-[11px]">
          <div className="flex items-center justify-between">
            <span>• Portfolio MCP</span>
            <span className="text-slate-400 font-mono">1.0.0</span>
          </div>
          <div className="flex items-center justify-between">
            <span>• Marketplace MCP</span>
            <span className="text-slate-400 font-mono">1.0.0</span>
          </div>
          <div className="flex items-center justify-between">
            <span>• Workspace MCP</span>
            <span className="text-slate-400 font-mono">1.0.0</span>
          </div>
        </div>
      </div>
    </aside>
  );
};
