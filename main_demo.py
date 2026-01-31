import pickle
import networkx as nx
import pandas as pd
import torch
import json
import os

FRONTEND_PUBLIC = "frontend/public"
os.makedirs(FRONTEND_PUBLIC, exist_ok=True)

def save_frontend_json(name, obj):
    with open(os.path.join(FRONTEND_PUBLIC, name), "w") as f:
        json.dump(obj, f, indent=2, default=str)


# =========================
# Imports
# =========================
from config import OUT_GRAPH_FILE

from analysis.t2_analysis import (
    add_fan_flags,
    add_peeling_features,
    add_illicit_proximity,
    add_centrality_proxy,
    add_risk_score
)

from features.node_features import compute_node_features
from explain.explain_suspect import explain_wallet
from viz.visualize import visualize_suspicious_subgraph

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from gnn.prepare_data import build_pyg_data
from gnn.train import train_gnn


print("\n=== INTELLIGENCE PIPELINE START ===")

# =========================
# 1️⃣ Load graph (Teammate 1)
# =========================
with open(OUT_GRAPH_FILE, "rb") as f:
    G_multi = pickle.load(f)

G = nx.DiGraph(G_multi)

print("Loaded graph")
print("Nodes:", G.number_of_nodes(), "Edges:", G.number_of_edges())

save_frontend_json("summary.json", {
    "nodes": G.number_of_nodes(),
    "edges": G.number_of_edges(),
    "illicit_wallets": len([n for n in G.nodes() if "illicit" in n])
})



# =========================
# 2️⃣ Load wallet stats (Teammate 1)
# =========================
stats_df = pd.read_csv("wallet_raw_stats.csv", index_col="wallet_id")
print("Loaded wallet stats:", stats_df.shape)


# =========================
# 3️⃣ Load REAL illicit labels
# =========================
labels_df = pd.read_csv("wallet_labels_synthetic.csv")
labels_df.columns = [c.lower() for c in labels_df.columns]

# ---- Parse illicit wallets correctly ----
illicit_wallets = set(
    labels_df.loc[labels_df["label"] == "illicit", "wallet_id"]
)

print("Loaded real illicit wallets:", len(illicit_wallets))


# =========================
# 4️⃣ Teammate 2 heuristic analysis
# =========================
stats_df = add_fan_flags(stats_df, fan_in_th=10, fan_out_th=10)

stats_df = add_peeling_features(
    G,
    stats_df,
    peel_ratio=0.9,
    min_chain_len=2,
    max_hops=5
)

stats_df = add_illicit_proximity(
    G,
    stats_df,
    illicit_seeds=list(illicit_wallets),
    max_depth=5,
    step_penalty=0.15
)

stats_df = add_centrality_proxy(stats_df)

stats_df = add_risk_score(
    stats_df,
    w_prox=0.35,
    w_fan_out=0.2,
    w_fan_in=0.2,
    w_peel=0.15,
    w_cent=0.1
)

print("Computed heuristic risk scores")


# =========================
# 5️⃣ Visualization (heuristic risk)
# =========================
visualize_suspicious_subgraph(
    G,
    stats_df["risk_score"].to_dict()
)


# =========================
# 6️⃣ Feature extraction (ML / GNN)
# =========================
features_df = compute_node_features(G)

features_df["heuristic_risk"] = stats_df.loc[
    features_df.index, "risk_score"
]

features_df["label"] = features_df.index.isin(illicit_wallets).astype(int)

print("\nNode feature table:", features_df.shape)
print("Label distribution:")
print(features_df["label"].value_counts())


# =========================
# 7️⃣ Baseline ML (Random Forest)
# =========================
X = features_df.drop(columns=["label"])
y = features_df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print("\n=== BASELINE ML RESULTS ===")
print(classification_report(y_test, y_pred))

print("\n=== FEATURE IMPORTANCE ===")
print(pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False))


# =========================
# 8️⃣ GNN
# =========================
data = build_pyg_data(G, features_df.drop(columns=["label"]))
labels = torch.tensor(features_df["label"].values, dtype=torch.long)

gnn_scores = train_gnn(data, labels)

features_df["gnn_score"] = gnn_scores


# =========================
# 9️⃣ Combine heuristic + GNN
# =========================
features_df["combined_score"] = (
    0.6 * features_df["gnn_score"] +
    0.4 * features_df["heuristic_risk"]
)

print("\n=== TOP SUSPICIOUS WALLETS (COMBINED) ===")
print(features_df.sort_values("combined_score", ascending=False).head(5))

# =========================
# SAVE TOP HIGH-RISK WALLETS (FRONTEND)
# =========================

# =========================
# SAVE TOP WALLETS (PERCENTILE-BASED)
# =========================

threshold = features_df["combined_score"].quantile(0.95)
print(f"Top-wallet threshold (95th percentile): {threshold:.3f}")

top_wallets_df = (
    features_df
    .sort_values("combined_score", ascending=False)
    .query("combined_score >= @threshold")
    .head(10)
    .copy()
)

top_wallets_df["wallet"] = top_wallets_df.index
top_wallets_df = top_wallets_df.reset_index(drop=True)

save_frontend_json(
    "top_wallets.json",
    top_wallets_df[["wallet", "combined_score"]].to_dict(orient="records")
)
# =========================

# =========================
# 🔟 Explain top suspect
# =========================
top_wallet = features_df.sort_values(
    "combined_score", ascending=False
).index[0]

print("\n=== EXPLANATION FOR TOP SUSPICIOUS WALLET ===")
print("Wallet:", top_wallet)

reasons = explain_wallet(
    wallet_id=top_wallet,
    G=G,
    risk_scores=stats_df["risk_score"].to_dict(),
    features_df=features_df,
    illicit_wallets=illicit_wallets
)

for r in reasons:
    print("-", r)

save_frontend_json("explanation.json", {
    "wallet": top_wallet,
    "reasons": reasons
})


print("\n=== PIPELINE COMPLETE ===")

# =========================
# SAVE FULL WALLET INTELLIGENCE
# =========================

wallet_intel = (
    features_df[
        ["heuristic_risk", "gnn_score", "combined_score"]
    ]
    .copy()
)

wallet_intel["wallet"] = wallet_intel.index
wallet_intel = wallet_intel.reset_index(drop=True)

save_frontend_json(
    "wallet_intelligence.json",
    wallet_intel.to_dict(orient="records")
)
wallet_explanations = {}

for wallet in wallet_intel["wallet"]:
    wallet_explanations[wallet] = explain_wallet(
        wallet_id=wallet,
        G=G,
        risk_scores=stats_df["risk_score"].to_dict(),
        features_df=features_df,
        illicit_wallets=illicit_wallets
    )


save_frontend_json("wallet_explanations.json", wallet_explanations)
