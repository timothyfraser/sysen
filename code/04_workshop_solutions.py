# 04_workshop_solutions.py
# Tim Fraser
# Workshop 4: Failure functions and system reliability (worked solutions)
# Chapter: System Reliability in Python

# In today's workshop, let's practice our many, many ways
# of using failure functions to analyze system reliability!

# See 04_workshop_solutions.py for solutions (but only after class!)

# 0. Load Packages --------------------------------------------------------

import sys
import numpy as np
import pandas as pd            # data wrangling
from plotnine import *         # visuals
import sympy as sp             # derivatives and integrals

# NOTE: R uses the `mosaicCalc` package for derivatives and integrals.
# Python has no `mosaicCalc`; we use `sympy` for symbolic calculus instead.
# sp.integrate() is our antiD() (PDF -> CDF)

# NOTE: `lambda` is a reserved word in Python (it makes tiny anonymous
# functions), so we can't name a variable `lambda`. We write `lambda_` instead.

# Our course functions live in functions/ at the repo root.
# (Run this script from the root of the sysen repo.)
sys.path.append("functions")
from functions_distributions import hist, exp, dexp, pexp


# 1. Making Functions -----------------------------------------------------

# You learned to make Functions in Week 3. Let's practice!
# https://timothyfraser.com/sigma/

# Nintendo is product testing its next Switch console.
# 1000 enthusiastic children received a console in the mail,
# played video games for days on end, and
# parents called in when the console eventually broke.

# On average, 1 console failed every 1200 hours (50 days).

# So, we say the constant failure rate lambda was 1/1200 hours

# Using your notes from Workshop 4, let's write a few functions using lambda!


## Example Function l() (for lambda) --------------------------------------

# The exponential distribution has one parameter
# lambda = the rate of failure
# 1 / mean time to failure


# units = how many pokeballs failed
# hours = how many hours they were used

# mu = hours / units ( mean hours to failure)
# lambda = 1 / mu
# every hour, how many pokeballs do we expect to fail?

def l(units, hours):
    return units / hours
# We have an empirical failure rate of 0.2 pokeballs per hour
l(units=200, hours=1000)

# Try it out
l(units=1, hours=1200)
# We can also, respecting the order of units and hours, write:
l(1, 1200)






# Note: In Python, for exponential distribution,
# we write e^something as exp(something) (np.exp works too)

# Q1. Let's write our probability density function d(t)
# PDF loooks like: d(t) = lambda * e^(-lambda*t)
def d(t, lambda_):
    return lambda_ * exp(-1 * lambda_ * t)

# PDF f(t) is always d(t) in R (and in our Python twin)
d(t=100, lambda_=0.01)
dexp(x=100, rate=0.01)

# Failure F(t)
def f(t, lambda_):
    return 1 - exp(-1 * lambda_ * t)
# cumulative probability of failure by 100 hours?
f(t=100, lambda_=0.01)
pexp(x=100, rate=0.01)
# Or, you could integrate the PDF to produce the equivalent function!!
# In R this was mosaicCalc::antiD(tilde = d(t, lambda) ~ t).
# In Python, we integrate d(t) symbolically with sympy from 0 to t,
# then turn the result back into a numeric function with sp.lambdify().
t_, lam_, u_ = sp.symbols("t lambda u", positive=True)
f2 = sp.lambdify((t_, lam_),
                 sp.integrate(lam_ * sp.exp(-lam_ * u_), (u_, 0, t_)), "numpy")
f2(100, 0.01)


# Reliability R(t)
def f(t, lambda_):
    return 1 - exp(-1 * lambda_ * t)

def r(t, lambda_):
    return 1 - f(t, lambda_)
# EXCEPT

def r(t, lambda_):
    # Tell my funciton r(t, lambda) that f(t, lambda) means this:
    def f(t, lambda_):
        return 1 - exp(-1 * lambda_ * t)
    # calcualte it!
    return 1 - f(t, lambda_)
    # output = 1 - f(t, lambda_);  return output

r(t=100, lambda_=0.01)


lambda_a = .01
lambda_b = .005

t = np.arange(1, 1001)
dat = pd.DataFrame({
    "t": t,
    "prob_a": r(t=t, lambda_=lambda_a),
    "prob_b": r(t=t, lambda_=lambda_b)
})

(ggplot() +
  geom_area(data=dat, mapping=aes(x='t', y='prob_b'),
            alpha=0.5, fill="darksalmon") +
  geom_area(data=dat, mapping=aes(x='t', y='prob_a'),
            alpha=0.75, fill="seagreen") +
  labs(x="Hours to Failure", y="Reliability (%)"))

# Failure Rate Function
def z(t, lambda_):
    return dexp(t, lambda_) / (1 - pexp(t, lambda_))

z(t=0.5, lambda_=0.01)


# Q2. Let's write our failure function f(t)
def f(t, lambda_):
    return 1 - exp(-1 * lambda_ * t)

# Q3. Let's write our reliability function r(t)
def r(t, lambda_):
    return exp(-1 * lambda_ * t)

# Q4. Let's write our failure rate z(t) (hazard rate)
def z(t, lambda_):
    # density function / aka change in failure function
    return (lambda_ * exp(-1 * lambda_ * t) /
            # reliability function
            exp(-1 * lambda_ * t))


# Q5. Test d(t), f(t), r(t), and z(t)
# over a span of 150 days (1 to 3600 hours)
# and visualize each with hist()

hist(pd.Series(d(t=np.arange(1, 3601), lambda_=1/1200)))

hist(pd.Series(f(t=np.arange(1, 3601), lambda_=1/1200)))

hist(pd.Series(r(t=np.arange(1, 3601), lambda_=1/1200)))

hist(pd.Series(z(t=np.arange(1, 3601), lambda_=1/1200)))

# What do you notice?

# Clear environment -------------------------------------------------------
# R clears everything with rm(list = ls()).
# In Python, we just delete the names we made.
del d, f, r, z, l, f2, dat, t, lambda_a, lambda_b


# 2. Higher level Functions -----------------------------------------------

# Sometimes, we make functions that USE functions inside them.
# Just make sure you either
# (1) put function A before function B, or
# (2) put function A INSIDE function B before using it


# We can re-write r(t) USING our function f(t)
def f(t, lambda_):
    return 1 - exp(-1 * lambda_ * t)

def r(t, lambda_):
    return 1 - f(t, lambda_)

# Or we can embed f(t) in r(t)
def r(t, lambda_):
    # Write f(t)
    def f(t, lambda_):
        return 1 - exp(-1 * lambda_ * t)
    # Then calculate and return r(t)
    return 1 - f(t, lambda_)

# We can use embedded functions to create super functions, like h(t) and afr(t)
