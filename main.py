import random

# Grid parameters
GRID_SIZE = (10, 10)   # rows x cols
NUM_AGENTS = 3
NUM_OBSTACLES = 2

# Symbols for console display
EMPTY = "."
AGENT = "A"
GOAL = "G"
OBSTACLE = "#"

class GridWorld:
    def __init__(self, rows, cols, num_agents, num_obstacles):
        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]

        # Place goal
        self.goal = (random.randint(0, rows - 1), random.randint(0, cols - 1))
        self.grid[self.goal[0]][self.goal[1]] = GOAL

        # Place agents
        self.agents = []
        for _ in range(num_agents):
            pos = self._random_empty_cell()
            self.agents.append(pos)
            self.grid[pos[0]][pos[1]] = AGENT

        # Place obstacles (rectangular)
        self.obstacles = []
        for _ in range(num_obstacles):
            r1, c1 = self._random_empty_cell()
            r2, c2 = min(r1 + random.randint(1, 2), rows - 1), min(c1 + random.randint(1, 2), cols - 1)
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    if self.grid[r][c] == EMPTY:
                        self.grid[r][c] = OBSTACLE
            self.obstacles.append(((r1, c1), (r2, c2)))

    def _random_empty_cell(self):
        while True:
            r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if self.grid[r][c] == EMPTY:
                return (r, c)

    def display(self):
        for row in self.grid:
            print(" ".join(row))
        print()

if __name__ == "__main__":
    env = GridWorld(GRID_SIZE[0], GRID_SIZE[1], NUM_AGENTS, NUM_OBSTACLES)
    env.display()
    print("Agents:", env.agents)
    print("Goal:", env.goal)
    print("Obstacles:", env.obstacles)