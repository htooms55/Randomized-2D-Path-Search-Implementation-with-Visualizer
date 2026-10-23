from collections import deque

def get_neighbors(node, grid):
    r, c = node
    rows, cols = grid.shape
    neighbors = []
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
            neighbors.append((nr, nc))
            
    return neighbors

def bfs_search(grid, start, goal):
    if start == goal:
        return [start], [start], []
        
    queue = deque([[start]])
    visited = {start}
    visited_order = [start]
    tree_edges = []  
    
    while queue:
        current_path = queue.popleft()  
        current_node = current_path[-1]
        
        if current_node == goal:
            return current_path, visited_order, tree_edges
            
        for neighbor in get_neighbors(current_node, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                visited_order.append(neighbor)
                
                tree_edges.append((current_node, neighbor))
                
                new_path = list(current_path)
                new_path.append(neighbor)
                queue.append(new_path)  
                
    return None, visited_order, tree_edges