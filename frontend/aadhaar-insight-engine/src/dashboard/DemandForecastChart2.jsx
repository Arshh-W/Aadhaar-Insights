import React from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer
} from "recharts";

const DemandForecastChart = ({ data }) => {
  // Check if data exists
  if (!data || data.length === 0) return <div className="p-4">No forecast data...</div>;

  return (
    <div style={{ width: "100%", height: 400, background: "#fff", padding: "10px", borderRadius: "8px" }}>
      <h3 style={{ marginBottom: "10px", fontSize: "1.1rem", fontWeight: "600", color: "#1e293b" }}>
        Simulated Demand Forecast
      </h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
          {/* Using 'district' or 'index' as X-Axis*/}
          <XAxis 
            dataKey="district" 
            tick={{ fontSize: 10 }} 
            interval="preserveStartEnd"
          />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip 
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} 
          />
          <Legend iconType="circle" />
          
          {/* Primary Prediction Line */}
          <Line 
            name="Forecasted Footfall"
            type="monotone" 
            dataKey="forecasted_footfall" 
            stroke="#2563eb" 
            strokeWidth={3} 
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />

          {/* Success Probability Line*/}
          <Line 
            name="Success Prob (%)"
            type="monotone" 
            dataKey="success_probability" 
            stroke="#10b981" 
            strokeWidth={2} 
            strokeDasharray="5 5"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DemandForecastChart;