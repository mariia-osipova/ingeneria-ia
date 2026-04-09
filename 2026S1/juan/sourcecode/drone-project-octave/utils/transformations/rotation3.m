function r = rotation3(phi, th, psi)
  % Compute rotation arround each axes (x, y and z)
  rot_x = [
    [1, 0, 0];
    [0, cos(phi), sin(phi)];
    [0, -sin(phi), cos(phi)];
  ];

  rot_y = [
    [cos(th), 0, -sin(th)];
    [0, 1, 0];
    [sin(th), 0, cos(th)]
  ];

  rot_z = [
    [cos(psi), sin(psi), 0];
    [-sin(psi), cos(psi), 0];
    [0, 0, 1];
  ];

  % Pack the homogeneous rotation matrix
  r = [rot_z * rot_y * rot_x, [0,0,0]'; [0,0,0,1]];
endfunction
