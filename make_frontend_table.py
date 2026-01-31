import pandas as pd

stats = pd.read_csv("wallet_raw_stats.csv")
scores = pd.read_csv("wallet_scores.csv")

df = stats.merge(scores, on="wallet_id", how="left")

frontend_df = df[[
    "wallet_id",
    "in_degree_x",
    "out_degree_x",
    "total_in_amount_x",
    "total_out_amount_x",
    "is_fan_in",
    "is_fan_out",
    "is_peeling",
    "peeling_depth",
    "risk_score",
    "gnn_score"
]].rename(columns={
    "in_degree_x": "in_degree",
    "out_degree_x": "out_degree",
    "total_in_amount_x": "total_in_amount",
    "total_out_amount_x": "total_out_amount"
})

frontend_df.to_csv("wallet_frontend_table.csv", index=False)
print("Saved wallet_frontend_table.csv ✅")
