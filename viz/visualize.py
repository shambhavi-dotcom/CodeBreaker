from pyvis.network import Network
import networkx as nx

def visualize_suspicious_subgraph(G, risk_scores):
    # 1️⃣ Pick the most suspicious wallet
    seed = max(risk_scores, key=risk_scores.get)

    # 2️⃣ Ego network (2 hops)
    ego = nx.ego_graph(G, seed, radius=2)

    # 3️⃣ Remove giant hubs
    MAX_DEGREE = 20
    ego = ego.copy()
    for node in list(ego.nodes()):
        if ego.degree(node) > MAX_DEGREE and node != seed:
            ego.remove_node(node)

    # 4️⃣ Visualization
    net = Network(height="750px", width="100%", directed=True)

    for node in ego.nodes():
        if node == seed:
            net.add_node(
                node,
                label=f"SUSPECT\n{node}",
                color="red",
                size=40
            )
        else:
            net.add_node(
                node,
                label="",          # 🔥 NO LABELS
                color="orange",
                size=15
            )

    for u, v in ego.edges():
        net.add_edge(u, v, color="red")

    # 5️⃣ Strong spacing, then freeze
    net.barnes_hut(
        gravity=-4000,
        central_gravity=0.05,
        spring_length=220,
        spring_strength=0.01,
        damping=0.9
    )

    net.show("suspicious_graph.html", notebook=False)
