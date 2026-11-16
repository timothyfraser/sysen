# What this file is ----------------------------------------------------------
#
# A short demonstration script. It loads functions_mle.R and calls each
# function once on a small crosstab of failures, so you can watch them work
# on real numbers before you use them yourself.
#
# Run it from the top of the project folder, a few lines at a time:
# highlight a chunk with your cursor and press CTRL and ENTER
# simultaneously. Change the numbers and run it again -- that is what
# this file is for.
#

# workflow_mle.R
# Simple demonstration script for the life distribution fitting functions

# Source the functions
source("functions/functions_mle.R")

# Example data: crops that failed, by 40-day interval
crops = tibble(lower = seq(0, 160, 40), upper = lower + 40,
               r_obs = c(18, 14, 10, 5, 3))

# Fit one distribution (75 crops planted, watched for 200 days)
get_mle(data = crops, n_total = 75, tmax = 200, dist = "weibull")

# Observed and expected failures in each interval
get_expected(crops, n_total = 75, dist = "exponential", lambda = 0.00595)

# Chi-squared test of that fit
get_chisq(data = crops, n_total = 75, f = pexp, rate = 0.00595)

# Fit and test all four distributions at once
get_fit(data = crops, n_total = 75, tmax = 200)

# The distribution functions, each called once
plife(t = 100, dist = "lognormal", t50 = 150, sigma = 0.8)
dlife(t = 100, dist = "lognormal", t50 = 150, sigma = 0.8)
qlife(p = 0.5, dist = "lognormal", t50 = 150, sigma = 0.8)
hlife(t = 100, dist = "lognormal", t50 = 150, sigma = 0.8)
rlife(n = 3, dist = "lognormal", t50 = 150, sigma = 0.8)
