# recitation_4.R
# System Reliability in R
# Dr. Fraser, Fall 2022

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

r1 = 0.98
r2 = 0.95
r3 = 0.93

r_series = r1 * r2 * r3

r_series


# Parallel/Redundant System:

# To get reliability of a Parallel system of parts

# R_parallel(t) = 1 - (F_1(t) * F_2(t) * ... F_n(t) )
# or
# R_parallel(t) = 1 - (1 - R_1(t)) * (1 - R_2(t)) * ... (1 - R_n(t) )


f1 = 0.01
f2 = 0.04
f3 = 0.30

r1 = 1 - f1
r2 = 1 - f2
r3 = 1 - f3

1 - (f1 * f2 * f3)

1 - ((1- r1) * (1 - r2)  * (1 - r3))


# Q1. Nintendo made a new model of the Switch! 
# (Hypothetically) each part (cord, screen, joystick A, joystick B)  has a specific failure rate, listed below.
# Calculate the overall probability that Nintendo's entire console DOESN'T fail after 1 hour

# 1 cord (1 / 5000 days)
# 1 screen (1 / 3000 days)
# 2 joysticks (1 / 1000 days)

cord = 1/5000
screen = 1/3000
joystick = 1/1000

r = function(t, lambda){ 1 - pexp(t, rate = lambda)}
r_cord <- r(t = 1/24, lambda = cord)
r_screen <- r(t = 1/24, lambda = screen)
r_joystick <- r(t = 1/24, lambda = joystick)

r_cord * r_screen * r_joystick * r_joystick
r_cord * r_screen * r_joystick^2


# Q2. Design a function to test console reliability for any time t.
# Test reliability after 1 hour, 24 hours, and 168 hours (7 days)


nintendo = function(t){
  r(t = t, lambda = cord) *
  r(t = t, lambda = screen) * 
  r(t = t, lambda = joystick)^2
}

c(1/24, 2/24, 5/24, 10/24) %>% nintendo()



# Q3. Use your function to visualize the reliability curve 
# for this overall system in ggplot, as it ranges from 1 to 2000 hours!

# Let's make a data.frame 's' for system  

data.frame(t = 1:2000 / 24) %>%
  mutate(reliability = nintendo(t)) %>%
  ggplot(mapping = aes(x = t, y = reliability)) +
  geom_area()






##################################################
# Team Analyses
##################################################

# Below are several different systems, each relating to an image! (see images in workshops folder)
# Use corresponding system diagram to calculate the reliability of each system.

# Choose one of the two, and read up on them at this link.
# https://github.com/timothyfraser/sysen/blob/main/workshops/recitation_4_diagrams.md

# Libraries


# Electrical Wiring

