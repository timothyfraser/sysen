# 09_workshop_solutions.py
# Tim Fraser
# Workshop 9: Parameter Estimation by Maximum Likelihood (worked solutions)
# Chapter: Useful Life Distributions (Weibull, Gamma, & Lognormal) in Python

# It mirrors 09_workshop_solutions.R section by section.
#
# Heads up: the normal-distribution demo below deliberately fails on purpose,
# to show what bad starting parameters do. Run this script chunk by chunk
# rather than all at once.
# Run it from the top of the sysen folder, so the file paths below work.

# Load packages
import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr + readr in R)
from plotnine import *         # visuals (ggplot2 in R)
import sys
# Load our R-style helpers: hist(), dnorm(), pnorm(), dunif(), dweibull(), pweibull()
sys.path.append("functions")
from functions_distributions import hist, dnorm, pnorm, dunif, dweibull, pweibull
from scipy.optimize import minimize  # optimizer (optim() in R)

# Load data.frame of crops by time to failure metric `days`
crops = pd.read_csv("workshops/crops.csv")
# View empirical distribution of days
hist(crops['days'])
# Calculate (empirically) lambda
mylambda = 1 / crops['days'].mean()
print(mylambda)

# PROBLEM: What if we can't calculate our parameters empirically?
# Applicable when multiple parameters, parameters are interdependent, trick distributions, etc.
# We need some other way to estimate our parameters.
# Maximum Likelihood Estimation! (MLE)

# 1 parameter = labmda
# lambda = 1 / mean(t)
# Failure Function CDF F(t)
def f(t, lam):
  return 1 - np.exp(-1 * t * lam)

# PDF function  f(t)
# (lambda is a reserved word in Python, so the argument is called lam)
def d(t, lam):
  return lam * np.exp(-t * lam)

# Let's look at our first 3 observations
print(crops['days'][0:3])
# This is the probability of a lifespan of 72, given this particular lambda value
print(d(t = 72, lam = mylambda))
# This is the JOINT probability of a lifespan of 72 AND another lifespan of 119, given this particular lambda value
print(d(t = 72, lam = mylambda) * d(t = 119, lam = mylambda))

# This is the JOINT probability of ALL these lifespans, given this lambda value
# np.prod() is product
# JOINT probability also called LIKELIHOOD
print(np.prod(d(t = crops['days'], lam = 0.014)))

# But tiny decimals are hard for Python to compute. So we often want to log them.
print(np.log(np.prod(d(t = crops['days'], lam = 0.014))))
# Excitingly the log of the product of probabilities is equal to the sum of logged probabilities
print(np.sum(np.log(d(t = crops['days'], lam = 0.014))))
# So we often find ourselves calculating:
# **log-likelihood**


# Calculate Log-Likelihood, by summing the log
def ll(t, lam):
  return np.log(d(t = t, lam = lam)).sum(skipna = False)  # NaN stays NaN, as in R
# Suppose lambda is 0.014.
# Then the log likelihood of this observed data t is...
# aka the probability of getting all these values simultaneously in one sample...
print(ll(t = crops['days'], lam = 0.014))



# Let's hack this manually!
# We're going to make a sequence of parameters from 0.00001 to 1
# and get the log likelihood of the crops['days'] vector given each of these parameters.
manyll = (pd.DataFrame({'parameter': np.arange(0.00001, 1, 0.001)})
  # For each of these parameters
  # Calculate a different loglik statistic
  .assign(loglik = lambda x: [ll(t = crops['days'], lam = p) for p in x['parameter']]))

# Check it out! Some parameters are more or less likely.
print(manyll.head(3))

# Let's find the maximum loglikelihood!
# That loglikelihood will pair with the parameter that is therefore MOST likely to match this observed distribution.
output = manyll[manyll['loglik'] == manyll['loglik'].max()]

print(output)
# PRETTY DARN CLOSE TO OUR ORIGINAL LAMBDA!!!!! HOLY SMOKES!
print(mylambda)



