import networkx as nx

def compute_risk_scores(G, illicit_wallets, fan_flags, peeling_flags):
    """
    G: NetworkX DiGraph
    illicit_wallets: set of wallet_ids
    fan_flags: dict {wallet_id: {"fan_in":0/1, "fan_out":0/1}}
    peeling_flags: dict {wallet_id: {"is_peeling":0/1, "depth":int}}
    """

    # Centrality (cheap + effective)
    centrality = nx.betweenness_centrality(G, normalized=True)

    risk_scores = {}

    for node in G.nodes():
        score = 0.0

        # 1. Direct or indirect illicit connection
        if node in illicit_wallets:
            score += 0.35
        else:
            for bad in illicit_wallets:
                if nx.has_path(G, bad, node):
                    score += 0.20
                    break

        # 2. Fan patterns
        if fan_flags.get(node, {}).get("fan_out", 0):
            score += 0.20
        if fan_flags.get(node, {}).get("fan_in", 0):
            score += 0.20

        # 3. Peeling
        if peeling_flags.get(node, {}).get("is_peeling", 0):
            score += 0.15

        # 4. Structural importance
        score += 0.10 * centrality.get(node, 0)

        risk_scores[node] = min(score, 1.0)

    return risk_scores
