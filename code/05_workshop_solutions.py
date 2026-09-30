# 05_workshop_solutions.py
# Tim Fraser
# Workshop 5: Statistical process control (worked solutions)
# Chapter: Statistical Process Control in Python

# Let's demo some statistical process control!
# It mirrors 05_workshop_solutions.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.

import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr + readr in R)
from plotnine import *         # visuals (ggplot2 in R)

# NOTE: R's ggpubr (for arranging several plots together) has no direct
# Python equivalent here; we show each plotnine chart on its own.

# Read in our data
water = pd.read_csv("workshops/onsen.csv")

# Let's measure the range of each subgroup, and make a nice rounded label
stat = (water
        .groupby('time', as_index=False)
        .agg(r=('temp', lambda t: abs(t.max() - t.min()))))
stat['label'] = stat['r'].round(2)

# Suppose we calculated an upper and lower specification limit, which were 11 and 3
# for simplicity, I'm just writing these in so we can demo the geom_hline function in ggplot()
line = pd.DataFrame({'upper': [11], 'lower': [3]})

# We can add horizontal lines too!
g_lines = (ggplot()
           + geom_hline(data=line, mapping=aes(yintercept='upper'), linetype="dashed")
           + geom_hline(data=line, mapping=aes(yintercept='lower'), linetype="dashed")
           + geom_line(data=stat, mapping=aes(x='time', y='r'))
           + geom_point(data=stat, mapping=aes(x='time', y='r'),
                        size=5, shape='o', fill="white", color="black")
           # + geom_text(data=stat, mapping=aes(x='time', y='r + 0.5', label='label'))
           + geom_label(data=stat, mapping=aes(x='time', y='r', label='label')))
g_lines


# Or, we can visualize the whole process in g1 and g2
g1 = (ggplot()
      # + geom_point(data=water, mapping=aes(x='time', y='temp'))
      + geom_jitter(data=water, mapping=aes(x='time', y='temp'),
                    width=0.25))

g2 = (ggplot()
      + geom_histogram(data=water, mapping=aes(x='temp'))
      + coord_flip()
      + labs(x=""))

# Combine them!
# In R, ggarrange(g1, g2) puts them side by side.
# plotnine has no ggarrange(), so we draw them in turn.
g1
g2


# Let's calculate sigma_s and sigma_t!
sig = (water
       .groupby('time', as_index=False)
       .agg(xbar=('temp', 'mean'),
            r=('temp', lambda t: t.max() - t.min()),
            sd=('temp', 'std'),
            nw=('temp', 'size')))
sig['df'] = sig['nw'] - 1
# How to get sigma-short!
#   we're trying to pool the standard deviation from all these different subgroups
#   to approximate the average standard deviation
sig['sigma_s'] = np.sqrt((sig['df'] * sig['sd'] ** 2).sum() / sig['df'].sum())
#    sig['sigma_s'] = np.sqrt((sig['sd'] ** 2).mean())
sig['sigma_t'] = water['temp'].std()
sig['se'] = sig['sigma_s'] / np.sqrt(sig['nw'])
sig['upper'] = sig['xbar'].mean() + 3 * sig['se']
sig['lower'] = sig['xbar'].mean() - 3 * sig['se']
print(sig)


# How do we approximate sigma-short?
def dn(n=12, reps=10000):
    # For 10,000 reps,
    # simulate the ranges of n values (one row of n draws per rep)
    draws = np.random.normal(loc=0, scale=1, size=(reps, n))
    r = np.abs(draws.max(axis=1) - draws.min(axis=1))
    # And calculate...
    # Mean range
    d2 = r.mean()
    # standard deviation of ranges
    d3 = r.std(ddof=1)
    # and constants for obtaining lower and upper ci for rbar
    D3 = 1 - 3 * (d3 / d2)  # sometimes written D3
    D4 = 1 + 3 * (d3 / d2)  # sometimes written D4
    # Sometimes D3 goes negative; we need to bound it at zero
    D3 = 0 if D3 < 0 else D3
    return pd.DataFrame({'d2': [d2], 'd3': [d3], 'D3': [D3], 'D4': [D4]})


print(dn(n=12))


# Let's write a function bn() to calculate our B3 and B4 statistics for any subgroup size n
def bn(n, reps=10000):
    draws = np.random.normal(loc=0, scale=1, size=(reps, n))
    s = draws.std(axis=1, ddof=1)
    b2 = s.mean()
    b3 = s.std(ddof=1)
    C4 = b2  # this is sometimes called C4
    A3 = 3 / (b2 * np.sqrt(n))
    B3 = 1 - 3 * b3 / b2
    B4 = 1 + 3 * b3 / b2
    # bound B3 at 0, since we can't have a standard deviation below 0
    B3 = 0 if B3 < 0 else B3
    return pd.DataFrame({'b2': [b2], 'b3': [b3], 'C4': [C4], 'A3': [A3],
                         'B3': [B3], 'B4': [B4]})

# For a subgroup of size 12
stat = bn(n=12)
# Statistic of interest
sbar = 2.5
# Lower Control Limit
print(sbar * stat['B3'])
# Upper control limit
print(sbar * stat['B4'])
