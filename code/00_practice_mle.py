# 00_practice_mle.py
# Tim Fraser
# Extra: practice estimating distribution parameters by maximum likelihood
# Chapter: Useful Life Distributions (Weibull, Gamma, & Lognormal) in Python

# When using MLE

import sys
import numpy as np
import pandas as pd            # data wrangling
from scipy.optimize import minimize   # our optim()

# Our course functions live in functions/ at the repo root.
# (Run this script from the root of the sysen repo.)
sys.path.append("functions")
from functions_distributions import dexp, pexp, dweibull, hist

crops = pd.read_csv("workshops/crops.csv")

# NOTE: `lambda` is a reserved word in Python, so we write `lambda_`.
def d(t, lambda_):
  return lambda_ * np.exp(-t * lambda_)

# NOTE: R's optim(..., control = list(fnscale = -1)) MAXIMIZES.
# scipy's minimize() only minimizes, so we minimize the NEGATIVE
# log-likelihood instead. Same answer. method = "Nelder-Mead" matches
# optim()'s default.

# EXPONENTIAL
def ll(par, t):
  # Testing values
  # t = crops.days; par = [0.001]
  return np.log(dexp(t, rate = par[0])).sum()

m = minimize(lambda par: -ll(par, t = crops.days), x0 = [0.001], method = "Nelder-Mead")
print(m.x, -m.fun)
# Translation:
# Our data crops.days, if exponentially distributed, is most likely to have a
# failure rate lambda of 0.014.


# WEIBULL
def ll(par, t):
  # Testing values
  # NOTE: R's optim() shrugs off impossible (negative) parameters; scipy
  # does not, so we tell it they are infinitely unlikely.
  if par[0] <= 0 or par[1] <= 0: return -np.inf
  return np.log(dweibull(t, shape = par[0], scale = par[1])).sum()

m = minimize(lambda par: -ll(par, t = crops.days), x0 = [1, 10000], method = "Nelder-Mead")
print(m.x, -m.fun)
# Translation:
# Our data crops.days, if weibull distributed, is most likely to have a
# shape parameter m of 1.49 and a characteristic life c of 77.2 days









# Loglikelihood - do you need a vector for it to work? --> YES! Good point.

hist(crops.days)

# https://timothyfraser.com/sigma/chapters/useful-life-distributions-weibull-gamma-lognormal-in-r.html#maximum-likelihood-estimation-mle
n = 75
r = 50
tmax = 200
crops.days

t = crops.days
par = [0.001]
np.prod([1,2,3])

# What's the joint probability that the first 50 did fail?
prob_d = dexp(t, rate = par[0]).prod()
# What's the joint probability that the other 25 didn't fail?
prob_r = (1 - pexp(tmax, rate = par[0]).iloc[0])**(n - r)

# What's the joint probability that BOTH things occurred?
loglik = np.log(prob_d * prob_r)
print(loglik)


def ll(par, t):
  n = 75
  r = 50
  tmax = 200

  # What's the joint probability that the first 50 did fail?
  prob_d = dexp(t, rate = par[0]).prod()
  # What's the joint probability that the other 25 didn't fail?
  prob_r = (1 - pexp(tmax, rate = par[0]).iloc[0])**(n - r)

  # What's the joint probability that BOTH things occurred?
  return np.log(prob_d * prob_r)

m = minimize(lambda par: -ll(par, t = crops.days), x0 = [0.001], method = "Nelder-Mead")
print(m.x, -m.fun)
