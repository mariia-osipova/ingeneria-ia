import numpy as np
from config import MASS, G, KD_LIN, DT


class Drone2D:
    """
    2D point-mass drone (x horizontal, z vertical).
    Forces fx (horizontal) and fz (vertical thrust) are the control inputs.
    """

    def __init__(self, x=0.0, z=0.0):
        self.x = x
        self.z = z
        self.vx = 0.0
        self.vz = 0.0

    def reset(self, x=0.0, z=0.0):
        self.x = x
        self.z = z
        self.vx = 0.0
        self.vz = 0.0

    def step(self, fx, fz, noise_std=0.0):
        """
        Integrate one timestep.
        Returns noisy observation (obs_x, obs_z, vx, vz).
        """
        ax = (fx - KD_LIN * self.vx) / MASS
        az = (fz - KD_LIN * self.vz) / MASS - G

        self.vx += ax * DT
        self.vz += az * DT
        self.x  += self.vx * DT
        self.z  += self.vz * DT

        # ground
        if self.z < 0.0:
            self.z  = 0.0
            self.vz = 0.0

        obs_x = self.x + np.random.normal(0.0, noise_std) if noise_std > 0 else self.x
        obs_z = self.z + np.random.normal(0.0, noise_std) if noise_std > 0 else self.z

        return obs_x, obs_z, self.vx, self.vz

    @property
    def pos(self):
        return np.array([self.x, self.z])
