import random
import numpy as np

class GridEnvironment:
    def __init__(self, grid_size=15, obstacle_ratio=0.15, start=None, goal=None):
        self.size = grid_size
        self.obstacle_ratio = obstacle_ratio

        #using numpy to create a grid
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.start = None
        self.goal = None
        # Run setup helpers
        self.place_obstacles()
        self.place_start_and_goal(start, goal)

    #method for placing obstacles within the grid/maze, sets a random position as "1" to indicate an obstacle
    def place_obstacles(self):
        target_obstacles = int(self.size*self.size*self.obstacle_ratio)
        placed = 0
        while placed < target_obstacles:
            random_row = random.randint(0, self.size-1)
            random_column = random.randint(0, self.size-1)
            if self.grid[random_row][random_column] == 0:
                self.grid[random_row][random_column] = 1
                placed += 1

    #Get a random row and random index within that row, that position must equal 0 to satisfy
    # a fair starting point and not intrude an occupying obstacle space

    def place_start_and_goal(self, start=None, goal=None):
        #setting starting point (user-chosen, or random)
        if start:
            self.grid[start] = 0
            self.start = start
        else:
            while True:
                random_row = random.randint(0, self.size-1)
                random_column = random.randint(0, self.size-1)
                if self.grid[random_row][random_column] == 0 and (random_row, random_column) != goal:
                    self.start = (random_row, random_column)
                    break
        #setting goal point (user-chosen, or random)
        if goal:
            self.grid[goal] = 0
            self.goal = goal
        else:
            while True:
                random_row = random.randint(0, self.size-1)
                random_column = random.randint(0, self.size-1)
                if self.grid[random_row][random_column] == 0 and (random_row, random_column) != self.start:
                    self.goal = (random_row, random_column)
                    break
                