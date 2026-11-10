import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { 
  PlayCircle, 
  CheckCircle2, 
  Clock, 
  AlertCircle, 
  Cpu, 
  ExternalLink, 
  Zap, 
  Layers, 
  Terminal, 
  Activity,
  ArrowRight
} from 'lucide-react';
import { AgentRun, AgentNodeRun } from '../types';

export const AgentRunViewerView: React.FC = () => {
  const { runs, selectedRunId, setSelectedRunId, openProposalStudio } = useApp();

  const activeRun: AgentRun = runs.find(r => r.run_id === selectedRunId) || runs[0];
  const [selectedNodeName, setSelectedNodeName] = useState<string>('critic');

  const selectedNode = activeRun.nodes.find(n => n.node_name === selectedNodeName) || activeRun.nodes[0];

  const totalTokens = activeRun.nodes.reduce((acc, n) => acc + (n.tokens_used || 0), 0);
  const totalCost = activeRun.nodes.reduce((acc, n) => acc + (n.cost_usd || 0), 0);
  const totalLatency = activeRun.nodes.reduce((acc, n) => acc + (n.latency_ms || 0), 0);

  const getNodeStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="w-4 h-4 text-emerald-400" />;
      case 'running':
        return <Activity className="w-4 h-4 text-indigo-400 animate-spin" />;
      case 'interrupted':
        return <Clock className="w-4 h-4 text-amber-400 animate-pulse" />;
      case 'failed':
        return <AlertCircle className="w-4 h-4 text-rose-400" />;
      default:
        return <div className="w-3 h-3 rounded-full bg-slate-700" />;
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-2xl font-black text-white tracking-tight">Agent Run Inspector</h1>
            <span className="bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-xs px-2.5 py-0.5 rounded-full font-mono">
              Live SSE Active
            </span>
          </div>
          <p className="text-sm text-slate-400">
            Node-by-node LangGraph execution trace, parallel handoff envelopes, token telemetry, and human-in-the-loop interrupts.
          </p>
        </div>

        {/* Trace Link */}
        <div className="flex items-center space-x-3">
          <a
            href={`https://smith.langchain.com/o/gigbid/traces/${activeRun.trace_id}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-1.5 bg-slate-900 hover:bg-slate-800 text-indigo-300 border border-slate-800 px-3 py-1.5 rounded-xl text-xs font-semibold transition"
          >
            <span>Trace ID: {activeRun.trace_id.slice(0, 16)}...</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>

      {/* Telemetry Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Run Status</div>
          <div className="text-lg font-bold text-amber-400 capitalize mt-1 flex items-center space-x-1.5">
            <Clock className="w-4 h-4" />
            <span>Awaiting Approval</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Total Latency</div>
          <div className="text-lg font-bold text-white mt-1 font-mono">
            {(totalLatency / 1000).toFixed(2)}s
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Total Tokens Used</div>
          <div className="text-lg font-bold text-white mt-1 font-mono">
            {totalTokens.toLocaleString()} tok
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Estimated Run Cost</div>
          <div className="text-lg font-bold text-emerald-400 mt-1 font-mono">
            ${totalCost.toFixed(4)}
          </div>
        </div>
      </div>

      {/* Main Execution Flow & Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column (1 col): Node timeline */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              LangGraph Superstep DAG
            </span>
            <span className="text-[11px] text-slate-500 font-mono">
              {activeRun.nodes.length} nodes
            </span>
          </div>

          <div className="space-y-2">
            {activeRun.nodes.map((node, idx) => {
              const isSelected = node.node_name === selectedNodeName;
              return (
                <button
                  key={idx}
                  onClick={() => setSelectedNodeName(node.node_name)}
                  className={`w-full text-left p-3 rounded-xl border text-xs font-medium transition flex items-center justify-between ${
                    isSelected
                      ? 'bg-indigo-600 text-white border-indigo-500 shadow-md'
                      : 'bg-slate-950/60 text-slate-300 border-slate-800/80 hover:bg-slate-800/40'
                  }`}
                >
                  <div className="flex items-center space-x-2.5">
                    {getNodeStatusBadge(node.status)}
                    <span className="font-mono uppercase tracking-wide text-[11px]">{node.node_name}</span>
                  </div>
                  <div className="flex items-center space-x-2 text-[10px]">
                    {node.latency_ms && (
                      <span className={isSelected ? 'text-indigo-200' : 'text-slate-500'}>
                        {node.latency_ms}ms
                      </span>
                    )}
                    {node.status === 'interrupted' && (
                      <span className="bg-amber-400/20 text-amber-300 px-1.5 py-0.5 rounded text-[9px] font-bold">
                        INTERRUPT
                      </span>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Column (2 cols): Selected Node Deep-Dive Inspector */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <div className="flex items-center space-x-2">
                <Terminal className="w-4 h-4 text-indigo-400" />
                <h3 className="text-base font-bold text-white uppercase tracking-wider font-mono">
                  Node Inspector: {selectedNode.node_name}
                </h3>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Detailed input state, handoff envelope, token count, and emitted state updates.
              </p>
            </div>

            <div className="flex items-center space-x-2">
              <span className={`px-2.5 py-1 rounded-md text-xs font-bold uppercase font-mono ${
                selectedNode.status === 'completed' 
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
              }`}>
                {selectedNode.status}
              </span>
            </div>
          </div>

          {/* Node Metrics */}
          <div className="grid grid-cols-3 gap-3 text-xs">
            <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-500 text-[10px] uppercase font-bold block">Latency</span>
              <span className="text-sm font-bold text-white font-mono">{selectedNode.latency_ms || 'Paused'} ms</span>
            </div>
            <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-500 text-[10px] uppercase font-bold block">Tokens Used</span>
              <span className="text-sm font-bold text-white font-mono">{selectedNode.tokens_used || 0} tokens</span>
            </div>
            <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-500 text-[10px] uppercase font-bold block">Inference Cost</span>
              <span className="text-sm font-bold text-emerald-400 font-mono">${(selectedNode.cost_usd || 0).toFixed(4)}</span>
            </div>
          </div>

          {/* State / Handoff Summary */}
          <div className="space-y-2">
            <div className="text-xs font-bold uppercase tracking-wider text-slate-400">
              State Reducer Output Payload (Handoff)
            </div>
            <pre className="bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs font-mono text-indigo-300 overflow-x-auto leading-relaxed">
              {JSON.stringify(selectedNode.output_summary || { status: 'Awaiting human decision in Human-in-the-Loop interrupt' }, null, 2)}
            </pre>
          </div>

          {/* Action trigger if interrupted */}
          {selectedNode.status === 'interrupted' && (
            <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 flex items-center justify-between">
              <div>
                <h4 className="text-xs font-bold text-amber-300">Human Approval Gate Triggered</h4>
                <p className="text-[11px] text-slate-300">
                  LangGraph workflow suspended execution at <code className="text-amber-300">interrupt()</code> before dispatching Connects.
                </p>
              </div>
              <button
                onClick={() => openProposalStudio('prop-ai-101')}
                className="bg-amber-500 hover:bg-amber-400 text-slate-950 px-3.5 py-1.5 rounded-lg text-xs font-bold transition flex items-center space-x-1"
              >
                <span>Resume in Studio</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

