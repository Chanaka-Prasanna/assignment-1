## Assignment 1 – Swarm Path Planning

Multi‑agent swarm navigation in a gridworld using tabular Q‑Learning and simple swarm coordination rules, visualized with Matplotlib.

GitHub repository: https://github.com/Chanaka-Prasanna/assignment-1

## Table of Contents

- [Project Description](#project-description)
- [Features Implemented](#features-implemented)
- [How to Install and Run](#how-to-install-and-run)
- [How to Use](#how-to-use)
- [Swarm Coordination Logic](#swarm-coordination-logic)
- [RL Update Rule](#rl-update-rule)
- [Evaluation Criteria Mapping](#evaluation-criteria-mapping)
- [Project Structure](#project-structure)

## Project Description

This project simulates a swarm of agents navigating a 2D grid with rectangular obstacles toward a single goal. Each agent learns online via tabular Q‑Learning while movement is constrained by swarm rules (keep distance, avoid obstacles, stay in bounds). The run is animated to show agent positions, obstacles, and the number of agents that have reached the goal.

## Features Implemented

- Grid environment with random goal placement and non‑overlapping, non‑touching rectangular obstacles (`env.py`).
- Multiple agents spawned on valid, free cells (`GridWorld.reset`).
- Tabular Q‑Learning agent with ε‑greedy action selection, discounting, and learning rate (`rl.py`).
- Action space includes stay and 4-neighborhood moves: down, up, right, left, stay.
- Swarm rules ensure: in‑bounds movement, obstacle avoidance, and minimum Manhattan spacing from other agents except when stepping onto the goal (`swarm.apply_swarm_rules`).
- Online learning each step; agents continue until all reach the goal (`main.py`).
- Matplotlib animation of the grid, obstacles, goal (red star), and live reached count overlay (`visualize.py`).
- Simple configurable parameters (`NUM_AGENTS`, `NUM_OBSTACLES`, `GRID_SIZE`, `MAX_STEPS`) and reward shaping via `reward_function` in `main.py`.

## How to Install and Run

Prerequisites:

- Python 3.10+
- Windows PowerShell examples below

### Clone the repository

```powershell
git clone https://github.com/Chanaka-Prasanna/assignment-1.git
cd assignment-1
```

### Set up the environment

- Conda

  - Create: `conda create -p ./venv python==3.10`
  - Activate (PowerShell): `conda activate ./venv`

- Python venv (no Conda)

  ```powershell
  py -3.10 -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

### Install dependencies

```powershell
pip install -r requirements.txt
```

### Run

```powershell
python main.py
```

## How to Use

- Edit parameters in `main.py`:
  - `NUM_AGENTS`, `NUM_OBSTACLES`, `GRID_SIZE`, `MAX_STEPS`
- Tweak `reward_function` to encourage desired behavior (goal reward, obstacle penalty, step penalty).
- Run `python main.py` to launch an animation window. The overlay shows how many agents have reached the goal.

## Swarm Coordination Logic

Implemented in `swarm.py` as `apply_swarm_rules(agent_pos, action, agents, obstacles, goal, min_dist=1, rows, cols)`:

1. Candidate move: `new_pos = agent_pos + action`.
2. In‑bounds clamp to `[0..rows-1] x [0..cols-1]`.
3. Obstacle avoidance: if `new_pos` lies in any rectangular obstacle, the agent stays (`return agent_pos`).
4. Minimum spacing: if `new_pos != goal`, and Manhattan distance to any other agent `<= min_dist`, the agent stays. Exception allows multiple agents to stack on the goal.
5. Otherwise, the agent moves to `new_pos`.

These rules deliver basic cohesion/spacing and collision avoidance while still letting everyone terminate on the same goal cell.

## RL Update Rule

Defined in `rl.py` (`QLearningAgent.update`), with constants `ALPHA = 0.5`, `GAMMA = 0.9`, `EPSILON = 0.2` and actions `[(1,0), (-1,0), (0,1), (0,-1), (0,0)]`.

- State representation: `(agent_row, agent_col, goal_row, goal_col)` from `get_state`.
- Action selection: ε‑greedy over tabular Q‑values.
- Update (tabular Q‑Learning):

  Q(s,a) ← Q(s,a) + α [ r + γ max_a' Q(s',a') − Q(s,a) ]

## Evaluation Criteria Mapping

- Correctness and robustness of swarm navigation
  - Bounds clamping, obstacle rejection, and minimum Manhattan spacing ensure safe moves; goal exception avoids deadlock at termination.
- Integration of RL with swarm behavior
  - Each step: agent proposes an action via Q‑Learning, then `apply_swarm_rules` validates/constrains it before reward and Q‑update, tightly coupling learning with swarm dynamics (`main.py`).
- Code clarity and scalability
  - Clear separation of concerns across `env.py`, `rl.py`, `swarm.py`, `visualize.py`, and `main.py`. Parameters centralized in `main.py`. Logic is easily extensible (e.g., more actions, different rewards, more rules).
- Visualization clarity
  - Grid with ticks, gray rectangles for obstacles, red star for goal, blue dots for agents, and a live reached counter overlay updated each frame.

## Project Structure

- `env.py` — `GridWorld` for goal/obstacle placement and agent spawning.
- `rl.py` — `QLearningAgent` with ε‑greedy policy and tabular Q updates.
- `swarm.py` — `apply_swarm_rules` for bounds/obstacle/spacing logic.
- `visualize.py` — Matplotlib animation and overlay.
- `main.py` — Simulation loop, rewards, and configuration.
- `requirements.txt` — Python dependencies.
