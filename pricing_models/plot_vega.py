"""Vega visualizations: how the option's price-sensitivity to vol behaves.

Vega is quoted here as "$ per 1 vol point" (raw dPrice/dsigma divided by 100).

Left panel  : vega vs spot, for three expiries -> shows the ATM hump, and how it
              grows TALLER and WIDER with more time to expiry.
Right panel : ATM vega vs time to expiry -> shows vega rising with sqrt(tau).
"""

import math

import matplotlib.pyplot as plt

from black_scholes_merton import vega

K = 100
r = 0.05
sigma = 0.20


def vega_pt(S, tau):
    """Vega in $ per 1 vol point (1 percentage point of sigma)."""
    return vega(S, K, r, tau, sigma) / 100


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- LEFT: vega vs spot, three expiries ---
spots = [s / 2 for s in range(100, 301)]   # 50 -> 150
for days, label in [(30, "1 month"), (90, "3 months"), (252, "1 year")]:
    tau = days / 252
    ax1.plot(spots, [vega_pt(S, tau) for S in spots], linewidth=2, label=label)
ax1.axvline(K, color="grey", linestyle=":", linewidth=1, label=f"strike {K}")
ax1.set_title("Vega vs spot  (hump peaks ATM, grows with time)")
ax1.set_xlabel("spot price  S")
ax1.set_ylabel("vega  ($ per 1 vol point)")
ax1.legend()
ax1.grid(alpha=0.3)

# --- RIGHT: ATM vega vs time to expiry ---
taus = [d / 252 for d in range(5, 505, 5)]   # ~1 week out to ~2 years
ax2.plot(taus, [vega_pt(K, t) for t in taus], color="tab:purple", linewidth=2)
ax2.set_title("ATM vega vs time to expiry  (rises with sqrt(tau))")
ax2.set_xlabel("time to expiry  tau  (years)")
ax2.set_ylabel("vega  ($ per 1 vol point)")
ax2.grid(alpha=0.3)

fig.tight_layout()

if __name__ == "__main__":
    plt.show()
