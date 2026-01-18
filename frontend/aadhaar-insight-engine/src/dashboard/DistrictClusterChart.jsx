import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";


export default function DistrictClusterChart({ data }) {
  if (!data || data.length === 0) return <div>Loading societal insights...</div>;

  return (
    <div style={{ width: "100%", height: 400 }}>
      <h3 className="section-title">Societal Feature Importance</h3>
  
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="feature" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="importance" fill="#2563eb" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  
  );
}
