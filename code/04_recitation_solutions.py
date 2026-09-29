# 04_recitation_solutions.py
# Tim Fraser
# Recitation 4: System reliability (worked solutions)
# Chapter: System Reliability in Python

# Load Packages -----------------------------------------------------------

import sys
import numpy as np
import pandas as pd            # data wrangling
from plotnine import *         # visuals
import sympy as sp             # derivatives and integrals

# NOTE: R uses the `mosaicCalc` package for derivatives and integrals.
# Python has no `mosaicCalc`; we use `sympy` for symbolic calculus instead.
# sp.diff() is our D()              (CDF -> PDF)
# sp.integrate() is our antiD() (PDF -> CDF)

# NOTE: `lambda` is a reserved word in Python (it makes tiny anonymous
# functions), so we can't name a variable `lambda`. We write `lambda_` instead.

# Our course functions live in functions/ at the repo root.
# (Run this script from the root of the sysen repo.)
sys.path.append("functions")
from functions_distributions import hist, exp, dexp, pexp


# 1. Reliability Calculations by TYPE of System ---------------------------

# We also learned how to calculate reliability for a series vs. parallel system
# Quick Recap

# Series Systems:

# To get reliability of a Series of parts,
# multiply probability of reliability among each part, written R_1(t), R_2(t), etc. below
# R_series(t) = R_1(t) * R_2(t) * R_3(t) * .... * R_n(t)

# Parallel/Redundant System:

# To get reliability of a Parallel system of parts

# R_parallel(t) = 1 - (F_1(t) * F_2(t) * ... F_n(t) )
# or
# R_parallel(t) = 1 - (1 - R_1(t)) * (1 - R_2(t)) * ... (1 - R_n(t) )


# Q1. Nintendo made a new model of the Switch!
# (Hypothetically) each part (cord, screen, joystick A, joystick B)  has a specific failure rate, listed below.
# Calculate the overall probability that Nintendo's entire console DOESN'T fail after 1 hour

# 1 cord (1 / 5000 days)
# 1 screen (1 / 3000 days)
# 2 joysticks (1 / 2500 days)

cord = 1 / 5000
screen = 1 / 3000
joystick = 1 / 1000

def r(t, lambda_):
    return exp(-1 * lambda_ * t)

(r(t=1, lambda_=cord) *
  r(t=1, lambda_=joystick)**2 *
  r(t=1, lambda_=screen))




# Q2. Design a function to test console reliability for any time t.
# Test reliability after 1 hour, 24 hours, and 168 hours (7 days)
def nintendo(t):
    return (r(t, lambda_=cord) *
            r(t, lambda_=joystick)**2 *
            r(t, lambda_=screen))

nintendo(np.array([1, 24, 168]))

# Q3. Use your function to visualize the reliability curve
# for this overall system in ggplot, as it ranges from 1 to 2000 hours!

# Let's make a DataFrame 's' for system
s = (pd.DataFrame({"t": np.arange(1, 2001)})
     .assign(p_n=lambda df: nintendo(df.t),
             p_j=lambda df: r(df.t, lambda_=joystick),
             p_c=lambda df: r(df.t, lambda_=cord),
             p_s=lambda df: r(df.t, lambda_=screen)))

(ggplot() +
  geom_area(data=s, mapping=aes(x='t', y='p_c', fill='"Cord"'), alpha=0.75) +
  geom_area(data=s, mapping=aes(x='t', y='p_s', fill='"Screen"'), alpha=0.75) +
  geom_area(data=s, mapping=aes(x='t', y='p_j', fill='"Joystick"'), alpha=0.75) +
  geom_area(data=s, mapping=aes(x='t', y='p_n', fill='"Overall"'), alpha=0.75))


## What if the joysticks were a parallel system instead of a series? -------
# Maybe you only need one to function.

def nintendo2(t):
    return (r(t, lambda_=cord) *
            (1 - (1 - r(t, lambda_=joystick)) * (1 - r(t, lambda_=joystick))) *
            r(t, lambda_=screen))

# Let's compare.
nintendo(t=100)
nintendo2(t=100)


# 2. Key Functions Recap --------------------------------------------------

# Recently, we learned key failure/reliability functions in Python, using the exponential distribution!

# Let's write a few functions for this!
# We'll use dexp() and pexp() at the base of our functions, to reduce the likelihood of error :)

# Write function f(t), renamed d(t), to give our PDF for any time t
def d(t, lambda_):
    return dexp(t, rate=lambda_)

# Write failure function F(t) to give our CDF for any time t
def f(t, lambda_):
    return pexp(t, rate=lambda_)

