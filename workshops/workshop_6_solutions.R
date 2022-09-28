# Workshop 6 Solutions
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
d = function(t, k, lambda){
  lambda / factorial(k - 1) * (lambda*t)^(k-1) * exp(-t*lambda)
}

# Gamma CDF (failure) function!
f = function(t, k, lambda){
  # Make a vector of values from 0 to k-1
  n = seq(from = 0, to = k - 1)
  # Now compute the failure function
  1 - sum( (lambda*t)^n / factorial(n)  * exp(-lambda*t) )
}
# Because of the k, this function can't handle multiple values of t at one time
# so I recommend using mosaicCalc's antiD to integrate to get the failure function instead.
f = antiD(d(t,k,lambda)~t)

# Mean (aka mean time to fail)
mttf = function(k, lambda){   k / lambda  }
# Variance
variance = function(k, lambda){ k / lambda^2 }


# Check out that failure function!
data.frame(t = 1:100) %>%
  mutate(prob = f(t, k = 3, lambda = 0.10)) %>% 
  ggplot(mapping = aes(x = t, y = prob)) +
  geom_area()



#################################
# 2. Weibull Distribution
#################################

# Weibull PDF function!
d = function(t, m, c){
  (m / t) * (t / c)^m * exp(-1*(t/c)^m)    
}

# Weibull CDF (failure) function!
f = function(t, m, c){ 1 - exp(-1*(t/c)^m) }

# Weibull Mean Time to Fail
mttf = function(c, m){  c * gamma( 1 + 1/m)  }

# Weibull Variance
variance = function(c, m){  c^2 * gamma( 1 + 2/m ) - ( c * gamma( 1 + 1/m) )^2  }


# Check out that failure function!
data.frame(t = 1:10) %>%
  mutate(prob = f(t, m = 1, c= 10)) %>% 
  ggplot(mapping = aes(x = t, y = prob)) +
  geom_area()




#################################
# 3. Log-Normal Distribution
#################################

# Log-Normal PDF function!
d = function(t, t50, sigma){ 1 / (sigma * t * sqrt(2*pi)) * exp( -(1/ 2 * sigma^2 )*(log(t) - log(t50))^2) } 

# Log-Normal CDF (failure) function!
f = function(t, t50, sigma){  pnorm( log(t / t50) / sigma ) }

# Log-Normal MTTF
mttf = function(t50, sigma){  t50 * exp(sigma^2  / 2)  }

# Log-Normal Variance
variance = function(t50, sigma){  t50 * exp(sigma^2) * (exp(sigma^2) - 1)  }


# Check out that density function!
data.frame(t = 1:50) %>%
  mutate(prob = d(t, t50 = 5, sigma = 1)) %>%
  ggplot(mapping = aes(x = t, y = prob)) +
  geom_area()



# Suppose...
t = 50
t50 = 100
sigma = 2
# Get the cumulative probability of failure at time t
p <- pnorm( log(t/t50) / sigma )
# Check it!
p


# Get the z-score for F(t) = 0.36!
z <- qnorm(p)
# Check it!
z

# We can also use z to solve for t, t50, or sigma

# For t
# t = exp(z * sigma) * t50
exp(z * sigma) * t50 

# For t50
# t50 = t / exp(z * sigma)
t / exp(z * sigma)

# For sigma
# sigma = log(t/t50) / z
log(t/t50) / z




#################################################
# 4. Maximum Likelihood Estimation
#################################################

# Suppose our crops data has a log-normal distribution.
# Let's use MLE to estimate its parameters!

# Get our PDF (d) and CDF (f) functions again
d = function(t, k, lambda){  lambda / factorial(k - 1) * (lambda*t)^(k-1) * exp(-t*lambda) }
f = function(t, k, lambda){  pgamma(t, shape = k, rate = lambda)  }



# Let's write a new function
ll = function(data, par){
  # Our parameters input is now going to be vector of 2 values
  # par[1] gives the first value, k
  # par[2] gives the second value, lambda
  d(t = data, k = par[1], lambda = par[2]) %>% 
    prod() %>% log()
}

# Let's use optim to find the parameters with the maximum likelihood!
optim(par = c(5, 0.01), data = crops$days, fn = ll, control = list(fnscale = -1))


# What does two-parameter likelihood really mean?

# Get all combinations of these ranges
mylikelihood <- expand_grid(
  k = seq(1, 5, by = 0.1),
  lambda = seq(0.001, 0.1, by = 0.001)
) %>%
  # For each ID,
  group_by(k, lambda) %>%
  summarize(loglik = ll(crops$days, par = c(k, lambda)))

mylikelihood %>% tail()

# We could visualize it as a tile plot
mylikelihood %>%
  ggplot(mapping = aes(x = k, y = lambda, fill = exp(loglik) )) +
  geom_tile() +
  scale_fill_viridis()



#######################################################
# 4. Maximum Likelihood Estimation with Censored Data
#######################################################

# Suppose we had 75 crops, evaluated over 200 days.
# Suppose that data had also been crosstabulated (but doesn't have to be.)

crosstab <- data.frame(
  label = c("[0,40]", "(40,80]", "(80,120]", "(120,160]", "(160,200]"),
  t = c(20, 60, 100, 140, 180),
  count = c(18, 14, 10, 5, 3))

# Suppose k = 1 and lambda = 0.01
# What's the loglikelihood?
k = 1
lambda = 0.01

crosstab %>%
  summarize(
    # Get total failures observed (sum of all tallies)
    r = sum(count),
    # Get total sample size,
    n = 75,
    # Get last timestep
    tmax = 200,
    # Take the product of the PDF at each timestep
    prob_d = d(t = t, k, lambda) %>% prod(),
    # Get probability of survival by the last time step,
    # for as many n-r observations that did not fail
    prob_r = (1 - f(t = tmax, k, lambda))^(n - r),
    # Get log-likelihood
    loglik = log(prob_d * prob_r))


# Let's make it a function!

ll = function(data, par){
  output <- data %>%
    summarize(
      r = sum(count),
      n = 75,
      tmax = 200,
      prob_d = d(t = t, k = par[1], lambda = par[2]) %>% prod(),
      prob_r = (1 - f(t = tmax, k = par[1], lambda = par[2]))^(n - r),
      loglik = log(prob_d * prob_r))
  # Return the output
  output$loglik
}


# Let's use optim to find the parameters with the maximum likelihood!
optim(par = c(5, 0.01), data = crosstab, fn = ll, control = list(fnscale = -1))

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


