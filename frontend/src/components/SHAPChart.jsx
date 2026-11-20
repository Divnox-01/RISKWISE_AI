import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';

export const SHAPChart = ({ contributions = [] }) => {
  if (!contributions || contributions.length === 0) {
    return (
      <div className="text-center py-8 text-slate-500 text-xs">
        No feature attribution data available for this prediction.
      </div>
    );
  }

  // Display top 8 most influential features
  const data = contributions.slice(0, 8).map(c => ({
    name: c.label || c.feature,
    value: c.shap_value,
    featureValue: c.feature_value,
    isPositive: c.shap_value > 0
  })).reverse();

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const item = payload[0].payload;
      return (
        <div className="bg-navy-900 border border-slate-700 p-3 rounded-lg shadow-xl text-xs space-y-1">
          <p className="font-semibold text-slate-200">{item.name}</p>
          <p className="text-slate-400">Observed Value: <span className="font-mono text-cyan-300">{item.featureValue}</span></p>
          <p className={item.isPositive ? "text-rose-400" : "text-emerald-400"}>
            SHAP Attribution: <span className="font-mono font-bold">{item.value > 0 ? `+${item.value}` : item.value}</span>
          </p>
          <p className="text-[10px] text-slate-500 italic">
            {item.isPositive ? "Elevates fraud suspicion" : "Mitigates fraud suspicion"}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 10, right: 30, left: 110, bottom: 5 }}
        >
          <XAxis type="number" stroke="#64748b" tick={{ fontSize: 10 }} />
          <YAxis
            type="category"
            dataKey="name"
            stroke="#94a3b8"
            tick={{ fontSize: 11 }}
            width={105}
          />
          <Tooltip content={<CustomTooltip />} />
          <ReferenceLine x={0} stroke="#334155" />
          <Bar dataKey="value" radius={[0, 4, 4, 0]}>
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.value > 0 ? '#ef4444' : '#10b981'}
                opacity={0.85}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
