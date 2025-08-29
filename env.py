import random

class GridWorld:
    def __init__(self, rows, cols, num_agents=3, num_obstacles=2):
        self.rows = rows
        self.cols = cols

        # Place goal
        self.goal = (random.randint(0, rows - 1), random.randint(0, cols - 1))

        # Place obstacles FIRST
        self.obstacles = []
        for _ in range(num_obstacles):
            r1, c1 = random.randint(0, rows - 2), random.randint(0, cols - 2)
            r2, c2 = min(r1 + random.randint(1, 2), rows - 1), min(c1 + random.randint(1, 2), cols - 1)
            self.obstacles.append(((r1, c1), (r2, c2)))

        # Initialize empty list before placing agents
        self.num_agents = num_agents
        self.agents = []
        for _ in range(num_agents):
            pos = self._random_free_cell()
            self.agents.append(pos)

    def _random_free_cell(self):
        """Pick random cell not goal, not inside obstacle, not already used"""
        while True:
            r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (r, c) == self.goal:
                continue
            if any(r1 <= r <= r2 and c1 <= c <= c2 for (r1, c1), (r2, c2) in self.obstacles):
                continue
            if (r, c) in self.agents:
                continue
            return (r, c)

    def reset(self):
        """Respawn agents in new valid cells (goal and obstacles stay the same)."""
        self.agents = []
        for _ in range(self.num_agents):
            self.agents.append(self._random_free_cell())
        return self.agents
