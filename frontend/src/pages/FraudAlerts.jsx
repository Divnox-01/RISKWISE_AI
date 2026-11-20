import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { alertAPI } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';
import { ShieldAlert, Filter, CheckCircle2, FileSearch, RefreshCw } from 'lucide-react';

export const FraudAlerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('');
  const [severityFilter, setSeverityFilter] = useState('');

  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const res = await alertAPI.list({
        status: statusFilter || undefined,
        severity: severityFilter || undefined
      });
      setAlerts(res.data);
    } catch (err) {
      console.error("Fetch alerts failed:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, [statusFilter, severityFilter]);

  const handleStatusChange = async (id, newStatus) => {
    try {
      await alertAPI.update(id, { status: newStatus });
      fetchAlerts();
    } catch (err) {
      console.error("Update alert failed:", err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-white">Fraud Alert Queue</h2>
          <p className="text-xs text-slate-400">Automated triage queue for elevated risk transactions (Risk Score &gt;= 35)</p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 bg-navy-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs">
            <span className="text-slate-400">Status:</span>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-transparent text-slate-200 border-none focus:outline-none text-xs"
            >
              <option value="">All</option>
              <option value="OPEN">OPEN</option>
              <option value="UNDER_INVESTIGATION">UNDER_INVESTIGATION</option>
              <option value="RESOLVED">RESOLVED</option>
              <option value="DISMISSED">DISMISSED</option>
            </select>
          </div>

          <div className="flex items-center gap-2 bg-navy-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs">
            <span className="text-slate-400">Severity:</span>
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="bg-transparent text-slate-200 border-none focus:outline-none text-xs"
            >
              <option value="">All</option>
              <option value="CRITICAL">CRITICAL</option>
              <option value="HIGH">HIGH</option>
              <option value="MEDIUM">MEDIUM</option>
            </select>
          </div>

          <button
            onClick={fetchAlerts}
            className="p-2 bg-navy-900 hover:bg-slate-800 border border-slate-800 rounded-lg text-slate-300 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {loading ? (
          <div className="p-12 text-center text-slate-500 bg-navy-900/60 rounded-xl border border-slate-800">
            <div className="w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
            <span>Loading security alerts queue...</span>
          </div>
        ) : alerts.length === 0 ? (
          <div className="p-12 text-center text-slate-500 bg-navy-900/60 rounded-xl border border-slate-800">
            No active alerts matching the selected filters.
          </div>
        ) : (
          alerts.map((alt) => (
            <div
              key={alt.id}
              className="bg-navy-900/90 border border-slate-800 hover:border-slate-700 rounded-xl p-5 transition-all flex flex-col md:flex-row items-start md:items-center justify-between gap-4"
            >
              <div className="space-y-2">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-sm font-bold text-white">{alt.alert_code}</span>
                  <RiskBadge category={alt.severity} score={alt.risk_score} />
                  <span className="font-mono text-xs px-2 py-0.5 rounded bg-slate-800 text-cyan-300">
                    Tx: {alt.tx_hash}
                  </span>
                </div>

                <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400">
                  <span>Modality: <strong className="text-slate-200">{alt.tx_type}</strong></span>
                  <span>Amount: <strong className="font-mono text-white">${Number(alt.amount || 0).toLocaleString(undefined, { minimumFractionDigits: 2 })}</strong></span>
                  <span>Sender: <span className="font-mono text-slate-300">{alt.sender}</span></span>
                  <span>Recipient: <span className="font-mono text-slate-300">{alt.recipient}</span></span>
                </div>
              </div>

              <div className="flex items-center gap-3 w-full md:w-auto justify-end border-t md:border-t-0 pt-3 md:pt-0 border-slate-800">
                <select
                  value={alt.status}
                  onChange={(e) => handleStatusChange(alt.id, e.target.value)}
                  className={`text-xs font-semibold px-2.5 py-1.5 rounded-lg border focus:outline-none ${
                    alt.status === 'OPEN' ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' :
                    alt.status === 'UNDER_INVESTIGATION' ? 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30' :
                    'bg-slate-800 text-slate-300 border-slate-700'
                  }`}
                >
                  <option value="OPEN">OPEN</option>
                  <option value="UNDER_INVESTIGATION">UNDER_INVESTIGATION</option>
                  <option value="RESOLVED">RESOLVED</option>
                  <option value="DISMISSED">DISMISSED</option>
                </select>

                <Link
                  to="/investigations"
                  className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 flex items-center gap-1.5 transition-colors"
                >
                  <FileSearch className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Investigate</span>
                </Link>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
