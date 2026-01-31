import torch
import torch.nn.functional as F
from gnn.model import WalletGNN

def train_gnn(data, labels):
    model = WalletGNN(data.x.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(50):
        optimizer.zero_grad()
        out = model(data)
        loss = F.cross_entropy(out, labels)
        loss.backward()
        optimizer.step()

    # 🔥 THIS IS IMPORTANT
    probs = F.softmax(out, dim=1)[:, 1].detach().numpy()
    return probs
