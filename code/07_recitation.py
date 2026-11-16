# 07_recitation.py
# Tim Fraser
# Recitation 7: Chi-squared goodness-of-fit tests
# Chapter: Statistical Techniques for Exponential Distributions in Python

# This is the Python twin of 07_recitation.R, section by section.
# Run it from the top of the sysen folder, so the file paths below work.

import sys
import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr + readr in R)
from plotnine import *         # visuals (ggplot2 in R)
from scipy import stats        # pchisq() / rchisq() in R live in scipy.stats

# Our course functions live in functions/ at the repo root.
# They give us R-style pexp(), ppois(), pnorm(), pweibull().
sys.path.append("functions")
from functions_distributions import pexp, ppois, pnorm, pweibull
# get_chisq() and the helpers it calls live in functions_mle.py
from functions_mle import get_chisq, _chisq_cells, _pool_cells

# NOTE: `lambda` is a reserved word in Python (it makes tiny anonymous
# functions), so we can't name a variable `lambda`. We write `lambda_` instead.
# NOTE: we also call our parameter count `np_` because `np` is numpy.

masks = pd.read_csv("workshops/masks.csv")


# TESTING VALUES
t = masks["fabric"]
n_total = 50
binwidth = 750
def f(t, lambda_):
    return 1 - np.exp(-t * lambda_)
np_ = 1


# ggplot2's cut_interval(t, length = binwidth) makes equal-width bins
# that line up on multiples of binwidth, closed on the right: [0,750], (750,1500], ...
# This helper does the same with pd.cut().
def cut_interval(t, length):
    lo = np.floor(t.min() / length) * length
    hi = np.ceil(t.max() / length) * length
    breaks = np.arange(lo, hi + length, length)
    return pd.cut(t, bins=breaks, right=True, include_lowest=True)


lambda_ = 1 / masks["fabric"].mean()

# get_chisq() hands back only the TEST result: chisq, nbin, np, df, p_value, min_exp.
# To plot observed against expected we need the table of cells itself:
# Step 1 (crosstab), Step 2-3 (expected counts, plus a last cell to infinity
# for the units that had not failed), Step 4 (merge cells until each expects at least 5).
tab = pd.DataFrame({"t": t})
tab["interval"] = cut_interval(tab["t"], length=binwidth)
tab = tab.groupby("interval", observed=False).size().reset_index(name="r_obs")
tab["bin"] = np.arange(1, len(tab) + 1)
tab["lower"] = (tab["bin"] - 1) * binwidth
tab["upper"] = tab["bin"] * binwidth

dat = _pool_cells(_chisq_cells(tab, n_total=n_total, f=f, lambda_=lambda_))
dat["cell"] = dat["lower"].astype(str) + "-" + dat["upper"].astype(str)
dat["cell"] = pd.Categorical(dat["cell"], categories=dat["cell"], ordered=True)

(ggplot() +
  geom_col(data=dat, mapping=aes(x="cell", y="r_obs")) +
  geom_point(data=dat, mapping=aes(x="cell", y="r_obs")) +
  geom_col(data=dat, mapping=aes(x="cell", y="r_exp"),
           alpha=0.5, fill="darksalmon") +
  geom_point(data=dat, mapping=aes(x="cell", y="r_exp"),
             alpha=0.5, fill="darksalmon") +
  labs(x="cell", y="units"))

# Step 5: Chi-squared statistic from the merged cells
print(pd.DataFrame({"chisq": [((dat["r_obs"] - dat["r_exp"]) ** 2 / dat["r_exp"]).sum()]}))

# The same test in one call
print(get_chisq(t=masks["fabric"], binwidth=750,
                n_total=50, f=f, np=1, lambda_=lambda_))


# chisq
# n_total - total number of observation
# np - total # of parameters
# lambda - our parameter (failure rate)
# f - exponential - CDF - failure function
# binwidth - size of interval
# df -
# p_value


# Reminders
# TA Evals


# rchisq() in R is stats.chi2.rvs() in Python
(ggplot(pd.DataFrame({"x": stats.chi2.rvs(df=3, size=1000)}), aes(x="x")) +
  geom_histogram(bins=30))



(ggplot() +
  geom_histogram(data=pd.DataFrame({"x": stats.chi2.rvs(df=3, size=1000)}),
                 mapping=aes(x="x"), bins=30) +
  geom_vline(xintercept=10, color="red"))



# R's tribble() writes a table row by row; in Python a list of rows does the same
dat = pd.DataFrame(
    [[0,   100, 50],
     [100, 200, 43],
     [200, 300, 20],
     [300, 400, 10],
     [400, 500, 5]],
    columns=["lower", "upper", "r_obs"])

dat = pd.DataFrame({
    "lower": [0, 100, 200, 300, 400],
    "upper": [100, 200, 300, 400, 500],
    "r_obs": [50, 43, 20, 10, 5]
})

print(get_chisq(data=dat, n_total=128, f=f, np=1, lambda_=0.01))
print(get_chisq(data=dat, n_total=128, f=pexp, np=1, rate=0.01))
# (our Python ppois() calls its mean `mu`, where R's calls it `lambda`)
print(get_chisq(data=dat, n_total=128, f=ppois, np=1, mu=masks["fabric"].mean()))
print(get_chisq(data=dat, n_total=128, f=pnorm, np=2,
                mean=masks["fabric"].mean(), sd=masks["fabric"].std()))
print(get_chisq(data=dat, n_total=128, f=pweibull, np=2,
                shape=0.01, scale=masks["fabric"].mean()))
