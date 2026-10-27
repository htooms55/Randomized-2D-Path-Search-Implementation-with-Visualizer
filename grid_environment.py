import random
import numpy as np

def create_grid(size, obstacle_ratio = 0.15, start=None, goal=None):
    #generate random numbers between 0.0 & 1.0 for the grid
    random_grid = np.random.rand(size, size) 
    #converting numbers > sparsity into 1 (obstacles) and < sparsity into 0 (free space)
    grid = (random_grid < obstacle_ratio).astype(int) 

    #creating random start and goal positions
    if start == None:
        start_row = random.randint(0,size-1)
        start_column = random.randint(0,size-1)
        start = (start_row,start_column)
    else: 
        start_row, start_column = start
    
    if goal == None:
        goal_row = random.randint(0,size-1)
        goal_column = random.randint(0,size-1)
        goal = (goal_row,goal_column)
    else: 
        goal_row, goal_column = goal

    #setting start and goal position to 0 to avoid obstacles
    grid[start_row,start_column] = 0
    grid[goal_row,goal_column] = 0

    return grid, start, goal
