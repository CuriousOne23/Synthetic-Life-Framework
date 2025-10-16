import numpy as np
import matplotlib.pyplot as plt

# Time range
t = np.arange(0, 50)

# Silence levels including 0
silence_levels = {
    "No Silence": 0,
    "Short Silence": 1,
    "Medium Silence": 5,
    "Long Silence": 10
}

# Identity curves
identity_curves = {}

for label, sil in silence_levels.items():
    # Avoid division by zero
    decay_factor = 10 + sil if sil > 0 else 10
    sigmoid_factor = sil if sil > 0 else 1

    M = np.exp(-t / decay_factor)  # Memory decay
    C = np.log(1 + sil * t / 10) if sil > 0 else np.zeros_like(t)  # Choice growth
    G = 1 / (1 + np.exp(-(t - 25) / sigmoid_factor))  # Governance sigmoid
    I = 0.4 * M + 0.3 * C + 0.3 * G  # Weighted identity
    identity_curves[label] = I

# Plotting
plt.figure(figsize=(10, 6))
for label, I in identity_curves.items():
    plt.plot(t, I, label
