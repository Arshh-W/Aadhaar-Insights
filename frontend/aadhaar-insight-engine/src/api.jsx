import axios from "axios";

// Flask backend base URL
const BASE_URL = "http://localhost:5000/api";



/** Resource Planner – Forecast chart */
export const fetchForecast = async () => {
  const res = await axios.get(`${BASE_URL}/forecast`);
  return res.data;
};

/** Digital Adoption / Pulse clusters */
export const fetchClusters = async () => {
  const res = await axios.get(`${BASE_URL}/clusters`);
  return res.data;
};

/** Sentinel / Threat anomalies */
export const fetchAnomalies = async () => {
  const res = await axios.get(`${BASE_URL}/anomalies`);
  return res.data;
};

/** Societal Insights – Feature importance */
export const fetchInsights = async () => {
  const res = await axios.get(`${BASE_URL}/insights`);
  return res.data;
};



/**
 * Upload CSV + mapping → get predictions
 * @param {File} file - CSV file
 * @param {Object} mapping - column mapping JSON
 */
export const simulatePerformance = async (file, mapping) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("mapping", JSON.stringify(mapping));

  const res = await axios.post(`${BASE_URL}/simulate`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return res.data;
};


/** Fetch AI-generated report */
export const fetchAIReport = async () => {
  const res = await axios.get(`${BASE_URL}/generate_report`);
  return res.data;
};
