# 10_lesson.py
# Tim Fraser
# Lesson 10: Physical Acceleration Models
# In this lesson, let's learn Weibull Acceleration modeling
# and MLE for acceleration modeling!

# It mirrors 10_lesson.R section by section.
# Run it from the top of the sysen folder.

# Packages
import numpy as np                     # math (base R in R)
import pandas as pd                    # data wrangling (dplyr in R)
import statsmodels.formula.api as smf  # linear models (lm() + broom in R)
from scipy.optimize import minimize    # optimization (optim() in R)
from plotnine import *                 # visualization (ggplot2 in R)
import warnings
# Nelder-Mead will sometimes try a negative c or m, which gives NaN (R warns
# about this too, quietly). We silence those numpy warnings to keep output tidy.
warnings.filterwarnings("ignore", category=RuntimeWarning)


# LINEAR REGRESSION FOR WEIBULL ACCELERATION MODELING ##############################


# Let's make a data.frame matching Example 1 from the lesson slides
data = pd.DataFrame({
    't': [24, 72, 168, 300, 500, 750, 1000, 1250, 1500],
    'r85': [1, 0, 0, 1, 0, 3, 0, 1, 2],
    'r105': [2, 1, 3, 2, 2, 4, 5, 1, 4],
    'r125': [5, 10, 13, 2, 3, 2, 2, 1, 0]})
n = 40

# Calculate probability of failure at time t under 85 degrees
data['f85'] = data['r85'].cumsum() / n
# Convert to this formula
data['y85'] = np.log(-np.log(1 - data['f85']))

# (R's lm(y ~ log(t)) becomes smf.ols("y ~ np.log(t)"))
m = smf.ols("y85 ~ np.log(t)", data=data).fit()

intercept = m.params.iloc[0]  # intercept
slope = m.params.iloc[1]      # slope

# These are our estimates for m and c at stress level 85
print(pd.DataFrame({'mhat': [slope], 'chat': [np.exp(-intercept / slope)]}))


# What!!!?

# Let's streamline this.

# t [numeric] vector of times to failure. Same length as vector r.
# r [integer] failures at time t. Same length as vector t.
# n [integer] number of total units under test. Length 1.
def graphical_estimates(t, r, n=40):

    # Testing values
    # t = data['t']; r = data['r85']; n = 40

    # Make data.frame
    df = pd.DataFrame({'t': np.asarray(t), 'r': np.asarray(r)})
    df['n'] = n

    # Calculate probability of failure
    df['f'] = df['r'].cumsum() / n

    # Calculate transformation variable y
    df['y'] = np.log(-np.log(1 - df['f']))

    # Get model m
    m = smf.ols("y ~ np.log(t)", data=df).fit()

    # Get coefficients
    intercept = m.params.iloc[0]
    slope = m.params.iloc[1]

    # Calculate estimates for m and c
    output = pd.DataFrame({'mhat': [slope], 'chat': [np.exp(-intercept / slope)]})

    return output

# Let's try it!
print(graphical_estimates(t=data['t'], r=data['r85'], n=40))

# Get parameters at different levels of stress
p85 = graphical_estimates(t=data['t'], r=data['r85'], n=40)
p105 = graphical_estimates(t=data['t'], r=data['r105'], n=40)
p125 = graphical_estimates(t=data['t'], r=data['r125'], n=40)

# We know c_u = AF x c_s,
# so AF = c_s / c_u

# AF from 85 to 105 degrees
print(p85['chat'][0] / p105['chat'][0])
# AF from 105 to 125 degrees
print(p105['chat'][0] / p125['chat'][0])
# AF from 85 to 125 degrees
print(p85['chat'][0] / p125['chat'][0])


# 85 C cell   m-hat = 0.57  c-hat 40222  Acceleration to 105 C = 18.2
# 105 C cell   m-hat = 0.70  c-hat 2208  Acceleration to 105 C = 9.1
# 125 C cell   m-hat = 0.71  c-hat 242  Acceleration to 105 C = 166.2


# (R's rm(list = ls()) clears the workspace; in Python we simply
# redefine what each section needs.)



# MLE WITH FIXED M FOR WEIBULL ACCELERATION MODELING #####################


