o"""Configuration for the simplified 2D drone project.

The project spec describes a 6DOF quadrotor, but this playground keeps the
implementation intentionally small and self-contained. The model here is a
planar quadrotor with state [x, z, theta, x_dot, z_dot, theta_dot].
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

import numpy as np


@dataclass(frozen=True)
class DroneConfig:
    """Physical parameters for the simplified planar drone."""

    mass: float = 1.0
    gravity: float = 9.81
    arm_length: float = 0.18
    inertia: float = 0.02
    thrust_coeff: float = 1.0
    drag_linear: float = 0.08
    drag_angular: float = 0.02
    max_thrust_per_motor: float = 12.0
    max_tilt: float = np.deg2rad(35.0)
    max_speed: float = 8.0
    max_angular_speed: float = 6.0
    position_bound: float = 12.0
    energy_cost_scale: float = 1.0


@dataclass(frozen=True)
class PIDGains:
    """Default cascaded PID gains.

    Outer-loop controls x/z targets, inner-loop controls attitude.
    """

    x: Tuple[float, float, float] = (1.2, 0.0, 0.55)
    z: Tuple[float, float, float] = (5.5, 0.3, 2.4)
    theta: Tuple[float, float, float] = (10.0, 0.1, 2.8)


@dataclass(frozen=True)
class SimulationConfig:
    """Integration and evaluation settings."""

    dt: float = 0.02
    horizon: float = 20.0
    target_tolerance: float = 0.15
    safety_radius: float = 10.0
    path_gain: float = 1.0
    seed: int = 7

    def steps(self) -> int:
        return int(np.ceil(self.horizon / self.dt))


@dataclass(frozen=True)
class WindConfig:
    """Sine-plus-noise wind model used by the simulator."""

    amplitude: float = 0.7
    frequency: float = 0.35
    phase: float = 0.0
    noise_std: float = 0.08
    vertical_ratio: float = 0.25
    angular_coupling: float = 0.15


@dataclass(frozen=True)
class WaypointConfig:
    """Default target path used by the comparison experiments."""

    waypoints: Tuple[Tuple[float, float], ...] = field(
        default_factory=lambda: ((0.0, 1.0), (2.0, 1.5), (4.0, 1.0))
    )
    switch_distance: float = 0.25
