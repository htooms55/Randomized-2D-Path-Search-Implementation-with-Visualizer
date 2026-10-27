import matplotlib.pyplot as plt 
from search import bfs_search
import numpy as np

def draw_grid(grid, start, goal):
    path, visited_order, visited = bfs_search(grid,start,goal)
    
    fig, (ax_maze, ax_tree) = plt.subplots(1,2, figsize = (15,7))
    rows, cols = grid.shape
    
    #MAZE SETUP
    ax_maze.imshow(grid, cmap='binary') 
    ax_maze.set_title("2D Environment")

    #Grid lines for x-axis and y-axis
    ax_maze.set_xticks(np.arange(-0.5, cols+0.5, 1), minor=True)
    ax_maze.set_yticks(np.arange(-0.5, rows+0.5, 1), minor=True)
    ax_maze.grid(which='minor', color='gray', linestyle='-', linewidth=0.8)
    ax_maze.tick_params(which='minor', size=0)

    #start and goal positions
    ax_maze.scatter(start[1], start[0], color='green', marker='s', s=200) 
    ax_maze.scatter(goal[1], goal[0], color='red', marker='s', s=200)

    #TREE GRAPH SETUP
    ax_tree.set_title("Search Tree", fontsize=14)
    ax_tree.axis('off')
    depth = {start: 0}
    level_counts = {}
    tree_pos = {start: (0, 0)}  # Root at top center (0, 0)
    ax_tree.scatter(0, 0, color='green', marker='o', s=120, zorder=5)   

    # visited node exploration
    for node in visited_order:
        parent = visited[node]
        
        # Maze: grey square
        if node != start and node != goal:
            ax_maze.scatter(node[1], node[0], color='grey', marker='s', s=200)
            
        # Tree: grey branch from parent -> node
        if parent is not None:
            d = depth[parent] + 1
            depth[node] = d
            
            slot = level_counts.get(d, 0)
            level_counts[d] = slot + 1
            
            tree_pos[node] = (slot, -d)
            
            px, py = tree_pos[parent]
            cx, cy = tree_pos[node]
            ax_tree.plot([px, cx], [py, cy], color='gray', linewidth=1)             
            ax_tree.scatter(cx, cy, color='red' if node == goal else 'gray', s=30)
            ax_tree.relim()
            ax_tree.autoscale_view()
            
        plt.pause(0.001)
    # final path 
    if path:
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            if v != goal:
                ax_maze.scatter(v[1], v[0], color='yellow', marker='s', s=200)
    
            ux,uy = tree_pos[u]
            vx,vy = tree_pos[v]
            ax_tree.plot([ux, vx], [uy, vy], color='yellow', linewidth=3)            
            plt.pause(0.002)
    else:
        print("Path is blocked")
    plt.tight_layout() 
    plt.show()

    """ #code before utilizing the yield function 
    #exploration for visited nodes
    if visited_order:
        for node in visited_order:
            if node != start and node != goal:
                ax_maze.scatter(node[1], node[0], color = 'grey', marker='s', s=200)
            plt.pause(0.001)  
        plt.pause(0.005) 
    #final path
    for node in path:
        if node != start and node != goal:
            ax_maze.scatter(node[1], node[0], color='yellow', marker='s', s=200)
            plt.pause(0.008)
    """

