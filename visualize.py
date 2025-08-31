import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

def visualize(env, agents_history):
    fig, ax = plt.subplots()
    ax.set_xlim(-0.5, env.cols - 0.5)
    ax.set_ylim(-0.5, env.rows - 0.5)
    ax.set_xticks(range(env.cols))
    ax.set_yticks(range(env.rows))
    ax.grid(True)

    # Draw obstacles
    for (r1, c1), (r2, c2) in env.obstacles:
        rect = patches.Rectangle((c1 - 0.5, r1 - 0.5),
                                 (c2 - c1 + 1), (r2 - r1 + 1),
                                 linewidth=1, edgecolor="black", facecolor="gray")
        ax.add_patch(rect)

    # Draw goal
    ax.plot(env.goal[1], env.goal[0], "r*", markersize=15)

    # Plot agents (current positions) - all same color
    agents_plot, = ax.plot([], [], "bo", markersize=10)

    # Trails per agent (paths taken) - distinct colors
    num_agents = len(agents_history[0]) if agents_history else 0
    cmap = plt.get_cmap("tab10")
    trail_colors = [cmap(i % cmap.N) for i in range(num_agents)]
    trails = [ax.plot([], [], "-", color=trail_colors[i], linewidth=1.5, alpha=0.9)[0]
              for i in range(num_agents)]

    # Title and overlay text objects
    title = ax.set_title("Run")
    overlay = ax.text(0.02, 1.02, "", transform=ax.transAxes, ha="left", va="bottom")

    def update(frame):
        if frame < len(agents_history):
            positions = agents_history[frame]
            reached = sum(1 for p in positions if p == env.goal)
            # update agent positions
            x = [c for r, c in positions]
            y = [r for r, c in positions]
            agents_plot.set_data(x, y)
            # update trails up to current frame
            for i in range(num_agents):
                xs = [agents_history[t][i][1] for t in range(frame + 1)]
                ys = [agents_history[t][i][0] for t in range(frame + 1)]
                trails[i].set_data(xs, ys)
            # update title and overlay
            title.set_text("Run")
            overlay.set_text(f"Reached: {reached}/{len(positions)}")
        return [agents_plot, *trails, title, overlay]

    # disable blit so text updates properly
    ani = FuncAnimation(fig, update, frames=len(agents_history), interval=500, blit=False, repeat=False)

    plt.show()
