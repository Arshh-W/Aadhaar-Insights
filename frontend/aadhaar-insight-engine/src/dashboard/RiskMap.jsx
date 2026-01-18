import { MapContainer, TileLayer, CircleMarker, Tooltip } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function RiskMap({ data }) {
  if (!data || data.length === 0) return <div>No threat data available</div>;

  return (
    <MapContainer center={[20.59, 78.96]} zoom={5} scrollWheelZoom={false} style={{ height: "400px", width: "100%" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {data.map((p, i) => (
        <CircleMarker
          key={i}
          center={[p.lat, p.lng]}
          radius={8}
          pathOptions={{ color: "red", fillOpacity: 0.6 }}
        >
          <Tooltip>
            <strong>{p.district}</strong><br />
            Risk Score: {p.score || 0}
          </Tooltip>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
