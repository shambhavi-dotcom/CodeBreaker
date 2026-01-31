import torch
from torch_geometric.data import Data
import networkx as nx

def build_pyg_data(G, features_df):
    # Map wallet_id → integer index
    node_to_idx = {node: i for i, node in enumerate(G.nodes())}

    # Edge index
    edges = [(node_to_idx[u], node_to_idx[v]) for u, v in G.edges()]
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()

    # Node features
    x = torch.tensor(features_df.values, dtype=torch.float)

    return Data(x=x, edge_index=edge_index)
