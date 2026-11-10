import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { 
  MessageSquare, 
  Send, 
  Calendar, 
  CheckCircle, 
  Clock, 
  User, 
  Sparkles, 
  AlertTriangle, 
  ShieldAlert,
  ArrowRight
} from 'lucide-react';
import { MessageThread } from '../types';

export const MessagesView: React.FC = () => {
  const { messages, selectedThreadId, setSelectedThreadId, bookInterviewSlotAction, sendClientMessageAction } = useApp();

  const activeThread = messages.find(m => m.id === selectedThreadId) || messages[0];
  const [replyText, setReplyText] = useState<string>(activeThread?.suggested_reply || '');

  const handleSelectThread = (thread: MessageThread) => {
    setSelectedThreadId(thread.id);
    setReplyText(thread.suggested_reply);
  };

  const handleSend = async () => {
    if (!replyText.trim()) return;
    await sendClientMessageAction(activeThread.id, replyText);
    setReplyText('');
  };

  const handleBookSlot = async (slot: string) => {
    await bookInterviewSlotAction(activeThread.id, slot);
  };

  const getIntentBadge = (intent: string) => {
    switch (intent) {
      case 'interview_invite':
        return (
          <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider flex items-center space-x-1">
            <Calendar className="w-3 h-3 text-emerald-400" />
            <span>Interview Invite</span>
          </span>
        );
      case 'scope_question':
        return (
          <span className="bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">
            Scope Inquiry
          </span>
        );
      case 'price_negotiation':
        return (
          <span className="bg-amber-500/20 text-amber-300 border border-amber-500/30 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">
            Price Negotiation
          </span>
        );
      case 'scam_offplatform':
        return (
          <span className="bg-rose-500/20 text-rose-300 border border-rose-500/30 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider flex items-center space-x-1">
            <ShieldAlert className="w-3 h-3 text-rose-400" />
            <span>Off-Platform Threat</span>
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-black text-white tracking-tight">Client Messaging & Workspace MCP</h1>
        <p className="text-sm text-slate-400">
          Inbound client communications with automated intent extraction, calendar slot hold booking, and liaison suggested replies.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl min-h-[620px]">
        {/* Left Column (1 col): Threads list */}
        <div className="border-r border-slate-800 flex flex-col bg-slate-950/40">
          <div className="p-4 border-b border-slate-800 text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center justify-between">
            <span>Conversations</span>
            <span className="text-indigo-400">{messages.length}</span>
          </div>

          <div className="divide-y divide-slate-800/80 overflow-y-auto flex-1">
            {messages.map((thread) => {
              const isSelected = thread.id === activeThread.id;
              const lastMsg = thread.messages[thread.messages.length - 1];

              return (
                <button
                  key={thread.id}
                  onClick={() => handleSelectThread(thread)}
                  className={`w-full p-4 text-left transition space-y-2 block ${
                    isSelected ? 'bg-indigo-950/40 border-l-4 border-indigo-500' : 'hover:bg-slate-800/30'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-white truncate max-w-[150px]">{thread.client_name}</span>
                    <span className="text-[10px] text-slate-400">{lastMsg?.timestamp}</span>
                  </div>

                  <p className="text-[11px] font-medium text-indigo-300 truncate">{thread.job_title}</p>

                  <div className="flex items-center justify-between">
                    {getIntentBadge(thread.intent)}
                    {thread.unread && (
                      <span className="w-2 h-2 rounded-full bg-indigo-500 ring-2 ring-indigo-400/40" />
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Column (2 cols): Message Thread + Workspace MCP Slot Booker */}
        <div className="md:col-span-2 flex flex-col justify-between p-6 bg-slate-900">
          {/* Thread Header */}
          <div className="border-b border-slate-800 pb-4 mb-4 flex items-center justify-between">
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-base font-bold text-white">{activeThread.client_name}</h3>
                {getIntentBadge(activeThread.intent)}
              </div>
              <p className="text-xs text-slate-400 mt-0.5">{activeThread.job_title}</p>
            </div>
            <span className="text-xs bg-slate-800 text-slate-400 px-2.5 py-1 rounded-md font-mono">
              Job: {activeThread.job_id}
            </span>
          </div>

          {/* Message History */}
          <div className="space-y-3 overflow-y-auto flex-1 pr-2 mb-4">
            {activeThread.messages.map((msg) => {
              const isClient = msg.sender === 'client';
              const isAgent = msg.sender === 'agent';

              return (
                <div
                  key={msg.id}
                  className={`flex flex-col ${isClient ? 'items-start' : 'items-end'}`}
                >
                  <div className="flex items-center space-x-1.5 text-[10px] text-slate-400 mb-1">
                    <span>{isClient ? activeThread.client_name : isAgent ? 'GigBid Agent' : 'You (Freelancer)'}</span>
                    <span>• {msg.timestamp}</span>
                  </div>
                  <div
                    className={`p-3.5 rounded-2xl max-w-lg text-xs leading-relaxed ${
                      isClient
                        ? 'bg-slate-800 text-slate-200 border border-slate-700/80 rounded-tl-none'
                        : isAgent
                        ? 'bg-indigo-950/60 text-indigo-200 border border-indigo-700/60 rounded-tr-none'
                        : 'bg-indigo-600 text-white rounded-tr-none shadow-lg shadow-indigo-600/20'
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              );
            })}

            {/* Workspace MCP Calendar Slot Booking Widget */}
            {activeThread.available_slots && activeThread.available_slots.length > 0 && (
              <div className="my-4 p-4 rounded-xl bg-slate-950/80 border border-indigo-500/40 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2 text-xs font-bold text-indigo-300">
                    <Calendar className="w-4 h-4 text-indigo-400" />
                    <span>Workspace MCP: Calendar Hold Availability</span>
                  </div>
                  <span className="text-[10px] text-slate-400 font-mono">mcp/workspace/hold_calendar_slot</span>
                </div>

                <p className="text-xs text-slate-300">
                  Client requested an intro call. Select an open calendar slot to place a tentative hold and offer it:
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                  {activeThread.available_slots.map((slot, idx) => {
                    const isBooked = activeThread.booked_slot === slot;
                    return (
                      <button
                        key={idx}
                        disabled={isBooked}
                        onClick={() => handleBookSlot(slot)}
                        className={`p-2.5 rounded-lg text-xs font-medium text-left border transition ${
                          isBooked
                            ? 'bg-emerald-950/60 border-emerald-500 text-emerald-300 font-bold'
                            : 'bg-slate-900 border-slate-800 hover:border-indigo-500 text-slate-200'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-[10px] text-slate-400">Slot {idx + 1}</span>
                          {isBooked && <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />}
                        </div>
                        <div className="text-[11px] leading-tight">{slot}</div>
                        {isBooked ? (
                          <span className="text-[10px] text-emerald-400 mt-1 block">Hold Confirmed</span>
                        ) : (
                          <span className="text-[10px] text-indigo-400 mt-1 block hover:underline">Click to Hold</span>
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </div>

          {/* Suggested Reply & Action Box */}
          <div className="space-y-3 pt-3 border-t border-slate-800">
            {activeThread.suggested_reply && (
              <div className="flex items-center justify-between text-xs bg-slate-950/60 px-3 py-1.5 rounded-lg border border-slate-800 text-slate-300">
                <div className="flex items-center space-x-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                  <span className="text-[11px] font-semibold text-slate-400">Client Liaison Agent Suggestion</span>
                </div>
                <button
                  onClick={() => setReplyText(activeThread.suggested_reply)}
                  className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold"
                >
                  Use Template
                </button>
              </div>
            )}

            <div className="flex items-end space-x-2">
              <textarea
                rows={3}
                value={replyText}
                onChange={(e) => setReplyText(e.target.value)}
                placeholder="Type your response to client or customize agent suggestion..."
                className="flex-1 bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-200 focus:outline-none focus:border-indigo-500 resize-none font-sans"
              />
              <button
                onClick={handleSend}
                className="bg-indigo-600 hover:bg-indigo-500 text-white p-3 rounded-xl transition shadow-lg shadow-indigo-600/30 shrink-0"
                title="Send Message"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
