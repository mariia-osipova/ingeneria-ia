"""Simplified planar quadrotor dynamics.

The project brief mentions a 6DOF drone and multiple controller families. For
this playground, a 2D x-z-theta model is a better fit: it keeps the API small,
is easy to tune, and still exercises cascaded control, wind disturbances, and
path tracking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Tuple

import numpy as np

from config import DroneConfig


State = np.ndarray
Action = np.ndarray


def _clip(value: float, low: float, high: float) -> float:
    return float(np.clip(value, low, high))


@dataclass
class Drone:
    """Planar quadrotor with x, z and pitch dynamics."""

    config: DroneConfig = field(default_factory=DroneConfig)

    def __post_init__(self) -> None:
        self.state = np.zeros(6, dtype=float)

    @property
    def mass(self) -> float:
        return self.config.mass

    def reset(self, state: Iterable[float] | None = None) -> State:
        """Reset state to zeros or to a provided initial condition."""

        if state is None:
            self.state = np.zeros(6, dtype=float)
        else:
            array = np.asarray(state, dtype=float)
            if array.shape != (6,):
                raise ValueError("Drone state must have shape (6,).")
            self.state = array.copy()
        return self.state.copy()

    def observation(self) -> State:
        return self.state.copy()

    def total_thrust_and_torque(self, motor_thrusts: Iterable[float]) -> Tuple[float, float]:
        motor = np.asarray(motor_thrusts, dtype=float)
        if motor.shape != (2,):
            raise ValueError("Expected two motor thrust commands for the planar model.")

        motor = np.clip(motor, 0.0, self.config.max_thrust_per_motor)
        total_thrust = float(np.sum(motor) * self.config.thrust_coeff)
        torque = float((motor[1] - motor[0]) * self.config.arm_length)
        return total_thrust, torque

    def dynamics(self, state: State, control: Action, wind: Action | None = None) -> State:
        """Continuous-time dynamics.

        Parameters
        ----------
        state:
            [x, z, theta, x_dot, z_dot, theta_dot]
        control:
            [thrust_left, thrust_right]
        wind:
            Optional disturbance vector [ax, az, alpha].
        """

        wind_vec = np.zeros(3, dtype=float) if wind is None else np.asarray(wind, dtype=float)
        if wind_vec.shape != (3,):
            raise ValueError("Wind disturbance must have shape (3,).")

        x, z, theta, x_dot, z_dot, theta_dot = np.asarray(state, dtype=float)
        total_thrust, torque = self.total_thrust_and_torque(control)
        m = self.config.mass
        g = self.config.gravity
        I = self.config.inertia

        x_ddot = -(total_thrust / m) * np.sin(theta) - self.config.drag_linear * x_dot + wind_vec[0]
        z_ddot = (total_thrust / m) * np.cos(theta) - g - self.config.drag_linear * z_dot + wind_vec[1]
        theta_ddot = torque / I - self.config.drag_angular * theta_dot + wind_vec[2]

        return np.array([x_dot, z_dot, theta_dot, x_ddot, z_ddot, theta_ddot], dtype=float)

    def step(self, control: Action, dt: float, wind: Action | None = None) -> State:
        """Advance the system with semi-implicit Euler integration."""

        deriv = self.dynamics(self.state, control, wind=wind)
        self.state = self.state + dt * deriv

        self.state[2] = _clip(self.state[2], -self.config.max_tilt, self.config.max_tilt)
        self.state[3] = _clip(self.state[3], -self.config.max_speed, self.config.max_speed)
        self.state[4] = _clip(self.state[4], -self.config.max_speed, self.config.max_speed)
        self.state[5] = _clip(self.state[5], -self.config.max_angular_speed, self.config.max_angular_speed)
        self.state[0] = _clip(self.state[0], -self.config.position_bound, self.config.position_bound)
        self.state[1] = _clip(self.state[1], -self.config.position_bound, self.config.position_bound)
        return self.state.copy()

    def is_safe(self) -> bool:
        return bool(np.linalg.norm(self.state[:2]) <= self.config.position_bound)

    def copy(self) -> "Drone":
        clone = Drone(self.config)
        clone.state = self.state.copy()
        return clone
