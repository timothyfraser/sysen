# slides_workshop_9_rectification.py -- Python twin of slides_workshop_9_rectification.R
# Feeds: Workshop 13 slide "Linear Rectification: what it does".
# Run from the sigma repo root:  python functions/slides_workshop_9_rectification.py
# Writes docs-v3/images/slides/workshop-9/gen_rectify_curve_py.png, gen_rectify_line_py.png
import numpy as np
import pandas as pd
from plotnine import *

red = "#B31B1B"
out = "docs-v3/images/slides/workshop-9/"

# Rectify: median-rank F, then X = ln t and Y = ln(-ln(1 - F))
cap = pd.read_csv("workshops/workshop9_capacitors.csv")
cap["F"] = (cap["i"] - 0.3) / (50 + 0.4)
cap["X"] = np.log(cap["t"])
cap["Y"] = np.log(-np.log(1 - cap["F"]))
m_hat, b_hat = np.polyfit(cap["X"], cap["Y"], 1)
c_hat = np.exp(-b_hat / m_hat)
print({"m_hat": round(m_hat, 4), "b_hat": round(b_hat, 4), "c_hat": round(c_hat, 4)})

# 1. Before: F(t_i) against t, with the fitted Weibull CDF
curve = pd.DataFrame({"t": np.linspace(0, 3000, 400)})
curve["F"] = 1 - np.exp(-(curve["t"] / c_hat) ** m_hat)
g1 = (ggplot() + geom_line(curve, aes("t", "F"), color=red, size=1.6)
      + geom_point(cap, aes("t", "F"), size=4, alpha=0.85)
      + labs(title="Before: F(t) curves in t", x="Failure time t (hours)", y="F(t), fraction failed")
      + theme_classic(base_size=26) + theme(plot_title=element_text(weight="bold", size=24)))
g1.save(out + "gen_rectify_curve_py.png", width=7, height=5.6, dpi=100, verbose=False)

# 2. After: Y against X is a straight line; read m and c off it
lab = (f"slope = m-hat = {m_hat:.2f}\nintercept = b-hat = {b_hat:.2f}\n"
       f"c-hat = e^(-b/m) = {c_hat:.0f}")
g2 = (ggplot(cap, aes("X", "Y")) + geom_abline(intercept=b_hat, slope=m_hat, color=red, size=1.6)
      + geom_point(size=4, alpha=0.85)
      + annotate("text", x=-0.4, y=-0.35, label=lab, ha="left", va="top", size=20, color=red, fontweight="bold")
      + labs(title="After: a straight line in ln t", x="X = ln t", y="Y = ln(-ln(1 - F))")
      + theme_classic(base_size=26) + theme(plot_title=element_text(weight="bold", size=24)))
g2.save(out + "gen_rectify_line_py.png", width=7, height=5.6, dpi=100, verbose=False)
