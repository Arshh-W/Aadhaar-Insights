import {
  LayoutDashboard,
  ShieldAlert,
  Users,
  BarChart3,
  FileText,
} from "lucide-react";
import "../styles/sidebar.css";

export default function Sidebar({ activeView, setActiveView }) {
  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <h2>Aadhaar</h2>
        <span>Command Center</span>
      </div>

      <hr className="hr" />

      {/* Navigation */}
      <nav className="sidebar-menu">
        {/* Dashboard */}
        <div
          className={`sidebar-item ${
            activeView === "dashboard" ? "active" : ""
          }`}
          onClick={() => setActiveView("dashboard")}
        >
          <LayoutDashboard size={18} />
          <span>Dashboard</span>
        </div>

        {/* Threat Intelligence */}
        <div
          className={`sidebar-item ${
            activeView === "threats" ? "active" : ""
          }`}
          onClick={() => setActiveView("threats")}
        >
          <ShieldAlert size={18} />
          <span>Threat Intel</span>
        </div>

        {/* Demographics */}
        <div
          className={`sidebar-item ${
            activeView === "societal" ? "active" : ""
          }`}
          onClick={() => setActiveView("societal")}
        >
          <Users size={18} />
          <span>Demographics</span>
        </div>

        {/* Resource Planner */}
        <div
          className={`sidebar-item ${
            activeView === "resource" ? "active" : ""
          }`}
          onClick={() => setActiveView("resource")}
        >
          <BarChart3 size={18} />
          <span>Resource Planning</span>
        </div>

        {/* Reports */}
        <div
          className={`sidebar-item ${
            activeView === "reports" ? "active" : ""
          }`}
          onClick={() => setActiveView("reports")}
        >
          <FileText size={18} />
          <span>Reports</span>
        </div>
      </nav>

      {/* Footer */}
      <div className="sidebar-footer">
        <div className="avatar">AU</div>
        <div>
          <strong>Admin User</strong>
          <p>admin@gov.in</p>
        </div>
      </div>
    </aside>
  );
}