# Write reliability function R(t) to give 1 - CDF for any time t
def r(t, lambda_):
    return 1 - pexp(t, rate=lambda_)

# Write failure rate function z(t) (aka hazard rate h(t)) to give PDF / (1 - CDF) for any time t
def z(t, lambda_):
    return dexp(t, rate=lambda_) / (1 - pexp(t, rate=lambda_))

# Write cumulative hazard rate function H(t), renamed h(t) for easy of coding
def h(t, lambda_):
    return -np.log(1 - pexp(t, rate=lambda_))

# Write average failure rate AFR(t1, t2), to show average rate of failure between times 1 and 2
# we'll reuse h(t) from above
def afr(t1, t2, lambda_):
    return (h(t2, lambda_) - h(t1, lambda_)) / (t2 - t1)


# 3. Calculus in Python ---------------------------------------------------

# In R, the mosaicCalc package gives us D() to derive and antiD() to integrate.
# In Python, sympy gives us sp.diff() to derive and sp.integrate() to integrate,
# and sp.lambdify() turns the answer back into a function we can feed numbers.

# It's written like...

# First, tell sympy which letters are symbols
x, z = sp.symbols("x z")

# If I have function f(x) = x^2 + 2*x
# We can get the derivative...
derivative = sp.lambdify((x, z), sp.diff(x**2 + 2*x + z**5, x), "numpy")
# And use it as a function like this
derivative(np.arange(1, 6), 1)
# You could write it like this too:
def f(x, z):
    return x**2 + 2*x + z**5
# Then take the derivative of the function
derivative2 = sp.lambdify((x, z), sp.diff(f(x, z), x), "numpy")
# And get valules like this!
derivative2(np.arange(1, 6), 1)

# We can get the integral...
integral = sp.lambdify((x, z), sp.integrate(x**2 + 2*x + z**5, x), "numpy")
# And use it as a function like this.
integral(np.arange(1, 6), 1)
# Or if we wrote it as a function again...
def f(x, z):
    return x**2 + 2*x + z**5
# You could take the integral of the function!
integral2 = sp.lambdify((x, z), sp.integrate(f(x, z), x), "numpy")
# And get values!
integral2(np.arange(1, 6), 1)


# Let's practice that a bit.

# sympy needs symbols for t and lambda, and our functions need to use
# sympy's exp() (sp.exp) so sympy can do calculus on them.
t, lam = sp.symbols("t lambda", positive=True)
u = sp.Symbol("u", positive=True)   # a dummy variable to integrate over

# Suppose we have our PDF function as d(t, lambda)
def d(t, lambda_):
    return lambda_ * sp.exp(-1 * lambda_ * t)
# and our CDF function as f(t, lambda)
def f(t, lambda_):
    return 1 - sp.exp(-1 * lambda_ * t)
# so our reliability function is...
def r(t, lambda_):
    return sp.exp(-1 * lambda_ * t)

# To feed numbers into these, we lambdify them too.
d_num = sp.lambdify((t, lam), d(t, lam), "numpy")
f_num = sp.lambdify((t, lam), f(t, lam), "numpy")
r_num = sp.lambdify((t, lam), r(t, lam), "numpy")

hours = np.arange(1, 3601)

# Q1. Find the integral of d(). What does it equal?
# (We integrate from 0 up to t, so the answer starts at 0 like a CDF should.)

fc = sp.integrate(lam * sp.exp(-1 * lam * u), (u, 0, t))
fc = sp.integrate(d(u, lam), (u, 0, t))
fc
fc = sp.lambdify((t, lam), fc, "numpy")
hist(pd.Series(fc(hours, 1/1200)))
# Compare with original
hist(pd.Series(f_num(hours, 1/1200)))


# Q2. Find the derivative of f()
dc = sp.diff(1 - sp.exp(-1 * lam * t), t)
dc = sp.diff(f(t, lam), t)
dc
dc = sp.lambdify((t, lam), dc, "numpy")
hist(pd.Series(dc(hours, 1/1200)))
# Compare with original
hist(pd.Series(d_num(hours, 1/1200)))


# Q3. Find the negative derivative of r()
dc2 = sp.lambdify((t, lam), sp.diff(-1 * r(t, lam), t), "numpy")
hist(pd.Series(dc2(hours, 1/1200)))
hist(pd.Series(d_num(hours, 1/1200)))



# Q4. Find 1 - the integral of d()
fc = sp.lambdify((t, lam), sp.integrate(d(u, lam), (u, 0, t)), "numpy")
hist(pd.Series(1 - fc(hours, 1/1200)))
hist(pd.Series(r_num(hours, 1/1200)))
