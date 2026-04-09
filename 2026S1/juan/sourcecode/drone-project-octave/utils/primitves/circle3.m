% radius of the circle
function c = circle3(r)
  % n is number of iteration
  n = 50;
  angle = linspace(0, 2*pi, n);
  x = r * cos(angle);
  y = r * sin(angle);
  z = zeros(1, n);
  c = [
    [x; y; z];
    ones(1, n);
  ];
endfunction


