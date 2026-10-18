import matplotlib.pyplot as plt
from grid_environment import GridEnvironment
from search import bfs_search
from visualize_maze import visualize_grid
from visualize_tree import visualize_search_tree

def get_number(prompt, default, low, high, cast):
    #Asks until the user enters a valid number Enter keeps the default.
    while True:
        raw = input(f"{prompt} [default {default}]: ").strip()
        if raw == "":
            return default
        try:
            value = cast(raw)
            if low <= value <= high:
                return value
            print(f"  Please enter a value between {low} and {high}.")
        except ValueError:
            print("  Invalid input, please enter a number.")

def choose_location(name, size):
    #choose location function 
    print(f"\n{name} location:")
    print("  1. Random")
    print("  2. Custom")
    choice = get_number("Choose an option", 1, 1, 2, int)
    if choice == 1:
        return None
    row = get_number(f"  {name} row (0-{size-1}, 0 = top)", 0, 0, size - 1, int)
    col = get_number(f"  {name} column (0-{size-1}, 0 = left)", 0, 0, size - 1, int)
    return (row, col)

def main():
    print("Welcome to the BFS Maze Search Visualizer")
    print("-" * 40)
    # 1. Get user input, then generate environment
    size = get_number("Select grid size N (N x N)", 15, 3, 50, int)
    percent = get_number("Obstacle percentage (0-90)", 15, 0, 90, float)
    start_in = choose_location("Start", size)
    goal_in = choose_location("Goal", size)
    if start_in and start_in == goal_in:
        print("Start and goal can't be the same cell, so the goal will be random.")
        goal_in = None
    env = GridEnvironment(grid_size=size, obstacle_ratio=percent / 100, start=start_in, goal=goal_in)
    grid, start, goal = env.grid, env.start, env.goal
    # 2. Run search
    path, visited_order, tree_edges = bfs_search(grid, start, goal)

    # 3. Render Window 1: 2D Maze (Non-blocking)
    visualize_grid(grid, start, goal, path=path, visited_order=visited_order)
    # 4. Render Window 2: Search Tree Graph
    visualize_search_tree(start, tree_edges, path=path, goal=goal)
    # 5. Keep both windows open concurrently
    plt.show()

if __name__ == "__main__":
    main()