clear; close all; clc;

dt = 0.01;
T = 8;
t = 0:dt:T;
n = numel(t);
z_ref = 1.0;

g = 9.81;
m = 1.0;
kp_values = [3, 5, 7, 9];
kd_values = [0.5, 1.0, 1.5];

results = zeros(numel(kp_values), numel(kd_values));
rmse_grid = zeros(size(results));

for i = 1:numel(kp_values)
    for j = 1:numel(kd_values)
        gains = [kp_values(i), 0.6, kd_values(j)];
        kp = gains(1);
        ki = gains(2);
        kd = gains(3);

        z = zeros(1, n);
        zdot = zeros(1, n);
        err = zeros(1, n);
        integral = 0;
        prev_err = 0;

        for k = 1:n-1
            err(k) = z_ref - z(k);
            integral = integral + err(k) * dt;
            deriv = (err(k) - prev_err) / dt;
            thrust = max(0, m * (g + kp * err(k) + ki * integral + kd * deriv));
            zddot = thrust / m - g;
            zdot(k + 1) = zdot(k) + zddot * dt;
            z(k + 1) = z(k) + zdot(k + 1) * dt;
            prev_err = err(k);
        end

        err(end) = z_ref - z(end);
        results(i, j) = max(z) - z_ref;
        rmse_grid(i, j) = sqrt(mean(err .^ 2));
    end
end

figure('Color', 'w');
subplot(1, 2, 1);
imagesc(kd_values, kp_values, results);
set(gca, 'YDir', 'normal');
xlabel('K_d');
ylabel('K_p');
title('Overshoot');
colorbar;

subplot(1, 2, 2);
imagesc(kd_values, kp_values, rmse_grid);
set(gca, 'YDir', 'normal');
xlabel('K_d');
ylabel('K_p');
title('RMSE');
colorbar;

nominal_err = zeros(1, n);
wind_err = zeros(1, n);

for case_idx = 1:2
    if case_idx == 1
        wind_amp = 0.0;
    else
        wind_amp = 0.15;
    end

    z = zeros(1, n);
    zdot = zeros(1, n);
    integral = 0;
    prev_err = 0;
    err = zeros(1, n);

    for k = 1:n-1
        err(k) = z_ref - z(k);
        integral = integral + err(k) * dt;
        deriv = (err(k) - prev_err) / dt;
        thrust = max(0, m * (g + 6 * err(k) + 1.0 * integral + 2.0 * deriv));
        wind = wind_amp * sin(1.3 * t(k));
        zddot = thrust / m - g + wind;
        zdot(k + 1) = zdot(k) + zddot * dt;
        z(k + 1) = z(k) + zdot(k + 1) * dt;
        prev_err = err(k);
    end

    err(end) = z_ref - z(end);
    if case_idx == 1
        nominal_err = err;
    else
        wind_err = err;
    end
end

rmse_nominal = sqrt(mean(nominal_err .^ 2));
rmse_wind = sqrt(mean(wind_err .^ 2));
disp(struct('rmse_nominal', rmse_nominal, 'rmse_wind', rmse_wind));
