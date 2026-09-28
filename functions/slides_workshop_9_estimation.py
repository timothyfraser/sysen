# slides_workshop_9_estimation.py -- Python twin of slides_workshop_9_estimation.R
# Run from the sigma repo root:  python functions/slides_workshop_9_estimation.py
import numpy as np
import pandas as pd
from plotnine import *

out = "docs-v3/images/slides/workshop-9/"

# crops.csv: exponential log-likelihood and its maximum
crops = pd.read_csv("workshops/crops.csv")
def ll(data, lam):
    return np.log(lam * np.exp(-lam * data)).sum()
best = 1 / crops["days"].mean()
print("crops MLE lambda =", best, " loglik =", ll(crops["days"], best))

# Example 1: linear rectification of the Weibull
cap = pd.read_csv("workshops/workshop9_capacitors.csv")
cap["F"] = (cap["i"] - 0.3) / (50 + 0.4)
cap["X"] = np.log(cap["t"])
cap["Y"] = np.log(-np.log(1 - cap["F"]))
m_hat, b_hat = np.polyfit(cap["X"], cap["Y"], 1)
c_hat = np.exp(-b_hat / m_hat)
print({"m_hat": round(m_hat, 4), "b_hat": round(b_hat, 4), "c_hat": round(c_hat, 4)})

# Charts (twins of the ggplot figures)
from scipy.stats import weibull_min
x = np.linspace(0.01, 3, 300)
w = pd.concat([pd.DataFrame({"x": x, "density": weibull_min.pdf(x, m), "m": str(m)}) for m in [0.5, 1, 2, 4, 10]])
g1 = (ggplot(w, aes("x", "density", color="m")) + geom_line(size=1.3) + coord_cartesian(ylim=(0, 2.5))
      + labs(x="Time (multiples of characteristic life c)", y="Density f(t)", color="Shape m")
      + theme_classic(base_size=20))
g1.save("/tmp/claude-0/-home-user/9448d86e-70dd-536d-9568-1f17c80db478/scratchpad/D22/py_weibull_pdf.png", width=7, height=4.2, dpi=100, verbose=False)
