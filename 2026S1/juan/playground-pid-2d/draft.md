# Playground PID 2D

Minimal project for comparing drone control strategies:

- `02-dynamics-1d.m`: vertical motion with gravity and thrust
- `03-dynamics-2d.m`: planar drone model with `x`, `z`, and pitch
- `04-pid-1d.m`: altitude PID tuning
- `05-pid-2d.m`: waypoint tracking with cascaded PID
- `06-tuning-experiments.m`: gain sweeps and disturbance tests

## Goals

- Show basic drone dynamics with a simple physics model
- Tune PID gains and observe overshoot, settling time, and steady-state error
- Compare tracking with and without wind/disturbances
- Produce plots that make the effect of each controller visible

## Metrics

- RMSE on position tracking
- Maximum overshoot
- Settling time
- Control effort
- Safety violations when the state leaves a soft bound

## How To Run

Open MATLAB in `matlab/` and run the scripts in order:

1. `01-intro-notes.md` for the project summary
2. `02-dynamics-1d.m` for the vertical dynamics baseline
3. `04-pid-1d.m` for altitude control
4. `03-dynamics-2d.m` for the planar model
5. `05-pid-2d.m` for waypoint tracking
6. `06-tuning-experiments.m` for parameter sweeps

Each script is standalone and generates its own figures.
