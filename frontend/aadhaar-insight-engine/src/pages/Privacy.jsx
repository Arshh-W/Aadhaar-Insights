import { ShieldCheck, Lock, EyeOff } from "lucide-react";
import "./Privacy.css";

function Privacy() {
  return (
    <div className="page-container">
    <div className="privacy-page">
      <h1>Privacy & Data Protection</h1>
      <p className="subtitle">
        Designed with privacy-first principles aligned with UIDAI guidelines.
      </p>

      <div className="privacy-cards">
        <div className="privacy-card">
          <ShieldCheck size={32} />
          <h3>Anonymized Data</h3>
          <p>
            All analytics are performed on aggregated and anonymized metadata.
            No individual Aadhaar records are accessed or displayed.
          </p>
        </div>

        <div className="privacy-card">
          <Lock size={32} />
          <h3>Secure Architecture</h3>
          <p>
            The system follows a modular design ensuring strict separation
            between identity data and analytical layers.
          </p>
        </div>

        <div className="privacy-card">
          <EyeOff size={32} />
          <h3>No Personal Tracking</h3>
          <p>
            The platform does not track individuals — it detects patterns at a
            population level only.
          </p>
        </div>
      </div>

      <div className="privacy-note">
        <p>
          This prototype demonstrates how insights can be derived without
          compromising citizen privacy or data security.
        </p>
      </div>
      </div>
    </div>
  );
}

export default Privacy;
