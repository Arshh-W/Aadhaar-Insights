import "../styles/statcard.css";

export default function StatCard({ title, value, trend, icon: Icon, danger, warning, loading }) {
  return (
    <div className={`stat-card ${danger ? "danger" : ""} ${warning ? "warning" : ""}`}>
      <div className="stat-header">
        <p className="stat-title">{title}</p>
        {Icon && <Icon size={20} />}
      </div>

      <h2 className="stat-value">
        {loading ? "Loading..." : value || "--"}
      </h2>
      {trend && <span className="stat-trend">{trend}</span>}
    </div>
  );
}
