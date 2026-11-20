import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  ShieldAlert,
  SearchCode,
  History,
  FileSearch,
  LineChart,
  BrainCircuit,
  SlidersHorizontal,
  Users,
  Settings,
  Cloud,
  LogOut,
  ShieldCheck
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Sidebar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navSections = [
    {
      title: "Monitoring",
      items: [
        { name: "Overview", to: "/", icon: LayoutDashboard },
        { name: "Live Inference", to: "/analyze", icon: SearchCode, highlight: true },
        { name: "Transactions", to: "/transactions", icon: History },
        { name: "Fraud Alerts", to: "/alerts", icon: ShieldAlert },
        { name: "Investigations", to: "/investigations", icon: FileSearch },
      ]
    },
    {
      title: "Intelligence & ML",
      items: [
        { name: "Risk Analytics", to: "/analytics", icon: LineChart },
        { name: "Model Insights", to: "/model-insights", icon: BrainCircuit },
        { name: "Model Registry", to: "/model-management", icon: SlidersHorizontal },
      ]
    },
    {
      title: "Platform & Cloud",
      items: [
        { name: "Azure Operations", to: "/cloud", icon: Cloud },
        { name: "User Directory", to: "/user-management", icon: Users },
        { name: "Settings", to: "/settings", icon: Settings },
      ]
    }
  ];

  return (
    <aside className="w-64 bg-navy-900 border-r border-slate-800 flex flex-col h-screen select-none sticky top-0 shrink-0">
      {/* Brand Header */}
      <div className="h-16 flex items-center gap-3 px-6 border-b border-slate-800/80 bg-navy-950/40">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-500 flex items-center justify-center shadow-lg shadow-cyan-500/20 text-white font-black text-lg">
          <ShieldCheck className="w-5 h-5 text-white" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-sm tracking-wider text-white">RISKWISE</span>
            <span className="text-[10px] bg-cyan-500/20 text-cyan-300 font-bold px-1.5 py-0.5 rounded border border-cyan-500/30">AI 2.0</span>
          </div>
          <p className="text-[10px] text-slate-400 font-medium tracking-tight">Fintech Fraud Intelligence</p>
        </div>
      </div>

      {/* Nav List */}
      <div className="flex-1 overflow-y-auto px-4 py-5 space-y-6">
        {navSections.map((sec, idx) => (
          <div key={idx}>
            <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500 px-3 mb-2">
              {sec.title}
            </p>
            <nav className="space-y-1">
              {sec.items.map((item) => {
                const Icon = item.icon;
                return (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    end={item.to === "/"}
                    className={({ isActive }) =>
                      `flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium transition-colors ${
                        isActive
                          ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-semibold shadow-sm"
                          : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                      } ${item.highlight && !window.location.pathname.includes(item.to) ? "border border-cyan-500/10 text-slate-300" : ""}`
                    }
                  >
                    <Icon className="w-4 h-4 shrink-0" />
                    <span>{item.name}</span>
                    {item.highlight && (
                      <span className="ml-auto w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
                    )}
                  </NavLink>
                );
              })}
            </nav>
          </div>
        ))}
      </div>

      {/* User Footer */}
      <div className="p-4 border-t border-slate-800/80 bg-navy-950/30">
        <div className="flex items-center justify-between">
          <div className="min-w-0 flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-xs font-bold text-cyan-400 uppercase">
              {user ? user.full_name?.charAt(0) : "U"}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-semibold text-slate-200 truncate">
                {user ? user.full_name : "Analyst"}
              </p>
              <p className="text-[10px] text-cyan-400/90 font-mono capitalize">
                {user ? user.role : "analyst"}
              </p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            title="Log out"
            className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
};
