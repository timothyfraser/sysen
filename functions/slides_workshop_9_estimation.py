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
g1.save(out + "gen_weibull_pdf_py.png", width=7, height=4.2, dpi=100, verbose=False)

grid = pd.DataFrame({"lam": np.linspace(0.004, 0.04, 300)})
grid["loglik"] = [ll(crops["days"], l) for l in grid["lam"]]
g2 = (ggplot(grid, aes("lam", "loglik")) + geom_line(color="#B31B1B", size=1.3)
      + geom_vline(xintercept=best, linetype="dashed")
      + annotate("text", x=best, y=grid["loglik"].min(), label=str(round(best, 5)), ha="left", size=20)
      + labs(x="Rate parameter lambda", y="Log-likelihood")
      + theme_classic(base_size=30))
g2.save(out + "gen_loglik_py.png", width=6.4, height=5.2, dpi=100, verbose=False)
