import { useEffect, useState } from "react";

export default function Explanation({ wallet }: { wallet: string | null }) {
  const [data, setData] = useState<Record<string, string[]> | null>(null);

  useEffect(() => {
    fetch("/wallet_explanations.json")
      .then(r => r.json())
      .then(setData);
  }, []);

  if (!wallet || !data || !data[wallet]) {
    return <div>Select a wallet to see explanation</div>;
  }

  return (
    <div>
      <h2 style={{ fontSize: 18, marginBottom: 8 }}>
        🧠 Why this wallet is risky
      </h2>

      <ul style={{ paddingLeft: 16 }}>
        {data[wallet].map((r, i) => (
          <li key={i} style={{ marginBottom: 6 }}>
            {r}
          </li>
        ))}
      </ul>
    </div>
  );
}
