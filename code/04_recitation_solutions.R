# recitation_4_solutions.R
# Dr. Fraser
# Recitation 4: System Reliability in R

######################################
# Load Packages
######################################
library(tidyverse)
library(mosaicCalc)


###############################################
# 1. Reliability Calculations by TYPE of System
###############################################

# We also learned how to calculate reliability for a series vs. parallel system
# Quick Recap

# Series Systems:

# To get reliability of a Series of parts,
# multiply probability of reliability among each part, written R_1(t), R_2(t), etc. below 
# R_series(t) = R_1(t) * R_2(t) * R_3(t) * .... * R_n(t)

# Parallel/Redundant System:

# To get reliability of a Parallel system of parts

# R_parallel(t) = 1 - (F_1(t) * F_2(t) * ... F_n(t) )
# or
# R_parallel(t) = 1 - (1 - R_1(t)) * (1 - R_2(t)) * ... (1 - R_n(t) )


# Q1. Nintendo made a new model of the Switch! 
# (Hypothetically) each part (cord, screen, joystick A, joystick B)  has a specific failure rate, listed below.
# Calculate the overall probability that Nintendo's entire console DOESN'T fail after 1 hour

# 1 cord (1 / 5000 days)
# 1 screen (1 / 3000 days)
# 2 joysticks (1 / 2500 days)

cord = 1 / 5000
screen = 1 / 3000
joystick = 1 / 1000

r = function(t, lambda){ exp(-1*lambda*t) }

r(t = 1, lambda = cord) * 
  r(t = 1, lambda = joystick)^2 * 
  r(t = 1, lambda = screen)




# Q2. Design a function to test console reliability for any time t.
# Test reliability after 1 hour, 24 hours, and 168 hours (7 days)
nintendo = function(t){
  r(t, lambda = cord) * 
    r(t, lambda = joystick)^2 * 
    r(t, lambda = screen)
}

c(1, 24, 168) %>% nintendo()

# Q3. Use your function to visualize the reliability curve 
# for this overall system in ggplot, as it ranges from 1 to 2000 hours!

# Let's make a data.frame 's' for system  
s <- data.frame(t = 1:2000) %>%
  mutate(p_n = nintendo(t),
         p_j = r(t, lambda = joystick),
         p_c = r(t, lambda = cord),
         p_s = r(t, lambda = screen))

ggplot() +
  geom_area(data = s, mapping = aes(x = t, y = p_c, fill = "Cord"), alpha = 0.75) +
  geom_area(data = s, mapping = aes(x = t, y = p_s, fill = "Screen"), alpha = 0.75) +
  geom_area(data = s, mapping = aes(x = t, y = p_j, fill = "Joystick"), alpha = 0.75) +
  geom_area(data = s, mapping = aes(x = t, y = p_n, fill = "Overall"), alpha = 0.75) 


# What if the joysticks were a parallel system instead of a series? Maybe you only need one to function. #######################

nintendo2 = function(t){
r(t, lambda = cord) * 
(1 -     (1 - r(t, lambda = joystick)) *     (1 - r(t, lambda = joystick))   ) * 
r(t, lambda = screen)
}

# Let’s compare.
nintendo(t = 100)
nintendo2(t = 100)


######################################
# 2. Key Functions Recap
######################################

# Recently, we learned key failure/reliability functions in R, using the exponential distribution!

# Let's write a few functions for this! 
# We'll use dexp() and pexp() at the base of our functions, to reduce the likelihood of error :)

# Write function f(t), renamed d(t), to give our PDF for any time t
d = function(t, lambda){  dexp(t, rate = lambda)  }

# Write failure function F(t) to give our CDF for any time t
f = function(t, lambda){  pexp(t, rate = lambda)  }

# Write reliability function R(t) to give 1 - CDF for any time t
r = function(t, lambda){ 1 - pexp(t, rate = lambda)  }

# Write failure rate function z(t) (aka hazard rate h(t)) to give PDF / (1 - CDF) for any time t
z = function(t, lambda){ dexp(t, rate = lambda)  / (1 - pexp(t, rate = lambda)) }

# Write cumulative hazard rate function H(t), renamed h(t) for easy of coding
h = function(t, lambda){ -log( 1 - pexp(t, rate = lambda) )  }

# Write average failure rate AFR(t1, t2), to show average rate of failure between times 1 and 2
# we'll reuse h(t) from above
afr = function(t1, t2, lambda){  ( h(t2, lambda) - h(t1, lambda) ) / (t2 - t1)  }


###################################
# 3. Calculus in R
###################################

# Thanks to the mosaicCalc package…
# We can use D() to derive and antiD() to integrate.

# It's written like...

# If I have function f(x) = x^2 + 2*x
# We can get the derivative...
derivative <- D(tilde = x^2 + 2*x + z^5 ~ x)
# And use it as a function like this
derivative(x = c(1:5), z = 1)
# You could write it like this too:
f = function(x, z){ x^2 + 2*x + z^5 }
# Then take the derivative of the function
derivative2 = D(tilde = f(x, z) ~ x)
# And get valules like this!
derivative2(x = 1:5, z = 1)

# We can get the integral...
integral <- antiD(tilde = x^2 + 2*x + z^5 ~ x)
# And use it as a function like this.
integral(x = c(1:5), z = 1)
# Or if we wrote it as a function again...
f = function(x, z){ x^2 + 2*x + z^5 }
# You could take the derivative of the function!
integral2 = antiD(tilde = f(x, z) ~ x)
# And get values!
integral2(x = 1:5, z = 1)


# Let's practice that a bit.

# Suppose we have our PDF function as d(t, lambda)
d = function(t, lambda){ lambda*exp(-1*lambda*t) }
# and our CDF function as f(t, lambda)
f = function(t, lambda){ 1 - exp(-1*lambda*t) }
# so our reliability function is...
r = function(t, lambda){  exp(-1*lambda*t) }

# Q1. Find the integral of d(). What does it equal?

fc = antiD(tilde = lambda*exp(-1*lambda*t) ~ t)
fc = antiD(tilde = d(t, lambda) ~ t)
fc(t = 1:3600, lambda = 1/1200) %>% hist()
# Compare with original
f(t = 1:3600, lambda = 1/1200) %>% hist()


# Q2. Find the derivative of f()
dc = D(tilde = 1 - exp(-1*lambda*t) ~ t)
dc = D(tilde = f(t, lambda) ~ t)
dc(t = 1:3600, lambda = 1/1200) %>% hist()
# Compare with original
d(t = 1:3600, lambda = 1/1200) %>% hist()


# Q3. Find the negative derivative of r() 
dc2 = D(tilde = -1*r(t, lambda) ~ t)
dc2(1:3600, lambda = 1/1200) %>% hist()
d(1:3600, lambda = 1/1200) %>% hist()



# Q4. Find 1 - the integral of d()
fc = antiD(tilde = d(t, lambda) ~ t)
(1 - fc(1:3600, lambda = 1/1200)) %>% hist()
r(1:3600, lambda = 1/1200) %>% hist()





