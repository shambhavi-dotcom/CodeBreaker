import torch
from torch_geometric.data import Data
from sklearn.preprocessing import StandardScaler
import numpy as np

def build_pyg_data(G, features_df, labels):
    """
    Builds PyG Data object with:
    - normalized node features
    - correct edge index
    - attached labels
    """

    # -------------------------
    # Node indexing
    # -------------------------
    node_to_idx = {node: i for i, node in enumerate(G.nodes())}

    # -------------------------
    # Edge index
    # -------------------------
    edges = [(node_to_idx[u], node_to_idx[v]) for u, v in G.edges()]
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()

    # -------------------------
    # Normalize node features
    # -------------------------
    scaler = StandardScaler()
    x_np = scaler.fit_transform(features_df.values)

    x = torch.tensor(x_np, dtype=torch.float)

    # -------------------------
    # Labels
    # -------------------------
    y = torch.tensor(labels, dtype=torch.float)

    return Data(x=x, edge_index=edge_index, y=y)
