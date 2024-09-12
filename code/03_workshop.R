# workshop_3.R
# Workshop 3: PDFs and CDFs in R
# Dr. Fraser


# Below, please find the following content for our recitation class from Friday.
library(dplyr) # data wrangling
library(ggplot2) # visuals
# install.packages("mosaicCalc")
library(mosaicCalc) # derivatives and integrals


# Exercise 1: Class teaches Dr. Fraser to analyze PDFs and CDFs

### How to make a function!




### When the PDF is provided ###################################

# the function that produces the line, 
# or the probability for every x value

# probability density function --> probability distribution

d = function(x){  (x + 2*x)/1000  }

d(x = 1)
# There is a 0.3% chance that we would get a value of 1
# from this particular distribution / density function.

# EXACTLY 1. --> probability densities
# More than or Less than 1 --> cumulative probabilities


# toaster - time (hours) to failure 
# How would I use this PDF for to find probability density of failure at 50 hours?




# Make our own `tibble` (an empowered data.frame from dplyr)
# How about for 0 to 1000 hours?




# How might I plot that?



# Oooh... can I save that plot?





### Simulated Distributions ###################################

# Archetypal Distributions, normal, poisson, exponential

# What are our 4 types of probability functions?
# use poisson as an example



# mean of 50 hours to failure
mu = 50


# How would I simulate 10 products with a mean time to failure of 50 hours?
# Assume poisson


# What's the histogram look like?


# How could I get the cumulative probability,
# from 1 to 100? Use a tibble.




# Empirical Hours to Failure for Some Toasters
obs = c(10,50, 20, 30, 40, 50, 30, 20, 90)

# Make an empirical probability density function


# empirical cumulative probability function for d()
pobs = mosaicCalc::antiD(tilde = d(x) ~ x)
pobs(x = c(1,2,3))

# Can't really easily do that for our approxfun()
dobs


# probabilities densities




# The cost of a component varies depending on market conditions.
# Over the last year, analysts report is cost on average $50, 
# with a standard deviation of $5.
# Assume normal distribution - so dnorm, etc.

# Pick 2!

# Q1. What is the probability the component will cost exactly $60?



# Q2. What is the probability the component costs less than $60?




# Q3. What is the probability that the component costs more than $60?



# Q4. What price is greater than 75% of all sales?



# Q5. What is the probability it costs between $45 and $55?



