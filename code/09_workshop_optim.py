# 09_workshop_optim.py
# Tim Fraser
# Workshop 9: Parameter Estimation - Multi-Parameter Maximum Likelihood with minimize()
# Chapter: Useful Life Distributions (Weibull, Gamma, & Lognormal) in Python
#
# Heads up: the normal-distribution demo below deliberately fails on purpose,
# to show what bad starting parameters do. Run this script chunk by chunk
# rather than all at once.
#
# R uses stats::optim(..., control = list(fnscale = -1)) to MAXIMIZE log-likelihood.
# The Python tutorial uses scipy.optimize.minimize on the *negative* log-likelihood
# (minimizing -ll is the same as maximizing ll). Same idea, different API.


# Using minimize() for MLE with 1 parameter ##############################################

# Load packages
import pandas as pd
import numpy as np
from scipy.stats import norm, expon, weibull_min, uniform
from scipy.optimize import minimize
from plotnine import *

# Load data.frame of crops by time to failure metric `days`
crops = pd.read_csv("workshops/crops.csv")


# Failure Function CDF F(t)
def f(t, lambda_):
    return 1 - np.exp(-1 * t * lambda_)

# PDF function  f(t)
def d(t, lambda_):
    return lambda_ * np.exp(-t * lambda_)

# Calculate Log-Likelihood, by summing the log
def ll(t, lambda_):
    return np.log(d(t=t, lambda_=lambda_)).sum()


# We did it manually, but how do we do it automatically?

# We use an OPTIMIZER, with scipy.optimize.minimize().
# It uses gradient descent to ascend/descend the curve/plane we visualized above.

# Minimize the negative log-likelihood (equivalent to maximizing log-likelihood)
def neg_ll(lambda_val, data):
    return -ll(t=data, lambda_=lambda_val[0])

q = minimize(fun=neg_ll, x0=[0.01], args=(crops['days'],), method='Nelder-Mead')

# q is an OptimizeResult object. We've learned several types of objects
# pd.DataFrame()
# np.array()
# Here's a dict example
mylist = {'df': pd.DataFrame({'x': range(1, 11)}),
          'par': 0.234}
# You can query the par vector in the dict like this.
mylist['par']

q
# Once we have our optimized parameters, we can pipe it into functions like this!
f(t=np.arange(1, 101), lambda_=q.x[0])



# Using minimize() for MLE with 2+ parameters ##############################################


# Load data.frame of crops by time to failure metric `days`
crops = pd.read_csv("workshops/crops.csv")



## uniform ##############################################################

# We could also write MULTI-PARAMETER loglikelihood functions!
def ll(t, par):
    return np.log(uniform.pdf(t, loc=par[0], scale=par[1] - par[0])).sum()

def neg_ll(par, data):
    return -ll(data, par)

crops['days'].min(), crops['days'].max()
# Let's try it!
# Note the starting values: for a UNIFORM likelihood, min and max must bracket
# every observation. Any t outside [min, max] has density 0, log(0) is -Inf,
# and the whole loglikelihood collapses to -Inf before minimize() can search.
minimize(fun=neg_ll, x0=[4, 197], args=(crops['days'],), method='Nelder-Mead')



## normal ##############################################################

# What about other distributions?

# Let's write a new function
def ll(t, par):
    # Our parameters input is now going to be a vector of 2 values
    # par[0] gives the first value, the mean
    # par[1] gives the second value, the standard deviation
    return np.log(norm.pdf(t, loc=par[0], scale=par[1])).sum()

def neg_ll(par, data):
    return -ll(data, par)

# Let's try it out!
# Heads up: this next line is SUPPOSED to fail. norm.pdf(crops['days'], 0, 1)
# underflows to 0, log(0) is -Inf, and minimize() refuses to start. Run it and
# read the error - diagnosing it is the next twenty lines of this script.
# minimize(fun=neg_ll, x0=[0, 1], args=(crops['days'],), method='Nelder-Mead')
# Why doesn't it work?

# Well, we're giving it super weird starting parameters. (0,1)
# What densities would they produce?
norm.pdf(crops['days'], loc=0, scale=1)
# What loglikelihood would they produce?
np.log(norm.pdf(crops['days'], loc=0, scale=1)).sum()

# Let's look at our real values...
crops['days']


# What if we picked more representative starting parameters?
q2 = minimize(fun=neg_ll, x0=[90, 15], args=(crops['days'],), method='Nelder-Mead')
q2.x
# Yay! It works!


norm.cdf(np.arange(1, 11), loc=q2.x[0], scale=q2.x[1])



## weibull ##############################################################


# Let's try a weibull!
# scipy's weibull_min uses shape `c` and scale; R's dweibull uses shape and scale.
weibull_min.cdf(1, c=2, scale=1)


def llweibull(t, par):
    return np.log(weibull_min.pdf(t, c=par[0], scale=par[1])).sum()

def neg_llweibull(par, data):
    return -llweibull(data, par)

q3 = minimize(fun=neg_llweibull, x0=[1, 1000], args=(crops['days'],), method='Nelder-Mead')

q3.x



# You might want to hang on to this
# Chunk of helper code
# def d(t, lambda_): return lambda_ * np.exp(-1 * t * lambda_)

# All done!



## fit() ###########################################################

# Feeling accomplished, but like this should be easier?
# That's what scipy.stats.*.fit() does. (R's MASS::fitdistr)

norm.fit(crops['days'])
expon.fit(crops['days'], floc=0)
weibull_min.fit(crops['days'], floc=0)


# Interested? Learn more here!
# https://timothyfraser.com/sigma/chapters/appendix-using-fitdistr-to-fitting-distribution-parameters.html
