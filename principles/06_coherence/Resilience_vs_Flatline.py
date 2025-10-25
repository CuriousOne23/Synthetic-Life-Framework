import numpy as np
import matplotlib.pyplot as plt

# Time domain
T = 100
t = np.linspace(0, T, T)

# Escalating perturbation
def escalating_sinusoid(t, base_amp=0.5, growth=0.05, freq=0.1):
    return (base_amp + growth * t) * np.sin(2 * np.pi * freq * t)

# Decay profile for MCG
def decay_profile(t, start=1.0, end=0.2):
    return np.clip(start - (start - end) * (t / t[-1]), end, start)

# Identity response with dynamic damping
def identity_response_dynamic(P, M_profile, C_profile, G_profile):
    I = np.zeros_like(t)
    for i in range(1, len(t)):
        damping = M_profile[i] * C_profile[i] * G_profile[i]
        I[i] = I[i-1] + damping * (P[i] - I[i-1])
    return I

# Identity response with fixed damping = 1
def identity_response_fixed(P):
    return P.copy()

# Generate inputs
P = escalating_sinusoid(t)
M = decay_profile(t)
C = decay_profile(t)
G = decay_profile(t)

# Simulate three cases
I_decay = identity_response_dynamic(P, M, C, G)
I_fixed = identity_response_fixed(P)
I_flat = np.zeros_like(t)

# Threshold marker: when damping drops below 0.3
threshold_index = np.argmax(M * C * G < 0.3)
threshold_time = t[threshold_index]

# Plot
plt.figure(figsize=(10, 6))
plt.plot(t, P, 'k--', linewidth=3, label='Escalating Perturbation')
plt.plot(t, I_decay, 'b', label='I_decay (decaying MCG)')
plt.plot(t, I_fixed, 'r--', label='I_fixed (damping = 1)')
plt.plot(t, I_flat, 'g--', label='I_flat (damping = 0)')
plt.axvline(x=threshold_time, color='purple', linestyle=':', linewidth=2, label='Resilience Threshold')
plt.xlabel("Time", labelpad=15)
plt.ylabel("Identity")
plt.title("Resilience vs Fixed and Flat", pad=14)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
