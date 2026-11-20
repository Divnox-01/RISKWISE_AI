import React, { useState, useEffect } from 'react';
import { investigationAPI } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';
import { FileSearch, Plus, Send, Clock, User, ShieldAlert, CheckCircle2 } from 'lucide-react';

export const InvestigationCenter = () => {
  const [investigations, setInvestigations] = useState([]);
  const [selectedInv, setSelectedInv] = useState(null);
  const [loading, setLoading] = useState(true);
  const [newNote, setNewNote] = useState('');
  const [submittingNote, setSubmittingNote] = useState(false);

  const fetchInvestigations = async () => {
    setLoading(true);
    try {
      const res = await investigationAPI.list();
      setInvestigations(res.data);
      if (res.data.length > 0 && !selectedInv) {
        setSelectedInv(res.data[0]);
      }
    } catch (err) {
      console.error("Fetch investigations error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInvestigations();
  }, []);

  const handleAddNote = async (e) => {
    e.preventDefault();
    if (!newNote.trim() || !selectedInv) return;
    setSubmittingNote(true);
    try {
      const res = await investigationAPI.addNote(selectedInv.id, { note_text: newNote });
      setSelectedInv({
        ...selectedInv,
        notes: [...selectedInv.notes, res.data]
      });
      setNewNote('');
    } catch (err) {
      console.error("Add note failed:", err);
    } finally {
      setSubmittingNote(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-bold text-white">Financial Crime Investigation Center</h2>
        <p className="text-xs text-slate-400">Formal AML/CFT case management with evidence dossiers and audit trails</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Cases List */}
        <div className="lg:col-span-5 space-y-3">
          <div className="flex items-center justify-between text-xs text-slate-400 px-1">
            <span>Active Cases ({investigations.length})</span>
          </div>

          {loading ? (
            <div className="p-8 text-center text-slate-500 bg-navy-900/60 rounded-xl border border-slate-800">
              <div className="w-5 h-5 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
              <span>Loading cases...</span>
            </div>
          ) : (
            investigations.map((inv) => (
              <div
                key={inv.id}
                onClick={() => setSelectedInv(inv)}
                className={`p-4 rounded-xl border cursor-pointer transition-all ${
                  selectedInv?.id === inv.id
                    ? "bg-navy-850 border-cyan-500/50 shadow-lg shadow-cyan-500/5"
                    : "bg-navy-900/80 border-slate-800 hover:border-slate-700"
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-mono text-xs font-bold text-cyan-400">{inv.case_number}</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                    inv.priority === 'P1' ? 'bg-rose-500/20 text-rose-300' : 'bg-amber-500/20 text-amber-300'
                  }`}>
                    Priority {inv.priority}
                  </span>
                </div>
                <h4 className="text-xs font-bold text-slate-200 line-clamp-1">{inv.title}</h4>
                <div className="flex items-center justify-between text-[11px] text-slate-400 mt-3 pt-2.5 border-t border-slate-800/80">
                  <span>Analyst: {inv.assigned_analyst || 'Unassigned'}</span>
                  <RiskBadge category={inv.status} />
                </div>
              </div>
            ))
          )}
        </div>

        {/* Selected Case Dossier */}
        <div className="lg:col-span-7 bg-navy-900/90 border border-slate-800 rounded-xl p-6">
          {selectedInv ? (
            <div className="space-y-6">
              <div className="border-b border-slate-800 pb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-mono text-xs font-bold text-cyan-400 bg-cyan-500/10 px-2.5 py-0.5 rounded border border-cyan-500/20">
                    {selectedInv.case_number}
                  </span>
                  <span className="text-xs text-slate-400">
                    Created: {new Date(selectedInv.created_at).toLocaleDateString()}
                  </span>
                </div>
                <h3 className="text-base font-extrabold text-white mt-1">{selectedInv.title}</h3>
                <p className="text-xs text-slate-400 mt-1">
                  Linked to Alert <strong className="font-mono text-slate-200">{selectedInv.alert_code}</strong> • Tx <strong className="font-mono text-slate-200">{selectedInv.tx_hash}</strong>
                </p>
              </div>

              {/* Case Summary */}
              <div className="p-4 bg-navy-950/70 border border-slate-800 rounded-lg text-xs space-y-2">
                <p className="font-bold uppercase tracking-wider text-slate-400 text-[10px]">Findings & Evidence Summary</p>
                <p className="text-slate-300 leading-relaxed">{selectedInv.findings_summary}</p>
                <div className="pt-2 flex items-center gap-4 text-slate-400 font-mono text-[11px]">
                  <span>Exposure: <strong className="text-white">${Number(selectedInv.amount || 0).toLocaleString()}</strong></span>
                  <span>Risk Score: <strong className="text-rose-400">{selectedInv.risk_score} / 100</strong></span>
                </div>
              </div>

              {/* Analyst Timeline Notes */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
                  <Clock className="w-3.5 h-3.5" />
                  <span>Analyst Audit Log & Notes ({selectedInv.notes?.length || 0})</span>
                </h4>

                <div className="space-y-3 max-h-56 overflow-y-auto pr-1">
                  {selectedInv.notes?.length === 0 ? (
                    <p className="text-xs text-slate-500 italic">No notes logged yet for this case.</p>
                  ) : (
                    selectedInv.notes.map((note) => (
                      <div key={note.id} className="p-3 bg-navy-950/50 border border-slate-800/80 rounded-lg text-xs space-y-1">
                        <div className="flex items-center justify-between text-[11px] text-slate-400">
                          <span className="font-semibold text-cyan-300 flex items-center gap-1.5">
                            <User className="w-3 h-3" />
                            {note.author_name} ({note.author_role})
                          </span>
                          <span className="text-[10px] text-slate-500">
                            {new Date(note.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </span>
                        </div>
                        <p className="text-slate-200">{note.note_text}</p>
                      </div>
                    ))
                  )}
                </div>

                {/* Add Note Form */}
                <form onSubmit={handleAddNote} className="mt-4 flex gap-2">
                  <input
                    type="text"
                    value={newNote}
                    onChange={(e) => setNewNote(e.target.value)}
                    placeholder="Append SAR observation, watchlist match, or compliance finding..."
                    className="flex-1 bg-navy-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
                  />
                  <button
                    type="submit"
                    disabled={submittingNote || !newNote.trim()}
                    className="px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-navy-950 font-bold rounded-lg text-xs flex items-center gap-1.5 transition-colors disabled:opacity-50"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>Post</span>
                  </button>
                </form>
              </div>
            </div>
          ) : (
            <div className="text-center py-24 text-slate-500 text-xs">
              Select an investigation case from the left panel to review evidence dossiers.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
