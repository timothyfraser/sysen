# What this file is ----------------------------------------------------------
#
# The five reliability functions for a part whose failures follow an
# exponential distribution: the chance it has failed by time t, the chance
# it is still working, the failure rate, the cumulative hazard, and the
# average failure rate across an interval.
#
# Load it, from the top of the project folder:
#   source("functions/functions_reliability.R")
#
# Then try:
#   r(t = 1000, lambda = 1/2000)   # chance a part survives to 1000 hours
#
# You never need to edit anything below.
#

#' @name functions_reliability.R
#' @title Functions for Reliability (Exponential Distribution)

library(mosaicCalc)

# Failure Function
f = function(t, lambda){ 1 - exp(-lambda * t) }

# Example
# f(t = 365.25*24, lambda = 1/1200)

# Reliability Function
r = function(t, lambda){  1 - f(t, lambda)    }
r = function(t, lambda){ exp(-lambda * t)    }

# Failure Rate Function
z = function(t, lambda){ 
  fd = D(tilde = f(t, lambda) ~ t)
  fd(t, lambda) / r(t, lambda) 
}

# Accumulative Hazard Function
h = antiD(tilde = z(t, lambda) ~ t)
h = function(t, lambda){ -log(r(t, lambda)) }

# Average Failure Rate Function
afr = function(t1, t2, lambda){
  top = h(t = t2, lambda = lambda) - h(t = t1, lambda = lambda)
  bottom = t2 - t1
  top / bottom
}
