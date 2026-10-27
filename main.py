import random
from grid_environment import create_grid
from visualize_maze import draw_grid
from search import bfs_search

print("\nWelcome to Randomized 2D Path Search")

# choose grid size
while True:
    size_input = input("\nEnter grid size (5 - 15) [Press Enter for 15]: ").strip()
    if size_input == "":
        size = 15
        break
    if size_input.isdigit() and 5 <= int(size_input) <= 15:
        size = int(size_input)
        break
    print("Please enter a whole number between 5 and 20.")

# obstacle ratio
while True:
    print("\nChoose Obstacle Ratio")
    print("1. Random Obstacle Ratio (15% - 30%)")
    print("2. Custom Obstacle Ratio (15% - 30%)")
    print("Press Enter for Default Obstacle Ratio (15%)")
    choice = input("\nEnter your choice: ").strip()

    if choice == "":
        obstacle_ratio = 0.15
        break
    elif choice == "1":
        obstacle_ratio = random.randint(15, 30) / 100
        break
    elif choice == "2":
        ratio_input = input("Enter obstacle ratio (15 - 30): ").strip()
        if ratio_input.isdigit() and 15 <= int(ratio_input) <= 30:
            obstacle_ratio = int(ratio_input) / 100
            break
        print("Invalid input. Please enter a number between 15 and 30.")
    else:
        print("Please enter 1, 2, or press Enter for default.")

# start and goal positions
while True:
    print("\nChoose Start & Goal Positions")
    print("1. Random Start & Goal")
    print("2. Custom Start & Goal")
    print(f"Press Enter for Default Start & Goal (0,0) to ({size},{size})")
    choice = input("\nEnter your choice: ").strip()

    if choice == "":
        start, goal = (0, 0), (size - 1, size - 1)
        break
    elif choice == "1": #generate_grid will choose random start & goal if None
        start, goal = None, None
        break
    elif choice == "2":
        try:
            custom_start_row = input(f"Enter start position row: ").strip()
            custom_start_col = input(f"Enter start position column: ").strip()
            custom_goal_row = input(f"Enter goal position row: ").strip()
            custom_goal_col = input(f"Enter goal position column: ").strip()
            start = (int(custom_start_row), int(custom_start_col))
            goal = (int(custom_goal_row), int(custom_goal_col))
            
            #check if coordinates are within bounds
            if 0 <= start[0] < size and 0 <= start[1] < size and 0 <= goal[0] < size and 0 <= goal[1] < size:
                break
            print(f"Coordinates must be within 0 and {size - 1}.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter whole numbers for row and column.")
    else:
        print("Please enter 1, 2, or press Enter for default.")

#create grid
grid, start, goal = create_grid(size, obstacle_ratio, start, goal)

draw_grid(grid, start, goal)

