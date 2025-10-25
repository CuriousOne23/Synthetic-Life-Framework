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
def periodic_governance(t, interval=20, boost=0.5, pulse_width=10):
    G = decay_profile(t)
    for i in range(0, len(t), interval):
        G[i:i+pulse_width] += boost
    return np.clip(G, 0, 1)

# Identity response
def identity_response(P, M, C, G):
    I = np.zeros_like(t)
    for i in range(1, len(t)):
        damping = M[i] * C[i] * G[i]
        I[i] = I[i-1] + damping * (P[i] - I[i-1])
    return I

# Return fidelity metric
epsilon = 1e-6
def return_fidelity(I, P, window=10):
    coherence = np.zeros_like(I)
    for i in range(len(I) - window):
        delta = np.abs(I[i+window] - I[i])
        perturb = np.abs(P[i+window] - P[i])
        coherence[i] = 1 - delta / (perturb + epsilon)
    return np.clip(coherence, 0, 1)

# Segment coherence by governance pulses
def segment_coherence(I, P, pulse_starts, pulse_width):
    scores = []
    for start in pulse_starts:
        end = min(start + pulse_width, len(I))
        delta_I = np.abs(I[end-1] - I[start])
        delta_P = np.abs(P[end-1] - P[start])
        score = 1 - delta_I / (delta_P + epsilon)
        scores.append(score)
    return np.clip(scores, 0, 1)

# Slope fidelity per pulse
def segmented_slope_fidelity(I, P, pulse_starts, pulse_width):
    scores = []
    for start in pulse_starts:
        end = min(start + pulse_width, len(I))
        dI = np.gradient(I[start:end])
        dP = np.gradient(P[start:end])
        fidelity = 1 - np.mean(np.abs(dI - dP)) / (np.mean(np.abs(dP)) + epsilon)
        scores.append(fidelity)
    return np.clip(scores, 0, 1)

# Memory fidelity across pulses
def memory_fidelity(I, pulse_starts, pulse_width):
    scores = []
    for i in range(1, len(pulse_starts)):
        prev = pulse_starts[i-1]
        curr = pulse_starts[i]
        dI_prev = np.gradient(I[prev:prev+pulse_width])
        dI_curr = np.gradient(I[curr:curr+pulse_width])
        score = 1 - np.mean(np.abs(dI_curr - dI_prev)) / (np.mean(np.abs(dI_prev)) + epsilon)
        scores.append(score)
    return np.clip(scores, 0, 1)

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
coherence_decay = return_fidelity(I_decay, P)
coherence_periodic = return_fidelity(I_periodic, P)

# Damping
D_decay = M * C * G_decay
D_periodic = M * C * G_periodic

# Slope difference
dI_decay = np.gradient(I_decay)
dI_periodic = np.gradient(I_periodic)
dP = np.gradient(P)
slope_diff_decay = np.abs(dI_decay - dP)
slope_diff_periodic = np.abs(dI_periodic - dP)

# Pulse intervals
pulse_starts = list(range(0, len(t), 20))

# Segment metrics
segment_scores = segment_coherence(I_periodic, P, pulse_starts, pulse_width=10)
slope_scores = segmented_slope_fidelity(I_periodic, P, pulse_starts, pulse_width=10)
memory_scores = memory_fidelity(I_periodic, pulse_starts, pulse_width=10)

# Plot panels
fig, axs = plt.subplots(6, 1, figsize=(14, 18), sharex=True)

# Identity
axs[0].plot(t, P, 'k--', linewidth=2, label='Escalating Perturbation')
axs[0].plot(t, I_decay, 'b', label='I_decay')
axs[0].plot(t, I_periodic, 'g', label='I_periodic')
axs[0].set_ylabel("Identity")
axs[0].set_title("Identity Response")
axs[0].legend()
axs[0].grid(True)

# Governance
axs[1].plot(t, G_decay, 'b', label='G_decay')
axs[1].plot(t, G_periodic, 'g', label='G_periodic')
axs[1].set_ylabel("Governance")
axs[1].set_title("Governance Profiles")
axs[1].legend()
axs[1].grid(True)

# Coherence
axs[2].plot(t, coherence_decay, 'b', label='Coherence (decay)')
axs[2].plot(t, coherence_periodic, 'g', label='Coherence (periodic)')
for start in pulse_starts:
    axs[2].axvspan(start, start+10, color='green', alpha=0.1)
axs[2].set_ylabel("Coherence")
axs[2].set_title("Return Fidelity with Pulse Intervals")
axs[2].legend()
axs[2].grid(True)

# Damping
axs[3].plot(t, D_decay, 'b', label='Damping (decay)')
axs[3].plot(t, D_periodic, 'g', label='Damping (periodic)')
axs[3].set_ylabel("Damping")
axs[3].set_title("Effective Damping Over Time")
axs[3].legend()
axs[3].grid(True)

# Slope Δ
axs[4].plot(t, slope_diff_decay, 'b', label='Slope Δ (decay)')
axs[4].plot(t, slope_diff_periodic, 'g', label='Slope Δ (periodic)')
axs[4].set_ylabel("Slope Δ")
axs[4].set_title("Slope Difference: Identity vs Perturbation")
axs[4].legend()
axs[4].grid(True)

# Memory Fidelity (bar plot)
axs[5].bar(range(1, len(memory_scores)+1), memory_scores, color='purple')
axs[5].set_ylabel("Memory Fidelity")
axs[5].set_xlabel("Pulse Index")
axs[5].set_title("Memory Fidelity Across Pulses")
axs[5].grid(True)

plt.tight_layout()
plt.show()

# Print segmented metrics
print("Segmented Coherence Scores:")
for i, score in enumerate(segment_scores):
    print(f"Pulse {i+1}: {score:.3f}")

print("\nSegmented Slope Fidelity Scores:")
for i, score in enumerate(slope_scores):
    print(f"Pulse {i+1}: {score:.3f}")

print("\nMemory Fidelity Scores:")
for i, score in enumerate(memory_scores):
    print(f"Between Pulse {i} and {i+1}: {score:.3f}")
