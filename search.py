from collections import deque
def bfs_search(grid, start, goal):
    # Initialize queue with starting node
    queue = deque([start]) 
    # stores node:parent node
    visited = {start: None} 
    visited_order = [] # to store the order of visited nodes

    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    while queue:
        current = queue.popleft()
        visited_order.append(current)
        if current == goal:
            # reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = visited[current] #current points to the value of visited's key, where key is current --> key : value

            return path[::-1], visited_order, visited 
        for row_direction, col_direction in directions:
            row = current[0] + row_direction
            col = current[1] + col_direction
            # checks if node is within bounds, not an obstacle, and not visited
            if (0 <= row < len(grid)) and (0 <= col < len(grid[0])) and grid[row][col] == 0 and (row, col) not in visited:
                visited[(row, col)] = current #adding to the dictionary visited node : parent node (came from)
                queue.append((row, col)) # add the neighbour node to the queue
    return None, visited_order, visited