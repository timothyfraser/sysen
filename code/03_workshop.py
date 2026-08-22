# 03_workshop.py
# Tim Fraser
# Workshop 3: PDFs and CDFs in Python
# Chapter: Probability in Python

# Below, please find the following content for our recitation class from Friday.

# Getting Started ---------------------------------------------------------

import sys
import numpy as np
import pandas as pd            # data wrangling
from plotnine import *         # visuals
import sympy as sp             # derivatives and integrals

# NOTE: R uses the `mosaicCalc` package for derivatives and integrals.
# Python has no `mosaicCalc`; we use `sympy` for symbolic calculus instead.

# Our course functions live in functions/ at the repo root.
# (Run this script from the root of the sigma repo.)
sys.path.append("functions")
from functions_distributions import density, tidy_density, approxfun


# Exercise 1 --------------------------------------------------------------
# Class teaches Dr. Fraser to analyze PDFs and CDFs

## How to make a function! ------------------------------------------------




## When the PDF is provided -----------------------------------------------

# the function that produces the line,
# or the probability for every x value

# probability density function --> probability distribution


def d(x):
    return (x + 2 * x) / 1000


d(x=1)
# There is a 0.3% chance that we would get a value of 1
# from this particular distribution / density function.

# EXACTLY 1. --> probability densities
# More than or Less than 1 --> cumulative probabilities


# toaster - time (hours) to failure
# How would I use this PDF to find probability density of failure at 50 hours?




# Make our own DataFrame with pandas
# How about for 0 to 1000 hours?




# How might I plot that?



# Oooh... can I save that plot?




## Simulated Distributions ------------------------------------------------

# Archetypal Distributions, normal, poisson, exponential

# What are our 4 types of probability functions?
# use poisson as an example



# mean of 50 hours to failure
mu = 50


# How would I simulate 10 products with a mean time to failure of 50 hours?
# Assume poisson


# What's the histogram look like?


# How could I get the cumulative probability,
# from 1 to 100? Use a DataFrame.




# Empirical Hours to Failure for Some Toasters
obs = [10, 50, 20, 30, 40, 50, 30, 20, 90]

# Make an empirical probability density function


# empirical cumulative probability function for d()
# In R this was mosaicCalc::antiD(tilde = d(x) ~ x).
# In Python, we integrate d(x) symbolically with sympy,
# then turn the result back into a numeric function with sp.lambdify().
x = sp.Symbol("x")
pobs = sp.lambdify(x, sp.integrate(d(x), x), "numpy")
pobs(np.array([1, 2, 3]))

# Can't really easily do that for our approxfun()
# dobs




# probabilities densities




## Exercise: The Cost of a Component --------------------------------------

# The cost of a component varies depending on market conditions.
# Over the last year, analysts report it cost on average $50,
# with a standard deviation of $5.
# Assume normal distribution - so dnorm, etc.

# Pick 2!

# Q1. What is the probability the component will cost exactly $60?



# Q2. What is the probability the component costs less than $60?




# Q3. What is the probability that the component costs more than $60?



# Q4. What price is greater than 75% of all sales?



# Q5. What is the probability it costs between $45 and $55?
