import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function DemandForecastChart({ data }) {
  // Check if data exists and has the correct keys
  if (!data || !Array.isArray(data) || data.length === 0) {
    return <div className="no-data-msg">No forecast data available</div>;
  }

 return (
    <div style={{ width: "100%", height: "450px", minHeight: "400px" }}>
      <h3 className="section-title">Footfall Forecast</h3>
      
      <ResponsiveContainer width="100%" height="100%">
        {/* REMOVED fixed width/height from LineChart */}
        <LineChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#eee" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }} 
            interval="preserveStartEnd"
          />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip />
          <Legend iconType="circle" />
          <Line
            type="monotone"
            dataKey="Actual"
            stroke="#2563eb"
            strokeWidth={3}
            dot={false}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="Predicted"
            stroke="#ef4444"
            strokeWidth={3}
            strokeDasharray="5 5"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
} 