import numpy as np
import matplotlib.pyplot as plt

# Time domain
T = 100
t = np.linspace(0, T, T)

# Escalating perturbation
def escalating_sinusoid(t, base_amp=0.5, growth=0.05, freq=0.1):
    return (base_amp + growth * t) * np.sin(2 * np.pi * freq * t)

# Decay profile
def decay_profile(t, start=1.0, end=0.2):
    return np.clip(start - (start - end) * (t / t[-1]), end, start)

# Governance boost after threshold
def governance_boost(t, threshold_index, boost=0.6):
    G = decay_profile(t)
    G[threshold_index:] += boost
    return np.clip(G, 0, 1)

# Identity response
def identity_response(P, M, C, G):
    I = np.zeros_like(t)
    for i in range(1, len(t)):
        damping = M[i] * C[i] * G[i]
        I[i] = I[i-1] + damping * (P[i] - I[i-1])
    return I

# Inputs
P = escalating_sinusoid(t)
M = decay_profile(t)
C = decay_profile(t)
G_decay = decay_profile(t)

# Threshold detection
threshold_index = np.argmax(M * C * G_decay < 0.3)
threshold_time = t[threshold_index]

# Stewardship intervention
G_steward = governance_boost(t, threshold_index)

# Simulate identity
I_decay = identity_response(P, M, C, G_decay)
I_steward = identity_response(P, M, C, G_steward)

# Plot with subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

# Top plot: Identity response
ax1.plot(t, P, 'k--', linewidth=3, label='Escalating Perturbation')
ax1.plot(t, I_decay, 'b', label='I_decay (no intervention)')
ax1.plot(t, I_steward, 'g', label='I_steward (governance boost)')
ax1.axvline(x=threshold_time, color='purple', linestyle=':', linewidth=2, label='Threshold of Stewardship')
ax1.set_ylabel("Identity")
ax1.set_title("Stewardship Invocation — Restoring Slope After Fray")
ax1.legend()
ax1.grid(True)

# Bottom plot: Governance profiles
ax2.plot(t, G_decay, 'b', label='G_decay')
ax2.plot(t, G_steward, 'g', label='G_steward')
ax2.axvline(x=threshold_time, color='purple', linestyle=':', linewidth=2)
ax2.set_ylabel("Governance")
ax2.set_xlabel("Time")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
