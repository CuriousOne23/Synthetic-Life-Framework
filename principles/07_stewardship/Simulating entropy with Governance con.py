# Simulating entropy with Governance constraint over 10 steps

import numpy as np
import matplotlib.pyplot as plt

# Parameters
steps = 10
entropy = [1.0]
slope = [0.0]  # initial slope is zero
max_delta = 0.2  # maximum allowed change in slope per step

# Simulation loop
for i in range(1, steps):
    raw_perturbation = np.random.uniform(-0.3, 0.3)  # unconstrained entropy change
    previous_slope = slope[-1]
    constrained_slope = np.clip(raw_perturbation, previous_slope - max_delta, previous_slope + max_delta)
    new_entropy = entropy[-1] + constrained_slope
    entropy.append(new_entropy)
    slope.append(constrained_slope)

# Plotting
plt.style.use('seaborn-v0_8')
plt.figure(figsize=(8, 5))
plt.plot(range(steps), entropy, color='black', linewidth=2, label='Entropy')
plt.plot(range(steps), slope, color='green', linewidth=2, label='Slope')
plt.title('Governance present. Volatility constrained. System coherent.')
plt.xlabel('Step')
plt.ylabel('Entropy / Slope')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("C:/Users/jeffg/OneDrive/Documents/Life/Python/governance_entropy_slope.png")
plt.show()
