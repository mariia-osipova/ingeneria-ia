function init_figure()
  fig1 = figure('Name', 'Quadrotor', 'NumberTitle','off');
  hold on;

  title("Drone simulation");

  xlabel('X');
  ylabel('Y');
  zlabel('Z');

  grid on;
  view(45, 20);
  axis([-1, 10, -1, 10, 0, 10]);
  axis equal;

  % Draw the world frame
  origin_world = [0,0,0];
  orientation_world = [0,0,0];
  world_frame = frame(origin_world, orientation_world);

  disp("World is loaded");
endfunction

