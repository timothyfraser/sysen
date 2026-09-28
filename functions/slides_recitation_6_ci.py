# slides_recitation_6_ci.py --------------------------------------------------
# Python twin of slides_recitation_6_ci.R (Recitation 6, slides 6 and 8).
# Run from the repo root:  python functions/slides_recitation_6_ci.py
import numpy as np
import pandas as pd
from scipy.stats import norm
from plotnine import *

water = pd.read_csv("workshops/onsen.csv")

# Capability Index (for centered, normal data)
def cp(sigma_s, upper, lower):
    return abs(upper - lower) / (6*sigma_s)

# Subgroup statistics (as in the chapter)
g = water.groupby("time")["temp"].agg(xbar="mean", sd="std", n_w="count")
stat = pd.DataFrame({
    "xbbar": [g["xbar"].mean()],
    "sigma_s": [np.sqrt((g["sd"]**2).mean())],
    "n": [g["n_w"].sum()],
    "n_w": [g["n_w"].iloc[0]],
    "k": [len(g)]})

# Slide 8: the z-score confidence interval for Cp
bands = stat.assign(
    # index
    estimate = lambda d: cp(sigma_s = d.sigma_s, lower = 42, upper = 50),
    # degrees of freedom
    v_short = lambda d: d.k * (d.n_w - 1),
    # standard error for cp
    se = lambda d: d.estimate * np.sqrt(1 / (2*d.v_short)),
    # z score: 97.5th percentile of the normal distribution
    z = norm.ppf(0.975),
    # upper and lower confidence interval
    lower = lambda d: d.estimate - d.z * d.se,
    upper = lambda d: d.estimate + d.z * d.se
)[["estimate", "v_short", "se", "z", "lower", "upper"]]
print(bands.round(4))

# Slide 6: the chart
bands["index"] = "Cp Index"
mychart = (ggplot(bands, aes(x = "index", y = "estimate", ymin = "lower", ymax = "upper")) +
  # benchmarks
  geom_hline(yintercept = [0, 1, 2], color = ["grey", "black", "grey"]) +
  geom_point() +
  geom_linerange() +
  theme_classic(base_size = 14) +
  coord_flip() +
  labs(y = "Index Value", x = ""))
# mychart.save("cp_ci_py.png", width = 6, height = 3, dpi = 150)
