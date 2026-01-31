# src/pipeline.py

import pandas as pd
import networkx as nx

REQUIRED_COLS = ["source_wallet_id", "dest_wallet_id", "timestamp", "amount", "token-type"]


def load_data(input_csv: str) -> pd.DataFrame:
    df = pd.read_csv(input_csv)

    # Normalize possible alternate column names
    df = df.rename(columns={
        "dest-wallet-id": "dest_wallet_id",
        "token_type": "token-type"
    })

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}\nFound columns: {list(df.columns)}")

    return df


def clean_data(df: pd.DataFrame, remove_self_loops: bool = True) -> pd.DataFrame:
    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df = df.dropna(subset=REQUIRED_COLS)

    if remove_self_loops:
        df = df[df["source_wallet_id"] != df["dest_wallet_id"]]

    return df


def filter_data(df: pd.DataFrame, use_last_n_days: int | None = 30, min_amount: float | None = 1e-6) -> pd.DataFrame:
    df = df.copy()

    if use_last_n_days is not None:
        end_time = df["timestamp"].max()
        cutoff = end_time - pd.Timedelta(days=use_last_n_days)
        df = df[df["timestamp"] >= cutoff].copy()

    if min_amount is not None:
        df = df[df["amount"] >= min_amount].copy()

    return df


def build_graph(df: pd.DataFrame) -> nx.MultiDiGraph:
    # Keep every transaction edge (MultiDiGraph)
    G = nx.MultiDiGraph()

    for _, row in df.iterrows():
        G.add_edge(
            row["source_wallet_id"],
            row["dest_wallet_id"],
            amount=float(row["amount"]),
            timestamp=row["timestamp"],
            token=row["token-type"]
        )

    return G


def compute_wallet_stats(df: pd.DataFrame) -> pd.DataFrame:
    # Totals
    out_amt = df.groupby("source_wallet_id")["amount"].sum().rename("total_out_amount")
    in_amt = df.groupby("dest_wallet_id")["amount"].sum().rename("total_in_amount")

    # Degrees (unique neighbors)
    out_deg = df.groupby("source_wallet_id")["dest_wallet_id"].nunique().rename("out_degree")
    in_deg  = df.groupby("dest_wallet_id")["source_wallet_id"].nunique().rename("in_degree")

    # Timestamp list per wallet (as src or dst)
    src_times = df.groupby("source_wallet_id")["timestamp"].apply(list)
    dst_times = df.groupby("dest_wallet_id")["timestamp"].apply(list)

    all_wallets = pd.Index(df["source_wallet_id"]).append(pd.Index(df["dest_wallet_id"])).unique()

    timestamps_list = {}
    for w in all_wallets:
        times = []
        if w in src_times: times += src_times[w]
        if w in dst_times: times += dst_times[w]
        timestamps_list[w] = sorted(times)

    # Combine into one table
    stats = pd.DataFrame(index=all_wallets)
    stats = stats.join(in_amt).join(out_amt).join(in_deg).join(out_deg)
    stats = stats.fillna(0)

    stats["timestamps_list"] = stats.index.map(lambda w: timestamps_list.get(w, []))
    return stats
