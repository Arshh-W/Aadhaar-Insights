import React, { useState, useMemo } from "react";
import axios from "axios";
import { 
  Upload, Play, AlertCircle, Loader2, FileCheck, 
  MapPin, Activity, BarChart3, FileText, Table as TableIcon, Search
} from "lucide-react";
import RiskMap from "../dashboard/RiskMap";
import DemandForecastChart2 from "../dashboard/DemandForecastChart2";
import DistrictClusterChart2 from "../dashboard/DistrictClusterChart2";
import "./ResourceSimulator.css";

export default function ResourceSimulator() {
  const [file, setFile] = useState(null);
  const [mapping, setMapping] = useState(JSON.stringify({
    "labor": "labor_score",
    "mobility": "mobility_val",
    "infiltration": "inf_index",
    "weekend": "record_date"
  }, null, 2));
  
  const [simResult, setSimResult] = useState(null); 
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeOption, setActiveOption] = useState("table");
  const [searchTerm, setSearchTerm] = useState("");

  const sanitizeData = (data) => {
    const stringified = JSON.stringify(data, (key, value) => {
      if (typeof value === 'number' && isNaN(value)) return 0;
      return value;
    });
    return JSON.parse(stringified);
  };

  const validateAndSetFile = (selectedFile) => {
    if (!selectedFile || !selectedFile.name.toLowerCase().endsWith(".csv")) {
      return alert("Please upload a valid .csv file.");
    }
    setFile(selectedFile);
    setError("");
    setSimResult(null);
  };

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("mapping", mapping);

    try {
      const res = await axios.post("http://localhost:5000/api/simulate", formData);
      const cleanData = sanitizeData(res.data);
      setSimResult(cleanData);
      setActiveOption("table");
    } catch (err) {
      setError(err.response?.data?.error || "Server connection failed.");
    } finally {
      setLoading(false);
    }
  };

  const filteredRows = useMemo(() => {
    const rows = simResult?.predictions || [];
    if (!searchTerm) return rows;
    return rows.filter(r => 
      r.district?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.state?.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [simResult, searchTerm]);

  return (
    <div className="page-container">
      <div className="sim-container">
        <header className="sim-header">
          <h1>Resource <span className="blue-gradient">Simulator</span></h1>
          <p>Multi-dimensional AI Analysis for District Operations</p>
        </header>

        <div className="upload-section-card">
          <div className="mapping-config">
            <label>Data Mapping Configuration:</label>
            <textarea 
              value={mapping} 
              onChange={(e) => setMapping(e.target.value)}
              className="mapping-area"
            />
          </div>

          <div className="drop-zone-wrapper">
            <input 
              type="file" 
              id="csvFile" 
              accept=".csv" 
              hidden 
              onChange={(e) => validateAndSetFile(e.target.files[0])} 
            />
            <label htmlFor="csvFile" className={`drop-zone ${file ? 'has-file' : ''}`}>
              {file ? <FileCheck className="icon-success" /> : <Upload />}
              <span>{file ? file.name : "Drop CSV or Click to Browse"}</span>
            </label>
            <button onClick={handleSubmit} disabled={loading || !file} className="run-btn">
              {loading ? <Loader2 className="spinner" /> : <Play />}
              {loading ? "Analyzing..." : "Run AI Simulation"}
            </button>
          </div>
        </div>

        {error && <div className="error-banner"><AlertCircle /><span>{error}</span></div>}

        {simResult && !loading && (
          <div className="simulator-workspace">
            <aside className="sim-sidebar">
              <button className={activeOption === "table" ? "active" : ""} onClick={() => setActiveOption("table")}><TableIcon size={18}/> Predictions</button>
              <button className={activeOption === "anomaly" ? "active" : ""} onClick={() => setActiveOption("anomaly")}><MapPin size={18}/> Risk Map</button>
              <button className={activeOption === "forecast" ? "active" : ""} onClick={() => setActiveOption("forecast")}><Activity size={18}/> Demand Forecast</button>
              <button className={activeOption === "importance" ? "active" : ""} onClick={() => setActiveOption("importance")}><BarChart3 size={18}/> Feature Insights</button>
              <button className={activeOption === "report" ? "active" : ""} onClick={() => setActiveOption("report")}><FileText size={18}/> AI Report</button>
            </aside>

            <main className="sim-display-area">
              {/* TABLE VIEW */}
              {activeOption === "table" && (
                <div className="table-view">
                  <div className="table-header-actions">
                    <div className="search-bar">
                      <Search size={16} />
                      <input 
                        type="text" 
                        placeholder="Search district..." 
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                      />
                    </div>
                    <span className="results-count">Results: {filteredRows.length}</span>
                  </div>
                  <div className="table-scroll">
                    <table className="custom-table">
                      <thead>
                        <tr>
                          <th>District</th>
                          <th>State</th>
                          <th>Success Prob</th>
                          <th>Status</th>
                          <th>Risk</th>
                        </tr>
                      </thead>
                      <tbody>
                        {filteredRows.map((row, i) => (
                          <tr key={i}>
                            <td><strong>{row.district}</strong></td>
                            <td>{row.state}</td>
                            <td className={row.success_probability > 65 ? "prob-high" : "prob-low"}>
                                {row.success_probability}%
                            </td>
                            <td>
                              <span className={`status-pill ${(row.performance_label || "N/A").replace(" ", "-").toLowerCase()}`}>
                                {row.performance_label}
                              </span>
                            </td>
                            <td>{row.anomaly_status}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* RISK MAP: Updated to use anomalies_map */}
              {activeOption === "anomaly" && (
                <div className="chart-container">
                  <RiskMap data={simResult.anomalies_map || []} />
                </div>
              )}

              {/* FORECAST: Updated to use predictions list */}
              {activeOption === "forecast" && (
                <div className="chart-container">
                  <DemandForecastChart2 data={simResult.predictions || []} />
                </div>
              )}

              {/* FEATURE IMPORTANCE: Updated to use clusters_map */}
              {activeOption === "importance" && (
                <div className="chart-container">
                  <DistrictClusterChart2 data={simResult.clusters_map || []} />
                </div>
              )}

              {/* REPORT: Wrapped in activeOption check */}
              {activeOption === "report" && (
                <div className="report-container" style={{ padding: '20px', background: 'white', borderRadius: '8px' }}>
                  <h3 className="text-xl font-bold mb-4" style={{ color: '#1e293b' }}>Detailed Analysis</h3>
                  {simResult.report ? (
                    <div className="report-text">
                      {typeof simResult.report === 'string' ? (
                        simResult.report.split('\n').filter(Boolean).map((para, index) => (
                          <p key={index} style={{ marginBottom: '15px', color: '#333', lineHeight: '1.6' }}>
                            {para}
                          </p>
                        ))
                      ) : (
                        <pre>{JSON.stringify(simResult.report, null, 2)}</pre>
                      )}
                    </div>
                  ) : (
                    <div className="p-10 text-center text-gray-400">
                      <p>No report found in simulation results.</p>
                      <p className="text-xs">Keys received: {Object.keys(simResult).join(', ')}</p>
                    </div>
                  )}
                </div>
              )}
            </main>
          </div>
        )}
      </div>
    </div>
  );
}