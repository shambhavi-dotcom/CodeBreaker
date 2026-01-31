# src/config.py

# ---------- INPUT ----------
INPUT_CSV = "wallet_transactions_synthetic.csv"

# ---------- FILTERS ----------
# Set to None to disable
USE_LAST_N_DAYS = 30  # keep only last N days from latest timestamp
MIN_AMOUNT = 1e-6  # remove dust / zero-ish transfers

REMOVE_SELF_LOOPS = True  # drop src == dst rows

# ---------- OUTPUTS ----------
OUT_STATS_CSV = "wallet_raw_stats.csv"
OUT_GRAPH_FILE = "wallet_graph.gpickle"