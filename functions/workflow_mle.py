# What this file is ----------------------------------------------------------
#
# A short demonstration script. It loads functions_mle.py and calls each
# function once on a small crosstab of failures, so you can watch them work
# on real numbers before you use them yourself.
#
# Run it from the top of the project folder, a few lines at a time:
# highlight a chunk with your cursor and run it. Change the numbers and run
# it again -- that is what this file is for.
#

# workflow_mle.py
# Simple demonstration script for the life distribution fitting functions

import sys
import pandas as pd
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

# Import the functions
sys.path.append("functions")
from functions_mle import get_mle, get_expected, get_chisq, get_fit, plife, dlife, qlife, hlife, rlife
from functions_distributions import pexp

# Example data: crops that failed, by 40-day interval
crops = pd.DataFrame({"lower": range(0, 161, 40)})
crops = crops.assign(upper = crops["lower"] + 40, r_obs = [18, 14, 10, 5, 3])

# Fit one distribution (75 crops planted, watched for 200 days)
print(get_mle(data = crops, n_total = 75, tmax = 200, dist = "weibull"))

# Observed and expected failures in each interval
print(get_expected(crops, n_total = 75, dist = "exponential", lambda_ = 0.00595))

# Chi-squared test of that fit
print(get_chisq(data = crops, n_total = 75, f = pexp, rate = 0.00595))

# Fit and test all four distributions at once
print(get_fit(data = crops, n_total = 75, tmax = 200))

# The distribution functions, each called once
print(plife(t = 100, dist = "lognormal", t50 = 150, sigma = 0.8))
print(dlife(t = 100, dist = "lognormal", t50 = 150, sigma = 0.8))
print(qlife(p = 0.5, dist = "lognormal", t50 = 150, sigma = 0.8))
print(hlife(t = 100, dist = "lognormal", t50 = 150, sigma = 0.8))
print(rlife(n = 3, dist = "lognormal", t50 = 150, sigma = 0.8))
