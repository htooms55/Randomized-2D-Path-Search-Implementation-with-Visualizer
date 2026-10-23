import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines  
import numpy as np

def visualize_grid(grid, start=None, goal=None, path=None, visited_order=None):
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="#86cdf4")
    ax.set_facecolor("#f8f7f7")
    ax.imshow(grid, cmap='binary', origin='upper', aspect='equal')
    
    # Grid lines & ticks
    size = grid.shape[0]
    ax.set_xticks(np.arange(-0.5, size, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, size, 1), minor=True)
    ax.grid(which="minor", color="#6d737a", linewidth=0.9)
    ax.tick_params(which="minor", size=0)
    ax.set_xticks([]); ax.set_yticks([])
    
    # Spines
    for spine in ax.spines.values():
        spine.set(visible=True, color='#1e293b', linewidth=1.8)
    
    # Start & Goal markers
    if start:
        ax.add_patch(patches.Circle((start[1], start[0]), 0.3, color="#10b981", zorder=4))
    if goal:
        ax.add_patch(patches.Circle((goal[1], goal[0]), 0.3, color="#ef4444", zorder=4))
        
    # Legend setup
    handles = [
        mlines.Line2D([], [], color='w', marker='o', markerfacecolor='#10b981', markersize=10, label='Start'),
        mlines.Line2D([], [], color='w', marker='o', markerfacecolor='#ef4444', markersize=10, label='Goal')
    ]
    if visited_order: 
        handles.append(mlines.Line2D([], [], color='w', marker='o', markerfacecolor='#cbd5e1', markersize=8, label='Visited'))
    if path: 
        handles.append(mlines.Line2D([], [], color='#4e8eef', linewidth=3.5, label='Path'))

    ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, -0.08), 
              ncol=4, framealpha=0.8, facecolor='#ffffff', edgecolor="#7e99bb")
    ax.set_title("2D Environment", fontsize=15, fontweight='bold', color='#1e293b', pad=15)

    plt.ion()
    plt.show(block=False)

    # Animate Visited Nodes
    if visited_order:
        filtered = [n for n in visited_order if n != start and n != goal]
        if filtered:
            v_rows, v_cols = zip(*filtered)
            v_plot = ax.scatter([], [], color='#cbd5e1', s=50, zorder=2)
            for i in range(len(filtered)):
                v_plot.set_offsets(np.c_[v_cols[:i+1], v_rows[:i+1]])
                plt.draw(); plt.pause(0.005)
            
    # Animate Path
    if path:
        p_rows, p_cols = zip(*path)
        path_line, = ax.plot([], [], color="#4e8eef", linewidth=3.5, alpha=0.85, zorder=3)
        for i in range(len(path)):
            path_line.set_data(p_cols[:i+1], p_rows[:i+1])
            plt.draw(); plt.pause(0.02)

    plt.tight_layout()
    plt.ioff()
    plt.show(block=False)