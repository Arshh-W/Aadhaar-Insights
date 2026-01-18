import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import DashboardTabs from "../components/DashboardTabs";


import RiskMap from "../dashboard/RiskMap";
import DigitalAdoptionMap from "../dashboard/DigitalAdoptionMap";
import DistrictClusterChart from "../dashboard/DistrictClusterChart";
import DemandForecastChart from "../dashboard/DemandForecastChart";
import Reports from "../dashboard/Reports";


import "../styles/dashboard.css";
import {
  fetchAnomalies,
  fetchClusters,
  fetchInsights,
  fetchForecast,
} from "../api";

export default function Dashboard() {
  const [activeView, setActiveView] = useState("dashboard");
  const [loading, setLoading] = useState(true);

  // Backend data
  const [riskData, setRiskData] = useState([]);
  const [digitalData, setDigitalData] = useState([]);
  const [societalData, setSocietalData] = useState([]);
  const [forecastData, setForecastData] = useState([]);

useEffect(() => {
  const loadData = async () => {
    setLoading(true);
    try {
      const [
        riskData,
        digitalData,
        societalData,
        forecastData
      ] = await Promise.all([
        fetchAnomalies(),
        fetchClusters(),
        fetchInsights(),
        fetchForecast()
      ]);

      // console.log("Risk:", riskData.length);
      // console.log("Clusters:", digitalData.length);
      // console.log("Insights:", societalData.length);
      // console.log("Forecast:", forecastData.length);

      setRiskData(riskData);
      setDigitalData(digitalData);
      setSocietalData(societalData);
      setForecastData(forecastData);

    } catch (err) {
      console.error("Error fetching dashboard data:", err);
      setRiskData([]);
      setDigitalData([]);
      setSocietalData([]);
      setForecastData([]);
    }
    setLoading(false);
  };

  loadData();
}, []);

  const tabs = [
    { key: "dashboard", label: "Overview" },
    { key: "threats", label: "Threat Intel" },
    { key: "societal", label: "Societal Trends" },
    { key: "resource", label: "Resource Planner" },
    { key: "reports", label: "Reports" },
  ];

 


  return (
    <div className="page-container">
      <div className="dashboard-layout">
        <Sidebar activeView={activeView} setActiveView={setActiveView} />

        <div className="dashboard-main">
          <Topbar />

          

          {/* ---------------- DASHBOARD OVERVIEW ---------------- */}
          {activeView === "dashboard" && (
            <section>
              <h3 className="section-title">Threat Intelligence</h3>
              {riskData.length ? (
                <RiskMap data={riskData} />
              ) : (
                <div>No threat data available</div>
              )}

              <h3 className="section-title">Digital Readiness</h3>
              {digitalData.length ? (
                <DigitalAdoptionMap data={digitalData} />
              ) : (
                <div>No digital adoption data available</div>
              )}
            </section>
          )}

          {/* ---------------- THREAT INTEL ---------------- */}
          {activeView === "threats" && (
            riskData.length ? (
              <RiskMap data={riskData} />
            ) : (
              <div>No threat data available</div>
            )
          )}

          {/* ---------------- SOCIETAL ---------------- */}
          {activeView === "societal" && (
            societalData.length ? (
              <DistrictClusterChart data={societalData} />
            ) : (
              <div>No societal insight data available</div>
            )
          )}

          {/* ---------------- RESOURCE ---------------- */}
          {activeView === "resource" && (
            forecastData.length ? (
              <DemandForecastChart data={forecastData} />
            ) : (
              <div>No forecast data available</div>
            )
          )}

         {/* ---------------- REPORTS VIEW ---------------- */}
          {activeView === "reports" && (
            <Reports />
          )}

        </div>
      </div>
    </div>
  );
}
