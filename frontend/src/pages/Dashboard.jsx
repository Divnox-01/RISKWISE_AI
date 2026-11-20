import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  ShieldAlert,
  ArrowUpRight,
  Percent,
  Clock,
  ExternalLink,
  ChevronRight,
  Zap
} from 'lucide-react';
import { StatCard } from '../components/StatCard';
import { RiskBadge } from '../components/RiskBadge';
import { analyticsAPI, transactionAPI, alertAPI } from '../services/api';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts';

export const Dashboard = () => {
  const [overview, setOverview] = useState(null);
  const [trends, setTrends] = useState([]);
  const [riskDist, setRiskDist] = useState([]);
  const [recentTransactions, setRecentTransactions] = useState([]);
  const [recentAlerts, setRecentAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [ovRes, trRes, distRes, txRes, altRes] = await Promise.all([
          analyticsAPI.overview(),
          analyticsAPI.trends(),
          analyticsAPI.riskDistribution(),
          transactionAPI.list({ limit: 6 }),
          alertAPI.list({ limit: 5 })
        ]);
        setOverview(ovRes.data);
        setTrends(trRes.data);
        setRiskDist(distRes.data);
        setRecentTransactions(txRes.data);
        setRecentAlerts(altRes.data);
      } catch (err) {
        console.error("Dashboard fetch error:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const COLORS = ['#10b981', '#f59e0b', '#ef4444'];

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-navy-900 via-navy-850 to-navy-900 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
            <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider">Multi-Modal Risk Engine</span>
          </div>
          <h2 className="text-xl font-extrabold text-white">Hybrid Fraud Intelligence Dashboard</h2>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Live evaluation across XGBoost (60%), Isolation Forest (25%), and PaySim Behavioural Rules (15%). Explainability powered by SHAP TreeExplainer.
          </p>
        </div>
        <div className="flex gap-3">
          <Link
            to="/analyze"
            className="flex items-center gap-2 px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-navy-950 font-bold rounded-xl text-xs transition-colors shadow-lg shadow-cyan-500/10"
          >
            <Zap className="w-4 h-4" />
            <span>Test Inference</span>
          </Link>
          <Link
            to="/alerts"
            className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold rounded-xl text-xs border border-slate-700 transition-colors"
          >
            <span>Review Alerts</span>
            <ChevronRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Transactions"
          value={overview?.total_transactions_analyzed?.toLocaleString() || "0"}
          subtitle="Processed through pipeline"
          icon={ArrowUpRight}
          color="blue"
        />
        <StatCard
          title="Fraud Detected"
          value={overview?.fraud_transactions_detected?.toLocaleString() || "0"}
          subtitle={`${overview?.fraud_detection_rate || 0}% overall fraud rate`}
          icon={ShieldAlert}
          color="rose"
        />
        <StatCard
          title="Average Risk Score"
          value={`${overview?.average_risk_score || 0} / 100`}
          subtitle="Multi-signal weighted index"
          icon={Percent}
          color="amber"
        />
        <StatCard
          title="Open Alerts"
          value={overview?.open_alerts_count?.toString() || "0"}
          subtitle={`${overview?.active_investigations_count || 0} in active investigation`}
          icon={Clock}
          color="cyan"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-navy-900/90 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-white">Fraud & Risk Trends</h3>
              <p className="text-xs text-slate-400">Hourly transaction volumes and elevated risk patterns</p>
            </div>
            <span className="text-[10px] font-mono text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20">
              PaySim 24h Windows
            </span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trends} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorTx" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="step_window" stroke="#475569" tick={{ fontSize: 10 }} />
                <YAxis stroke="#475569" tick={{ fontSize: 10 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '11px' }}
                />
                <Area type="monotone" dataKey="transaction_count" stroke="#06b6d4" fillOpacity={1} fill="url(#colorTx)" name="Volume" />
                <Area type="monotone" dataKey="high_risk_count" stroke="#ef4444" fillOpacity={1} fill="url(#colorRisk)" name="High Risk" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-navy-900/90 border border-slate-800 rounded-xl p-5">
          <div className="mb-4">
            <h3 className="text-sm font-bold text-white">Risk Triage Distribution</h3>
            <p className="text-xs text-slate-400">Breakdown by risk category tiers</p>
          </div>
          <div className="h-44">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={riskDist} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <XAxis dataKey="category" stroke="#475569" tick={{ fontSize: 9 }} />
                <YAxis stroke="#475569" tick={{ fontSize: 10 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '11px' }}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {riskDist.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-2 mt-4 pt-3 border-t border-slate-800 text-xs">
            {riskDist.map((d, i) => (
              <div key={i} className="flex items-center justify-between">
                <span className="flex items-center gap-1.5 text-slate-300">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS[i] }}></span>
                  {d.category}
                </span>
                <span className="font-mono font-bold text-white">{d.count} ({d.percentage}%)</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-navy-900/90 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-white">Recent Transactions</h3>
              <p className="text-xs text-slate-400">Live transaction stream with hybrid scoring</p>
            </div>
            <Link to="/transactions" className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1">
              <span>View All</span>
              <ExternalLink className="w-3 h-3" />
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-[10px] uppercase font-bold text-slate-400 bg-navy-950/60 border-b border-slate-800">
                <tr>
                  <th className="py-2.5 px-3">Tx Hash</th>
                  <th className="py-2.5 px-3">Type</th>
                  <th className="py-2.5 px-3">Amount</th>
                  <th className="py-2.5 px-3">Sender / Recipient</th>
                  <th className="py-2.5 px-3">Risk Tier</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {recentTransactions.map((tx) => (
                  <tr key={tx.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-3 px-3 font-mono text-cyan-300 font-medium">{tx.tx_hash}</td>
                    <td className="py-3 px-3">
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px] font-semibold">
                        {tx.type}
                      </span>
                    </td>
                    <td className="py-3 px-3 font-mono font-bold text-white">
                      ${Number(tx.amount).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                    <td className="py-3 px-3 text-slate-400 font-mono text-[11px]">
                      {tx.nameOrig} → {tx.nameDest}
                    </td>
                    <td className="py-3 px-3">
                      <RiskBadge category={tx.risk_category} score={tx.risk_score} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-navy-900/90 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-white">Priority Alerts</h3>
              <p className="text-xs text-slate-400">Transactions requiring review</p>
            </div>
            <Link to="/alerts" className="text-xs text-cyan-400 hover:text-cyan-300">
              Manage
            </Link>
          </div>
          <div className="space-y-3">
            {recentAlerts.map((alt) => (
              <div key={alt.id} className="p-3 bg-navy-950/70 border border-slate-800 rounded-lg hover:border-slate-700 transition-colors">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="font-mono text-xs font-bold text-cyan-400">{alt.alert_code}</span>
                  <RiskBadge category={alt.severity} score={alt.risk_score} />
                </div>
                <div className="flex items-center justify-between text-xs text-slate-300">
                  <span className="font-mono">${Number(alt.amount || 0).toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
                  <span className={`text-[10px] uppercase font-bold px-1.5 py-0.5 rounded ${
                    alt.status === 'OPEN' ? 'bg-rose-500/20 text-rose-300' : 'bg-cyan-500/20 text-cyan-300'
                  }`}>
                    {alt.status}
                  </span>
                </div>
                <p className="text-[10px] text-slate-500 mt-1 truncate">Sender: {alt.sender}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
