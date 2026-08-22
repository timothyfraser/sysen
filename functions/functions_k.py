# functions_k.py

"""
k-factor Functions for Python

This module provides Python equivalents of the k-factor functions from functions_k.R.
These functions are used for estimating confidence intervals and visualizing 
sampling distributions of failure rates.
"""

from scipy.stats import chi2
from numpy import log, array, isnan
from pandas import Series
import warnings

# Import utility functions from functions_distributions
from functions_distributions import runif, approxfun, density, tidy_density, seq


def qk(p, r, time=False, failure=False):
    """
    k-factor Quantiles
    
    Function to return quantiles for k-factors.
    Intended for estimating confidence intervals for failure rates.
    
    Parameters
    ----------
    p : array-like
        Vector of probabilities / percentile(s) (must be between 0 and 1)
    r : int
        Number of failures (non-negative integers; can include zero)
    time : bool, optional
        Logical; is case time-censored data? (default: False)
    failure : bool, optional
        Logical; is case failure-censored data? (default: False)
    
    Returns
    -------
    Series
        k-factor quantiles corresponding to the input probabilities
    
    Notes
    -----
    - time and failure cannot both be True
    - If r == 0, then time must be True
    - Returns NA values for invalid input combinations with a warning message
    """
    # Convert input to array for vectorized operations
    p = array(p)
    r = int(r)
    
    # Input error handling
    if not all((p >= 0) & (p <= 1)):
        raise ValueError("All probabilities p must be between 0 and 1")
    
    if not isinstance(r, int) or r < 0:
        raise ValueError("r must be a non-negative integer")
    
    if not isinstance(time, bool):
        raise ValueError("time must be a boolean")
    
    if not isinstance(failure, bool):
        raise ValueError("failure must be a boolean")
    
    # Check mutual exclusivity: time and failure cannot both be True
    if time and failure:
        raise ValueError("time and failure cannot both be True")
    
    # Check zero-failure condition
    if r == 0 and not time:
        raise ValueError("If r == 0, then time must be True")
    
    if r == 0 and failure:
        raise ValueError("If r == 0, then failure cannot be True")
    
    # Evaluate if p is in the upper or lower tail
    upper = p > 0.5
    
    # Does r == 0?
    zerofailures = (r == 0)
    
    # Initialize result array with NaN
    k = array([float('nan')] * len(p))
    
    # Apply conditional logic (equivalent to R's case_when)
    # Convert boolean arrays to conditions for each element
    for i in range(len(p)):
        if not zerofailures and not time and not failure and upper[i]:
            # 1+ failures AND complete data AND UPPER tail --> Get k-factor for r as normal
            k[i] = chi2.ppf(p[i], df=2*r) / (2*r)
        elif not zerofailures and not time and not failure and not upper[i]:
            # 1+ failures AND complete data AND LOWER tail --> Get k-factor for r as normal
            k[i] = chi2.ppf(p[i], df=2*r) / (2*r)
        elif not zerofailures and time and not failure and upper[i]:
            # 1+ failures AND time-censored data AND UPPER tail --> Get k-factor for r+1
            k[i] = chi2.ppf(p[i], df=2*(r + 1)) / (2*r)
        elif not zerofailures and time and not failure and not upper[i]:
            # 1+ failures AND time-censored data AND LOWER tail --> Get k-factor for r as normal
            k[i] = chi2.ppf(p[i], df=2*r) / (2*r)
        elif not zerofailures and not time and failure and upper[i]:
            # 1+ failures AND failure-censored data AND UPPER tail --> Get k-factor with adjustment
            k[i] = chi2.ppf(p[i], df=2*((r-1) + 1)) / (2 * (r-1)) * (r-1)/r
        elif not zerofailures and not time and failure and not upper[i]:
            # 1+ failures AND failure-censored data AND LOWER tail --> Get k-factor with r as normal
            k[i] = chi2.ppf(p[i], df=2*r) / (2*r)
        elif zerofailures and time and not failure:
            # If zero failures --> then time-censored --> time = TRUE, and upper/lower distinction doesn't matter.
            k[i] = -log(1 - p[i])
        else:
            # Otherwise, return NA.
            k[i] = float('nan')
    
    # Check for NA values and warn
    if any(isnan(k)):
        warnings.warn("At least 1 k-factor could not be calculated, due to improper inputs. Review the rules for time-censored, failure-censored, and zero-failure data.")
    
    return Series(k)


