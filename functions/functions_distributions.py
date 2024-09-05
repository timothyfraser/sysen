# Import scipy functions
# !pip install scipy
from scipy.stats import norm, expon, gamma, weibull_min, poisson, uniform, binom

# Simple visualization #############################

# Want to make a quick histogram?
def hist(x):
  """
  Make a quick histogram, in syntax matching the method in R.
  
  Parameters:
    x: a pandas Series of values to be turned into a histogram
    
  Returns: 
    figure: a ggplot figure object.
  """
  from plotnine import ggplot, geom_histogram, aes
  output = ggplot(aes(x = x)) + geom_histogram()
  return output

# Skewness & Kurtosis ##############################
def skewness(x):
    from pandas import Series
    x = Series(x)
    diff = x - x.mean()
    n = len(x) - 1
    sigma = x.std()
    output = sum(diff**3) / (n * sigma**3)
    return output

def kurtosis(x):
    from pandas import Series
    x = Series(x)
    diff = x - x.mean()
    n = len(x) - 1
    sigma = x.std()
    output = sum(diff**4) / (n * sigma**4)
    return output


# Probability Distribution Functions ####################

# Sequence function, matching syntax of R
def seq(from_, to, length_out=None, by=None):
    import pandas as pd
    
    if length_out is not None and by is not None:
        raise ValueError("Only one of `length_out` or `by` should be provided.")
    
    # Generate sequence based on `length_out`
    if length_out is not None:
        if length_out < 1:
            raise ValueError("`length_out` must be at least 1.")
        # Use pandas' `pd.Series` and `linspace` to generate the sequence
        sequence = pd.Series(pd.Series(range(length_out)).apply(lambda x: from_ + (to - from_) * x / (length_out - 1)))
    
    # Generate sequence based on `by`
    elif by is not None:
        if by == 0:
            raise ValueError("`by` must be non-zero.")
        # Use pandas' `pd.Series` and `range` to generate the sequence
        sequence = pd.Series(range(int((to - from_) / by) + 1)).apply(lambda x: from_ + x * by)
    
    else:
        raise ValueError("Either `length_out` or `by` must be provided.")
    
    return sequence

# It works!
# seq(0,1,length_out = 10)
# seq(-3,1,by = 0.1)



# We can build ourself the PDF of our lifetime distribution here
def density(x):
  from scipy.stats import gaussian_kde as density
  output = density(x)
  return output

def tidy_density(model, n = 1000):
  # Estimate density using a Gaussian KDE
  from numpy import linspace
  from pandas import Series, DataFrame
  # Get linerange
  values = linspace(start = model.dataset.min(), stop = model.dataset.max(), num = n)
  # Get density values
  densities = model(values)
  # Create a tidy dataframe of x and density values
  output = DataFrame({'x': Series(values), 'y': Series(densities) })
  return output 

def approxfun(data, fill_value='extrapolate',bounds_error=False):
  # Approximate a data.frame of x and y data into a function
  from scipy.interpolate import interp1d
  output = interp1d(data.x, data.y, kind='linear', fill_value=fill_value, bounds_error = bounds_error)
  return output

## Euler's number
def exp(x = 1):
  from numpy import exp
  output = exp(x)
  return output

## Normal Distribution ##########################
def dnorm(x, mean=0, sd=1):
    from scipy.stats import norm
    from pandas import Series
    output = norm.pdf(x, loc=mean, scale=sd)
    output = Series(output)
    return output

def pnorm(x, mean=0, sd=1):
    from scipy.stats import norm
    from pandas import Series
    output = norm.cdf(x, loc=mean, scale=sd)
    output = Series(output)
    return output
  
def qnorm(x, mean=0, sd=1):
    from scipy.stats import norm
    from pandas import Series
    return norm.ppf(x, loc=mean, scale=sd)

def rnorm(n, mean=0, sd=1):
    from scipy.stats import norm
    from pandas import Series
    output = norm.rvs(loc = mean, scale = sd, size=n)
    output = Series(output)
    return output

## Exponential Distribution ##########################
def dexp(x, rate = 0.01):
    from scipy.stats import expon
    from pandas import Series
    output = expon.pdf(x, loc=0, scale=1/rate)
    output = Series(output)
    return output

def pexp(x, rate = 0.01):
    from scipy.stats import expon
    from pandas import Series
    output = expon.cdf(x, loc=0, scale=1/rate)
    output = Series(output)
    return output

