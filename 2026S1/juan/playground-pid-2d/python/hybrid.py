"""PID and hybrid controllers for the 2D drone project."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import math

import numpy as np

from rl_agent import DroneConfig, LinearFeedbackPolicy


@dataclass
class PIDGains:
    x_p: float = 1.6
    x_i: float = 0.05
    x_d: float = 0.8
    z_p: float = 2.8
    z_i: float = 0.08
    z_d: float = 1.1
    theta_p: float = 8.0
    theta_d: float = 1.8


class CascadePIDController:
    """Planar cascade PID: outer position loop, inner attitude loop."""

    def __init__(self, config: DroneConfig | None = None, gains: PIDGains | None = None):
        self.config = config or DroneConfig()
        self.gains = gains or PIDGains()
        self._x_integral = 0.0
        self._z_integral = 0.0
        self._prev_error = np.zeros(2, dtype=float)

    def reset(self) -> None:
        self._x_integral = 0.0
        self._z_integral = 0.0
        self._prev_error = np.zeros(2, dtype=float)

    def _normalize_thrust(self, thrust: float) -> float:
        hover = self.config.mass * self.config.gravity
        return float(np.clip((thrust / hover - 1.0) / 0.75, -1.0, 1.0))

    def _normalize_torque(self, torque: float) -> float:
        return float(np.clip(torque / self.config.max_torque, -1.0, 1.0))

    def act(self, observation: np.ndarray) -> np.ndarray:
        x, z, vx, vz, theta, omega, tx, tz = np.asarray(observation, dtype=float)
        ex = tx - x
        ez = tz - z

        dt = self.config.dt
        self._x_integral += ex * dt
        self._z_integral += ez * dt
        dex = (ex - self._prev_error[0]) / dt
        dez = (ez - self._prev_error[1]) / dt
        self._prev_error = np.array([ex, ez], dtype=float)

        theta_des = -(
            self.gains.x_p * ex
            + self.gains.x_i * self._x_integral
            + self.gains.x_d * (-vx + 0.1 * dex)
        )
        theta_des = float(np.clip(theta_des, -self.config.max_tilt, self.config.max_tilt))

        thrust = self.config.mass * self.config.gravity + (
            self.gains.z_p * ez + self.gains.z_i * self._z_integral + self.gains.z_d * (-vz + 0.1 * dez)
        ) * self.config.mass
        thrust = float(np.clip(thrust, 0.0, self.config.max_thrust * self.config.mass * self.config.gravity))

        theta_error = theta_des - theta
        theta_rate_error = -omega
        torque = self.gains.theta_p * theta_error + self.gains.theta_d * theta_rate_error

        return np.array([self._normalize_thrust(thrust), self._normalize_torque(torque)], dtype=float)


class HybridController:
    """Blend a PID controller with an RL-style linear policy.

    The blend weight increases when the drone is far from the target, so the RL
    policy can contribute navigation while PID keeps the vehicle stable near the
    goal.
    """

    def __init__(
        self,
        pid: CascadePIDController | None = None,
        rl_policy: LinearFeedbackPolicy | None = None,
        blend_center: float = 1.5,
        blend_scale: float = 0.8,
        max_rl_weight: float = 0.03,
    ):
        self.pid = pid or CascadePIDController()
        self.rl_policy = rl_policy or LinearFeedbackPolicy.from_heuristic()
        self.blend_center = blend_center
        self.blend_scale = blend_scale
        self.max_rl_weight = max_rl_weight

    def reset(self) -> None:
        self.pid.reset()
        self.rl_policy.reset()

    def act(self, observation: np.ndarray) -> np.ndarray:
        pid_action = self.pid.act(observation)
        rl_action = self.rl_policy.act(observation)
        x, z, vx, vz, theta, omega, tx, tz = np.asarray(observation, dtype=float)
        error = math.sqrt((tx - x) ** 2 + (tz - z) ** 2)
        blend = 1.0 / (1.0 + math.exp(-(error - self.blend_center) / max(self.blend_scale, 1e-6)))
        blend = float(np.clip(self.max_rl_weight * blend, 0.0, self.max_rl_weight))
        action = (1.0 - blend) * pid_action + blend * rl_action
        return np.clip(action, -1.0, 1.0)


def build_default_pid() -> CascadePIDController:
    return CascadePIDController()


def build_default_hybrid(rl_policy: LinearFeedbackPolicy | None = None) -> HybridController:
    return HybridController(pid=build_default_pid(), rl_policy=rl_policy)
