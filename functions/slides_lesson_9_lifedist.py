# slides_lesson_9_lifedist.py -- Python twin of slides_lesson_9_lifedist.R
# Run from the sigma repo root.
import numpy as np
import pandas as pd
from math import factorial
from scipy import stats
from plotnine import *

out = "docs-v3/images/slides/lesson-9"
red = "#B31B1B"

# Gamma: f(t), R(t), z(t) for several k, lambda = 1
rows = []
for k in [0.5, 1, 2, 3]:
    t = np.arange(0.01, 6.001, 0.01)
    f = stats.gamma.pdf(t, a=k, scale=1)
    r = 1 - stats.gamma.cdf(t, a=k, scale=1)
    for fn, v in [("PDF f(t)", f), ("Reliability R(t)", r), ("Failure rate z(t)", f / r)]:
        rows.append(pd.DataFrame({"k": f"k = {k:g}", "t": t, "fn": fn, "value": v}))
curves = pd.concat(rows)
curves = curves[curves.value <= 2.5]
curves["fn"] = pd.Categorical(curves.fn, ["PDF f(t)", "Reliability R(t)", "Failure rate z(t)"])

g = (ggplot(curves, aes(x="t", y="value", color="k")) +
     geom_line(size=1.4) +
     facet_wrap("~fn", scales="free_y") +
     scale_color_manual(values=["#E8A0A0", "#D05050", red, "#4A0A0A"]) +
     labs(x="Time t (lambda = 1)", y="", color="") +
     theme_classic(base_size=20) +
     theme(legend_position="bottom", strip_background=element_blank()))
g.save(f"{out}/gen_gamma_functions_py.png", width=13, height=5.2, dpi=150, verbose=False)

# Example 1 / 2: k = 3, lambda = 0.05, t = 24
k, lam, t = 3, 0.05, 24
terms = [(lam * t) ** n / factorial(n) * np.exp(-lam * t) for n in range(k)]
print(terms, sum(terms))
print(1 - stats.gamma.cdf(t, a=k, scale=1 / lam))
print(k / lam, k / lam ** 2)

# Weibull Example 1: capacitors, c = 20000 hr
for t in [100, 1000, 20000, 30000]:
    for m in [0.5, 1, 2]:
        cdf = 100 * stats.weibull_min.cdf(t, c=m, scale=20000)
        z = 100 * 1000 * (m / 20000) * (t / 20000) ** (m - 1)
        print(t, m, round(cdf, 3), round(z, 4))
# Rayleigh arm offset, sigma = 0.1, r = 0.4
print(1 - np.exp(-0.4 ** 2 / (2 * 0.1 ** 2)))
# Lognormal: T50 = 5000, sigma = 0.7, t = 2000
print(np.log(2000 / 5000) / 0.7, stats.lognorm.cdf(2000, s=0.7, scale=5000))
