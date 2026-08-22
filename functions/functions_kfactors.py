# Import scipy functions
from scipy.stats import chi2
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

# Import helper functions from functions_distributions
# Note: These should be imported when the file is used
# from functions_distributions import runif, approxfun, density

def qk(p, r, time=False, failure=False):
    """
    k-factor Quantiles
    
    Function to return quantiles for k-factors.
    Intended for estimating confidence intervals for failure rates.
    
    Parameters:
    -----------
    p : float or array-like
        vector of probabilities / percentile(s)
    r : int
        number of failures (non-negative integers; can include zero)
    time : bool, default False
        logical; is case time-censored data?
    failure : bool, default False
        logical; is case failure-censored data?
    
    Returns:
    --------
    k : float or Series
        k-factor quantiles
    """
    # Testing values
    # p = 0.95; r = 20; time = False; failure = False
    
    # Convert p to numpy array for vectorized operations
    p = np.asarray(p)
    is_scalar = p.ndim == 0
    if is_scalar:
        p = np.array([p])
    
    # Input error handling
    if not (np.all(np.isreal(p)) and np.all((p >= 0) & (p <= 1))):
        raise ValueError("p must be numeric and between 0 and 1")
    if not (isinstance(r, (int, np.integer)) or (isinstance(r, float) and r.is_integer())):
        raise ValueError("r must be numeric and convertible to integer")
    r = int(r)
    if not isinstance(time, bool):
        raise ValueError("time must be logical (bool)")
    if not isinstance(failure, bool):
        raise ValueError("failure must be logical (bool)")
    if not ((time == True and failure == False) or 
            (time == False and failure == False) or 
            (time == False and failure == True)):
        raise ValueError("time and failure cannot both be True")
    if not ((r > 0) or (r == 0 and time == True)):
        raise ValueError("r must be > 0, or r == 0 and time == True")
    
    # Evaluate if p is in the upper or lower tail
    upper = p > 0.5
    
    # Does r == 0?
    zerofailures = (r == 0)
    
    # Initialize k array
    k = np.full(len(p), np.nan)
    
    # Apply conditional logic for each element
    for i in range(len(p)):
        p_val = p[i]
        upper_val = upper[i]
        
        if (zerofailures == False and time == False and failure == False and upper_val == True):
            # 1+ failures AND complete data AND UPPER tail --> Get k-factor for r as normal
            k[i] = chi2.ppf(p_val, df=2*r) / (2*r)
        elif (zerofailures == False and time == False and failure == False and upper_val == False):
            # 1+ failures AND complete data AND LOWER tail --> Get k-factor for r as normal
            k[i] = chi2.ppf(p_val, df=2*r) / (2*r)
        elif (zerofailures == False and time == True and failure == False and upper_val == True):
            # 1+ failures AND time-censored data AND UPPER tail --> Get k-factor for r+1
            k[i] = chi2.ppf(p_val, df=2*(r + 1)) / (2*r)
        elif (zerofailures == False and time == True and failure == False and upper_val == False):
            # 1+ failures AND time-censored data AND LOWER tail --> Get k-factor for r as normal
            k[i] = chi2.ppf(p_val, df=2*r) / (2*r)
        elif (zerofailures == False and time == False and failure == True and upper_val == True):
            # 1+ failures AND failure-censored (Type II) data AND UPPER tail
            # --> The 3-factor rule chi2.ppf(p, 2*((r-1)+1)) / (2*(r-1)) * (r-1)/r
            #     reduces algebraically to the complete-data formula, so use it directly.
            k[i] = chi2.ppf(p_val, df=2*r) / (2*r)
        elif (zerofailures == False and time == False and failure == True and upper_val == False):
            # 1+ failures AND failure-censored (Type II) data AND LOWER tail --> complete-data formula
            k[i] = chi2.ppf(p_val, df=2*r) / (2*r)
        elif (zerofailures == True and time == True and failure == False):
            # If zero failures --> then time-censored --> time = True, and upper/lower distinction doesn't matter.
            k[i] = -np.log(1 - p_val)
        else:
            # Otherwise, return NA.
            k[i] = np.nan
    
    if np.any(np.isnan(k)):
        print("At least 1 k-factor could not be calculated, due to improper inputs. Review the rules for time-censored, failure-censored, and zero-failure data.")
    
    # Return scalar if input was scalar, otherwise return Series
    if is_scalar:
        return float(k[0])
    else:
        return Series(k)


def rk(n, r, time=False, failure=False):
    """
    k-factor Random Deviates
    
    Get a random sample of k-factor values for simulating sampling distributions of failure rates.
    
    Parameters:
    -----------
    n : int
        number of observations
    r : int
        number of failures (non-negative integers; can include zero)
    time : bool, default False
        logical; is case time-censored data?
    failure : bool, default False
        logical; is case failure-censored data?
    
    Returns:
    --------
    k : Series
        random sample of k-factor values
    """
    # Testing values
    # n = 100; r = 20; time = False; failure = False
    
    # Import runif here to avoid circular imports
    import sys
    import os
    # Try to import from functions_distributions
    try:
        from functions_distributions import runif
    except ImportError:
        # If not available, define a simple runif
        from scipy.stats import uniform
        def runif(n, min=0, max=1):
            output = uniform.rvs(loc=min, scale=max, size=n)
            return Series(output)
    
    # Input error handling
    if not (isinstance(n, (int, np.integer)) or (isinstance(n, float) and n.is_integer())):
        raise ValueError("n must be numeric and convertible to integer")
    n = int(n)
    if n <= 0:
        raise ValueError("n must be > 0")
    if not isinstance(time, bool):
        raise ValueError("time must be logical (bool)")
    if not isinstance(failure, bool):
        raise ValueError("failure must be logical (bool)")
    if not ((time == True and failure == False) or 
            (time == False and failure == False) or 
            (time == False and failure == True)):
        raise ValueError("time and failure cannot both be True")
    
    # Does r == 0?
    zerofailures = (r == 0)
    
    # Generate a uniform distribution of percentiles p
    p_uniform = runif(n=n, min=0, max=1)
    
    # Return quantiles for the random percentiles
    k = qk(p=p_uniform, r=r, time=time, failure=failure)
    return k


