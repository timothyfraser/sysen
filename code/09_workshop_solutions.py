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
from scipy import stats        # distributions (dunif, dnorm, dweibull in R)
from scipy.optimize import minimize  # optimizer (optim() in R)

# Load data.frame of crops by time to failure metric `days`
crops = pd.read_csv("workshops/crops.csv")

# View empirical distribution of days
# (hist() in base R; geom_histogram() in plotnine)
(ggplot(crops, aes(x = 'days')) + geom_histogram(bins = 10))

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
print(d(t = 72, lam = 0.014359))
print(d(t = 72, lam = 0.015))







# This is the JOINT probability of a lifespan of 72
# AND another lifespan of 119, given this particular lambda value
print(d(t = 72, lam = mylambda) * d(t = 119, lam = mylambda))










# This is the JOINT probability of ALL these lifespans, given this lambda value
# np.prod() is product
# JOINT probability also called LIKELIHOOD
print(np.prod(d(t = crops['days'], lam = 0.014)))










# But tiny decimals are hard for Python to compute. So we often want to log them.
print(np.log(np.prod(d(t = crops['days'], lam = 0.014))))












# Excitingly the log of the product of probabilities
# is equal to the sum of logged probabilities
print(np.sum(np.log(d(t = crops['days'], lam = 0.014))))
print(np.log(np.prod(d(t = crops['days'], lam = 0.014))))







# So we often find ourselves calculating:
# **log-likelihood**





# Calculate Log-Likelihood, by summing the log
def ll(t, lam):
  return np.sum(np.log(d(t = t, lam = lam)))







# Suppose lambda is 0.014.
# Then the log likelihood of this observed data t is...
# aka the probability of getting all
# of these values simultaneously in one sample...
print(ll(t = crops['days'], lam = 0.014))



# (plot() of a two-column table in base R is a scatterplot)
lambdas = np.arange(0.00001, 1, 0.001)
(ggplot(pd.DataFrame({
    'lambda': lambdas,
    'loglik': [ll(t = crops['days'], lam = l) for l in lambdas]}),
  aes(x = 'lambda', y = 'loglik'))
  + geom_point())




# Let's hack this manually!
# We're going to make a sequence of parameters from 0.00001 to 1
# and get the log likelihood of the crops['days'] vector given each of these parameters.
manyll = pd.DataFrame({'parameter': np.arange(0.00001, 1, 0.001)})
# For each of these parameters
# Calculate a different loglik statistic
manyll['loglik'] = [ll(t = crops['days'], lam = p) for p in manyll['parameter']]




# Check it out! Some parameters are more or less likely.
print(manyll.head(3))

# Let's find the maximum loglikelihood!
# That loglikelihood will pair with the parameter that is therefore MOST likely to match this observed distribution.
output = manyll[manyll['loglik'] == manyll['loglik'].max()]

print(output)
# PRETTY DARN CLOSE TO OUR ORIGINAL LAMBDA!!!!! HOLY SMOKES!
print(mylambda)



# We can visualize this process like so!
p = output['parameter'].iloc[0]
g = (ggplot()
  + geom_line(data = manyll, mapping = aes(x = 'parameter', y = 'loglik'), color = "steelblue")
  + geom_vline(xintercept = p, linetype = "dashed")
  + theme_classic(base_size = 14)
  + labs(x = "parameter (lambda)", y = "loglik (Log-Likelihood)",
         subtitle = "Maximizing the Log-Likelihood (Visually)")
  # We can actually adust the x-axis to work better with log-scales here
  + scale_x_log10()
  # We can also annnotate our visuals like so.
  + annotate("text", x = 0.1, y = -2000, label = str(round(p, 5))))
g



# We did it manually, but how do we do it automatically?

# We use an OPTIMIZER. R has optim(); Python has scipy.optimize.minimize().
# It searches along the curve/plane we visualized above.
# R's optim() defaults to the Nelder-Mead method, so we use it too.

# Optimize and collect the quantities of interest
# minimize() only MINIMIZES. R flips the sign with control = list(fnscale = -1);
# in Python we minimize the NEGATIVE log-likelihood, which is the same thing.
q = minimize(lambda par: -ll(t = crops['days'], lam = par[0]),
             x0 = [0.01], method = "Nelder-Mead")

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
# (dunif(t, min, max) in R is stats.uniform.pdf(t, loc = min, scale = max - min))
def ll(t, par):
  return np.sum(np.log(stats.uniform.pdf(t, loc = par[0], scale = par[1] - par[0])))

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
  return np.sum(np.log(stats.norm.pdf(t, loc = par[0], scale = par[1])))

# Let's try it out!
# Heads up: this next line is SUPPOSED to fail. stats.norm.pdf(days, 0, 1)
# underflows to 0, log(0) is -inf, and the optimizer cannot search.
# R's optim() stops with an error; minimize() just gives back a useless answer
# (success False, or the starting values unchanged). Read it - diagnosing it
# is the next twenty lines of this script.
with np.errstate(divide = 'ignore'):
  bad = minimize(lambda par: -ll(t = crops['days'], par = par),
                 x0 = [0, 1], method = "Nelder-Mead")
print(bad.success, bad.x, bad.fun)
# Why doesn't it work?

# Well, we're giving it super weird starting parameters. (0,1)
# What densities would they produce?
print(stats.norm.pdf(crops['days'], loc = 0, scale = 1))
# What loglikelihood would they produce?
with np.errstate(divide = 'ignore'):
  print(np.sum(np.log(stats.norm.pdf(crops['days'], loc = 0, scale = 1))))

# Let's look at our real values...
print(crops['days'].values)


# What if we picked more representative starting parameters?
q2 = minimize(lambda par: -ll(t = crops['days'], par = par),
              x0 = [90, 15], method = "Nelder-Mead")
print(q2.x)
# Yay! It works!


print(stats.norm.cdf(np.arange(1, 11), loc = q2.x[0], scale = q2.x[1]))


# Let's try a weibull!
# (pweibull(q, shape, scale) in R is stats.weibull_min.cdf(q, c = shape, scale = scale))
print(stats.weibull_min.cdf(1, c = 2, scale = 1))


def llweibull(t, par):
  return np.sum(np.log(stats.weibull_min.pdf(t, c = par[0], scale = par[1])))

q3 = minimize(lambda par: -llweibull(t = crops['days'], par = par),
              x0 = [1, 1000], method = "Nelder-Mead")

print(q3.x)



# You might want to hang on to this
# Chunk of helper code
# minimize(lambda par: -ll(t, par), x0 = [...], method = "Nelder-Mead")
# def d(t, lam): return lam * np.exp(-1 * t * lam)

# All done!
