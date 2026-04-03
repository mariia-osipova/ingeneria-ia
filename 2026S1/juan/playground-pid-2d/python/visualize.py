"""Visualization helpers for the drone control comparison."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence

import matplotlib

matplotlib.use("Agg", force=True)

import matplotlib.pyplot as plt
import numpy as np


def _ensure_path(path: str | Path | None) -> Path | None:
    if path is None:
        return None
    return Path(path)


def plot_trajectory_comparison(
    runs: Mapping[str, Mapping[str, np.ndarray]],
    *,
    output_path: str | Path | None = None,
    title: str = "Drone control comparison",
):
    """Plot x-z trajectories and time series for a set of controllers."""

    if not runs:
        raise ValueError("runs must not be empty")

    output_path = _ensure_path(output_path)
    fig, axes = plt.subplots(2, 2, figsize=(13, 9), constrained_layout=True)
    traj_ax, x_ax, z_ax, control_ax = axes.flat

    for name, rollout in runs.items():
        times = np.asarray(rollout["times"], dtype=float)
        states = np.asarray(rollout["states"], dtype=float)
        actions = np.asarray(rollout["actions"], dtype=float)
        targets = np.asarray(rollout["targets"], dtype=float)

        traj_ax.plot(states[:, 0], states[:, 1], label=name, linewidth=2)
        traj_ax.scatter([targets[-1, 0]], [targets[-1, 1]], marker="x", s=70)
        x_ax.plot(times, states[:, 0], label=name, linewidth=2)
        z_ax.plot(times, states[:, 1], label=name, linewidth=2)
        if actions.size:
            control_ax.plot(times[:-1], np.linalg.norm(actions, axis=1), label=name, linewidth=2)

    target = np.asarray(next(iter(runs.values()))["targets"])[-1]
    traj_ax.scatter([target[0]], [target[1]], color="black", marker="*", s=140, label="target")

    traj_ax.set_title("Planar trajectory")
    traj_ax.set_xlabel("x [m]")
    traj_ax.set_ylabel("z [m]")
    traj_ax.grid(True, alpha=0.3)
    traj_ax.legend()

    x_ax.set_title("Horizontal position")
    x_ax.set_xlabel("time [s]")
    x_ax.set_ylabel("x [m]")
    x_ax.grid(True, alpha=0.3)

    z_ax.set_title("Altitude")
    z_ax.set_xlabel("time [s]")
    z_ax.set_ylabel("z [m]")
    z_ax.grid(True, alpha=0.3)

    control_ax.set_title("Control effort")
    control_ax.set_xlabel("time [s]")
    control_ax.set_ylabel("||action||")
    control_ax.grid(True, alpha=0.3)

    fig.suptitle(title)
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=160)
    return fig


def plot_metrics_bars(
    summary: Mapping[str, Mapping[str, float]],
    *,
    output_path: str | Path | None = None,
    metric: str = "position_rmse_mean",
    title: str | None = None,
):
    if not summary:
        raise ValueError("summary must not be empty")

    output_path = _ensure_path(output_path)
    names = list(summary.keys())
    values = [float(summary[name].get(metric, float("nan"))) for name in names]
    fig, ax = plt.subplots(figsize=(9, 4.5), constrained_layout=True)
    bars = ax.bar(names, values, color=["#1f77b4", "#ff7f0e", "#2ca02c"][: len(names)])
    ax.set_ylabel(metric.replace("_", " "))
    ax.set_title(title or metric.replace("_", " ").title())
    ax.grid(True, axis="y", alpha=0.25)
    for bar, value in zip(bars, values, strict=False):
        ax.text(bar.get_x() + bar.get_width() / 2.0, bar.get_height(), f"{value:.3f}", ha="center", va="bottom")
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=160)
    return fig

