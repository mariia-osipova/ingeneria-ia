"""Entry point for the PID vs RL vs Hybrid drone comparison.

The repository uses a simplified planar model, but the structure mirrors the
project brief: run a PID baseline, a lightweight RL-style learner, and a hybrid
controller; evaluate position RMSE, time-to-target, energy cost, and safety
violations; then save plots and a concise text summary.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable

from hybrid import HybridController, build_default_pid
from metrics import aggregate_metrics, format_metrics_table, summarize_episode
from rl_agent import DroneConfig, DroneEnv, evaluate_controller, run_episode, train_linear_policy
from visualize import plot_metrics_bars, plot_trajectory_comparison


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare PID, RL, and hybrid drone controllers.")
    parser.add_argument("--episodes", type=int, default=4, help="number of evaluation scenarios")
    parser.add_argument("--train-episodes", type=int, default=6, help="scenarios used to score each RL candidate")
    parser.add_argument("--candidates", type=int, default=24, help="policy candidates explored during RL search")
    parser.add_argument("--steps", type=int, default=600, help="maximum simulation steps per episode")
    parser.add_argument("--seed", type=int, default=7, help="random seed")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"), help="where to store plots and summaries")
    parser.add_argument("--no-save", action="store_true", help="print results without writing files")
    parser.add_argument("--no-wind", action="store_true", help="disable wind disturbances")
    return parser


def build_env(args: argparse.Namespace) -> DroneEnv:
    config = DroneConfig(wind_enabled=not args.no_wind)
    config.max_time = float(args.steps) * config.dt
    return DroneEnv(config=config, seed=args.seed)


def build_scenarios(env: DroneEnv, count: int, seed: int) -> list[tuple]:
    scenarios = []
    for offset in range(count):
        scenarios.append(env.sample_scenario(seed=seed + offset * 101))
    return scenarios


def flatten_rollouts(rollouts):
    return [rollout.as_dict() for rollout in rollouts]


def controller_name(controller) -> str:
    return controller.__class__.__name__


def run_experiment(args: argparse.Namespace) -> tuple[dict, dict[str, list[dict]], dict[str, object]]:
    env = build_env(args)
    scenarios = build_scenarios(env, args.episodes, args.seed)

    pid = build_default_pid()
    rl_policy = train_linear_policy(
        env,
        seed=args.seed,
        candidates=args.candidates,
        episodes=args.train_episodes,
        max_steps=args.steps,
    )
    hybrid = HybridController(pid=build_default_pid(), rl_policy=rl_policy)

    controllers = {
        "PID": pid,
        "RL": rl_policy,
        "Hybrid": hybrid,
    }

    raw_runs: dict[str, list[dict]] = {}
    per_controller_metrics: dict[str, list[dict]] = {}

    for name, controller in controllers.items():
        runs = evaluate_controller(env, controller, scenarios, max_steps=args.steps)
        raw_runs[name] = [run.as_dict() for run in runs]
        per_controller_metrics[name] = [
            summarize_episode(run.as_dict(), tolerance=env.config.target_tolerance, hold_steps=env.config.hold_steps)
            for run in runs
        ]

    summary = aggregate_metrics(per_controller_metrics)
    artifacts = {"controllers": controllers, "env": env, "scenarios": scenarios}
    return summary, raw_runs, artifacts


def save_artifacts(args: argparse.Namespace, summary, raw_runs) -> None:
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    representative_runs = {name: runs[0] for name, runs in raw_runs.items() if runs}
    plot_trajectory_comparison(representative_runs, output_path=args.output_dir / "trajectories.png")
    plot_metrics_bars(summary, output_path=args.output_dir / "rmse.png", metric="position_rmse_mean")
    plot_metrics_bars(summary, output_path=args.output_dir / "reward.png", metric="total_reward_mean", title="Average total reward")


def main(argv: list[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)
    summary, raw_runs, _ = run_experiment(args)
    print(format_metrics_table(summary))
    if not args.no_save:
        save_artifacts(args, summary, raw_runs)
        print(f"\nSaved outputs to: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
