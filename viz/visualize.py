from pyvis.network import Network
import networkx as nx

def visualize_suspicious_subgraph(G, risk_scores):
    seed = max(risk_scores, key=risk_scores.get)
    ego = nx.ego_graph(G, seed, radius=2)

    net = Network(
        height="800px",
        width="100%",
        directed=True,
        bgcolor="#0b1220",
        font_color="white"
    )

    net.toggle_physics(True)

    degrees = dict(ego.degree())

    # --- Add nodes ---
    for node in ego.nodes():
        risk = risk_scores.get(node, 0)
        deg = degrees[node]

        # classify
        if node == seed:
            group = "suspect"
            color = "#ef4444"
            size = 45
            label = "SUSPECT"
        elif "exchange" in node:
            group = "exchange"
            color = "#fb923c"
            size = 25 + deg
            label = ""
        elif "mixer" in node:
            group = "mixer"
            color = "#a855f7"
            size = 22 + deg
            label = ""
        else:
            group = "wallet"
            color = "#22c55e" if risk < 0.4 else "#eab308"
            size = 10 + deg
            label = ""

        net.add_node(
            node,
            label=label,
            group=group,
            color=color,
            size=size,
            title=f"""
            Wallet: {node}<br>
            Risk: {risk:.2f}<br>
            Degree: {deg}<br>
            """
        )

    # --- Add edges ---
    for u, v in ego.edges():
        net.add_edge(
            u, v,
            arrows="to",
            color="rgba(239,68,68,0.6)",
            physics=True
        )

    # --- CLUSTERING ---
    net.set_options("""
    {
      "nodes": {
        "borderWidth": 0,
        "shadow": true,
        "font": {
          "size": 14,
          "face": "monospace"
        }
      },
      "edges": {
        "smooth": {
          "enabled": true,
          "type": "dynamic"
        }
      },
      "interaction": {
        "hover": true,
        "zoomView": true,
        "dragView": true,
        "navigationButtons": true,
        "tooltipDelay": 50
      },
      "physics": {
        "enabled": true,
        "solver": "forceAtlas2Based",
        "forceAtlas2Based": {
          "gravitationalConstant": -80,
          "centralGravity": 0.01,
          "springLength": 120,
          "springConstant": 0.02,
          "damping": 0.4,
          "avoidOverlap": 1
        },
        "stabilization": {
          "enabled": true,
          "iterations": 500,
          "fit": true
        }
      }
    }
    """)

    net.show("frontend/graph.html", notebook=False)
