import { Bell, Settings, User, Search, ShieldCheck } from "lucide-react";
import "../styles/topbar.css";

export default function Topbar({ title }) {
  return (
    <header className="topbar">
      {/* Left: Branding & Title */}
      <div className="topbar-left">
        <div className="status-indicator">
          <ShieldCheck size={18} className="shield-icon" />
          <span className="status-text">System Secure</span>
        </div>
        <h2 className="topbar-title">{title || "Intelligence Overview"}</h2>
      </div>

      {/* Middle: Global Search (Useful for finding districts) */}
      <div className="topbar-center">
        <div className="search-wrapper">
          <Search size={18} />
          <input type="text" placeholder="Search District or UIDAI Node..." />
        </div>
      </div>

      {/* Right: Actions & Profile */}
      <div className="topbar-right">
        <div className="action-icons">
          <button className="icon-btn" title="Notifications">
            <Bell size={20} />
            <span className="badge-dot"></span>
          </button>
          <button className="icon-btn" title="System Settings">
            <Settings size={20} />
          </button>
        </div>

        <div className="user-profile">
          <div className="user-info">
            <span className="user-name">Admin User</span>
            <span className="user-role">Control Officer</span>
          </div>
          <div className="user-avatar">
            <User size={20} />
          </div>
        </div>
      </div>
    </header>
  );
}