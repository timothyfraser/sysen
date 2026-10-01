# 06_recitation_solutions.py
# Tim Fraser
# Recitation 6: Capability and performance indices (worked solutions)
# Chapter: Indices and Confidence Intervals for Statistical Process Control in Python

# This is the Python twin of 06_recitation_solutions.R, section by section.
# Run it from the top of the sysen folder, so the file paths below work.

import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr + readr in R)
from plotnine import *         # visuals (ggplot2 in R)
import sys
# Load our R-style distribution helpers (qnorm() works just like in R)
sys.path.append("functions")
from functions_distributions import qnorm


water = pd.read_csv("workshops/onsen.csv")

# Capability Index (for centered, normal data)
def cp(sigma_s, upper, lower):
    return abs(upper - lower) / (6 * sigma_s)

# Process Performance Index (for centered, normal data)
def pp(sigma_t, upper, lower):
    return abs(upper - lower) / (6 * sigma_t)

# Capability Index (for skewed, uncentered data)
def cpk(mu, sigma_s, lower=None, upper=None):
    if lower is not None:
        a = abs(mu - lower) / (3 * sigma_s)
    if upper is not None:
        b = abs(upper - mu) / (3 * sigma_s)
    # We can also write if else statements like this
    # If we got both stats, return the min!
    if lower is not None and upper is not None:
        return min(a, b)
    # If we got just the upper stat, return b (for upper)
    elif lower is None:
        return b
    # If we got just the lower stat, return a (for lower)
    elif upper is None:
        return a


# Process Performance Index (for skewed, uncentered data)
def ppk(mu, sigma_t, lower=None, upper=None):
    if lower is not None:
        a = abs(mu - lower) / (3 * sigma_t)
    if upper is not None:
        b = abs(upper - mu) / (3 * sigma_t)
    # We can also write if else statements like this
    # If we got both stats, return the min!
    if lower is not None and upper is not None:
        return min(a, b)
    # If we got just the upper stat, return b (for upper)
    elif lower is None:
        return b
    # If we got just the lower stat, return a (for lower)
    elif upper is None:
        return a


# For example
print(ppk(mu=2, sigma_t=2.5, lower=2.1))




# Theoretical sampling distributions
# (NOTE: pandas .std() uses n - 1 by default, just like R's sd())
by_time = (water.groupby("time")
           .agg(xbar=("temp", "mean"),
                s=("temp", "std"),
                n_w=("temp", "size"))
           .reset_index())

stat = pd.DataFrame({
    "xbbar": [by_time["xbar"].mean()],              # grand mean x-double-bar
    "sigma_s": [np.sqrt((by_time["s"] ** 2).mean())],  # sigma_short
    "sigma_t": [water["temp"].std()],               # sigma_total!
    "n": [by_time["n_w"].sum()],                    # or just n = len(water)   # Total sample size
    "n_w": [by_time["n_w"].unique()[0]],
    "k": [by_time["time"].nunique()]                # Get total subgroups
})


# Capability Index (for centered, normal data)
def cp(sigma_s, upper, lower):
    return abs(upper - lower) / (6 * sigma_s)



bands = stat.copy()
bands["limit_lower"] = 42
bands["limit_upper"] = 50
# index
bands["estimate"] = cp(sigma_s=bands["sigma_s"], lower=bands["limit_lower"], upper=bands["limit_upper"])
# Get our extra quantities of interest
bands["v_short"] = bands["k"] * (bands["n_w"] - 1)  # get degrees of freedom
# Get standard error for estimate
bands["se"] = bands["estimate"] * np.sqrt(1 / (2 * bands["v_short"]))
# Get z score
bands["z"] = qnorm(0.975)  # get position of 97.5th percentile in normal distribution
bands["lower"] = bands["estimate"] - bands["z"] * bands["se"]
bands["upper"] = bands["estimate"] + bands["z"] * bands["se"]
# (summarize() in R keeps only the new columns)
bands = bands[["limit_lower", "limit_upper", "estimate", "v_short", "se", "z", "lower", "upper"]]

print(bands)
# Check it!
print(stat)


# Why qnorm(0.975) rather than qnorm(0.95)? ###############################
# A TWO-sided 95% interval splits alpha = 0.05 across both tails
# (0.025 low + 0.025 high), so each end sits at the 97.5th percentile:
# qnorm(0.975), about 1.96. That is what `bands` above computes.
#
# But the question we actually care about here is ONE-directional:
# "is Cp below 1?" For that, report a one-sided UPPER bound (a ceiling):
# put ALL of alpha in the upper tail, so use qnorm(0.95), about 1.645.
# (A floor - "Cp is at least..." - would be a one-sided LOWER bound,
# estimate - z * se, with the same qnorm(0.95).)
# See the chapter's "One-Sided Bounds" subsection:
# https://timothyfraser.com/sigma/chapters/indices-and-confidence-intervals-for-statistical-process-control-in-python.html#one-sided-bounds

alpha = 0.05  # 95% confidence

ceiling_cp = pd.DataFrame({
    "estimate": cp(sigma_s=stat["sigma_s"], lower=42, upper=50)
})
ceiling_cp["v_short"] = stat["k"] * (stat["n_w"] - 1)  # degrees of freedom
ceiling_cp["se"] = ceiling_cp["estimate"] * np.sqrt(1 / (2 * ceiling_cp["v_short"]))
# ALL of alpha in one tail: the 95th percentile, not the 97.5th
ceiling_cp["z"] = qnorm(1 - alpha)  # about 1.645
ceiling_cp["upper"] = ceiling_cp["estimate"] + ceiling_cp["z"] * ceiling_cp["se"]  # a ceiling: "Cp is at most..."

print(ceiling_cp)
# The 95% one-sided upper bound (about 0.735) is still well below 1,
# so we are 95% confident the true Cp is LESS THAN 1: not capable.
# It is a little tighter than the two-sided upper end in `bands`
# (about 0.747), because no alpha was spent on the low tail.
