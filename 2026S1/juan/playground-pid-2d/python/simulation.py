import numpy as np
from drone import Drone2D
from pid import PIDController
from config import (TARGET, MAX_STEPS, DT, F_HOVER, SETTLE_THRESHOLD,
                    KP_Z, KI_Z, KD_Z, KP_X, KI_X, KD_X)


def reward_fn(x, z, vx, vz, fx, fz, target):
    tx, tz = target
    dist = np.sqrt((x - tx)**2 + (z - tz)**2)
    energy = 0.001 * (fx**2 + (fz - F_HOVER)**2)
    safety = -50.0 if (z < 0.05 and dist > 1.0) else 0.0
    return -dist - energy + safety


def run_episode(controller_type, noise_std=0.0, seed=None):
    """
    Run one episode. Returns a dict with trajectory and metrics.
    controller_type: 'PID' | 'RL' | 'Hybrid'
    """
    if seed is not None:
        np.random.seed(seed)

    drone = Drone2D(x=0.0, z=0.0)
    tx, tz = TARGET

    pid = PIDController() if controller_type in ('PID', 'Hybrid') else None

    xs, zs, rewards = [], [], []
    time_to_target = None
    safety_violations = 0
    settled = False

    for step in range(MAX_STEPS):
        obs_x, obs_z, vx, vz = drone.step(0.0, F_HOVER, noise_std=0.0)  # get clean state first
        # now get noisy observation for controller
        obs_xn = obs_x + np.random.normal(0, noise_std) if noise_std > 0 else obs_x
        obs_zn = obs_z + np.random.normal(0, noise_std) if noise_std > 0 else obs_z

        if controller_type == 'PID':
            fx, fz = pid.act(obs_xn, obs_zn, vx, vz, tx, tz)

        elif controller_type == 'RL':
            # Untrained RL: noisy random policy biased toward hover
            fx = np.random.normal(0, 3.0)
            fz = F_HOVER + np.random.normal(0, 6.0)
            fz = max(0.0, fz)

        elif controller_type == 'Hybrid':
            # PID for altitude, random for horizontal
            _, fz = pid.act(obs_xn, obs_zn, vx, vz, tx, tz)
            fx = np.random.normal(0, 2.5)

        # Apply to drone
        obs_x, obs_z, vx, vz = drone.step(fx, fz, noise_std=0.0)

        r = reward_fn(drone.x, drone.z, vx, vz, fx, fz, TARGET)
        xs.append(drone.x)
        zs.append(drone.z)
        rewards.append(r)

        dist = np.sqrt((drone.x - tx)**2 + (drone.z - tz)**2)

        if dist < SETTLE_THRESHOLD and time_to_target is None:
            time_to_target = step * DT
            settled = True

        if drone.z < 0.05 and step > 5:
            safety_violations += 1

    xs = np.array(xs)
    zs = np.array(zs)
    pos = np.stack([xs, zs], axis=1)
    target_arr = np.array(TARGET)
    rmse = float(np.sqrt(np.mean(np.sum((pos - target_arr)**2, axis=1))))
    final_error = float(np.sqrt((xs[-1] - tx)**2 + (zs[-1] - tz)**2))

    return {
        'xs': xs,
        'zs': zs,
        'rewards': np.array(rewards),
        'rmse': rmse,
        'final_error': final_error,
        'time_to_target': time_to_target,
        'safety_violations': safety_violations,
        'settled': settled,
    }


def run_noise_sweep(controller_type, noise_levels, n_episodes=5):
    """Returns mean RMSE per noise level."""
    rmses = []
    for noise in noise_levels:
        episode_rmses = [
            run_episode(controller_type, noise_std=noise, seed=i)['rmse']
            for i in range(n_episodes)
        ]
        rmses.append(np.mean(episode_rmses))
    return np.array(rmses)
