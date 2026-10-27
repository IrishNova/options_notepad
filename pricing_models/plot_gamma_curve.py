"""Stationary gamma curve: gamma plotted against spot price, holding everything else fixed.

Shows the hump -- gamma peaks at (near) the strike and fades deep ITM / deep OTM.
"""

import matplotlib.pyplot as plt

from black_scholes_merton import gamma

K = 100
r = 0.05
sigma = 0.20
tau = 60 / 252   # ~60 trading days to expiry, fixed

spots = [s / 2 for s in range(100, 301)]   # 50 -> 150 in $0.50 steps
gammas = [gamma(S, K, r, tau, sigma) for S in spots]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(spots, gammas, color="tab:red", linewidth=2)
ax.axvline(K, color="grey", linestyle=":", linewidth=1, label=f"strike {K}")
ax.set_title("Gamma vs spot price  (the hump)")
ax.set_xlabel("spot price  S")
ax.set_ylabel("gamma")
ax.legend()
ax.grid(alpha=0.3)

if __name__ == "__main__":
    plt.show()
