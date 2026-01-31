import { useEffect, useState } from "react";

export default function ModelBreakdown() {
  const [rows, setRows] = useState<any[]>([]);

  useEffect(() => {
    fetch("/wallet_intelligence.json")
      .then(r => r.json())
      .then(setRows);
  }, []);

  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th align="left">Wallet</th>
          <th align="right">Heuristic</th>
          <th align="right">GNN</th>
          <th align="right">Combined</th>
        </tr>
      </thead>
      <tbody>
        {rows.slice(0, 20).map(r => (
          <tr key={r.wallet}>
            <td>{r.wallet}</td>
            <td align="right">{r.heuristic_risk.toFixed(3)}</td>
            <td align="right">{r.gnn_score.toFixed(3)}</td>
            <td
              align="right"
              style={{ color: r.combined_score > 0.8 ? "#f87171" : "#facc15" }}
            >
              {r.combined_score.toFixed(3)}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
