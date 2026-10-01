# 00_p_charts.py
# Tim Fraser
# Extra: fraction-defective (p) charts - the short version of 00_attribute_charts.py
# Chapter: Statistical Process Control in Python

import os, sys
import numpy as np
import pandas as pd
from math import factorial
sys.path.append(os.path.abspath('functions'))
from functions_distributions import rpois

# Fraction defection (p) chart
# # of defective items
# has a binomial distribution
# each of the n itmes being tests is being classified
# into 2 categories: defective or not defective
# the probability p of a defective item is constant for every item.

# If X represents the # of defective items in n items,
# then the probability of finding x defective in n items is:
data = (pd.DataFrame({'t': np.arange(1, 1001)})
  .assign(
    t2 = lambda d: np.floor(d.t / 10) + 1,
    n = rpois(n = 1000, mu = 100),
    x = rpois(n = 1000, mu = 5),
    p = lambda d: d.x / d.n
  ))


def p(x,n,p): return factorial(n) / (factorial(x)*factorial(n - x)) * p**(x)*(1 - p)**(n-x)


# data.agg(prob_p = ('x', lambda v: v.sum() / len(v)))

# prob_p = data.x.sum() / len(data)
# p(x = 1, n = len(data), p = prob_p)

p(x = 5, n = 150, p = 0.50)

(data.groupby('t2')
  .agg(n = ('n', 'sum'), x = ('x', 'sum'))
  .assign(p = lambda d: d.x / d.n))
stat_s = (data
  .assign(
    prob = lambda d: [p(x = int(xi), n = int(ni), p = pi) for xi, ni, pi in zip(d.x, d.n, d.p)],
    mu = lambda d: d.n * d.p,
    sigma = lambda d: np.sqrt(d.n*d.p*(1-d.p))
  ))

stat_t = (pd.DataFrame({'xsum': [data.x.sum()], 'nsum': [data.n.sum()]})
  .assign(
    pbar = lambda d: d.xsum / d.nsum,
    se = lambda d: np.sqrt(d.pbar * (1 - d.pbar) / d.nsum),
    lower = lambda d: d.pbar - 3*d.se,
    upper = lambda d: d.pbar + 3*d.se
  ))

from plotnine import *
(ggplot() +
  geom_line(data = stat_s, mapping = aes(x = 't', y = 'mu')) +
  geom_point(data = stat_s, mapping = aes(x = 't', y = 'mu')))
