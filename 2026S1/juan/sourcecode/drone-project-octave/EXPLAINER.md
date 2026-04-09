# Drone Project — Technical Explainer

---

## Table of Contents

1. [Project overview](#1-project-overview)
2. [Quadrotor fundamentals](#2-quadrotor-fundamentals)
3. [What this simulation models (and what it doesn't)](#3-what-this-simulation-models-and-what-it-doesnt)
4. [GNU Octave](#4-gnu-octave)
5. [3D coordinates and state representation](#5-3d-coordinates-and-state-representation)
6. [Roll, Pitch, and Yaw](#6-roll-pitch-and-yaw)
7. [Homogeneous transformation matrices](#7-homogeneous-transformation-matrices)
8. [Project structure](#8-project-structure)
9. [File-by-file breakdown](#9-file-by-file-breakdown)
    - [main.m](#mainm)
    - [quadrotor/drone.m](#quadrotordronem)
    - [quadrotor/draw_drone.m](#quadrotordraw_dronem)
    - [quadrotor/physics_step.m](#quadrotorphysics_stepm)
    - [quadrotor/controller.m](#quadrotorcontrollerm)
    - [utils/transformations/translation3.m](#utilstransformationstranslation3m)
    - [utils/transformations/rotation3.m](#utilstransformationsrotation3m)
    - [utils/primitves/circle3.m](#utilsprimtvescircle3m)
    - [utils/frame.m](#utilsframem)
    - [utils/init_figure.m](#utilsinit_figurem)
    - [utils/clean_workspace.m](#utilsclean_workspacem)
10. [Visual output](#10-visual-output)
11. [Limitations](#11-limitations)
12. [Glossary](#12-glossary)
13. [Physics model — equations of motion](#13-physics-model--equations-of-motion)

---

## 1. Project overview

This project is a 3D visualization of a quadrotor drone, implemented in GNU Octave. It simulates drone flight using rigid-body physics and homogeneous transformation matrices to position and orient every geometric element in the scene.

The core topics it demonstrates:
- Representing a 3D object as a set of homogeneous coordinate vectors
- Composing rigid-body transforms (rotation + translation) as 4×4 matrix products
- Efficient animation via plot handle updates rather than re-rendering
- Quadrotor equations of motion: gravity, per-motor thrust, torques, and air drag

---

## 2. Quadrotor fundamentals

A quadrotor has 4 motors arranged in a cross or X configuration. Each motor spins a propeller that generates thrust. The vehicle steers by differentially adjusting motor speeds — no control surfaces needed.

To avoid net torque on the body, motors alternate spin direction:

```
        Motor 1 — CCW (FRONT)
             |
Motor 2 ---[BODY]--- Motor 4
 CW (LEFT)   |         CW (RIGHT)
        Motor 3 — CCW (BACK)
```

In `main.m`:
```matlab
blade_speed = [150, -150, 150, -150];  % deg/s, sign encodes direction
```

Basic motion control summary:

| Maneuver | Motor adjustment |
|---|---|
| Throttle up/down | All motors faster/slower |
| Roll | Differential left/right |
| Pitch | Differential front/back |
| Yaw | Differential CW vs CCW pairs |

Motor speeds are set in `main.m` and drive both the physics (thrust and torque) and the visual animation (blade ring spin and thrust arrow length).

The hover speed is derived analytically:
```matlab
w_hover = sqrt(mass * g / (4 * k))   % ≈ 11.07 rad/s with default params
```
Setting all motors to `w_hover` produces exactly enough thrust to counteract gravity.

---

## 3. What this simulation models (and what it doesn't)

The drone's trajectory is determined by physics integration each frame. The simulation:

- Draws a geometrically correct drone shape in 3D
- Integrates rigid-body equations of motion driven by motor speeds
- Runs a closed-loop controller that reads simulated sensors and adjusts motor speeds each frame
- Holds a target altitude and stabilises roll/pitch/yaw to zero
- Animates spinning blade rings and thrust arrows
- Projects a shadow onto the ground plane (Z=0)

It does **not** model complex aerodynamics (blade flapping, ground effect, etc.) or external disturbances.

---

## 4. GNU Octave

GNU Octave is a free, open-source numerical computing environment compatible with MATLAB. Its native data type is the matrix, which makes it well-suited for this kind of transform-heavy 3D geometry code.

Run the project:
```bash
octave main.m
```

---

## 5. 3D coordinates and state representation

Points in this project are stored as 4-element homogeneous column vectors `[x, y, z, 1]'`. The trailing `1` enables both rotation and translation to be expressed as a single 4×4 matrix multiplication (see section 7).

The drone's state is a 6-element vector:
```
[x, y, z, roll, pitch, yaw]
```

World bounds: X and Y span \[-1, 10\], Z spans \[0, 10\]. The drone starts at `(5, 5, 1)`.

---

## 6. Roll, Pitch, and Yaw

Orientation is parameterized by three Euler angles (Tait-Bryan / ZYX convention):

- **Roll (φ)** — rotation around the X axis (tilt left/right)
- **Pitch (θ)** — rotation around the Y axis (tilt forward/back)
- **Yaw (ψ)** — rotation around the Z axis (heading)

These map directly to the `rotation3(phi, theta, psi)` function, which builds the combined rotation matrix as `Rz * Ry * Rx`.

---

## 7. Homogeneous transformation matrices

All geometry in this project is transformed using 4×4 homogeneous matrices. This is the standard approach in robotics and computer graphics for composing rotations and translations into a single linear operator.

### Translation

```matlab
translation3(x, y, z) =
| 1  0  0  x |
| 0  1  0  y |
| 0  0  1  z |
| 0  0  0  1 |
```

Multiplying this by `[px, py, pz, 1]'` yields `[px+x, py+y, pz+z, 1]'`.

### Rotation

`rotation3(phi, theta, psi)` builds the full 3D rotation as:

**Rx (roll):**
```
| 1      0       0    0 |
| 0   cos(φ)  sin(φ)  0 |
| 0  -sin(φ)  cos(φ)  0 |
| 0      0       0    1 |
```

**Ry (pitch):**
```
| cos(θ)   0  -sin(θ)  0 |
|    0      1     0    0 |
| sin(θ)   0   cos(θ)  0 |
|    0      0     0    1 |
```

**Rz (yaw):**
```
|  cos(ψ)  sin(ψ)  0  0 |
| -sin(ψ)  cos(ψ)  0  0 |
|    0        0    1  0 |
|    0        0    0  1 |
```

Combined: `R = Rz * Ry * Rx`

### Composing transforms

Multiple transforms can be multiplied into a single matrix before being applied to any geometry. For example, placing motor 1 (offset `arm_len` units in front of the drone body) at the drone's world pose:

```matlab
motor1_world = translation(drone_pos) * rotation(drone_angle) * translation(0, arm_len, 0) * local_point
```

Matrix multiplication is applied right-to-left: local offset → rotate by drone orientation → translate to world position. This is the pattern used throughout `drone.m` and `draw_drone.m`.

Since all geometry for a given element is stored as columns of one matrix, a single matrix multiply transforms every point simultaneously.

---

## 8. Project structure

```
drone-project-octave/
│
├── main.m                          ← Entry point. Simulation loop. Sets z_target.
│
├── quadrotor/
│   ├── drone.m                     ← Initializes the drone struct and draws it once
│   ├── draw_drone.m                ← Updates geometry each frame
│   ├── physics_step.m              ← Integrates equations of motion
│   └── controller.m                ← Sensor reading + PID altitude hold + attitude stabiliser
│
└── utils/
    ├── init_figure.m               ← Opens and configures the 3D figure window
    ├── frame.m                     ← Draws an RGB coordinate axis indicator
    ├── clean_workspace.m           ← Utility: clears Octave state
    ├── primitves/
    │   └── circle3.m               ← Generates a 3D circle (used for motor rings)
    └── transformations/
        ├── rotation3.m             ← Builds 4×4 rotation matrix from roll/pitch/yaw
        └── translation3.m          ← Builds 4×4 translation matrix from x/y/z
```

Execution flow:
```
main.m
  ├─ init_figure()       → configure 3D window and draw world frame
  ├─ drone()             → build drone struct, draw initial geometry
  └─ while true:
       ├─ controller()        (read sensors, compute motor speeds)
       ├─ physics_step()      (integrate equations of motion)
       └─ draw_drone()        (recompute and update all plot handles)
```

---

## 9. File-by-file breakdown

---

### `main.m`

```matlab
addpath('utils');
addpath('utils/transformations');
addpath('utils/primitves');
addpath('quadrotor');
```
Registers the subdirectories on Octave's function search path.

```matlab
position    = [5, 5, 0];
orientation = [0, 0, 0];
uav = drone(position, orientation);
z_target = 5.0;
```
Instantiates the drone on the ground at `(5, 5, 0)` with zero orientation. `z_target` is the altitude the drone will climb to and hold. Change this value to set a different hover height. `uav` is a struct containing geometry, physics state, controller state, and plot handles. Motor speeds are no longer set by hand — the controller computes them each frame.

```matlab
dt = 0.02;
```
Time step: 20 ms per frame → 50 Hz update rate.

```matlab
blades_angles = [0, 0, 0, 0];
```
`blades_angles` accumulates each motor's rotation over time (for visual animation only).

```matlab
while true
  uav = controller(uav, z_target, dt);
  uav = physics_step(uav, dt);
  blades_angles += uav.motor_speeds * dt;
  draw_drone(uav, uav.motor_speeds, blades_angles);
  drawnow;
  pause(dt);
```
Each iteration: the controller reads sensors and writes new motor speeds, physics integrates the resulting forces, blade angles accumulate for animation, then the frame is rendered. The controller always runs before the physics step so it acts on the current state.

---

### `quadrotor/drone.m`

Called once at startup. Builds the drone struct and issues the initial `plot3` calls.

```matlab
d_struct.state     = [position, orientation];
d_struct.arm_len   = 1;
d_struct.k         = 0.02;        % thrust coefficient  (N / (rad/s)^2)
d_struct.motor_diam = 0.3;

% Physics parameters (added)
d_struct.mass    = 1.0;           % kg
d_struct.g       = 9.81;          % m/s^2
d_struct.Ixx     = 0.02;          % roll  moment of inertia  (kg·m²)
d_struct.Iyy     = 0.02;          % pitch moment of inertia  (kg·m²)
d_struct.Izz     = 0.04;          % yaw   moment of inertia  (kg·m²)
d_struct.b_drag  = 0.001;         % propeller reaction-torque constant
d_struct.kd_lin  = 0.15;          % linear  air drag  (N·s/m)
d_struct.kd_ang  = 0.05;          % angular air drag  (N·m·s/rad)

d_struct.vel          = [0,0,0];  % linear  velocity [vx vy vz]
d_struct.omega        = [0,0,0];  % angular velocity [p  q  r ]
d_struct.motor_speeds = [0,0,0,0];
```
`k` is the thrust coefficient: `F = k * w²` per motor. `b_drag` is the propeller reaction-torque constant used for yaw. `kd_lin` / `kd_ang` damp translational and rotational motion to prevent runaway acceleration. `motor_diam` is relative to `arm_len`.

```matlab
d_struct.motor_blades = circle3(d_struct.motor_diam * d_struct.arm_len);
```
Pre-computes a 4×50 matrix of homogeneous circle points. Reused every frame.

```matlab
d = 0.05;
d_struct.drone_vertex = [
    [0, arm_len, arm_len, arm_len, 0, -arm_len, ...];   % X
    [0, arm_len, arm_len, arm_len, 0, -arm_len, ...];   % Y
    [0, 0, d, 0, 0, 0, d, ...];                          % Z
    [1, 1, 1, 1, 1, 1, ...];                             % homogeneous
];
```
Body vertices as a 4×N matrix. The small `d` offset in Z adds visual thickness to the body frame. Storing points column-wise allows a single matrix multiply to transform all of them.

```matlab
t = translation3(d_struct.state(1), d_struct.state(2), d_struct.state(3));
r = rotation3(d_struct.state(4), d_struct.state(5), d_struct.state(6));
d_struct.drone_vertex = t * r * d_struct.drone_vertex;
```
Applies the initial pose transform to all body vertices in one operation.

Motor placement uses chained transforms:
- Motor 1: `t * r * translation3(0, arm_len, 0) * rotation3(0,0,pi/4)` → front (+Y), 45° arm rotation
- Motor 2: left (-X)
- Motor 3: back (-Y)
- Motor 4: right (+X)

The 45° rotation aligns the arm orientation with the standard quadrotor X-frame layout.

```matlab
d_struct.body   = plot3(...);
d_struct.motor1 = plot3(...);
...
```
`plot3` returns a handle to the drawn line object. Saving these handles into the struct allows `draw_drone` to update geometry with `set(handle, 'xdata', ..., 'ydata', ..., 'zdata', ...)` — significantly faster than deleting and re-plotting each frame.

```matlab
d_struct.shadow_body = plot3(..., 0 * d_struct.drone_vertex(3,:));
```
Shadow is the body with all Z coordinates zeroed — a ground-plane projection.

---

### `quadrotor/draw_drone.m`

Called every frame. Recomputes world-space geometry from the current state and updates plot handles.

```matlab
t = translation3(uav.state(1), uav.state(2), uav.state(3));
r = rotation3(uav.state(4), uav.state(5), uav.state(6));
```
Rebuild the pose matrices from the current state.

```matlab
new_thrust1 = [[0,0,0,1]; [0,0, -uav.k * angular_vel1 * abs(angular_vel1), 1]]';
```
Thrust arrow: a line from `[0,0,0]` to `[0,0, -k*w*|w|]`. The `w * |w|` form gives `w²` with the correct sign. The arrow points down in the local frame — after applying the world transform (which includes the drone's orientation), it ends up pointing upward relative to the world for a level drone.

```matlab
f1 = t * r * translation3(0, uav.arm_len, 0) * rotation3(0, 0, pi/4);
motor1 = f1 * rotation3(0, 0, -angle1) * [uav.motor_blades, ...];
```
`f1` is the combined placement matrix for motor 1. The motor ring points are rotated by the accumulated blade angle before being placed, producing the spinning animation. Motor direction sign matches `blade_speed` sign.

```matlab
set(uav.body, 'xdata', drone_vertex(1,:), 'ydata', drone_vertex(2,:), 'zdata', drone_vertex(3,:));
set(uav.shadow_body, 'xdata', drone_vertex(1,:), 'ydata', drone_vertex(2,:), 'zdata', 0*drone_vertex(3,:));
```
In-place update of the existing plot objects. The shadow reuses the XY coordinates with Z forced to zero.

```matlab
x_axe = t * rotation3(0, 0, pi/4) * [0, 0.5; 0, 0; 0, 0; 1, 1];
```
The body frame indicator (RGB axis arrows at the drone center) is rotated 45° to align with the arm directions.

---

### `quadrotor/physics_step.m`

Called once per frame before `draw_drone`. Integrates the rigid-body equations of motion using forward Euler and writes the result back into the `uav` struct.

**Thrust**

Each motor produces a thrust force proportional to its speed squared:
```
F_i = k * w_i²
```
Thrust magnitude is always positive — propellers push air downward regardless of spin direction. Total thrust `T = F1 + F2 + F3 + F4`.

**World-frame force**

The thrust acts along the drone's body Z axis. To find the world-frame direction, the third column of the ZYX rotation matrix is used:
```
bz = [ cos(ψ)sin(θ)cos(φ) + sin(ψ)sin(φ),
       sin(ψ)sin(θ)cos(φ) − cos(ψ)sin(φ),
       cos(θ)cos(φ) ]
```
Linear acceleration including gravity and linear drag:
```
a = (T * bz − kd_lin * v) / mass − [0, 0, g]
```

**Torques (body frame)**

| Axis | Source | Expression |
|---|---|---|
| Roll (X) | right arm vs left arm | `L * (F4 − F2)` |
| Pitch (Y) | front arm vs rear arm | `L * (F1 − F3)` |
| Yaw (Z) | propeller reaction torques | `b * (w1\|w1\| + w2\|w2\| + w3\|w3\| + w4\|w4\|)` |

Motor speeds are **signed**: CCW motors (1, 3) have positive `w`, CW motors (2, 4) have negative `w`. Because `w*|w|` is already negative for CW motors, all four terms are summed with `+` (no alternating signs). With symmetric hover speeds the sum is zero and yaw torques cancel.

Angular acceleration including angular drag:
```
α = (τ − kd_ang * ω) / I
```

**Integration**

Simple forward Euler: `v += a*dt`, `pos += v*dt`, `ω += α*dt`, `angle += ω*dt`.

**Ground constraint**

If `z < 0`, position is clamped to 0 and all velocities are zeroed (inelastic ground collision).

---

### `quadrotor/controller.m`

Called once per frame **before** `physics_step`. Reads simulated sensors, computes the four motor speeds needed to hold altitude and keep the drone level, and writes them into `uav.motor_speeds`.

**Simulated sensors**

| Sensor | Source field | What it measures |
|---|---|---|
| Altimeter | `uav.state(3)` | Current height `z` (m) |
| IMU | `uav.state(4:6)` | Roll `φ`, pitch `θ`, yaw `ψ` (rad) |
| Gyroscope | `uav.omega` | Body angular rates `p, q, r` (rad/s) |
| Barometer / vel | `uav.vel(3)` | Vertical velocity `vz` (m/s) — used as altitude-rate derivative |

**Altitude PID**

Drives `z` toward `z_target`:
```
ez         = z_target − z
integral  += ez * dt          (clamped ±5 to prevent windup)
dw_total   = Kp_z * ez  +  Ki_z * integral  −  Kd_z * vz
```
`dw_total` is added to the base hover speed for all four motors uniformly (throttle channel).

**Attitude PD**

Drives roll, pitch, and yaw back to zero using body-rate feedback as the derivative term:
```
dw_phi   = −(Kp_att * φ  +  Kd_att * p)
dw_theta = −(Kp_att * θ  +  Kd_att * q)
dw_psi   = −(Kp_yaw * ψ  +  Kd_yaw * r)
```

**Motor mixing**

The three correction signals are combined using the torque relations of the quadrotor:

```
w_base = max(2, w_hover + dw_total)

motor1 (front CCW) =  w_base + dw_theta + dw_psi
motor2 (left  CW)  = −(w_base − dw_phi  − dw_psi)
motor3 (back  CCW) =  w_base − dw_theta + dw_psi
motor4 (right CW)  = −(w_base + dw_phi  − dw_psi)
```

Negative signs on motors 2 and 4 encode their CW spin direction. `w_base` is floored at 2 rad/s to prevent motor stall.

**Controller gains (defaults)**

| Gain | Value | Role |
|---|---|---|
| `Kp_z` | 1.5 | Altitude proportional |
| `Ki_z` | 0.3 | Altitude integral (removes steady-state offset) |
| `Kd_z` | 2.5 | Altitude derivative (damps oscillation) |
| `Kp_att` | 7.0 | Roll/pitch proportional |
| `Kd_att` | 2.5 | Roll/pitch derivative |
| `Kp_yaw` | 4.0 | Yaw proportional |
| `Kd_yaw` | 2.0 | Yaw derivative |

---

### `utils/transformations/translation3.m`

```matlab
function t = translation3(x, y, z)
  t = [eye(3), [x, y, z]'; [0, 0, 0, 1]];
endfunction
```

Constructs the standard 4×4 homogeneous translation matrix. `eye(3)` is the 3×3 identity.

---

### `utils/transformations/rotation3.m`

```matlab
function r = rotation3(phi, th, psi)
  rot_x = [1, 0, 0; 0, cos(phi), sin(phi); 0, -sin(phi), cos(phi)];
  rot_y = [cos(th), 0, -sin(th); 0, 1, 0; sin(th), 0, cos(th)];
  rot_z = [cos(psi), sin(psi), 0; -sin(psi), cos(psi), 0; 0, 0, 1];
  r = [rot_z * rot_y * rot_x, [0,0,0]'; [0,0,0,1]];
endfunction
```

Builds the full rotation matrix using ZYX Tait-Bryan convention: roll first, then pitch, then yaw (`Rz * Ry * Rx`). Padded to 4×4 with zeros in the translation column/row and a `1` in the bottom-right corner.

---

### `utils/primitves/circle3.m`

```matlab
function c = circle3(r)
  n = 50;
  angle = linspace(0, 2*pi, n);
  c = [[r*cos(angle); r*sin(angle); zeros(1,n)]; ones(1,n)];
endfunction
```

Returns a 4×50 matrix of homogeneous points on a circle of radius `r` in the XY plane. Used as the template for all four motor rings — the same circle is placed at each motor's position via the frame transform.

---

### `utils/frame.m`

```matlab
function f = frame(origin, orientation)
  norm = 0.5;
  x_axe = [0, norm; 0, 0; 0, 0; 1, 1];
  y_axe = [0, 0; 0, norm; 0, 0; 1, 1];
  z_axe = [0, 0; 0, 0; 0, norm; 1, 1];

  r = rotation3(orientation(1), orientation(2), orientation(3));
  t = translation3(origin(1), origin(2), origin(3));

  x_axe = t * r * x_axe;
  ...
  f.x_vec = plot3(..., 'Color', 'r');
  f.y_vec = plot3(..., 'Color', 'g');
  f.z_vec = plot3(..., 'Color', 'b');
endfunction
```

Draws a coordinate axis indicator at a given origin and orientation. Each axis is a line segment from the origin to 0.5 units along that axis direction. Used for the static world frame at `(0,0,0)` and the body frame attached to the drone.

---

### `utils/init_figure.m`

```matlab
function init_figure()
  figure('Name', 'Quadrotor', 'NumberTitle', 'off');
  hold on;
  title("Drone simulation");
  xlabel('X'); ylabel('Y'); zlabel('Z');
  grid on;
  view(45, 20);
  axis([-1, 10, -1, 10, 0, 10]);
  axis equal;
  frame([0,0,0], [0,0,0]);
  disp("World is loaded");
endfunction
```

- `hold on` — required to accumulate multiple `plot3` calls on the same axes
- `view(45, 20)` — camera azimuth 45°, elevation 20°
- `axis equal` — uniform scale across all three axes

---

### `utils/clean_workspace.m`

```matlab
clc; clf; clear; close all;
```

Convenience utility for interactive development. Clears terminal output, figure, variables, and all windows. Not used during simulation.

---

## 10. Visual output

Running `octave main.m` opens a 3D figure with:

| Element | Description | Color |
|---|---|---|
| 3 arrows at origin | Fixed world coordinate frame | Red=X, Green=Y, Blue=Z |
| X-cross wireframe | Drone body/arms | Gray |
| 4 circular rings | Motor propeller rings (animated) | Red (front), Blue (left), Green (back), Magenta (right) |
| Lines at each motor | Thrust arrows, length ∝ speed² | Orange |
| 3 arrows at drone center | Body frame indicator (moves with drone) | Red=X, Green=Y, Blue=Z |
| Ground-plane outline | Shadow projection at Z=0 | Black |

The drone traces a figure-8 (Lissajous) path in XY while oscillating in Z and rotating continuously in yaw. The shadow on the ground makes the horizontal trajectory easy to follow.

---

## 11. Limitations

| Aspect | Reality | This project |
|---|---|---|
| Physics | Gravity, aerodynamics, inertia | Gravity + thrust + linear/angular drag ✓ |
| Control | PID or other controller | Altitude PID + attitude PD ✓ |
| Motor dynamics | Speed changes affect trajectory | Recomputed every frame by controller ✓ |
| Gyroscopic effect | Spinning rotors resist attitude change | Not modelled |
| Blade aerodynamics | Flapping, induced drag, ground effect | Not modelled |
| Collision | Detectable via geometry | Ground plane only (z ≥ 0 clamp) |
| Sensors | GPS, IMU | None |
| Disturbances | Wind, turbulence | None |

---
<!-- 
## 12. Glossary

| Term | Meaning |
|---|---|
| **UAV** | Unmanned Aerial Vehicle |
| **Quadrotor** | Drone with 4 rotors |
| **Thrust** | Upward force from spinning propellers |
| **Torque reaction** | Rotational force on the body caused by a spinning motor; cancelled by opposite-spin motor pairs |
| **State vector** | `[x, y, z, roll, pitch, yaw]` — full pose descriptor |
| **Roll / Pitch / Yaw** | Rotation around X / Y / Z axis respectively |
| **Euler angles** | Parameterization of 3D orientation as three sequential axis rotations |
| **Tait-Bryan ZYX** | Specific Euler convention: yaw applied first, then pitch, then roll |
| **Homogeneous coordinates** | Appending a `1` to a 3D point so rotation and translation unify into a single 4×4 matrix multiplication |
| **Transformation matrix** | 4×4 matrix encoding rotation and/or translation |
| **Lissajous curve** | Parametric curve formed by composing two sinusoids at different frequencies |
| **Plot handle** | Reference to an existing Octave/MATLAB graphics object; use `set(handle, ...)` to update it in-place |
| **`drawnow`** | Flushes the graphics queue and renders the current frame |
| **`dt`** | Simulation time step (seconds per loop iteration) |
| **`struct`** | Octave/MATLAB data container grouping named fields |
| **`eye(3)`** | 3×3 identity matrix |
| **CCW / CW** | Counter-clockwise / Clockwise |
| **Thrust coefficient k** | Constant relating motor speed to thrust: `F = k * w²` |
| **Reaction torque** | Torque exerted on the drone body by a spinning propeller (opposite to spin direction); used to control yaw |
| **Moment of inertia (I)** | Resistance to angular acceleration; analogous to mass for rotation |
| **Forward Euler** | Simplest numerical integration method: `x(t+dt) = x(t) + dx/dt * dt` |
| **Air drag** | Velocity-proportional force/torque opposing motion; stabilises the simulation |
| **Body frame** | Coordinate system fixed to the drone; Z points up through the drone's top |
| **World frame** | Fixed global coordinate system; Z points straight up |
| **`physics_step`** | Function that advances the simulation by one time step using the equations of motion |

--- -->

## 13. Physics model — equations of motion

This section consolidates the full rigid-body model implemented in `physics_step.m`.

---

### State variables

| Symbol | Code | Meaning |
|---|---|---|
| `x, y, z` | `uav.state(1:3)` | World-frame position (m) |
| `φ, θ, ψ` | `uav.state(4:6)` | Roll, pitch, yaw (rad) |
| `vx, vy, vz` | `uav.vel` | World-frame linear velocity (m/s) |
| `p, q, r` | `uav.omega` | Body-frame angular rates (rad/s) |
| `w₁…w₄` | `uav.motor_speeds` | Motor angular speeds (rad/s) |

---

### Motor thrust

Each motor produces thrust proportional to its speed squared:

```
F_i = k · w_i²
```

Thrust is always positive — the sign of `w_i` only matters for yaw reaction torque. Total thrust:

```
T = F₁ + F₂ + F₃ + F₄
```

---

### World-frame thrust direction

Thrust acts along the drone's body Z axis. The body-Z direction in world coordinates is the third column of the ZYX rotation matrix `R = Rz·Ry·Rx`:

```
bz = [ cos(ψ)·sin(θ)·cos(φ) + sin(ψ)·sin(φ) ]
     [ sin(ψ)·sin(θ)·cos(φ) − cos(ψ)·sin(φ) ]
     [ cos(θ)·cos(φ)                          ]
```

---

### Linear dynamics

Newton's second law in the world frame, including gravity and linear air drag:

```
a = (T · bz − kd_lin · v) / mass − [0, 0, g]
```

Forward Euler integration:

```
v   += a  · dt
pos += v  · dt
```

---

### Torques (body frame)

Motor layout (`L` = arm length):

| Axis | Torque | Expression |
|---|---|---|
| Roll (X) | right arm vs left arm | `τ_φ = L · (F₄ − F₂)` |
| Pitch (Y) | front arm vs rear arm | `τ_θ = L · (F₁ − F₃)` |
| Yaw (Z) | propeller reaction torques | `τ_ψ = b · (w₁|w₁| + w₂|w₂| + w₃|w₃| + w₄|w₄|)` |

Motor speeds are signed: CCW motors (1, 3) have positive `w`, CW motors (2, 4) have negative `w`. `w·|w|` is already negative for CW motors, so all four terms are summed with `+`. At symmetric hover speeds, the sum is zero and yaw torques cancel exactly.

---

### Angular dynamics

Euler's equation for rigid-body rotation (gyroscopic coupling ignored):

```
α = (τ − kd_ang · ω) / I
```

Applied per axis with the respective moment of inertia (`Ixx`, `Iyy`, `Izz`):

```
ω     += α · dt
angle += ω · dt
```

---

### Ground constraint

Inelastic collision: if `z < 0`, position is clamped to zero and all linear and angular velocities are zeroed.

```matlab
if uav.state(3) < 0
  uav.state(3) = 0;
  uav.vel      = [0, 0, 0];
  uav.omega    = [0, 0, 0];
end
```

---

### Physical parameters (defaults)

| Parameter | Symbol | Value | Meaning |
|---|---|---|---|
| `mass` | m | 1.0 kg | Total drone mass |
| `g` | g | 9.81 m/s² | Gravitational acceleration |
| `k` | k | 0.02 N/(rad/s)² | Thrust coefficient |
| `b_drag` | b | 0.001 N·m·s²/rad² | Propeller reaction-torque constant |
| `kd_lin` | — | 0.15 N·s/m | Linear air drag coefficient |
| `kd_ang` | — | 0.05 N·m·s/rad | Angular air drag coefficient |
| `Ixx, Iyy` | — | 0.02 kg·m² | Roll / pitch moment of inertia |
| `Izz` | — | 0.04 kg·m² | Yaw moment of inertia |

Hover speed (all four motors equal, net vertical force = 0):

```
w_hover = sqrt(mass · g / (4 · k))  ≈ 11.07 rad/s
```
