import React from "react";

export default function AlertsPanel({ alerts, loading }) {
  return (
    <div className="alerts-card">
      {loading ? (
        <p style={{ textAlign: "center", color: "#6b7280" }}>Loading alerts...</p>
      ) : alerts && alerts.length > 0 ? (
        alerts.map((alert, idx) => (
          <div className="alert-item" key={idx}>
            ⚠️ {alert.message}
          </div>
        ))
      ) : (
        <p style={{ textAlign: "center", color: "#6b7280" }}>No alerts yet</p>
      )}
    </div>
  );
}
