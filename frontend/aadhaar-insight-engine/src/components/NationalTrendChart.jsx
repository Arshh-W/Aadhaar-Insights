import React from "react";

export default function NationalTrendChart({ data, loading }) {
  return (
    <div
      className="chart-card"
      style={{
        minHeight: "250px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: "#6b7280",
      }}
    >
      {loading
        ? "Loading chart..."
        : data && data.length > 0
        ? "📈 Chart will render here"
        : "No chart data yet"}
    </div>
  );
}
