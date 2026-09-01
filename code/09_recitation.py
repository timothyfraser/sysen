# 09_recitation.py
# Tim Fraser
# Recitation 9: Fault Tree Analysis
# Chapter: Fault Tree Analysis in Python

import pandas as pd
import numpy as np
from scipy.stats import expon, norm
from plotnine import *

# PART 1: Using Raw Probabilities #################################
def f1(m, c, d, k):
    top = m + c * d * k
    return top
# For example... given these probabilities, the chance Superman turns evil is highly contingent on event m - the success of superman movies at the box office.
probs1 = f1(m=0.50, c=0.99, d=0.25, k=0.01)
# view it!
probs1


# PART 2: Using Failure Rates at Time t ############################

# But if we knew the failure rate of each event,
# we could calculate the probability of the top event at any time t!


def f2(t, lambda_m, lambda_c, lambda_d, lambda_k):
    # Get probability at time t...
    # scipy expon uses scale = 1/rate  (R pexp uses rate=)
    t = np.asarray(t)
    prob_m = expon.cdf(t, scale=1 / lambda_m)
    prob_c = expon.cdf(t, scale=1 / lambda_c)
    prob_d = expon.cdf(t, scale=1 / lambda_d)
    prob_k = expon.cdf(t, scale=1 / lambda_k)
    # Use boolean equation to calculate top event
    prob_top = prob_m + (prob_c * prob_d * prob_k)
    return prob_top

# Then we could simulate the probability of the top event over time!
probs2 = pd.DataFrame({'t': range(1, 101)})
probs2 = probs2.assign(prob=lambda df: f2(t=df['t'], lambda_m=0.01, lambda_c=0.001,
                                          lambda_d=0.025, lambda_k=0.00005))
# Check out the first few rows!
probs2.head(3)


# PART 3: Simulating Uncertainty in Probabilities ###################
n = 1000
probs3 = pd.DataFrame({
    'n': n,
    'prob_m': np.random.binomial(n=1, p=0.50, size=n),
    'prob_c': np.random.binomial(n=1, p=0.99, size=n),
    'prob_d': np.random.binomial(n=1, p=0.25, size=n),
    'prob_k': np.random.binomial(n=1, p=0.01, size=n)
})
probs3['prob_top'] = f1(m=probs3['prob_m'], c=probs3['prob_c'],
                        d=probs3['prob_d'], k=probs3['prob_k'])
# Let's get some descriptive statistics -
# the average will be particularly informative
pd.DataFrame({
    'mu_top': [probs3['prob_top'].mean()],
    'sigma_top': [probs3['prob_top'].std()]
})



# PART 4: Simulating Uncertainty in Failure Rates ##############################
# Suppose each failure rate has a specific standard error:
# for m, 0.0001; for c, 0.00001, for d and k, 0.000002.


def f4(t, lambda_m, lambda_c, lambda_d, lambda_k):
    sim_lambda_m = np.random.normal(loc=lambda_m, scale=0.0001)
    sim_lambda_c = np.random.normal(loc=lambda_c, scale=0.00001)
    sim_lambda_d = np.random.normal(loc=lambda_d, scale=0.000002)
    sim_lambda_k = np.random.normal(loc=lambda_k, scale=0.000002)

    t = np.asarray(t)
    # Get probability at time t...
    sim_prob_m = expon.cdf(t, scale=1 / max(sim_lambda_m, 1e-12))
    sim_prob_c = expon.cdf(t, scale=1 / max(sim_lambda_c, 1e-12))
    sim_prob_d = expon.cdf(t, scale=1 / max(sim_lambda_d, 1e-12))
    sim_prob_k = expon.cdf(t, scale=1 / max(sim_lambda_k, 1e-12))
    # Use boolean equation to calculate top event
    prob_top = sim_prob_m + (sim_prob_c * sim_prob_d * sim_prob_k)
    return prob_top

# Then we could simulate the probability of the top event over time,
probs4 = pd.DataFrame({'t': range(1, 101)})
probs4 = probs4.assign(prob=lambda df: f4(t=df['t'], lambda_m=0.01, lambda_c=0.001,
                                          lambda_d=0.025, lambda_k=0.00005))


# But we really probably want MANY random simulations per time period.
rows = []
for reps in range(1, 1001):
    t = np.arange(1, 101)
    rows.append(pd.DataFrame({
        'reps': reps,
        't': t,
        'prob': f4(t=t, lambda_m=0.01, lambda_c=0.001,
                   lambda_d=0.025, lambda_k=0.00005)
    }))
probs5 = pd.concat(rows, ignore_index=True)

probs5.head(3)


# And then we could get quantities of interest for each time period!
probs6 = (probs5.groupby('t')
          .agg(mu=('prob', 'mean'),
               sigma=('prob', 'std'),
               lower=('prob', lambda s: s.quantile(0.025)),
               upper=('prob', lambda s: s.quantile(0.975)))
          .reset_index())
probs6['lower_approx'] = probs6['mu'] - norm.ppf(0.025) * probs6['sigma']
probs6['upper_approx'] = probs6['mu'] + norm.ppf(0.975) * probs6['sigma']

probs6.head(3)
