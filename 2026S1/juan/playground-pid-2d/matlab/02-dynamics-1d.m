clear; close all; clc;

dt = 0.01;
T = 8;
t = 0:dt:T;
n = numel(t);

g = 9.81;
m = 1.0;

z = zeros(1, n);
zdot = zeros(1, n);
thrust = zeros(1, n);

for k = 1:n-1
    if t(k) < 1.0
        thrust(k) = m * g;
    elseif t(k) < 4.0
        thrust(k) = 1.15 * m * g;
    else
        thrust(k) = 0.92 * m * g;
    end

    zddot = thrust(k) / m - g;
    zdot(k+1) = zdot(k) + zddot * dt;
    z(k+1) = z(k) + zdot(k) * dt;
end

figure('Color', 'w');
subplot(3, 1, 1);
plot(t, z, 'LineWidth', 1.6);
ylabel('z [m]');
title('1D Vertical Dynamics');
grid on;

subplot(3, 1, 2);
plot(t, zdot, 'LineWidth', 1.6);
ylabel('v_z [m/s]');
grid on;

subplot(3, 1, 3);
plot(t, thrust, 'LineWidth', 1.6);
xlabel('time [s]');
ylabel('thrust [N]');
grid on;
