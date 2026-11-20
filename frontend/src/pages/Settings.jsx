import React, { useState } from 'react';
import { Settings as SettingsIcon, Save, Bell, Shield, Sliders } from 'lucide-react';

export const Settings = () => {
  const [highRiskThreshold, setHighRiskThreshold] = useState(65);
  const [mediumRiskThreshold, setMediumRiskThreshold] = useState(35);
  const [autoBlockHighRisk, setAutoBlockHighRisk] = useState(true);
  const [saved, setSaved] = useState(false);

  const handleSave = (e) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <SettingsIcon className="w-5 h-5 text-cyan-400" />
          System Settings & Operational Policies
        </h2>
        <p className="text-xs text-slate-400">Manage risk cutoffs, notification triggers, and automated settlement rules</p>
      </div>

      <form onSubmit={handleSave} className="bg-navy-900/90 border border-slate-800 rounded-xl p-6 space-y-6 max-w-2xl">
        <div className="space-y-4">
          <h3 className="text-sm font-bold text-white border-b border-slate-800 pb-2">Fraud Decision Boundaries</h3>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">High Risk Threshold (Block)</label>
              <input
                type="number"
                min="50"
                max="95"
                value={highRiskThreshold}
                onChange={(e) => setHighRiskThreshold(parseInt(e.target.value))}
                className="w-full bg-navy-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white font-mono focus:border-cyan-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Medium Risk Threshold (Review)</label>
              <input
                type="number"
                min="20"
                max="49"
                value={mediumRiskThreshold}
                onChange={(e) => setMediumRiskThreshold(parseInt(e.target.value))}
                className="w-full bg-navy-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white font-mono focus:border-cyan-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="flex items-center gap-2 pt-2">
            <input
              type="checkbox"
              id="autoBlock"
              checked={autoBlockHighRisk}
              onChange={(e) => setAutoBlockHighRisk(e.target.checked)}
              className="rounded bg-navy-950 border-slate-800 text-cyan-500 focus:ring-0"
            />
            <label htmlFor="autoBlock" className="text-xs text-slate-300 select-none">
              Automatically decline settlements exceeding High Risk cutoff
            </label>
          </div>
        </div>

        <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
          <button
            type="submit"
            className="px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-navy-950 font-bold rounded-lg text-xs flex items-center gap-2 transition-colors"
          >
            <Save className="w-3.5 h-3.5" />
            <span>Save Settings</span>
          </button>

          {saved && (
            <span className="text-xs text-emerald-400 font-semibold">Settings saved successfully.</span>
          )}
        </div>
      </form>
    </div>
  );
};
