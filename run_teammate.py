# src/run_teammate1.py
import pickle
import os
import networkx as nx

from config import (
    INPUT_CSV, USE_LAST_N_DAYS, MIN_AMOUNT, REMOVE_SELF_LOOPS,
    OUT_STATS_CSV, OUT_GRAPH_FILE
)
from pipeline import load_data, clean_data, filter_data, build_graph, compute_wallet_stats


def ensure_parent_dir(path: str):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def main():
    print("=== Teammate 1: Graph Backbone ===")

    # Make sure output folders exist
    ensure_parent_dir(OUT_STATS_CSV)
    ensure_parent_dir(OUT_GRAPH_FILE)

    # 1) Load
    df = load_data(INPUT_CSV)
    print("Loaded:", df.shape)

    # 2) Clean
    df = clean_data(df, remove_self_loops=REMOVE_SELF_LOOPS)
    print("After cleaning:", df.shape)

    # 3) Filter
    df = filter_data(df, use_last_n_days=USE_LAST_N_DAYS, min_amount=MIN_AMOUNT)
    print("After filtering:", df.shape)

    # 4) Graph
    G = build_graph(df)
    print("Graph built ✅  Nodes:", G.number_of_nodes(), "Edges:", G.number_of_edges())

    # 5) Stats
    stats = compute_wallet_stats(df)
    print("Stats computed ✅  Wallets:", len(stats))

    # 6) Save outputs
    stats.to_csv(OUT_STATS_CSV, index_label="wallet_id")
    with open(OUT_GRAPH_FILE, "wb") as f:
        pickle.dump(G, f)

    print("\nSaved outputs ✅")
    print("1) Stats:", OUT_STATS_CSV)
    print("2) Graph:", OUT_GRAPH_FILE)


if __name__ == "__main__":
    main()
