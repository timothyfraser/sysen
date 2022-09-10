# Recitation 3: PDFs and CDFs in R
# Dr. Fraser, Fall 2022

# Below, please find the following content for our recitation class from Friday.

# Exercise 1: Class teaches Dr. Fraser to analyze PDFs and CDFs

# Q1: Find the prob that someone visits more than 5 stalls

# Class told Dr. Fraser we need....
# Probability Density Function...
# for a Normal Distribution...
# using rnorm() function in R
# which requires...
# mean...
# sd...
# and n....

# Simulated 500 points (people) on the distribution
rnorm(n = 500, mean = 5.5, sd = 2.5)

# That's cool, but wait! That's not quite what we need! 
# We're looking for the cumulative probability.

# Cumulative Probability that someone visits less than 5 stalls
x <- pnorm(5, mean = 5.5, sd = 2.5)
x
# Cumulative probability that someone visits MORE than 5 stalls?
1 - x


# Q2. How to make an empirical probability density function?
# Eg. get the exact PDF for a real observed vector of data

# Let's load our vector
obs <- c(1, 5, 3, 4, 3, 2, 3)

# Let's load our packages
library(dplyr) 
library(broom)
library(ggplot2)

# Use density() to get the x and y coordinates for our density plot,
# then use tidy() to put those values in a nice data.frame with an x and y column
dat <- obs %>% density() %>% tidy()

# Graph it!
ggplot(data = dat, mapping = aes(x = x, y = y)) +
  geom_area()

ggplot(data = dat, mapping = aes(x = x, y = y)) +
  geom_area(fill = "steelblue") +
  geom_line(color = "pink", size = 10)

# Using approxfun(), we can take those x and y coordinates and
# generate our own empirical probability density function,
# much like the dnorm function, except it doesn't require any parameters (because we've got the real thing!)
dobs <- dat %>% approxfun()

# Try it out, for a value of x of 3
dobs(3)
# x = 0
dobs(0)

# Supply it a vector
c(0,1,2,3,4,5,6) %>% dobs()

# Easy way to write 0 to 6
0:6 %>% dobs()

# We can also calculate the cumulative probability density, p
dat  %>%
  mutate(
    # Taking the cumulative sum of the densities...
    ycum = cumsum(y),
    # and then normalizing them by the sum of all densities, so it goes from 0 to 1
    p = ycum / sum(y))

# We can code the CDF even more succinctly like so
pobs <- dat %>%
  mutate(y = cumsum(y) / sum(y)) %>%
  # And use approxfun to create a CDF function styled afted pnorm(), but for our observed data
  approxfun()

# Try out our CDF function!
0:5%>% pobs()
# Notice how it gets closer and closer cumulatively to 1?

# Visualize it!
dat %>%
  mutate(y = cumsum(y) / sum(y)) %>%
  ggplot(mapping = aes(x = x , y =y)) +
  geom_area()


# How to check colors
colors




# Questions for Recitation 3


# The cost of a component varies depending on market conditions.
# Over the last year, analysts report is cost on average $50, 
# with a standard deviation of $5.

# What is the probability the component will cost exactly $60?


# What is the probability the component costs less than $60?


# What is the probability that the component costs more than $60?

# What price is greater than 75% of all sales?


# What is the probability it costs between $45 and $55?



# Q2. You're developing a new medical device for measuring blood sugar. You might test "High" (T = 1) vs. "Fine" (0), and you might *actually* be "High" (R = 1) or "Fine" (0) 

# Given that you tested "High", what's the probability that your blood sugar is *actually* "High"?
# Fortunately, you collected the crosstable.
# Here's your data.

# 4 people really were "High" when they tested "High".
# 6 people really were "High" when they tested "Fine".
# 5 people really were "Fine" when they tested "Fine".
# 3 people really were "Fine" when they tested "High".

# Find the probability P(R=1|T=1), and use this empirical data to PROVE that Bayes Rule works.
