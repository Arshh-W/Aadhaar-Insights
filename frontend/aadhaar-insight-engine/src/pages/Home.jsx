import React from "react";
import {
  BarChart2,
  AlertTriangle,
  ShieldCheck,
  Radar,
  Cpu,
  LineChart,
  ArrowDown
} from "lucide-react";
import "./Home.css";

function Home() {
  return (
    <div className="home-container">
      {/* --- BACKGROUND LAYERS --- */}
      <div className="background-layers">
        <div className="blob blob1"></div>
        <div className="blob blob2"></div>
        <div className="particle-container">
          {[...Array(6)].map((_, i) => (
            <div key={i} className={`particle p${i + 1}`}></div>
          ))}
        </div>
      </div>

      {/* --- HERO SECTION --- */}
      <section className="hero">
        <div className="logo-container">
          <img src="/aadhar_insight_logo.png" alt="Aadhar Engine Logo" className="alive-logo" />
        </div>

        <h1 className="hero-title">
          Aadhaar <span className="blue-gradient">Insights</span> Platform
        </h1>

        <p className="hero-subtitle">
          AI-driven intelligence for identity security, societal insights,
          and data-backed public policy decisions.
        </p>

        <div className="hero-buttons">
          <a href="/dashboard" className="primary-btn">
            Explore Dashboard
          </a>
          <a href="/resourcesimulator" className="secondary-btn">
            Run Simulator
          </a>
        </div>

        <div className="scroll-indicator">
          <p>Discover Features</p>
          <ArrowDown size={20} className="bounce" />
        </div>
      </section>

      {/* --- FEATURES GRID --- */}
      <section className="features-section">
        <div className="section-header">
          <h2>Core Capabilities</h2>
          <div className="header-line"></div>
        </div>
        
        <div className="features-grid">
          <Feature
            icon={<AlertTriangle />}
            title="Anomaly Detection"
            desc="Detects suspicious Aadhaar update patterns using intelligent clustering."
          />
          <Feature
            icon={<Radar />}
            title="Digital Pulse Mapping"
            desc="Visualizes regional digital adoption and workforce intensity."
          />
          <Feature
            icon={<Cpu />}
            title="Resource Simulator"
            desc="Scenario-based performance simulator for district optimization."
          />
          <Feature
            icon={<BarChart2 />}
            title="Societal Insights"
            desc="Explains the drivers behind labor, mobility, and demographic shifts."
          />
          <Feature
            icon={<LineChart />}
            title="Demand Forecasting"
            desc="Predicts future Aadhaar service demand using time-series models."
          />
          <Feature
            icon={<ShieldCheck />}
            title="Privacy by Design"
            desc="Only aggregated and anonymized data is ever processed."
          />
        </div>
      </section>

      {/* --- IMPACT SECTION --- */}
      <section className="impact-section">
        <div className="impact-card">
          <h2>Why This Platform Matters</h2>
          <div className="impact-grid">
            <div className="impact-item"><span>✔</span> Prevent identity misuse early</div>
            <div className="impact-item"><span>✔</span> Improve trust in digital public infrastructure</div>
            <div className="impact-item"><span>✔</span> Enable data-driven governance</div>
            <div className="impact-item"><span>✔</span> Optimize workforce planning</div>
          </div>
        </div>
      </section>
    </div>
  );
}

function Feature({ icon, title, desc }) {
  return (
    <div className="feature-card">
      <div className="icon-box">{icon}</div>
      <h3>{title}</h3>
      <p>{desc}</p>
    </div>
  );
}

export default Home;