// src/components/DashboardTabs.jsx
import React from "react";
import "../styles/dashboard.css"; 

export default function DashboardTabs({ tabs, onTabChange, activeKey }) {
  return (
    <div className="dashboard-tabs">
      {tabs.map((tab) => (
        <div
          key={tab.key}
          className={`dashboard-tab ${tab.key === activeKey ? "active" : ""}`}
          onClick={() => onTabChange(tab.key)}
        >
          {tab.label}
        </div>
      ))}
    </div>
  );
}
