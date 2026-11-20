import React, { useState } from 'react';
import {
  Sparkles,
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  Play,
  AlertCircle,
  FileText
} from 'lucide-react';
import { mlAPI } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';
import { SHAPChart } from '../components/SHAPChart';

export const TransactionAnalysis = () => {
  const [formData, setFormData] = useState({
    step: 120,
    type: 'TRANSFER',
    amount: 450000.0,
    nameOrig: 'C104928371',
    oldbalanceOrg: 450000.0,
    nameDest: 'C902817293',
    oldbalanceDest: 0.0,
    persist: true
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const presets = [
    {
      label: "Critical Fraud (Drain + Empty Mule)",
      data: {
        step: 140,
        type: 'TRANSFER',
        amount: 650000.0,
        nameOrig: 'C819283746',
        oldbalanceOrg: 650000.0,
        nameDest: 'C192837465',
        oldbalanceDest: 0.0,
        persist: true
      }
    },
    {
      label: "Suspicious Cash-out (Large sum)",
      data: {
        step: 95,
        type: 'CASH_OUT',
        amount: 280000.0,
        nameOrig: 'C981726354',
        oldbalanceOrg: 300000.0,
        nameDest: 'C582910293',
        oldbalanceDest: 2000.0,
        persist: true
      }
    },
    {
      label: "Medium Risk (New Destination Wire)",
      data: {
        step: 60,
        type: 'TRANSFER',
        amount: 85000.0,
        nameOrig: 'C381928374',
        oldbalanceOrg: 150000.0,
        nameDest: 'C748291029',
        oldbalanceDest: 0.0,
        persist: true
      }
    },
    {
      label: "Genuine Routine Payment",
      data: {
        step: 30,
        type: 'PAYMENT',
        amount: 125.50,
        nameOrig: 'C291827364',
        oldbalanceOrg: 4200.0,
        nameDest: 'M291827364',
        oldbalanceDest: 0.0,
        persist: true
      }
    }
  ];

  const handleSubmit = async (e) => {
    e?.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await mlAPI.predict(formData);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Inference execution failed.");
    } finally {
      setLoading(false);
    }
  };

  const getActionTheme = (action) => {
    switch (action) {
      case 'BLOCK':
        return {
          border: 'border-rose-500/30',
          bg: 'bg-rose-500/10',
          text: 'text-rose-400',
          icon: ShieldAlert,
          title: 'IMMEDIATE TRANSACTION BLOCK'
        };
      case 'REVIEW':
        return {
          border: 'border-amber-500/30',
          bg: 'bg-amber-500/10',
          text: 'text-amber-400',
          icon: AlertTriangle,
          title: 'FLAGGED FOR ANALYST STEP-UP REVIEW'
        };
      default:
        return {
          border: 'border-emerald-500/30',
          bg: 'bg-emerald-500/10',
          text: 'text-emerald-400',
          icon: ShieldCheck,
          title: 'TRANSACTION APPROVED (LOW RISK)'
        };
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-navy-900 border border-slate-800 rounded-xl p-5">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-cyan-400" />
          Real-Time Transaction Inference & Explainability
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Execute live scoring across XGBoost, Isolation Forest anomaly scoring, and behavioural rules with SHAP feature explanations.
        </p>

        <div className="flex flex-wrap items-center gap-2 mt-4 pt-4 border-t border-slate-800/80">
          <span className="text-[11px] font-semibold text-slate-400 uppercase">Test Presets:</span>
          {presets.map((p, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => { setFormData(p.data); setResult(null); }}
              className="text-xs px-2.5 py-1 rounded bg-slate-800 hover:bg-cyan-500/20 hover:text-cyan-300 text-slate-300 border border-slate-700 transition-colors"
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-5 bg-navy-900/90 border border-slate-800 rounded-xl p-5">
          <h3 className="text-sm font-bold text-white mb-4">Transaction Payload</h3>

          <form onSubmit={handleSubmit} className="space-y-3.5 text-xs">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-400 mb-1 font-medium">Chronological Step (1-744)</label>
                <input
                  type="number"
                  min="1"
                  max="744"
                  value={formData.step}
                  onChange={(e) => setFormData({ ...formData, step: parseInt(e.target.value) || 1 })}
                  className="w-full bg-navy-950 border border-slate-800 rounded-lg px-3 py-2 text-white font-mono focus:border-cyan-500 focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-slate-400 mb-1 font-medium">Transaction Modality</label>
                <select
                  value={formData.type}
                  onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                  className="w-full bg-navy-950 border border-slate-800 rounded-lg px-3 py-2 text-white font-mono focus:border-cyan-500 focus:outline-none"
                >
                  <option value="TRANSFER">TRANSFER</option>
                  <option value="CASH_OUT">CASH_OUT</option>
                  <option value="PAYMENT">PAYMENT</option>
                  <option value="CASH_IN">CASH_IN</option>
                  <option value="DEBIT">DEBIT</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Transaction Amount ($ USD)</label>
              <input
                type="number"
                step="0.01"
                min="0.01"
                value={formData.amount}
                onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) || 0 })}
                className="w-full bg-navy-950 border border-slate-800 rounded-lg px-3 py-2 text-white font-mono text-sm font-bold focus:border-cyan-500 focus:outline-none"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-400 mb-1 font-medium">Origin Account ID</label>
                <input
                  type="text"
                  value={formData.nameOrig}
                  onChange={(e) => setFormData({ ...formData, nameOrig: e.target.value })}
                  className="w-full bg-navy-950 border border-slate-800 rounded-lg px-3 py-2 text-white font-mono focus:border-cyan-500 focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-slate-400 mb-1 font-medium">Initial Sender Balance ($)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.oldbalanceOrg}
                  onChange={(e) => setFormData({ ...formData, oldbalanceOrg: parseFloat(e.target.value) || 0 })}
                  className="w-full bg-navy-950 border border-slate-800 rounded-lg px-3 py-2 text-white font-mono focus:border-cyan-500 focus:outline-none"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-400 mb-1 font-medium">Destination Account ID</label>
                <input
                  type="text"
                  value={formData.nameDest}
                  onChange={(e) => setFormData({ ...formData, nameDest: e.target.value })}
                  className="w-full bg-navy-950 border border-slate-800 rounded-lg px-3 py-2 text-white font-mono focus:border-cyan-500 focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-slate-400 mb-1 font-medium">Initial Recipient Balance ($)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.oldbalanceDest}
                  onChange={(e) => setFormData({ ...formData, oldbalanceDest: parseFloat(e.target.value) || 0 })}
                  className="w-full bg-navy-950 border border-slate-800 rounded-lg px-3 py-2 text-white font-mono focus:border-cyan-500 focus:outline-none"
                  required
                />
              </div>
            </div>

            <div className="flex items-center gap-2 pt-2">
              <input
                type="checkbox"
                id="persist"
                checked={formData.persist}
                onChange={(e) => setFormData({ ...formData, persist: e.target.checked })}
                className="rounded bg-navy-950 border-slate-800 text-cyan-500 focus:ring-0"
              />
              <label htmlFor="persist" className="text-slate-400 select-none">
                Persist record and trigger automated alert if risk &gt;= 35
              </label>
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 px-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold rounded-xl flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20 transition-all disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Computing Multi-Modal Inference...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 fill-white" />
                    <span>Execute Inference & Explain</span>
                  </>
                )}
              </button>
            </div>
          </form>

          {error && (
            <div className="mt-4 p-3 bg-rose-500/10 border border-rose-500/20 rounded-lg text-rose-400 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>

        <div className="lg:col-span-7 space-y-5">
          {result ? (
            <>
              {(() => {
                const theme = getActionTheme(result.recommended_action);
                const Icon = theme.icon;
                return (
                  <div className={`p-5 rounded-xl border ${theme.border} ${theme.bg}`}>
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-3">
                        <div className={`p-2.5 rounded-lg bg-navy-950/60 ${theme.text}`}>
                          <Icon className="w-6 h-6" />
                        </div>
                        <div>
                          <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Risk Assessment Outcome</p>
                          <h3 className={`text-base font-extrabold ${theme.text}`}>{theme.title}</h3>
                        </div>
                      </div>
                      <div className="text-right">
                        <span className="text-[10px] text-slate-400 block uppercase">Composite Risk</span>
                        <span className="text-3xl font-black font-mono text-white">{result.risk_score}</span>
                        <span className="text-xs text-slate-400"> / 100</span>
                      </div>
                    </div>

                    <p className="text-xs text-slate-300 mt-3 pt-3 border-t border-slate-700/40">
                      {result.action_description}
                    </p>

                    {result.alert_created && (
                      <div className="mt-3 flex items-center gap-2 text-xs font-mono text-rose-300 bg-rose-950/40 px-3 py-1.5 rounded border border-rose-800/40">
                        <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
                        <span>Security Alert Generated: <strong>{result.alert_code}</strong></span>
                      </div>
                    )}
                  </div>
                );
              })()}

              <div className="bg-navy-900 border border-slate-800 rounded-xl p-5">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
                  Multi-Signal Model Breakdown
                </h4>
                <div className="grid grid-cols-3 gap-3 text-center">
                  <div className="p-3 bg-navy-950/60 rounded-lg border border-slate-800">
                    <p className="text-[10px] text-slate-400">Supervised XGBoost (60%)</p>
                    <p className="text-lg font-bold font-mono text-cyan-400 mt-0.5">
                      {(result.score_breakdown.xgb_fraud_probability * 100).toFixed(1)}%
                    </p>
                    <p className="text-[10px] text-slate-500 font-mono">+{result.score_breakdown.xgb_weighted_contribution.toFixed(1)} pts</p>
                  </div>
                  <div className="p-3 bg-navy-950/60 rounded-lg border border-slate-800">
                    <p className="text-[10px] text-slate-400">Isolation Forest (25%)</p>
                    <p className="text-lg font-bold font-mono text-blue-400 mt-0.5">
                      {(result.score_breakdown.isolation_forest_anomaly_score * 100).toFixed(1)}%
                    </p>
                    <p className="text-[10px] text-slate-500 font-mono">+{result.score_breakdown.isolation_forest_weighted_contribution.toFixed(1)} pts</p>
                  </div>
                  <div className="p-3 bg-navy-950/60 rounded-lg border border-slate-800">
                    <p className="text-[10px] text-slate-400">Rule Engine (15%)</p>
                    <p className="text-lg font-bold font-mono text-amber-400 mt-0.5">
                      {(result.score_breakdown.rule_engine_score * 100).toFixed(1)}%
                    </p>
                    <p className="text-[10px] text-slate-500 font-mono">+{result.score_breakdown.rule_engine_weighted_contribution.toFixed(1)} pts</p>
                  </div>
                </div>
              </div>

              <div className="bg-navy-900 border border-slate-800 rounded-xl p-5">
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                      SHAP Explainability Waterfall (Local Feature Drivers)
                    </h4>
                    <p className="text-[11px] text-slate-500">
                      Additive contribution to model log-odds. Red = elevates risk, Green = mitigates risk.
                    </p>
                  </div>
                  <span className="text-[10px] text-cyan-400 font-mono bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800">
                    TreeExplainer
                  </span>
                </div>

                <SHAPChart contributions={result.shap_explanation.all_contributions || result.shap_explanation.top_risk_drivers} />

                <div className="mt-3 space-y-1.5 pt-3 border-t border-slate-800 text-xs">
                  {result.shap_explanation.summary_insights?.map((insight, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-slate-300">
                      <span className="text-cyan-400 mt-0.5">•</span>
                      <span>{insight}</span>
                    </div>
                  ))}
                  <p className="text-[10px] text-slate-500 italic mt-2">
                    {result.shap_explanation.disclaimer}
                  </p>
                </div>
              </div>

              {result.rules?.flags?.length > 0 && (
                <div className="bg-navy-900 border border-slate-800 rounded-xl p-5">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
                    Triggered PaySim Typology Rules ({result.rules.flags.length})
                  </h4>
                  <div className="space-y-2">
                    {result.rules.flags.map((flag, idx) => (
                      <div key={idx} className="p-2.5 bg-navy-950/60 border border-slate-800 rounded-lg flex items-start gap-3">
                        <RiskBadge category={flag.severity} />
                        <div>
                          <p className="text-xs font-semibold text-slate-200">{flag.name}</p>
                          <p className="text-[11px] text-slate-400">{flag.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="bg-navy-900/60 border border-dashed border-slate-800 rounded-xl p-12 text-center flex flex-col items-center justify-center min-h-[420px]">
              <div className="w-12 h-12 rounded-xl bg-slate-800/80 flex items-center justify-center text-slate-400 mb-3">
                <FileText className="w-6 h-6 text-slate-500" />
              </div>
              <h4 className="text-sm font-bold text-slate-300">Awaiting Transaction Execution</h4>
              <p className="text-xs text-slate-500 max-w-sm mt-1">
                Configure transaction parameters on the left or select a preset to generate a real-time risk evaluation and SHAP waterfall explanation.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
