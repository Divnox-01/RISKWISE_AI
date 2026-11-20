import React from 'react';
import { Cloud, Server, Database, Key, Activity, ShieldCheck, Terminal, ExternalLink } from 'lucide-react';

export const CloudOperations = () => {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <Cloud className="w-5 h-5 text-cyan-400" />
          Microsoft Azure Architecture & Cloud Operations
        </h2>
        <p className="text-xs text-slate-400">
          Infrastructure-as-Code, Azure App Service containerization, and Key Vault integration
        </p>
      </div>

      {/* Cloud Service Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 bg-navy-900 border border-slate-800 rounded-xl space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-white">Azure App Service</span>
            <Server className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-[11px] text-slate-400">Linux B1 Containerized Python 3.13 FastAPI Runtime</p>
          <div className="flex items-center gap-1.5 text-[10px] text-emerald-400 font-mono pt-2 border-t border-slate-800">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            <span>IaC Prepared (Bicep)</span>
          </div>
        </div>

        <div className="p-4 bg-navy-900 border border-slate-800 rounded-xl space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-white">Azure Blob Storage</span>
            <Database className="w-4 h-4 text-blue-400" />
          </div>
          <p className="text-[11px] text-slate-400">Model Artifacts Bucket & Hot Audit Archive</p>
          <div className="flex items-center gap-1.5 text-[10px] text-cyan-400 font-mono pt-2 border-t border-slate-800">
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
            <span>riskwise-model-artifacts</span>
          </div>
        </div>

        <div className="p-4 bg-navy-900 border border-slate-800 rounded-xl space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-white">Application Insights</span>
            <Activity className="w-4 h-4 text-purple-400" />
          </div>
          <p className="text-[11px] text-slate-400">Telemetry, Latency, and Distributed Tracing</p>
          <div className="flex items-center gap-1.5 text-[10px] text-emerald-400 font-mono pt-2 border-t border-slate-800">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            <span>Telemetry Configured</span>
          </div>
        </div>

        <div className="p-4 bg-navy-900 border border-slate-800 rounded-xl space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-white">Azure Key Vault</span>
            <Key className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-[11px] text-slate-400">JWT Secret & Storage Keys Encryption</p>
          <div className="flex items-center gap-1.5 text-[10px] text-amber-400 font-mono pt-2 border-t border-slate-800">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
            <span>RBAC Managed Identity</span>
          </div>
        </div>
      </div>

      {/* Azure CLI & Deployment Specs */}
      <div className="bg-navy-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
        <h3 className="text-sm font-bold text-white flex items-center gap-2">
          <Terminal className="w-4 h-4 text-cyan-400" />
          Automated Azure CLI Deployment Commands
        </h3>
        <p className="text-xs text-slate-400">
          Ready-to-run commands for provisioning production resources in resource group <code className="text-cyan-300">rg-riskwise-ai-prod</code>
        </p>

        <div className="bg-navy-950 p-4 rounded-lg border border-slate-800 font-mono text-xs text-slate-300 space-y-2 overflow-x-auto">
          <p className="text-slate-500"># 1. Login to Azure and set resource group</p>
          <p className="text-cyan-300">az login</p>
          <p className="text-cyan-300">az group create --name rg-riskwise-ai-prod --location eastus</p>
          <p className="text-slate-500 mt-2"># 2. Deploy Bicep template (App Service, Blob Storage, Key Vault, App Insights)</p>
          <p className="text-cyan-300">az deployment group create --resource-group rg-riskwise-ai-prod --template-file azure/main.bicep</p>
          <p className="text-slate-500 mt-2"># 3. Synchronize local trained model artifacts to Azure Blob Storage</p>
          <p className="text-cyan-300">az storage blob upload-batch --destination riskwise-model-artifacts --source backend/artifacts --account-name stgaccountriskwise</p>
        </div>
      </div>
    </div>
  );
};
