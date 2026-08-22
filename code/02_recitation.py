# 02_recitation.py
# Tim Fraser
# Recitation 2: Descriptive Statistics and Quality Control
# Chapter: Distributions and Descriptive Statistics in Python

# Louisiana Parishes ------------------------------------------------------

## Load packages ----

import pandas as p

## Data ----

# Read in stuff
la = p.read_csv("workshops/la_parishes.csv")

## Statistics ----

# Percentage of houses damaged by the hurricane
la.pc_damage

sigma = la.pc_damage.std()
# The percentage of houses damaged by the hurricane varies from the average by ~20 (units)
mu = la.pc_damage.mean()
# The average county had 51% of houses damaged
n = len(la.pc_damage)

mu + sigma
mu - sigma

# mu + sigma*3
# mu - sigma*3

## Coefficient of Variation ----

sigma / mu

## Standard Error ----

se = sigma / n**0.5

## Confidence Interval ----

mu + se * 1.96
mu - se * 1.96

mu

## Clear our objects ----

# Python's closest match for R's rm(list = ls()) is globals().clear(),
# but that would drop our imports too, so we delete just what we made.
del la, mu, sigma, n, se


# Quality Control with Cheese ---------------------------------------------

## Packages ----

import pandas as p
from plotnine import *

## Data ----

# Hours until failure for cheese from three suppliers
a = p.Series([50, 70, 125, 235, 230, 200, 180, 260, 300, 500, 275, 280])
b = p.Series([300, 380, 250, 50, 55, 57, 60, 65, 100, 150, 250, 200, 150, 175, 225, 200, 225, 250])
c = p.Series([400, 300, 400, 300, 350, 200, 250, 300, 330, 375])

## Mean
## Std
## Coefficient of Variation / Standard Error

# Tell me who you'd buy your cheese from and why.

a.mean()
b.mean()
c.mean()

## Statistics ----

data = p.DataFrame({
  'type': ["a", "b", "c"],
  'mu': [a.mean(), b.mean(), c.mean()],
  'sigma': [a.std(), b.std(), c.std()],
  'n': [len(a), len(b), len(c)]
})

data['cv'] = data.sigma / data.mu
data['se'] = data.sigma / data.n**0.5

data['upper'] = data.mu + data.sigma
data['lower'] = data.mu - data.sigma
data

## Visualize ----

# A quoted string inside aes() maps a constant label to the color legend,
# exactly the way color = "Mean" behaves in ggplot2.
g1 = (ggplot() +
  geom_point(data=data, mapping=aes(x='mu', y='type', color='"Mean"')) +
  geom_point(data=data, mapping=aes(x='lower', y='type', color='"-1 sigma"')) +
  geom_point(data=data, mapping=aes(x='upper', y='type', color='"+1 sigma"')) +
  labs(x="Time to Failure (hours)"))
g1
