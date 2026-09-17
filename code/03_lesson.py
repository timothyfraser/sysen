# 03_lesson.py
# Tim Fraser
# Lesson 3: New data.frame functions, and writing your own functions
# Chapter: Functions in Python
# Chapter: Distributions and Descriptive Statistics in Python

# Let's learn how to use several new pandas functions,
# and let's learn how to make our own functions.


# Getting Started ---------------------------------------------------------

import sys
import numpy as np
import pandas as pd

# Our course functions live in functions/ at the repo root.
# (Run this script from the root of the sigma repo.)
sys.path.append("functions")
from functions_distributions import pexp


# New pandas functions ----------------------------------------------------

# Make a DataFrame
chairs = pd.DataFrame({
    # unique IDs always help
    'id': [1, 2, 3, 4, 5],
    # how many people used chair each day
    'uses': [1, 5, 2, 3, 4],
    # cost of each chair
    'cost': [30, 50, 40, 100, 20]
})

## .assign() --------------------------------------------------------------

# .assign() creates or edits a column. (This is R's mutate().)
chairs.assign(value=lambda df: df['cost'] / df['uses'] / 365.25)

# overwrite a DataFrame
chairs = chairs.assign(days=[200, 300, 2, 50, 75])

chairs

## .agg() -----------------------------------------------------------------

# .agg() consolidates many rows into a summary statistic.
# (This is R's summarize().)
stat = chairs.agg({'days': 'mean'}).rename({'days': 'mttf'})

# Extract a value from that summary
stat['mttf']

## pd.concat() ------------------------------------------------------------

# Make a second DataFrame
more_chairs = pd.DataFrame({
    'id': [6, 7],
    'uses': [3, 5],
    'cost': [30, 40]
})

# stack two DataFrames together
chairs2 = pd.concat([chairs, more_chairs], ignore_index=True)

# Notice that 'days' fills with NaN for the new rows,
# since 'days' wasn't in the second DataFrame.
chairs2

## Referencing a column you just made -------------------------------------

# doesn't work!
# You can't reference 'hours' while you are still building the dictionary.
# pd.DataFrame({
#     'hours': range(20, 26),
#     'hours_later5': hours + 5
# })

# does work!
# Build the DataFrame first, then .assign() using the column you just made.
pd.DataFrame({'hours': range(20, 26)}).assign(
    hours_later5=lambda df: df['hours'] + 5)

# And you can chain .assign() to overwrite a column with one you just computed.
(pd.DataFrame({'hours': range(20, 26)})
    .assign(hours_later5=lambda df: df['hours'] + 5)
    .assign(hours=lambda df: df['hours_later5']))


# Making Functions --------------------------------------------------------

# the mathematical function for pexp() is this
# F(t) = 1 - e^(-t*lambda)
#
# NOTE: `lambda` is a reserved word in Python (it makes anonymous functions),
# so we name that input `rate`, exactly as pexp() does.
def f(t, rate):
    return 1 - np.exp(-1 * t * rate)


# Why do we care?
f(t=2, rate=0.05)
pexp(2, rate=0.05)

# Can pass vectors to functions
f(t=pd.Series([2, 5, 7, 5, 8]), rate=0.05)

# Get lots of probabilities fast
f(t=np.array([2, 5, 7, 5, 8]), rate=0.05)

# Can pass functions to DataFrames too
pd.DataFrame({'t': [2, 5, 7, 5, 8]}).assign(
    prob=lambda df: f(t=df['t'], rate=0.05))


## Anatomy of a function --------------------------------------------------

# inputs --> process --> output
# def myfunction():

# Let's make an addone() function
def addone(a):
    return a + 1


addone(a=1)
addone(1)


# This works too...
def addone(a):
    output = a + 1
    return output


addone(a=1)


# This won't work - need to return the output
# def addone(a):
#     output = a + 1
# addone(1)


## Default arguments ------------------------------------------------------

# Can add default arguments/parameters
def addone(a=2):
    return a + 1


addone()
addone(a=3)


# Can add multiple arguments/parameters
def addx(a, x):
    return a + x


addx(a=1, x=2)


# Can add testing values, as long as you comment them out
def addx(a, x):
    # testing values
    # a = 2; x = 3

    return a + x


addx(a=5, x=2)


# All done!

# Cleanup!
globals().clear()
