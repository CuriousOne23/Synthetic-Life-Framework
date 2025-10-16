import numpy as np
import matplotlib.pyplot as plt

# Time range
t = np.arange(0, 50)

# Silence levels
silence_levels = {
    "Short Silence": 1,
    "Medium Silence": 5,
    "Long Silence": 10
}

# Identity curves
identity_curves = {}

for label, sil in silence_levels.items():
    M = np.exp(-t / (10 + sil))  # Memory decay
    C = np.log(1 + sil * t / 10)  # Choice growth
    G = 1 / (1 + np.exp(-(t - 25) / sil))  # Governance sigmoid
    I = 0.4 * M + 0.3 * C + 0.3 * G  # Weighted identity
    identity_curves[label] = I

# Plotting
plt.figure(figsize=(10, 6))
for label, I in identity_curves.items():
    plt.plot(t, I, label=label)

plt.title("Effect of Silence Duration on Identity Over Time")
plt.xlabel("Time (Events)")
plt.ylabel("Identity (I)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Silent_Identity_Curves.png")
plt.show()