def rk(n, r, time=False, failure=False):
    """
    k-factor Random Deviates
    
    Get a random sample of k-factor values for simulating sampling distributions 
    of failure rates.
    
    Parameters
    ----------
    n : int
        Number of observations (must be positive integer)
    r : int
        Number of failures (non-negative integers; can include zero)
    time : bool, optional
        Logical; is case time-censored data? (default: False)
    failure : bool, optional
        Logical; is case failure-censored data? (default: False)
    
    Returns
    -------
    Series
        Random sample of k-factor values
    """
    # Input error handling
    n = int(n)
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
    if not isinstance(time, bool):
        raise ValueError("time must be a boolean")
    
    if not isinstance(failure, bool):
        raise ValueError("failure must be a boolean")
    
    # Check mutual exclusivity
    if time and failure:
        raise ValueError("time and failure cannot both be True")
    
    # Generate a uniform distribution of percentiles p
    p_uniform = runif(n=n, min=0, max=1)
    
    # Return quantiles for the random percentiles
    k = qk(p=p_uniform, r=r, time=time, failure=failure)
    return k


def pk(q, r, time=False, failure=False):
    """
    k-factor Cumulative Distribution Function
    
    Function to return cumulative probabilities / percentiles given a supplied 
    k-factor quantile `q`.
    Intended for confidence intervals for failure rates.
    
    Parameters
    ----------
    q : array-like
        Vector of quantiles (k-factors)
    r : int
        Number of failures (non-negative integers; can include zero)
    time : bool, optional
        Logical; is case time-censored data? (default: False)
    failure : bool, optional
        Logical; is case failure-censored data? (default: False)
    
    Returns
    -------
    Series
        Cumulative probabilities corresponding to the input quantiles
    """
    # Convert input to array
    q = array(q)
    
    # Construct an approximation function f, which gives the inverse of the Quantile Function,
    # such that you use linear interpolation to return a Probability for any Quantile supplied.
    by = 0.001
    p_range_list = [by/10000, by/1000, by/100, by/10]
    p_range_list.extend(seq(from_=0, to=1, by=by).tolist())
    p_range_list.extend([1 - by/10, 1 - by/100, 1 - by/1000, 1 - by/10000])
    p_range = sorted(p_range_list)
    
    # Get the quantiles for that range
    q_range = qk(p=p_range, r=r, time=time, failure=failure)
    
    # Remove NaN values for interpolation
    valid_mask = ~q_range.isna()
    q_range_clean = q_range[valid_mask]
    p_range_clean = [p_range[i] for i in range(len(p_range)) if valid_mask.iloc[i]]
    
    # Create DataFrame for approxfun (it expects x and y columns)
    from pandas import DataFrame
    data = DataFrame({'x': q_range_clean, 'y': p_range_clean})
    
    # Get the inverse quantile function
    # Note: R's approxfun with rule=2 means extrapolate, which is the default in Python's interp1d
    f = approxfun(data, fill_value='extrapolate', bounds_error=False)
    
    # Return the expected CDF for that quantile
    p = f(q)
    
    # Convert to Series if not already
    if not isinstance(p, Series):
        p = Series(p)
    
    return p


def dk(x, r, time=False, failure=False):
    """
    k-factor Probability Density Function
    
    Function to return probability densities given a supplied k-factor quantile `x`.
    Intended for visualizing sampling distributions of failure rates.
    
    Parameters
    ----------
    x : array-like
        Vector of quantiles (k-factors)
    r : int
        Number of failures (non-negative integers; can include zero)
    time : bool, optional
        Logical; is case time-censored data? (default: False)
    failure : bool, optional
        Logical; is case failure-censored data? (default: False)
    
    Returns
    -------
    Series
        Probability densities corresponding to the input quantiles
    """
    # Convert input to array
    x = array(x)
    
    # Construct a range of quantiles corresponding to a range of cumulative probabilities
    by = 0.001
    p_range_list = [by/10000, by/1000, by/100, by/10]
    p_range_list.extend(seq(from_=0, to=1, by=by).tolist())
    p_range_list.extend([1 - by/10, 1 - by/100, 1 - by/1000, 1 - by/10000])
    p_range = sorted(p_range_list)
    
    # Get the quantiles for that range
    q_range = qk(p=p_range, r=r, time=time, failure=failure)
    
    # Filter out NaN values for density estimation
    q_range_clean = q_range.dropna()
    
    # Fit a density curve to that quantile data
    # Note: R's density() with cut=c(0) truncates at 0, but Python's gaussian_kde
    # doesn't have this option. We'll use the standard density() function.
    model = density(q_range_clean)
    
    # Get tidy density DataFrame with x and y columns
    density_df = tidy_density(model, n=1000)
    
    # Approximate a function using the density curve's x and y values
    f = approxfun(density_df, fill_value='extrapolate', bounds_error=False)
    
    # Estimate density
    d = f(x)
    
    # Convert to Series if not already
    if not isinstance(d, Series):
        d = Series(d)
    
    return d

