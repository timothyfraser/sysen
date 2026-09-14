# 03_workshop_solutions.py
# Tim Fraser
# Workshop 3: PDFs and CDFs in Python (worked solutions)
# Chapter: Probability Functions in Python

# Below, please find the following content for our recitation class from Friday.

# Getting Started ---------------------------------------------------------

import os, sys
import numpy as np
import pandas as pd            # data wrangling
from plotnine import *         # visuals

# Our course functions live in functions/ at the repo root.
# (Run this script from the root of the repo.)
sys.path.append(os.path.abspath('functions'))
from functions_distributions import (
    hist, density, tidy_density, approxfun,
    dnorm, pnorm, qnorm, rpois, ppois
)

# NOTE: R uses the `mosaicCalc` package for derivatives and integrals.
# Python has no `mosaicCalc`, so where R uses antiD() and D(), we use scipy:
# quad() from scipy.integrate is our antiD()  (PDF -> CDF)
# a small difference quotient is our D()      (CDF -> PDF)
from scipy.integrate import quad


# Exercise 1 --------------------------------------------------------------
# Class teaches Dr. Fraser to analyze PDFs and CDFs

## When the PDF is provided -----------------------------------------------

# the function that produces the line,
# or the probability for every x value

# probability density function --> probability distribution


def d(x):
    return (x + 2 * x) / 1000


# What's the chance that we get a toaster that fails **at** 1 hour
d(x=1)

# There is a 0.3% chance that we would get a value of 1
# from this particular distribution / density function.

# EXACTLY 1. --> probability densities
# More than or Less than 1 --> cumulative probabilities


# toaster - time (hours) to failure
# How would I use this PDF to find probability density of failure at 50 hours?
d(x=50)


# Make our own DataFrame with pandas
# How about for 0 to 1000 hours?

dat = pd.DataFrame({'hours': range(0, 51)}).assign(
    prob=lambda df: d(x=df['hours']))

dat

## Plotting it ------------------------------------------------------------

# How might I plot that?

# R has colors(); in Python, plotnine uses matplotlib's named colors.
# eg. "tomato", "darksalmon", "slategray", "thistle"

(ggplot() +
    geom_point(data=dat, mapping=aes(x='hours', y='prob'),
               color="tomato"))

(ggplot() +
    geom_line(data=dat, mapping=aes(x='hours', y='prob', group='"my line"'),
              color="tomato", size=2))

(ggplot() +
    geom_area(data=dat, mapping=aes(x='hours', y='prob', group='"my line"'),
              color="tomato", fill="darksalmon", alpha=0.5, size=2))


# Oooh... can I save that plot?

gg = (ggplot() +
      geom_area(data=dat, mapping=aes(x='hours', y='prob', group='"my line"'),
                color="tomato", fill="darksalmon", alpha=0.5, size=2))

# The R version wrote a .png into the repo with ggsave().
# We'll just build the plot object and look at it instead.
gg
# gg.show()


dat
d(x=2)


# Exercise 2 --------------------------------------------------------------

## Simulated Distributions ------------------------------------------------

# Archetypal Distributions, normal, poisson, exponential

# What are our 4 types of probability functions?
# use poisson as an example


# mean of 50 hours to failure
mu = 50


# How would I simulate 10 products with a mean time to failure of 50 hours?
# Assume poisson

# dpois() # PDF - densities
# ppois() # CDF - cumulative probabilities
# qpois() # quantiles
# rpois() # random samples

toasters = rpois(n=10, mu=50)
rpois(n=10, mu=mu)


# What's the histogram look like?

hist(toasters)


# How could I get the cumulative probability,
# from 1 to 100? Use a DataFrame.

dat = pd.DataFrame({'hours': range(1, 101)}).assign(
    prob=lambda df: ppois(df['hours'], mu=mu))


(ggplot() + geom_point(data=dat, mapping=aes(x='hours', y='prob')))


# Exercise 3 --------------------------------------------------------------

# Empirical Hours to Failure for Some Toasters
obs = [10, 50, 20, 30, 40, 50, 30, 20, 90]


# Make an empirical probability density function
# known density function


def d(x):
    return (x + 2 * x) / 1000


# observed density function
# In R: obs %>% density() %>% approxfun()
# In Python, density() gives us a kernel density model,
# tidy_density() turns it into a DataFrame of x and y,
# and approxfun() connects-the-dots into a function.
dobs = approxfun(tidy_density(density(obs)))

d(50)
dobs(50)

