# 09_recitation.py
# Tim Fraser
# Recitation 9: Fault Tree Analysis
# Chapter: Fault Tree Analysis in Python

# It mirrors 09_recitation.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.

import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr + readr in R)
from plotnine import *         # visuals (ggplot2 in R)
import sys
# Load our R-style distribution helpers: pexp(), rbinom(), rnorm(), qnorm()
sys.path.append("functions")
from functions_distributions import pexp, rbinom, rnorm, qnorm

# PART 1: Using Raw Probabilities #################################
def f1(m, c, d, k):
  top = m + c * d * k
  return top

# For example... given these probabilities, the chance Superman turns evil is highly contigent on event m - the success of superman movies at the box office.
probs1 = f1(m = 0.50, c = 0.99, d = 0.25, k = 0.01)
# view it!
print(probs1)


# PART 2: Using Failure Rates at Time t ############################

# But if we knew the failure rate of each event,
# we could calculate the probability of the top event at any time t!

def f2(t, lambda_m, lambda_c, lambda_d, lambda_k):
  # Get probability at time t...
  prob_m = pexp(t, rate = lambda_m)
  prob_c = pexp(t, rate = lambda_c)
  prob_d = pexp(t, rate = lambda_d)
  prob_k = pexp(t, rate = lambda_k)
  # Use boolean equation to calculate top event
  prob_top = prob_m + (prob_c * prob_d * prob_k)
  return prob_top

# Then we could simulate the probability of the top event over time!
probs2 = pd.DataFrame({'t': np.arange(1, 101)})
probs2['prob'] = f2(t = probs2['t'], lambda_m = 0.01, lambda_c = 0.001,
                    lambda_d = 0.025, lambda_k = 0.00005)
# Check out the first few rows!
print(probs2.head(3))


# PART 3: Simulating Uncertainty in Probabilities ###################
probs3 = pd.DataFrame({
  'n': 1000,
  'prob_m': rbinom(n = 1000, size = 1, prob = 0.50),
  'prob_c': rbinom(n = 1000, size = 1, prob = 0.99),
  'prob_d': rbinom(n = 1000, size = 1, prob = 0.25),
  'prob_k': rbinom(n = 1000, size = 1, prob = 0.01)
})
# Calculate probability of top event for each simulation
probs3['prob_top'] = f1(m = probs3['prob_m'], c = probs3['prob_c'],
                        d = probs3['prob_d'], k = probs3['prob_k'])
# Let's get some descriptive statistics -
# the average will be particularly informative
print(pd.DataFrame({
  'mu_top': [probs3['prob_top'].mean()],
  'sigma_top': [probs3['prob_top'].std()]}))



# PART 4: Simulating Uncertainty in Failure Rates ##############################
# Suppose each failure rate has a specific standard error:
# for m, 0.0001; for c, 0.00001, for d and k, 0.000002.


def f4(t, lambda_m, lambda_c, lambda_d, lambda_k):
  sim_lambda_m = rnorm(n = 1, mean = lambda_m, sd = 0.0001)
  sim_lambda_c = rnorm(n = 1, mean = lambda_c, sd = 0.00001)
  sim_lambda_d = rnorm(n = 1, mean = lambda_d, sd = 0.000002)
  sim_lambda_k = rnorm(n = 1, mean = lambda_k, sd = 0.000002)

  # Get probability at time t...
  sim_prob_m = pexp(t, rate = sim_lambda_m)
  sim_prob_c = pexp(t, rate = sim_lambda_c)
  sim_prob_d = pexp(t, rate = sim_lambda_d)
  sim_prob_k = pexp(t, rate = sim_lambda_k)
  # Use boolean equation to calculate top event
  prob_top = sim_prob_m + (sim_prob_c * sim_prob_d * sim_prob_k)
  return prob_top

# Then we could simulate the probability of the top event over time,
probs4 = pd.DataFrame({'t': np.arange(1, 101)})
# This would give us 1 random simulation per time period
probs4['prob'] = f4(t = probs4['t'], lambda_m = 0.01, lambda_c = 0.001,
                    lambda_d = 0.025, lambda_k = 0.00005)


# But we really probably want MANY random simulations per time period.
# In R, reframe() returns MANY rows per group; in Python we build one
# 100-row frame per replicate and stack them with pd.concat().
probs5 = pd.concat([
  pd.DataFrame({
    'reps': r,
    't': np.arange(1, 101),
    'prob': f4(t = np.arange(1, 101), lambda_m = 0.01, lambda_c = 0.001,
               lambda_d = 0.025, lambda_k = 0.00005)})
  for r in range(1, 1001)], ignore_index = True)

print(probs5.head(3))


# And then we could get quantities of interest for each time period!
probs6 = (probs5
  .groupby('t')['prob']
  .agg(
    mu = 'mean',
    sigma = 'std',
    # Exact lower and upper 95% simulated confidence intervals
    lower = lambda x: x.quantile(0.025),
    upper = lambda x: x.quantile(0.975))
  .reset_index())
# Approximated lower and upper 95% confidence intervals
probs6['lower_approx'] = probs6['mu'] - qnorm(0.025) * probs6['sigma']
probs6['upper_approx'] = probs6['mu'] + qnorm(0.975) * probs6['sigma']

print(probs6.head(3))
