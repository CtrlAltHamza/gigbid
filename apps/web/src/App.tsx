import React from 'react';
import { useApp } from './context/AppContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { InboxView } from './views/InboxView';
import { JobDetailView } from './views/JobDetailView';
import { ProposalStudioView } from './views/ProposalStudioView';
import { PipelineBoardView } from './views/PipelineBoardView';
import { MessagesView } from './views/MessagesView';
import { AgentRunViewerView } from './views/AgentRunViewerView';
import { AnalyticsView } from './views/AnalyticsView';
import { SettingsView } from './views/SettingsView';
import { OnboardingView } from './views/OnboardingView';

export const AppContent: React.FC = () => {
  const { currentView } = useApp();

  const renderView = () => {
    switch (currentView) {
      case 'inbox':
        return <InboxView />;
      case 'job_detail':
        return <JobDetailView />;
      case 'proposal_studio':
        return <ProposalStudioView />;
      case 'pipeline':
        return <PipelineBoardView />;
      case 'messages':
        return <MessagesView />;
      case 'runs':
        return <AgentRunViewerView />;
      case 'analytics':
        return <AnalyticsView />;
      case 'settings':
        return <SettingsView />;
      case 'onboarding':
        return <OnboardingView />;
      default:
        return <InboxView />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col font-sans">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-8 overflow-y-auto max-h-[calc(100vh-61px)]">
          {renderView()}
        </main>
      </div>
    </div>
  );
};

