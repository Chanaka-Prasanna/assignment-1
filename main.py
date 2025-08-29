from env import GridWorld
from rl import QLearningAgent
from swarm import apply_swarm_rules
from visualize import visualize

NUM_AGENTS = 3
NUM_OBSTACLES = 2
GRID_SIZE = (10, 10)
EPISODES = 1       # for visualization, run 1 episode
MAX_STEPS = 200

def reward_function(agent_pos, goal_pos, obstacles):
    if agent_pos == goal_pos:
        return 10
    if any(r1 <= agent_pos[0] <= r2 and c1 <= agent_pos[1] <= c2 for (r1, c1), (r2, c2) in obstacles):
        return -5
    return -1
def run_simulation():
    env = GridWorld(GRID_SIZE[0], GRID_SIZE[1], NUM_AGENTS, NUM_OBSTACLES)
    agents = [QLearningAgent(env.rows, env.cols) for _ in range(NUM_AGENTS)]

    all_history = []  # track across episodes

    for episode in range(EPISODES):
        positions = env.reset()
        agents_history = []

        for step in range(MAX_STEPS):
            new_positions = []
            for i, pos in enumerate(positions):
                if pos == env.goal:
                    new_positions.append(pos)
                    continue

                state = agents[i].get_state(pos, env.goal)
                action = agents[i].choose_action(state)

                next_pos = apply_swarm_rules(
                    pos, action, positions, env.obstacles, env.goal,
                    rows=env.rows, cols=env.cols
                )

                reward = reward_function(next_pos, env.goal, env.obstacles)
                next_state = agents[i].get_state(next_pos, env.goal)
                agents[i].update(state, action, reward, next_state)

                new_positions.append(next_pos)

            positions = new_positions
            agents_history.append((episode+1, positions))  # include episode number

            if all(p == env.goal for p in positions):
                print(f"✅ Episode {episode+1}: all agents reached the goal in {step+1} steps")
                break

        # add episode history to global
        all_history.extend(agents_history)
        # add a pause (3 frames with same positions)
        all_history.extend([(episode+1, positions)] * 3)

    # Visualize all episodes
    visualize(env, all_history)

if __name__ == "__main__":
    run_simulation()
