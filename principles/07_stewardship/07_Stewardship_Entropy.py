import numpy as np
import matplotlib.pyplot as plt

steps = 200
entropy = [1.0]
slope = [0.0]
max_delta = 0.2

# Governed path (stewardship on)
entropy_g = [1.0]
slope_g = [0.0]
perturbation = []
governance = [1.0]  # Base governance level
for i in range(1, steps):
    raw = np.random.uniform(0.8, 1.2)
    perturbation.append(raw)
    # Periodic governance boost every 20 steps
    if i % 20 < 10:  # 10-step pulse width
        gov_boost = 0.6
    else:
        gov_boost = 0.0
    current_gov = 1.0 + gov_boost  # Base + pulse
    governance.append(current_gov)
    delta = raw - slope_g[-1]
    if abs(delta) > max_delta:
        change = np.sign(delta) * max_delta
    else:
        change = delta
    new_slope = slope_g[-1] + change
    new_ent = entropy_g[-1] + new_slope
    slope_g.append(new_slope)
    entropy_g.append(new_ent)

# Ungoverned path (no stewardship)
entropy_u = [1.0]
slope_u = [0.0]
for i in range(1, steps):
    raw = np.random.uniform(0.8, 1.2)
    new_slope = raw
    new_ent = entropy_u[-1] + new_slope
    slope_u.append(new_slope)
    entropy_u.append(new_ent)

# One-score metric: mean final stretch efficacy (using negative entropy for consistency)
efficacy = np.mean([-e for e in entropy_g[-20:]]) - np.mean([-e for e in entropy_u[-20:]])
print(f"Stewardship efficacy score: {efficacy:.3f}")

# Calculate delta (No - With stewardship for negative entropy)
delta_entropy = [g -u for g, u in zip(entropy_g, entropy_u)]  # Reflects -(g - u) for negative entropy delta

# Plot with four subplots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 14), sharex=True)

# Positive entropy plot
ax1.plot(entropy_g, label='With stewardship', linewidth=2.5, color='green')
ax1.plot(entropy_u, label='No stewardship', linewidth=2, color='red', alpha=0.8)
ax1.axhline(2.0, color='k', linestyle='--', alpha=0.5)
ax1.set_ylabel('Entropy')
ax1.set_title('Stewardship keeps entropy low - efficacy score above')
ax1.legend()
ax1.grid(True)

# Delta plot (negative entropy context)
ax2.plot(delta_entropy, label='Delta (With - No stewardship)', linewidth=1.5, color='orange')
ax2.set_ylabel('Entropy')
ax2.legend()
ax2.grid(True)

# Perturbation plot
ax3.plot(perturbation, label='Raw perturbation', linewidth=1.5, color='blue')
ax3.set_ylabel('Perturbation')
ax3.legend()
ax3.grid(True)

# Governance plot
ax4.plot(governance, label='Periodic stewardship', linewidth=1.5, color='purple')
ax4.set_ylabel('Governance level')
ax4.set_xlabel('Time steps')
ax4.legend()
ax4.grid(True)

plt.tight_layout()
plt.show()