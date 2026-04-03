"""Lightweight RL scaffold for the drone comparison project.

The PDF mentions PPO and Stable-Baselines3, but the repository should still be
usable without heavyweight training dependencies. This module provides:

* a compact 2D quadrotor environment;
* a gym-like API (`reset`, `step`, `observation_space`, `action_space`);
* a small linear policy class;
* a lightweight random-search learner that can act as an RL baseline;
* rollout helpers shared by PID, RL, and hybrid controllers.

The dynamics are intentionally planar. The state is:

    [x, z, vx, vz, theta, omega]

and the action is:

    [collective_thrust_cmd, torque_cmd]

both normalized to [-1, 1]. This is sufficient for the project notebook and
lets a future PPO implementation drop into the same interface.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, Mapping, Protocol, Sequence

import math
import random

import numpy as np


class ControllerLike(Protocol):
    def act(self, observation: np.ndarray) -> np.ndarray:
        ...

    def reset(self) -> None:
        ...


@dataclass(frozen=True)
class BoxSpace:
    """Small substitute for `gym.spaces.Box`."""

    low: np.ndarray
    high: np.ndarray

    def sample(self, rng: np.random.Generator | None = None) -> np.ndarray:
        rng = rng or np.random.default_rng()
        return rng.uniform(self.low, self.high)

    def contains(self, value: Sequence[float] | np.ndarray) -> bool:
        arr = np.asarray(value, dtype=float)
        return arr.shape == self.low.shape and np.all(arr >= self.low) and np.all(arr <= self.high)


@dataclass
class DroneConfig:
    mass: float = 1.0
    gravity: float = 9.81
    inertia: float = 0.02
    arm_length: float = 0.16
    drag_linear: float = 0.08
    drag_angular: float = 0.12
    max_tilt: float = math.radians(35.0)
    max_thrust: float = 2.2
    max_torque: float = 2.5
    dt: float = 0.02
    max_time: float = 12.0
    target_tolerance: float = 0.15
    hold_steps: int = 8
    action_penalty: float = 0.02
    position_penalty: float = 1.0
    velocity_penalty: float = 0.15
    attitude_penalty: float = 0.05
    reward_bonus: float = 8.0
    wind_strength: float = 0.12
    wind_frequency: float = 0.7
    wind_noise: float = 0.02
    wind_enabled: bool = True
    x_bounds: tuple[float, float] = (-5.0, 5.0)
    z_bounds: tuple[float, float] = (0.0, 5.0)
    target: tuple[float, float] = (1.0, 1.0)
    initial_x_span: tuple[float, float] = (-0.4, 0.4)
    initial_z_span: tuple[float, float] = (0.15, 0.45)
    initial_velocity_span: tuple[float, float] = (-0.05, 0.05)


@dataclass
class DroneState:
    x: float = 0.0
    z: float = 0.25
    vx: float = 0.0
    vz: float = 0.0
    theta: float = 0.0
    omega: float = 0.0

    def as_array(self) -> np.ndarray:
        return np.array([self.x, self.z, self.vx, self.vz, self.theta, self.omega], dtype=float)

    @classmethod
    def from_array(cls, values: Sequence[float] | np.ndarray) -> "DroneState":
        arr = np.asarray(values, dtype=float)
        if arr.shape != (6,):
            raise ValueError("DroneState expects a 6-element vector")
        return cls(*map(float, arr))


@dataclass
class Rollout:
    times: np.ndarray
    states: np.ndarray
    actions: np.ndarray
    targets: np.ndarray
    rewards: np.ndarray
    infos: list[dict]
    dt: float

    def as_dict(self) -> dict[str, np.ndarray | list[dict] | float]:
        return {
            "times": self.times,
            "states": self.states,
            "actions": self.actions,
            "targets": self.targets,
            "rewards": self.rewards,
            "infos": self.infos,
            "dt": self.dt,
        }


def _clip(value: np.ndarray, low: float, high: float) -> np.ndarray:
    return np.minimum(np.maximum(value, low), high)


class DroneEnv:
    """Simple 2D drone environment with a Gym-like API."""

    def __init__(self, config: DroneConfig | None = None, seed: int | None = None):
        self.config = config or DroneConfig()
        self.rng = np.random.default_rng(seed)
        self.state = DroneState()
        self.target = np.array(self.config.target, dtype=float)
        self.time = 0.0
        self._wind_phase = float(self.rng.uniform(0.0, 2.0 * math.pi))
        self.observation_space = BoxSpace(
            low=np.array([-10.0, 0.0, -20.0, -20.0, -math.pi, -20.0, -10.0, 0.0], dtype=float),
            high=np.array([10.0, 10.0, 20.0, 20.0, math.pi, 20.0, 10.0, 10.0], dtype=float),
        )
        self.action_space = BoxSpace(
            low=np.array([-1.0, -1.0], dtype=float),
            high=np.array([1.0, 1.0], dtype=float),
        )

    @property
    def hover_thrust(self) -> float:
        return self.config.mass * self.config.gravity

    def sample_initial_state(self) -> DroneState:
        x = float(self.rng.uniform(*self.config.initial_x_span))
        z = float(self.rng.uniform(*self.config.initial_z_span))
        vx = float(self.rng.uniform(*self.config.initial_velocity_span))
        vz = float(self.rng.uniform(*self.config.initial_velocity_span))
        theta = float(self.rng.normal(0.0, math.radians(2.5)))
        omega = float(self.rng.normal(0.0, 0.05))
        return DroneState(x=x, z=z, vx=vx, vz=vz, theta=theta, omega=omega)

    def sample_scenario(self, seed: int | None = None) -> tuple[DroneState, np.ndarray, float]:
        rng = np.random.default_rng(seed) if seed is not None else self.rng
        initial = DroneState(
            x=float(rng.uniform(*self.config.initial_x_span)),
            z=float(rng.uniform(*self.config.initial_z_span)),
            vx=float(rng.uniform(*self.config.initial_velocity_span)),
            vz=float(rng.uniform(*self.config.initial_velocity_span)),
            theta=float(rng.normal(0.0, math.radians(2.5))),
            omega=float(rng.normal(0.0, 0.05)),
        )
        target = np.array(self.config.target, dtype=float)
        return initial, target, float(rng.uniform(0.0, 2.0 * math.pi))

    def reset(
        self,
        initial_state: DroneState | Sequence[float] | None = None,
        target: Sequence[float] | None = None,
        wind_phase: float | None = None,
        seed: int | None = None,
    ) -> np.ndarray:
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.state = (
            initial_state
            if isinstance(initial_state, DroneState)
            else DroneState.from_array(initial_state)
            if initial_state is not None
            else self.sample_initial_state()
        )
        if target is not None:
            self.target = np.asarray(target, dtype=float)
        else:
            self.target = np.array(self.config.target, dtype=float)
        self.time = 0.0
        self._wind_phase = float(wind_phase if wind_phase is not None else self.rng.uniform(0.0, 2.0 * math.pi))
        return self._observation()

    def _observation(self) -> np.ndarray:
        return np.array(
            [
                self.state.x,
                self.state.z,
                self.state.vx,
                self.state.vz,
                self.state.theta,
                self.state.omega,
                self.target[0],
                self.target[1],
            ],
            dtype=float,
        )

    def _wind_force(self) -> np.ndarray:
        if not self.config.wind_enabled:
            return np.zeros(2, dtype=float)
        oscillation = math.sin(self.config.wind_frequency * self.time + self._wind_phase)
        gust = self.config.wind_strength * np.array(
            [
                oscillation,
                0.5 * math.cos(0.7 * self.config.wind_frequency * self.time + 0.5 * self._wind_phase),
            ],
            dtype=float,
        )
        noise = self.rng.normal(0.0, self.config.wind_noise, size=2)
        return gust + noise

    def _apply_action(self, action: np.ndarray) -> None:
        action = np.asarray(action, dtype=float)
        if action.shape != (2,):
            raise ValueError("Action must be a 2-element vector")
        action = _clip(action, -1.0, 1.0)

        collective_cmd, torque_cmd = action
        thrust = self.hover_thrust * (1.0 + 0.75 * collective_cmd)
        thrust = float(np.clip(thrust, 0.0, self.config.max_thrust * self.hover_thrust))
        torque = float(np.clip(torque_cmd, -1.0, 1.0) * self.config.max_torque)

        wind = self._wind_force()
        sin_theta = math.sin(self.state.theta)
        cos_theta = math.cos(self.state.theta)
        ax = (-thrust / self.config.mass) * sin_theta + wind[0] / self.config.mass - self.config.drag_linear * self.state.vx
        az = (thrust / self.config.mass) * cos_theta - self.config.gravity + wind[1] / self.config.mass - self.config.drag_linear * self.state.vz
        alpha = torque / self.config.inertia - self.config.drag_angular * self.state.omega

        self.state.x += self.state.vx * self.config.dt
        self.state.z += self.state.vz * self.config.dt
        self.state.vx += ax * self.config.dt
        self.state.vz += az * self.config.dt
        self.state.theta += self.state.omega * self.config.dt
        self.state.omega += alpha * self.config.dt
        self.state.theta = float(np.clip(self.state.theta, -self.config.max_tilt, self.config.max_tilt))
        self.state.z = float(max(0.0, self.state.z))
        if self.state.z <= 0.0 and self.state.vz < 0.0:
            self.state.vz = 0.0
        self.time += self.config.dt

    def step(self, action: Sequence[float] | np.ndarray) -> tuple[np.ndarray, float, bool, dict]:
        before = self._observation()
        self._apply_action(np.asarray(action, dtype=float))
        observation = self._observation()
        position_error = self.target - observation[:2]
        velocity_penalty = float(np.linalg.norm(observation[2:4]))
        attitude_penalty = float(abs(observation[4]) + 0.3 * abs(observation[5]))
        action_penalty = float(np.linalg.norm(np.asarray(action, dtype=float)))
        reward = (
            -self.config.position_penalty * float(np.linalg.norm(position_error))
            -self.config.velocity_penalty * velocity_penalty
            -self.config.attitude_penalty * attitude_penalty
            -self.config.action_penalty * action_penalty
        )

        success = float(np.linalg.norm(position_error)) <= self.config.target_tolerance and velocity_penalty < 0.15
        if success:
            reward += self.config.reward_bonus

        terminated = bool(self.time >= self.config.max_time)
        truncated = bool(
            observation[1] <= 0.0 and self.time > self.config.dt * 2.0
            or abs(observation[0]) > max(abs(self.config.x_bounds[0]), abs(self.config.x_bounds[1])) * 1.5
        )
        done = terminated or truncated
        info = {
            "success": success,
            "terminated": terminated,
            "truncated": truncated,
            "position_error": float(np.linalg.norm(position_error)),
            "before": before,
        }
        return observation, reward, done, info


def _policy_action(controller: ControllerLike | Callable[[np.ndarray], Sequence[float]], observation: np.ndarray) -> np.ndarray:
    if hasattr(controller, "act"):
        action = controller.act(observation)  # type: ignore[attr-defined]
    else:
        action = controller(observation)
    return np.asarray(action, dtype=float)


def run_episode(
    env: DroneEnv,
    controller: ControllerLike | Callable[[np.ndarray], Sequence[float]],
    *,
    initial_state: DroneState | Sequence[float] | None = None,
    target: Sequence[float] | None = None,
    wind_phase: float | None = None,
    seed: int | None = None,
    max_steps: int | None = None,
) -> Rollout:
    """Roll out one controller against one scenario."""

    observation = env.reset(initial_state=initial_state, target=target, wind_phase=wind_phase, seed=seed)
    if hasattr(controller, "reset"):
        controller.reset()  # type: ignore[attr-defined]

    steps = max_steps or int(math.ceil(env.config.max_time / env.config.dt))
    times = [env.time]
    states = [env.state.as_array()]
    actions: list[np.ndarray] = []
    targets: list[np.ndarray] = [env.target.copy()]
    rewards: list[float] = []
    infos: list[dict] = []

    for _ in range(steps):
        action = _policy_action(controller, observation)
        next_observation, reward, done, info = env.step(action)
        actions.append(np.asarray(action, dtype=float))
        rewards.append(float(reward))
        infos.append(info)
        observation = next_observation
        times.append(env.time)
        states.append(env.state.as_array())
        targets.append(env.target.copy())
        if done:
            break

    return Rollout(
        times=np.asarray(times, dtype=float),
        states=np.asarray(states, dtype=float),
        actions=np.asarray(actions, dtype=float) if actions else np.zeros((0, 2), dtype=float),
        targets=np.asarray(targets, dtype=float),
        rewards=np.asarray(rewards, dtype=float),
        infos=infos,
        dt=env.config.dt,
    )


class LinearFeedbackPolicy:
    """Tiny linear policy used as a PPO-style scaffold.

    The policy maps a feature vector to two bounded actions via `tanh`. The
    features are intentionally simple so the same class can later be replaced by
    a Stable-Baselines3 PPO model without changing the rest of the project.
    """

    def __init__(self, weights: np.ndarray | None = None, bias: np.ndarray | None = None):
        self.weights = np.asarray(weights, dtype=float) if weights is not None else np.zeros((8, 2), dtype=float)
        self.bias = np.asarray(bias, dtype=float) if bias is not None else np.zeros(2, dtype=float)

    @staticmethod
    def features(observation: np.ndarray) -> np.ndarray:
        x, z, vx, vz, theta, omega, tx, tz = np.asarray(observation, dtype=float)
        ex = tx - x
        ez = tz - z
        return np.array(
            [ex, ez, vx, vz, theta, omega, ex * ez, 1.0],
            dtype=float,
        )

    def act(self, observation: np.ndarray) -> np.ndarray:
        features = self.features(observation)
        action = np.tanh(features @ self.weights + self.bias)
        return np.clip(action, -1.0, 1.0)

    def reset(self) -> None:
        return None

    @classmethod
    def from_heuristic(cls) -> "LinearFeedbackPolicy":
        weights = np.array(
            [
                [0.8, 0.0],
                [1.2, 0.0],
                [0.25, 0.0],
                [-0.15, 0.0],
                [0.0, -1.6],
                [0.0, -0.4],
                [0.15, 0.0],
                [0.0, 0.0],
            ],
            dtype=float,
        )
        bias = np.array([0.0, 0.0], dtype=float)
        return cls(weights=weights, bias=bias)

    def copy(self) -> "LinearFeedbackPolicy":
        return LinearFeedbackPolicy(weights=self.weights.copy(), bias=self.bias.copy())


def _evaluate_policy_once(
    env: DroneEnv,
    policy: ControllerLike,
    scenario: tuple[DroneState, np.ndarray, float],
    max_steps: int | None = None,
) -> float:
    initial_state, target, wind_phase = scenario
    rollout = run_episode(
        env,
        policy,
        initial_state=initial_state,
        target=target,
        wind_phase=wind_phase,
        max_steps=max_steps,
    )
    total_reward = float(np.sum(rollout.rewards))
    final_error = float(np.linalg.norm(rollout.states[-1, :2] - rollout.targets[-1]))
    return total_reward - 4.0 * final_error


def train_linear_policy(
    env: DroneEnv,
    *,
    seed: int | None = None,
    candidates: int = 24,
    episodes: int = 6,
    max_steps: int | None = None,
    noise_scale: float = 0.25,
) -> LinearFeedbackPolicy:
    """Search around a heuristic policy to produce an RL baseline.

    This is not PPO. It is a lightweight, dependency-free stand-in that keeps
    the same control interface and gives the rest of the project something
    reproducible to compare against.
    """

    rng = np.random.default_rng(seed)
    base = LinearFeedbackPolicy.from_heuristic()
    if candidates <= 0 or episodes <= 0:
        return base

    best_policy = base.copy()
    scenarios = [env.sample_scenario(seed=int(rng.integers(0, 2**31 - 1))) for _ in range(episodes)]
    best_score = -float("inf")

    for _ in range(candidates):
        candidate = base.copy()
        candidate.weights = candidate.weights + rng.normal(0.0, noise_scale, size=candidate.weights.shape)
        candidate.bias = candidate.bias + rng.normal(0.0, noise_scale * 0.2, size=candidate.bias.shape)

        score = 0.0
        for scenario in scenarios:
            score += _evaluate_policy_once(env, candidate, scenario, max_steps=max_steps)
        score /= float(len(scenarios))

        if score > best_score:
            best_score = score
            best_policy = candidate

    return best_policy


def evaluate_controller(
    env: DroneEnv,
    controller: ControllerLike | Callable[[np.ndarray], Sequence[float]],
    scenarios: Sequence[tuple[DroneState, np.ndarray, float]],
    *,
    max_steps: int | None = None,
) -> list[Rollout]:
    runs: list[Rollout] = []
    for initial_state, target, wind_phase in scenarios:
        rollout = run_episode(
            env,
            controller,
            initial_state=initial_state,
            target=target,
            wind_phase=wind_phase,
            max_steps=max_steps,
        )
        runs.append(rollout)
    return runs

