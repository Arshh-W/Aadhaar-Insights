import { useEffect, useState } from "react";
import axios from "axios";
import "./Anomalies.css";

function Anomalies() {
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnomalies = async () => {
      try {
        const res = await axios.get("http://localhost:5000/api/anomalies");
        setAnomalies(Array.isArray(res.data) ? res.data : []);
      } catch (err) {
        console.error("Error fetching anomalies:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnomalies();
  }, []);

  const high = anomalies.filter(a => a.score > 80).length;
  const medium = anomalies.filter(a => a.score <= 80 && a.score > 50).length;
  const low = anomalies.filter(a => a.score <= 50).length;

  if (loading) return <p>Loading anomalies...</p>;

  return (
    <div className="page-container">
    <div className="anomaly-container">
      <h1>Anomaly Detection Engine</h1>

      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="card high">
          <h2>{high}</h2>
          <p>High Risk</p>
        </div>
        <div className="card medium">
          <h2>{medium}</h2>
          <p>Medium Risk</p>
        </div>
        <div className="card low">
          <h2>{low}</h2>
          <p>Low Risk</p>
        </div>
      </div>

      {/* Table */}
      <table className="anomaly-table">
        <thead>
          <tr>
            <th>State</th>
            <th>District</th>
            <th>Risk Score</th>
            <th>Severity</th>
          </tr>
        </thead>
        <tbody>
          {anomalies.map((item, idx) => {
            const severity =
              item.score > 80 ? "High" :
              item.score > 50 ? "Medium" : "Low";

            return (
              <tr key={idx}>
                <td>{item.state}</td>
                <td>{item.district}</td>
                <td>{item.score.toFixed(2)}</td>
                <td>
                  <span className={`badge ${severity.toLowerCase()}`}>
                    {severity}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
    </div>
  );
}

export default Anomalies;
