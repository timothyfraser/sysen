# 04_workshop.py
# Tim Fraser
# Workshop 4: Failure functions and system reliability
# Chapter: System Reliability in Python

# In today's workshop, let's practice our many, many ways
# of using failure functions to analyze system reliability!

# See 04_workshop_solutions for solutions (but only after class!)
# R uses mosaicCalc::antiD() for integrals; Python has no mosaicCalc.
# We use sympy for symbolic calculus, matching the Python tutorial.

# 0. Load Packages ################################################

import pandas as pd
import numpy as np
from plotnine import *
import sympy as sp
import math
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_distributions import dexp, pexp, hist


# 1. Making Functions ##############################################

# You learned to make Functions in Week 3. Let's practice!
# https://timothyfraser.com/sigma/chapters/functions-in-python.html

# Nintendo is product testing its next Switch console.
# 1000 enthusiastic children received a console in the mail,
# played video games for days on end, and
# parents called in when the console eventually broke.

# On average, 1 console failed every 1200 hours (50 days).

# So, we say the constant failure rate lambda was 1/1200 hours

# Using your notes from Workshop 4, let's write a few functions using lambda!




### Example Function l() (for lambda) ###################################

# The exponential distribution has one parameter
# lambda = the rate of failure
# 1 / mean time to failure


# units = how many pokeballs failed
# hours = how many hours they were used

# mu = hours / units ( mean hours to failure)
# lambda = 1 / mu
# every hour, how many pokeballs do we expect to fail?

def l(units, hours):
    return units / hours


# We have an empirical failure rate of 0.2 pokeballs per hour




# Note: In Python, for exponential distribution,
# we write e^something as np.exp(something)  (or math.exp for a scalar)

# Q1. Let's write our probability density function d(t)
# PDF looks like: d(t) = lambda * e^(-lambda*t)


# d(t) = density
# f(t) = failure rate (CDF)
# r(t) = reliability
# z(t) = failure rate (hazard)
# h(t) = accumulative hazard
# afr(t) = average failure rate

def d(t, lambda_):
    return lambda_ * np.exp(-1 * lambda_ * t)

def f(t, lambda_):
    return 1 - np.exp(-lambda_ * t)
# 1 - e^(-lambda*t)

# Or, you could integrate the PDF to produce the equivalent function!!
# sympy.integrate is the Python twin of mosaicCalc::antiD()
t_sym, lambda_sym = sp.symbols('t lambda', positive=True)
f2 = sp.lambdify((t_sym, lambda_sym),
                 sp.integrate(lambda_sym * sp.exp(-lambda_sym * t_sym), t_sym),
                 'numpy')
f2(100, 0.01)

f(t=100, lambda_=0.01)


# PDF f(t) is always d(t) in this course
d(t=100, lambda_=0.01)
dexp(x=100, rate=0.01)


# INTEGRATING FUNCTIONS ##############################################

# PDF d(t) (also called little f(t), but to avoid confusion, we say d(t))
def d(t, lambda_):
    return lambda_ * np.exp(-1 * lambda_ * t)

# Failure F(t)
def f(t, lambda_):
    return 1 - np.exp(-1 * lambda_ * t)

# cumulative probability of failure by 100 hours?
f(t=100, lambda_=0.01)
pexp(x=100, rate=0.01)




# VISUALIZE IT ########################################


lambda_a = .01
lambda_b = .005

# Reliability R(t) - we need these two before we can plot anything with them
def f(t, lambda_):
    return 1 - np.exp(-1 * lambda_ * t)

def r(t, lambda_):
    return 1 - f(t, lambda_)

t_vals = np.arange(1, 1001)
pd.DataFrame({
    't': t_vals,
    'prob_a': r(t=t_vals, lambda_=lambda_a),
    'prob_b': r(t=t_vals, lambda_=lambda_b)
})


dat = pd.DataFrame({
    't': t_vals,
    'prob_a': r(t=t_vals, lambda_=lambda_a),
    'prob_b': r(t=t_vals, lambda_=lambda_b)
})

(ggplot() +
    geom_area(data=dat, mapping=aes(x='t', y='prob_b'),
              alpha=0.5, fill='darksalmon') +
    geom_area(data=dat, mapping=aes(x='t', y='prob_a'),
              alpha=0.75, fill='seagreen') +
    labs(x='Hours to Failure', y='Reliability (%)'))


(ggplot() +
    geom_area(data=dat, mapping=aes(x='t', y='prob_a', fill='"A"'), alpha=0.5) +
    geom_area(data=dat, mapping=aes(x='t', y='prob_b', fill='"B"'), alpha=0.5) +
    scale_fill_manual(values=['seagreen', 'darksalmon']))