# We can visualize this process like so!
(ggplot()
  + geom_line(data = manyll, mapping = aes(x = 'parameter', y = 'loglik'), color = "steelblue")
  + geom_vline(xintercept = output['parameter'].iloc[0], linetype = "dashed")
  + theme_classic(base_size = 14)
  + labs(x = "parameter (lambda)", y = "loglik (Log-Likelihood)",
         subtitle = "Maximizing the Log-Likelihood (Visually)")
  # We can actually adust the x-axis to work better with log-scales here
  + scale_x_log10()
  # We can also annnotate our visuals like so.
  + annotate("text", x = 0.1, y = -2000, label = str(round(output['parameter'].iloc[0], 5))))



# We did it manually, but how do we do it automatically?

# We use an OPTIMIZER. R has optim(); Python has scipy.optimize.minimize().
# It searches along the curve/plane we visualized above.
# R's optim() defaults to the Nelder-Mead method, so we use it too.

# Optimize and collect the quantities of interest
# minimize() only MINIMIZES. R flips the sign with control = list(fnscale = -1);
# in Python we minimize the NEGATIVE log-likelihood, which is the same thing.
q = minimize(lambda par: -ll(t = crops['days'], lam = par[0]),
             x0 = [0.01], method = "Nelder-Mead")

q = minimize(fun = lambda par: -ll(t = crops['days'], lam = par[0]), x0 = [0.01], method = "Nelder-Mead")

# q is an OptimizeResult object - a dictionary with named parts.
# We've learned several types of objects
pd.DataFrame()
[]
# Here's a dictionary example (a list() in R)
mylist = {'df': pd.DataFrame({'x': range(1, 11)}),
          'par': 0.234}
# You can query the par value in the dictionary like this.
print(mylist['par'])

print(q)
# The optimized parameters live in q.x (q$par in R)
# Once we have our optimized parameters, we can pipe it into functions like this!
print(f(t = np.arange(1, 101), lam = q.x[0]))


# We could also write MULTI-PARAMETER loglikelihood functions!
def ll(t, par):
  return np.log(dunif(t, min = par[0], max = par[1])).sum(skipna = False)  # NaN stays NaN, as in R

print(crops['days'].min(), crops['days'].max())
# Let's try it!
# Note the starting values: for a UNIFORM likelihood, min and max must bracket
# every observation. Any t outside [min, max] has density 0, log(0) is -inf,
# and the whole loglikelihood collapses to -inf before the optimizer can search.
with np.errstate(divide = 'ignore'):
  print(minimize(lambda par: -ll(t = crops['days'], par = par),
                 x0 = [4, 197], method = "Nelder-Mead"))

# What about other distributions?

# Let's write a new function
def ll(t, par):
  # Our parameters input is now going to be vector of 2 values
  # par[0] gives the first value, the mean (Python counts from 0)
  # par[1] gives the second value, the standard deviation
  return np.log(dnorm(t, mean = par[0], sd = par[1])).sum(skipna = False)  # NaN stays NaN, as in R
# Let's try it out!
# Heads up: this next line is SUPPOSED to fail. dnorm(days, 0, 1)
# underflows to 0, log(0) is -inf, and the optimizer cannot search.
# R's optim() stops with an error; minimize() just hands back a useless answer
# (success False, the starting values unchanged). Read it - the two lines
# below show you exactly why.
with np.errstate(divide = 'ignore'):
  print(minimize(lambda par: -ll(t = crops['days'], par = par), x0 = [0, 1], method = "Nelder-Mead"))
  print(dnorm(crops['days'], mean = 0, sd = 1))
  print(np.log(dnorm(crops['days'], mean = 0, sd = 1)).sum(skipna = False))

print(crops['days'].values)

q2 = minimize(lambda par: -ll(t = crops['days'], par = par), x0 = [90, 15], method = "Nelder-Mead")
print(q2.x)


print(pnorm(np.arange(1, 11), mean = q2.x[0], sd = q2.x[1]))

# Let's try a weibull!
print(pweibull(1, shape = 2, scale = 1))


def llweibull(t, par):
  return np.log(dweibull(t, shape = par[0], scale = par[1])).sum(skipna = False)  # NaN stays NaN, as in R

q3 = minimize(lambda par: -llweibull(t = crops['days'], par = par),
              x0 = [1, 1000], method = "Nelder-Mead")

print(q3.x)

# You might want to hang on to this
# Chunk of helper code
# minimize(lambda par: -ll(t, par), x0 = [...], method = "Nelder-Mead")
# def d(t, lam): return lam * np.exp(-1 * t * lam)

# All done!