def qexp(x, rate = 0.01):
    from scipy.stats import expon
    from pandas import Series
    output = expon.ppf(x, loc=0, scale=1/rate)
    output = Series(output)
    return output

def rexp(n, rate = 0.01):
    from scipy.stats import expon
    from pandas import Series
    output = expon.rvs(loc=0, scale=1/rate, size = n)
    output = Series(output)
    return output

## Weibull Distribution ##########################
def dweibull(x, shape = 2, scale = 1):
    from scipy.stats import weibull_min
    from pandas import Series
    output = weibull_min.pdf(x, c = shape, scale = scale)
    output = Series(output)
    return output
def pweibull(x, shape = 2, scale = 1):
    from scipy.stats import weibull_min
    from pandas import Series
    output =  weibull_min.cdf(x, c = shape, scale = scale)
    output = Series(output)
    return output
def qweibull(x, shape = 2, scale = 1):
    from scipy.stats import weibull_min
    from pandas import Series
    output =  weibull_min.ppf(x, c = shape, scale = scale)
    output = Series(output)
    return output
def rweibull(n, shape = 2, scale = 1):
    from scipy.stats import weibull_min
    from pandas import Series
    output =  weibull_min.rvs(c = shape, scale = scale, size = n)
    output = Series(output)
    return output

## Gamma Distribution ##########################
def dgamma(x, shape = 2, rate = 1):
    from scipy.stats import gamma
    from pandas import Series
    output = gamma.pdf(x, a = shape, scale = 1/rate)
    output = Series(output)
    return output
def pgamma(x, shape = 2, rate = 1):
    from scipy.stats import gamma
    from pandas import Series
    output = gamma.cdf(x, a = shape, scale = 1/rate)
    output = Series(output)
    return output

def qgamma(x, shape = 2, rate = 1):
    from scipy.stats import gamma
    from pandas import Series
    output = gamma.ppf(x, a = shape, scale = 1/rate)
    output = Series(output)
    return output
def rgamma(n, shape = 2, rate = 1):
    from scipy.stats import gamma
    from pandas import Series
    output = gamma.rvs(a = shape, scale = 1/rate, size=n)
    output = Series(output)
    return output

## Poisson Distribution ##########################
def dpois(x, mu = 1):
    from scipy.stats import poisson
    from pandas import Series
    output = poisson.pmf(x, mu=mu)
    output = Series(output)
    return output
def ppois(x, mu = 1):
    from scipy.stats import poisson
    from pandas import Series
    output = poisson.cdf(x, mu=mu)
    output = Series(output)
    return output
def qpois(x, mu = 1):
    from scipy.stats import poisson
    from pandas import Series
    output = poisson.ppf(x, mu=mu)
    output = Series(output)
    return output
def rpois(n, mu = 1):
    from scipy.stats import poisson
    from pandas import Series
    output = poisson.rvs(mu = mu, size = n)
    output = Series(output)
    return output

## Binomial Distribution ##########################
def dbinom(x, size = 1, prob = 0.5):
    from scipy.stats import binom
    from pandas import Series
    output = binom.pmf(x, n=size, p=prob)
    output = Series(output)
    return output
def pbinom(x, size = 1, prob = 0.5):
    from scipy.stats import binom
    from pandas import Series
    output = binom.cdf(x, n=size, p=prob)
    output = Series(output)
    return output
def qbinom(x, size = 1, prob = 0.5):
    from scipy.stats import binom
    from pandas import Series
    output = binom.ppf(x, n=size, p=prob)
    output = Series(output)
    return output
def rbinom(n, size = 1, prob = 0.5):
    from scipy.stats import binom
    from pandas import Series
    output = binom.rvs(n=size, p=prob, size = n)
    output = Series(output)
    return output

## Uniform Distribution ##########################
def dunif(x, min=0, max=1):
    from scipy.stats import uniform
    from pandas import Series
    output = uniform.pdf(x, loc=min, scale=max)
    output = Series(output)
    return output
def punif(x, min=0, max=1):
    from scipy.stats import uniform
    from pandas import Series
    output = uniform.cdf(x, loc=min, scale=max)
    output = Series(output)
    return output
def qunif(x, min=0, max=1):
    from scipy.stats import uniform
    from pandas import Series
    output = uniform.ppf(x, loc=min, scale=max)
    output = Series(output)
    return output
def runif(n, min=0, max=1):
    from scipy.stats import uniform
    from pandas import Series
    output = uniform.rvs(loc=min, scale=max, size = n)
    output = Series(output)
    return output
