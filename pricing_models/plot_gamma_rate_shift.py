"""How the risk-free rate shifts the gamma hump.

Two gamma curves at different r, everything else fixed. Higher r -> stronger
upward drift -> the "most likely to finish at the strike" spot starts lower ->
the peak slides LEFT. (The shift is small -- r is a weak lever on gamma.)
"""

import matplotlib.pyplot as plt

from black_scholes_merton import gamma

K = 100
sigma = 0.20
tau = 60 / 252   # ~60 trading days to expiry, fixed

spots = [s / 2 for s in range(100, 301)]   # 50 -> 150 in $0.50 steps

g_05 = [gamma(S, K, 0.05, tau, sigma) for S in spots]
g_10 = [gamma(S, K, 0.10, tau, sigma) for S in spots]

# find each peak's spot for annotation
peak_05 = spots[g_05.index(max(g_05))]
peak_10 = spots[g_10.index(max(g_10))]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(spots, g_05, color="tab:red", linewidth=2, label=f"r = 5%   (peak S ~ {peak_05:.1f})")
ax.plot(spots, g_10, color="tab:blue", linewidth=2, label=f"r = 10%  (peak S ~ {peak_10:.1f})")
ax.axvline(K, color="grey", linestyle=":", linewidth=1, label=f"strike {K}")
ax.set_title("Gamma hump: how the risk-free rate shifts the peak")
ax.set_xlabel("spot price  S")
ax.set_ylabel("gamma")
ax.legend()
ax.grid(alpha=0.3)

if __name__ == "__main__":
    plt.show()
