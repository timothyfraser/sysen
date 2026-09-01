# 07_recitation.py
# Tim Fraser
# Recitation 7: Chi-squared goodness-of-fit tests
# Chapter: Statistical Techniques for Exponential Distributions in Python

import pandas as pd
import numpy as np
from plotnine import *
from scipy.stats import chi2, expon, poisson, norm, weibull_min
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_distributions import get_chisq, pexp, ppois, pnorm, pweibull

masks = pd.read_csv("workshops/masks.csv")

# @name get_chisq
# @title Function to Get Chi-Squared!
# If observed vector...
# @param t a vector of times to failure
# @param binwidth size of intervals (eg. 5 hours) (Only if t is provided)
# If cross-tabulated data...
# @param data a DataFrame with the vectors `lower`, `upper`, and `r_obs`
# Common Parameters:
# @param n_total total number of units.
# @param f specific failure function, such as `f = f(t, lambda)`
# @param np total number of parameters in your function (eg. if exponential, 1 (lambda))
# @param **kwargs fill in here any named parameters you need, like lambda_=2.4 or rate=2.3

# TESTING VALUES
t = masks['fabric']
n_total = 50
binwidth = 750

def f(t, lambda_):
    return 1 - np.exp(-t * lambda_)

np_params = 1

# The packaged helper is functions_distributions.get_chisq — same contract as
# the R recitation's get_chisq(). We also rebuild the binned table by hand
# below, because get_chisq() hands back only the TEST result.

lambda_ = 1 / masks['fabric'].mean()

# get_chisq() hands back only the TEST result: chisq, nbin, np, df, p_value.
# To plot observed against expected we need the binned table itself, which is
# the same Step 1 + Step 2 crosstab the chapter walks through by hand.
dat = pd.DataFrame({'t': masks['fabric']})
max_t = int(dat['t'].max())
bins = list(range(0, max_t + 750 + 1, 750))
dat['interval'] = pd.cut(dat['t'], bins=bins, right=True, include_lowest=True)
dat = (dat.groupby('interval', observed=False)
       .size()
       .reset_index(name='r_obs'))
dat['bin'] = range(1, len(dat) + 1)
dat['lower'] = (dat['bin'] - 1) * 750
dat['upper'] = dat['bin'] * 750
dat['p_upper'] = f(dat['upper'], lambda_=lambda_)
dat['p_lower'] = f(dat['lower'], lambda_=lambda_)
dat['p_fail'] = dat['p_upper'] - dat['p_lower']
dat['n_total'] = 50
dat['r_exp'] = dat['n_total'] * dat['p_fail']
dat = dat[['interval', 'r_obs', 'p_fail', 'n_total', 'r_exp']]



(ggplot() +
    geom_col(data=dat, mapping=aes(x='interval', y='r_obs')) +
    geom_point(data=dat, mapping=aes(x='interval', y='r_obs')) +
    geom_col(data=dat, mapping=aes(x='interval', y='r_exp'),
             alpha=0.5, fill='darksalmon') +
    geom_point(data=dat, mapping=aes(x='interval', y='r_exp'),
               alpha=0.5, fill='darksalmon') +
    theme(axis_text_x=element_text(rotation=45, ha='right')))


pd.DataFrame({
    'chisq': [((dat['r_obs'] - dat['r_exp']) ** 2 / dat['r_exp']).sum()]
})


def f(t, lambda_):
    return 1 - np.exp(-t * lambda_)

lambda_ = 1 / masks['fabric'].mean()
get_chisq(t=masks['fabric'], binwidth=750,
          n_total=50, f=f, np=1, lambda_=lambda_)



# chisq
# n_total - total number of observation
# np - total # of parameters
# lambda - our parameter (failure rate)
# f - exponential - CDF - failure function
# binwidth - size of interval
# df -
# p_value


rchisq = chi2.rvs(df=3, size=1000)
hist_chi = (ggplot(pd.DataFrame({'x': rchisq}), aes(x='x')) +
            geom_histogram(bins=30) +
            geom_vline(xintercept=10, color='red'))
hist_chi



dat = pd.DataFrame({
    'lower': [0, 100, 200, 300, 400],
    'upper': [100, 200, 300, 400, 500],
    'r_obs': [50, 43, 20, 10, 5]
})

get_chisq(data=dat, n_total=50, f=f, np=1, lambda_=0.01)
get_chisq(data=dat, n_total=50, f=pexp, np=1, rate=0.01)
get_chisq(data=dat, n_total=50, f=ppois, np=1, mu=masks['fabric'].mean())
get_chisq(data=dat, n_total=50, f=pnorm, np=2,
          mean=masks['fabric'].mean(), sd=masks['fabric'].std())
get_chisq(data=dat, n_total=50, f=pweibull, np=2,
          shape=0.01, scale=masks['fabric'].mean())
