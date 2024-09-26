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
