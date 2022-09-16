# recitation_4_solutions.R
# Dr. Fraser, Fall 2022
# Recitation 4: System Reliability in R

######################################
# Load Packages
######################################
library(tidyverse)
library(mosaicCalc)

######################################
# Recap
######################################

# In Wednesday's Workshop 4, we learned to code key failure/reliability functions in R, 
# using the exponential distribution!

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


###############################################
# Reliability Calculations by TYPE of System
###############################################

# We also learned in Workshop 4 how to calculate reliability for a series vs. parallel system
# Section 5.1 & 5.2
# https://timothyfraser.github.io/sysen/workshop_4

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








##################################################
# Team Analyses
##################################################

# Below are several different systems, each relating to an image! (see images in workshops folder)
# Use corresponding system diagram to calculate the reliability of each system.

# Choose one of the two, and read up on them at this link.
# https://github.com/timothyfraser/sysen/blob/main/workshops/recitation_4_diagrams.md

# Libraries


# Electrical Wiring


