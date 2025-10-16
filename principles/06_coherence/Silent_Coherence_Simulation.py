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

# Coherence curves
coherence_curves = {}

for label, sil in silence_levels.items():
    # Avoid division by zero
    decay_factor = 10 + sil if sil > 0 else 10
    sigmoid_factor = sil if sil > 0 else 1

    # Compute M, C, G
    M = np.exp(-t / decay_factor)
    C = np.log(1 + sil * t / 10) if sil > 0 else np.zeros_like(t)
    G = 1 / (1 + np.exp(-(t - 25) / sigmoid_factor))
    I = 0.4 * M + 0.3 * C + 0.3 * G

    # Compute coherence as inverse of local std deviation
    coherence = []
    for i in range(len(I)):
        if i < 4:
            coherence.append(0)  # Not enough data for window
        else:
            window = I[i-4:i+1]
            std_dev = np.std(window)
            coherence.append(1 - std_dev)

    # Normalize coherence to [0, 1]
    coherence = np.array(coherence)
    coherence = (coherence - np.min(coherence)) / (np.max(coherence) - np.min(coherence))
    coherence_curves[label] = coherence

# Plotting
plt.figure(figsize=(10, 6))
for label, coh in coherence_curves.items():
    plt.plot(t, coh, label=label)

plt.title("Derived Coherence from Identity Under Varying Silence")
plt.xlabel("Time (Events)")
plt.ylabel("Coherence")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("coherence_from_identity_silence.png")
plt.show()
