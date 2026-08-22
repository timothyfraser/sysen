# 09_recitation_solutions.R
# Tim Fraser
# Recitation 9: Fault Tree Analysis (worked solutions)
# Chapter: Fault Tree Analysis in R

# Workshop code paired with the textbook chapter
# "Fault Tree Analysis in R" at timothyfraser.com/sigma.

# What this script does:
# We build a fault tree by hand, as a function f() that turns the failure
# probabilities of five components (b, s, h, o, n) into the probability of
# the TOP EVENT. Then we make that function progressively more realistic:
#   fixed probabilities -> probabilities that grow over time from failure
#   rates (lambdas) -> lambdas that are themselves uncertain and simulated.

# Inputs: none. Every number is typed into the script; no data files are read.
# Packages: dplyr, ggplot2

library(dplyr)
library(ggplot2)

# 1. A top event function ######################################

# Probability of top event
f = function(b, s, h, o, n){ b + s + h + o * n }

f(b = 1, s = 0, h = 1, o = 0, n = 0)


f = function(b, s, h, o, n){ 
  top = b + s + h + o * n 
  top = if_else(top > 1, true = 1, false = top)
  return(top)
}

f(b = 1, s = 0, h = 1, o = 0, n = 0)

# Using probabilities
f(b = 0.0005, s = 0, h = 0.5, o = 0, n = 0)


# 2. One set of component probabilities ########################

# Put the five component probabilities in a tibble and let f() compute
# the top event probability t for that one combination.
tibble(
  b = 0.000000000005,
  s = 0.00001,
  h = 0.02,
  o = 0.10,
  n = 0.00001,
  
  t = f(b,s,h,o,n)
)


# 3. Sweeping one component across a range #####################

# Hold b, s, h, o fixed and let n vary from 0 to 1, so we can see how
# sensitive the top event is to that one component.
probs = tibble(
  b = 0.000000005,
  s = 0.00001,
  h = 0.02,
  o = 0.10,
  n = seq(from = 0, to = 1, by = 0.01),
  
  t = f(b,s,h,o,n)
)

probs %>%
  select(n, t) %>%
  plot()


# 4. Where do these probabilities come from? ###################

# Probabilities are uncertain ---> simulate from binomial
# Probabilities vary over time ---> calculate probability at time t
# Probabilities depend on Distributions ---> use exponential
# Distributions depend on parameters ---> calculate probability at time t given lambda
# Parameters are uncertain --> simulate lambda from normal

# Goal:

# 1. Write a function
# 2. Make up lambdas
# 3. For some time t, calculate probability of top event

f = function(b, s, h, o, n){
  top = b + s + h + o * n 
  top = if_else(top > 1, true = 1, false = top)
  return(top)
}










# 5. Probabilities that grow over time #########################

# Each component has a failure rate (lambda). pexp(t, rate = lambda) turns
# a rate into the probability that the component has failed by time t.
mylambdas = tibble(
  t = 0:5,
  b_lambda = 0.0000001,
  s_lambda = 0.002,
  h_lambda = 0.00001,
  o_lambda = 0.001,
  n_lambda = 0.00001
)

myprobs = mylambdas %>%
  mutate(b = pexp(t, rate = b_lambda),
         s = pexp(t, rate = s_lambda),
         h = pexp(t, rate = h_lambda),
         o = pexp(t, rate = o_lambda),
         n = pexp(t, rate = n_lambda)) %>%
  mutate(top = f(b,s,h,o,n))

myprobs %>%
  glimpse()

ggplot() +
  geom_line(data = myprobs, mapping = aes(x = t, y = top))


myprobs %>%
  glimpse()


# 6. Uncertain lambdas: simulate them ##########################

# What if lambdas vary?


mylambdas = tibble(
  n = 1000,
  b_lambda = rnorm(n = n, mean = 0.0000001, sd = 0.00000001),
  s_lambda = rnorm(n = n, mean = 0.002, sd = 0.00001),
  h_lambda = rnorm(n = n, mean = 0.00001, sd = 0.00000001),
  o_lambda = rnorm(n = n, mean = 0.001, sd = 0.00001),
  n_lambda = rnorm(n = n, mean = 0.00001, sd = 0.00000002)
)


# Cross every simulated set of lambdas with every time point t, compute
# each component's failure probability at t, then the top event.
sim1 = tibble(t = 1:10) %>%
  group_by(t) %>%
  reframe(mylambdas) %>%
  mutate(b = pexp(t, rate = b_lambda),
         s = pexp(t, rate = s_lambda),
         h = pexp(t, rate = h_lambda),
         o = pexp(t, rate = o_lambda),
         n = pexp(t, rate = n_lambda))  %>%
  mutate(top = f(b,s,h,o,n))

qi1 = sim1 %>%
# Summarize the 1000 simulations at each time t into a median and a
# 95% simulated confidence interval.
  group_by(t) %>%
  summarize(lower = quantile(top, prob = 0.025),
            median = quantile(top, prob = 0.50),
            upper = quantile(top, prob = 0.975))

qi1


# Solutions #################################

# Goal:

# 1. Write a function
# 2. Make up lambdas
# 3. For some time t, calculate probability of top event

f = function(b, s, h, o, n){
  top = b + s + h + o * n 
  top = if_else(top > 1, true = 1, false = top)
  return(top)
}

lambda_b = 0.00001
lambda_s = 0.00002
lambda_h = 0.0003
lambda_o = 0.004
lambda_n = 0.00001

t = 10

prob_b = pexp(t, rate = lambda_b)
prob_s = pexp(t, rate = lambda_s)
prob_h = pexp(t, rate = lambda_h)
prob_o = pexp(t, rate = lambda_o)
prob_n = pexp(t, rate = lambda_n)

f(b = prob_b, prob_s, prob_h, prob_o, prob_n)


