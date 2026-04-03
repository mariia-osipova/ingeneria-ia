clear; close all; clc;

dt = 0.01;
T = 10;
t = 0:dt:T;
n = numel(t);

g = 9.81;
m = 1.0;
L = 0.25;
drag = 0.08;

state = zeros(6, n);
% state = [x; z; theta; xdot; zdot; thetadot]
u_thrust = zeros(1, n);
u_torque = zeros(1, n);

for k = 1:n-1
    x = state(1, k);
    z = state(2, k);
    theta = state(3, k);
    xdot = state(4, k);
    zdot = state(5, k);
    thetadot = state(6, k);

    target_x = 1.5 * sin(0.35 * t(k));
    target_z = 1.0 + 0.35 * cos(0.25 * t(k));
    ex = target_x - x;
    ez = target_z - z;

    u_thrust(k) = m * (g + 2.0 * ez - 0.8 * zdot);
    theta_cmd = min(max(0.6 * ex - 0.25 * xdot, -0.5), 0.5);
    u_torque(k) = 4.0 * (theta_cmd - theta) - 0.8 * thetadot;

    xddot = (u_thrust(k) / m) * sin(theta) - drag * xdot;
    zddot = (u_thrust(k) / m) * cos(theta) - g - drag * zdot;
    thetaddot = u_torque(k) / (m * L^2 / 3);

    state(4, k + 1) = xdot + xddot * dt;
    state(5, k + 1) = zdot + zddot * dt;
    state(6, k + 1) = thetadot + thetaddot * dt;
    state(1, k + 1) = x + state(4, k + 1) * dt;
    state(2, k + 1) = z + state(5, k + 1) * dt;
    state(3, k + 1) = theta + state(6, k + 1) * dt;
end

figure('Color', 'w');
subplot(2, 2, 1);
plot(state(1, :), state(2, :), 'LineWidth', 1.6);
axis equal;
xlabel('x [m]');
ylabel('z [m]');
title('Planar Trajectory');
grid on;

subplot(2, 2, 2);
plot(t, state(3, :), 'LineWidth', 1.6);
ylabel('\theta [rad]');
title('Pitch');
grid on;

subplot(2, 2, 3);
plot(t, state(4, :), 'LineWidth', 1.6);
ylabel('xdot [m/s]');
grid on;

subplot(2, 2, 4);
plot(t, state(5, :), 'LineWidth', 1.6);
xlabel('time [s]');
ylabel('zdot [m/s]');
grid on;
