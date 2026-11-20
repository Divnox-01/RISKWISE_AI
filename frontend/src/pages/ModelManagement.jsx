import React, { useState } from 'react';
import { SlidersHorizontal, CheckCircle2, ShieldCheck, Cpu } from 'lucide-react';

export const ModelManagement = () => {
  const [weights, setWeights] = useState({
    xgb: 60,
    iforest: 25,
    rules: 15
  });

  const [thresholds, setThresholds] = useState({
    medium: 35,
    high: 65
  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <SlidersHorizontal className="w-5 h-5 text-cyan-400" />
          Model Governance & Registry
        </h2>
        <p className="text-xs text-slate-400">Configure multi-signal hybrid ensemble weights and classification thresholds</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Model Registry List */}
        <div className="bg-navy-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="text-sm font-bold text-white">Registered Model Artifacts</h3>
          <div className="space-y-3">
            <div className="p-4 rounded-xl border border-cyan-500/30 bg-navy-850">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-cyan-300">v2.0.0-prod</span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                  ACTIVE DEPLOYMENT
                </span>
              </div>
              <p className="text-xs text-slate-300 font-semibold mt-1">Hybrid Multi-Modal Ensemble</p>
              <p className="text-[11px] text-slate-400 mt-1">
                Supervised XGBoost (60%) + Isolation Forest (25%) + PaySim Rule Engine (15%) + SHAP TreeExplainer
              </p>
              <div className="flex gap-4 text-[10px] text-slate-500 font-mono mt-2 pt-2 border-t border-slate-800">
                <span>PR-AUC: 0.9994</span>
                <span>F1-Score: 0.9512</span>
                <span>Trained: 2026-11-20</span>
              </div>
            </div>

            <div className="p-4 rounded-xl border border-slate-800 bg-navy-950/40 opacity-70">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-slate-400">v1.2.0-legacy</span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                  ARCHIVED
                </span>
              </div>
              <p className="text-xs text-slate-400 font-semibold mt-1">Standalone Random Forest</p>
              <div className="flex gap-4 text-[10px] text-slate-500 font-mono mt-2 pt-2 border-t border-slate-800">
                <span>PR-AUC: 0.8240</span>
                <span>F1-Score: 0.7300</span>
              </div>
            </div>
          </div>
        </div>

        {/* Weights Configuration */}
        <div className="bg-navy-900/90 border border-slate-800 rounded-xl p-5 space-y-5">
          <div>
            <h3 className="text-sm font-bold text-white">Hybrid Ensemble Weighting</h3>
            <p className="text-xs text-slate-400">Normalized contribution towards the 0-100 composite risk score</p>
          </div>

          <div className="space-y-4 text-xs">
            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Supervised XGBoost Weight</span>
                <span className="font-mono font-bold text-cyan-400">{weights.xgb}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={weights.xgb}
                onChange={(e) => setWeights({ ...weights, xgb: parseInt(e.target.value) })}
                className="w-full accent-cyan-400"
              />
            </div>

            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Isolation Forest Anomaly Weight</span>
                <span className="font-mono font-bold text-blue-400">{weights.iforest}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={weights.iforest}
                onChange={(e) => setWeights({ ...weights, iforest: parseInt(e.target.value) })}
                className="w-full accent-blue-400"
              />
            </div>

            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Behavioural Rule Engine Weight</span>
                <span className="font-mono font-bold text-amber-400">{weights.rules}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={weights.rules}
                onChange={(e) => setWeights({ ...weights, rules: parseInt(e.target.value) })}
                className="w-full accent-amber-400"
              />
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800">
            <h4 className="text-xs font-bold text-white mb-2">Operational Triage Thresholds</h4>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 bg-navy-950/60 border border-slate-800 rounded-lg">
                <span className="text-[10px] text-slate-400 block">Medium Risk (Review)</span>
                <span className="text-lg font-mono font-bold text-amber-400">{thresholds.medium}</span>
              </div>
              <div className="p-3 bg-navy-950/60 border border-slate-800 rounded-lg">
                <span className="text-[10px] text-slate-400 block">High Risk (Block)</span>
                <span className="text-lg font-mono font-bold text-rose-400">{thresholds.high}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
