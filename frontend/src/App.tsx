import { useState } from "react";

import GraphView from "./components/Graphview";
import SummaryCards from "./components/SummaryCards";
import TopWallets from "./components/topwallets";
import Explanation from "./components/Explanation";
import WalletSearch from "./components/walletsearch";
import ModelBreakdown from "./components/modelbreakdown";

type WalletIntel = {
  wallet: string;
  heuristic_risk: number;
  gnn_score: number;
  combined_score: number;
};

type Panel =
  | "overview"
  | "wallet"
  | "top"
  | "models";

export default function App() {
  const [panel, setPanel] = useState<Panel>("overview");
  const [selectedWallet, setSelectedWallet] = useState<WalletIntel | null>(null);

  return (
    <div style={{ width: "100vw", height: "100vh", display: "flex", flexDirection: "column" }}>

      {/* HEADER */}
      <div
        style={{
          height: 56,
          background: "#0f172a",
          color: "white",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 16px",
          borderBottom: "1px solid #1e293b"
        }}
      >
        <strong style={{ color: "#f87171" }}>
          🚨 Crypto Intelligence Dashboard
        </strong>

        <div style={{ display: "flex", gap: 8 }}>
          <Btn label="Overview" onClick={() => setPanel("overview")} />
          <Btn label="Wallet" onClick={() => setPanel("wallet")} />
          <Btn label="Top Wallets" onClick={() => setPanel("top")} />
          <Btn label="Models" onClick={() => setPanel("models")} />
        </div>
      </div>

      {/* MAIN CONTENT */}
      <div style={{ flex: 1, display: "flex" }}>

        {/* GRAPH — ALWAYS VISIBLE */}
        <div style={{ flex: 0.65, position: "relative" }}>
          <GraphView />
        </div>

        {/* RIGHT PANEL */}
        <div
          style={{
            flex: 0.35,
            background: "#020617",
            color: "white",
            borderLeft: "1px solid #1e293b",
            overflowY: "auto",
            padding: 16
          }}
        >

          {/* OVERVIEW */}
          {panel === "overview" && (
            <>
              <h2 style={{ marginBottom: 12 }}>📊 System Overview</h2>
              <SummaryCards />
            </>
          )}

          {/* WALLET SEARCH + DETAILS */}
          {panel === "wallet" && (
            <>
              <h2 style={{ marginBottom: 8 }}>🔍 Wallet Search</h2>

              <WalletSearch
                onSelect={(w) => {
                  setSelectedWallet(w);
                }}
              />

              {selectedWallet && (
                <>
                  <div
                    style={{
                      marginTop: 16,
                      padding: 12,
                      border: "1px solid #1e293b",
                      borderRadius: 8
                    }}
                  >
                    <h3 style={{ marginBottom: 6 }}>📌 Wallet Profile</h3>

                    <Metric label="Heuristic Risk" value={selectedWallet.heuristic_risk} />
                    <Metric label="GNN Score" value={selectedWallet.gnn_score} />
                    <Metric label="Combined Score" value={selectedWallet.combined_score} />
                  </div>

                  <div style={{ marginTop: 16 }}>
                    <Explanation wallet={selectedWallet.wallet} />
                  </div>
                </>
              )}
            </>
          )}

          {/* TOP WALLETS */}
          {panel === "top" && (
            <>
              <h2 style={{ marginBottom: 12 }}>🏆 Highest Risk Wallets</h2>
              <TopWallets />
            </>
          )}

          {/* MODEL BREAKDOWN */}
          {panel === "models" && (
            <>
              <h2 style={{ marginBottom: 12 }}>🤖 Model Breakdown</h2>
              <ModelBreakdown />
            </>
          )}

        </div>
      </div>
    </div>
  );
}

/* ---------- SMALL REUSABLE UI ---------- */

function Btn({ label, onClick }: { label: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "6px 12px",
        borderRadius: 6,
        background: "#1e293b",
        color: "white",
        border: "none",
        cursor: "pointer"
      }}
    >
      {label}
    </button>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  const color =
    value > 0.8 ? "#f87171" :
    value > 0.6 ? "#facc15" :
    "#4ade80";

  return (
    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
      <span>{label}</span>
      <span style={{ color, fontWeight: 600 }}>
        {value.toFixed(3)}
      </span>
    </div>
  );
}
