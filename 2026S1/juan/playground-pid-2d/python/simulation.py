"""Simulation utilities for the planar drone playground."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

from config import SimulationConfig, WindConfig, WaypointConfig
from drone import Drone
from pid import CascadedPIDController, HybridController, PIDGains


def default_wind(t: float, config: WindConfig, rng: np.random.Generator) -> np.ndarray:
    """Sine + noise disturbance matching the project brief."""

    base = config.amplitude * np.sin(2.0 * np.pi * config.frequency * t + config.phase)
    noise = rng.normal(0.0, config.noise_std, size=3)
    return np.array(
        [
            base + noise[0],
            config.vertical_ratio * base + noise[1],
            config.angular_coupling * base + noise[2],
        ],
        dtype=float,
    )


def rmse(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    return float(np.sqrt(np.mean(np.square(values)))) if values.size else 0.0


def path_rmse(positions: np.ndarray, target: np.ndarray) -> float:
    positions = np.asarray(positions, dtype=float)
    target = np.asarray(target, dtype=float)
    errors = positions[:, :2] - target[None, :]
    return rmse(np.linalg.norm(errors, axis=1))


def energy_cost(actions: np.ndarray, dt: float, scale: float = 1.0) -> float:
    actions = np.asarray(actions, dtype=float)
    return float(scale * np.sum(np.sum(np.square(actions), axis=1) * dt))


def time_to_target(positions: np.ndarray, target: np.ndarray, dt: float, tolerance: float) -> Optional[float]:
    positions = np.asarray(positions, dtype=float)
    target = np.asarray(target, dtype=float)
    distances = np.linalg.norm(positions[:, :2] - target[None, :], axis=1)
    hits = np.flatnonzero(distances <= tolerance)
    if hits.size == 0:
        return None
    return float(hits[0] * dt)


def safety_violations(positions: np.ndarray, bound: float) -> int:
    positions = np.asarray(positions, dtype=float)
    return int(np.sum(np.linalg.norm(positions[:, :2], axis=1) > bound))


@dataclass
class EpisodeResult:
    states: np.ndarray
    actions: np.ndarray
    targets: np.ndarray
    times: np.ndarray
    metrics: Dict[str, float | int | None]


@dataclass
class DroneSimulator:
    """Run closed-loop episodes with a controller and disturbance model."""

    drone: Drone = field(default_factory=Drone)
    sim_config: SimulationConfig = field(default_factory=SimulationConfig)
    wind_config: Optional[WindConfig] = None
    rng: np.random.Generator = field(init=False)

    def __post_init__(self) -> None:
        self.rng = np.random.default_rng(self.sim_config.seed)

    def reset(self, state: Iterable[float] | None = None) -> np.ndarray:
        return self.drone.reset(state)

    def _wind(self, t: float) -> np.ndarray:
        if self.wind_config is None:
            return np.zeros(3, dtype=float)
        return default_wind(t, self.wind_config, self.rng)

    def step(self, control: np.ndarray, t: float) -> np.ndarray:
        wind = self._wind(t)
        return self.drone.step(control, self.sim_config.dt, wind=wind)

    def run(
        self,
        controller: Callable[[np.ndarray, np.ndarray, float], np.ndarray],
        target: np.ndarray,
        initial_state: Iterable[float] | None = None,
    ) -> EpisodeResult:
        """Run a single target-tracking episode."""

        self.reset(initial_state)
        target = np.asarray(target, dtype=float)
        if target.shape != (2,):
            raise ValueError("Target must be [x, z].")

        steps = self.sim_config.steps()
        states: List[np.ndarray] = []
        actions: List[np.ndarray] = []
        times: List[float] = []
        targets: List[np.ndarray] = []

        for step in range(steps):
            t = step * self.sim_config.dt
            state = self.drone.observation()
            action = np.asarray(controller(state, target, self.sim_config.dt), dtype=float)
            if action.shape != (2,):
                raise ValueError("Controller must return two motor commands.")
            post_state = self.step(action, t)
            states.append(post_state)
            actions.append(action)
            times.append(t)
            targets.append(target.copy())

        state_array = np.asarray(states, dtype=float)
        action_array = np.asarray(actions, dtype=float)
        time_array = np.asarray(times, dtype=float)
        target_array = np.asarray(targets, dtype=float)

        metrics = {
            "position_rmse": path_rmse(state_array, target),
            "time_to_target": time_to_target(
                state_array, target, self.sim_config.dt, self.sim_config.target_tolerance
            ),
            "energy_cost": energy_cost(action_array, self.sim_config.dt),
            "safety_violations": safety_violations(state_array, self.sim_config.safety_radius),
            "final_distance": float(np.linalg.norm(state_array[-1, :2] - target)),
        }
        return EpisodeResult(state_array, action_array, target_array, time_array, metrics)

    def follow_waypoints(
        self,
        controller: Callable[[np.ndarray, np.ndarray, float], np.ndarray],
        waypoints: Sequence[Sequence[float]] | None = None,
        initial_state: Iterable[float] | None = None,
    ) -> EpisodeResult:
        """Run the simulator over a waypoint list."""

        sequence = waypoints or WaypointConfig().waypoints
        segment_states: List[np.ndarray] = []
        segment_actions: List[np.ndarray] = []
        segment_targets: List[np.ndarray] = []
        segment_times: List[np.ndarray] = []
        offset = 0.0
        for target in sequence:
            result = self.run(controller, np.asarray(target, dtype=float), initial_state=initial_state)
            segment_states.append(result.states)
            segment_actions.append(result.actions)
            segment_targets.append(result.targets)
            segment_times.append(result.times + offset)
            offset = float(segment_times[-1][-1] + self.sim_config.dt)
            initial_state = result.states[-1]

        states = np.vstack(segment_states)
        actions = np.vstack(segment_actions)
        targets = np.vstack(segment_targets)
        times = np.concatenate(segment_times)
        target_center = np.mean(np.asarray(sequence, dtype=float), axis=0)
        metrics = {
            "position_rmse": path_rmse(states, target_center),
            "time_to_target": time_to_target(states, np.asarray(sequence[-1], dtype=float), self.sim_config.dt, self.sim_config.target_tolerance),
            "energy_cost": energy_cost(actions, self.sim_config.dt),
            "safety_violations": safety_violations(states, self.sim_config.safety_radius),
            "final_distance": float(np.linalg.norm(states[-1, :2] - np.asarray(sequence[-1], dtype=float))),
        }
        return EpisodeResult(states, actions, targets, times, metrics)


class DroneEnv:
    """Gym-like environment wrapper.

    The interface is intentionally lightweight: it exposes reset/step/observe
    methods and can be used by a future Gym or Stable-Baselines3 wrapper.
    """

    def __init__(
        self,
        simulator: DroneSimulator | None = None,
        target: Sequence[float] = (0.0, 1.0),
    ) -> None:
        self.simulator = simulator or DroneSimulator()
        self.target = np.asarray(target, dtype=float)
        self.t = 0.0

    def reset(self, state: Iterable[float] | None = None) -> np.ndarray:
        self.t = 0.0
        return self.simulator.reset(state)

    def observation(self) -> np.ndarray:
        return self.simulator.drone.observation()

    def step(self, action: Sequence[float]) -> Tuple[np.ndarray, float, bool, Dict[str, float]]:
        state = self.simulator.step(np.asarray(action, dtype=float), self.t)
        self.t += self.simulator.sim_config.dt
        distance = float(np.linalg.norm(state[:2] - self.target))
        reward = -distance - 0.01 * float(np.sum(np.square(action)))
        done = bool(distance <= self.simulator.sim_config.target_tolerance)
        info = {"distance": distance}
        return state, reward, done, info


def make_pid_controller() -> CascadedPIDController:
    return CascadedPIDController()


def make_hybrid_controller() -> HybridController:
    return HybridController()


def run_pid_episode(
    target: Sequence[float] = (0.0, 1.0),
    wind: bool = False,
    initial_state: Iterable[float] | None = None,
) -> EpisodeResult:
    simulator = DroneSimulator(wind_config=WindConfig() if wind else None)
    controller = make_pid_controller()

    def policy(state: np.ndarray, tgt: np.ndarray, dt: float) -> np.ndarray:
        return controller.compute(state, tgt, dt)

    return simulator.run(policy, np.asarray(target, dtype=float), initial_state=initial_state)


def run_heuristic_episode(
    target: Sequence[float] = (0.0, 1.0),
    wind: bool = False,
    initial_state: Iterable[float] | None = None,
) -> EpisodeResult:
    simulator = DroneSimulator(wind_config=WindConfig() if wind else None)
    controller = CascadedPIDController(
        gains=PIDGains(
            x=(0.7, 0.0, 0.25),
            z=(3.5, 0.12, 1.2),
            theta=(6.5, 0.05, 1.7),
        )
    )

    def policy(state: np.ndarray, tgt: np.ndarray, dt: float) -> np.ndarray:
        return controller.compute(state, tgt, dt)

    return simulator.run(policy, np.asarray(target, dtype=float), initial_state=initial_state)


def run_hybrid_episode(
    target: Sequence[float] = (0.0, 1.0),
    wind: bool = False,
    initial_state: Iterable[float] | None = None,
    residual_fn: Callable[[np.ndarray, np.ndarray, float], np.ndarray] | None = None,
) -> EpisodeResult:
    simulator = DroneSimulator(wind_config=WindConfig() if wind else None)
    controller = make_hybrid_controller()

    def policy(state: np.ndarray, tgt: np.ndarray, dt: float) -> np.ndarray:
        residual = residual_fn(state, tgt, dt) if residual_fn is not None else None
        return controller.compute(state, tgt, dt, residual=residual)

    return simulator.run(policy, np.asarray(target, dtype=float), initial_state=initial_state)
