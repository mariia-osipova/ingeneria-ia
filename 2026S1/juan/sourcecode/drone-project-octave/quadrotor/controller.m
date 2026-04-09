function uav = controller(uav, z_target, dt)
  % Attitude stabiliser + altitude hold for a cross-configuration quadrotor.
  %
  % Simulated sensors:
  %   Altimeter  → uav.state(3)          [z position, m]
  %   IMU        → uav.state(4:6)        [roll φ, pitch θ, yaw ψ, rad]
  %   Gyroscope  → uav.omega  [p q r, rad/s — body angular rates]
  %   Barometer  → uav.vel(3)            [vz, m/s]
  %
  % Outputs: uav.motor_speeds updated each call.
  %
  % Motor layout (body frame):
  %   w1 : +Y arm (front)  — CCW → positive speed
  %   w2 : -X arm (left)   — CW  → negative speed
  %   w3 : -Y arm (back)   — CCW → positive speed
  %   w4 : +X arm (right)  — CW  → negative speed

  % Hover speed (derived from physical parameters)
  w_hover = sqrt(uav.mass * uav.g / (4 * uav.k));

  % Controller gains
  % Altitude PID
  Kp_z  = 1.5;
  Ki_z  = 0.3;
  Kd_z  = 2.5;
  % Roll / pitch PD  (shared gains — symmetric airframe)
  Kp_att = 7.0;
  Kd_att = 2.5;
  % Yaw PD
  Kp_yaw = 4.0;
  Kd_yaw = 2.0;

  % Sensor readings
  z     = uav.state(3);
  phi   = uav.state(4);
  theta = uav.state(5);
  psi   = uav.state(6);
  vz    = uav.vel(3);
  p     = uav.omega(1);   % roll  rate
  q     = uav.omega(2);   % pitch rate
  r     = uav.omega(3);   % yaw   rate

  % Altitude PID
  ez = z_target - z;
  uav.err_z_int += ez * dt;
  uav.err_z_int  = max(-5, min(5, uav.err_z_int));   % anti-windup clamp

  dw_total = Kp_z * ez  +  Ki_z * uav.err_z_int  -  Kd_z * vz;

  % Attitude PD (target: φ=0, θ=0, ψ=0)
  dw_phi   = -(Kp_att * phi   + Kd_att * p);
  dw_theta = -(Kp_att * theta + Kd_att * q);
  dw_psi   = -(Kp_yaw * psi   + Kd_yaw * r);

  % Motor mixing
  %
  % Torque relations (linearised around w_base):
  %   tau_phi   = L*k*(|w4|^2 - |w2|^2)  ≈ 4*L*k*w_base * dw_phi
  %   tau_theta = L*k*(|w1|^2 - |w3|^2)  ≈ 4*L*k*w_base * dw_theta
  %   tau_psi   = b*(|w1|^2 - |w2|^2 + |w3|^2 - |w4|^2)
  %                                       ≈ 8*b*w_base   * dw_psi
  %
  % Mixing table:
  %   front (CCW+) :  w_base + dw_theta + dw_psi
  %   left  (CW-)  : -(w_base - dw_phi  - dw_psi)
  %   back  (CCW+) :  w_base - dw_theta + dw_psi
  %   right (CW-)  : -(w_base + dw_phi  - dw_psi)

  w_base = max(2, w_hover + dw_total);   % never stall motors

  uav.motor_speeds(1) =  (w_base + dw_theta + dw_psi);    % front CCW
  uav.motor_speeds(2) = -(w_base - dw_phi   - dw_psi);    % left  CW
  uav.motor_speeds(3) =  (w_base - dw_theta + dw_psi);    % back  CCW
  uav.motor_speeds(4) = -(w_base + dw_phi   - dw_psi);    % right CW

endfunction
