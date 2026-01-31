# t2_config.py

# Inputs from Teammate 1
STATS_CSV = "wallet_raw_stats.csv"
GRAPH_FILE = "wallet_graph.gpickle"

# Optional labels file (for illicit seed list)
LABELS_CSV = "wallet_labels_synthetic.csv"   # set to None if you don't have it

# Fan thresholds
FAN_IN_THRESHOLD = 5
FAN_OUT_THRESHOLD = 5

# Peeling settings
PEEL_RATIO = 0.90
MIN_PEEL_CHAIN_LEN = 3
MAX_HOPS = 12

# Illicit proximity settings
PROX_MAX_DEPTH = 6
PROX_STEP_PENALTY = 0.2  # dist 0->1.0, 1->0.8, 2->0.6...

# Baseline risk weights
W_PROX = 0.35
W_FAN_OUT = 0.20
W_FAN_IN = 0.20
W_PEEL = 0.15
W_CENT = 0.10

# Output for frontend
OUT_SCORES_CSV = "wallet_scores.csv"
