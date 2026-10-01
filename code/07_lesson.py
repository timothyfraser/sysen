# 07_lesson.py
# Tim Fraser
# Lesson 7: The exponential distribution
# Chapter: Useful Life Distributions (Exponential) in Python
#
# More info here: https://timothyfraser.com/sigma/

# This is the Python twin of 07_lesson.R, section by section.
# Run it from the top of the sysen folder, so the file paths below work.

import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr + readr in R)
from plotnine import *         # visuals (ggplot2 in R)
import sympy as sp             # derivatives and integrals

# NOTE: R uses the `mosaicCalc` package for antiD() (integrals).
# Python has no `mosaicCalc`; we use `sympy` for symbolic calculus instead.

# NOTE: `lambda` is a reserved word in Python (it makes tiny anonymous
# functions), so we can't name a variable `lambda`. We write `lambda_` instead.

masks = pd.read_csv("workshops/masks.csv")

masks.info()

# Let's write some functions!
# failure function (CDF)
def f(t, lambda_):
    return 1 - np.exp(-1 * t * lambda_)
# reliability function
def r(t, lambda_):
    return np.exp(-1 * t * lambda_)



stat = (pd.DataFrame({
    # The literal mean time to fail
    # in our observed distribution is this
    "mttf": [masks["left_earloop"].mean()]})
  .assign(
    # And lambda is this...
    lambda_ = lambda x: 1 / x["mttf"],
    # The observed median is this....
    median = masks["left_earloop"].median(),
    # But if we assume it's an exponential distribution
    # and calculate the median from lambda,
    # we get t50, which is very close.
    t50 = lambda x: np.log(2) / x["lambda_"]))

# hist() in R draws a quick histogram; here we use plotnine
ggplot(masks, aes(x="left_earloop")) + geom_histogram(bins=30)

print(stat["lambda_"][0])

print(r(t=10 + 5, lambda_=stat["lambda_"][0]) / r(t=10, lambda_=stat["lambda_"][0]))





def cr(t, x, lambda_):
    # We can actually nest functions inside each other,
    # to make them easier to write
    def r(t, lambda_):
        return np.exp(-1 * t * lambda_)

    # Calculate R(x + t) / R(t)
    output = r(t=t + x, lambda_=lambda_) / r(t=t, lambda_=lambda_)

    # and return the result!
    return output

print(cr(t=10, x=5, lambda_=stat["lambda_"][0]))




# Calculate Mean Residual Life
def mu(t, lambda_):

    # Get the Reliability Function for exponential distribution
    def r(t, lambda_):
        return np.exp(-1 * t * lambda_)

    # Get the MTTF (integral of reliability function)
    # In Python, we integrate R(u) symbolically with sympy from 0 to t,
    # then turn the result back into a numeric function with sp.lambdify().
    t_, lam_, u_ = sp.symbols("t lambda u", positive=True)
    mttf = sp.lambdify((t_, lam_),
                       sp.integrate(sp.exp(-1 * u_ * lam_), (u_, 0, t_)), "numpy")

    # Now calculate mu(), the Mean Residual Life function at time t
    output = mttf(np.inf, lambda_) / r(t=t, lambda_=lambda_)

    return output

# Get the MTTF (integral of reliability function)
def r(t, lambda_):
    return np.exp(-1 * t * lambda_)
print(r(t=100, lambda_=0.01))

# (antiD() in R: sympy integrates R(t) from 0 to t; lambdify() makes it a function)
t_, lambda_ = sp.symbols("t lambda", positive=True)
mttf = sp.lambdify((t_, lambda_), sp.integrate(sp.exp(-1 * t_ * lambda_), (t_, 0, t_)), "numpy")

# mttf(1000, 0.001)
print(mttf(np.inf, 0.001))

print(1 / 0.001)
