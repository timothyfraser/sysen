# 07_lesson.py
# Tim Fraser
# Lesson 7: The exponential distribution
# Chapter: Useful Life Distributions (Exponential) in Python
#
# More info here: https://timothyfraser.com/sigma/


import pandas as pd
import numpy as np
import sympy as sp
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_distributions import hist

masks = pd.read_csv("workshops/masks.csv")

masks.info()

# Let's write some functions!
# failure function (CDF)
def f(t, lambda_):
    return 1 - np.exp(-1 * t * lambda_)
# reliability function
def r(t, lambda_):
    return np.exp(-1 * t * lambda_)



stat = pd.DataFrame({
    # The literal mean time to fail
    # in our observed distribution is this
    'mttf': [masks['left_earloop'].mean()]
})
stat['lambda'] = 1 / stat['mttf']
# The observed median is this....
stat['median'] = masks['left_earloop'].median()
# But if we assume it's an exponential distribution
# and calculate the median from lambda,
# we get t50, which is very close.
stat['t50'] = np.log(2) / stat['lambda']
stat

hist(masks['left_earloop'])

stat['lambda'].iloc[0]

r(t=10 + 5, lambda_=stat['lambda'].iloc[0]) / r(t=10, lambda_=stat['lambda'].iloc[0])





def cr(t, x, lambda_):
    # We can actually nest functions inside each other,
    # to make them easier to write
    def r(t, lambda_):
        return np.exp(-1 * t * lambda_)

    # Calculate R(x + t) / R(t)
    output = r(t=t + x, lambda_=lambda_) / r(t=t, lambda_=lambda_)

    # and return the result!
    return output

cr(t=10, x=5, lambda_=stat['lambda'].iloc[0])




# Calculate Mean Residual Life
# R uses mosaicCalc::antiD(); Python uses sympy.integrate.
def mu(t, lambda_):

    # Get the Reliability Function for exponential distribution
    def r(t, lambda_):
        return np.exp(-1 * t * lambda_)

    t_sym, lam_sym = sp.symbols('t lambda', positive=True)
    mttf_expr = sp.integrate(sp.exp(-lam_sym * t_sym), (t_sym, 0, sp.oo))
    mttf_fn = sp.lambdify(lam_sym, mttf_expr, 'numpy')

    # Now calculate mu(), the Mean Residual Life function at time t
    output = mttf_fn(lambda_) / r(t=t, lambda_=lambda_)

    return output

# Get the MTTF (integral of reliability function)
def r(t, lambda_):
    return np.exp(-1 * t * lambda_)

r(t=100, lambda_=0.01)

t_sym, lam_sym = sp.symbols('t lambda', positive=True)
mttf = sp.lambdify(lam_sym,
                   sp.integrate(sp.exp(-lam_sym * t_sym), (t_sym, 0, sp.oo)),
                   'numpy')

# mttf(0.001)
mttf(0.001)

1 / 0.001
