"""Metrics helpers for the drone control comparison project.

The PDF describes position RMSE, time-to-target, energy cost, and safety
violations. This module keeps those calculations lightweight and dependency
free so the rest of the project can run without gym/stable-baselines.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Sequence

import numpy as np


@dataclass(frozen=True)
class SafetyBounds:
    """Axis-aligned safety envelope for the planar drone."""

    x_min: float = -5.0
    x_max: float = 5.0
    z_min: float = 0.0
    z_max: float = 5.0


def _to_array(values: Sequence[float] | np.ndarray) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if array.ndim == 1:
        return array
    return np.asarray(array, dtype=float)


def position_error(states: np.ndarray, targets: np.ndarray) -> np.ndarray:
    """Return the planar position error for each sample."""

    states = _to_array(states)
    targets = _to_array(targets)
    if states.shape[0] != targets.shape[0]:
        raise ValueError("states and targets must have the same length")
    return targets[:, :2] - states[:, :2]


def rmse(errors: np.ndarray) -> float:
    errors = _to_array(errors)
    if errors.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(np.sum(np.square(errors), axis=-1))))


def energy_cost(actions: np.ndarray, dt: float) -> float:
    """Approximate control effort by integrating the squared action norm."""

    actions = _to_array(actions)
    if actions.size == 0:
        return 0.0
    return float(np.sum(np.sum(np.square(actions), axis=-1)) * float(dt))


def time_to_target(
    times: np.ndarray,
    states: np.ndarray,
    target: np.ndarray,
    tolerance: float = 0.15,
    hold_steps: int = 8,
) -> float | None:
    """First time the drone remains within tolerance for a short hold window."""

    times = _to_array(times)
    states = _to_array(states)
    target = _to_array(target)
    if times.size == 0:
        return None

    errors = np.linalg.norm(states[:, :2] - target[:2], axis=1)
    within = errors <= tolerance
    if hold_steps <= 1:
        candidates = np.flatnonzero(within)
        return float(times[candidates[0]]) if candidates.size else None

    window = np.ones(int(hold_steps), dtype=int)
    streak = np.convolve(within.astype(int), window, mode="valid")
    candidates = np.flatnonzero(streak >= hold_steps)
    if candidates.size == 0:
        return None
    return float(times[candidates[0]])


def safety_violations(states: np.ndarray, bounds: SafetyBounds | Mapping[str, float] = SafetyBounds()) -> int:
    """Count samples outside a conservative safety envelope."""

    states = _to_array(states)
    if isinstance(bounds, Mapping):
        bounds = SafetyBounds(**bounds)
    x = states[:, 0]
    z = states[:, 1]
    violations = (x < bounds.x_min) | (x > bounds.x_max) | (z < bounds.z_min) | (z > bounds.z_max)
    return int(np.count_nonzero(violations))


def summarize_episode(
    rollout: Mapping[str, np.ndarray],
    tolerance: float = 0.15,
    hold_steps: int = 8,
    bounds: SafetyBounds | Mapping[str, float] = SafetyBounds(),
) -> Dict[str, float]:
    """Compute the standard metrics for a single rollout."""

    states = _to_array(rollout["states"])
    actions = _to_array(rollout["actions"])
    times = _to_array(rollout["times"])
    targets = _to_array(rollout["targets"])
    dt = float(rollout.get("dt", times[1] - times[0] if times.size > 1 else 0.0))

    errors = position_error(states, targets)
    position_rmse = rmse(errors)
    final_error = float(np.linalg.norm(errors[-1])) if errors.size else 0.0
    result = {
        "position_rmse": position_rmse,
        "final_error": final_error,
        "energy_cost": energy_cost(actions, dt),
        "safety_violations": float(safety_violations(states, bounds)),
        "total_reward": float(np.sum(np.asarray(rollout.get("rewards", []), dtype=float))),
    }

    target_time = time_to_target(times, states, targets[-1], tolerance=tolerance, hold_steps=hold_steps)
    result["time_to_target"] = float(target_time) if target_time is not None else float("nan")
    result["settled"] = float(1.0 if target_time is not None else 0.0)
    result["peak_altitude"] = float(np.max(states[:, 1])) if states.size else 0.0
    result["peak_horizontal_error"] = float(np.max(np.abs(errors[:, 0]))) if errors.size else 0.0
    return result


def aggregate_metrics(results: Mapping[str, Sequence[Mapping[str, float]]]) -> Dict[str, Dict[str, float]]:
    """Aggregate per-episode metrics into mean/std summaries."""

    summary: Dict[str, Dict[str, float]] = {}
    for name, runs in results.items():
        if not runs:
            continue
        keys = sorted({key for run in runs for key in run.keys()})
        stats: Dict[str, float] = {}
        for key in keys:
            values = np.asarray([run.get(key, np.nan) for run in runs], dtype=float)
            finite = values[np.isfinite(values)]
            if finite.size == 0:
                stats[f"{key}_mean"] = float("nan")
                stats[f"{key}_std"] = float("nan")
            else:
                stats[f"{key}_mean"] = float(np.mean(finite))
                stats[f"{key}_std"] = float(np.std(finite))
        summary[name] = stats
    return summary


def format_metrics_table(summary: Mapping[str, Mapping[str, float]]) -> str:
    """Render a compact text table for terminal output."""

    if not summary:
        return "No metrics available."

    metric_keys = [
        "position_rmse_mean",
        "final_error_mean",
        "time_to_target_mean",
        "energy_cost_mean",
        "safety_violations_mean",
        "total_reward_mean",
    ]
    header = ["controller"] + [key.replace("_mean", "") for key in metric_keys]
    widths = [max(len(cell), 12) for cell in header]
    for name, stats in summary.items():
        widths[0] = max(widths[0], len(name))
        for idx, key in enumerate(metric_keys, start=1):
            widths[idx] = max(widths[idx], len(f"{stats.get(key, float('nan')):.3f}"))

    lines = []
    head = " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(header))
    lines.append(head)
    lines.append("-+-".join("-" * width for width in widths))
    for name, stats in summary.items():
        cells = [name.ljust(widths[0])]
        for idx, key in enumerate(metric_keys, start=1):
            value = stats.get(key, float("nan"))
            cells.append(f"{value:.3f}".ljust(widths[idx]))
        lines.append(" | ".join(cells))
    return "\n".join(lines)
