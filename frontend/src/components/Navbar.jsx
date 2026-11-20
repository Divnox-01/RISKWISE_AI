import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Activity, Bell, Shield, Sparkles, CheckCircle2, RefreshCw } from 'lucide-react';
import { systemAPI } from '../services/api';

export const Navbar = () => {
  const [health, setHealth] = useState({ status: "CHECKING", cloud_storage: "LOCAL" });
  const location = useLocation();

  const fetchHealth = async () => {
    try {
      const res = await systemAPI.health();
      setHealth(res.data);
    } catch {
      setHealth({ status: "DEGRADED", cloud_storage: "OFFLINE" });
    }
  };

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const pageTitles = {
    '/': 'Executive Overview',
    '/analyze': 'Real-Time Transaction Analysis',
    '/transactions': 'Historical Transaction Ledger',
    '/alerts': 'Fraud Alert Management',
    '/investigations': 'Financial Crime Investigation Center',
    '/analytics': 'Quantitative Risk Analytics',
    '/model-insights': 'Model Performance & SHAP Explainability',
    '/model-management': 'ML Governance & Version Control',
    '/user-management': 'Access Control & User Directory',
    '/settings': 'Platform & Heuristic Settings',
    '/cloud': 'Microsoft Azure Operations & Architecture'
  };

  const currentTitle = pageTitles[location.pathname] || 'Risk Intelligence Platform';

  return (
    <header className="h-16 bg-navy-900/80 backdrop-blur border-b border-slate-800 px-8 flex items-center justify-between sticky top-0 z-30">
      <div>
        <h1 className="text-base font-bold text-white tracking-tight">{currentTitle}</h1>
        <p className="text-[11px] text-slate-400">PaySim Hybrid Engine • XGBoost + Isolation Forest + SHAP</p>
      </div>

      <div className="flex items-center gap-4">
        {/* System Health Badge */}
        <div className="hidden sm:flex items-center gap-2 px-3 py-1 bg-navy-950/80 rounded-full border border-slate-800 text-[11px]">
          <span className={`w-2 h-2 rounded-full ${health.status === 'HEALTHY' ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}></span>
          <span className="text-slate-300 font-medium">Core API:</span>
          <span className="font-mono text-emerald-400 font-semibold">{health.status}</span>
        </div>

        {/* Azure Cloud Status */}
        <div className="hidden md:flex items-center gap-1.5 px-3 py-1 bg-blue-950/40 rounded-full border border-blue-900/40 text-[11px] text-blue-300">
          <span className="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
          <span>Azure:</span>
          <span className="font-mono text-cyan-300 font-semibold">{health.cloud_storage === 'LOCAL_STORAGE_FALLBACK' ? 'Simulated' : 'Connected'}</span>
        </div>

        {/* Quick Action */}
        <Link
          to="/analyze"
          className="flex items-center gap-2 px-3.5 py-1.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white rounded-lg text-xs font-semibold shadow-md shadow-cyan-500/20 transition-all"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>New Inference</span>
        </Link>
      </div>
    </header>
  );
};
