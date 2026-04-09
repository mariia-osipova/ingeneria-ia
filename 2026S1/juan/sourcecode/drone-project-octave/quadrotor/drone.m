function d_struct = drone(position, orientation)
  % Pack drone state vector
  d_struct.state = [position, orientation];
  d_struct.arm_len = 1;

  %  Drone thrust factor (N / (rad/s)^2)
  d_struct.k          = 0.02;
  d_struct.motor_diam = 0.3;

  % Physics parameters
  d_struct.mass    = 1.0;    % kg
  d_struct.g       = 9.81;   % m/s^2
  d_struct.Ixx     = 0.02;   % roll  moment of inertia (kg*m^2)
  d_struct.Iyy     = 0.02;   % pitch moment of inertia (kg*m^2)
  d_struct.Izz     = 0.04;   % yaw   moment of inertia (kg*m^2)
  d_struct.b_drag  = 0.001;  % propeller reaction-torque constant
  d_struct.kd_lin  = 0.15;   % linear  air drag (N*s/m)
  d_struct.kd_ang  = 0.05;   % angular air drag (N*m*s/rad)

  % Dynamic state (initialised at rest)
  d_struct.vel          = [0, 0, 0];   % linear  velocity [vx vy vz]  (m/s)
  d_struct.omega        = [0, 0, 0];   % angular velocity [p  q  r ]  (rad/s)
  d_struct.motor_speeds = [0, 0, 0, 0]; % rad/s (CCW positive)
  d_struct.err_z_int    = 0;           % altitude integral accumulator

  % Draw circle at the end of each arm (motors positionning)
  d_struct.motor_blades = circle3(d_struct.motor_diam*d_struct.arm_len);

  % Homogeenous matrix of a plus shaped drone
##  d_struct.drone_vertex = [
##    [d_struct.arm_len, -d_struct.arm_len, 0, 0, 0];
##    [0, 0, 0, d_struct.arm_len, -d_struct.arm_len];
##    [0, 0, 0, 0, 0];
##    [1, 1, 1, 1, 1]
##   ];
  d = 0.05;
  d_struct.drone_vertex = [
    [0, d_struct.arm_len, d_struct.arm_len, d_struct.arm_len, 0, -d_struct.arm_len, -d_struct.arm_len, -d_struct.arm_len, -d_struct.arm_len, 0, -d_struct.arm_len, -d_struct.arm_len, -d_struct.arm_len, -d_struct.arm_len, 0, d_struct.arm_len, d_struct.arm_len, d_struct.arm_len, d_struct.arm_len];
    [0, d_struct.arm_len, d_struct.arm_len, d_struct.arm_len, 0, -d_struct.arm_len, -d_struct.arm_len, -d_struct.arm_len, -d_struct.arm_len, 0, d_struct.arm_len, d_struct.arm_len, d_struct.arm_len, d_struct.arm_len, 0, -d_struct.arm_len, -d_struct.arm_len, -d_struct.arm_len, -d_struct.arm_len];
    [0, 0, d, 0, 0, 0, d, 0, 0, 0, 0, d, 0, 0, 0, 0, d, 0, 0];
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
   ];


  % Compute initial position and attitude of the drone according to the state vector
  t = translation3(d_struct.state(1), d_struct.state(2), d_struct.state(3));
  r = rotation3(d_struct.state(4), d_struct.state(5), d_struct.state(6));

  % Perform homogeneous translation and rotation
  d_struct.drone_vertex = t * r * d_struct.drone_vertex;

  % Construct the drone frame (x, y and z coordinate in the body frame)
  d_struct.drone_frame = frame([d_struct.state(1), d_struct.state(2), d_struct.state(3)],[d_struct.state(4), d_struct.state(5), pi/4]);

  % Draw body
  d_struct.body = plot3(d_struct.drone_vertex(1,:), d_struct.drone_vertex(2,:), d_struct.drone_vertex(3,:), 'Color', [0.69,0.69,0.69]);
  hold on;

  % Compute thrust vector
  thrust = [[0,0,0,1];[0,0,0,1]]';

  thrust1 = t * r * translation3(0,d_struct.arm_len,0) * rotation3(0,0,pi/4) * thrust;
  thrust2 = t * r * translation3(-d_struct.arm_len,0,0) * rotation3(0,0,pi/4) * thrust;
  thrust3 = t * r * translation3(0,-d_struct.arm_len,0) * rotation3(0,0,pi/4) * thrust;
  thrust4 = t * r * translation3(d_struct.arm_len,0,0) * rotation3(0,0,pi/4) * thrust;

  motor1 = t * r * translation3(0,d_struct.arm_len,0) * rotation3(0,0,pi/4) * [d_struct.motor_blades, [d_struct.motor_diam*d_struct.arm_len 0 0 1]', [-d_struct.motor_diam*d_struct.arm_len 0 0 1]'];
  motor2 = t * r * translation3(-d_struct.arm_len,0,0) * [d_struct.motor_blades, [d_struct.motor_diam*d_struct.arm_len 0 0 1]', [-d_struct.motor_diam*d_struct.arm_len 0 0 1]'];
  motor3 = t * r * translation3(0,-d_struct.arm_len,0) * [d_struct.motor_blades, [d_struct.motor_diam*d_struct.arm_len 0 0 1]', [-d_struct.motor_diam*d_struct.arm_len 0 0 1]'];
  motor4 = t * r * translation3(d_struct.arm_len,0,0) * [d_struct.motor_blades, [d_struct.motor_diam*d_struct.arm_len 0 0 1]', [-d_struct.motor_diam*d_struct.arm_len 0 0 1]'];

  d_struct.thrust1 = plot3(thrust1(1, :), thrust1(2, :), thrust1(3, :), 'Color', [1, 0.5,0], 'Linewidth', 2);
  d_struct.thrust2 = plot3(thrust2(1, :), thrust2(2, :), thrust2(3, :), 'Color', [1, 0.5,0], 'Linewidth', 2);
  d_struct.thrust3 = plot3(thrust3(1, :), thrust3(2, :), thrust3(3, :), 'Color', [1, 0.5,0], 'Linewidth', 2);
  d_struct.thrust4 = plot3(thrust4(1, :), thrust4(2, :), thrust4(3, :), 'Color', [1, 0.5,0], 'Linewidth', 2);

  d_struct.motor1 = plot3(motor1(1, :), motor1(2, :), motor1(3, :), 'Color', 'r', 'Linewidth', 1);
  d_struct.motor2 = plot3(motor2(1, :), motor2(2, :), motor2(3, :), 'Color', 'b', 'Linewidth', 1);
  d_struct.motor3 = plot3(motor3(1, :), motor3(2, :), motor3(3, :), 'Color', 'g', 'Linewidth', 1);
  d_struct.motor4 = plot3(motor4(1, :), motor4(2, :), motor4(3, :), 'Color', 'm', 'Linewidth', 1);

  d_struct.shadow_body = plot3(d_struct.drone_vertex(1,:), d_struct.drone_vertex(2,:), 0*d_struct.drone_vertex(3,:), 'Color', 'k');
  d_struct.shadow_motor1 = plot3(motor1(1, :), motor1(2, :), 0*motor1(3, :), 'Color', 'k');
  d_struct.shadow_motor2 =  plot3(motor2(1, :), motor2(2, :), 0*motor2(3, :), 'Color', 'k');
  d_struct.shadow_motor3 =  plot3(motor3(1, :), motor3(2, :), 0*motor3(3, :), 'Color', 'k');
  d_struct.shadow_motor4 =  plot3(motor4(1, :), motor4(2, :), 0*motor4(3, :), 'Color', 'k');

endfunction

