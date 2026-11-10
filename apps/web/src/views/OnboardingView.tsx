import React from 'react';
import { useApp } from '../context/AppContext';
import { 
  UserCheck, 
  Cpu, 
  Code2, 
  BarChart, 
  CheckCircle, 
  ArrowRight, 
  ShieldCheck, 
  Layers, 
  KeyRound, 
  Zap 
} from 'lucide-react';
import { PersonaType } from '../types';

export const OnboardingView: React.FC = () => {
  const { settings, setPersona, setCurrentView } = useApp();

  const personas: {
    id: PersonaType;
    title: string;
    icon: React.ElementType;
    tagline: string;
    caseStudiesCount: number;
    hourlyFloor: number;
    specialties: string[];
  }[] = [
    {
      id: 'ai_engineer',
      title: 'AI & LLM Engineer',
      icon: Cpu,
      tagline: 'Specialized in LangGraph multi-agent orchestration, hybrid RAG, and sub-100ms model inference.',
      caseStudiesCount: 20,
      hourlyFloor: 75,
      specialties: ['LangGraph', 'FastAPI', 'Hybrid RAG', 'Qdrant', 'Cross-Encoder', 'PyTorch'],
    },
    {
      id: 'fullstack_dev',
      title: 'Full-Stack Developer',
      icon: Code2,
      tagline: 'Production Next.js, FastAPI, PostgreSQL, and scalable microservices architecture.',
      caseStudiesCount: 20,
      hourlyFloor: 65,
      specialties: ['React/Next.js', 'Node.js', 'PostgreSQL', 'Docker', 'GraphQL', 'Tailwind'],
    },
    {
      id: 'data_analyst',
      title: 'Data Analyst & BI Specialist',
      icon: BarChart,
      tagline: 'Predictive analytics, automated SQL dbt modeling, and executive KPI intelligence dashboards.',
      caseStudiesCount: 20,
      hourlyFloor: 55,
      specialties: ['SQL/dbt', 'Python Pandas', 'Tableau', 'BigQuery', 'Snowflake', 'Statistics'],
    },
  ];

  return (
    <div className="space-y-8 max-w-5xl mx-auto py-4">
      {/* Welcome Banner */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center space-x-2 bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 px-3 py-1 rounded-full text-xs font-semibold">
          <Zap className="w-3.5 h-3.5 text-indigo-400" />
          <span>Multi-Tenant Freelancer Profile Setup</span>
        </div>
        <h1 className="text-3xl font-black text-white tracking-tight sm:text-4xl">
          Select Your Active Freelance Persona
        </h1>
        <p className="text-sm text-slate-400 max-w-xl mx-auto">
          GigBid adapts its grounding corpus, case studies, pricing heuristics, and tone to match your chosen professional domain.
        </p>
      </div>

      {/* 3 Persona Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {personas.map((p) => {
          const Icon = p.icon;
          const isSelected = settings.persona === p.id;

          return (
            <div
              key={p.id}
              onClick={() => setPersona(p.id)}
              className={`p-6 rounded-2xl border cursor-pointer transition-all flex flex-col justify-between space-y-4 shadow-xl ${
                isSelected
                  ? 'bg-gradient-to-b from-indigo-950/60 to-slate-900 border-indigo-500 ring-2 ring-indigo-500/30'
                  : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className={`p-2.5 rounded-xl ${isSelected ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300'}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  {isSelected && (
                    <span className="bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 text-[10px] px-2 py-0.5 rounded-full font-bold uppercase">
                      Active Persona
                    </span>
                  )}
                </div>

                <h3 className="text-lg font-bold text-white">{p.title}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{p.tagline}</p>
              </div>

              <div className="space-y-3 pt-3 border-t border-slate-800/80 text-xs">
                <div className="flex justify-between text-slate-400">
                  <span>Indexed Case Studies:</span>
                  <span className="font-bold text-white font-mono">{p.caseStudiesCount} verified</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Target Hourly Floor:</span>
                  <span className="font-bold text-emerald-400 font-mono">${p.hourlyFloor}/hr</span>
                </div>

                <div className="flex flex-wrap gap-1 pt-1">
                  {p.specialties.slice(0, 4).map((s, idx) => (
                    <span key={idx} className="bg-slate-800 text-slate-300 text-[10px] px-2 py-0.5 rounded">
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Integration Checks & Launch */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl">
        <div className="flex flex-wrap items-center gap-6 text-xs text-slate-300">
          <div className="flex items-center space-x-2">
            <CheckCircle className="w-4 h-4 text-emerald-400" />
            <span>Portfolio MCP Server Ready</span>
          </div>
          <div className="flex items-center space-x-2">
            <CheckCircle className="w-4 h-4 text-emerald-400" />
            <span>RAG Index Active (BM25 + Dense)</span>
          </div>
          <div className="flex items-center space-x-2">
            <CheckCircle className="w-4 h-4 text-emerald-400" />
            <span>Multi-Agent LangGraph Ready</span>
          </div>
        </div>

        <button
          onClick={() => setCurrentView('inbox')}
          className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-6 py-3 rounded-xl text-xs flex items-center space-x-2 transition shadow-lg shadow-indigo-600/30 shrink-0"
        >
          <span>Launch Copilot Workspace</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

