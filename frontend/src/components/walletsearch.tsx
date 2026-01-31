import { useEffect, useState } from "react";

type WalletIntel = {
  wallet: string;
  heuristic_risk: number;
  gnn_score: number;
  combined_score: number;
};

export default function WalletSearch({
  onSelect
}: {
  onSelect: (wallet: WalletIntel) => void;
}) {
  const [data, setData] = useState<WalletIntel[]>([]);
  const [query, setQuery] = useState("");

  useEffect(() => {
    fetch("/wallet_intelligence.json")
      .then(r => r.json())
      .then(setData);
  }, []);

  const results = data.filter(w =>
    w.wallet.toLowerCase().includes(query.toLowerCase())
  ).slice(0, 10);

  return (
    <div>
      <input
        placeholder="Search wallet…"
        value={query}
        onChange={e => setQuery(e.target.value)}
        style={{
          width: "100%",
          padding: 8,
          borderRadius: 6,
          border: "1px solid #334155",
          background: "#020617",
          color: "white"
        }}
      />

      {query && (
        <div style={{ marginTop: 8 }}>
          {results.map(w => (
            <div
              key={w.wallet}
              onClick={() => onSelect(w)}
              style={{
                padding: 6,
                cursor: "pointer",
                borderBottom: "1px solid #1e293b"
              }}
            >
              {w.wallet}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
