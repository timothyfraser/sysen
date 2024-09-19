# 00_demo.R

# Packages ###################################

#install.packages(c("dplyr", "readr", "ggplot2", "broom"))
library(dplyr)
library(readr)
library(ggplot2)
library(broom)


# Base R ###################################

c(1,2,34,4,5)

# spreadsheets!
data.frame(x = c(1,2,3), name = c("Tim", "Briana", "Kunj"))

dat = data.frame(
  x = c(1,2,3), 
  name = c("Tim", "Briana", "Kunj"))

dat

dat$x + 2

dat$x = dat$x + 2

dat

dat$y = 3
dat

dat$y = c(1,2,3)

dat


# dplyr operations ###################################
dat = data.frame(
  x = c(1,2,3), 
  name = c("Tim", "Briana", "Kunj"))

# pipeline (ctrl shift m)
# %>% 
# links inputs to functions
dat %>%
  select(name)

dat %>%
  select(., name)

select(dat, name)


dat %>%
  select(x) %>%
  mutate(y = c(53,44,33))

dat$x %>% mean()
mean(dat$x)


dat2 = dat %>%
  select(x) %>%
  mutate(y = c(53,44,33))

# Take a data.frame and shrink it into 1 row
dat2 %>%
  summarize(mu = mean(x), mu_y = mean(y))

dat2 %>%
  summarize(
    mu = mean(x), 
    mu_y = mean(y)
  )


dat2 %>%
  summarize(
    mu = mean(x), 
    sd = sd(x),
    count = length(x),
    median = median(x),
    min = quantile(x, prob = 0.00),
    max = quantile(x, prob = 1.00),
    q75 = quantile(x, prob = 0.75)
  )

# Stack two data.frames on top of each other.
superdat = bind_rows(dat, dat2)
superdat

# reorder columns?
superdat %>% 
  select(name, x, y)
# Overwrite data.frame
superdat = superdat %>% 
  select(name, x, y)

superdat # view it


# Probability Functions ########################

# probability + iteration

# 4 types of probability functions ('normal' example)
# rnorm
# dnorm
# pnorm
# qexp

# take a random sample from a normal distribution
x = rnorm(n = 1000, mean = 0, sd = 1)
hist(x)

# histograms stack frequeny of values in a vector
# distributions appproximate shape of histogram as a line
# distribution = PDF (probability density function)

# Approximate 
x %>% density()
# Want to see it?
x %>% density() %>% plot()

# This is the density function as a line
x %>% density() %>% broom::tidy()


# Turn this data.frame of densities into a function...
dobs = x %>% density() %>% broom::tidy() %>% approxfun()
# What's the probability density when x = 0?
dobs(0)

# dobs is an observed probability density function.
# we made it because we had a vector of data.

# Instead... we often need 'hypothetical distributions'
# normal *****
# poisson
# gamma 
# exponential *****
# weibull
# lognormal
# uniform
# binomial

# If we know the traits of our data (parameters)
mu = mean(x)
sigma = sd(x)

c(mu, sigma)

# Make me a normal distribution
# whose sample size is 1000
# whose mean is the mean of our observed data
# whose std is the std of our observed data
rnorm(n = 1000, mean = mu, sd = sigma) %>% hist()
# equivalent
rnorm(1000, mu, sigma) %>% hist()

# like dobs() density
# what's the probability density when x = 0
# if normal distribution with these traits
dnorm(0, mean = mu, sd = sigma)

# alternatively,
# what's the probability density when x = 0
# if exponential distribution with this trait
dexp(0, rate = 1 / mu)


# dplyr function called tibble()

mu = 1500

# smart data.frame
dat = tibble(
  # as product lifespan goes from t = 0 to 1000 hours
  t = 0:2000,
  # What is the probability density
  dprob = dexp(t, rate = 1/ mu)
)

ggplot() +
  geom_area(data = dat, mapping = aes(x = t, y = dprob))

# With a data.frame
data.frame(t = 0:2000) %>%
  mutate(dprob = dexp(t, rate = 1 /mu))



dat = tibble(
  # as product lifespan goes from t = 0 to 1000 hours
  t = 0:5000,
  # What is the probability density at time t
  dprob = dexp(t, rate = 1/ mu),
  # What is the cumulative probability at time t
  cprob = pexp(t, rate = 1 / mu)
)

ggplot() +
  geom_line(data = dat, mapping = aes(x = t, y = dprob))

ggplot() +
  geom_line(data = dat, mapping = aes(x = t, y = cprob))

# Looks like 75% of products fail by t = 2000 hours of use.
# d / p





dat = tibble(
  t = 0:5000,
  # calculate cumulative probability
  cprob = pexp(t, rate = 1 / mu),
  # qexp = quantile function
  # It translates percentiles/cumulative probabilities 
  # back into x axis values
  q = qexp(cprob, rate = 1 / mu)
)

dat


# rexp
# dexp
# pexp
# qexp

# Suppose we have 300 phones
# How many phones do we expect would fail after time t?
dat %>%
  mutate(prob2 = cprob * 300)

