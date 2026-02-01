import { useState } from "react";

export default function GraphView() {
  const [risk, setRisk] = useState<"all" | "high" | "medium" | "low">("all");

  return (
    <div style={{ position: "relative", width: "100%", height: "100%" }}>
      
      {/* GRAPH */}
      <iframe
        key={risk} // forces reload when risk changes
        src={`/graph.html?risk=${risk}`}
        title="Suspicious Graph"
        style={{
          width: "100%",
          height: "100%",
          border: "none"
        }}
      />

      {/* FILTER BUTTONS */}
      <div
        style={{
          position: "absolute",
          bottom: 16,
          left: 16,
          display: "flex",
          gap: 8,
          zIndex: 10,
          background: "rgba(0,0,0,0.6)",
          padding: 8,
          borderRadius: 8
        }}
      >
        <button onClick={() => setRisk("high")}>🔴 High</button>
        <button onClick={() => setRisk("medium")}>🟠 Medium</button>
        <button onClick={() => setRisk("low")}>🟢 Low</button>
        <button onClick={() => setRisk("all")}>🔁 All</button>
      </div>
    </div>
  );
}
