"""Raw vs. weighted vega across the term structure (ATM).

Raw vega grows with sqrt(tau) -- so by the raw number, short-dated options look
almost vega-less. But short-dated VOL moves far more than long-dated vol
(vol-of-vol ~ 1/sqrt(T)). Weighting each tenor's vega by sqrt(T_ref/T) puts every
expiry on the same "typical vol move" footing -- and the weighted line comes out
roughly FLAT, which is what makes the term structure comparable tenor-to-tenor.

    weighted_vega(T) = raw_vega(T) * sqrt(T_ref / T)

Reference tenor here = 1 year (252 trading days).
"""

import math

import matplotlib.pyplot as plt

from black_scholes_merton import vega

K = 100
r = 0.05
sigma = 0.20
T_ref = 252 / 252   # 1 year, in years


def raw_vega_pt(tau):
    """ATM raw vega, $ per 1 vol point."""
    return vega(K, K, r, tau, sigma) / 100


def weighted_vega_pt(tau):
    """Raw vega scaled to put this tenor on the reference tenor's footing."""
    return raw_vega_pt(tau) * math.sqrt(T_ref / tau)


days = list(range(5, 505, 5))          # ~1 week out to ~2 years
taus = [d / 252 for d in days]

raw = [raw_vega_pt(t) for t in taus]
weighted = [weighted_vega_pt(t) for t in taus]
multiplier = [math.sqrt(T_ref / t) for t in taus]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- LEFT: raw vs weighted vega ---
ax1.plot(days, raw, color="tab:blue", linewidth=2, label="raw vega (grows ~sqrt(T))")
ax1.plot(days, weighted, color="tab:red", linewidth=2,
         label="weighted vega  x sqrt(T_ref/T)  (~flat)")
ax1.axvline(252, color="grey", linestyle=":", linewidth=1, label="reference = 1yr")
ax1.set_title("Raw vs weighted ATM vega across tenors")
ax1.set_xlabel("time to expiry  (trading days)")
ax1.set_ylabel("vega  ($ per 1 vol point)")
ax1.legend()
ax1.grid(alpha=0.3)

# --- RIGHT: the weighting multiplier itself ---
ax2.plot(days, multiplier, color="tab:green", linewidth=2)
ax2.axhline(1.0, color="grey", linestyle=":", linewidth=1)
ax2.axvline(252, color="grey", linestyle=":", linewidth=1)
ax2.set_title("The weighting multiplier  sqrt(T_ref / T)")
ax2.set_xlabel("time to expiry  (trading days)")
ax2.set_ylabel("multiply raw vega by...")
ax2.grid(alpha=0.3)
# annotate the 1-month boost
m21 = math.sqrt(T_ref / (21 / 252))
ax2.annotate(f"1 month -> x{m21:.1f}", xy=(21, m21), xytext=(70, m21 - 0.4),
             arrowprops=dict(arrowstyle="->", color="black"))

fig.tight_layout()

if __name__ == "__main__":
    plt.show()
