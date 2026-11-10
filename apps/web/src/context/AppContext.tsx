import React, { createContext, useContext, useState, useEffect } from 'react';
import { Job, Proposal, MessageThread, AgentRun, MemoryRule, UserSettings, AnalyticsSummary, PersonaType } from '../types';
import { api } from '../lib/api';
import { INITIAL_JOBS, INITIAL_PROPOSALS, INITIAL_MESSAGES, INITIAL_RUNS, INITIAL_RULES, INITIAL_ANALYTICS } from '../lib/mockData';

export type AppView = 
  | 'onboarding'
  | 'inbox'
  | 'job_detail'
  | 'proposal_studio'
  | 'pipeline'
  | 'messages'
  | 'runs'
  | 'analytics'
  | 'settings';

interface AppContextType {
  currentView: AppView;
  setCurrentView: (view: AppView) => void;
  selectedJobId: string | null;
  setSelectedJobId: (id: string | null) => void;
  selectedProposalId: string | null;
  setSelectedProposalId: (id: string | null) => void;
  selectedThreadId: string | null;
  setSelectedThreadId: (id: string | null) => void;
  selectedRunId: string | null;
  setSelectedRunId: (id: string | null) => void;
  
  // Data state
  jobs: Job[];
  proposals: Proposal[];
  messages: MessageThread[];
  runs: AgentRun[];
  rules: MemoryRule[];
  settings: UserSettings;
  analytics: AnalyticsSummary;
  
  // Actions
  selectJobForDetail: (jobId: string) => void;
  openProposalStudio: (proposalId: string) => void;
  submitProposalAction: (proposalId: string, editedContent?: string) => Promise<void>;
  rejectProposalAction: (proposalId: string, feedback: string) => Promise<void>;
  bookInterviewSlotAction: (threadId: string, slot: string) => Promise<void>;
  sendClientMessageAction: (threadId: string, text: string) => Promise<void>;
  deleteMemoryRuleAction: (ruleId: string) => Promise<void>;
  updateSettingsAction: (newSettings: Partial<UserSettings>) => Promise<void>;
  triggerScoutAction: () => Promise<void>;
  toggleDegradedMode: () => void;
  setPersona: (persona: PersonaType) => void;
  
