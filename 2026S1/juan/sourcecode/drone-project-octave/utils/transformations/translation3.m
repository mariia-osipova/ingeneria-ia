function t = translation3(x, y, z)
  % Pack the homogeneous translation matrix
  t = [
    eye(3), [x, y, z]'; [0, 0, 0, 1]
  ];
endfunction

