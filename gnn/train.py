import torch
import torch.nn.functional as F
from gnn.model import WalletGNN

def train_gnn(data, labels, epochs=100):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = WalletGNN(data.x.shape[1]).to(device)
    data = data.to(device)
    labels = labels.to(device)

    # 🔥 CLASS IMBALANCE FIX
    pos_weight = (labels == 0).sum() / (labels == 1).sum()
    criterion = torch.nn.CrossEntropyLoss(
        weight=torch.tensor([1.0, pos_weight], device=device)
    )

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.003,        # 👈 safer for GNNs
        weight_decay=5e-4
    )

    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()

        out = model(data)
        loss = criterion(out, labels)

        loss.backward()
        optimizer.step()

        if epoch % 20 == 0:
            with torch.no_grad():
                probs = F.softmax(out, dim=1)[:, 1]
                print(
                    f"Epoch {epoch:03d} | "
                    f"Loss {loss.item():.4f} | "
                    f"GNN max {probs.max():.3f}"
                )

    # ✅ FINAL PROBABILITIES (ILLICIT CLASS)
    model.eval()
    with torch.no_grad():
        out = model(data)
        probs = F.softmax(out, dim=1)[:, 1]

    return probs.cpu().numpy()
