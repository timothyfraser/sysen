# 04_recitation_solutions.py
# Tim Fraser
# Recitation 4: System reliability (worked solutions)
# Chapter: System Reliability in Python

######################################
# Load Packages
######################################
import numpy as np
import pandas as pd                     # data wrangling
import matplotlib.pyplot as plt         # visuals
from scipy.stats import expon           # the exponential distribution
import sympy as sp                      # symbolic calculus (our mosaicCalc)

# NOTE: `lambda` is a reserved word in Python (it makes anonymous functions),
# so everywhere R writes lambda = ..., we write rate = ..., exactly as the
# course's dexp() / pexp() functions do.

# NOTE: scipy's exponential is written in terms of a *scale*, where
# scale = 1 / rate. So:
#   R's dexp(t, rate = lambda)  -->  expon.pdf(t, scale = 1 / rate)
#   R's pexp(t, rate = lambda)  -->  expon.cdf(t, scale = 1 / rate)


###############################################
# 1. Reliability Calculations by TYPE of System
###############################################

# We also learned how to calculate reliability for a series vs. parallel system
# Quick Recap

# Series Systems:

# To get reliability of a Series of parts,
# multiply probability of reliability among each part, written R_1(t), R_2(t), etc. below
# R_series(t) = R_1(t) * R_2(t) * R_3(t) * .... * R_n(t)

# Parallel/Redundant System:

# To get reliability of a Parallel system of parts

# R_parallel(t) = 1 - (F_1(t) * F_2(t) * ... F_n(t) )
# or
# R_parallel(t) = 1 - (1 - R_1(t)) * (1 - R_2(t)) * ... (1 - R_n(t) )


# Q1. Nintendo made a new model of the Switch!
# (Hypothetically) each part (cord, screen, joystick A, joystick B)  has a specific failure rate, listed below.
# Calculate the overall probability that Nintendo's entire console DOESN'T fail after 1 hour

# 1 cord (1 / 5000 days)
# 1 screen (1 / 3000 days)
# 2 joysticks (1 / 2500 days)

cord = 1 / 5000
screen = 1 / 3000
joystick = 1 / 1000


def r(t, rate):
    return np.exp(-1 * rate * t)


print(
    r(t=1, rate=cord) *
    r(t=1, rate=joystick)**2 *
    r(t=1, rate=screen)
)


# Q2. Design a function to test console reliability for any time t.
# Test reliability after 1 hour, 24 hours, and 168 hours (7 days)
def nintendo(t):
    return (r(t, rate=cord) *
            r(t, rate=joystick)**2 *
            r(t, rate=screen))


print(nintendo(np.array([1, 24, 168])))

# Q3. Use your function to visualize the reliability curve
# for this overall system in matplotlib, as it ranges from 1 to 2000 hours!

# Let's make a DataFrame 's' for system
s = pd.DataFrame({'t': range(1, 2001)}).assign(
    p_n=lambda df: nintendo(df['t']),
    p_j=lambda df: r(df['t'], rate=joystick),
    p_c=lambda df: r(df['t'], rate=cord),
    p_s=lambda df: r(df['t'], rate=screen))

print(s.head())

# geom_area() in ggplot fills the space under a line;
# in matplotlib, that's fill_between().
plt.figure()
plt.fill_between(s['t'], s['p_c'], alpha=0.75, label="Cord")
plt.fill_between(s['t'], s['p_s'], alpha=0.75, label="Screen")
plt.fill_between(s['t'], s['p_j'], alpha=0.75, label="Joystick")
plt.fill_between(s['t'], s['p_n'], alpha=0.75, label="Overall")
plt.xlabel('t')
plt.ylabel('reliability')
plt.legend()
plt.show()


# What if the joysticks were a parallel system instead of a series? Maybe you only need one to function. #######################

def nintendo2(t):
    return (r(t, rate=cord) *
            (1 - (1 - r(t, rate=joystick)) * (1 - r(t, rate=joystick))) *
            r(t, rate=screen))


# Let's compare.
print(nintendo(t=100))
print(nintendo2(t=100))


######################################
# 2. Key Functions Recap
######################################

# Recently, we learned key failure/reliability functions in Python, using the exponential distribution!

# Let's write a few functions for this!
# We'll use expon.pdf() and expon.cdf() at the base of our functions, to reduce the likelihood of error :)

# Write function f(t), renamed d(t), to give our PDF for any time t
def d(t, rate):
    return expon.pdf(t, scale=1 / rate)


# Write failure function F(t) to give our CDF for any time t
def f(t, rate):
    return expon.cdf(t, scale=1 / rate)


