# workshop_4.R
# Dr. Fraser

# In today's workshop, let's practice our many, many ways 
# of using failure functions to analyze system reliability! 

# See workshop_4_solutions.R for solutions (but only after class!)

# 0. Load Packages ################################################3
library(dplyr)
library(ggplot2)
library(mosaicCalc)


# 1. Making Functions ##############################################

# You learned to make Functions in Week 3. Let's practice!
# https://timothyfraser.com/sigma/skill-functions-in-r.html

# Nintendo is product testing its next Switch console.
# 1000 enthusiastic children received a console in the mail,
# played video games for days on end, and 
# parents called in when the console eventually broke.

# On average, 1 console failed every 1200 hours (50 days).

# So, we say the constant failure rate lambda was 1/1200 hours

# Using your notes from Workshop 4, let's write a few functions using lambda!




### Example Function l() (for lambda) ###################################

# The exponential distribution has one parameter
# lambda = the rate of failure
# 1 / mean time to failure


# units = how many pokeballs failed
# hours = how many hours they were used

# mu = hours / units ( mean hours to failure)
# lambda = 1 / mu
# every hour, how many pokeballs do we expect to fail?

l = function(units, hours){ units / hours }


# We have an empirical failure rate of 0.2 pokeballs per hour




# Note: In r, for exponential distribution,
# we write e^something as exp(something)

# Q1. Let's write our probability density function d(t)
# PDF loooks like: d(t) = lambda * e^(-lambda*t)


# d(t) = density 
# f(t) = failure rate
# r(t) = reliability
# z(t) = failure rate
# h(t) = accumulative hazard
# afr(t) = average failure rate

d = function(t, lambda){  lambda * exp(-1*lambda*t)   }

f = function(t, lambda){ 1 - exp(-lambda*t)}
# 1 - e^(-lambda*t)

# Or, you could integrate the PDF to produce the equivalent function!!
f2 = mosaicCalc::antiD(tilde = d(t, lambda) ~ t)
f2(t = 100, lambda = 0.01)

f(t = 100, lambda = 0.01)


# PDF f(t) is always d(t) in R
d(t = 100, lambda = 0.01)
dexp(x = 100, rate = 0.01)


# INTEGRATING FUNCTIONS ##############################################

# PDF d(t) (also called little f(t), but to avoid confusion, we say d(t))
d = function(t, lambda){  lambda * exp(-1*lambda*t) }

# Failure F(t)
f = function(t, lambda){ 1 - exp(-1*lambda*t) }

# cumulative probability of failure by 100 hours?
f(t = 100, lambda = 0.01)
pexp(q = 100, rate = 0.01)



# Or, you could integrate the PDF to produce the equivalent function!!
f2 = mosaicCalc::antiD(tilde = d(t, lambda) ~ t)
f2(t = 100, lambda = 0.01)







# VISUALIZE IT ########################################


lambda_a = .01
lambda_b = .005

tibble(
  t = 1:1000,
  prob_a = r(t = t, lambda = lambda_a),
  prob_b = r(t = t, lambda = lambda_b)
)


# Reliability R(t)
f = function(t, lambda){ 1 - exp(-1*lambda*t) }
r = function(t, lambda){ 1 - f(t, lambda) }


dat = tibble(
  t = 1:1000,
  prob_a = r(t = t, lambda = lambda_a),
  prob_b = r(t = t, lambda = lambda_b)
)

ggplot() +
  geom_area(data = dat, mapping = aes(x = t, y = prob_b),
            alpha = 0.5, fill = "darksalmon") +
  geom_area(data = dat, mapping = aes(x = t, y = prob_a),
            alpha = 0.75, fill = "seagreen") +
  labs(x = "Hours to Failure", y = "Reliability (%)")



ggplot() +
  geom_area(data = dat, mapping = aes(x = t, y = prob_a, fill = "A"), alpha = 0.5) +
  geom_area(data = dat, mapping = aes(x = t, y = prob_b, fill = "B"), alpha = 0.5) +
  scale_fill_manual(values = c('seagreen', "darksalmon"))

ggplot() +
  geom_line(data = dat, mapping = aes(x = t, y = prob_a, color = "A"), 
            alpha = 0.5, linewidth = 1.5) +
  geom_line(data = dat, mapping = aes(x = t, y = prob_b, color = "B"),
            alpha = 0.5, linewidth = 1.5) +
  scale_color_manual(values = c('seagreen', "darksalmon")) +
  theme_classic()




# Failure Rate Function ##################################################
z = function(t, lambda){ dexp(t, lambda) / (1 - pexp(t, lambda) )}
z(t = 0.5, lambda = 0.01)


# Q2. Let's write our failure function f(t) ###################################
f = function(t, lambda){1 - exp(-1*lambda * t)}


# Q3. Let's write our reliability function r(t) ###################################
r = function(t, lambda){exp(-1 * lambda * t)}

# Q4. Let's write our failure rate z(t) (hazard rate) ###################################
z = function(t, lambda){
  # density function / aka change in failure function
  lambda * exp(-1 * lambda * t) /
    # reliability function
    exp(-1*lambda*t)
}





# Q5. Test d(t), f(t), r(t), and z(t) ###################################
# over a span of 150 days (1 to 3600 hours)
# and visualize each with hist()

d(t = 1:3600, lambda = 1/1200) %>% hist()

f(t = 1:3600, lambda = 1/1200) %>% hist()

r(t = 1:3600, lambda = 1/1200) %>% hist()

z(t = 1:3600, lambda = 1/1200) %>% hist()

# What do you notice?


# Clear environment ###################################
rm(list = ls())





# 2. Higher level Functions ###################################

# Sometimes, we make functions that USE functions inside them.
# Just make sure you either 
# (1) put function A before function B, or 
# (2) put function A INSIDE function B before using it


# We can re-write r(t) USING our function f(t)
f = function(t, lambda){ 1 - exp(-1*lambda*t) }

# Zero dependencies
r = function(t, lambda){   exp(-1*lambda*t) }
# I already defined f, so I can use it in my function
r = function(t, lambda){ 1 - f(t, lambda)}

remove(f,r)
r = function(t, lambda){ 1 - f(t, lambda)}
r(t = 2, lambda = 0.001)

r = function(t, lambda){ 1 - f(t, lambda)   }




# Or we can embed f(t) in r(t)
r = function(t, lambda){ 
  # Write f(t)
  f = function(t, lambda){ 1 - exp(-1*lambda*t) }
  
  # Then calculate and return r(t)
  1 - f(t, lambda)   
  
}


# We can use embedded functions to create super functions, like h(t) and afr(t)
