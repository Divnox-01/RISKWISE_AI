import React from 'react';

export const RiskBadge = ({ category, score }) => {
  let bg = "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
  let dot = "bg-emerald-400";

  if (category === "High Risk" || category === "CRITICAL" || category === "HIGH" || score >= 65) {
    bg = "bg-rose-500/10 text-rose-400 border-rose-500/20";
    dot = "bg-rose-400 animate-pulse";
  } else if (category === "Medium Risk" || category === "MEDIUM" || (score >= 35 && score < 65)) {
    bg = "bg-amber-500/10 text-amber-400 border-amber-500/20";
    dot = "bg-amber-400";
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border ${bg}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dot}`}></span>
      {category || "Low Risk"}
      {score !== undefined && score !== null && (
        <span className="opacity-75 font-mono ml-0.5">({Number(score).toFixed(1)})</span>
      )}
    </span>
  );
};
