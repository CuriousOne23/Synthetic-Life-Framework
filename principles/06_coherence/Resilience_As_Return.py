import numpy as np
import matplotlib.pyplot as plt

# Time domain
T = 100
t = np.linspace(0, T, T)

# Perturbations
def impulse(t, location=50, magnitude=1):
    impulse_array = np.zeros_like(t)
    idx = (np.abs(t - location)).argmin()
    impulse_array[idx] = magnitude
    return impulse_array


def sinusoidal(t, freq=0.1, amplitude=1):
    return amplitude * np.sin(2 * np.pi * freq * t)

def noise(t, seed=42, scale=0.5):
    np.random.seed(seed)
    return scale * np.random.normal(size=len(t))

# Identity response function
def identity_response(perturbation, memory=1.0, choice=1.0, governance=1.0):
    I = np.zeros_like(t)
    for i in range(1, len(t)):
        damping = memory * choice * governance
        I[i] = I[i-1] + damping * (perturbation[i] - I[i-1])
    return I

# Models
perturbations = {
    "Impulse": impulse(t),
    "Sinusoidal": sinusoidal(t),
    "Noise": noise(t)
}

models = {
    "I_full": (1.0, 1.0, 1.0),
    "I_no_memory": (0.0, 1.0, 1.0),
    "I_no_choice": (1.0, 0.0, 1.0),
    "I_no_governance": (1.0, 1.0, 0.0)
}

# Plotting
fig, axs = plt.subplots(len(perturbations), 1, figsize=(10, 8.5))  # Slightly reduced height
fig.suptitle("Resilience as Return — Identity Under Perturbation", fontsize=14)

for idx, (label, P) in enumerate(perturbations.items()):
    axs[idx].plot(t, P, 'k--', linewidth=3, label='Perturbation')  # Thicker perturbation line
    for model_name, (m, c, g) in models.items():
        I = identity_response(P, memory=m, choice=c, governance=g)
        axs[idx].plot(t, I, label=model_name)
    axs[idx].set_title(f"{label} Perturbation", pad=14)  # More space above title
    axs[idx].set_ylabel("Identity")
    axs[idx].set_xlabel("Time", labelpad=18)  # More space below X-axis label
    axs[idx].legend()

plt.tight_layout(rect=[0, 0, 1, 0.94])  # Slightly more top margin
plt.show()