  // Notifications
  notification: { type: 'success' | 'warning' | 'error' | 'info'; message: string } | null;
  setNotification: (notif: { type: 'success' | 'warning' | 'error' | 'info'; message: string } | null) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentView, setCurrentView] = useState<AppView>('inbox');
  const [selectedJobId, setSelectedJobId] = useState<string | null>('job-ai-101');
  const [selectedProposalId, setSelectedProposalId] = useState<string | null>('prop-ai-101');
  const [selectedThreadId, setSelectedThreadId] = useState<string | null>('thread-01');
  const [selectedRunId, setSelectedRunId] = useState<string | null>('run-9842');

  const [jobs, setJobs] = useState<Job[]>(INITIAL_JOBS);
  const [proposals, setProposals] = useState<Proposal[]>(INITIAL_PROPOSALS);
  const [messages, setMessages] = useState<MessageThread[]>(INITIAL_MESSAGES);
  const [runs, setRuns] = useState<AgentRun[]>(INITIAL_RUNS);
  const [rules, setRules] = useState<MemoryRule[]>(INITIAL_RULES);
  const [analytics, setAnalytics] = useState<AnalyticsSummary>(INITIAL_ANALYTICS);
  const [settings, setSettings] = useState<UserSettings>({
    persona: 'ai_engineer',
    autonomy_level: 'draft_and_ask',
    hourly_rate_floor: 75,
    max_daily_connects: 40,
    connects_balance: 150,
    degraded_mode_simulated: false,
    min_client_rating: 4.5,
    auto_submit_confidence_threshold: 0.95,
  });

  const [notification, setNotification] = useState<{ type: 'success' | 'warning' | 'error' | 'info'; message: string } | null>(null);

  // Sync initial data from backend if available
  useEffect(() => {
    async function loadData() {
      try {
        const [j, p, m, r, rl, s, a] = await Promise.all([
          api.getJobs(),
          api.getProposals(),
          api.getMessages(),
          api.getRuns(),
          api.getMemoryRules(),
          api.getSettings(),
          api.getAnalytics(),
        ]);
        if (j.length) setJobs(j);
        if (p.length) setProposals(p);
        if (m.length) setMessages(m);
        if (r.length) setRuns(r);
        if (rl.length) setRules(rl);
        setSettings(s);
        setAnalytics(a);
      } catch (err) {
        console.info('Running in local standalone state with mock corpus.');
      }
    }
    loadData();
  }, []);

  const selectJobForDetail = (jobId: string) => {
    setSelectedJobId(jobId);
    setCurrentView('job_detail');
  };

  const openProposalStudio = (proposalId: string) => {
    setSelectedProposalId(proposalId);
    setCurrentView('proposal_studio');
  };

  const submitProposalAction = async (proposalId: string, editedContent?: string) => {
    const cost = 16;
    if (settings.connects_balance < cost) {
      setNotification({ type: 'error', message: 'Insufficient Connects balance to submit proposal.' });
      return;
    }

    setProposals(prev => prev.map(p => {
      if (p.id === proposalId) {
        return {
          ...p,
          status: 'submitted',
          draft_content: editedContent || p.draft_content,
          updated_at: 'Just now',
        };
      }
      return p;
    }));

    setSettings(prev => ({
      ...prev,
      connects_balance: prev.connects_balance - cost,
    }));

    setAnalytics(prev => ({
      ...prev,
      proposals_sent: prev.proposals_sent + 1,
      connects_spent: prev.connects_spent + cost,
    }));

    setNotification({
      type: 'success',
      message: `Proposal approved and submitted! Deducted ${cost} Connects (Balance: ${settings.connects_balance - cost}).`,
    });

    try {
      await api.submitProposal(proposalId, editedContent);
    } catch (e) {
      // Handled locally
    }
  };

  const rejectProposalAction = async (proposalId: string, feedback: string) => {
    const newRule: MemoryRule = {
      id: `rule-mem-${Date.now()}`,
      source_proposal_id: proposalId,
      rule_text: feedback,
      confidence: 0.95,
      created_at: 'Just now',
      category: 'tone',
    };

    setRules(prev => [newRule, ...prev]);

    setProposals(prev => prev.map(p => {
      if (p.id === proposalId) {
        return { ...p, status: 'lost', feedback };
      }
      return p;
    }));

    setNotification({
      type: 'info',
      message: `Proposal rejected. Feedback distilled and promoted to Long-Term Memory Store: "${feedback}".`,
    });

    try {
      await api.rejectProposal(proposalId, feedback);
    } catch (e) {
      // Handled locally
    }
  };

  const bookInterviewSlotAction = async (threadId: string, slot: string) => {
    setMessages(prev => prev.map(t => {
      if (t.id === threadId) {
        return {
          ...t,
          booked_slot: slot,
          messages: [
            ...t.messages,
            {
              id: `msg-${Date.now()}`,
              sender: 'agent',
              text: `Interview hold confirmed via Workspace MCP for: ${slot}. Calendar invitation dispatched.`,
              timestamp: 'Just now',
            },
          ],
        };
      }
      return t;
    }));

    setNotification({
      type: 'success',
      message: `Calendar hold confirmed for ${slot} via Workspace MCP.`,
    });

    try {
      await api.bookInterviewSlot(threadId, slot);
    } catch (e) {
      // Handled locally
    }
  };

  const sendClientMessageAction = async (threadId: string, text: string) => {
    setMessages(prev => prev.map(t => {
      if (t.id === threadId) {
        return {
          ...t,
          messages: [
            ...t.messages,
            {
              id: `msg-${Date.now()}`,
              sender: 'user',
              text,
              timestamp: 'Just now',
            },
          ],
        };
      }
      return t;
    }));

    setNotification({ type: 'success', message: 'Message dispatched to client.' });

    try {
      await api.sendMessage(threadId, text);
    } catch (e) {
      // Handled locally
    }
  };

  const deleteMemoryRuleAction = async (ruleId: string) => {
    setRules(prev => prev.filter(r => r.id !== ruleId));
    setNotification({ type: 'info', message: 'Learned rule successfully deleted from Memory Store.' });

    try {
      await api.deleteMemoryRule(ruleId);
    } catch (e) {
      // Handled locally
    }
  };

  const updateSettingsAction = async (newSettings: Partial<UserSettings>) => {
    setSettings(prev => ({ ...prev, ...newSettings }));
    setNotification({ type: 'success', message: 'Settings saved successfully.' });

    try {
      await api.updateSettings(newSettings);
    } catch (e) {
      // Handled locally
    }
  };

  const triggerScoutAction = async () => {
    setNotification({ type: 'info', message: 'Scout agent scanning Upwork marketplace...' });
    setTimeout(() => {
      setNotification({ type: 'success', message: 'Scout complete: 3 new matching jobs indexed.' });
    }, 1200);
  };

  const toggleDegradedMode = () => {
    const newState = !settings.degraded_mode_simulated;
    setSettings(prev => ({ ...prev, degraded_mode_simulated: newState }));
    if (newState) {
      setNotification({
        type: 'warning',
        message: 'Degraded Mode Activated: Upwork API throttled/down. Seamlessly switched to local GigSim simulator fallback.',
      });
    } else {
      setNotification({
        type: 'success',
        message: 'Live Mode Restored: Connected directly to Upwork Marketplace adapter.',
      });
    }
  };

  const setPersona = (persona: PersonaType) => {
    setSettings(prev => ({ ...prev, persona }));
    setNotification({ type: 'info', message: `Active persona switched to: ${persona.replace('_', ' ').toUpperCase()}` });
  };

  return (
    <AppContext.Provider
      value={{
        currentView,
        setCurrentView,
        selectedJobId,
        setSelectedJobId,
        selectedProposalId,
        setSelectedProposalId,
        selectedThreadId,
        setSelectedThreadId,
        selectedRunId,
        setSelectedRunId,
        jobs,
        proposals,
        messages,
        runs,
        rules,
        settings,
        analytics,
        selectJobForDetail,
        openProposalStudio,
        submitProposalAction,
        rejectProposalAction,
        bookInterviewSlotAction,
        sendClientMessageAction,
        deleteMemoryRuleAction,
        updateSettingsAction,
        triggerScoutAction,
        toggleDegradedMode,
        setPersona,
        notification,
        setNotification,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
