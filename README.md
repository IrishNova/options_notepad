# options_notepad

A personal notepad for building out **all things options** — pricing models, Greeks,
implied-vol experiments, payoff diagrams, and whatever small ideas I want to tinker with.

This is a public, open-ended scratch space. Nothing here is production or financial advice —
just me working through options concepts in code.

## Environment

- **Python:** 3.12
- **Virtual environment:** `.venv/` (git-ignored — recreate it locally, see below)

## Setup

```bash
# Clone
git clone <your-repo-url> options_notepad
cd options_notepad

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Opening in PyCharm

1. **Open** this folder as a project.
2. PyCharm should detect `.venv/` automatically. If not:
   *Settings → Project → Python Interpreter → Add Interpreter → Existing* → point it at
   `.venv/bin/python`.
3. Start tinkering.

## What's installed

| Package | Why it's here |
|---|---|
| `numpy`, `pandas`, `scipy` | Core numeric / data stack |
| `matplotlib`, `seaborn` | Plotting payoffs, vol surfaces, etc. |
| `py_vollib` | Black-Scholes pricing, implied vol, Greeks |
| `statsmodels` | Stats / modeling |
| `yfinance` | Quick-and-dirty market data for experiments |
| `jupyterlab`, `ipykernel` | Interactive notebooks |

## A quick sanity check

```python
from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.greeks.analytical import delta

price = black_scholes(flag='c', S=100, K=100, t=0.25, r=0.01, sigma=0.20)
d = delta('c', S=100, K=100, t=0.25, r=0.01, sigma=0.20)
print(f"Call price: {price:.4f}  |  delta: {d:.4f}")
```

## Conventions

- Keep dependencies in `requirements.txt`.
- The virtual environment and IDE settings stay out of git (see `.gitignore`).
- No rigid structure — add files as the ideas come.
