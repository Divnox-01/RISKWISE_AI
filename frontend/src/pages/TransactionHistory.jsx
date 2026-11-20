import React, { useState, useEffect } from 'react';
import { transactionAPI } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';
import { Filter, RefreshCw, ChevronLeft, ChevronRight, Search } from 'lucide-react';

export const TransactionHistory = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState('');
  const [offset, setOffset] = useState(0);
  const limit = 20;

  const fetchTransactions = async () => {
    setLoading(true);
    try {
      const res = await transactionAPI.list({
        limit,
        offset,
        type: filterType || undefined
      });
      setTransactions(res.data);
    } catch (err) {
      console.error("Fetch transactions failed:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, [filterType, offset]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-white">Transaction History</h2>
          <p className="text-xs text-slate-400">Chronological transaction stream with hybrid scoring attribution</p>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <div className="flex items-center gap-2 bg-navy-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={filterType}
              onChange={(e) => { setFilterType(e.target.value); setOffset(0); }}
              className="bg-transparent text-slate-200 border-none focus:outline-none text-xs"
            >
              <option value="">All Modalities</option>
              <option value="TRANSFER">TRANSFER</option>
              <option value="CASH_OUT">CASH_OUT</option>
              <option value="PAYMENT">PAYMENT</option>
              <option value="CASH_IN">CASH_IN</option>
              <option value="DEBIT">DEBIT</option>
            </select>
          </div>

          <button
            onClick={fetchTransactions}
            className="p-2 bg-navy-900 hover:bg-slate-800 border border-slate-800 rounded-lg text-slate-300 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="bg-navy-900/90 border border-slate-800 rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="text-[10px] uppercase font-bold text-slate-400 bg-navy-950/70 border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Tx Hash</th>
                <th className="py-3 px-4">Step / Time</th>
                <th className="py-3 px-4">Type</th>
                <th className="py-3 px-4">Amount</th>
                <th className="py-3 px-4">Origin Account & Balance</th>
                <th className="py-3 px-4">Destination Account</th>
                <th className="py-3 px-4">Risk Evaluation</th>
                <th className="py-3 px-4">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {loading ? (
                <tr>
                  <td colSpan={8} className="py-12 text-center text-slate-500">
                    <div className="w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
                    <span>Loading transactions ledger...</span>
                  </td>
                </tr>
              ) : transactions.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-12 text-center text-slate-500">
                    No transactions found matching criteria.
                  </td>
                </tr>
              ) : (
                transactions.map((tx) => (
                  <tr key={tx.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-3 px-4 font-mono font-medium text-cyan-300">{tx.tx_hash}</td>
                    <td className="py-3 px-4 text-slate-400 font-mono text-[11px]">
                      Step {tx.step} (H{(tx.step % 24).toString().padStart(2, '0')}:00)
                    </td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px] font-semibold">
                        {tx.type}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono font-bold text-white">
                      ${Number(tx.amount).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                    <td className="py-3 px-4 text-slate-400 font-mono text-[11px]">
                      <div>{tx.nameOrig}</div>
                      <div className="text-[10px] text-slate-500">
                        Prior: ${Number(tx.oldbalanceOrg).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                      </div>
                    </td>
                    <td className="py-3 px-4 text-slate-400 font-mono text-[11px]">
                      <div>{tx.nameDest}</div>
                      <div className="text-[10px] text-slate-500">
                        Prior: ${Number(tx.oldbalanceDest).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <RiskBadge category={tx.risk_category} score={tx.risk_score} />
                    </td>
                    <td className="py-3 px-4">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                        tx.recommended_action === 'BLOCK' ? 'bg-rose-500/20 text-rose-300' :
                        tx.recommended_action === 'REVIEW' ? 'bg-amber-500/20 text-amber-300' :
                        'bg-emerald-500/20 text-emerald-300'
                      }`}>
                        {tx.recommended_action || 'ALLOW'}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        <div className="p-4 border-t border-slate-800 bg-navy-950/40 flex items-center justify-between text-xs text-slate-400">
          <span>Showing offset {offset} to {offset + transactions.length}</span>
          <div className="flex items-center gap-2">
            <button
              disabled={offset === 0}
              onClick={() => setOffset(Math.max(0, offset - limit))}
              className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 disabled:opacity-40 transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              disabled={transactions.length < limit}
              onClick={() => setOffset(offset + limit)}
              className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 disabled:opacity-40 transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
