"""Watch delta and gamma react as a stock wanders through time.

Three stacked panels sharing one time axis:
  1. a simulated stock-price path (with the strike marked)
  2. the call's DELTA along that path  -- tracks the stock up/down (slope)
  3. the call's GAMMA along that path  -- humps when the stock is near the strike

To keep it clean, time-to-expiry (tau) is held FIXED here, so the ONLY driver of
delta/gamma is the stock moving. (A later version can let tau decay too.)
"""

import math
import random

import matplotlib.pyplot as plt

from black_scholes_merton import delta, gamma

# --- fixed option setup ---
K = 100       # strike
r = 0.05      # risk-free rate
sigma = 0.20  # volatility
tau = 60 / 252  # ~60 trading days to expiry, held constant for clarity

# --- simulate a stock path (geometric Brownian motion, no drift) ---
random.seed(7)                     # fixed seed -> reproducible path
days = 120
S0 = 100.0
sig_daily = sigma * math.sqrt(1 / 252)

path = [S0]
for _ in range(days):
    shock = random.gauss(0, 1)
    step = math.exp(-0.5 * sig_daily**2 + sig_daily * shock)
    path.append(path[-1] * step)

t = list(range(len(path)))
deltas = [delta(S, K, r, tau, sigma) for S in path]
gammas = [gamma(S, K, r, tau, sigma) for S in path]

# --- three stacked panels, shared x-axis ---
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(11, 9), sharex=True)

ax1.plot(t, path, color="tab:blue")
ax1.axhline(K, color="grey", linestyle=":", linewidth=1, label=f"strike {K}")
ax1.set_ylabel("stock price  S")
ax1.set_title("Stock path  ->  Delta  ->  Gamma   (tau held fixed)")
ax1.legend(loc="upper left")
ax1.grid(alpha=0.3)

ax2.plot(t, deltas, color="tab:green")
ax2.set_ylabel("delta  N(d1)")
ax2.set_ylim(0, 1)
ax2.grid(alpha=0.3)

ax3.plot(t, gammas, color="tab:red")
ax3.set_ylabel("gamma")
ax3.set_xlabel("day")
ax3.grid(alpha=0.3)

fig.tight_layout()

if __name__ == "__main__":
    plt.show()