(ggplot() +
    geom_line(data=dat, mapping=aes(x='t', y='prob_a', color='"A"'),
              alpha=0.5, size=1.5) +
    geom_line(data=dat, mapping=aes(x='t', y='prob_b', color='"B"'),
              alpha=0.5, size=1.5) +
    scale_color_manual(values=['seagreen', 'darksalmon']) +
    theme_classic())



# Failure Rate Function ##################################################
def z(t, lambda_):
    return dexp(t, lambda_) / (1 - pexp(t, lambda_))

z(t=0.5, lambda_=0.01)


# Q2. Let's write our failure function f(t) ###################################
def f(t, lambda_):
    return 1 - np.exp(-1 * lambda_ * t)


# Q3. Let's write our reliability function r(t) ###################################
def r(t, lambda_):
    return np.exp(-1 * lambda_ * t)

# Q4. Let's write our failure rate z(t) (hazard rate) ###################################
def z(t, lambda_):
    # density function / aka change in failure function
    return (
        lambda_ * np.exp(-1 * lambda_ * t) /
        # reliability function
        np.exp(-1 * lambda_ * t)
    )




# Q5. Test d(t), f(t), r(t), and z(t) ###################################
# over a span of 150 days (1 to 3600 hours)
# and visualize each with hist()

hours = np.arange(1, 3601)
hist(d(t=hours, lambda_=1/1200))

hist(f(t=hours, lambda_=1/1200))

hist(r(t=hours, lambda_=1/1200))

hist(z(t=hours, lambda_=1/1200))

# What do you notice?


# 2. Higher level Functions ###################################

# Sometimes, we make functions that USE functions inside them.
# Just make sure you either
# (1) put function A before function B, or
# (2) put function A INSIDE function B before using it


# We can re-write r(t) USING our function f(t)
def f(t, lambda_):
    return 1 - np.exp(-1 * lambda_ * t)

# Zero dependencies
def r(t, lambda_):
    return np.exp(-1 * lambda_ * t)
# I already defined f, so I can use it in my function
def r(t, lambda_):
    return 1 - f(t, lambda_)

# Heads up: the next three lines are SUPPOSED to fail. We throw f away, then
# ask r() to use it anyway. Run them and read the error - that is the whole
# point of rule (1) above.
del f, r
def r(t, lambda_):
    return 1 - f(t, lambda_)
# r(t=2, lambda_=0.001)   # NameError: f is not defined

def r(t, lambda_):
    return 1 - f(t, lambda_)




# Or we can embed f(t) in r(t)
def r(t, lambda_):
    # Write f(t)
    def f(t, lambda_):
        return 1 - np.exp(-1 * lambda_ * t)

    # Then calculate and return r(t)
    return 1 - f(t, lambda_)


# We can use embedded functions to create super functions, like h(t) and afr(t)
# The Python tutorial writes these with math.log / math.exp (scalars).

def f(t):
    return 1 - math.exp(-((t / 2000) ** 0.5))

def z(t, change=1):
    # Get change in failure function
    deltaf = (f(t + change) - f(t)) / change
    # Get reliability function
    r = 1 - f(t)
    # Get hazard rate
    return deltaf / r

def h(t):
    return -1 * math.log(1 - f(t))

def afr(t1, t2):
    r1 = 1 - f(t1)
    r2 = 1 - f(t2)
    h1 = -math.log(r1)
    h2 = -math.log(r2)
    return (h2 - h1) / (t2 - t1)

# % per 1000 hours
def pk(rate):
    return rate * 100 * 10**3

# PPM/1000 hours
def ppmk(rate):
    return rate * 10**9

# Hazard rate at t=10
z(10)
# Hazard rate per 1000 hours
pk(z(10))
# Average failure rate from 1000 to 10000 hours
afr(1000, 10000)
pk(afr(1000, 10000))


# Series vs. parallel reliability (Python tutorial, end of the chapter)
def r_exp(t, mean_time):
    return math.exp(-t / mean_time)

def series_reliability(t, means):
    rel = 1.0
    for m in means:
        rel *= r_exp(t, m)
    return rel

def parallel_reliability(t, means):
    prod_fail = 1.0
    for m in means:
        prod_fail *= (1 - r_exp(t, m))
    return 1 - prod_fail

print("Series reliability:", series_reliability(1000, [750, 900, 1200]))
print("Parallel reliability:", parallel_reliability(1000, [750, 900, 1200]))
