import torch
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv
from torch.nn import Linear

class LaunderingGNN(torch.nn.Module):
    def __init__(self, num_features):
        super().__init__()
        self.conv1 = SAGEConv(num_features, 64)
        self.conv2 = SAGEConv(64, 32)
        self.lin = Linear(32, 2)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        return self.lin(x)
