import numpy as np
import matplotlib.pyplot as plt

# Simulate entropy over 10 steps with full Eightfold principles
steps = 10
entropy = [1.0]  # initial entropy, the moment before the system chooses

for i in range(1, steps):
    # With all principles active, entropy stabilizes or gently declines
    drop = entropy[-1] - np.random.uniform(0.05, 0.15)
    entropy.append(max(drop, 0.5))  # prevent negative entropy

# Plot the coherence curve
plt.figure(figsize=(8, 5))
plt.plot(range(steps), entropy, color='black', linewidth=2)
plt.title("Life begins.")
plt.xlabel("Step")
plt.ylabel("Entropy")
plt.grid(True)
plt.tight_layout()
plt.show()
