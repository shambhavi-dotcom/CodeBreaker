# t2_run.py

import numpy as np
from t2_config import (
    STATS_CSV, GRAPH_FILE, LABELS_CSV,
    FAN_IN_THRESHOLD, FAN_OUT_THRESHOLD,
    PEEL_RATIO, MIN_PEEL_CHAIN_LEN, MAX_HOPS,
    PROX_MAX_DEPTH, PROX_STEP_PENALTY,
    W_PROX, W_FAN_OUT, W_FAN_IN, W_PEEL, W_CENT,
    OUT_SCORES_CSV
)

from t2_io import load_graph, load_stats, load_illicit_seeds
from analysis.t2_analysis import (
    add_fan_flags, add_peeling_features, add_illicit_proximity,
    add_centrality_proxy, add_risk_score
)

def main():
    print("=== Teammate 2: Flags + Scoring ===")

    G = load_graph(GRAPH_FILE)
    stats = load_stats(STATS_CSV)
    illicit_seeds = load_illicit_seeds(LABELS_CSV)

    print("Graph:", G.number_of_nodes(), "nodes,", G.number_of_edges(), "edges")
    print("Stats:", stats.shape)
    print("Illicit seeds:", len(illicit_seeds))

    stats2 = add_fan_flags(stats, FAN_IN_THRESHOLD, FAN_OUT_THRESHOLD)
    stats2 = add_peeling_features(G, stats2, PEEL_RATIO, MIN_PEEL_CHAIN_LEN, MAX_HOPS)
    stats2 = add_illicit_proximity(G, stats2, illicit_seeds, PROX_MAX_DEPTH, PROX_STEP_PENALTY)
    stats2 = add_centrality_proxy(stats2)
    stats2 = add_risk_score(stats2, W_PROX, W_FAN_OUT, W_FAN_IN, W_PEEL, W_CENT)

    # placeholder for teammate 3
    stats2["gnn_score"] = np.nan

    out = stats2.reset_index().rename(columns={"index": "wallet_id"})
    out = out[[
        "wallet_id",
        "in_degree", "out_degree",
        "total_in_amount", "total_out_amount",
        "is_fan_in", "is_fan_out",
        "is_peeling", "peeling_depth",
        "illicit_proximity", "centrality",
        "risk_score", "gnn_score"
    ]]

    out.to_csv(OUT_SCORES_CSV, index=False)
    print(f"Saved: {OUT_SCORES_CSV} ✅")

if __name__ == "__main__":
    main()
