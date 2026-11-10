import { Job, Proposal, MessageThread, AgentRun, MemoryRule, UserSettings, AnalyticsSummary } from '../types';
import { INITIAL_JOBS, INITIAL_PROPOSALS, INITIAL_MESSAGES, INITIAL_RUNS, INITIAL_RULES, INITIAL_ANALYTICS } from './mockData';

const BASE_URL = '/api';

class ApiService {
  private token: string | null = null;

  setToken(token: string | null) {
    this.token = token;
    if (token) {
      localStorage.setItem('gigbid_token', token);
    } else {
      localStorage.removeItem('gigbid_token');
    }
  }

  getToken(): string | null {
    if (!this.token) {
      this.token = localStorage.getItem('gigbid_token');
    }
    return this.token;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}, fallbackData?: T): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(`${BASE_URL}${endpoint}`, {
        ...options,
        headers,
      });

      if (!response.ok) {
        throw new Error(`API error ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (err) {
      console.warn(`Request failed to ${endpoint}, falling back to local state:`, err);
      if (fallbackData !== undefined) {
        return fallbackData;
      }
      throw err;
    }
  }

  // Jobs
  async getJobs(): Promise<Job[]> {
    return this.request<Job[]>('/jobs', {}, INITIAL_JOBS);
  }

  async getJob(id: string): Promise<Job> {
    const fallback = INITIAL_JOBS.find(j => j.id === id) || INITIAL_JOBS[0];
    return this.request<Job>(`/jobs/${id}`, {}, fallback);
  }

  async triggerScout(): Promise<{ status: string; new_jobs: number }> {
    return this.request('/jobs/scout', { method: 'POST' }, { status: 'completed', new_jobs: 3 });
  }

  // Proposals
  async getProposals(): Promise<Proposal[]> {
    return this.request<Proposal[]>('/proposals', {}, INITIAL_PROPOSALS);
  }

  async getProposal(id: string): Promise<Proposal> {
    const fallback = INITIAL_PROPOSALS.find(p => p.id === id) || INITIAL_PROPOSALS[0];
    return this.request<Proposal>(`/proposals/${id}`, {}, fallback);
  }

  async generateProposal(jobId: string, persona: string): Promise<Proposal> {
    return this.request<Proposal>(
      `/proposals/generate`,
      {
        method: 'POST',
        body: JSON.stringify({ job_id: jobId, persona }),
      },
      INITIAL_PROPOSALS[0]
    );
  }

  async submitProposal(proposalId: string, editedContent?: string): Promise<{ success: boolean; connects_remaining: number }> {
    return this.request(
      `/proposals/${proposalId}/submit`,
      {
        method: 'POST',
        body: JSON.stringify({ proposal_id: proposalId, content: editedContent }),
      },
      { success: true, connects_remaining: 134 }
    );
  }

  async rejectProposal(proposalId: string, feedback: string): Promise<{ success: boolean; rule_created?: MemoryRule }> {
    return this.request(
      `/proposals/${proposalId}/reject`,
      {
        method: 'POST',
        body: JSON.stringify({ proposal_id: proposalId, feedback }),
      },
      {
        success: true,
        rule_created: {
          id: `rule-mem-${Date.now()}`,
          source_proposal_id: proposalId,
          rule_text: feedback,
          confidence: 0.95,
          created_at: 'Just now',
          category: 'pricing',
        },
      }
    );
  }

  // Approvals
  async getPendingApprovals(): Promise<Proposal[]> {
    return this.request<Proposal[]>('/approvals', {}, INITIAL_PROPOSALS.filter(p => p.status === 'drafted'));
  }

  // Messages
  async getMessages(): Promise<MessageThread[]> {
    return this.request<MessageThread[]>('/messages', {}, INITIAL_MESSAGES);
  }

  async sendMessage(threadId: string, text: string): Promise<{ success: boolean }> {
    return this.request(
      `/messages/${threadId}/reply`,
      {
        method: 'POST',
        body: JSON.stringify({ message: text }),
      },
      { success: true }
    );
  }

  async bookInterviewSlot(threadId: string, slot: string): Promise<{ success: boolean; hold_id: string }> {
    return this.request(
      `/messages/${threadId}/book-slot`,
      {
        method: 'POST',
        body: JSON.stringify({ slot }),
      },
      { success: true, hold_id: `hld-${Date.now()}` }
    );
  }

  // Runs
  async getRuns(): Promise<AgentRun[]> {
    return this.request<AgentRun[]>('/runs', {}, INITIAL_RUNS);
  }

  async getRun(runId: string): Promise<AgentRun> {
    const fallback = INITIAL_RUNS.find(r => r.run_id === runId) || INITIAL_RUNS[0];
    return this.request<AgentRun>(`/runs/${runId}`, {}, fallback);
  }

  // Analytics
  async getAnalytics(): Promise<AnalyticsSummary> {
    return this.request<AnalyticsSummary>('/analytics', {}, INITIAL_ANALYTICS);
  }

  // Settings & Memory
  async getSettings(): Promise<UserSettings> {
    return this.request<UserSettings>(
      '/settings',
      {},
      {
        persona: 'ai_engineer',
        autonomy_level: 'draft_and_ask',
        hourly_rate_floor: 75,
        max_daily_connects: 40,
        connects_balance: 150,
        degraded_mode_simulated: false,
        min_client_rating: 4.5,
        auto_submit_confidence_threshold: 0.95,
      }
    );
  }

  async updateSettings(settings: Partial<UserSettings>): Promise<UserSettings> {
    return this.request<UserSettings>(
      '/settings',
      {
        method: 'PATCH',
        body: JSON.stringify(settings),
      },
      {
        persona: 'ai_engineer',
        autonomy_level: settings.autonomy_level || 'draft_and_ask',
        hourly_rate_floor: settings.hourly_rate_floor || 75,
        max_daily_connects: settings.max_daily_connects || 40,
        connects_balance: settings.connects_balance || 150,
        degraded_mode_simulated: settings.degraded_mode_simulated ?? false,
        min_client_rating: 4.5,
        auto_submit_confidence_threshold: 0.95,
      }
    );
  }

  async getMemoryRules(): Promise<MemoryRule[]> {
    return this.request<MemoryRule[]>('/settings/memory-rules', {}, INITIAL_RULES);
  }

  async deleteMemoryRule(id: string): Promise<{ success: boolean }> {
    return this.request(
      `/settings/memory-rules/${id}`,
      { method: 'DELETE' },
      { success: true }
    );
  }
}

export const api = new ApiService();

