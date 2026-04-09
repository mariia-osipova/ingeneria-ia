% Draw a coordinnate system at the origin with the given orientation
% origin shape : 1x3, orientation shape : 1x3
function f = frame(origin, orientation)
  % Unit vector norm
  norm = 0.5;
  x_axe = [0, norm; 0, 0; 0, 0; 1, 1];
  y_axe = [0, 0; 0, norm; 0, 0; 1, 1];
  z_axe = [0, 0; 0, 0; 0, norm; 1, 1];

  % Perform homogeneous transformation
  r = rotation3(orientation(1), orientation(2), orientation(3));
  t = translation3(origin(1), origin(2), origin(3));

  % transform each axes
  x_axe = t * r * x_axe;
  y_axe = t * r * y_axe;
  z_axe = t * r * z_axe;

  % Create plot which correspond to each computed axes
  f.x_vec = plot3(x_axe(1,:), x_axe(2,:), x_axe(3,:), 'Color', 'r', 'Linewidth', 1.5);
  f.y_vec = plot3(y_axe(1,:), y_axe(2,:), y_axe(3,:), 'Color', 'g', 'Linewidth', 1.5);
  f.z_vec = plot3(z_axe(1,:), z_axe(2,:), z_axe(3,:), 'Color', 'b', 'Linewidth', 1.5);

endfunction