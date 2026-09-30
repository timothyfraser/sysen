# 09_workshop.py
# Tim Fraser
# Workshop 9: Parameter Estimation - Single-Parameter Maximum Likelihood
# Chapter: Useful Life Distributions (Weibull, Gamma, & Lognormal) in Python

# It mirrors 09_workshop.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.

# Load packages
import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr + readr in R)
from plotnine import *         # visuals (ggplot2 in R)

# Load data.frame of crops by time to failure metric `days`
crops = pd.read_csv("workshops/crops.csv")

print(crops)

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
