# Workshop 6 Solutions
# Useful Life Distributions
# Dr. Fraser, Fall 2022

###############################
# 0. Getting Started
###############################

# Let's load our packages
library(tidyverse)
library(mosaicCalc)

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

# Mean (aka mean time to fail)
mttf = function(k, lambda){   k / lambda  }
# Variance
variance = function(k, lambda){ k / lambda^2 }




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



#################################
# 2. Weibull Distribution
#################################

# Log-Normal MTTF
mttf = function(t50, sigma){  t50 * exp(sigma^2  / 2)  }

# Log-Normal Variance
variance = function(t50, sigma){  t50 * exp(sigma^2) * (exp(sigma^2) - 1)  }



credentials::set_github_pat()

