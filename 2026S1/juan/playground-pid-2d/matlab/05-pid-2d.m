clear; close all; clc;

setenv('GNUTERM', 'qt');
toolkits = available_graphics_toolkits();
if any(strcmp(toolkits, 'gnuplot'))
    graphics_toolkit('gnuplot');
end

dt = 0.01;
T = 15;
t = 0:dt:T;
n = numel(t);

params.g = 9.81;
params.m = 1.0;
params.L = 0.25;
params.drag = 0.05;
params.wind_amp = 0.15;
params.wind_freq = 0.9;

waypoints = [0.0, 0.9;
             1.2, 1.1;
             2.0, 1.0;
             2.0, 1.3];

gains.outer = [1.2, 0.0, 0.45];
gains.inner = [12.0, 1.6, 3.0];

state = zeros(6, n);
theta_cmd = zeros(1, n);
thrust = zeros(1, n);

waypoint_idx = 1;
x_target = waypoints(1, 1);
z_target = waypoints(1, 2);
outer_integral = 0;
inner_integral = 0;
prev_outer_err = 0;
prev_inner_err = 0;

for k = 1:n-1
    x = state(1, k);
    z = state(2, k);
    theta = state(3, k);
    xdot = state(4, k);
    zdot = state(5, k);
    thetadot = state(6, k);

    if waypoint_idx < rows(waypoints)
        if norm([x - x_target, z - z_target]) < 0.15
            waypoint_idx = waypoint_idx + 1;
            x_target = waypoints(waypoint_idx, 1);
            z_target = waypoints(waypoint_idx, 2);
        end
    end

    wind = params.wind_amp * sin(params.wind_freq * t(k));

    ex = x_target - x;
    outer_integral = outer_integral + ex * dt;
    outer_deriv = (ex - prev_outer_err) / dt;
    theta_cmd(k) = min(max(gains.outer(1) * ex + gains.outer(2) * outer_integral + gains.outer(3) * outer_deriv, -0.55), 0.55);
    prev_outer_err = ex;

    ez = z_target - z;
    inner_integral = inner_integral + ez * dt;
    inner_deriv = (ez - prev_inner_err) / dt;
    thrust(k) = params.m * (params.g + 2.2 * ez + 0.8 * inner_integral + 1.0 * inner_deriv - 0.4 * zdot);
    thrust(k) = max(0.1, thrust(k));
    prev_inner_err = ez;

    torque = 6.0 * (theta_cmd(k) - theta) - 0.8 * thetadot;
    xddot = (thrust(k) / params.m) * sin(theta) - params.drag * xdot + wind;
    zddot = (thrust(k) / params.m) * cos(theta) - params.g - params.drag * zdot;
    thetaddot = torque / (params.m * params.L ^ 2 / 3);

    state(4, k + 1) = xdot + xddot * dt;
    state(5, k + 1) = zdot + zddot * dt;
    state(6, k + 1) = thetadot + thetaddot * dt;
    state(1, k + 1) = x + state(4, k + 1) * dt;
    state(2, k + 1) = z + state(5, k + 1) * dt;
    state(3, k + 1) = theta + state(6, k + 1) * dt;
end

theta_cmd(end) = theta_cmd(end - 1);
thrust(end) = thrust(end - 1);

target_path = interp1(linspace(0, t(end), rows(waypoints)), waypoints, t, 'linear', 'extrap');
pos = state(1:2, :).';
target = target_path(:, 1:2);
diff_xy = pos - target;
err = sqrt(sum(diff_xy .^ 2, 2));

metrics = struct();
metrics.rmse = sqrt(mean(err .^ 2));
metrics.max_radius = max(sqrt(sum(pos .^ 2, 2)));
metrics.safety_violations = sum(abs(state(1, :)) > 3 | state(2, :) < 0);

if ~isempty(toolkits)
    figure('Color', 'w');
    subplot(2, 2, 1);
    plot(state(1, :), state(2, :), 'LineWidth', 1.6); hold on;
    plot(waypoints(:, 1), waypoints(:, 2), 'ro--', 'LineWidth', 1.2);
    axis equal;
    xlabel('x [m]');
    ylabel('z [m]');
    title('Waypoint Tracking');
    grid on;

    subplot(2, 2, 2);
    plot(t, state(3, :), 'LineWidth', 1.6);
    ylabel('\theta [rad]');
    grid on;

    subplot(2, 2, 3);
    plot(t, thrust, 'LineWidth', 1.6);
    ylabel('thrust [N]');
    grid on;

    subplot(2, 2, 4);
    plot(t, theta_cmd, 'LineWidth', 1.6);
    xlabel('time [s]');
    ylabel('\theta_{cmd} [rad]');
    grid on;

    figure('Color', 'w');
    axis equal;
    x_margin = 0.8;
    z_margin = 0.8;
    xmin = min([state(1, :), waypoints(:, 1)']) - x_margin;
    xmax = max([state(1, :), waypoints(:, 1)']) + x_margin;
    zmin = min([state(2, :), waypoints(:, 2)']) - z_margin;
    zmax = max([state(2, :), waypoints(:, 2)']) + z_margin;
    axis([xmin, xmax, zmin, zmax]);
    xlabel('x [m]');
    ylabel('z [m]');
    title('Drone Animation');
    grid on;
    hold on;
    plot(waypoints(:, 1), waypoints(:, 2), 'ro--', 'LineWidth', 1.0);
    trajectory_plot = plot(state(1, 1), state(2, 1), 'b-', 'LineWidth', 1.0);
    body_plot = plot([0, 0], [0, 0], 'k-', 'LineWidth', 3.0);
    rotor_left = plot(0, 0, 'bo', 'MarkerFaceColor', 'b', 'MarkerSize', 6);
    rotor_right = plot(0, 0, 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 6);
    center_plot = plot(0, 0, 'ks', 'MarkerFaceColor', 'k', 'MarkerSize', 5);

    arm_half = params.L;
    frame_skip = max(1, floor(n / 300));
    for k = 1:frame_skip:n
        x = state(1, k);
        z = state(2, k);
        theta = state(3, k);
        dx = arm_half * cos(theta);
        dz = arm_half * sin(theta);

        set(trajectory_plot, 'XData', state(1, 1:k), 'YData', state(2, 1:k));
        set(body_plot, 'XData', [x - dx, x + dx], 'YData', [z - dz, z + dz]);
        set(rotor_left, 'XData', x - dx, 'YData', z - dz);
        set(rotor_right, 'XData', x + dx, 'YData', z + dz);
        set(center_plot, 'XData', x, 'YData', z);
        drawnow();
        pause(0.01);
    end
else
    disp('No Octave graphics toolkit available. Skipping plots.');
end

disp(metrics);
