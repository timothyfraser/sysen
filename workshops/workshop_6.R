# Workshop 6 (Your copy)
# Useful Life Distributions
# Dr. Fraser, Fall 2022

###############################
# 0. Getting Started
###############################

# Let's load our packages
library(tidyverse)
library(mosaicCalc)
library(viridis)

# Import crop failure data
crops <- read_csv("workshops/crops.csv")


# Let's write a few functions!

#################################
# 1. Gamma Distribution
#################################

# Gamma PDF function!

# Gamma CDF (failure) function!


# Mean (aka mean time to fail)

# Variance



# Check out that failure function!
# Suppose k = 3, lambda = 0.10, and t = 1:100








#################################
# 2. Weibull Distribution
#################################

# Weibull PDF function!

# Weibull CDF (failure) function!

# Weibull Mean Time to Fail

# Weibull Variance


# Check out that failure function!
# Suppose c = 10, m = 1, and t = 1:10







#################################
# 3. Log-Normal Distribution
#################################

# Log-Normal PDF function!

# Log-Normal CDF (failure) function!

# Log-Normal MTTF

# Log-Normal Variance


# Check out that density function!
# Suppose t50 = 5, sigma = 1, and t = 1:50








# Suppose...
t = 50
t50 = 100
sigma = 2
# Get the cumulative probability of failure at time t

# Get the z-score for F(t) = 0.36!



# We can also use z to solve for t, t50, or sigma

# For t

# For t50

# For sigma







#################################################
# 4. Maximum Likelihood Estimation
#################################################

# Suppose our crops data has a log-normal distribution.
# Let's use MLE to estimate its parameters!

# Get our PDF (d) and CDF (f) functions again


# Let's write a log-likelihood function

# Let's use optim to find the parameters with the maximum likelihood!





#######################################################
# 5. Maximum Likelihood Estimation with Censored Data
#######################################################

# Suppose we had 75 crops, evaluated over 200 days.
# Suppose that data had also been crosstabulated (but doesn't have to be.)

crosstab <- data.frame(
  label = c("[0,40]", "(40,80]", "(80,120]", "(120,160]", "(160,200]"),
  t = c(20, 60, 100, 140, 180),
  count = c(18, 14, 10, 5, 3))

# Suppose k = 1 and lambda = 0.01
# What's the loglikelihood?


# Let's make a new log-likelihood function!

# Let's use optim to find the parameters with the maximum likelihood!





# Yay! Pretty comparable!

# Sometimes you'll get warnings,
# because you're dealing with numbers that are pretty close to zero.
# As long as the warning makes sense, you'll be fine.


# Tada!
# You can maximize likelihood and get parameter estimates for anything now!




# Problems

################################
# Q1. Characteristic Life
################################

# Find the characteristic life necessary 
# for 15% of failures to occur by 180 hours, 
# if the shape parameter m=3.

# Hint: derive it from the Weibull CDF formula
# F = 1 - exp(-1*(t/c)^m)




################################
# Q2. Sigma and the Log-Normal
################################

# A coffee company produces milk frothers! 
# These electronics have a median lifespan of about 500 hours, 
# and 20% were observed to fail after 200 hours.
# Suppose they have a log-normal distribution.
# (1) Find the shape parameter for this distribution, and
# (2) Calculate the probability of failure after 800 hours.
# (3) Calculate the standard deviation of product lifespans.

# Hint: derive it from the failure function
# f = pnorm( log(t/t50) / sigma )


# (1) Find the shape parameter for this distribution

# f = pnorm( log(t/t50) / sigma )

# sigma, the shape parameter, should equal...



# (2) Calculate the probability of failure after 800 hours.



# (3) Calculate the standard deviation of product lifespans.

