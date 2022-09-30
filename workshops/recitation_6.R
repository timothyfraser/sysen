# Recitation 6 Solutions
# Dr. Fraser, 2022

# Load Packages
library(tidyverse)
library(mosaicCalc)
library(broom)


############################
# Coding Review Checklist
############################

# You just learned a LOT of code in the last few weeks!
# But which parts are really key to know going forward?
# Here's a checklist of problems we have covered 
# through our tutorials, workshops, and recitations.
# Use this as a guide! 

# If you can do these, you should feel pretty good 
# about your coding going forward. 
# Unsure how to do some of these? That's okay! 
# Make this checklist your goal.



# 1. Make a data.frame with 3 vectors and 5 rows, named 'dat.'


# 2. Take the mean and standard deviation of one 
# of your numeric vectors in your data.frame!


# 3. Take the mean and standard deviation, but this time use 'summarize'!

# 4. Add a new column to your dataframe using mutate(), 
# and save your new data.frame as dat2.

# 5. Add a new column to dat2 using rnorm(), 
# simulating n() cases with a mean of 3 and a standard deviation of 2.
# Save it as dat3.


# 6. Make an addition function called 'add()' with 2 inputs. 
# Add together 120 and 350.


# 7. Make an exponential failure function (from scratch), called 'fe()'
# Get the probability of failure at time 1 given a failure rate of 0.01

# 8. Make a Weibull failure function (from scratch), called fw().
# Get the probability of failure at time 1 given a characteristic life of 2000 hours and a shape parameter of 5.

# 9. Make a Weibull failure rate function, called z(). 
# Doesn't have to be from scratch.
# Get the failure rate at time 1000 given a characteristic life of 2000 hours and a shape of 5



# 10. Get the failure rates from time 1 to 1000, 
# assuming a weibull life distribution 
# with a characteristic life of 3000 hours and a shape parameter of 2.
# Save the time and failue rates in a data.frame, called rates.


# 11. Plot those failure rates in your data.frame 'rates' in ggplot.

# 12. Give that plot you made labels and at least 1 color/fill.

# 13. Get the log-likelihoods for a vector of 30 values (you choose),
# if lambda = 0.01, assuming an exponential life distribution

# 14. Write a maximum likelihood function and use optim for that.

# (See workshop 6)


# 15. Write me 3 examples, explaining
# what pweibull, qweibull, and dweibull require as inputs and then output




# Workshop 6 Problems

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


# (2) Calculate the probability of failure after 800 hours.




# (3) Calculate the standard deviation of product lifespans.

