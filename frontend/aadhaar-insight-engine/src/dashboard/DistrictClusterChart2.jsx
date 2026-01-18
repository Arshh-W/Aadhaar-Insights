import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from "recharts";

export default function DistrictClusterChart({ data }) {
  // 1. Data Validation
  if (!data || !Array.isArray(data) || data.length === 0) {
    return (
      <div style={{ padding: "40px", textAlign: "center", color: "#94a3b8", background: "#f8fafc", borderRadius: "12px" }}>
        <p>Waiting for cluster analysis data...</p>
      </div>
    );
  }

  //  Take the top 15 districts to keep the chart readable
  const chartData = data.slice(0, 15).sort((a, b) => b.labor_intensity - a.labor_intensity);

  return (
    <div style={{ width: "100%", height: "450px", background: "#fff", padding: "20px", borderRadius: "12px" }}>
      <div style={{ marginBottom: "15px" }}>
        <h3 style={{ margin: 0, fontSize: "1.1rem", fontWeight: "600", color: "#1e293b" }}>
          Labor Intensity by District
        </h3>
        <p style={{ margin: 0, fontSize: "0.8rem", color: "#64748b" }}>
          Top districts ranked by simulated labor demand
        </p>
      </div>
      
      <ResponsiveContainer width="100%" height="90%">
        <BarChart 
          data={chartData} 
          layout="vertical" 
          margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
          
          {/* XAxis shows the intensity score (0 to 1) */}
          <XAxis 
            type="number" 
            domain={[0, 1]} 
            tick={{ fontSize: 11, fill: '#94a3b8' }}
            axisLine={{ stroke: '#e2e8f0' }}
          />
          
          {/* YAxis shows the District Names */}
          <YAxis 
            dataKey="district" 
            type="category" 
            tick={{ fontSize: 11, fill: '#2c3037', fontWeight: 500 }}
            width={100}
            axisLine={false}
            tickLine={false}
          />
          
          <Tooltip 
            cursor={{ fill: '#f8fafc' }}
            contentStyle={{ 
              borderRadius: '8px', 
              border: 'none', 
              boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)',
              fontSize: '12px'
            }}
            formatter={(value, name, props) => [
              value.toFixed(2), 
              `Intensity (${props.payload.cluster_name})`
            ]}
          />
          
          <Bar 
            dataKey="labor_intensity" 
            radius={[0, 4, 4, 0]} 
            barSize={18}
          >
            {chartData.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                // Color bars based on intensity: High (Dark Blue), Low (Light Blue)
                fill={entry.labor_intensity > 0.7 ? '#1d4ed8' : '#60a5fa'} 
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}