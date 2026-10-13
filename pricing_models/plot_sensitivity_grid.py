"""Sensitivity grid: how the call-price curve shifts when each input moves one notch down / up.

Layout: 4 rows (one per tweakable input) x 3 columns (down | baseline | up).
 - x-axis of every cell is spot price S (the 5th input, swept, so it can't be a row).
 - middle column is ALWAYS the same baseline curve.
 - left/right cells move that row's variable one measure down/up; the faint grey line
   is the baseline curve, so you can see how far the coloured line has shifted.
 - dashed line is the payoff at expiry, max(S-K, 0), as a fixed reference.
"""

import matplotlib.pyplot as plt

from black_scholes_merton import d1, d2, call_price

# spot grid swept along every x-axis
spots = [s / 10 for s in range(600, 1401)]   # 60.0 -> 140.0 in $0.10 steps

# the centre-column settings; every "baseline" curve uses exactly these
baseline = dict(K=100, r=0.05, tau=0.25, sigma=0.20)

# each row: (label, which input, (down, baseline, up))
rows = [
    ("K  (strike)",     "K",     (90, 100, 110)),
    ("r  (rate)",       "r",     (0.01, 0.05, 0.09)),
    ("tau (time, yrs)", "tau",   (0.10, 0.25, 0.40)),
    ("sigma (vol)",     "sigma", (0.10, 0.20, 0.30)),
]

col_titles = ("one measure DOWN", "baseline", "one measure UP")


def bs_call(S, K, r, tau, sigma):
    """Today's Black-Scholes price of the call at spot S."""
    return call_price(S, K, r, tau, d1(S, K, r, tau, sigma), d2(S, K, r, tau, sigma))


def curve(**params):
    """Price curve across the spot grid for a given set of inputs."""
    return [bs_call(S, **params) for S in spots]


def build_grid():
    base_curve = curve(**baseline)   # the grey reference drawn behind every cell

    fig, axes = plt.subplots(len(rows), 3, figsize=(13, 14), sharex=True, sharey=True)

    for i, (label, var, values) in enumerate(rows):
        for j, value in enumerate(values):
            ax = axes[i][j]

            params = baseline.copy()
            params[var] = value                 # move just this row's variable
            y = curve(**params)
            payoff = [max(S - params["K"], 0) for S in spots]   # strike may move on the K row

            ax.plot(spots, base_curve, color="lightgrey", linewidth=1)   # where we started
            ax.plot(spots, y, color="tab:blue", linewidth=2)             # the moved curve
            ax.plot(spots, payoff, color="tab:orange", linestyle="--", linewidth=1)
            ax.grid(alpha=0.25)
            ax.set_title(f"{var} = {value}", fontsize=9)

            if i == 0:
                ax.text(0.5, 1.28, col_titles[j], transform=ax.transAxes,
                        ha="center", fontsize=10, fontweight="bold")
            if j == 0:
                ax.set_ylabel(label, fontsize=10, fontweight="bold")

    fig.suptitle("Black-Scholes call price vs spot — one input moved at a time", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    return fig


if __name__ == "__main__":
    build_grid()
    plt.show()
