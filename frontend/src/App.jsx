import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Sidebar } from './components/Sidebar';
import { Navbar } from './components/Navbar';

import { Dashboard } from './pages/Dashboard';
import { TransactionAnalysis } from './pages/TransactionAnalysis';
import { TransactionHistory } from './pages/TransactionHistory';
import { FraudAlerts } from './pages/FraudAlerts';
import { InvestigationCenter } from './pages/InvestigationCenter';
import { RiskAnalytics } from './pages/RiskAnalytics';
import { ModelInsights } from './pages/ModelInsights';
import { ModelManagement } from './pages/ModelManagement';
import { UserManagement } from './pages/UserManagement';
import { CloudOperations } from './pages/CloudOperations';
import { Settings } from './pages/Settings';
import { Login } from './pages/Login';
import { Register } from './pages/Register';

const Layout = ({ children }) => {
  return (
    <div className="flex h-screen bg-navy-950 text-slate-100 overflow-hidden font-['Plus_Jakarta_Sans',sans-serif]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Layout><Dashboard /></Layout>} />
          <Route path="/analyze" element={<Layout><TransactionAnalysis /></Layout>} />
          <Route path="/transactions" element={<Layout><TransactionHistory /></Layout>} />
          <Route path="/alerts" element={<Layout><FraudAlerts /></Layout>} />
          <Route path="/investigations" element={<Layout><InvestigationCenter /></Layout>} />
          <Route path="/analytics" element={<Layout><RiskAnalytics /></Layout>} />
          <Route path="/model-insights" element={<Layout><ModelInsights /></Layout>} />
          <Route path="/model-management" element={<Layout><ModelManagement /></Layout>} />
          <Route path="/user-management" element={<Layout><UserManagement /></Layout>} />
          <Route path="/cloud" element={<Layout><CloudOperations /></Layout>} />
          <Route path="/settings" element={<Layout><Settings /></Layout>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
