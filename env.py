import random

class GridWorld:
    def __init__(self, rows, cols, num_agents=3, num_obstacles=2):
        self.rows = rows
        self.cols = cols

        # Place goal
        self.goal = (random.randint(0, rows - 1), random.randint(0, cols - 1))

        # Place obstacles FIRST (ensure they neither overlap nor touch)
        self.obstacles = []
        def rects_touch_or_overlap(A, B):
            (ar1, ac1), (ar2, ac2) = A
            (br1, bc1), (br2, bc2) = B
            # normalize
            ar1, ar2 = min(ar1, ar2), max(ar1, ar2)
            ac1, ac2 = min(ac1, ac2), max(ac1, ac2)
            br1, br2 = min(br1, br2), max(br1, br2)
            bc1, bc2 = min(bc1, bc2), max(bc1, bc2)
            # expand B by 1 so that mere touching counts as overlap
            br1e = max(0, br1 - 1)
            br2e = min(self.rows - 1, br2 + 1)
            bc1e = max(0, bc1 - 1)
            bc2e = min(self.cols - 1, bc2 + 1)
            # if A intersects expanded B, they touch/overlap
            return not (ar2 < br1e or br2e < ar1 or ac2 < bc1e or bc2e < ac1)

        attempts = 0
        max_attempts = 5000
        while len(self.obstacles) < num_obstacles and attempts < max_attempts:
            attempts += 1
            r1, c1 = random.randint(0, rows - 2), random.randint(0, cols - 2)
            r2 = min(r1 + random.randint(1, 2), rows - 1)
            c2 = min(c1 + random.randint(1, 2), cols - 1)
            candidate = ((r1, c1), (r2, c2))
            if any(rects_touch_or_overlap(candidate, ob) for ob in self.obstacles):
                continue
            self.obstacles.append(candidate)

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
