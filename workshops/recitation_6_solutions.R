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

dat <- data.frame(
  person = c("Tim", "Melanie", "Taka", "David", "Courtney"),
  coffee = c(1,3,5,6,3),
  price = c(5.00, 3.00, 2.33, 5.33, 2.33)
)

# 2. Take the mean and standard deviation of one 
# of your numeric vectors in your data.frame!

dat$coffee %>% mean()
dat$coffee %>% sd()

# 3. Take the mean and standard deviation, but this time use 'summarize'!
dat %>%
  summarize(
    mu = mean(coffee),
    sigma = sd(coffee))

# 4. Add a new column to your dataframe using mutate(), 
# and save your new data.frame as dat2.
dat2 <- dat %>%
  mutate(place = c("Gimme Coffee", "Collegetown Bagels",
                   "Gimme Coffee", "Gimme Coffee",
                   "Upson"))

# 5. Add a new column to dat2 using rnorm(), 
# simulating n() cases with a mean of 3 and a standard deviation of 2.
# Save it as dat3.

dat3 <- dat2 %>%
  mutate(tastiness = rnorm(n = n(), mean = 3, sd = 2))


# 6. Make an addition function called 'add()' with 2 inputs. 
# Add together 120 and 350.
add = function(a, b){ a + b }

add(120, 350)


# 7. Make an exponential failure function (from scratch), called 'fe()'
# Get the probability of failure at time 1 given a failure rate of 0.01
fe = function(t, lambda){ 1 - exp(-t*lambda)  }
fe(t = 1, lambda = 0.01)

# 8. Make a Weibull failure function (from scratch), called fw().
# Get the probability of failure at time 1 given a characteristic life of 2000 hours and a shape parameter of 5.
fw = function(t, c, m){ 1 - exp(-(t/c)^m) }
fw(1, c = 2000, m = 5)

# 9. Make a Weibull failure rate function, called z(). 
# Doesn't have to be from scratch.
# Get the failure rate at time 1000 given a characteristic life of 2000 hours and a shape of 5
z = function(t, c, m){
  dweibull(t, scale = c, shape = m) / (1 - pweibull(t, scale = c, shape = m))
}
z(t = 1000, c = 2000, m = 5)

# 10. Get the failure rates from time 1 to 1000, 
# assuming a weibull life distribution 
# with a characteristic life of 3000 hours and a shape parameter of 2.
# Save the time and failue rates in a data.frame, called rates.

rates <- data.frame(time = 1:1000) %>%
  mutate(failure_rate = z(t = time, c = 3000, m = 2))


# 11. Plot those failure rates in your data.frame 'rates' in ggplot.
rates %>%
  ggplot(mapping = aes(x = time, y = failure_rate)) +
  geom_area()


# 12. Give that plot you made labels and at least 1 color/fill.
rates %>%
  ggplot(mapping = aes(x = time, y = failure_rate)) +
  geom_area(color = "black", fill = "steelblue") +
  labs(x = "Time t", y = "Failure Rate z(t)")


# 13. Get the log-likelihoods for a vector of 30 values (you choose),
# if lambda = 0.01, assuming an exponential life distribution

myll <- c(5,3, 20, 30 ,4, 3, 2, 200,
  34, 5,6,3, 3,5,6,64,2,3234,234,
  234,234,22,3,5,4,3) %>%
  dexp(rate = 0.01) %>%
  prod() %>%
  log()

myll

myll <- c(5,3, 20, 30 ,4, 3, 2, 200,
          34, 5,6,3, 3,5,6,64,2,3234,234,
          234,234,22,3,5,4,3) %>%
  dexp(rate = 0.01) %>%
  log() %>%
  sum()


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
# 1 - F = exp(-1*(t/c)^m )
# -log(1 - F) = 1*(t/c)^m
# (-log(1 - F))^(1/m) = t/c
# c = t / ( (-log(1 - F))^(1/m)  )

t = 150
f = 0.15
m = 1.5
# characteristic life equals....
t / ( (-log(1 - f))^(1/m)  )




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
# qnorm(f) = log(t/t50) / sigma
# qnorm(f) * sigma = log(t/t50)
# sigma = log(t/t50) / qnorm(f)

# Suppose...
t = 200
t50 = 500
f = 0.20

# The sigma, the shape parameter, should equal...
sigma <- log(t/t50) / qnorm(f)

sigma


# (2) Calculate the probability of failure after 800 hours.
t = 800
t50 = 500
pnorm( log(t/t50) / sigma )




# (3) Calculate the standard deviation of product lifespans.

# Log-Normal Variance
variance = function(t50, sigma){  t50 * exp(sigma^2) * (exp(sigma^2) - 1)  }

# Get the standard deviation!
variance(t50 = 500, sigma = sigma) %>% sqrt()

