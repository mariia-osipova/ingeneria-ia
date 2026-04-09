import numpy as np

# Target position (x, z) in metres
TARGET = (5.0, 5.0)

# Simulation
DT = 0.02          # timestep (s)  →  50 Hz
MAX_STEPS = 400    # 8 seconds per episode
N_EPISODES = 8

# Drone physics
MASS = 1.0         # kg
G = 9.81           # m/s²
KD_LIN = 0.15      # linear air drag (N·s/m)
K_THRUST = 0.02    # thrust coefficient

# Hover thrust (vertical force to cancel gravity)
F_HOVER = MASS * G  # = 9.81 N

# PID gains — altitude (z)
KP_Z = 9.0
KI_Z = 1.0
KD_Z = 5.0

# PID gains — horizontal (x)
KP_X = 3.5
KI_X = 0.2
KD_X = 4.0

# Settled threshold (m from target)
SETTLE_THRESHOLD = 0.3

# Noise levels (std of Gaussian added to observations)
NOISE_LEVELS = [0.0, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0]