# Write reliability function R(t) to give 1 - CDF for any time t
def r(t, rate):
    return 1 - expon.cdf(t, scale=1 / rate)


# Write failure rate function z(t) (aka hazard rate h(t)) to give PDF / (1 - CDF) for any time t
def z(t, rate):
    return expon.pdf(t, scale=1 / rate) / (1 - expon.cdf(t, scale=1 / rate))


# Write cumulative hazard rate function H(t), renamed h(t) for easy of coding
def h(t, rate):
    return -np.log(1 - expon.cdf(t, scale=1 / rate))


# Write average failure rate AFR(t1, t2), to show average rate of failure between times 1 and 2
# we'll reuse h(t) from above
def afr(t1, t2, rate):
    return (h(t2, rate) - h(t1, rate)) / (t2 - t1)


###################################
# 3. Calculus in Python
###################################

# R has the mosaicCalc package, which gives us D() to derive and antiD() to integrate.
# Python has sympy, which does the same job symbolically.
# Let's write ourselves D() and antiD() so the code reads the same way.

# our symbols - the letters sympy will do algebra with
t, x, z_, rate = sp.symbols('t x z rate', positive=True)


def D(expr, var):
    # the derivative of expr with respect to var,
    # handed back as a function of the letters expr contained
    args = sorted(expr.free_symbols, key=str)
    return sp.lambdify(args, sp.diff(expr, var), 'numpy')


def antiD(expr, var):
    # the antiderivative of expr with respect to var,
    # measured from 0 (just like mosaicCalc's antiD)
    args = sorted(expr.free_symbols, key=str)
    out = sp.integrate(expr, var)
    out = out - out.subs(var, 0)
    return sp.lambdify(args, out, 'numpy')


# It's written like...

# If I have function f(x) = x^2 + 2*x
# We can get the derivative...
derivative = D(x**2 + 2*x + z_**5, x)
# And use it as a function like this
print(derivative(np.arange(1, 6), 1))
# You could write it like this too:


def f(x, z):
    return x**2 + 2*x + z**5


# Then take the derivative of the function
derivative2 = D(f(x, z_), x)
# And get values like this!
print(derivative2(np.arange(1, 6), 1))

# We can get the integral...
integral = antiD(x**2 + 2*x + z_**5, x)
# And use it as a function like this.
print(integral(np.arange(1, 6), 1))
# Or if we wrote it as a function again...


def f(x, z):
    return x**2 + 2*x + z**5


# You could take the integral of the function!
integral2 = antiD(f(x, z_), x)
# And get values!
print(integral2(np.arange(1, 6), 1))


# Let's practice that a bit.

# Suppose we have our PDF function as d(t, rate)
def d(t, rate):
    return rate * np.exp(-1 * rate * t)


# and our CDF function as f(t, rate)
def f(t, rate):
    return 1 - np.exp(-1 * rate * t)


# so our reliability function is...
def r(t, rate):
    return np.exp(-1 * rate * t)


# The symbolic twins of those three, for sympy to chew on.
# (numpy's exp() can't do algebra; sympy's can.)
d_sym = rate * sp.exp(-1 * rate * t)
f_sym = 1 - sp.exp(-1 * rate * t)
r_sym = sp.exp(-1 * rate * t)

# Q1. Find the integral of d(). What does it equal?

fc = antiD(d_sym, t)
plt.figure()
plt.hist(fc(rate=1/1200, t=np.arange(1, 3601)))
plt.show()
# Compare with original
plt.figure()
plt.hist(f(t=np.arange(1, 3601), rate=1/1200))
plt.show()


# Q2. Find the derivative of f()
dc = D(f_sym, t)
plt.figure()
plt.hist(dc(rate=1/1200, t=np.arange(1, 3601)))
plt.show()
# Compare with original
plt.figure()
plt.hist(d(t=np.arange(1, 3601), rate=1/1200))
plt.show()


# Q3. Find the negative derivative of r()
dc2 = D(-1 * r_sym, t)
plt.figure()
plt.hist(dc2(rate=1/1200, t=np.arange(1, 3601)))
plt.show()
plt.figure()
plt.hist(d(np.arange(1, 3601), rate=1/1200))
plt.show()


# Q4. Find 1 - the integral of d()
fc = antiD(d_sym, t)
plt.figure()
plt.hist(1 - fc(rate=1/1200, t=np.arange(1, 3601)))
plt.show()
plt.figure()
plt.hist(r(np.arange(1, 3601), rate=1/1200))
plt.show()
