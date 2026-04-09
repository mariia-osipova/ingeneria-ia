# PID drone — take off and hold 5 m

**Mariia Osipova · April 2026**

---

## What we built

Two implementations of the same thing: a drone that takes off and holds a target altitude of 5 metres using a PID controller.

- **Octave** — 3D animated simulation with rigid-body physics and spinning blades. Run with `octave main.m`.
- **Python** — 2D benchmark that runs PID, RL, and a Hybrid controller and compares how they do.

---

## How the PID loop works

Each timestep:

```
read altitude z  →  error = 5.0 − z  →  PID → Δw  →  motor speeds  →  thrust  →  physics  ↺
```

`Δw` is added to the hover speed for all four motors uniformly (throttle channel).

Hover speed is derived from physics: `w_hover = sqrt(m·g / 4k) ≈ 11.07 rad/s`

| Gain | Value | Role |
|---|---|---|
| Kp_z | 1.5 | Proportional — push toward target |
| Ki_z | 0.3 | Integral — removes steady-state error |
| Kd_z | 2.5 | Derivative — damps overshoot |

The Octave version also runs a PD attitude controller that keeps roll, pitch, and yaw at zero.

---

## Octave — 3D simulation

The drone starts at `(5, 5, 0)` and climbs to `z = 5.0`. Runs at 50 Hz (`dt = 0.02 s`).

**Physics:** gravity, per-motor thrust (`F = k·w²`), linear and angular air drag, forward Euler integration. Ground clamped at `z = 0`.

**Geometry:** everything uses 4×4 homogeneous transformation matrices. Each frame, all geometry is transformed via `T · R · local_point` and plot handles are updated in-place (no re-plotting).

**Files:**

```
main.m               ← simulation loop, sets z_target = 5.0
quadrotor/
  controller.m       ← altitude PID + attitude PD
  physics_step.m     ← equations of motion
  drone.m            ← drone struct + initial draw
  draw_drone.m       ← per-frame geometry update
utils/
  rotation3.m        ← 4×4 rotation matrix (ZYX Euler)
  translation3.m     ← 4×4 translation matrix
  circle3.m          ← motor ring geometry
```

**What you see in the window:**
- X-cross wireframe drone body
- 4 spinning motor rings (animated by accumulated blade angle)
- Thrust arrows at each motor, length proportional to w²
- RGB body frame indicator (moves with drone)
- Ground-plane shadow at Z = 0
- Fixed world frame at origin

---

## Python — 2D benchmark results

Same altitude task in 2D, three controllers, multiple episodes with varying sensor noise.

| Controller | Final error (m) | RMSE | Safety violations | Settled |
|---|---|---|---|---|
| **PID** | **0.03** | **0.25** | **0** | **100%** |
| RL | 4.9 | 2.5 | 42.8 avg | — |
| Hybrid | 6.7 | 5.9 | 15.3 avg | 0% |

PID reaches the target in ~1.67 s on average. RL and Hybrid are untrained at this point — these numbers are just the baseline before any learning happens.

**Output plots:** `playground-pid-2d/python/outputs/`
- `trajectories.png` — flight paths
- `reward.png` — reward over episodes
- `rmse.png` — position error across noise levels

---

## Key parameters

| Parameter | Value | Meaning |
|---|---|---|
| `z_target` | 5.0 m | Target altitude |
| `dt` | 0.02 s | Timestep (50 Hz) |
| `mass` | 1.0 kg | Drone mass |
| `k` | 0.02 N/(rad/s)² | Thrust coefficient |
| `w_hover` | ≈ 11.07 rad/s | Speed where thrust = gravity |
| `kd_lin` | 0.15 | Linear air drag |
| `kd_ang` | 0.05 | Angular air drag |

## Demo

<img src="/Users/maria/CLionProjects/ingeneria-ia/2026S1/juan/img/SR.gif" alt="Demo gif" />