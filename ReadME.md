#  Adhaar Insights: AI-Powered Governance Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

**Adhaar Insights** is a proactive governance intelligence platform designed to optimize Aadhaar Seva Kendra operations. It shifts administrative decision-making from **reactive firefighting** to **predictive optimization** using advanced Machine Learning and Real-Time Analytics.

##  Table of Contents
- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Key Features](#-key-features)
- [Technical Architecture](#-technical-architecture)
- [Installation & Setup](#-installation--setup)
- [API Reference](#-api-reference)
- [Screenshots](#-screenshots)
- [Team](#-team)

---

##  Problem Statement
The current Aadhaar ecosystem faces three critical operational challenges:
1.  **Unpredictable Footfall:** Centers oscillate between overcrowding and idle capacity, leading to resource wastage and high wait times.
2.  **Reactive Fraud Detection:** Anomalies (like illegal infiltration or fake enrollments) are often detected days or weeks later during manual audits.
3.  **"One-Size-Fits-All" Governance:** Diverse districts are managed with identical protocols, ignoring local factors like labor intensity and mobility.

##  Our Solution
**Adhaar Insights** integrates 4 specialized ML models into a unified dashboard that empowers decision-makers to:
* **Predict Demand:** Forecast footfall 60 days in advance.
* **Detect Anomalies:** Flag suspicious districts in real-time (Sentinel Model).
* **Simulate Policy:** Test "What-If" scenarios (e.g., changing labor allocation) before implementation.
* **Cluster Operations:** Segment districts into "Labor Zones", "Urban Hubs", or "Mixed Zones" for targeted governance.

---

##  Technical Architecture

### **The Intelligence Pipeline**
Our system follows a robust **ETL (Extract, Transform, Load)** architecture:

1.  **Data Ingestion:** Merges Enrolment, Biometric, and Demographic logs.
2.  **Preprocessing:** Feature engineering (Cyclical Time, Efficiency Metrics, Infiltration Index).
3.  **Model Inference:**
    * **Model 01 (Sentinel):** Isolation Forest for Anomaly Detection.
    * **Model 02 (Pulse):** K-Means for Operational Clustering.
    * **Model 03 (Forecast):** Ensemble (XGBoost + Random Forest) for Demand Prediction.
    * **Model 04 (Simulator):** Random Forest Classifier for Policy Simulation.
4.  **Reporting:** LLM-based automated executive summaries.

---

##  Key Features

### 1. **Dynamic "What-If" Simulator**
Administrators can upload hypothetical datasets or adjust sliders (Labor Intensity, Mobility) to see instant predictions on District Success Probability.

### 2. **Geospatial Intelligence**
* **Pulse Map:** Visualizes operational clusters (e.g., Red for Manual Labor Zones, Blue for Tech Hubs).
* **Sentinel Map:** A dedicated "Risk Layer" that plots only high-risk anomaly zones (Risk Score > 60).

### 3. **AI-Generated Reports**
Translates complex CSV data into human-readable strategic reports instantly, highlighting key risks and recommendations.

---

##  Installation & Setup

### Prerequisites
* Python 3.8+
* Node.js & npm

### Step 1: Backend Setup
Navigate to the `backend` folder.

```bash

cd backend
pip install -r requirements.txt

Start the Server:Bashpython app.py
Server runs at http://localhost:5000Step 2: Frontend SetupOpen a new terminal and navigate to the frontend folder.Bashcd frontend
npm install
npm start

Dashboard runs at http://localhost:3000 
API:
 GET/api/healthSystem heartbeat & model status check.
 GET/api/forecastReturns 60-day actual vs. predicted footfall trends.
 GET/api/clustersReturns geospatial data for operational clustering.
 GET/api/anomaliesReturns high-risk districts flagged by Sentinel model.
 POST/api/simulateMaster Endpoint: Runs full pipeline on uploaded CSV (Anomaly -> Forecast -> Report).