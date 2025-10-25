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

# Periodic governance boost
def periodic_governance(t, interval=20, boost=0.5):
    G = decay_profile(t)
    for i in range(0, len(t), interval):
        G[i:i+5] += boost  # short pulse
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
G_periodic = periodic_governance(t)

# Simulate identity
I_decay = identity_response(P, M, C, G_decay)
I_periodic = identity_response(P, M, C, G_periodic)

# Plot with subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

# Top plot: Identity response
ax1.plot(t, P, 'k--', linewidth=3, label='Escalating Perturbation')
ax1.plot(t, I_decay, 'b', label='I_decay (no intervention)')
ax1.plot(t, I_periodic, 'g', label='I_periodic (periodic stewardship)')
ax1.set_ylabel("Identity")
ax1.set_title("Periodic Stewardship — Recursive Restoration of Slope")
ax1.legend()
ax1.grid(True)

# Bottom plot: Governance profiles
ax2.plot(t, G_decay, 'b', label='G_decay')
ax2.plot(t, G_periodic, 'g', label='G_periodic')
ax2.set_ylabel("Governance")
ax2.set_xlabel("Time")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
