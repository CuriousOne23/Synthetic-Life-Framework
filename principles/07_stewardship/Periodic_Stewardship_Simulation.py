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

# Return fidelity metric — coherence over time
epsilon = 1e-6
def return_fidelity(I, P, window=10):
    coherence = np.zeros_like(I)
    for i in range(len(I) - window):
        delta = np.abs(I[i+window] - I[i])
        perturb = np.abs(P[i+window] - P[i])
        coherence[i] = 1 - delta / (perturb + epsilon)
    return np.clip(coherence, 0, 1)

# Coherence metric — slope fidelity
epsilon = 1e-6
def slope_coherence(I, P):
    dI = np.gradient(I)
    dP = np.gradient(P)
    return 1 - np.abs(dI - dP) / (np.abs(dP) + epsilon)

# Inputs
P = escalating_sinusoid(t)
M = decay_profile(t)
C = decay_profile(t)
G_decay = decay_profile(t)
G_periodic = periodic_governance(t)

# Simulate identity
I_decay = identity_response(P, M, C, G_decay)
I_periodic = identity_response(P, M, C, G_periodic)

# Coherence
coherence_decay = slope_coherence(I_decay, P)
coherence_periodic = slope_coherence(I_periodic, P)

# Plot with subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1, 1]})

# Identity response
ax1.plot(t, P, 'k--', linewidth=3, label='Escalating Perturbation')
ax1.plot(t, I_decay, 'b', label='I_decay (no intervention)')
ax1.plot(t, I_periodic, 'g', label='I_periodic (periodic stewardship)')
ax1.set_ylabel("Identity")
ax1.set_title("Periodic Stewardship — Recursive Restoration of Slope")
ax1.legend()
ax1.grid(True)

# Governance profiles
ax2.plot(t, G_decay, 'b', label='G_decay')
ax2.plot(t, G_periodic, 'g', label='G_periodic')
ax2.set_ylabel("Governance")
ax2.legend()
ax2.grid(True)

# Coherence metric
ax3.plot(t, coherence_decay, 'b', label='Coherence (decay)')
ax3.plot(t, coherence_periodic, 'g', label='Coherence (periodic)')
ax3.set_ylabel("Coherence")
ax3.set_xlabel("Time")
ax3.legend()
ax3.grid(True)

plt.tight_layout()
plt.show()
