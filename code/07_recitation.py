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


def get_chisq(t=None, binwidth=5, data=None, n_total=None, f=None, np_=1, **kwargs):
    """
    Function to Get Chi-Squared!
    Tim Fraser

    If observed vector...
      t         a vector of times to failure
      binwidth  size of intervals (eg. 5 hours) (Only if t is provided)
    If cross-tabulated data...
      data      a data.frame with the vectors `lower`, `upper`, and `r_obs`
    Common Parameters:
      n_total   total number of units.
      f         specific failure function, such as `f = f(t, lambda_)`
      np_       total number of parameters in your function (eg. if exponential, 1 (lambda))
      **kwargs  fill in here any named parameters you need, like `lambda_ = 2.4`
                or `rate = 2.3` or `mean = 0, sd = 2`
    """

    # If vector `t` is NOT None
    # Do the raw data route
    if t is not None:

        # Make a data frame called 'tab'
        tab = pd.DataFrame({"t": t})
        # Part 1.1: Split into bins
        tab["interval"] = cut_interval(tab["t"], length=binwidth)
        # Part 1.2: Tally up observed failures 'r_obs' by bin
        # (observed=False keeps empty bins, like .drop = FALSE in R)
        tab = (tab.groupby("interval", observed=False)
               .size().reset_index(name="r_obs"))
        # Let's repeat our process from before!
        tab["bin"] = np.arange(1, len(tab) + 1)
        tab["lower"] = (tab["bin"] - 1) * binwidth
        tab["upper"] = tab["bin"] * binwidth
        tab["midpoint"] = (tab["lower"] + tab["upper"]) / 2

    # Otherwise, if data.frame `data` is NOT None
    # Do the cross-tabulated data route
    elif data is not None:
        tab = data.copy()
        tab["bin"] = np.arange(1, len(tab) + 1)
        tab["midpoint"] = (tab["lower"] + tab["upper"]) / 2

    # Part 2. Calculate probabilities by interval
    tab["p_upper"] = f(tab["upper"], **kwargs)  # supplied parameters
    tab["p_lower"] = f(tab["lower"], **kwargs)  # supplied parameters
    tab["p_fail"] = tab["p_upper"] - tab["p_lower"]
    tab["n_total"] = n_total
    tab["r_exp"] = tab["n_total"] * tab["p_fail"]

    # Part 3-4: Calculate Chi-Squared statistic and p-value
    chisq = ((tab["r_obs"] - tab["r_exp"]) ** 2 / tab["r_exp"]).sum()
    nbin = len(tab)
    df = nbin - np_ - 1
    output = pd.DataFrame({
        "chisq": [chisq],
        "nbin": [nbin],
        "np": [np_],
        "df": [df],
        "p_value": [1 - stats.chi2.cdf(chisq, df=df)]
    })

    return output

lambda_ = 1 / masks["fabric"].mean()

# get_chisq() hands back only the TEST result: chisq, nbin, np, df, p_value.
# To plot observed against expected we need the binned table itself, which is
# the same Step 1 + Step 2 crosstab the chapter walks through by hand.
dat = pd.DataFrame({"t": masks["fabric"]})
dat["interval"] = cut_interval(dat["t"], length=750)
dat = dat.groupby("interval", observed=False).size().reset_index(name="r_obs")
dat["bin"] = np.arange(1, len(dat) + 1)
dat["lower"] = (dat["bin"] - 1) * 750
dat["upper"] = dat["bin"] * 750
dat["p_upper"] = f(dat["upper"], lambda_=lambda_)
dat["p_lower"] = f(dat["lower"], lambda_=lambda_)
dat["p_fail"] = dat["p_upper"] - dat["p_lower"]
dat["n_total"] = 50
dat["r_exp"] = dat["n_total"] * dat["p_fail"]
dat = dat[["interval", "r_obs", "p_fail", "n_total", "r_exp"]]



g1 = (ggplot() +
  geom_col(data=dat, mapping=aes(x="interval", y="r_obs")) +
  geom_point(data=dat, mapping=aes(x="interval", y="r_obs")) +
  geom_col(data=dat, mapping=aes(x="interval", y="r_exp"),
           alpha=0.5, fill="darksalmon") +
  geom_point(data=dat, mapping=aes(x="interval", y="r_exp"),
             alpha=0.5, fill="darksalmon"))
g1


print(pd.DataFrame({"chisq": [((dat["r_obs"] - dat["r_exp"]) ** 2 / dat["r_exp"]).sum()]}))


def f(t, lambda_):
    return 1 - np.exp(-t * lambda_)
lambda_ = 1 / masks["fabric"].mean()
print(get_chisq(t=masks["fabric"], binwidth=750,
                n_total=50, f=f, np_=1, lambda_=lambda_))



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
g2 = (ggplot(pd.DataFrame({"x": stats.chi2.rvs(df=3, size=1000)}), aes(x="x")) +
      geom_histogram(bins=30))
g2



g3 = (ggplot() +
  geom_histogram(data=pd.DataFrame({"x": stats.chi2.rvs(df=3, size=1000)}),
                 mapping=aes(x="x"), bins=30) +
  geom_vline(xintercept=10, color="red"))
g3



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

print(get_chisq(data=dat, n_total=50, f=f, np_=1, lambda_=0.01))
print(get_chisq(data=dat, n_total=50, f=pexp, np_=1, rate=0.01))
# (our Python ppois() calls its mean `mu`, where R's calls it `lambda`)
print(get_chisq(data=dat, n_total=50, f=ppois, np_=1, mu=masks["fabric"].mean()))
print(get_chisq(data=dat, n_total=50, f=pnorm, np_=2,
                mean=masks["fabric"].mean(), sd=masks["fabric"].std()))
print(get_chisq(data=dat, n_total=50, f=pweibull, np_=2,
                shape=0.01, scale=masks["fabric"].mean()))
