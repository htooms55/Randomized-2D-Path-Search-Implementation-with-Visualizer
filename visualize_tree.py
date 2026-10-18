import math
import matplotlib.pyplot as plt
import networkx as nx

# --- Layout tuning (edit these) ---
EDGE_LEN = 3.0        # every edge will have exactly this length
ANGLE_STEP = 30       # degrees between sibling branches
MAX_SPREAD = 160      # max total fan angle (keeps branches from going sideways/upward)


def _layout_equal_edges(G, start, path, edge_len=EDGE_LEN,
                        angle_step=ANGLE_STEP, max_spread=MAX_SPREAD):
    """
    Parent-relative layout: each child is placed exactly `edge_len` from its
    parent, so all edges have identical length. The winning path goes straight
    down (aligned in one column); alternative branches fan out around it.
    """
    path_set = set(path or [])
    pos = {start: (0.0, 0.0)}
    stack = [(start, -90.0)]  # (node, base direction in degrees; -90 = straight down)

    while stack:
        node, base = stack.pop()
        x, y = pos[node]
        kids = [c for c in G.successors(node) if c not in pos]

        # Winning-path child goes in the middle so branches fan out evenly around it
        others = [c for c in kids if c not in path_set]
        mid = len(others) // 2
        ordered = others[:mid] + [c for c in kids if c in path_set] + others[mid:]

        n = len(ordered)
        step = min(angle_step, max_spread / (n - 1)) if n > 1 else 0

        for i, child in enumerate(ordered):
            ang_deg = base + (i - (n - 1) / 2) * step
            ang = math.radians(ang_deg)
            pos[child] = (x + edge_len * math.cos(ang),
                          y + edge_len * math.sin(ang))
            # Path nodes always continue straight down; other nodes keep their own direction
            stack.append((child, -90.0 if child in path_set else ang_deg))

    return pos


def visualize_search_tree(start, tree_edges, path=None, goal=None, options=None):  # CHANGED: added options
    """
    Renders the winning path (spine) and all alternative child routes/branches 
    that diverge directly from each node along the winning path.
    """
    path = path or []
    path_set = set(path)

    # 1. Graph = every edge whose parent is on the winning path
    #    (the path itself plus all alternative children, but no grandchildren)
    G = nx.DiGraph()
    if start:
        G.add_node(start)
    # CHANGED: also include `options` (every neighbor perceived), and skip edges that
    # lead back onto the path except the real next step
    path_edge_set = set(zip(path, path[1:]))
    G.add_edges_from((p, c) for p, c in list(tree_edges or []) + list(options or [])
                     if p in path_set and (c not in path_set or (p, c) in path_edge_set))

    # 2. Coordinates with constant edge length
    pos = _layout_equal_edges(G, start, path) if start in G else {n: (0.0, 0.0) for n in G}

    # 3. Window for tree graph
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor("#bce1f4")
    ax.set_facecolor("#f8f7f7")
    ax.set_title("Search Tree | BFS", fontsize=12, fontweight='bold', color="#121313", pad=15)
    ax.axis('off')
    ax.set_aspect('equal')  # keeps equal data lengths looking equal on screen

    def draw_nodes(nodes, fill, edge):
        nx.draw_networkx_nodes(G, pos, nodelist=list(nodes), ax=ax, node_size=60,
                               node_color=fill, edgecolors=edge, linewidths=1.2)

    # Alternative branch edges (muted background) and nodes
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#1f2123", width=1.2, arrows=False, alpha=0.5)
    draw_nodes([n for n in G if n != start and n not in path_set and n != goal], '#e2e8f0', '#94a3b8')

    # Start node (level 0) and goal node (if discovered in the tree)
    draw_nodes([start] if start in G else [], '#10b981', '#047857')
    draw_nodes([goal] if goal in G else [], '#ef4444', '#b91c1c')

    # Final winning path on top of the tree view
    path_edges = [e for e in zip(path, path[1:]) if G.has_edge(*e)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=ax, edge_color="#F7F449", width=2.0, arrows=False)
    draw_nodes(path_set - {start, goal}, '#F7F449', '#212122')

    plt.tight_layout()
    plt.show(block=False)