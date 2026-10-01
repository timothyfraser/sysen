# 09_workshop_optim.py
# Tim Fraser
# Workshop 9: Parameter Estimation - Multi-Parameter Maximum Likelihood with an optimizer
# Chapter: Useful Life Distributions (Weibull, Gamma, & Lognormal) in Python
#
# It mirrors 09_workshop_optim.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.
#
# Heads up: the normal-distribution demo below deliberately fails on purpose,
# to show what bad starting parameters do. Run this script chunk by chunk
# rather than all at once.


# Using an optimizer for MLE with 1 parameter ##############################################

# Load packages
import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr + readr in R)
from plotnine import *         # visuals (ggplot2 in R)
from scipy import stats        # scipy distributions, for the .fit() check below
import sys
# Load our R-style distribution helpers: dnorm(), pnorm(), dunif(), dweibull(), pweibull()
sys.path.append("functions")
from functions_distributions import dnorm, pnorm, dunif, dweibull, pweibull
from scipy.optimize import minimize  # optimizer (optim() in R)

# Load data.frame of crops by time to failure metric `days`
crops = pd.read_csv("workshops/crops.csv")


# Failure Function CDF F(t)
# (lambda is a reserved word in Python, so the argument is called lam)
def f(t, lam):
  return 1 - np.exp(-1 * t * lam)

# PDF function  f(t)
def d(t, lam):
  return lam * np.exp(-t * lam)

# Calculate Log-Likelihood, by summing the log
def ll(t, lam):
  return np.sum(np.log(d(t = t, lam = lam)))


# We did it manually, but how do we do it automatically?

# We use an OPTIMIZER. R has optim(); Python has scipy.optimize.minimize().
# It searches along the curve/plane we visualized above.
# R's optim() defaults to the Nelder-Mead method, so we use it too.

# Optimize and collect the quantities of interest
# minimize() only MINIMIZES. R flips the sign with control = list(fnscale = -1);
# in Python we minimize the NEGATIVE log-likelihood, which is the same thing.
q = minimize(lambda par: -ll(t = crops['days'], lam = par[0]),
             x0 = [0.01], method = "Nelder-Mead")

# q is an OptimizeResult object - a dictionary with named parts.
# We've learned several types of objects
pd.DataFrame()
[]
# Here's a dictionary example (a list() in R)
mylist = {'df': pd.DataFrame({'x': range(1, 11)}),
          'par': 0.234}
# You can query the par value in the dictionary like this.
print(mylist['par'])

print(q)
# The optimized parameters live in q.x (q$par in R)
# Once we have our optimized parameters, we can pipe it into functions like this!
print(f(t = np.arange(1, 101), lam = q.x[0]))




# Using an optimizer for MLE with 2+ parameters ##############################################


# Load data.frame of crops by time to failure metric `days`
crops = pd.read_csv("workshops/crops.csv")



## uniform ##############################################################

# We could also write MULTI-PARAMETER loglikelihood functions!
def ll(t, par):
  return np.log(dunif(t, min = par[0], max = par[1])).sum(skipna = False)  # NaN stays NaN, as in R

print(crops['days'].min(), crops['days'].max())
# Let's try it!
# Note the starting values: for a UNIFORM likelihood, min and max must bracket
# every observation. Any t outside [min, max] has density 0, log(0) is -inf,
# and the whole loglikelihood collapses to -inf before the optimizer can search.
with np.errstate(divide = 'ignore'):
  print(minimize(lambda par: -ll(t = crops['days'], par = par),
                 x0 = [4, 197], method = "Nelder-Mead"))




## normal ##############################################################

# What about other distributions?

# Let's write a new function
def ll(t, par):
  # Our parameters input is now going to be vector of 2 values
  # par[0] gives the first value, the mean (Python counts from 0)
  # par[1] gives the second value, the standard deviation
  return np.log(dnorm(t, mean = par[0], sd = par[1])).sum(skipna = False)  # NaN stays NaN, as in R

# Let's try it out!
# Heads up: this next line is SUPPOSED to fail. dnorm(days, 0, 1)
# underflows to 0, log(0) is -inf, and the optimizer cannot search.
# R's optim() stops with an error; minimize() just gives back a useless answer
# (success False, or the starting values unchanged). Read it - diagnosing it
# is the next twenty lines of this script.
with np.errstate(divide = 'ignore'):
  bad = minimize(lambda par: -ll(t = crops['days'], par = par),
                 x0 = [0, 1], method = "Nelder-Mead")
print(bad.success, bad.x, bad.fun)
# Why doesn't it work?

# Well, we're giving it super weird starting parameters. (0,1)
# What densities would they produce?
print(dnorm(crops['days'], mean = 0, sd = 1))
# What loglikelihood would they produce?
with np.errstate(divide = 'ignore'):
  print(np.sum(np.log(dnorm(crops['days'], mean = 0, sd = 1))))

# Let's look at our real values...
print(crops['days'].values)


# What if we picked more representative starting parameters?
q2 = minimize(lambda par: -ll(t = crops['days'], par = par),
              x0 = [90, 15], method = "Nelder-Mead")
print(q2.x)
# Yay! It works!


print(pnorm(np.arange(1, 11), mean = q2.x[0], sd = q2.x[1]))



## weibull ##############################################################


# Let's try a weibull!
print(pweibull(1, shape = 2, scale = 1))


def llweibull(t, par):
  return np.log(dweibull(t, shape = par[0], scale = par[1])).sum(skipna = False)  # NaN stays NaN, as in R

q3 = minimize(lambda par: -llweibull(t = crops['days'], par = par),
              x0 = [1, 1000], method = "Nelder-Mead")

print(q3.x)



# You might want to hang on to this
# Chunk of helper code
# minimize(lambda par: -ll(t, par), x0 = [...], method = "Nelder-Mead")
# def d(t, lam): return lam * np.exp(-1 * t * lam)

# All done!



## fitdistr ###########################################################

# Feeling accomplished, but like this should be easier?
# That's what R's MASS::fitdistr() does. In Python, each scipy distribution
# has a .fit() method. floc = 0 pins the location at 0, like R's versions.

print(stats.norm.fit(crops['days']))                          # (mean, sd)
print(1 / stats.expon.fit(crops['days'], floc = 0)[1])        # rate = 1 / scale
print(stats.weibull_min.fit(crops['days'], floc = 0))         # (shape, loc, scale)


# Interested? Learn more here!
# https://timothyfraser.com/sigma/chapters/appendix-using-fitdistr-to-fitting-distribution-parameters.html
