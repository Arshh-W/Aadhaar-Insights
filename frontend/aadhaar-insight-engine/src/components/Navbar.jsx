import React from "react";
import { Link, useLocation } from "react-router-dom";
import { Home as HomeIcon, AlertTriangle, BarChart2, Shield, Activity } from "lucide-react";
import "./Navbar.css";

function Navbar() {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="navbar">
      <div className="nav-content">
        {/* Brand Section */}
        <Link to="/" className="nav-logo-section">
          <div className="nav-logo-container">
            <img src="/aadhar_insight_logo.png" alt="logo" className="nav-mini-logo" />
          </div>
          <span className="nav-brand-text">Aadhaar <span className="brand-accent">Insight</span></span>
        </Link>

        {/* Navigation Links */}
        <div className="nav-links">
          <Link to="/" className={`nav-item ${isActive("/") ? "active" : ""}`}>
            <HomeIcon size={18} /> <span>Home</span>
          </Link>

          <Link to="/dashboard" className={`nav-item ${isActive("/dashboard") ? "active" : ""}`}>
            <BarChart2 size={18} /> <span>Dashboard</span>
          </Link>

          <Link to="/anomalies" className={`nav-item ${isActive("/anomalies") ? "active" : ""}`}>
            <AlertTriangle size={18} /> <span>Anomalies</span>
          </Link>

          <Link to="/resourcesimulator" className={`nav-item ${isActive("/resourcesimulator") ? "active" : ""}`}>
            <Activity size={18} /> <span>Simulator</span>
          </Link>

          <Link to="/privacy" className={`nav-item ${isActive("/privacy") ? "active" : ""}`}>
            <Shield size={18} /> <span>Privacy</span>
          </Link>
        </div>

        <div className="nav-action">
          <button className="nav-support-btn">System Status</button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;