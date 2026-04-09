import numpy as np
from config import DT, KP_Z, KI_Z, KD_Z, KP_X, KI_X, KD_X, F_HOVER


class PIDAxis:
    def __init__(self, kp, ki, kd, clamp=8.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.clamp = clamp
        self.integral = 0.0

    def update(self, error, derivative):
        self.integral += error * DT
        self.integral = float(np.clip(self.integral, -self.clamp, self.clamp))
        return self.kp * error + self.ki * self.integral - self.kd * derivative

    def reset(self):
        self.integral = 0.0


class PIDController:
    """
    Independent PID loops for x (horizontal) and z (altitude).
    Returns (fx, fz) forces to apply to the drone.
    """

    def __init__(self):
        self.pid_z = PIDAxis(KP_Z, KI_Z, KD_Z)
        self.pid_x = PIDAxis(KP_X, KI_X, KD_X)

    def reset(self):
        self.pid_z.reset()
        self.pid_x.reset()

    def act(self, obs_x, obs_z, vx, vz, target_x, target_z):
        fz = F_HOVER + self.pid_z.update(target_z - obs_z, vz)
        fx =          self.pid_x.update(target_x - obs_x, vx)
        fz = float(np.clip(fz, 0.0, 30.0))
        fx = float(np.clip(fx, -15.0, 15.0))
        return fx, fz
