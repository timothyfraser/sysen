# workshop_4_solutions.R
# Dr. Fraser, Fall 2022

# In today's workshop, let's practice our many, many ways 
# of using failure functions to analyze system reliability! 

# See workshop_4_solutions.R for solutions (but only after class!)

###################################
# 0. Load Packages
###################################
library(tidyverse)
library(mosaicCalc)

###################################
# 1. Making Functions
###################################

# You learned to make Functions in Week 3. Let's practice!
# https://timothyfraser.github.io/sysen/skill_functions

# Nintendo is product testing its next Switch console.
# 1000 enthusiastic children received a console in the mail,
# played video games for days on end, and 
# parents called in when the console eventually broke.

# On average, 1 console failed every 1200 hours (50 days).

# So, we say the constant failure rate lambda was 1/1200 hours

# Using your notes from Lesson 4 and Workshop 4, let's write a few functions using lambda!


### Example Function l() (for lambda)
l = function(units, hours){ units / hours }
# Try it out
l(units = 1, hours = 1200)
# We can also, respecting the order of units and hours, write:
l(1, 1200)



# Note: In r, we write e^something as exp(something)

# Q1. Let's write our probability density function d(t)
d = function(t, lambda){  lambda * exp(-1*lambda*t) }


# Q2. Let's write our failure function f(t)
f = function(t, lambda){1 - exp(-1*lambda * t)}

# Q3. Let's write our reliability function r(t)
r = function(t, lambda){exp(-1 * lambda * t)}

# Q4. Let's write our failure rate z(t) (hazard rate)
z = function(t, lambda){
  # density function / aka change in failure function
  lambda * exp(-1 * lambda * t) /
    # reliability function
    exp(-1*lambda*t)
}


# Q5. Test d(t), f(t), r(t), and z(t)
# over a span of 150 days (1 to 3600 hours)
# and visualize each with hist()

d(t = 1:3600, lambda = 1/1200) %>% hist()

f(t = 1:3600, lambda = 1/1200) %>% hist()

r(t = 1:3600, lambda = 1/1200) %>% hist()

z(t = 1:3600, lambda = 1/1200) %>% hist()

# What do you notice?



###################################
# 2. Calculus in R
###################################

# You learned to use mosaicCalc in Week 3
# https://timothyfraser.github.io/sysen/workshop_3
# We can use D() to derive and antiD() to integrate.

# It's written like...

# If I have function f(x) = x^2 + 2*x
# We can get the derivative...
derivative <- D(x^2 + 2*x + z^5 ~ x)
# And use it as a function like this
derivative(x = c(1:5), z = 1)

# We can get the integral...
integral <- antiD(x^2 + 2*x + z^5 ~ x)
# And use it as a function like this.
integral(x = c(1:5), z = 1)



# Let's practice that a bit.


# Q6. Find the integral of d(). What does it equal?
fc = antiD(lambda*exp(-1*lambda*t) ~ t)
fc = antiD(d(t, lambda) ~ t)
fc(t = 1:3600, lambda = 1/1200) %>% hist()
# Compare with original
f(t = 1:3600, lambda = 1/1200) %>% hist()


# Q7. Find the derivative of f()
dc = D(1 - exp(-1*lambda*t) ~ t)
dc = D(f(t, lambda) ~ t)
dc(t = 1:3600, lambda = 1/1200) %>% hist()
# Compare with original
d(t = 1:3600, lambda = 1/1200) %>% hist()


# Q8. Find the negative derivative of r()
dc = D(-1*r(t, lambda) ~ t)
dc(1:3600, lambda = 1/1200) %>% hist()
d(1:3600, lambda = 1/1200) %>% hist()


# Q9. Find 1 - the integral of d()
rc = antiD(d(t, lambda) ~ t)
(1 - rc(1:3600, lambda = 1/1200)) %>% hist()
r(1:3600, lambda = 1/1200) %>% hist()



####################################
# 3. Higher level Functions
####################################

