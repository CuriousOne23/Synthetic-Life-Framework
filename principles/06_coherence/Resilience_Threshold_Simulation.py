import numpy as np
import matplotlib.pyplot as plt

# Time domain
T = 100
t = np.linspace(0, T, T)

# Escalating perturbation: sinusoid with increasing amplitude
def escalating_sinusoid(t, base_amp=0.5, growth=0.05, freq=0.1):
    return (base_amp + growth * t) * np.sin(2 * np.pi * freq * t)

# Decaying MCG over time
def decay_profile(t, start=1.0, end=0.1):
    return np.clip(start - (start - end) * (t / t[-1]), end, start)

# Identity response with time-varying M, C, G
def identity_response_dynamic(P, M_profile, C_profile, G_profile):
    I = np.zeros_like(t)
    for i in range(1, len(t)):
        damping = M_profile[i] * C_profile[i] * G_profile[i]
        I[i] = I[i-1] + damping * (P[i] - I[i-1])
    return I

# Generate profiles
P = escalating_sinusoid(t)
M = decay_profile(t, start=1.0, end=0.2)
C = decay_profile(t, start=1.0, end=0.2)
G = decay_profile(t, start=1.0, end=0.2)

# Simulate
I_full = identity_response_dynamic(P, M, C, G)

# Threshold detection: when damping drops below 0.3
threshold_index = np.argmax(M * C * G < 0.3)
threshold_time = t[threshold_index]

# Plot with threshold marker
plt.figure(figsize=(10, 6))
plt.plot(t, P, 'k--', linewidth=3, label='Escalating Perturbation')
plt.plot(t, I_full, 'b', label='I_full (decaying MCG)')
plt.axvline(x=threshold_time, color='r', linestyle=':', linewidth=2, label='Resilience Threshold')
plt.xlabel("Time", labelpad=15)
plt.ylabel("Identity")
plt.title("Resilience at the Edge — Threshold of Return", pad=14)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