def pk(q, r, time=False, failure=False):
    """
    k-factor Cumulative Distribution Function
    
    Function to return cumulative probabilities / percentiles given a supplied k-factor quantile `q`.
    Intended for confidence intervals for failure rates.
    
    Parameters:
    -----------
    q : float or array-like
        vector of quantiles (k-factors)
    r : int
        number of failures (non-negative integers; can include zero)
    time : bool, default False
        logical; is case time-censored data?
    failure : bool, default False
        logical; is case failure-censored data?
    
    Returns:
    --------
    p : float or Series
        cumulative probabilities / percentiles
    """
    # Testing values
    # q = 2; r = 20; time = False; failure = False
    
    # Import approxfun here to avoid circular imports
    try:
        from functions_distributions import approxfun
    except ImportError:
        from scipy.interpolate import interp1d
        def approxfun(data, fill_value='extrapolate', bounds_error=False):
            output = interp1d(data.x, data.y, kind='linear', fill_value=fill_value, bounds_error=bounds_error)
            return output
    
    # Convert q to numpy array for vectorized operations
    q = np.asarray(q)
    is_scalar = q.ndim == 0
    if is_scalar:
        q = np.array([q])
    
    # Construct an approximation function f, which gives the inverse of the Quantile Function,
    # such that you use linear interpolation to return a Probability for any Quantile supplied.
    by = 0.001
    p_range = np.concatenate([
        [by/10000, by/1000, by/100, by/10],
        np.arange(0, 1 + by, by),
        [1 - by/10, 1 - by/100, 1 - by/1000, 1 - by/10000]
    ])
    p_range = np.sort(p_range)
    
    # Get the quantiles for that range
    q_range = qk(p=p_range, r=r, time=time, failure=failure)
    
    # Convert to Series if needed for approxfun
    if isinstance(q_range, Series):
        q_range_values = q_range.values
    else:
        q_range_values = np.asarray(q_range)
    
    # Create DataFrame for approxfun
    data = DataFrame({'x': Series(q_range_values), 'y': Series(p_range)})
    
    # Get the inverse quantile function
    f = approxfun(data, fill_value='extrapolate', bounds_error=False)
    
    # Return the expected CDF for that quantile
    p = f(q)
    
    # Convert to Series if input was array-like, scalar if input was scalar
    if is_scalar:
        return float(p)
    else:
        return Series(p)


def dk(x, r, time=False, failure=False):
    """
    k-factor Probability Density Function
    
    Function to return probability densities given a supplied k-factor quantile `x`.
    Intended for visualizing sampling distributions of failure rates.
    
    Parameters:
    -----------
    x : float or array-like
        vector of quantiles (k-factors)
    r : int
        number of failures (non-negative integers; can include zero)
    time : bool, default False
        logical; is case time-censored data?
    failure : bool, default False
        logical; is case failure-censored data?
    
    Returns:
    --------
    d : float or Series
        probability densities
    """
    # Testing values
    # x = 2; r = 21; time = True; failure = False

    # The k-factor equals chi2(df) / (2*r), so its density has the exact closed
    # form 2*r * chi2.pdf(2*r*x, df) (and is 0 for x < 0, since the k-factor >= 0).
    # df follows the same rule as qk(): 2*r for complete or Type II
    # (failure-censored) data, 2*(r + 1) for time-censored data.

    # Convert x to numpy array for vectorized operations
    x = np.asarray(x, dtype=float)
    is_scalar = x.ndim == 0
    if is_scalar:
        x = np.array([x])

    # Input error handling (mirror qk())
    r = int(r)
    if not isinstance(time, bool):
        raise ValueError("time must be logical (bool)")
    if not isinstance(failure, bool):
        raise ValueError("failure must be logical (bool)")
    if not ((time and not failure) or (not time and not failure) or (not time and failure)):
        raise ValueError("time and failure cannot both be True")
    if not ((r > 0) or (r == 0 and time)):
        raise ValueError("r must be > 0, or r == 0 and time == True")

    if r == 0:
        # Zero failures (time-censored): the k-factor is Exponential(rate = 1)
        d = np.where(x >= 0, np.exp(-x), 0.0)
    else:
        # Degrees of freedom for the chi-squared numerator of the k-factor
        df = 2 * (r + 1) if time else 2 * r
        # Exact density (chi2.pdf returns 0 for negative arguments)
        d = 2 * r * chi2.pdf(2 * r * x, df=df)

    # Return scalar if input was scalar, otherwise return Series
    if is_scalar:
        return float(d[0])
    else:
        return Series(d)
