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
            risk=risk,
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

    # Generate the HTML file
    net.show("frontend/graph.html", notebook=False)

    # ==========================================
    # NEW: Inject Client-Side Filtering Script
    # ==========================================
    
    js_filtering_script = """
    <script type="text/javascript">
        (function() {
            // This function runs after the graph is initialized.
            // It looks at the URL parameter 'risk' and filters nodes.
            window.addEventListener('load', function() {
                const params = new URLSearchParams(window.location.search);
                const riskFilter = params.get('risk');

                // If a filter is specified and it's not 'all'
                if (riskFilter && riskFilter !== 'all') {
                    
                    // Access the global 'nodes' dataset created by Pyvis
                    // 'allNodes' is also a global object containing the full data
                    const nodesArray = Object.values(allNodes);
                    const idsToRemove = [];

                    nodesArray.forEach(node => {
                        const risk = node.risk;
                        let shouldRemove = true;

                        // Logic matching main_demo.py thresholds
                        if (riskFilter === 'high' && risk >= 0.66) {
                            shouldRemove = false;
                        } else if (riskFilter === 'medium' && risk >= 0.33 && risk < 0.66) {
                            shouldRemove = false;
                        } else if (riskFilter === 'low' && risk < 0.33) {
                            shouldRemove = false;
                        }

                        if (shouldRemove) {
                            idsToRemove.push(node.id);
                        }
                    });

                    // Perform the removal on the vis.js dataset
                    if (idsToRemove.length > 0) {
                        nodes.remove(idsToRemove);
                    }
                }
            });
        })();
    </script>
    """

    # Append the script to the generated HTML file
    with open("frontend/graph.html", "a") as f:
        f.write(js_filtering_script)
        
    print("Generated frontend/graph.html with filtering enabled.")