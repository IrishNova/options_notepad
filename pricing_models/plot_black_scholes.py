"""Visualising the Black-Scholes call: the smooth price curve TODAY vs. the payoff AT EXPIRY."""

import matplotlib.pyplot as plt

from black_scholes_merton import d1, d2, call_price

# --- fixed inputs (everything except S, which we sweep along the x-axis) ---
K = 100       # strike
r = 0.05      # risk-free rate
tau = 0.25    # time to expiry, in years
sigma = 0.20  # volatility

# sweep spot across a fine grid so the model curve comes out smooth
spots = [s / 10 for s in range(600, 1401)]   # 60.0 -> 140.0 in $0.10 steps


def bs_call(S):
    """Today's Black-Scholes price of the call at spot S."""
    return call_price(S, K, r, tau, d1(S, K, r, tau, sigma), d2(S, K, r, tau, sigma))


bs_prices = [bs_call(S) for S in spots]        # the model's price, TODAY (with time left)
payoffs = [max(S - K, 0) for S in spots]       # what the call is worth AT expiry (intrinsic value)

fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(spots, bs_prices, linewidth=2, label=f"BS price today  (tau={tau})")
ax.plot(spots, payoffs, linestyle="--", label="payoff at expiry  max(S-K, 0)")
ax.axvline(K, color="grey", linewidth=1, linestyle=":")   # mark the strike
ax.set_title("Black-Scholes call: price today vs. payoff at expiry")
ax.set_xlabel("spot price  S")
ax.set_ylabel("option value  ($)")
ax.legend()
ax.grid(alpha=0.3)

plt.show()
