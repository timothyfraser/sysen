#' @name lesson_7
#' @author Tim Fraser
#' @title Lesson 7 - Exponential Distribution!
#' @note more info here: https://timothyfraser.com/sigma/ 


library(dplyr)
library(readr)
library(mosaicCalc)

masks <- read_csv("workshops/masks.csv")

masks %>% glimpse()

# Let's write some functions!
# failure function (CDF)
f = function(t, lambda){ 1 - exp(-1*t*lambda)}
# reliability function
r = function(t, lambda){ exp(-1*t*lambda) }



stat <- masks %>%
  summarize(
    # The literal mean time to fail 
    # in our observed distribution is this
    mttf = mean(left_earloop),
    # And lambda is this...
    lambda = 1 / mttf,
    # The observed median is this....
    median = median(left_earloop),
    # But if we assume it's an exponential distribution
    # and calculate the median from lambda,
    # we get t50, which is very close.
    t50 = log(2) / lambda)

masks$left_earloop %>% hist()

stat$lambda

r(t = 10 + 5, lambda = stat$lambda) / r(t = 10, lambda = stat$lambda)





cr = function(t, x, lambda){
  # We can actually nest functions inside each other, 
  # to make them easier to write
  r = function(t, lambda){ exp(-1*t*lambda)}
  
  # Calculate R(x + t) / R(t) 
  output <- r(t = t + x, lambda) / r(t = t, lambda)
  
  # and return the result!
  return(output)
}

cr(t = 10, x = 5, lambda = stat$lambda)




# Calculate Mean Residual Life
mu = function(t, lambda){
  
  # Get the Reliability Function for exponential distribution
  r = function(t, lambda){ exp(-1*t*lambda)}
  
  # Get the MTTF (integral of reliability function)
  mttf = antiD(tilde = r(t, lambda) ~ t)
  
  # Now calculate mu(), the Mean Residual Life function at time t
  output <- mttf(t = Inf, lambda = lambda) / r(t = t, lambda = lambda)
  
  return(output)
}

# Get the MTTF (integral of reliability function)
r = function(t, lambda){ exp(-1*t*lambda)}
r(t = 100, lambda = 0.01)

mttf = antiD(tilde = r(t, lambda) ~ t)

# mttf(t = 1000, lambda = 0.001)
mttf(t = Inf, lambda = 0.001)

1 / 0.001
