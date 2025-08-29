import random
import numpy as np

ACTIONS = [(1,0), (-1,0), (0,1), (0,-1), (0,0)]  # down, up, right, left, stay
ALPHA = 0.5
GAMMA = 0.9
EPSILON = 0.2

class QLearningAgent:
    def __init__(self, rows, cols):
        self.q_table = {}
        self.rows = rows
        self.cols = cols

    def get_state(self, pos, goal):
        """State = (agent_row, agent_col, goal_row, goal_col)"""
        return (pos[0], pos[1], goal[0], goal[1])

    def choose_action(self, state):
        if random.random() < EPSILON:   # explore
            return random.choice(ACTIONS)
        else:                           # exploit
            q_values = [self.q_table.get((state, a), 0) for a in ACTIONS]
            return ACTIONS[int(np.argmax(q_values))]

    def update(self, state, action, reward, next_state):
        old_q = self.q_table.get((state, action), 0)
        future_q = max([self.q_table.get((next_state, a), 0) for a in ACTIONS])
        new_q = old_q + ALPHA * (reward + GAMMA * future_q - old_q)
        self.q_table[(state, action)] = new_q