# Let's make a data.frame matching Example 1 from the lesson slides
data = pd.DataFrame({
    't': [24, 72, 168, 300, 500, 750, 1000, 1250, 1500],
    'r85': [1, 0, 0, 1, 0, 3, 0, 1, 2],
    'r105': [2, 1, 3, 2, 2, 4, 5, 1, 4],
    'r125': [5, 10, 13, 2, 3, 2, 2, 1, 0]})
n85 = 40
n105 = 40
n125 = 40


# Let's write ourselves a speedy weibull density function 'd()'
def d(t, m, c):
    return (m / t) * (t / c)**m * np.exp(-1 * (t / c)**m)

def r(t, m, c):
    return np.exp(-(t / c)**m)

# Let's write our crosstable's likelihood function
def ll(par, t, x1, x2, x3, n1, n2, n3):
    t = np.asarray(t, dtype=float)
    # Get total failures
    r1 = np.sum(x1)
    r2 = np.sum(x2)
    r3 = np.sum(x3)
    tmax = np.max(t)  # Record last time step

    # Get product of log-densities at each time step, for all failures then
    prob_d1 = np.sum(np.log(d(t, c=par[0], m=par[3])) * x1)
    prob_d2 = np.sum(np.log(d(t, c=par[1], m=par[3])) * x2)
    prob_d3 = np.sum(np.log(d(t, c=par[2], m=par[3])) * x3)

    # For last time step, get probability of each remaining unit surviving
    prob_r1 = np.log(r(t=tmax, c=par[0], m=par[3])**(n1 - r1))
    prob_r2 = np.log(r(t=tmax, c=par[1], m=par[3])**(n2 - r2))
    prob_r3 = np.log(r(t=tmax, c=par[2], m=par[3])**(n3 - r3))

    # Get joint log-likelihood, across ALL vectors
    return prob_d1 + prob_r1 + prob_d2 + prob_r2 + prob_d3 + prob_r3


# And let's run MLE!
# R's optim(..., control = list(fnscale = -1)) MAXIMIZES the log-likelihood.
# scipy's minimize() minimizes, so we hand it the NEGATIVE log-likelihood.
# optim()'s default method is Nelder-Mead, so we use that too.
mle = minimize(
    lambda par: -ll(par, t=data['t'],
                    x1=data['r85'], n1=n85,
                    x2=data['r105'], n2=n105,
                    x3=data['r125'], n3=n125),
    x0=[1000, 1000, 1000, 1],
    method="Nelder-Mead")


# Extract parameters into a dataframe
p = pd.DataFrame({
    'c85': [mle.x[0]],
    'c105': [mle.x[1]],
    'c125': [mle.x[2]],
    'm': [mle.x[3]]})
print(p)

# Acceleration Factor from 85 C to 105 C
print(p['c85'][0] / p['c105'][0])
# Acceleration Factor from 105 to 125 C
print(p['c105'][0] / p['c125'][0])
# Acceleration Factor from 85 to 125 C
print(p['c85'][0] / p['c125'][0])



# 3. MLE WITH VARYING M ################################################


# Let's make a data.frame matching Example 1 from the lesson slides
data = pd.DataFrame({
    't': [24, 72, 168, 300, 500, 750, 1000, 1250, 1500],
    'r85': [1, 0, 0, 1, 0, 3, 0, 1, 2],
    'r105': [2, 1, 3, 2, 2, 4, 5, 1, 4],
    'r125': [5, 10, 13, 2, 3, 2, 2, 1, 0]})
n85 = 40
n105 = 40
n125 = 40


# Let's write ourselves a speedy weibull density function 'd()'
def d(t, m, c):
    return (m / t) * (t / c)**m * np.exp(-1 * (t / c)**m)

def r(t, m, c):
    return np.exp(-(t / c)**m)

# Let's write our crosstable's likelihood function
def ll(par, t, x1, x2, x3, n1, n2, n3):
    t = np.asarray(t, dtype=float)
    # Get total failures
    r1 = np.sum(x1)
    r2 = np.sum(x2)
    r3 = np.sum(x3)
    tmax = np.max(t)  # Record last time step

    # Get product of log-densities at each time step, for all failures then
    prob_d1 = np.sum(np.log(d(t, c=par[0], m=par[3])) * x1)
    prob_d2 = np.sum(np.log(d(t, c=par[1], m=par[4])) * x2)
    prob_d3 = np.sum(np.log(d(t, c=par[2], m=par[5])) * x3)

    # For last time step, get probability of each remaining unit surviving
    prob_r1 = np.log(r(t=tmax, c=par[0], m=par[3])**(n1 - r1))
    prob_r2 = np.log(r(t=tmax, c=par[1], m=par[4])**(n2 - r2))
    prob_r3 = np.log(r(t=tmax, c=par[2], m=par[5])**(n3 - r3))

    # Get joint log-likelihood, across ALL vectors
    return prob_d1 + prob_r1 + prob_d2 + prob_r2 + prob_d3 + prob_r3


