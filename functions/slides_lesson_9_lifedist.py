# slides_lesson_9_lifedist.py -- Python twin of slides_lesson_9_lifedist.R
# Run from the sigma repo root.
import numpy as np
import pandas as pd
from scipy import stats
from scipy.integrate import quad
from scipy.special import factorial, gamma as gamma_func
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

# Lognormal: f(t) and F(t) for several sigma, t in multiples of T50
# (T50 = 1, so t is in multiples of the median). PDF panel to t = 3 with the
# sigma = 5 spike near zero clipped at 2.5; CDF panel to t = 5.
sigmas = [0.2, 0.5, 1, 2, 5]
rows = []
for s in sigmas:
    t = np.concatenate([10 ** np.arange(-6, -2.49, 0.25), np.arange(0.005, 5.0001, 0.005)])
    f = stats.lognorm.pdf(t, s=s, scale=1)
    cdf = stats.lognorm.cdf(t, s=s, scale=1)
    for fn, v in [("PDF f(t)", f), ("CDF F(t)", cdf)]:
        rows.append(pd.DataFrame({"sigma": f"{s:g}", "t": t, "fn": fn, "value": v}))
ln_curves = pd.concat(rows)
ln_curves = ln_curves[~((ln_curves.fn == "PDF f(t)") & ((ln_curves.t > 3) | (ln_curves.value > 2.5)))]
ln_curves["fn"] = pd.Categorical(ln_curves.fn, ["PDF f(t)", "CDF F(t)"])
ln_curves["sigma"] = pd.Categorical(ln_curves.sigma, [f"{s:g}" for s in sigmas])

g2 = (ggplot(ln_curves, aes(x="t", y="value", color="sigma", linetype="sigma")) +
      geom_line(size=1.2) +
      facet_wrap("~fn", scales="free") +
      scale_color_manual(values=["#DE6C68", "#CC4743", red, "#7F1010", "#4A0505"]) +
      scale_linetype_manual(values=["solid", "dashed", "solid", "dashed", "solid"]) +
      labs(x="Time t (multiples of T50)", y="", color="σ", linetype="σ") +
      theme_classic(base_size=17) +
      theme(legend_position="right", strip_background=element_blank(),
            strip_text=element_text(weight="bold", size=17),
            axis_text=element_text(size=15.3),
            legend_text=element_text(size=15.3),
            legend_key_width=31,
            legend_margin=0,
            plot_margin=0.03))
# sized for the right-hand third of the slide: little whitespace, so it reads at ~377 px wide
g2.save(f"{out}/gen_lognormal_functions_py.png", width=5.2, height=3.15, dpi=150, verbose=False)

# Example 1 / 2: k = 3, lambda = 0.05, t = 24
k, lam, t = 3, 0.05, 24
terms = [(lam * t) ** n / factorial(n) * np.exp(-lam * t) for n in range(k)]
print(terms, sum(terms))
print(1 - stats.gamma.cdf(t, a=k, scale=1 / lam))
print(k / lam, k / lam ** 2)

# Example 1 by hand, term by term (the code on the Example 1 slide)
k2 = (0.05*24)**2 / factorial(2) * np.exp(-0.05*24)
k1 = (0.05*24)**1 / factorial(1) * np.exp(-0.05*24)
k0 = (0.05*24)**0 / factorial(0) * np.exp(-0.05*24)
# Key thing to know: factorial of 0 = 1.
print(np.round([k2, k1, k0], 7))               # 0.2168598 0.3614331 0.3011942
print(round(k2 + k1 + k0, 7))                  # 0.8794871

# Weibull Example 1: capacitors, c = 20000 hr
for t in [100, 1000, 20000, 30000]:
    for m in [0.5, 1, 2]:
        cdf = 100 * stats.weibull_min.cdf(t, c=m, scale=20000)
        z = 100 * 1000 * (m / 20000) * (t / 20000) ** (m - 1)
        print(t, m, round(cdf, 3), round(z, 4))

# Weibull Example 2: variable choke valve, m = 2.25, lambda = 1.15e-4 /hr
m, lam, t1, t2 = 2.25, 1.15e-4, 4380, 4380           # 6 months = 4380 hrs
print(round(np.exp(-(lam * t1) ** m), 7))             # R(4380): 0.808
print(round(gamma_func(1 / m + 1) / lam, 3))          # MTTF: 7702 hrs
print(round((1 / lam) * np.log(2) ** (1 / m), 3))     # median life t_m: 7389 hrs
print(round(np.exp(-(lam * (t1 + t2)) ** m) / np.exp(-(lam * t1) ** m), 7))  # R(t1 + t2 | t1): 0.448

# Rayleigh arm offset, sigma = 0.1, r = 0.4
print(1 - np.exp(-0.4 ** 2 / (2 * 0.1 ** 2)))

# Lognormal properties: MTTF and variance, T50 = 5000, sigma = 0.7
# The course chapter's formulas; the variance is checked by integrating
# (t - MTTF)^2 f(t) over t, so a wrong formula cannot hide here.
t50, sigma = 5000, 0.7
mttf = t50 * np.exp(sigma ** 2 / 2)
variance = t50 ** 2 * np.exp(sigma ** 2) * (np.exp(sigma ** 2) - 1)
check = quad(lambda t: (t - mttf) ** 2 * stats.lognorm.pdf(t, s=sigma, scale=t50), 0, np.inf)[0]
print({"mttf": round(mttf), "variance": round(variance), "check": round(check)})

# Lognormal: T50 = 5000, sigma = 0.7, t = 2000
print(np.log(2000 / 5000) / 0.7, stats.lognorm.cdf(2000, s=0.7, scale=5000))
