# What this file is ----------------------------------------------------------
#
# The five reliability functions for a part whose failures follow an
# exponential distribution: the chance it has failed by time t, the chance
# it is still working, the failure rate, the cumulative hazard, and the
# average failure rate across an interval.
#
# This is the Python twin of functions_reliability.R: the same five function
# names -- f(), r(), z(), h(), afr() -- and the same arguments, with one
# spelling change. Python reserves the word `lambda`, so the failure-rate
# argument is `lambda_` here (the spelling the Python chapters already use).
#
# Load it, from the top of the project folder:
#   import sys
#   sys.path.append("functions")
#   from functions_reliability import f, r, z, h, afr
#
# Then try:
#   r(t = 1000, lambda_ = 1/2000)   # chance a part survives to 1000 hours
#
# Like the other course helpers, every function returns a pandas Series,
# even for a single number.
#
# You never need to edit anything below.
#

import numpy as np
import pandas as pd


def _num(x):
    """Turn a number, list, numpy array or pandas Series into a float array."""
    return np.asarray(x, dtype=float)


def _series(x):
    """Wrap a result as a pandas Series, the way the other helpers return."""
    return pd.Series(np.atleast_1d(x))


# Failure Function
def f(t, lambda_):
  """
  Failure function F(t): the chance a part has failed by time t.

  Parameters:
    t: time(s), a number or a vector of numbers
    lambda_: failure rate (failures per unit of time)

  Returns:
    a pandas Series, 1 - exp(-lambda_ * t)
  """
  t, lambda_ = _num(t), _num(lambda_)
  return _series(1 - np.exp(-lambda_ * t))

# Example
# f(t = 365.25*24, lambda_ = 1/1200)

# Reliability Function
def r(t, lambda_):
  """
  Reliability function R(t): the chance a part is still working at time t.

  Parameters:
    t: time(s), a number or a vector of numbers
    lambda_: failure rate (failures per unit of time)

  Returns:
    a pandas Series, exp(-lambda_ * t), which is 1 - f(t, lambda_)
  """
  t, lambda_ = _num(t), _num(lambda_)
  return _series(np.exp(-lambda_ * t))

# Failure Rate Function
def z(t, lambda_):
  """
  Failure rate z(t): the density of failure divided by the reliability.

  The R version differentiates f() with mosaicCalc's D(); the derivative of
  1 - exp(-lambda * t) with respect to t is lambda * exp(-lambda * t), so this
  divides that by r(t, lambda_). For the exponential it is lambda_ at every t.

  Parameters:
    t: time(s), a number or a vector of numbers
    lambda_: failure rate (failures per unit of time)

  Returns:
    a pandas Series, f'(t) / r(t)
  """
  t, lambda_ = _num(t), _num(lambda_)
  fd = lambda_ * np.exp(-lambda_ * t)
  with np.errstate(divide = "ignore", invalid = "ignore"):
    output = fd / r(t, lambda_).to_numpy()
  return _series(output)

# Accumulative Hazard Function
def h(t, lambda_):
  """
  Cumulative hazard H(t): the failure rate added up from time 0 to t.

  Parameters:
    t: time(s), a number or a vector of numbers
    lambda_: failure rate (failures per unit of time)

  Returns:
    a pandas Series, -log(r(t, lambda_))
  """
  with np.errstate(divide = "ignore"):
    output = -np.log(r(t, lambda_).to_numpy())
  return _series(output)

# Average Failure Rate Function
def afr(t1, t2, lambda_):
  """
  Average failure rate between two times, t1 and t2.

  Parameters:
    t1: start time(s)
    t2: end time(s)
    lambda_: failure rate (failures per unit of time)

  Returns:
    a pandas Series, (h(t2) - h(t1)) / (t2 - t1)
  """
  top = h(t = t2, lambda_ = lambda_).to_numpy() - h(t = t1, lambda_ = lambda_).to_numpy()
  bottom = _num(t2) - _num(t1)
  return _series(top / bottom)