# And let's run MLE!
mle = minimize(
    lambda par: -ll(par, t=data['t'],
                    x1=data['r85'], n1=n85,
                    x2=data['r105'], n2=n105,
                    x3=data['r125'], n3=n125),
    x0=[1000, 1000, 1000, 1, 1, 1],
    method="Nelder-Mead",
    options={'maxiter': 5000, 'maxfev': 5000})


# Extract parameters into a dataframe
p = pd.DataFrame({
    'c85': [mle.x[0]],
    'c105': [mle.x[1]],
    'c125': [mle.x[2]],
    'm85': [mle.x[3]],
    'm105': [mle.x[4]],
    'm125': [mle.x[5]]})
print(p)

# Acceleration Factor from 85 C to 105 C
print(p['c85'][0] / p['c105'][0])
# Acceleration Factor from 105 to 125 C
print(p['c105'][0] / p['c125'][0])
# Acceleration Factor from 85 to 125 C
print(p['c85'][0] / p['c125'][0])




# 4. MLE 3 times FOR WEIBULL ACCELERATION MODELING #####################
# Not really recommended -- just an extra example to show the distinction


# Let's make a data.frame matching Example 1 from the lesson slides
data = pd.DataFrame({
    't': [24, 72, 168, 300, 500, 750, 1000, 1250, 1500],
    'r85': [1, 0, 0, 1, 0, 3, 0, 1, 2],
    'r105': [2, 1, 3, 2, 2, 4, 5, 1, 4],
    'r125': [5, 10, 13, 2, 3, 2, 2, 1, 0]})
n85 = 40
n105 = 40
n125 = 40


# Let's write ourselves a speedy weibull density function 'd()'
def d(t, m, c):
    return (m / t) * (t / c)**m * np.exp(-1 * (t / c)**m)

def r(t, m, c):
    return np.exp(-(t / c)**m)

# Let's write our crosstable's likelihood function
def ll(par, t, x1, n1):
    t = np.asarray(t, dtype=float)
    # Get total failures
    r1 = np.sum(x1)
    tmax = np.max(t)  # Record last time step

    # Get product of log-densities at each time step, for all failures then
    prob_d1 = np.sum(np.log(d(t, c=par[0], m=par[1])) * x1)

    # For last time step, get probability of each remaining unit surviving
    prob_r1 = np.log(r(t=tmax, c=par[0], m=par[1])**(n1 - r1))

    # Get joint log-likelihood, across ALL vectors
    return prob_d1 + prob_r1


# And let's run MLE!
mle85 = minimize(lambda par: -ll(par, t=data['t'], x1=data['r85'], n1=n85),
                 x0=[1000, 1], method="Nelder-Mead")

mle105 = minimize(lambda par: -ll(par, t=data['t'], x1=data['r105'], n1=n105),
                  x0=[1000, 1], method="Nelder-Mead")

mle125 = minimize(lambda par: -ll(par, t=data['t'], x1=data['r125'], n1=n125),
                  x0=[1000, 1], method="Nelder-Mead")


# Extract parameters into a dataframe
p = pd.DataFrame({
    'c85': [mle85.x[0]],
    'c105': [mle105.x[0]],
    'c125': [mle125.x[0]],
    'm85': [mle85.x[1]],
    'm105': [mle105.x[1]],
    'm125': [mle125.x[1]]})

print(p)
# Acceleration Factor from 85 C to 105 C
print(p['c85'][0] / p['c105'][0])
# Acceleration Factor from 105 to 125 C
print(p['c105'][0] / p['c125'][0])
# Acceleration Factor from 85 to 125 C
print(p['c85'][0] / p['c125'][0])



# 5. Conditional Probability of Failure given Burn-In #############################

# Let's write the Weibull density and failure function, as always...
def d(t, c, m):
    return (m / t) * (t / c)**m * np.exp(-1 * (t / c)**m)

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
print(fb(t=1000, tb=100, a=20, c=2000, m=1.5))
