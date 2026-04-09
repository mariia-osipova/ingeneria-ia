function draw_drone(uav, u, blades_angles)
  % Unpack control vector
  angular_vel1 = u(1);
  angular_vel2 = u(2);
  angular_vel3 = u(3);
  angular_vel4 = u(4);

  % Unpack angular position
  angle1 = blades_angles(1);
  angle2 = blades_angles(2);
  angle3 = blades_angles(3);
  angle4 = blades_angles(4);

  %  Compute actual position and orientation of the drone
  t = translation3(uav.state(1),uav.state(2),uav.state(3));
  r = rotation3(uav.state(4),uav.state(5),uav.state(6));

  %  Compute all thrust
  new_thrust1 = [[0,0,0,1];[0,0,-uav.k*angular_vel1*abs(angular_vel1),1]]';
  new_thrust2 = [[0,0,0,1];[0,0,-uav.k*angular_vel2*abs(angular_vel2),1]]';
  new_thrust3 = [[0,0,0,1];[0,0,-uav.k*angular_vel3*abs(angular_vel3),1]]';
  new_thrust4 = [[0,0,0,1];[0,0,-uav.k*angular_vel4*abs(angular_vel4),1]]';

  % Compute the new thrust vectors and motors placement
  f1 = t * r * translation3(0,uav.arm_len,0) * rotation3(0,0,pi/4);
  f2 = t * r * translation3(-uav.arm_len,0,0) * rotation3(0,0,pi/4);
  f3 = t * r * translation3(0,-uav.arm_len,0) * rotation3(0,0,pi/4);
  f4 = t * r * translation3(uav.arm_len,0,0) * rotation3(0,0,pi/4);

  % Draw the drone vertex with new position and orientation
  drone_vertex = [
    [uav.arm_len, -uav.arm_len, 0, 0, 0];
    [0, 0, 0, uav.arm_len, -uav.arm_len];
    [0, 0, 0, 0, 0];
    [1, 1, 1, 1, 1]
   ];

  % Compute the drone body placement
  drone_vertex = t * r * drone_vertex;

  % Update all homogeneous matrices
  thrust1 = f1 * new_thrust1;
  thrust2 = f2 * new_thrust2;
  thrust3 = f3 * new_thrust3;
  thrust4 = f4 * new_thrust4;

  motor1 =  f1 * rotation3(0,0,-angle1) * [uav.motor_blades, [uav.motor_diam*uav.arm_len 0 0 1]', [-uav.motor_diam*uav.arm_len 0 0 1]'];
  motor2 =  f2 * rotation3(0,0,angle2) * [uav.motor_blades, [uav.motor_diam*uav.arm_len 0 0 1]', [-uav.motor_diam*uav.arm_len 0 0 1]'];
  motor3 =  f3 * rotation3(0,0,-angle3) * [uav.motor_blades, [uav.motor_diam*uav.arm_len 0 0 1]', [-uav.motor_diam*uav.arm_len 0 0 1]'];
  motor4 =  f4 * rotation3(0,0,angle4) * [uav.motor_blades, [uav.motor_diam*uav.arm_len 0 0 1]', [-uav.motor_diam*uav.arm_len 0 0 1]'];

  % Set all drawn element with x, y and z new coordinate

  % Drone coordinate system
  x_axe = t * rotation3(0,0,pi/4) * [0, 0.5; 0, 0; 0, 0; 1, 1];
  y_axe = t * rotation3(0,0,pi/4) * [0, 0; 0, 0.5; 0, 0; 1, 1];
  z_axe = t * rotation3(0,0,pi/4) * [0, 0; 0, 0; 0, 0.5; 1, 1];

  set(uav.drone_frame.x_vec, 'xdata', x_axe(1, :), 'ydata', x_axe(2, :), 'zdata', x_axe(3, :));
  set(uav.drone_frame.y_vec, 'xdata', y_axe(1, :), 'ydata', y_axe(2, :), 'zdata', y_axe(3, :));
  set(uav.drone_frame.z_vec, 'xdata', z_axe(1, :), 'ydata', z_axe(2, :), 'zdata', z_axe(3, :));

  % Drone body
  set(uav.body, 'xdata', drone_vertex(1, :), 'ydata', drone_vertex(2, :), 'zdata', drone_vertex(3, :));
  set(uav.motor1, 'xdata', motor1(1, :), 'ydata', motor1(2, :), 'zdata', motor1(3, :));
  set(uav.motor2, 'xdata', motor2(1, :), 'ydata', motor2(2, :), 'zdata', motor2(3, :));
  set(uav.motor3, 'xdata', motor3(1, :), 'ydata', motor3(2, :), 'zdata', motor3(3, :));
  set(uav.motor4, 'xdata', motor4(1, :), 'ydata', motor4(2, :), 'zdata', motor4(3, :));

  % Thrust vectors
  set(uav.thrust1, 'xdata', thrust1(1, :), 'ydata', thrust1(2, :), 'zdata', thrust1(3, :));
  set(uav.thrust2, 'xdata', thrust2(1, :), 'ydata', thrust2(2, :), 'zdata', thrust2(3, :));
  set(uav.thrust3, 'xdata', thrust3(1, :), 'ydata', thrust3(2, :), 'zdata', thrust3(3, :));
  set(uav.thrust4, 'xdata', thrust4(1, :), 'ydata', thrust4(2, :), 'zdata', thrust4(3, :));

  % Shadow
  set(uav.shadow_body, 'xdata', drone_vertex(1, :), 'ydata', drone_vertex(2, :), 'zdata',0*drone_vertex(3, :));
  set(uav.shadow_motor1, 'xdata', motor1(1, :), 'ydata', motor1(2, :), 'zdata', 0*motor1(3, :));
  set(uav.shadow_motor2, 'xdata', motor2(1, :), 'ydata', motor2(2, :), 'zdata', 0*motor2(3, :));
  set(uav.shadow_motor3, 'xdata', motor3(1, :), 'ydata', motor3(2, :), 'zdata', 0*motor3(3, :));
  set(uav.shadow_motor4, 'xdata', motor4(1, :), 'ydata', motor4(2, :), 'zdata', 0*motor4(3, :));

endfunction

