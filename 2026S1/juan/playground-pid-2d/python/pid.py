"""PID controllers for the planar drone.

The project spec describes a cascaded controller. This module implements a
pragmatic outer-loop position controller feeding an inner-loop attitude/thrust
controller. It also exposes a residual blending hook so the same interface can
support hybrid or RL-assisted control later.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Tuple

import numpy as np

from config import DroneConfig, PIDGains


def _clip(value: float, low: float, high: float) -> float:
    return float(np.clip(value, low, high))


@dataclass
class PIDAxis:
    """Single-axis PID with anti-windup and derivative on measurement."""

    kp: float
    ki: float
    kd: float
    integral_limit: float = 4.0
    output_limit: float = 10.0
    integral: float = 0.0
    previous_error: float = 0.0

    def reset(self) -> None:
        self.integral = 0.0
        self.previous_error = 0.0

    def update(self, error: float, dt: float) -> float:
        self.integral += error * dt
        self.integral = _clip(self.integral, -self.integral_limit, self.integral_limit)
        derivative = (error - self.previous_error) / dt if dt > 0 else 0.0
        self.previous_error = error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        return _clip(output, -self.output_limit, self.output_limit)


@dataclass
class CascadedPIDController:
    """Outer x/z loop and inner pitch loop."""

    gains: PIDGains = field(default_factory=PIDGains)
    drone_config: DroneConfig = field(default_factory=DroneConfig)
    x_pid: PIDAxis = field(init=False)
    z_pid: PIDAxis = field(init=False)
    theta_pid: PIDAxis = field(init=False)

    def __post_init__(self) -> None:
        self.x_pid = PIDAxis(*self.gains.x, output_limit=self.drone_config.max_tilt)
        self.z_pid = PIDAxis(
            *self.gains.z,
            output_limit=2.0 * self.drone_config.mass * self.drone_config.gravity,
        )
        self.theta_pid = PIDAxis(
            *self.gains.theta,
            output_limit=self.drone_config.max_thrust_per_motor * self.drone_config.arm_length,
        )

    def reset(self) -> None:
        self.x_pid.reset()
        self.z_pid.reset()
        self.theta_pid.reset()

    def compute(self, state: np.ndarray, target: np.ndarray, dt: float) -> np.ndarray:
        """Return planar motor thrust commands."""

        state = np.asarray(state, dtype=float)
        target = np.asarray(target, dtype=float)
        if state.shape != (6,):
            raise ValueError("State must have shape (6,).")
        if target.shape != (2,):
            raise ValueError("Target must have shape (2,) for [x, z].")

        x, z, theta, x_dot, z_dot, theta_dot = state
        target_x, target_z = target

        x_error = target_x - x
        z_error = target_z - z

        # Positive x error requires a negative pitch command in this planar model.
        theta_ref = -self.x_pid.update(x_error, dt)
        theta_ref = _clip(theta_ref, -self.drone_config.max_tilt, self.drone_config.max_tilt)

        thrust_correction = self.z_pid.update(z_error, dt)
        thrust_base = self.drone_config.mass * self.drone_config.gravity + thrust_correction

        theta_error = theta_ref - theta
        torque_cmd = self.theta_pid.update(theta_error, dt)

        left = 0.5 * (thrust_base - torque_cmd / self.drone_config.arm_length)
        right = 0.5 * (thrust_base + torque_cmd / self.drone_config.arm_length)
        motor = np.array([left, right], dtype=float)
        return np.clip(motor, 0.0, self.drone_config.max_thrust_per_motor)


@dataclass
class HybridController:
    """Blend a nominal PID policy with a residual correction.

    The residual is interpreted as a small adjustment to the two motor thrust
    commands. This makes the class suitable for an RL policy that outputs
    corrections over a safe PID baseline.
    """

    pid: CascadedPIDController = field(default_factory=CascadedPIDController)
    residual_scale: float = 0.35

    def reset(self) -> None:
        self.pid.reset()

    def compute(self, state: np.ndarray, target: np.ndarray, dt: float, residual: Iterable[float] | None = None) -> np.ndarray:
        nominal = self.pid.compute(state, target, dt)
        if residual is None:
            return nominal
        correction = np.asarray(residual, dtype=float)
        if correction.shape != (2,):
            raise ValueError("Residual correction must have shape (2,).")
        corrected = nominal + self.residual_scale * correction
        return np.clip(corrected, 0.0, self.pid.drone_config.max_thrust_per_motor)


def heuristic_policy(state: np.ndarray, target: np.ndarray, config: DroneConfig | None = None) -> np.ndarray:
    """Lightweight RL placeholder.

    This is intentionally not a training implementation. It provides a
    deterministic policy-like interface that can later be swapped with PPO or
    any learned model without changing the simulator API.
    """

    cfg = config or DroneConfig()
    state = np.asarray(state, dtype=float)
    target = np.asarray(target, dtype=float)
    x, z, theta, x_dot, z_dot, theta_dot = state
    x_error = target[0] - x
    z_error = target[1] - z

    # This is a compact policy baseline, not a learned agent.
    theta_ref = np.clip(-1.4 * x_error - 0.6 * x_dot, -cfg.max_tilt, cfg.max_tilt)
    theta_error = theta_ref - theta
    torque = np.clip(
        9.0 * theta_error - 1.3 * theta_dot,
        -cfg.max_thrust_per_motor * cfg.arm_length,
        cfg.max_thrust_per_motor * cfg.arm_length,
    )
    base = cfg.mass * cfg.gravity + 6.2 * z_error - 2.3 * z_dot
    left = 0.5 * (base - torque / cfg.arm_length)
    right = 0.5 * (base + torque / cfg.arm_length)
    return np.clip(np.array([left, right], dtype=float), 0.0, cfg.max_thrust_per_motor)
