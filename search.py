from collections import deque

def get_neighbors(node, grid):
    """Returns valid 4-cardinal neighbors that are not obstacles."""
    r, c = node
    rows, cols = grid.shape
    neighbors = []
    
    # North, South, East, West
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        # Check boundaries and ensure it's not an obstacle (0 is path, 1 is obstacle typically)
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
            neighbors.append((nr, nc))
            
    return neighbors

def bfs_search(grid, start, goal):
    """
    Performs Breadth-First Search (BFS) using a Queue (FIFO).
    Returns path, visited order, and tree edges (parent-child connections).
    """
    if start == goal:
        return [start], [start], []
        
    # Use a queue instead of a stack for FIFO (First-In, First-Out) behavior
    queue = deque([[start]])
    visited = {start}
    visited_order = [start]
    tree_edges = []  # Track parent -> child links for tree visualization
    
    while queue:
        current_path = queue.popleft()  # Pop from the left for BFS
        current_node = current_path[-1]
        
        if current_node == goal:
            return current_path, visited_order, tree_edges
            
        for neighbor in get_neighbors(current_node, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                visited_order.append(neighbor)
                
                # Record the tree edge expansion
                tree_edges.append((current_node, neighbor))
                
                new_path = list(current_path)
                new_path.append(neighbor)
                queue.append(new_path)  # Append to the right for BFS
                
    return None, visited_order, tree_edges