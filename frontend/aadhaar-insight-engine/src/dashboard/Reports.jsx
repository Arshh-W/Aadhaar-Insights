import { useEffect, useState } from "react";
import { FileText, Loader2, RefreshCcw } from "lucide-react";
import { fetchAIReport } from "../api";
import "./reports.css";

export default function Reports() {
  const [loading, setLoading] = useState(true);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  const loadReport = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchAIReport();
      setReport(data);
    } catch (err) {
      console.error("Report fetch error:", err);
      setError("Unable to generate report at the moment.");
    }
    setLoading(false);
  };

  useEffect(() => {
    loadReport();
  }, []);

  return (
    <div className="reports-container">
      <div className="reports-header">
        <div>
          <h2>AI Intelligence Report</h2>
          <p>Generated insights from nationwide Aadhaar activity data</p>
        </div>

        <button className="refresh-btn" onClick={loadReport}>
          <RefreshCcw size={16} />
          Refresh
        </button>
      </div>

      {loading && (
        <div className="report-loading">
          <Loader2 className="spin" size={28} />
          <p>Generating AI report…</p>
        </div>
      )}

      {error && <div className="report-error">{error}</div>}

      {!loading && report && (
        <>
          {/* Summary Card */}
          <div className="report-summary-card">
            <FileText size={20} />
            <div>
              <h4>Executive Summary</h4>
              <p>{report.summary}</p>
            </div>
          </div>

          {/* Full Report */}
          <div className="report-content">
            <h3>Detailed Analysis</h3>
            {report.report
              .split("\n")
              .filter(Boolean)
              .map((para, index) => (
                <p key={index}>{para}</p>
              ))}
          </div>
        </>
      )}
    </div>
  );
}
