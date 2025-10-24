import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.arange(0, 50)

# --- Perturbations ---
# Impulse: sharp spike at t = 25
impulse = np.zeros_like(t)
impulse[25] = 1.0

# Sinusoidal: smooth oscillation
sinusoidal = 0.1 * np.sin(t / 3)

# --- Optimal Base Components ---
# Memory: slower decay to preserve continuity
M = 1 / (1 + t / 20)

# Governance: graceful emergence with reduced gain
G = 0.05 * (np.tanh((t - 35) / 45) + 1)

# Choice with impulse
C_impulse = np.log(1 + t / 5) + impulse

# Choice with sinusoidal
C_sinusoidal = np.log(1 + t / 5) + sinusoidal

# --- Identity Models (Impulse) ---
I_full_impulse = 0.4 * M + 0.3 * C_impulse + 0.3 * G
I_no_memory_impulse = 0.5 * C_impulse + 0.5 * G
I_no_choice_impulse = 0.5 * M + 0.5 * G
I_no_governance_impulse = 0.5 * M + 0.5 * C_impulse

# --- Identity Models (Sinusoidal) ---
I_full_sinusoidal = 0.4 * M + 0.3 * C_sinusoidal + 0.3 * G
I_no_memory_sinusoidal = 0.5 * C_sinusoidal + 0.5 * G
I_no_choice_sinusoidal = 0.5 * M + 0.5 * G
I_no_governance_sinusoidal = 0.5 * M + 0.5 * C_sinusoidal

# --- Plot Perturbations + Components ---
plt.figure(figsize=(15, 8))

# Subplot 1: Impulse perturbation
plt.subplot(3, 1, 1)
plt.plot(t, impulse, color='red')
plt.title('Impulse Perturbation')
plt.ylabel('Magnitude')
plt.grid(True)

# Subplot 2: Sinusoidal perturbation
plt.subplot(3, 1, 2)
plt.plot(t, sinusoidal, color='blue')
plt.title('Sinusoidal Perturbation')
plt.ylabel('Magnitude')
plt.grid(True)

# Subplot 3: Component curves
plt.subplot(3, 1, 3)
plt.plot(t, M, label='Memory (M)', color='green')
plt.plot(t, C_sinusoidal, label='Choice (C)', color='orange')  # sinusoidal version shown
plt.plot(t, G, label='Governance (G)', color='purple')
plt.title('Component Curves')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# --- Plot Identity Responses ---
plt.figure(figsize=(15, 6))

# Subplot 1: Impulse response
plt.subplot(1, 2, 1)
plt.plot(t, I_full_impulse, label='I_full', linewidth=2)
plt.plot(t, I_no_memory_impulse, label='I_no_memory', linestyle='--')
plt.plot(t, I_no_choice_impulse, label='I_no_choice', linestyle='--')
plt.plot(t, I_no_governance_impulse, label='I_no_governance', linestyle='--')
plt.title('Identity Response to Impulse')
plt.xlabel('Time')
plt.ylabel('Identity')
plt.legend()
plt.grid(True)

# Subplot 2: Sinusoidal response
plt.subplot(1, 2, 2)
plt.plot(t, I_full_sinusoidal, label='I_full', linewidth=2)
plt.plot(t, I_no_memory_sinusoidal, label='I_no_memory', linestyle='--')
plt.plot(t, I_no_choice_sinusoidal, label='I_no_choice', linestyle='--')
plt.plot(t, I_no_governance_sinusoidal, label='I_no_governance', linestyle='--')
plt.title('Identity Response to Sinusoidal')
plt.xlabel('Time')
plt.ylabel('Identity')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
