# 06_workshop_extra.py
# Tim Fraser
# Workshop 6 extra: capability indices and bootstrap CIs
# Chapter: Indices and Confidence Intervals for Statistical Process Control in Python


# EXERCISE 1 - Writing a Function #####################

def f(Eu, El, sd):
    cp = (Eu - El) / (6 * sd)
    return cp

# roxygen2-style commenting for functions

# @name f
# @title Cp Process Control Index Function
# @description
# Calculate any Cp statistic with just 3 inputs! Yay!
# @param Eu Upper Specification Limit
# @param El Lower Specification Limit
# @param sd Sigma-short (average within group standard deviation)
def f(Eu, El, sd):
    cp = (Eu - El) / (6 * sd)
    return cp


f(Eu=10, El=2, sd=5)

# EXERCISE 2 ###################################
import pandas as pd
import numpy as np
from plotnine import *
from scipy.stats import norm
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_process_control import cp, pp, cpk, ppk

water = pd.read_csv("workshops/onsen.csv")
water.head()
water.info()






# EXERCISE 3 #####################################


# What's bootstrapping?
# Take the existing data
# Sample with Replacement for the entire data
# Calculate a Stat
# Get a stat that has been slightly influenced by random chance



water = pd.read_csv("workshops/onsen.csv")

pd.DataFrame({'sigma_t': [water['temp'].std()]})


# We need 1000 standard deviations
# We need 1000 resampled water datasets
# We need 1000 water datasets --- x
# We need a dataframe of 1000 ids -- x

n = len(water)
reps = 1000
sigma_t = []
for rep in range(1, reps + 1):
    sample = water.sample(n=n, replace=True)
    sigma_t.append(sample['temp'].std())

stat = pd.DataFrame({'rep': range(1, reps + 1), 'sigma_t': sigma_t})

hist = (ggplot(stat, aes(x='sigma_t')) +
        geom_histogram(bins=30, fill='steelblue', color='white') +
        theme_classic())
hist

ci = pd.DataFrame({
    'estimate': [stat['sigma_t'].mean()],
    'se': [stat['sigma_t'].std()]
})
ci['upper'] = ci['estimate'] + ci['se'] * norm.ppf(0.975)
ci['lower'] = ci['estimate'] - ci['se'] * norm.ppf(0.975)
ci


# The Python tutorial also writes Cp / Pp / Cpk / Ppk by hand,
# then bootstraps Cp. The packaged helpers live in functions_process_control.py.

limit_lower = 42
limit_upper = 50

stat_s = (water.groupby('time')
          .agg(xbar=('temp', 'mean'), s=('temp', 'std'), n_w=('temp', 'size'))
          .reset_index())

proc = pd.DataFrame({
    'xbbar': [stat_s['xbar'].mean()],
    'sigma_s': [(stat_s['s'] ** 2).mean() ** 0.5],
    'sigma_t': [water['temp'].std()]
})
proc

estimate_cp = cp(proc['sigma_s'][0], upper=limit_upper, lower=limit_lower)
estimate_pp = pp(proc['sigma_t'][0], upper=limit_upper, lower=limit_lower)
estimate_cpk = cpk(mu=proc['xbbar'][0], sigma_s=proc['sigma_s'][0],
                   lower=limit_lower, upper=limit_upper)
estimate_ppk = ppk(mu=proc['xbbar'][0], sigma_t=proc['sigma_t'][0],
                   lower=limit_lower, upper=limit_upper)

print("Cp:", estimate_cp)
print("Pp:", estimate_pp)
print("Cpk:", estimate_cpk)
print("Ppk:", estimate_ppk)
