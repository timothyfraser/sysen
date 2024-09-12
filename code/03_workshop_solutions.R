# workshop_3_solutions.R
# Workshop 3: PDFs and CDFs in R
# Dr. Fraser


# Below, please find the following content for our recitation class from Friday.
library(dplyr) # data wrangling
library(ggplot2) # visuals
# install.packages("mosaicCalc")
library(mosaicCalc) # derivatives and integrals

# Exercise 1 #####################################################
# Class teaches Dr. Fraser to analyze PDFs and CDFs


### When the PDF is provided ###################################

# the function that produces the line, 
# or the probability for every x value

# probability density function --> probability distribution

d = function(x){  (x + 2*x)/1000  }

# What's the chance that we get a toaster that fails **at** 1 hour
d(x = 1)



# There is a 0.3% chance that we would get a value of 1
# from this particular distribution / density function.

# EXACTLY 1. --> probability densities
# More than or Less than 1 --> cumulative probabilities


# toaster - time (hours) to failure 
# How would I use this PDF for to find probability density of failure at 50 hours?
d(x = 50)



# Make our own `tibble` (an empowered data.frame from dplyr)
# How about for 0 to 1000 hours?

dat = tibble(
  hours = 0:50,
  prob = d(x = hours)
)


dat

# How might I plot that?

# thistle4
# tomato3
# darksalmon2
# slategray4
colors()

ggplot() +
  geom_point(data = dat, mapping = aes(x = hours, y = prob),
             color = "tomato2")

ggplot() +
  geom_line(data = dat, mapping = aes(x = hours, y = prob, group = "my line"), 
            color = "tomato2", linewidth = 2)

ggplot() +
  geom_area(data = dat, mapping = aes(x = hours, y = prob, group = "my line"), 
            color = "tomato2", fill = "darksalmon", alpha = 0.5, linewidth = 2)


# Oooh... can I save that plot?

gg = ggplot() +
  geom_area(data = dat, mapping = aes(x = hours, y = prob, group = "my line"), 
            color = "tomato2", fill = "darksalmon", alpha = 0.5, linewidth = 2)

ggsave(gg, filename = "code/03_workshop_image.png", 
       dpi = 200, width = 5, height = 10)



dat
d(x = 2)



# Exercise 2 ########################################################

### Simulated Distributions ###################################

# Archetypal Distributions, normal, poisson, exponential

# What are our 4 types of probability functions?
# use poisson as an example



# mean of 50 hours to failure
mu = 50





# How would I simulate 10 products with a mean time to failure of 50 hours?
# Assume poisson

# dpois() # PDF - densities
# ppois() # CDF - cumulative probabilities
# qpois() # quantiles 
# rpois() # random samples

toasters = rpois(n = 10, lambda = 50)
rpois(n = 10, lambda = mu)




# What's the histogram look like?

toasters %>% hist()


# How could I get the cumulative probability,
# from 1 to 100? Use a tibble.



dat = tibble(
  hours = 1:100,
  prob = ppois(hours, lambda = mu)
)


ggplot() + geom_point(data = dat, mapping = aes(x = hours, y = prob))



# Exercise 3 #################################################

# Empirical Hours to Failure for Some Toasters
obs = c(10,50, 20, 30, 40, 50, 30, 20, 90)


# Make an empirical probability density function
# install.packages("broom")
library(broom)
# known density function
d = function(x){  (x + 2*x)/1000  }
# observed density function
dobs = obs %>% density() %>% approxfun()

d(50)
dobs(50)

# Integrating the PDF to get the CDF
p = mosaicCalc::antiD(tilde = d(x) ~ x)
p(50)

# You can't integrate a density model function.
# pobs = mosaicCalc::antiD(tilde = dobs(x) ~ x)
obs

# empirical cumulative probability function for d()
pobs = mosaicCalc::antiD(tilde = d(x) ~ x)
pobs(x = c(1,2,3))

# Can't really easily do that for our approxfun()
dobs

rm(list = ls())


# Exercise 4 ########################################################

# The cost of a component varies depending on market conditions.
# Over the last year, analysts report is cost on average $50, 
# with a standard deviation of $5.
# Assume normal distribution - so dnorm, etc.

# Pick 2!

# Q1. What is the probability [density] the component will cost exactly $60?

# PDF
dnorm(x = 60, mean = 50, sd = 5)
dnorm(x = 60.5, mean = 50, sd = 5)

0:50 %>% dnorm(mean = 50, sd = 5)


# Q2. What is the probability the component costs less than $60?

# CDF
pnorm(60, mean = 50, sd = 5)


# Q3. What is the probability that the component costs more than $60?

1 - pnorm(60, mean = 50, sd = 5)


# Q4. What price is greater than 75% of all sales?

# quantiles
qnorm(0.75, mean = 50, sd = 5)



# Q5. What is the probability it costs between $45 and $55?

pnorm(45, mean = 50, sd = 5)

pnorm(55, mean = 50, sd = 5)

pnorm(55, mean = 50, sd = 5) - pnorm(45, mean = 50, sd = 5)


# Exercise 5 ################################

# Can we make a function to simplify the process 
# of making probability calculations of Between X1 and X2? (like above)
pslice = function(x1, x2, mean, sd){
  pnorm(x2, mean = mean, sd = sd) - pnorm(x1, mean = mean, sd = sd)
}
# It works!
pslice(x1 = 45, x2 = 55, mean=  50, sd = 5)

# Exercise 6 ############################################################

# dexp()
# pexp()
# qexp()
# rexp()

rate = 0.002
mu = 1 / rate
mu
# Our product has an a mean time to failure of 500 hours of use

# 1. Make a tibble of hours from 1 to 1000
# 2. Calculate the probability density
# 3. Calculate the cumulative probability
# 4. Plot one of them.


# Exercise 7 #############################################

# How do we get the CDF from an observed vector?

# Empirical Hours to Failure for Some Toasters
obs = c(10,50, 20, 30, 40, 50, 30, 20, 90)

# observed density function
dobs = obs %>% density() %>% approxfun()

# See the observed PDF
obs %>% density() %>% broom::tidy() %>% plot()

# Get the CDF from the observed PDF
pobs = obs %>% density() %>% broom::tidy() %>%
  dplyr::select(hours = x, prob = y) %>%
  mutate(cprob = cumsum(prob) / sum(prob) ) %>%
  dplyr::select(hours, cprob) %>%
  approxfun()

pobs(50)

# Let's write ourselves a function get_pobs()
# to help us get the CDF from an observed vector
get_pobs = function(obs){
  
  obs %>% density() %>% broom::tidy() %>%
    dplyr::select(hours = x, prob = y) %>%
    mutate(cprob = cumsum(prob) / sum(prob) ) %>%
    dplyr::select(hours, cprob) %>%
    approxfun()
  
}

pobs = obs %>% get_pobs()
pobs(50)

rm(list = ls())


