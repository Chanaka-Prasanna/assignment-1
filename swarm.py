def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def apply_swarm_rules(agent_pos, action, agents, obstacles, goal, min_dist=1, rows=10, cols=10):
    """Modify RL-chosen action to respect swarm rules + boundaries"""
    new_pos = (agent_pos[0] + action[0], agent_pos[1] + action[1])

    # --- FIX 1: keep inside grid bounds ---
    nr, nc = new_pos
    if nr < 0: nr = 0
    if nr >= rows: nr = rows - 1
    if nc < 0: nc = 0
    if nc >= cols: nc = cols - 1
    new_pos = (nr, nc)

    # 2. Avoid obstacles
    for (r1, c1), (r2, c2) in obstacles:
        if r1 <= new_pos[0] <= r2 and c1 <= new_pos[1] <= c2:
            return agent_pos  # stay instead of disappearing

    # 3. Maintain minimum distance
    for other in agents:
        if other != agent_pos and manhattan(new_pos, other) <= min_dist:
            return agent_pos

    return new_pos
