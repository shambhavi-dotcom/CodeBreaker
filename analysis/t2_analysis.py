# t2_analysis.py

import pandas as pd
from collections import deque

def add_fan_flags(stats: pd.DataFrame, fan_in_th: int, fan_out_th: int) -> pd.DataFrame:
    stats = stats.copy()
    stats["is_fan_in"] = (stats["in_degree"] >= fan_in_th).astype(int)
    stats["is_fan_out"] = (stats["out_degree"] >= fan_out_th).astype(int)
    return stats

def find_peel_wallets(stats: pd.DataFrame, peel_ratio: float) -> set[str]:
    peel = set()
    for w in stats.index:
        if stats.loc[w, "out_degree"] != 1:
            continue
        in_amt = stats.loc[w, "total_in_amount"]
        out_amt = stats.loc[w, "total_out_amount"]
        if in_amt <= 0:
            continue
        if (out_amt / in_amt) >= peel_ratio:
            peel.add(w)
    return peel

def compute_peeling_depth(G, peel_set: set[str], start_wallet: str, max_hops: int) -> int:
    depth = 0
    current = start_wallet
    for _ in range(max_hops):
        if current not in peel_set:
            break
        out_edges = list(G.out_edges(current))
        if len(out_edges) != 1:
            break
        _, nxt = out_edges[0]
        depth += 1
        current = nxt
    return depth

def add_peeling_features(G, stats: pd.DataFrame, peel_ratio: float, min_chain_len: int, max_hops: int) -> pd.DataFrame:
    stats = stats.copy()
    peel_set = find_peel_wallets(stats, peel_ratio)

    stats["is_peeling"] = stats.index.map(lambda w: int(w in peel_set))
    stats["peeling_depth"] = stats.index.map(lambda w: compute_peeling_depth(G, peel_set, w, max_hops))
    stats["is_peeling_chain"] = (stats["peeling_depth"] >= min_chain_len).astype(int)

    return stats

def multi_source_bfs_distance(G, sources: list[str], max_depth: int) -> dict[str, int]:
    dist = {}
    q = deque()

    for s in sources:
        if s in G:
            dist[s] = 0
            q.append(s)

    while q:
        u = q.popleft()
        if dist[u] >= max_depth:
            continue
        for _, v in G.out_edges(u):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)

    return dist

def add_illicit_proximity(G, stats: pd.DataFrame, illicit_seeds: list[str], max_depth: int, step_penalty: float) -> pd.DataFrame:
    stats = stats.copy()

    if not illicit_seeds:
        stats["illicit_proximity"] = 0.0
        return stats

    dist_map = multi_source_bfs_distance(G, illicit_seeds, max_depth=max_depth)

    def dist_to_prox(w):
        d = dist_map.get(w, None)
        if d is None:
            return 0.0
        return max(0.0, 1.0 - step_penalty * d)

    stats["illicit_proximity"] = stats.index.map(dist_to_prox)
    return stats

def add_centrality_proxy(stats: pd.DataFrame) -> pd.DataFrame:
    stats = stats.copy()
    deg = stats["in_degree"] + stats["out_degree"]
    stats["centrality"] = (deg / (deg.max() if deg.max() > 0 else 1)).astype(float)
    return stats

def add_risk_score(stats: pd.DataFrame,
                   w_prox: float, w_fan_out: float, w_fan_in: float, w_peel: float, w_cent: float) -> pd.DataFrame:
    stats = stats.copy()

    # normalize peeling depth
    pdmax = stats["peeling_depth"].max() if "peeling_depth" in stats.columns else 0
    peel_depth_norm = stats["peeling_depth"] / (pdmax if pdmax > 0 else 1)

    stats["risk_score"] = (
        w_prox * stats.get("illicit_proximity", 0.0) +
        w_fan_out * stats.get("is_fan_out", 0).astype(float) +
        w_fan_in * stats.get("is_fan_in", 0).astype(float) +
        w_peel * (0.7 * stats.get("is_peeling_chain", 0).astype(float) + 0.3 * peel_depth_norm) +
        w_cent * stats.get("centrality", 0.0)
    ).clip(0, 1)

    return stats
