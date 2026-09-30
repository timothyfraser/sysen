# 00_demo.py
# A live-coding demo: base Python, pandas, and probability functions.
# It mirrors 00_demo.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.

# Packages ###################################

# !pip install -r functions/requirements.txt
import sys
import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr + readr in R)
from plotnine import *         # visuals (ggplot2 in R)

# Our course functions live in functions/ at the repo root.
# They give us R-style probability functions: rnorm(), dnorm(), dexp(), ...
sys.path.append("functions")
from functions_distributions import (
  hist, density, tidy_density, approxfun,
  rnorm, dnorm, dexp, pexp, qexp
)

# NOTE: R's broom::tidy() turns a density() into a data.frame.
# Here, tidy_density() does that job, and approxfun() matches R's approxfun().


# Base Python ###################################

# A vector in R is a list (or a numpy array) in Python
print([1, 2, 34, 4, 5])

# spreadsheets!
print(pd.DataFrame({'x': [1, 2, 3], 'name': ["Tim", "Briana", "Kunj"]}))

dat = pd.DataFrame({
  'x': [1, 2, 3],
  'name': ["Tim", "Briana", "Kunj"]})

print(dat)

# R's dat$x is dat.x (or dat['x']) in Python
print(dat.x + 2)

dat['x'] = dat.x + 2

print(dat)

dat['y'] = 3
print(dat)

dat['y'] = [1, 2, 3]

print(dat)


# pandas operations ###################################
dat = pd.DataFrame({
  'x': [1, 2, 3],
  'name': ["Tim", "Briana", "Kunj"]})

# NOTE: R chains steps with the pipe %>% (ctrl shift m).
# pandas chains steps with dots: dat.step1().step2()
# links inputs to functions
print(dat[['name']])

# select(dat, name) - same thing, written another way
print(dat.filter(['name']))


print(dat[['x']].assign(y = [53, 44, 33]))

print(dat.x.mean())
print(np.mean(dat.x))


dat2 = dat[['x']].assign(y = [53, 44, 33])

# Take a data.frame and shrink it into 1 row
print(pd.DataFrame({'mu': [dat2.x.mean()], 'mu_y': [dat2.y.mean()]}))

print(pd.DataFrame({
  'mu': [dat2.x.mean()],
  'mu_y': [dat2.y.mean()]
}))


print(pd.DataFrame({
  'mu': [dat2.x.mean()],
  'sd': [dat2.x.std()],
  'count': [len(dat2.x)],
  'median': [dat2.x.median()],
  'min': [dat2.x.quantile(0.00)],
  'max': [dat2.x.quantile(1.00)],
  'q75': [dat2.x.quantile(0.75)]
}))

# Stack two data.frames on top of each other.
# (R's bind_rows() is pd.concat(); missing columns fill with NaN, R's NA)
superdat = pd.concat([dat, dat2], ignore_index = True)
print(superdat)

# reorder columns?
print(superdat[['name', 'x', 'y']])
# Overwrite data.frame
superdat = superdat[['name', 'x', 'y']]

print(superdat) # view it


# Probability Functions ########################

# probability + iteration

# 4 types of probability functions ('normal' example)
# rnorm
# dnorm
# pnorm
# qexp

# take a random sample from a normal distribution
x = rnorm(n = 1000, mean = 0, sd = 1)
hist(x)

# histograms stack frequeny of values in a vector
# distributions appproximate shape of histogram as a line
# distribution = PDF (probability density function)

# Approximate
density(x)
# Want to see it?
# NOTE: R's plot(density(x)) draws it in base graphics; we use ggplot.
(ggplot(tidy_density(density(x)), aes(x = 'x', y = 'y')) + geom_line())

# This is the density function as a line
print(tidy_density(density(x)))


# Turn this data.frame of densities into a function...
dobs = approxfun(tidy_density(density(x)))
# What's the probability density when x = 0?
print(dobs(0))

# dobs is an observed probability density function.
# we made it because we had a vector of data.

# Instead... we often need 'hypothetical distributions'
# normal *****
# poisson
# gamma
# exponential *****
# weibull
# lognormal
# uniform
# binomial

# If we know the traits of our data (parameters)
mu = x.mean()
sigma = x.std()

print([mu, sigma])

# Make me a normal distribution
# whose sample size is 1000
# whose mean is the mean of our observed data
# whose std is the std of our observed data
hist(rnorm(n = 1000, mean = mu, sd = sigma))
# equivalent
hist(rnorm(1000, mu, sigma))

# like dobs() density
# what's the probability density when x = 0
# if normal distribution with these traits
print(dnorm(0, mean = mu, sd = sigma))

# alternatively,
# what's the probability density when x = 0
# if exponential distribution with this trait
print(dexp(0, rate = 1 / mu))


# R's tibble() is pd.DataFrame() here too

mu = 1500

# smart data.frame
# NOTE: R's tibble() lets dprob use the t it just made; in pandas we
# make t first. R's 0:2000 is np.arange(0, 2001) (the end is excluded).
t = np.arange(0, 2001)
dat = pd.DataFrame({
  # as product lifespan goes from t = 0 to 1000 hours
  't': t,
  # What is the probability density
  'dprob': dexp(t, rate = 1 / mu)
})

(ggplot() +
  geom_area(data = dat, mapping = aes(x = 't', y = 'dprob')))

# With a data.frame
print(pd.DataFrame({'t': np.arange(0, 2001)})
      .assign(dprob = lambda d: dexp(d.t, rate = 1 / mu)))



t = np.arange(0, 5001)
dat = pd.DataFrame({
  # as product lifespan goes from t = 0 to 1000 hours
  't': t,
  # What is the probability density at time t
  'dprob': dexp(t, rate = 1 / mu),
  # What is the cumulative probability at time t
  'cprob': pexp(t, rate = 1 / mu)
})

(ggplot() +
  geom_line(data = dat, mapping = aes(x = 't', y = 'dprob')))

(ggplot() +
  geom_line(data = dat, mapping = aes(x = 't', y = 'cprob')))

# Looks like 75% of products fail by t = 2000 hours of use.
# d / p





t = np.arange(0, 5001)
# calculate cumulative probability
cprob = pexp(t, rate = 1 / mu)
dat = pd.DataFrame({
  't': t,
  'cprob': cprob,
  # qexp = quantile function
  # It translates percentiles/cumulative probabilities
  # back into x axis values
  'q': qexp(cprob, rate = 1 / mu)
})

print(dat)


# rexp
# dexp
# pexp
# qexp

# Suppose we have 300 phones
# How many phones do we expect would fail after time t?
print(dat.assign(prob2 = dat.cprob * 300))
