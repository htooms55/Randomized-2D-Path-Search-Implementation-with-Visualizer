import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines  # <-- Import for custom legend handles
import numpy as np

def visualize_grid(grid, start=None, goal=None, path=None, visited_order=None):
    """Takes data from the environment and renders it with styled titles and circular legend icons."""
    
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor("#86cdf4")
    ax.set_facecolor("#f8f7f7")
    
    # Draw the grid walls and open spaces
    ax.imshow(grid, cmap='binary', origin='upper')
    
    # Lock Aspect Ratio So Cells Stay Square
    ax.set_aspect('equal')
    
    # Add Faint Grid Lines
    size = grid.shape[0]
    ax.set_xticks(np.arange(-0.5, size, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, size, 1), minor=True)
    ax.grid(which="minor", color="#6d737a", linestyle="-", linewidth=0.9)
    ax.tick_params(which="minor", size=0)
    
    # Bold Perimeter Border Around the Grid Canvas
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('#1e293b')
        spine.set_linewidth(1.8)
    
    # Precise Data-Coordinate Circles
    if start:
        start_circle = patches.Circle((start[1], start[0]), radius=0.30, color="#10b981", zorder=4)
        ax.add_patch(start_circle)
        
    if goal:
        goal_circle = patches.Circle((goal[1], goal[0]), radius=0.30, color="#ef4444", zorder=4)
        ax.add_patch(goal_circle)
        
    # Clear major ticks
    ax.set_xticks([])
    ax.set_yticks([])
    
    # --- Custom Circular Legend Handles ---
    legend_handles = [
        mlines.Line2D([], [], color='w', marker='o', markerfacecolor='#10b981', markersize=10, label='Start'),
        mlines.Line2D([], [], color='w', marker='o', markerfacecolor='#ef4444', markersize=10, label='Goal')
    ]

    if visited_order:
        legend_handles.append(mlines.Line2D([], [], color='w', marker='o', markerfacecolor='#cbd5e1', markersize=8, label='Visited'))
    if path:
        legend_handles.append(mlines.Line2D([], [], color='#4e8eef', linewidth=3.5, label='Path'))

    # --- Start Interactive Mode for Live Animation ---
    plt.ion()
    plt.show(block=False)

    # --- Animate Visited Nodes (Search Expansion) ---
    if visited_order:
        visited_rows = []
        visited_cols = []
        visited_plot = ax.scatter([], [], color='#cbd5e1', s=50, zorder=2)
        
        for node in visited_order:
            if node == start or node == goal:
                continue
            visited_rows.append(node[0])
            visited_cols.append(node[1])
            visited_plot.set_offsets(np.c_[visited_cols, visited_rows])
            plt.draw()
            plt.pause(0.005)  # Adjust speed here (smaller = faster)

    # --- Animate the Final Path ---
    if path:
        path_rows = [node[0] for node in path]
        path_cols = [node[1] for node in path]
        
        path_line, = ax.plot([], [], color="#4e8eef", linewidth=3.5, alpha=0.85, zorder=3)
        
        for i in range(len(path)):
            path_line.set_data(path_cols[:i+1], path_rows[:i+1])
            plt.draw()
            plt.pause(0.02)  # Adjust speed for path drawing here

    # --- Legend ---
    ax.legend(
        handles=legend_handles,
        loc='upper center', 
        bbox_to_anchor=(0.5, -0.08), 
        ncol=4, 
        framealpha=0.8,
        facecolor='#ffffff',
        edgecolor="#7e99bb"
    )
    
    # --- Title ---
    plt.title(
        "2D Environment", 
        fontsize=15, 
        fontweight='bold', 
        fontfamily='sans-serif', 
        style='normal',  
        color='#1e293b', 
        pad=15
    )
    
    plt.tight_layout()
    
    # --- Turn off interactive mode and keep window open ---
    plt.ioff()
    plt.show(block=False)