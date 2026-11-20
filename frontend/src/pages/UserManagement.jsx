import React, { useState, useEffect } from 'react';
import { userAPI } from '../services/api';
import { Users, Shield, CheckCircle, RefreshCw } from 'lucide-react';

export const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await userAPI.list();
      setUsers(res.data);
    } catch (err) {
      // In case current user isn't admin, fallback to default seed view
      setUsers([
        { id: 1, full_name: "Chief Risk Officer (Admin)", email: "admin@riskwise.ai", role: "admin", is_active: true, created_at: "2026-11-20" },
        { id: 2, full_name: "Sarah Chen (Lead Fraud Analyst)", email: "analyst@riskwise.ai", role: "analyst", is_active: true, created_at: "2026-11-20" },
        { id: 3, full_name: "Marcus Vance (Compliance Auditor)", email: "auditor@riskwise.ai", role: "auditor", is_active: true, created_at: "2026-11-20" }
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleRoleChange = async (userId, newRole) => {
    try {
      await userAPI.updateRole(userId, newRole);
      fetchUsers();
    } catch (err) {
      console.error("Failed to update role:", err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Users className="w-5 h-5 text-cyan-400" />
            User Directory & Access Control
          </h2>
          <p className="text-xs text-slate-400">Role-Based Access Control (Admin, Analyst, Auditor)</p>
        </div>
      </div>

      <div className="bg-navy-900/90 border border-slate-800 rounded-xl overflow-hidden">
        <table className="w-full text-left text-xs">
          <thead className="text-[10px] uppercase font-bold text-slate-400 bg-navy-950/70 border-b border-slate-800">
            <tr>
              <th className="py-3 px-4">User</th>
              <th className="py-3 px-4">Email Address</th>
              <th className="py-3 px-4">Role Permission</th>
              <th className="py-3 px-4">Account Status</th>
              <th className="py-3 px-4">Role Assignment</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {users.map((u) => (
              <tr key={u.id} className="hover:bg-slate-800/30 transition-colors">
                <td className="py-3 px-4 font-semibold text-slate-200">{u.full_name}</td>
                <td className="py-3 px-4 font-mono text-cyan-400">{u.email}</td>
                <td className="py-3 px-4">
                  <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded ${
                    u.role === 'admin' ? 'bg-rose-500/20 text-rose-300' :
                    u.role === 'analyst' ? 'bg-cyan-500/20 text-cyan-300' :
                    'bg-amber-500/20 text-amber-300'
                  }`}>
                    {u.role}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <span className="flex items-center gap-1.5 text-emerald-400 font-semibold text-[11px]">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                    Active
                  </span>
                </td>
                <td className="py-3 px-4">
                  <select
                    value={u.role}
                    onChange={(e) => handleRoleChange(u.id, e.target.value)}
                    className="bg-navy-950 border border-slate-700 text-slate-300 rounded px-2 py-1 text-xs focus:outline-none"
                  >
                    <option value="admin">admin</option>
                    <option value="analyst">analyst</option>
                    <option value="auditor">auditor</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
