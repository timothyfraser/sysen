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

# We're going to use several functions from
# functions/functions_distributions.py
# which adapts R functions to Python,
# while keeping the same general syntax we find in the textbook.


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
# fun fact: we've written a custom function hist() that does this quickly
hist(mynorm)

# Compare
[mynorm.mean(), mymean]
[mynorm.std(), mysd]
# Pretty close!


## Poisson Distribution ##############################
# Randomly sample from a poisson distribution of counts
# In R the parameter is 'lambda', 
# but in Python, we have to change it to 'mu',
# because lambda is a reserved term.
from scipy

rpois(n=1000, mu = 5).mean()

mypois = rpois(n = 1000, mu = mymean)
# Visualize!
ggplot(aes(x = 'mypois')) + geom_histogram()
hist(mypois)

## Exponential Distribution ######################

# Get lambda, the rate
myrate_e = 1 / sw.mean()
# Simulate
myexp = rexp(n = 1000, rate = myrate_e)
# Visualize!
ggplot(aes(x = 'myexp')) + geom_histogram()
hist(myexp)
# Compare
[1 / myexp.mean(), myrate_e]
# Pretty close!

## Gamma Distribution ################################

# For shape, we want the rate of how much greater the mean-squared is than the variance.
myshape = sw.mean()**2 / sw.var()

# For rate, we like to get the inverse of the variance divided by the mean.
myrate =  1 / (sw.var() / sw.mean() )

# Simulate it!
mygamma = rgamma(n = 1000, shape = myshape, rate = myrate)

## View it!
ggplot(aes(x = 'mygamma')) + geom_histogram()
hist(mygamma)


## What were the parameter values for this distribution?
[myshape, myrate]

## Weibull Distribution ########################

# Load extra package for fitting distributions
from scipy import stats as fitdistr

# Fit Weibull distribution with location parameter fixed to 0
myshape_w, loc, myscale_w = fitdistr.weibull_min.fit(sw, floc = 0)
# Simulate
myweibull = rweibull(n = 1000, shape = myshape_w, scale = myscale_w)
## View it!
ggplot(aes(x = 'myweibull')) + geom_histogram()
hist(myweibull)


# Special Distributions ##############################

## Binomial Distributions

rbinom(n = 10, size = 1, prob = 0.5)

# In how many cases was the observed value greater than the mean?
myprob = sum(sw > mymean) / len(sw)

# Sample from binomial distribution with that probability
mybinom = rbinom(1000, size = 1, prob = myprob)

# View histogram!
hist(mybinom)



## Uniform Distributions ##########################3

# Simulate a uniform distribution ranging from 0 to 1
myunif = runif(n = 1000, min = 0, max = 1)
# View histogram!
hist(myunif)

# Comparing Distributions #########################



# Finally, we’re going to want to outfit those vectors 
# in nice data.frames (skipping rbinom() and runif()), 
# and stack them into 1 data.frame to visualize.

# Using pandas's concat function...
mysim = p.concat(
  [
    # Make a bunch of data.frames, all with the same variable names,
    p.DataFrame({'x': sw, 'type': "Observed"}),
    # and stack them!
    p.DataFrame({'x': mynorm, 'type': "Normal"}),
    # And stack it!
    p.DataFrame({'x': mypois, 'type': "Poisson"}),
    # stack, stack, stack stack stack stack stack
    p.DataFrame({'x': mygamma, 'type': "Gamma"}),
    # so many stacks!
    p.DataFrame({'x': myexp, 'type': "Exponential"}),
    # so much data!!!!
    p.DataFrame({'x': myweibull, 'type': "Weibull"})
  ]
)



# Let's write the initial graph and save it as an object
g1 = (ggplot(data = mysim, mapping = aes(x = 'x', fill = 'type')) +
  geom_density(alpha = 0.5) +
  labs(x = "Seawall Height (m)", y = "Density (Frequency)", 
       subtitle = "Which distribution fits best?", fill = "Type"))
g1

# Then view it!
g1 + xlim(0,10)


# Yay! Be sure to complete the learning checks to test out your knowledge.
# Great work!

# Clear environment
globals().clear()
