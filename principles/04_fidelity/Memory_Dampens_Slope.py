import numpy as np
import matplotlib.pyplot as plt

# Simulate entropy over 10 steps with Memory present
steps = 10
entropy = [1.0]
slope = [0]  # initial slope

memory_strength = 0.5  # how strongly Memory resists change

for i in range(1, steps):
    # Raw perturbation
    perturb = np.random.uniform(0.8, 1.2)
    
    # Memory dampens the perturbation based on previous slope
    dampened = perturb * (1 - memory_strength * slope[-1])
    
    # Update entropy and slope
    new_entropy = entropy[-1] + dampened
    entropy.append(new_entropy)
    slope.append(dampened)

# Plot with dual y-axes
fig, ax1 = plt.subplots(figsize=(8, 5))

# Entropy curve (black)
ax1.plot(range(steps), entropy, color='black', linewidth=2, label='Entropy')
ax1.set_xlabel("Step")
ax1.set_ylabel("Entropy", color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Slope curve (blue)
ax2 = ax1.twinx()
ax2.plot(range(steps), slope, color='blue', linewidth=2, label='Slope')
ax2.set_ylabel("Slope", color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# Title and legend
plt.title("Memory present. Slope dampened. Identity preserved.")
fig.legend(loc="upper left", bbox_to_anchor=(0.5, 0.9))
plt.grid(True)
plt.tight_layout()
plt.show()
