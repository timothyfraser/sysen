# 09_recitation_solutions.py
# Tim Fraser
# Recitation 9: Fault Tree Analysis (worked solutions)
# Chapter: Fault Tree Analysis in Python

# Workshop code paired with the textbook chapter
# "Fault Tree Analysis in Python" at timothyfraser.com/sigma.
# It mirrors 09_recitation_solutions.R section by section.

# What this script does:
# We build a fault tree by hand, as a function f() that turns the failure
# probabilities of five components (b, s, h, o, n) into the probability of
# the TOP EVENT. Then we make that function progressively more realistic:
#   fixed probabilities -> probabilities that grow over time from failure
#   rates (lambdas) -> lambdas that are themselves uncertain and simulated.

# Inputs: none. Every number is typed into the script; no data files are read.
# Packages: numpy, pandas, plotnine (plus our functions_distributions helpers)

import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr in R)
from plotnine import *         # visuals (ggplot2 in R)
import sys
# Load our R-style distribution helpers: pexp() and rnorm() work just like in R
sys.path.append("functions")
from functions_distributions import pexp, rnorm

# 1. A top event function ######################################

# Probability of top event
def f(b, s, h, o, n):
  return b + s + h + o * n

print(f(b = 1, s = 0, h = 1, o = 0, n = 0))


def f(b, s, h, o, n):
  top = b + s + h + o * n
  # if_else(top > 1, 1, top) in R; np.where() in Python
  top = np.where(top > 1, 1, top)
  return top

print(f(b = 1, s = 0, h = 1, o = 0, n = 0))

# Using probabilities
print(f(b = 0.0005, s = 0, h = 0.5, o = 0, n = 0))


# 2. One set of component probabilities ########################

# Put the five component probabilities in a data frame and let f() compute
# the top event probability t for that one combination.
one = pd.DataFrame({
  'b': [0.000000000005],
  's': [0.00001],
  'h': [0.02],
  'o': [0.10],
  'n': [0.00001]
})
one['t'] = f(one['b'], one['s'], one['h'], one['o'], one['n'])
print(one)


# 3. Sweeping one component across a range #####################

# Hold b, s, h, o fixed and let n vary from 0 to 1, so we can see how
# sensitive the top event is to that one component.
probs = pd.DataFrame({'n': np.round(np.arange(0, 1.001, 0.01), 2)})
probs['b'] = 0.000000005
probs['s'] = 0.00001
probs['h'] = 0.02
probs['o'] = 0.10
probs['t'] = f(probs['b'], probs['s'], probs['h'], probs['o'], probs['n'])

# R's base plot() of two columns is a scatterplot
(ggplot(probs, aes(x = 'n', y = 't'))
  + geom_point())


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

def f(b, s, h, o, n):
  top = b + s + h + o * n
  top = np.where(top > 1, 1, top)
  return top










# 5. Probabilities that grow over time #########################

# Each component has a failure rate (lambda). pexp(t, rate = lambda) turns
# a rate into the probability that the component has failed by time t.
mylambdas = pd.DataFrame({
  't': np.arange(0, 6),
  'b_lambda': 0.0000001,
  's_lambda': 0.002,
  'h_lambda': 0.00001,
  'o_lambda': 0.001,
  'n_lambda': 0.00001
})

myprobs = mylambdas.assign(
  b = lambda d: pexp(d['t'], rate = d['b_lambda']),
  s = lambda d: pexp(d['t'], rate = d['s_lambda']),
  h = lambda d: pexp(d['t'], rate = d['h_lambda']),
  o = lambda d: pexp(d['t'], rate = d['o_lambda']),
  n = lambda d: pexp(d['t'], rate = d['n_lambda']))
myprobs['top'] = f(myprobs['b'], myprobs['s'], myprobs['h'], myprobs['o'], myprobs['n'])

myprobs.info()

(ggplot()
  + geom_line(data = myprobs, mapping = aes(x = 't', y = 'top')))


myprobs.info()


# 6. Uncertain lambdas: simulate them ##########################

# What if lambdas vary?

mylambdas = pd.DataFrame({
  'n': 1000,
  'b_lambda': rnorm(n = 1000, mean = 0.0000001, sd = 0.00000001),
  's_lambda': rnorm(n = 1000, mean = 0.002, sd = 0.00001),
  'h_lambda': rnorm(n = 1000, mean = 0.00001, sd = 0.00000001),
  'o_lambda': rnorm(n = 1000, mean = 0.001, sd = 0.00001),
  'n_lambda': rnorm(n = 1000, mean = 0.00001, sd = 0.00000002)
})


# Cross every simulated set of lambdas with every time point t, compute
# each component's failure probability at t, then the top event.
# (group_by(t) %>% reframe(mylambdas) in R is a cross join in pandas.)
sim1 = (pd.DataFrame({'t': np.arange(1, 11)})
  .merge(mylambdas, how = 'cross')
  .assign(
    b = lambda d: pexp(d['t'], rate = d['b_lambda']),
    s = lambda d: pexp(d['t'], rate = d['s_lambda']),
    h = lambda d: pexp(d['t'], rate = d['h_lambda']),
    o = lambda d: pexp(d['t'], rate = d['o_lambda']),
    n = lambda d: pexp(d['t'], rate = d['n_lambda'])))
sim1['top'] = f(sim1['b'], sim1['s'], sim1['h'], sim1['o'], sim1['n'])

# Summarize the 1000 simulations at each time t into a median and a
# 95% simulated confidence interval.
qi1 = (sim1
  .groupby('t')['top']
  .agg(lower = lambda x: x.quantile(0.025),
       median = lambda x: x.quantile(0.50),
       upper = lambda x: x.quantile(0.975))
  .reset_index())

print(qi1)


# Solutions #################################

# Goal:

# 1. Write a function
# 2. Make up lambdas
# 3. For some time t, calculate probability of top event

def f(b, s, h, o, n):
  top = b + s + h + o * n
  top = np.where(top > 1, 1, top)
  return top

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

print(f(b = prob_b, s = prob_s, h = prob_h, o = prob_o, n = prob_n))
