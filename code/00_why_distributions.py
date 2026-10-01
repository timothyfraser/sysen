# 00_why_distributions.py


# A quick example summarizing why we use hypothetical distributions

import os, sys
import numpy as np
import pandas as pd   # DataFrame() comes from here
from plotnine import *
sys.path.append(os.path.abspath('functions'))
from functions_distributions import density, tidy_density, approxfun

# If we have the observed data, great! Let's use that
hours = pd.Series([1000, 2000,3000, 2500, 3200, 500, 3000, 5000, 600, 4000, 3000])
# Make observed density function
dobs = approxfun(tidy_density(density(hours)))

# If we DON'T have the observed data, we could use exponential.
def dexp(t, lambda_): return lambda_ * np.exp(-lambda_ * t)

# Let's get a crap ton of probabilities
dat = pd.DataFrame({'t': np.arange(1, 1001)}).assign(
  prob = lambda d: dexp(t = d.t, lambda_ = 0.001),
  prob2 = lambda d: dexp(d.t, lambda_ = 0.002),
  prob3 = lambda d: dexp(d.t, lambda_ = 0.003),
  prob4 = lambda d: dobs(d.t),
  prob5 = lambda d: dexp(d.t, lambda_ = 1 / hours.mean()))

# Key finding: don't use the exponential to model this particular data
# it doesn't look right AT ALL!
(ggplot() +
  geom_line(data = dat, mapping = aes(x = 't', y = 'prob')) +
  geom_line(data = dat, mapping = aes(x = 't', y = 'prob2')) +
  geom_line(data = dat, mapping = aes(x = 't', y = 'prob3'))  +
  geom_line(data = dat, mapping = aes(x = 't', y = 'prob4'), color = "red") +
  geom_line(data = dat, mapping = aes(x = 't', y = 'prob5'), color = "blue"))
