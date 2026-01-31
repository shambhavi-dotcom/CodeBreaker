import { useEffect, useState } from "react";

type Row = {
  wallet: string;
  combined_score: number;
};

export default function TopWallets() {
  const [rows, setRows] = useState<Row[]>([]);

  useEffect(() => {
    fetch("/top_wallets.json")
      .then(r => r.json())
      .then(setRows);
  }, []);

  return (
    <div>
      <h2 style={{ fontSize: 18, marginBottom: 12 }}>
        🔴 Top Suspicious Wallets
      </h2>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ borderBottom: "1px solid #334155" }}>
            <th align="left">Wallet</th>
            <th align="right">Risk</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(r => (
            <tr key={r.wallet} style={{ borderBottom: "1px solid #1e293b" }}>
              <td style={{ fontFamily: "monospace", padding: "6px 0" }}>
                {r.wallet}
              </td>
              <td align="right" style={{ color: r.combined_score > 0.8 ? "#f87171" : "#facc15" }}>
                {r.combined_score.toFixed(3)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
