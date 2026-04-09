import json
import numpy as np
from simulation import run_episode, run_noise_sweep
from visualize import save_trajectories, save_reward, save_rmse
from config import TARGET, DT, N_EPISODES, NOISE_LEVELS

CONTROLLERS = ['PID', 'RL', 'Hybrid']

print('Running episodes...')
episodes = {}
for name in CONTROLLERS:
    eps = [run_episode(name, noise_std=0.0, seed=i) for i in range(N_EPISODES)]
    episodes[name] = eps
    settled = sum(e['settled'] for e in eps)
    mean_err = np.mean([e['final_error'] for e in eps])
    print(f'  {name:8s}  settled={settled}/{N_EPISODES}  final_error={mean_err:.2f} m')

print('Running noise sweep...')
rmse_sweep = {}
for name in CONTROLLERS:
    rmse_sweep[name] = run_noise_sweep(name, NOISE_LEVELS, n_episodes=6)

print('Saving plots...')
save_trajectories(episodes, TARGET)
save_reward(episodes, DT)
save_rmse(rmse_sweep, NOISE_LEVELS)

# summary.json
summary = {}
for name, eps in episodes.items():
    ttts = [e['time_to_target'] for e in eps if e['time_to_target'] is not None]
    summary[name] = {
        'final_error_mean':          float(np.mean([e['final_error'] for e in eps])),
        'final_error_std':           float(np.std([e['final_error'] for e in eps])),
        'position_rmse_mean':        float(np.mean([e['rmse'] for e in eps])),
        'position_rmse_std':         float(np.std([e['rmse'] for e in eps])),
        'time_to_target_mean':       float(np.mean(ttts)) if ttts else float('nan'),
        'time_to_target_std':        float(np.std(ttts))  if ttts else float('nan'),
        'safety_violations_mean':    float(np.mean([e['safety_violations'] for e in eps])),
        'settled_mean':              float(np.mean([e['settled'] for e in eps])),
        'total_reward_mean':         float(np.mean([e['rewards'].sum() for e in eps])),
    }

with open('outputs/summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print('Done — outputs/ updated.')