# Integrating the PDF to get the CDF
# In R this was mosaicCalc::antiD(tilde = d(x) ~ x).
# quad() integrates d() from 0 up to each x, giving cumulative probability.
def p(x):
    # quad() returns (value, error), so keep just the value
    return np.array([quad(d, 0, xi)[0] for xi in np.atleast_1d(x)])


p(50)

# You can integrate dobs() too, but it's a connect-the-dots model,
# so outside the range of the data it just returns NaN.
# p_obs = quad(dobs, 0, 50)
obs

# empirical cumulative probability function for d()
pobs = p
pobs([1, 2, 3])

# And the other direction: R's D() takes the derivative (CDF -> PDF).
# In Python, a small difference quotient does the same job.
def d2(x, h=1e-5):
    return (p(x + h) - p(x - h)) / (2 * h)


# It gets us back our original density function d()
d2(50)
d(50)

# Can't really easily do that for our approxfun()
dobs

# R would clear everything here with rm(list = ls()).
# In Python, we just delete the objects we made.
del dat, gg, obs, dobs, p, pobs, d2, toasters, mu


# Exercise 4 --------------------------------------------------------------

# The cost of a component varies depending on market conditions.
# Over the last year, analysts report it cost on average $50,
# with a standard deviation of $5.
# Assume normal distribution - so dnorm, etc.

# Pick 2!

## Q1 ---------------------------------------------------------------------
# What is the probability [density] the component will cost exactly $60?

# PDF
dnorm(x=60, mean=50, sd=5)
dnorm(x=60.5, mean=50, sd=5)

dnorm(np.arange(0, 51), mean=50, sd=5)


## Q2 ---------------------------------------------------------------------
# What is the probability the component costs less than $60?

# CDF
pnorm(60, mean=50, sd=5)


## Q3 ---------------------------------------------------------------------
# What is the probability that the component costs more than $60?

1 - pnorm(60, mean=50, sd=5)


## Q4 ---------------------------------------------------------------------
# What price is greater than 75% of all sales?

# quantiles
qnorm(0.75, mean=50, sd=5)


## Q5 ---------------------------------------------------------------------
# What is the probability it costs between $45 and $55?

pnorm(45, mean=50, sd=5)

pnorm(55, mean=50, sd=5)

pnorm(55, mean=50, sd=5) - pnorm(45, mean=50, sd=5)


# Exercise 5 --------------------------------------------------------------

# Can we make a function to simplify the process
# of making probability calculations of Between X1 and X2? (like above)
def pslice(x1, x2, mean, sd):
    return pnorm(x2, mean=mean, sd=sd) - pnorm(x1, mean=mean, sd=sd)


# It works!
pslice(x1=45, x2=55, mean=50, sd=5)


# Exercise 6 --------------------------------------------------------------

# dexp()
# pexp()
# qexp()
# rexp()

rate = 0.002
mu = 1 / rate
mu
# Our product has a mean time to failure of 500 hours of use

# 1. Make a DataFrame of hours from 1 to 1000
# 2. Calculate the probability density
# 3. Calculate the cumulative probability
# 4. Plot one of them.


# Exercise 7 --------------------------------------------------------------

# How do we get the CDF from an observed vector?

# Empirical Hours to Failure for Some Toasters
obs = [10, 50, 20, 30, 40, 50, 30, 20, 90]

# observed density function
dobs = approxfun(tidy_density(density(obs)))

# See the observed PDF
# In R: obs %>% density() %>% broom::tidy() %>% plot()
(ggplot(tidy_density(density(obs)), aes(x='x', y='y')) + geom_line())

# Get the CDF from the observed PDF
pobs = approxfun(
    tidy_density(density(obs))
    .rename(columns={'x': 'hours', 'y': 'prob'})
    .assign(cprob=lambda df: df['prob'].cumsum() / df['prob'].sum())
    # approxfun() wants columns named x and y
    .rename(columns={'hours': 'x', 'cprob': 'y'})[['x', 'y']]
)

pobs(50)


# Let's write ourselves a function get_pobs()
# to help us get the CDF from an observed vector
def get_pobs(obs):

    return approxfun(
        tidy_density(density(obs))
        .rename(columns={'x': 'hours', 'y': 'prob'})
        .assign(cprob=lambda df: df['prob'].cumsum() / df['prob'].sum())
        .rename(columns={'hours': 'x', 'cprob': 'y'})[['x', 'y']]
    )


pobs = get_pobs(obs)
pobs(50)

# Cleanup!
globals().clear()
