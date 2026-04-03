clear; close all; clc;

dt = 0.01;
T = 10;
t = 0:dt:T;
n = numel(t);

g = 9.81;
m = 1.0;
z_ref = 1.2;

gains = [6.0, 1.4, 2.2];
kp = gains(1);
ki = gains(2);
kd = gains(3);

z = zeros(1, n);
zdot = zeros(1, n);
thrust = zeros(1, n);
err = zeros(1, n);
integral = 0;
prev_err = 0;

for k = 1:n-1
    err(k) = z_ref - z(k);
    integral = integral + err(k) * dt;
    deriv = (err(k) - prev_err) / dt;
    u = m * (g + kp * err(k) + ki * integral + kd * deriv);
    thrust(k) = max(0, u);

    zddot = thrust(k) / m - g;
    zdot(k + 1) = zdot(k) + zddot * dt;
    z(k + 1) = z(k) + zdot(k + 1) * dt;
    prev_err = err(k);
end

err(end) = z_ref - z(end);
rmse_value = sqrt(mean(err .^ 2));
max_overshoot = max(0, max(z) - z_ref);

tol = 0.02 * max(1, abs(z_ref));
settling_idx = find(abs(z - z_ref) > tol, 1, 'last');
if isempty(settling_idx)
    settling_time = 0;
elseif settling_idx >= numel(t)
    settling_time = t(end);
else
    settling_time = t(settling_idx + 1);
end

metrics = struct();
metrics.rmse = rmse_value;
metrics.max_overshoot = max_overshoot;
metrics.settling_time = settling_time;
metrics.energy = sum(abs(thrust) * dt);

figure('Color', 'w');
subplot(3, 1, 1);
plot(t, z, 'LineWidth', 1.6); hold on;
plot([t(1), t(end)], [z_ref, z_ref], '--', 'LineWidth', 1.2);
ylabel('z [m]');
title('Altitude PID');
grid on;

subplot(3, 1, 2);
plot(t, err, 'LineWidth', 1.6);
ylabel('error [m]');
grid on;

subplot(3, 1, 3);
plot(t, thrust, 'LineWidth', 1.6);
xlabel('time [s]');
ylabel('thrust [N]');
grid on;

disp(metrics);
