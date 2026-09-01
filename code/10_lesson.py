# 10_lesson.py
# Tim Fraser
# Lesson 10: Physical Acceleration Models
# Chapter: Physical Acceleration Models in Python
# In this lesson, let's learn Weibull Acceleration modeling
# and MLE for acceleration modeling!

# Packages
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_models import lm


# LINEAR REGRESSION FOR WEIBULL ACCELERATION MODELING ##############################


# Let's make a data.frame matching Example 1 from the lesson slides
data = pd.DataFrame({
    't': [24, 72, 168, 300, 500, 750, 1000, 1250, 1500],
    'r85': [1, 0, 0, 1, 0, 3, 0, 1, 2],
    'r105': [2, 1, 3, 2, 2, 4, 5, 1, 4],
    'r125': [5, 10, 13, 2, 3, 2, 2, 1, 0]
})
n = 40

# Calculate probability of failure at time t under 85 degrees
data = data.assign(f85=lambda df: df['r85'].cumsum() / n)
# Convert to this formula
data = data.assign(y85=lambda df: np.log(-np.log(1 - df['f85'])))
data = data.assign(log_t=lambda df: np.log(df['t']))

m = lm(formula='y85 ~ log_t', data=data)

intercept = m.params['Intercept']
slope = m.params['log_t']

# These are our estimates for m and c at stress level 85
pd.DataFrame({'mhat': [slope], 'chat': [np.exp(-intercept / slope)]})


# What!!!?

# Let's streamline this.

# @param t [numeric] vector of times to failure. Same length as vector r.
# @param r [integer] failures at time t. Same length as vector t.
# @param n [integer] number of total units under test. Length 1.
def graphical_estimates(t, r, n=40):

    # Make data.frame
    df = pd.DataFrame({'t': t, 'r': r, 'n': n})

    # Calculate probability of failure
    df = df.assign(f=lambda d: d['r'].cumsum() / n)

    # Calculate transformation variable y
    df = df.assign(y=lambda d: np.log(-np.log(1 - d['f'])))
    df = df.assign(log_t=lambda d: np.log(d['t']))

    # Get model m
    m = lm(formula='y ~ log_t', data=df)

    # Get coefficients
    intercept = m.params['Intercept']
    slope = m.params['log_t']

    # Calculate estimates for m and c
    output = pd.DataFrame({'mhat': [slope], 'chat': [np.exp(-intercept / slope)]})

    return output

# Let's try it!
graphical_estimates(t=data['t'], r=data['r85'], n=40)

# Get parameters at different levels of stress
p85 = graphical_estimates(t=data['t'], r=data['r85'], n=40)
p105 = graphical_estimates(t=data['t'], r=data['r105'], n=40)
p125 = graphical_estimates(t=data['t'], r=data['r125'], n=40)

# We know c_u = AF x c_s,
# so AF = c_s / c_u

# AF from 85 to 105 degrees
p85['chat'].iloc[0] / p105['chat'].iloc[0]
# AF from 105 to 125 degrees
p105['chat'].iloc[0] / p125['chat'].iloc[0]
# AF from 85 to 125 degrees
p85['chat'].iloc[0] / p125['chat'].iloc[0]


# 85 C cell   m-hat = 0.57  c-hat 40222  Acceleration to 105 C = 18.2
# 105 C cell   m-hat = 0.70  c-hat 2208  Acceleration to 105 C = 9.1
# 125 C cell   m-hat = 0.71  c-hat 242  Acceleration to 105 C = 166.2




# MLE WITH FIXED M FOR WEIBULL ACCELERATION MODELING #####################


# Let's make a data.frame matching Example 1 from the lesson slides
data = pd.DataFrame({
    't': [24, 72, 168, 300, 500, 750, 1000, 1250, 1500],
    'r85': [1, 0, 0, 1, 0, 3, 0, 1, 2],
    'r105': [2, 1, 3, 2, 2, 4, 5, 1, 4],
    'r125': [5, 10, 13, 2, 3, 2, 2, 1, 0]
})
n85 = 40
n105 = 40
n125 = 40


# Let's write ourselves a speedy weibull density function 'd()'
def d(t, m, c):
    t = np.asarray(t, dtype=float)
    return (m / t) * (t / c)**m * np.exp(-1 * (t / c)**m)

def r(t, m, c):
    t = np.asarray(t, dtype=float)
    return np.exp(-(t / c)**m)

# Let's write our crosstable's likelihood function
# R uses optim(..., control=list(fnscale=-1)) to maximize.
# Python minimize()s the negative log-likelihood.
def ll(par, t, x1, x2, x3, n1, n2, n3):
    r1 = np.sum(x1)
    r2 = np.sum(x2)
    r3 = np.sum(x3)
    tmax = np.max(t)

    prob_d1 = (np.log(d(t, c=par[0], m=par[3])) * x1).sum()
    prob_d2 = (np.log(d(t, c=par[1], m=par[3])) * x2).sum()
    prob_d3 = (np.log(d(t, c=par[2], m=par[3])) * x3).sum()

    prob_r1 = np.log(r(t=tmax, c=par[0], m=par[3]) ** (n1 - r1))
    prob_r2 = np.log(r(t=tmax, c=par[1], m=par[3]) ** (n2 - r2))
    prob_r3 = np.log(r(t=tmax, c=par[2], m=par[3]) ** (n3 - r3))

    return prob_d1 + prob_r1 + prob_d2 + prob_r2 + prob_d3 + prob_r3


def neg_ll(par, t, x1, x2, x3, n1, n2, n3):
    return -ll(par, t, x1, x2, x3, n1, n2, n3)

# And let's run MLE!
mle = minimize(
    fun=neg_ll,
    x0=[1000, 1000, 1000, 1],
    args=(data['t'].values, data['r85'].values, data['r105'].values,
          data['r125'].values, n85, n105, n125),
    method='Nelder-Mead'
)


# Extract parameters into a dataframe
p = pd.DataFrame({
    'c85': [mle.x[0]],
    'c105': [mle.x[1]],
    'c125': [mle.x[2]],
    'm': [mle.x[3]]
})

# Acceleration Factor from 85 C to 105 C
p['c85'].iloc[0] / p['c105'].iloc[0]
# Acceleration Factor from 105 to 125 C
p['c105'].iloc[0] / p['c125'].iloc[0]
# Acceleration Factor from 85 to 125 C
p['c85'].iloc[0] / p['c125'].iloc[0]



# 5. Conditional Probability of Failure given Burn-In #############################

# Let's write the Weibull density and failure function, as always...
def d(t, c, m):
    return (m / t) * (t / c)**m * np.exp(-1 * ((t / c)**m))

def f(t, c, m):
    return 1 - np.exp(-1 * ((t / c)**m))

def fb(t, tb, a, c, m):
    # Change in probability of failure
    delta_failure = f(t=t + a * tb, c=c, m=m) - f(t=a * tb, c=c, m=m)
    # Reliability after burn-in period
    reliability = 1 - f(t=a * tb, c=c, m=m)
    # conditional probability of failure
    return delta_failure / reliability

# 1000 hours after burn-in
# with a burn-in period of 100 hours
# an acceleration factor of 20
# characteristic life c = 2000 hours
# and
# shape parameter m = 1.5
fb(t=1000, tb=100, a=20, c=2000, m=1.5)
