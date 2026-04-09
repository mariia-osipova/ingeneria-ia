import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

COLORS = {
    'PID':    '#2a6ebb',
    'RL':     '#c0392b',
    'Hybrid': '#e67e22',
}

STYLE = {
    'figure.facecolor': '#fafafa',
    'axes.facecolor':   '#fafafa',
    'axes.edgecolor':   '#cccccc',
    'axes.grid':        True,
    'grid.color':       '#e0e0e0',
    'grid.linewidth':   0.6,
    'axes.spines.top':  False,
    'axes.spines.right':False,
    'font.family':      'sans-serif',
    'font.size':        10,
    'axes.labelsize':   10,
    'axes.titlesize':   11,
    'axes.titleweight': 'normal',
    'xtick.labelsize':  9,
    'ytick.labelsize':  9,
    'legend.fontsize':  9,
    'legend.frameon':   False,
}


def save_trajectories(episodes_by_controller, target):
    with plt.rc_context(STYLE):
        fig, ax = plt.subplots(figsize=(6, 5))

        tx, tz = target
        ax.scatter([tx], [tz], s=80, color='#333', zorder=5, marker='x', linewidths=2)
        ax.annotate('target (5, 5)', (tx, tz), textcoords='offset points',
                    xytext=(6, 6), fontsize=8, color='#555')

        ax.scatter([0], [0], s=60, color='#888', zorder=5, marker='o')
        ax.annotate('start', (0, 0), textcoords='offset points',
                    xytext=(4, 4), fontsize=8, color='#888')

        for name, episodes in episodes_by_controller.items():
            color = COLORS[name]
            for i, ep in enumerate(episodes):
                alpha = 0.35 if i > 0 else 0.9
                lw = 1.4 if i > 0 else 2.0
                ax.plot(ep['xs'], ep['zs'], color=color, alpha=alpha, linewidth=lw)

        patches = [mpatches.Patch(color=COLORS[n], label=n)
                   for n in episodes_by_controller]
        ax.legend(handles=patches, loc='upper left')
        ax.set_xlabel('x  (m)')
        ax.set_ylabel('z  (m)')
        ax.set_title('Flight trajectories')
        ax.set_xlim(-1, 9)
        ax.set_ylim(-0.3, 9)

        fig.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, 'trajectories.png'), dpi=140)
        plt.close(fig)


def save_reward(episodes_by_controller, dt):
    with plt.rc_context(STYLE):
        fig, ax = plt.subplots(figsize=(6, 4))

        for name, episodes in episodes_by_controller.items():
            color = COLORS[name]
            # mean reward across episodes
            rewards = np.stack([ep['rewards'] for ep in episodes])
            mean_r = rewards.mean(axis=0)
            std_r  = rewards.std(axis=0)
            t = np.arange(len(mean_r)) * dt

            ax.plot(t, mean_r, color=color, linewidth=1.8, label=name)
            ax.fill_between(t, mean_r - std_r, mean_r + std_r,
                            color=color, alpha=0.15)

        ax.axhline(0, color='#aaa', linewidth=0.8, linestyle='--')
        ax.set_xlabel('time  (s)')
        ax.set_ylabel('reward')
        ax.set_title('Reward over episode')
        ax.legend()

        fig.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, 'reward.png'), dpi=140)
        plt.close(fig)


def save_rmse(rmse_by_controller, noise_levels):
    with plt.rc_context(STYLE):
        fig, ax = plt.subplots(figsize=(6, 4))

        for name, rmses in rmse_by_controller.items():
            ax.plot(noise_levels, rmses, color=COLORS[name],
                    linewidth=1.8, marker='o', markersize=5, label=name)

        ax.set_xlabel('sensor noise  σ  (m)')
        ax.set_ylabel('position RMSE  (m)')
        ax.set_title('RMSE vs sensor noise')
        ax.legend()

        fig.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, 'rmse.png'), dpi=140)
        plt.close(fig)
