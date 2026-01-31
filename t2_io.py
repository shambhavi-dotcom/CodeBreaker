# t2_io.py

import pickle
import pandas as pd

REQUIRED_STATS_COLS = ["total_in_amount", "total_out_amount", "in_degree", "out_degree"]

def load_graph(graph_file: str):
    with open(graph_file, "rb") as f:
        return pickle.load(f)

def load_stats(stats_csv: str) -> pd.DataFrame:
    stats = pd.read_csv(stats_csv)

    if "wallet_id" not in stats.columns:
        raise ValueError("wallet_raw_stats.csv must contain 'wallet_id' column.")

    stats = stats.set_index("wallet_id")

    # ensure required numeric columns exist
    for c in REQUIRED_STATS_COLS:
        if c not in stats.columns:
            raise ValueError(f"wallet_raw_stats.csv missing required column: {c}")
        stats[c] = pd.to_numeric(stats[c], errors="coerce").fillna(0)

    return stats

def load_illicit_seeds(labels_csv: str | None) -> list[str]:
    if labels_csv is None:
        return []

    labels = pd.read_csv(labels_csv)

    if "label" not in labels.columns or "wallet_id" not in labels.columns:
        return []

    # Prefer seed illicit wallets if present
    if "is_seed" in labels.columns:
        seeds = labels[(labels["label"] == "illicit") & (labels["is_seed"] == 1)]["wallet_id"].tolist()
        return seeds

    # fallback: all illicit
    return labels[labels["label"] == "illicit"]["wallet_id"].tolist()
