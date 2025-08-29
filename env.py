import random

class GridWorld:
    def __init__(self, rows, cols, num_agents=3, num_obstacles=2):
        self.rows = rows
        self.cols = cols

        # Place goal
        self.goal = (random.randint(0, rows - 1), random.randint(0, cols - 1))

        # Place agents
        self.agents = []
        for _ in range(num_agents):
            pos = self._random_cell_away_from_goal()
            self.agents.append(pos)

        # Place obstacles
        self.obstacles = []
        for _ in range(num_obstacles):
            r1, c1 = random.randint(0, rows - 2), random.randint(0, cols - 2)
            r2, c2 = min(r1 + random.randint(1, 2), rows - 1), min(c1 + random.randint(1, 2), cols - 1)
            self.obstacles.append(((r1, c1), (r2, c2)))

    def _random_cell_away_from_goal(self):
        """Pick a cell at least distance 2 away from goal and unique from agents"""
        while True:
            r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (r, c) != self.goal and abs(r - self.goal[0]) + abs(c - self.goal[1]) > 2 and (r, c) not in self.agents:
                return (r, c)

    def reset(self):
        """Respawn agents at new random locations"""
        self.agents = [self._random_cell_away_from_goal() for _ in self.agents]
        return self.agents
