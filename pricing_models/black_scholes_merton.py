import math
from statistics import stdev

# single source of truth: our base z-score range, -3 to 3 inclusive.
# everything below flows from this one array.
base = [-3, -2, -1, 0, 1, 2, 3]     # 0 == current price, arr of standard deviations


def phi(x):
    """Shape of the bell curve, central limit theorem"""
    return 1/ math.sqrt(2 * math.pi) * math.exp(-x ** 2 / 2)


print("Phi: the shape of a bell curve\n")
print(f"{'x':>4} | {'phi(x)':>8} | height")
print("-" * 40)
for x in base:
    height = phi(x)
    bar = "#" * round(height * 50)   # scaled bar so the peak is tall
    print(f"{x:>4} | {height:>8.4f} | {bar}")


def N(x):
    """Cumulative area under the bell curve, integral establishing change"""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


print("\nN: the area to the LEFT of x (a probability, 0 -> 1)\n")
print(f"{'x':>4} | {'N(x)':>8} | bucket fill")
print("-" * 40)
for x in base:
    area = N(x)
    bar = "#" * round(area * 30)   # scaled bar so full (1.0) is wide
    print(f"{x:>4} | {area:>8.4f} | {bar}")


def naieve_d1():
    ...

def naive_d2(d1_values, volatility, tau):
    """Shifts z-scores down by one measure of volatility sqrt(tau)"""
    shift = volatility * math.sqrt(tau)
    return [d1 - shift for d1 in d1_values]


d1_values = base   # naive d1: the base range, unchanged
d2_values = naive_d2(d1_values, volatility=0.20, tau=0.25)

print("\nNaive d1 -> d2   (shift = sigma*sqrt(tau) = 0.10)\n")
print(f"{'d1':>6} | {'d2':>6}")
print("-" * 16)
for a, b in zip(d1_values, d2_values):
    print(f"{a:>6.2f} | {b:>6.2f}")


def call_price(S, K, r, tau, d1, d2):
    """Call price: what you receive (stock leg) minus what you pay (strike leg)."""
    receive = S * N(d1)                     # stock leg, weighted by delta = N(d1)
    pay = K * math.exp(-r * tau) * N(d2)    # strike leg, discounted & weighted by P(ITM)
    return receive - pay


S, K, r, tau = 100, 100, 0.05, 0.25
print(f"\nNaive call price   (S={S}  K={K}  r={r}  tau={tau})\n")
print(f"{'d1':>6} | {'d2':>6} | {'N(d1)':>7} | {'N(d2)':>7} | {'price':>8}")
print("-" * 48)
for d1, d2 in zip(d1_values, d2_values):
    price = call_price(S, K, r, tau, d1, d2)
    print(f"{d1:>6.2f} | {d2:>6.2f} | {N(d1):>7.4f} | {N(d2):>7.4f} | {price:>8.4f}")
