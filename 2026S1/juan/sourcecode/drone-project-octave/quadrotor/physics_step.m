function uav = physics_step(uav, dt)
  % Rigid-body physics for a cross-configuration quadrotor.
  %
  % Motor layout (body frame):
  %   motor 1 : +Y arm (front)   — CCW
  %   motor 2 : -X arm (left)    — CW
  %   motor 3 : -Y arm (back)    — CCW
  %   motor 4 : +X arm (right)   — CW
  %
  % State:  uav.state  = [x  y  z  phi  theta  psi]
  %         uav.vel    = [vx vy vz]
  %         uav.omega  = [p  q  r]   (body-frame angular rates)

  % Unpack
  phi   = uav.state(4);
  theta = uav.state(5);
  psi   = uav.state(6);

  vx = uav.vel(1);  vy = uav.vel(2);  vz = uav.vel(3);
  p  = uav.omega(1); q = uav.omega(2); r = uav.omega(3);

  w = uav.motor_speeds;  % [w1 w2 w3 w4]

  % Per-motor thrust
  % Thrust magnitude is always positive (propellers push air down regardless
  % of spin direction). Sign of w only matters for yaw reaction torque.
  F = uav.k * w.^2;   % always positive
  T = sum(F);

  % Rotation matrix (ZYX Euler: yaw → pitch → roll)
  cphi = cos(phi);   sphi = sin(phi);
  ct   = cos(theta); st   = sin(theta);
  cpsi = cos(psi);   spsi = sin(psi);

  % Third column of R (body-z in world frame) — thrust direction
  bz_x =  cpsi*st*cphi + spsi*sphi;
  bz_y =  spsi*st*cphi - cpsi*sphi;
  bz_z =  ct*cphi;

  % Linear dynamics
  ax = (T * bz_x - uav.kd_lin * vx) / uav.mass;
  ay = (T * bz_y - uav.kd_lin * vy) / uav.mass;
  az = (T * bz_z - uav.kd_lin * vz) / uav.mass - uav.g;

  uav.vel(1) += ax * dt;
  uav.vel(2) += ay * dt;
  uav.vel(3) += az * dt;

  uav.state(1) += uav.vel(1) * dt;
  uav.state(2) += uav.vel(2) * dt;
  uav.state(3) += uav.vel(3) * dt;

  % Torques in body frame
  L = uav.arm_len;

  % Roll  (τ_x): right arm (motor4, +X) vs left arm (motor2, -X)
  tau_phi   = L * (F(4) - F(2));

  % Pitch (τ_y): front arm (motor1, +Y) vs rear arm (motor3, -Y)
  tau_theta = L * (F(1) - F(3));

  % Yaw   (τ_z): propeller reaction torques — CCW props add +z, CW add -z
  %   motors 1,3 are CCW (+), motors 2,4 are CW (-)
  % Motor speeds are signed (CW motors have negative w), so w*|w| is already
  % negative for CW motors — sum all four directly (no alternating signs).
  tau_psi = uav.b_drag * ( w(1)*abs(w(1)) + w(2)*abs(w(2)) ...
                          + w(3)*abs(w(3)) + w(4)*abs(w(4)) );

  % Angular dynamics (simplified: no gyroscopic cross-coupling)
  dp = (tau_phi   - uav.kd_ang * p) / uav.Ixx;
  dq = (tau_theta - uav.kd_ang * q) / uav.Iyy;
  dr = (tau_psi   - uav.kd_ang * r) / uav.Izz;

  uav.omega(1) += dp * dt;
  uav.omega(2) += dq * dt;
  uav.omega(3) += dr * dt;

  uav.state(4) += uav.omega(1) * dt;
  uav.state(5) += uav.omega(2) * dt;
  uav.state(6) += uav.omega(3) * dt;

  % Ground constraint
  if uav.state(3) < 0
    uav.state(3) = 0;
    uav.vel      = [0, 0, 0];
    uav.omega    = [0, 0, 0];
  end

endfunction
