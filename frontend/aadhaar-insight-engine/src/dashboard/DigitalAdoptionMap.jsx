import { MapContainer, TileLayer, CircleMarker, Tooltip } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const COLORS = {
  "Urban / Digital Hub": "#22c55e",
  "Manual Labor Zone": "#ef4444",
  "Evolving / Mixed": "#eab308"
};

export default function DigitalAdoptionMap({ data }) {
  if (!data || data.length === 0) return <div>No digital adoption data available</div>;

  return (
    <MapContainer center={[20.59, 78.96]} zoom={5} scrollWheelZoom={false} style={{ height: "400px", width: "100%" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {data.map((p, i) => (
        <CircleMarker
          key={i}
          center={[p.lat, p.lng]}
          radius={6}
          pathOptions={{ color: COLORS[p.cluster_name] || "#6366f1", fillOpacity: 0.7 }}
        >
          <Tooltip>
            <strong>{p.district}</strong><br />
            {p.cluster_name}
          </Tooltip>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
