import math


def phi(x):
    """Shape of the bell curve, central limit theorem"""
    return 1/ math.sqrt(2 * math.pi) * math.exp(-x ** 2 / 2)


def N(x):
    """
    Cumulative area under the bell curve, sum of all bars, an integral.
    How much of the area under the normal distribution to that point (point=z-score) takes up.
    This returns Delta: how much a contract moves in relation to a $1 move in the underlying.
    """

    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def naive_d2(d1_values, volatility, tau):
    """Shifts z-scores down by one measure of volatility sqrt(tau)"""
    shift = volatility * math.sqrt(tau)
    return [d1 - shift for d1 in d1_values]


def call_price(S, K, r, tau, d1, d2):
    """Call price: what you receive (stock leg) minus what you pay (strike leg)."""
    receive = S * N(d1)                     # stock leg: price x delta = $ value of stock you expect to receive | the N(d1) shares you HOLD, in $
    pay = K * math.exp(-r * tau) * N(d2)    # strike leg: discounted strike x P(ITM) = $ you expect to pay | the $ you BORROW at the risk-free rate to fund it
    return receive - pay                    # present value of expected payoff


def d1(S, K, r, tau, sigma):
    """The upper z-score: how far spot sits ABOVE the strike, measured in
    bell-widths (sigma*sqrt(tau)), after tilting the center up by the drift
    (r + 1/2 sigma^2)*tau.

    It answers: "how many standard deviations is the strike from today's
    drift-adjusted price?" Run through N(), it becomes delta = N(d1) -- the
    slope of the price curve, i.e. the shares to hold to replicate the call.
    """
    return ((math.log(S/K)                  # gap to strike, in log terms
            + (r + 0.5 * sigma**2) * tau)   # the drift (risk-free growth r plus the log normal nudge)
            / (sigma * math.sqrt(tau)))     # the bell width


def d2(S, K, r, tau, sigma):
    """d2 = d1 shifted down by one bell-width (sigma*sqrt(tau))."""
    return d1(S, K, r, tau, sigma) - sigma * math.sqrt(tau)


def delta(S, K, r, tau, sigma):
    """Delta = N(d1): the slope of the price curve. Shares to hold per option,
    and how many dollars the call moves per $1 move in the stock. Lives in 0..1."""
    return N(d1(S, K, r, tau, sigma))


def gamma(S, K, r, tau, sigma):
    """Gamma = how fast delta changes per $1 move in the stock (delta's slope,
    price's curvature). Highest near the strike, fades deep ITM/OTM."""
    return phi(d1(S, K, r, tau, sigma)) / (S * sigma * math.sqrt(tau))


def vega(S, K, r, tau, sigma):
    """Vega = how much the option's PRICE changes per unit change in volatility
    (dPrice/dsigma). This is per 1.00 of sigma; divide by 100 for the usual
    "$ per 1 vol point" trader quote. Peaks ATM, grows with sqrt(tau) -- more
    time to expiry = more vega. Same for calls and puts."""
    return S * phi(d1(S, K, r, tau, sigma)) * math.sqrt(tau)


if __name__ == "__main__":
    # single source of truth: our base z-score range, -3 to 3 inclusive.
    # everything below flows from this one array.
    base = [-3, -2, -1, 0, 1, 2, 3]     # 0 == current price, arr of standard deviations

    print("Phi: the shape of a bell curve\n")
    print(f"{'x':>4} | {'phi(x)':>8} | height")
    print("-" * 40)
    for x in base:
        height = phi(x)
        bar = "#" * round(height * 50)   # scaled bar so the peak is tall
        print(f"{x:>4} | {height:>8.4f} | {bar}")

    print("\nN: the area to the LEFT of x (a probability, 0 -> 1)\n")
    print(f"{'x':>4} | {'N(x)':>8} | bucket fill")
    print("-" * 40)
    for x in base:
        area = N(x)
        bar = "#" * round(area * 30)   # scaled bar so full (1.0) is wide
        print(f"{x:>4} | {area:>8.4f} | {bar}")

    d1_values = base   # naive d1: the base range, unchanged
    d2_values = naive_d2(d1_values, volatility=0.20, tau=0.25)

    print("\nNaive d1 -> d2   (shift = sigma*sqrt(tau) = 0.10)\n")
    print(f"{'d1':>6} | {'d2':>6}")
    print("-" * 16)
    for a, b in zip(d1_values, d2_values):
        print(f"{a:>6.2f} | {b:>6.2f}")

    S, K, r, tau = 100, 100, 0.05, 0.25
    print(f"\nNaive call price   (S={S}  K={K}  r={r}  tau={tau})\n")
    print(f"{'d1':>6} | {'d2':>6} | {'N(d1)':>7} | {'N(d2)':>7} | {'price':>8}")
    print("-" * 48)
    for d1_naive, d2_naive in zip(d1_values, d2_values):
        price = call_price(S, K, r, tau, d1_naive, d2_naive)
        print(f"{d1_naive:>6.2f} | {d2_naive:>6.2f} | {N(d1_naive):>7.4f} | {N(d2_naive):>7.4f} | {price:>8.4f}")

    # dummy stock prices centered on $100, to feed the real d1
    prices = list(range(80, 121, 5))   # [80, 85, 90, ..., 115, 120]

    sigma = 0.20
    print(f"\nReal Black-Scholes price sweep   (K={K}  r={r}  tau={tau}  sigma={sigma})\n")
    print(f"{'S':>5} | {'d1':>7} | {'d2':>7} | {'N(d1)':>6} | {'N(d2)':>6} | {'call':>7}")
    print("-" * 54)
    for S_i in prices:
        # Two metrics, measuring the same thing: how far the strike in question is, away from the drift-price, on a normal distribution, centered on the current price
        a = d1(S_i, K, r, tau, sigma)   # z-score of how far the strike is away from the center of the distribution, N(d1) = Delta
        b = d2(S_i, K, r, tau, sigma)   # z-score used to determine the N(d2) probability the strike finishes ITM
        call = call_price(S_i, K, r, tau, a, b)
        print(f"{S_i:>5} | {a:>7.3f} | {b:>7.3f} | {N(a):>6.3f} | {N(b):>6.3f} | {call:>7.3f}")
