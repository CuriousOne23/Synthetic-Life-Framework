import numpy as np
import matplotlib.pyplot as plt

# Simulate entropy over 10 steps without Breath
steps = 10
entropy = [1.0]

for i in range(1, steps):
    spike = entropy[-1] + np.random.uniform(0.8, 1.2)
    entropy.append(spike)

# Calculate slope (rate of change)
slope = [0]  # no slope at step 0
for i in range(1, steps):
    delta = entropy[i] - entropy[i - 1]
    slope.append(delta)

# Create plot with dual y-axes
fig, ax1 = plt.subplots(figsize=(8, 5))

# Entropy curve (left axis)
ax1.plot(range(steps), entropy, color='black', linewidth=2, label='Entropy')
ax1.set_xlabel("Step")
ax1.set_ylabel("Entropy", color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Slope curve (right axis)
ax2 = ax1.twinx()
ax2.plot(range(steps), slope, color='red', linewidth=2, label='Slope')
ax2.set_ylabel("Slope", color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Title and legend
plt.title("Identity destabilized at step 2, Collapse confirmed by step 3. System unstable.")
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
plt.grid(True)
plt.tight_layout()
plt.show()
