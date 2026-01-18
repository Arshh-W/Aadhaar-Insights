import React from "react";

export default function DistrictTable({ districts, loading }) {
  return (
    <div className="table-card">
      {loading ? (
        <p style={{ textAlign: "center", color: "#6b7280" }}>Loading districts...</p>
      ) : districts && districts.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>District</th>
              <th>Risk Level</th>
              <th>Enrollments</th>
            </tr>
          </thead>
          <tbody>
            {districts.map((d, idx) => (
              <tr key={idx}>
                <td>{d.district}</td>
                <td
                  className={
                    d.risk?.toLowerCase() === "high"
                      ? "risk high"
                      : d.risk?.toLowerCase() === "medium"
                      ? "risk medium"
                      : "risk low"
                  }
                >
                  {d.risk}
                </td>
                <td>{d.enrollments}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p style={{ textAlign: "center", color: "#6b7280" }}>No district data yet</p>
      )}
    </div>
  );
}
