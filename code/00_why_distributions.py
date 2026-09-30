# 00_why_distributions.py


# A quick example summarizing why we use hypothetical distributions

import sys
import numpy as np
import pandas as pd            # data wrangling
from plotnine import *         # visuals

# Our course functions live in functions/ at the repo root.
# (Run this script from the root of the sysen repo.)
sys.path.append("functions")
from functions_distributions import density, tidy_density, approxfun

# If we have the observed data, great! Let's use that
hours = pd.Series([1000, 2000,3000, 2500, 3200, 500, 3000, 5000, 600, 4000, 3000])
# Make observed density function
# NOTE: R's density() pads the curve 3 bandwidths past the data;
# tidy_density() only spans min to max, so outside that range
# approxfun() extrapolates. scipy's KDE also uses a slightly
# different default bandwidth (Scott's rule) than R's (nrd0).
dobs = approxfun(tidy_density(density(hours)))

# If we DON'T have the observed data, we could use exponential.
# NOTE: `lambda` is a reserved word in Python, so we write `lambda_`.
def dexp(t, lambda_):
  return lambda_ * np.exp(-lambda_ * t)

# Let's get a crap ton of probabilities
t = np.arange(1, 1001)
dat = pd.DataFrame({
  't': t,
  'prob': dexp(t = t, lambda_ = 0.001),
  'prob2': dexp(t, lambda_ = 0.002),
  'prob3': dexp(t, lambda_ = 0.003),
  'prob4': dobs(t),
  'prob5': dexp(t, lambda_ = 1 / hours.mean())})
print(dat.head())

# Key finding: don't use the exponential to model this particular data
# it doesn't look right AT ALL!
(ggplot() +
  geom_line(data = dat, mapping = aes(x = 't', y = 'prob')) +
  geom_line(data = dat, mapping = aes(x = 't', y = 'prob2')) +
  geom_line(data = dat, mapping = aes(x = 't', y = 'prob3'))  +
  geom_line(data = dat, mapping = aes(x = 't', y = 'prob4'), color = "red") +
  geom_line(data = dat, mapping = aes(x = 't', y = 'prob5'), color = "blue"))
