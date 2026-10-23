import math
import matplotlib.pyplot as plt
import networkx as nx

def visualize_search_tree(start, tree_edges, path=None, goal=None, options=None):
    path, path_set, p_edges = path or [], set(path or []), set(zip(path or [], path[1:] if path else []))
    
    # Build graph
    G = nx.DiGraph()
    if start: G.add_node(start)
    G.add_edges_from((p, c) for p, c in list(tree_edges or []) + list(options or []) 
                     if p in path_set and (c not in path_set or (p, c) in p_edges))

    # Layout calculation (variables removed, values hardcoded directly)
    pos = {start: (0.0, 0.0)} if start else {}
    stack = [(start, -90.0)] if start else []
    while stack:
        node, base = stack.pop()
        x, y = pos[node]
        kids = [c for c in G.successors(node) if c not in pos]
        if not kids: continue
        
        others = [c for c in kids if c not in path_set]
        ordered = others[:len(others)//2] + [c for c in kids if c in path_set] + others[len(others)//2:]
        n = len(ordered)
        step = min(30, 160 / (n - 1)) if n > 1 else 0

        for i, child in enumerate(ordered):
            ang = math.radians(base + (i - (n - 1) / 2) * step)
            pos[child] = (x + 3.0 * math.cos(ang), y + 3.0 * math.sin(ang))
            stack.append((child, -90.0 if child in path_set else math.degrees(ang)))

    # Plotting setup
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="#bce1f4")
    ax.set(facecolor="#f8f7f7", title="Search Tree | BFS", aspect='equal')
    ax.axis('off')

    # Draw nodes and edges
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#1f2123", width=1.2, arrows=False, alpha=0.5)
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G if n != start and n not in path_set and n != goal], ax=ax, node_size=60, node_color='#e2e8f0', edgecolors='#94a3b8', linewidths=1.2)
    
    if start in G: nx.draw_networkx_nodes(G, pos, nodelist=[start], ax=ax, node_size=60, node_color='#10b981', edgecolors='#047857', linewidths=1.2)
    if goal in G: nx.draw_networkx_nodes(G, pos, nodelist=[goal], ax=ax, node_size=60, node_color='#ef4444', edgecolors='#b91c1c', linewidths=1.2)
    
    p_nodes = list(path_set - {start, goal})
    if p_nodes: nx.draw_networkx_nodes(G, pos, nodelist=p_nodes, ax=ax, node_size=60, node_color='#F7F449', edgecolors='#212122', linewidths=1.2)
    
    nx.draw_networkx_edges(G, pos, edgelist=[e for e in p_edges if G.has_edge(*e)], ax=ax, edge_color="#F7F449", width=2.0, arrows=False)
    
    plt.tight_layout()
    plt.show(block=False)