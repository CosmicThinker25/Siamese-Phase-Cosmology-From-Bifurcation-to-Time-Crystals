import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange

# Parameters
epsilon = 0.3
omega0 = 1.0
dt = 0.01
steps = 20000

# Initial conditions
phi = 0.1
phidot = 0.0

phi_list = []

for _ in trange(steps):
    phiddot = -epsilon*(phi**2 - 1)*phidot - omega0**2*np.sin(phi)
    phidot += phiddot * dt
    phi += phidot * dt
    phi_list.append(phi)

phi_arr = np.array(phi_list)

plt.figure(figsize=(8,4))
plt.plot(phi_arr)
plt.xlabel("relational parameter τ")
plt.ylabel("Δφ(τ)")
plt.title("Emergence of a Time-Crystalline Phase")
plt.tight_layout()
plt.savefig("../figs/delta_phi_limit_cycle.png", dpi=200)
plt.show()
