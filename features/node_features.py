import networkx as nx
import pandas as pd

def compute_node_features(G):
    """
    Takes a NetworkX graph and returns a DataFrame
    where each row = wallet, each column = feature.
    """

    # Precompute PageRank once (important)
    pagerank = nx.pagerank(G)

    features = {}

    for node in G.nodes():
        features[node] = {
            "in_degree": G.in_degree(node),
            "out_degree": G.out_degree(node),
            "total_degree": G.degree(node),
            "pagerank": pagerank.get(node, 0)
        }

    df = pd.DataFrame.from_dict(features, orient="index")
    df.index.name = "wallet_id"

    return df
