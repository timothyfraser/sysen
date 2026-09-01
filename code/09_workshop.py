# 09_workshop.py
# Tim Fraser
# Workshop 9: Parameter Estimation - Single-Parameter Maximum Likelihood
# Chapter: Useful Life Distributions (Weibull, Gamma, & Lognormal) in Python

# Load packages
import pandas as pd
import numpy as np
from plotnine import *
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_distributions import hist

# Load data.frame of crops by time to failure metric `days`
crops = pd.read_csv("workshops/crops.csv")

crops

# View empirical distribution of days
hist(crops['days'])

# Calculate (empirically) lambda
mylambda = 1 / crops['days'].mean()

mylambda


# PROBLEM: What if we can't calculate our parameters empirically?
# Applicable when multiple parameters, parameters are interdependent, trick distributions, etc.
# We need some other way to estimate our parameters.
# Maximum Likelihood Estimation! (MLE)

# 1 parameter = lambda
# lambda = 1 / mean(t)


# Failure Function CDF F(t)
def f(t, lambda_):
    return 1 - np.exp(-1 * t * lambda_)

# PDF function  f(t)
def d(t, lambda_):
    return lambda_ * np.exp(-t * lambda_)





# Let's look at our first 3 observations
crops['days'].iloc[0:3]







# This is the probability of a lifespan of 72, given this particular lambda value
d(t=72, lambda_=mylambda)
d(t=72, lambda_=0.014359)
d(t=72, lambda_=0.015)







# This is the JOINT probability of a lifespan of 72
# AND another lifespan of 119, given this particular lambda value
d(t=72, lambda_=mylambda) * d(t=119, lambda_=mylambda)









# This is the JOINT probability of ALL these lifespans, given this lambda value
# .prod() is product
# JOINT probability also called LIKELIHOOD
d(t=crops['days'], lambda_=0.014).prod()









# But tiny decimals are hard for Python to compute. So we often want to log them.
np.log(d(t=crops['days'], lambda_=0.014).prod())









# Excitingly the log of the product of probabilities
# is equal to the sum of logged probabilities
np.log(d(t=crops['days'], lambda_=0.014)).sum()
np.log(d(t=crops['days'], lambda_=0.014).prod())






# So we often find ourselves calculating:
# **log-likelihood**





# Calculate Log-Likelihood, by summing the log
def ll(t, lambda_):
    return np.log(d(t=t, lambda_=lambda_)).sum()







# Suppose lambda is 0.014.
# Then the log likelihood of this observed data t is...
# aka the probability of getting all
# of these values simultaneously in one sample...
ll(t=crops['days'], lambda_=0.014)



manyll = pd.DataFrame({
    'lambda': np.arange(0.00001, 1, 0.001)
})
manyll['loglik'] = [ll(t=crops['days'], lambda_=p) for p in manyll['lambda']]
manyll.plot(x='lambda', y='loglik')




# Let's hack this manually!
# We're going to make a sequence of parameters from 0.00001 to 1
# and get the log likelihood of the crops$days vector given each of these parameters.
manyll = pd.DataFrame({
    'parameter': np.arange(0.00001, 1, 0.001)
})
# For each of these parameters
# Calculate a different loglik statistic
manyll['loglik'] = [ll(t=crops['days'], lambda_=p) for p in manyll['parameter']]




# Check it out! Some parameters are more or less likely.
manyll.head(3)

# Let's find the maximum loglikelihood!
# That loglikelihood will pair with the parameter that is therefore MOST likely to match this observed distribution.
output = manyll[manyll['loglik'] == manyll['loglik'].max()]

output
# PRETTY DARN CLOSE TO OUR ORIGINAL LAMBDA!!!!! HOLY SMOKES!
mylambda



# We can visualize this process like so!
(ggplot() +
    geom_line(data=manyll, mapping=aes(x='parameter', y='loglik'), color='steelblue') +
    geom_vline(xintercept=output['parameter'].iloc[0], linetype='dashed') +
    theme_classic(base_size=14) +
    labs(x='parameter (lambda)', y='loglik (Log-Likelihood)',
         subtitle='Maximizing the Log-Likelihood (Visually)') +
    # We can actually adjust the x-axis to work better with log-scales here
    scale_x_log10() +
    # We can also annotate our visuals like so.
    annotate('text', x=0.1, y=-2000, label=str(output['parameter'].iloc[0])))
