# # 03_training.py
# Training: Distributions and Descriptive Statistics
# Pairs with R training:
# https://timothyfraser.com/sigma/workshop-distributions-and-descriptive-statistics.html
# Tim Fraser

# Getting Started ##########################

# Load packages
import pandas as p # Import pandas functions
from plotnine import * # import plotnine 
import os
import sys
 # Append files in this folder (functions) to the Python Path
sys.path.append(os.path.abspath('functions'))
# Now you can reference them directly
from functions_distributions import *


# Our Data ####################


# You could code it as a vector, save it as an object, then use your functions!
sw = p.Series([4.5, 5, 5.5, 5, 5.5, 6.5, 6.5, 6, 5, 4])
# View it
sw


# Size ########################

## Length ##########################

# How big is our sample?
len(sw)

# Location #######################

## Mean #######################
sw.mean()
## Median ########################
sw.median()
## Mode ########################
sw.mode()

# Spread (1) ###########################


# Percentiles
sw.quantile(q = 0) # min
sw.quantile(q = 1) # max


sw.quantile(q = .75) # 75th percentile

# Spread (2) ##########################

## Standard Deviation #####################


x = (sw - sw.mean())**2 # get squared deviations from mean
x = x.sum() # get sum
x = x / (len(sw) - 1) # divide by length - 1
x = x**0.5 # square root

x # view it

# Or, much more quickly...
sw.std()

# Remove x
del x

## Variance ########################

sw.var()

sw.std()**2 # same!


## Coefficient of Variation (CV) ###############

# How many times does the mean fit into the standard deviation?
# How great a share of the mean does that average variation constitute?
sw.std() / sw.mean()

## Standard Error (SE) ###########################
# How big is the variation in the data, given how big the data sample size is?

# sample size adjusted variance
sw.var() / len(sw)

# standard area = sample size adjusted standard deviation
# Calculated as 
se = sw.std() / (len(sw)**0.5)
se 
# Or as:
(sw.std()**2 / len(sw) )**0.5
# Or as
(sw.var() / len(sw))**0.5


# Shape #############################

## Skewness ########################

diff = sw - sw.mean()
diff**3
n = len(sw) - 1
sigma = sw.std()
sum(diff**3) / n
sum(diff**3) / (n * sigma**3)

# We could even write ourselves a function for it
# This is in the functions/functions_distributions.py script you loaded
# try it!
skewness(x = sw)

# Get skewness from a pandas series
sw.skew() # their formula differs slightly.


## Kurtosis  ########################


diff = sw - sw.mean()
diff**4
n = len(sw) - 1
sigma = sw.std()
sum(diff**4) / n
sum(diff**4) / (n * sigma**4)

# We could even write ourselves a function for it
# This is in the functions/functions_distributions.py script you loaded
# try it!
kurtosis(sw)

# Get kurtosis from a pandas series
sw.kurtosis() # their formula differs slightly
sw.kurt()


# Finding Parameters for Your Distributions #######################

# Reload your data, in case it changed
sw = p.Series([4.5, 5, 5.5, 5, 5.5, 6.5, 6.5, 6, 5, 4])

# Common Distributions ##############################

## Normal Distributions #########################

# rnorm() can randomly generate for us any numbers randomly sampled from a normal distribution.
# This is a wrapper function, loaded from functions/functions_distributions.py

# For example
mymean = sw.mean()
mysd = sw.std()
# simulate!
mynorm = rnorm(n = 1000, mean = mymean, sd = mysd)
# Visualize the histogram
ggplot(aes(x = 'mynorm')) + geom_histogram()

# Compare
[mynorm.mean(), mymean]
[mynorm.std(), mysd]
# Pretty close!


## Poisson Distribution ##############################
# Randomly sample from a poisson distribution of counts
# In R the parameter is 'lambda', 
# but in Python, we have to change it to 'mu',
# because lambda is a reserved term.
mypois = rpois(n = 1000, mu = mymean)
# Visualize!
ggplot(aes(x = 'mypois')) + geom_histogram()

## Exponential Distribution ######################

# Get lambda, the rate
myrate_e = 1 / sw.mean()
# Simulate
myexp = rexp(n = 1000, rate = myrate_e)
# Visualize!
ggplot(aes(x = 'myexp')) + geom_histogram()
# Compare
[1 / myexp.mean(), myrate_e]
# Pretty close!

## Gamma Distribution ################################


# Clear environment
globals().clear()
