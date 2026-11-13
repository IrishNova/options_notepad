"""Why typical distance grows with sqrt(t), not t.

Simulate many coin-flip random walks. At each step, plot how far a typical
walker is from the start (the RMS distance). It traces sqrt(t), NOT t --
because variance adds linearly (the straight line) and distance is its root.
"""

import math
import random

import matplotlib.pyplot as plt

STEPS = 100
WALKERS = 5000

# each walker: +1/-1 per step; track position over time
positions = [0] * WALKERS
rms = []          # typical (root-mean-square) distance from zero at each step
variance = []     # mean squared distance -- the thing that adds linearly

for t in range(1, STEPS + 1):
    for i in range(WALKERS):
        positions[i] += 1 if random.random() < 0.5 else -1
    mean_sq = sum(p * p for p in positions) / WALKERS
    variance.append(mean_sq)
    rms.append(math.sqrt(mean_sq))

steps = list(range(1, STEPS + 1))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# LEFT: variance (mean squared distance) -- adds linearly, a straight line
ax1.plot(steps, variance, color="tab:red", linewidth=2, label="variance (mean sq. distance)")
ax1.plot(steps, steps, color="grey", linestyle="--", linewidth=1, label="y = t  (straight)")
ax1.set_title("Variance adds LINEARLY  ->  straight line")
ax1.set_xlabel("steps (time)")
ax1.set_ylabel("mean squared distance")
ax1.legend()
ax1.grid(alpha=0.3)

# RIGHT: typical distance = sqrt of that -- the sqrt(t) curve
ax2.plot(steps, rms, color="tab:blue", linewidth=2, label="typical distance (RMS)")
ax2.plot(steps, [math.sqrt(t) for t in steps], color="grey", linestyle="--",
         linewidth=1, label="y = sqrt(t)")
ax2.set_title("Typical distance = its square root  ->  sqrt(t)")
ax2.set_xlabel("steps (time)")
ax2.set_ylabel("typical distance from start")
ax2.legend()
ax2.grid(alpha=0.3)

fig.tight_layout()

if __name__ == "__main__":
    plt.show()
