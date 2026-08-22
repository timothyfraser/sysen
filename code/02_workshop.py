# 02_workshop.py
# Tim Fraser
# Workshop 2: Distributions and Descriptive Statistics
# Chapter: Distributions and Descriptive Statistics in Python

# Setup -------------------------------------------------------------------

## Install packages ----
# %pip install pandas plotnine scipy

## Import packages ----
import os, sys
import pandas as p
from plotnine import *

# Our course helper functions mirror R's hist(), rnorm(), rpois(), and rexp().
sys.path.append(os.path.abspath('functions'))
from functions_distributions import *


# Data --------------------------------------------------------------------

# Louisiana parishes, after Hurricane Katrina
la = p.read_csv("workshops/la_parishes.csv")

# Percent damaged in Hurricane Katrina
la.pc_damage

# pc_damage = % houses damaged
# pc_severe = % severely damaged
# pc_poverty = % residents living in poverty


# Descriptive Statistics --------------------------------------------------

## Mean ----

# what percentage of houses were damaged
# in an average parish?
la.pc_damage.mean()

# There's no dplyr in our Python stack, so where R would pipe into
# summarize(mu = mean(pc_damage)), pandas builds that one-row table directly.
p.DataFrame({'mu': [la.pc_damage.mean()]})

## Mean and Standard Deviation ----

mu = la.pc_damage.mean()
sigma = la.pc_damage.std()

mu
sigma


# Simulating Distributions ------------------------------------------------

## Normal ----

# Draw 20 hypothetical parishes, using our mu and sigma
sims = rnorm(n=20, mean=mu, sd=sigma)

# How close is the simulated mean to the real one?
sims.mean()
mu

# And the simulated standard deviation?
sims.std()
sigma

## Histograms ----

# hist() returns a plotnine figure, so we build the object
# and then view it, just like any other ggplot.
h1 = hist(sims)
h1

h2 = hist(la.pc_damage)
h2

## Poisson ----

# R's rpois() has a twin here: rpois(n = 100, mu = mu)

## Exponential ----

# The exponential distribution's rate is 1 / mean
rexp(n=100, rate=1 / la.pc_damage.mean())

h3 = hist(rexp(n=100, rate=1 / mu))
h3
