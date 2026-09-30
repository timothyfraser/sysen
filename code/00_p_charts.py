# 00_p_charts.py
# Tim Fraser
# Extra: fraction-defective (p) charts - the short version of 00_attribute_charts.py
# Chapter: Statistical Process Control in Python

import numpy as np
import pandas as pd            # data wrangling
from plotnine import *         # visuals
from math import factorial

# Fraction defection (p) chart
# # of defective items
# has a binomial distribution
# each of the n itmes being tests is being classified
# into 2 categories: defective or not defective
# the probability p of a defective item is constant for every item.

# If X represents the # of defective items in n items,
# then the probability of finding x defective in n items is:
t = np.arange(1, 1001)
data = pd.DataFrame({
  't': t,
  't2': np.floor(t / 10) + 1,
  'n': np.random.poisson(lam = 100, size = 1000),
  'x': np.random.poisson(lam = 5, size = 1000)
})
data['p'] = data.x / data.n

# NOTE: R's factorial() works on whole vectors and returns Inf for huge n.
# Python's math.factorial() takes one whole number at a time, so we
# loop over rows with a list comprehension when we need a vector.
def p(x, n, p):
  return factorial(n) / (factorial(x) * factorial(n - x)) * p**x * (1 - p)**(n - x)


# data.agg(prob_p = ('x', lambda v: v.sum() / len(v)))

# prob_p = data.x.sum() / len(data)
# p(x = 1, n = len(data), p = prob_p)

print(p(x = 5, n = 150, p = 0.50))

print(
  data.groupby('t2').agg(n = ('n', 'sum'), x = ('x', 'sum'))
  .assign(p = lambda d: d.x / d.n)
  .reset_index()
)

stat_s = pd.DataFrame({
  't': data.t,
  'prob': [p(x = int(xi), n = int(ni), p = pi) for xi, ni, pi in zip(data.x, data.n, data.p)],
  'mu': data.n * data.p,
  'sigma': np.sqrt(data.n * data.p * (1 - data.p))
})

xsum = data.x.sum()
nsum = data.n.sum()
pbar = xsum / nsum
se = np.sqrt(pbar * (1 - pbar) / nsum)
stat_t = pd.DataFrame({
  'xsum': [xsum], 'nsum': [nsum], 'pbar': [pbar], 'se': [se],
  'lower': [pbar - 3*se], 'upper': [pbar + 3*se]
})
print(stat_t)

(ggplot() +
  geom_line(data = stat_s, mapping = aes(x = 't', y = 'mu')) +
  geom_point(data = stat_s, mapping = aes(x = 't', y = 'mu')))
