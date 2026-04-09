% Drone simulation — physics-based main entry point
addpath('utils');
addpath('utils/transformations');
addpath('utils/primitves');
addpath('quadrotor');

clc; close all;

% Initialize figure
init_figure();

% Physics-derived hover speed
% At hover:  4 * k * w_hover^2 = mass * g
%   w_hover = sqrt(mass * g / (4 * k))
%   With mass=1 kg, g=9.81, k=0.02  →  w_hover ≈ 11.07 rad/s
mass  = 1.0;
g     = 9.81;
k     = 0.02;
w_hover = sqrt(mass * g / (4 * k));   % ≈ 11.07 rad/s

% Create drone: resting on the ground
position    = [5, 5, 0];
orientation = [0, 0, 0];
uav = drone(position, orientation);

% Target altitude
z_target = 5.0;    % metres — drone will take off and hold this height

% Simulation parameters
dt = 0.02;           % time step (s)
blades_angles = [0, 0, 0, 0];

while true
  % Controller (sensors → motor commands)
  uav = controller(uav, z_target, dt);

  % Physics integration
  uav = physics_step(uav, dt);

  % Spin blade angle according to motor speed
  blades_angles += uav.motor_speeds * dt;

  % Render
  draw_drone(uav, uav.motor_speeds, blades_angles);
  drawnow;
  pause(dt);
end