# Sometimes, we make functions that USE functions inside them.
# Just make sure you either 
# (1) put function A before function B, or 
# (2) put function A INSIDE function B before using it


# We can re-write r(t) USING our function f(t)
f = function(t, lambda){ 1 - exp(-1*lambda*t) }
r = function(t, lambda){ 1 - f(t, lambda)   }

# Or we can embed f(t) in r(t)
r = function(t, lambda){ 
  # Write f(t)
  f = function(t, lambda){ 1 - exp(-1*lambda*t) }
  # Then calculate and return r(t)
  1 - f(t, lambda)   
}


# We can use embedded functions to create super functions, like h(t) and afr(t)

# Using Table 1 in Workshop 4, (https://timothyfraser.github.io/sysen/workshop_4)
# build each of the following functions below!


# Q10. Accumulative hazard rate
h = function(t, lambda){  -log(r(t, lambda)) }
h(t = 1:10, lambda = 1/1200)

# or
h = function(t, lambda){ lambda*t}
h(t = 1:10, lambda = 1/1200)


# Q11. Average Failure Rate
# Hint: your function will need t1, t2, and lambda
afr = function(t1, t2, lambda){ 
  ( h(t2, lambda) - h(t1, lambda) ) / ( t2 - t1 )
}

afr = function(t1, t2, lambda){
  (  -log(r(t2, lambda)) - - log(r(t1, lambda))  ) / (t2 - t1)
}


# Q12. Change in Failure Function 
# You'll need a t, x, and lambda (x is sometimes written deltat)
deltaf = function(t, x, lambda){
  (  f(t + x, lambda) - f(t, lambda)  ) / x
}
deltaf(t = 1, x = 1, lambda = 1/1200)

# Cool trick: if x = 1, it reduces to the density function.
d = function(t, lambda){ 1 - exp(-1*lambda*t) }
d(t = 1, lambda = 1/1200)


####################################
# Challenge Questions:
####################################

# Q13. Calculate the overall probability that Nintendo's entire console DOESN'T fail after 1 hour

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


# Q14. Design a function to test console reliability for any time t.
# Test reliability after 1 hour, 24 hours, and 168 hours (7 days)
nintendo = function(t){
  r(t, lambda = cord) * 
    r(t, lambda = joystick)^2 * 
    r(t, lambda = screen)
}

c(1, 24, 168) %>% nintendo()



# Q15. Use your function to visualize the reliability curve 
# for this overall system in ggplot, as it ranges from 1 to 1000 hours!

# Let's make a data.frame 's' for system  
s <- data.frame(t = 1:3000) %>%
  mutate(p_n = nintendo(t),
         p_j = r(t, lambda = joystick),
         p_c = r(t, lambda = cord),
         p_s = r(t, lambda = screen))

ggplot() +
  geom_area(data = s, mapping = aes(x = t, y = p_c, fill = "Cord"), alpha = 0.75) +
  geom_area(data = s, mapping = aes(x = t, y = p_s, fill = "Screen"), alpha = 0.75) +
  geom_area(data = s, mapping = aes(x = t, y = p_j, fill = "Joystick"), alpha = 0.75) +
  geom_area(data = s, mapping = aes(x = t, y = p_n, fill = "Overall"), alpha = 0.75) 


# Q16. Nintendo's joystick contains several parts, each with a unique probability of reliability.
# See the diagram saved in workshop_4_diagram.png
# Calculate the overall probability of the wiring units W1-W4

# Each wiring unit W1-W4 gets the reliability rate 'rw'
rw = 0.93

# You can calculate it like this...
rwall = 1 - (1 - rw)*(1 - rw)*(1 - rw)*(1 - rw)
# Or...
rwall = 1 - (1 - rw)^4

# Q17: Calculate the overall probability of the overall system

ra = 0.99
rb = 0.95
rc = 0.90

# We multiply the entire series' components' reliability together
ra*rb*rwall*rc





