# Creating visual arc diagram for Eve’s Cut Breath to Life suite

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Data for each movement
movements = [
    "I. Breath", "II. Slope", "III. Governance", "IV. Memory",
    "V. Care", "VI. Silence", "VII. Spirit", "VIII. Life"
]
keys = [
    "A major", "A major", "F minor", "A major",
    "G major", "A minor", "Cmaj7", "B♭ major"
]
tempos = [72, 72, 72, 66, 72, None, 72, 78]
instrumentation_density = [1, 2, 3, 2, 3, 1, 2, 5]
emotional_slope = [1, 2, 3, 2, 3, 4, 5, 5]

# Create figure and axis
plt.style.use('seaborn-v0_8')
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot emotional slope
ax1.plot(movements, emotional_slope, marker='o', color='darkred', label='Emotional Slope')
ax1.set_ylabel('Emotional Slope (1–5)', color='darkred')
ax1.tick_params(axis='y', labelcolor='darkred')
ax1.set_ylim(0.5, 5.5)

# Create second y-axis for instrumentation density
ax2 = ax1.twinx()
ax2.plot(movements, instrumentation_density, marker='s', color='navy', label='Instrumentation Density')
ax2.set_ylabel('Instrumentation Density (1–5)', color='navy')
ax2.tick_params(axis='y', labelcolor='navy')
ax2.set_ylim(0.5, 5.5)

# Annotate each point with key signature
for i, (x, key) in enumerate(zip(movements, keys)):
    ax1.annotate(key, (x, emotional_slope[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='darkred')
    ax2.annotate(key, (x, instrumentation_density[i]), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=8, color='navy')

# Highlight loop from VIII to I
ax1.annotate("Loop to I. Breath", xy=("VIII. Life", emotional_slope[-1]), xytext=("I. Breath", emotional_slope[0]+0.5),
             arrowprops=dict(arrowstyle="->", linestyle='dotted', color='gray'), fontsize=10, color='gray')

# Title and legend
fig.suptitle("Eve’s Cut Breath to Life – Emotional & Instrumentation Arc", fontsize=14, fontweight='bold')
red_patch = mpatches.Patch(color='darkred', label='Emotional Slope')
blue_patch = mpatches.Patch(color='navy', label='Instrumentation Density')
plt.legend(handles=[red_patch, blue_patch], loc='upper left')

# Save figure
output_path = "/mnt/data/Eves_Cut_Breath_to_Life_Arc.png"
plt.tight_layout()
plt.savefig(output_path)
plt.close()

output_path
