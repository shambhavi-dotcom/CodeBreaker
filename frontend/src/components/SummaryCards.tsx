import { useEffect, useState } from "react";

export default function SummaryCards() {
  const [data, setData] = useState<Record<string, number> | null>(null);

  useEffect(() => {
    fetch("/summary.json")
      .then(r => r.json())
      .then(setData);
  }, []);

  if (!data) return null;

  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
      {Object.entries(data).map(([k, v]) => (
        <div
          key={k}
          style={{
            background: "#020617",
            border: "1px solid #1e293b",
            borderRadius: 8,
            padding: 16
          }}
        >
          <div style={{ fontSize: 12, color: "#94a3b8" }}>
            {k.replace("_", " ").toUpperCase()}
          </div>
          <div style={{ fontSize: 28, fontWeight: 600 }}>
            {v}
          </div>
        </div>
      ))}
    </div>
  );
}
