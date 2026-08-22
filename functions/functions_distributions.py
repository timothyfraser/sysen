# Import scipy functions
# !pip install scipy
from scipy.stats import norm, expon, gamma, weibull_min, poisson, uniform, binom, chi2
import pandas as pd

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

## Chi-Squared Goodness-of-Fit Test ##########################
def get_chisq(t=None, binwidth=5, data=None, n_total=None, f=None, np=1, **kwargs):
    """
    Function to Get Chi-Squared!
    
    If observed vector...
    t: a vector of times to failure
    binwidth: size of intervals (eg. 5 hours) (Only if t is provided)
    If cross-tabulated data...
    data: a DataFrame with the vectors 'lower', 'upper', and 'r_obs'
    Common Parameters:
    n_total: total number of units.
    f: specific failure function, such as f = f(t, lambda)
    np: total number of parameters in your function (eg. if exponential, 1 (lambda))
    **kwargs: fill in here any named parameters you need, like lambda=2.4 or rate=2.3 or mean=0, sd=2
    """
    
    # If vector `t` is NOT None
    # Do the raw data route
    if t is not None:
        # Make a DataFrame called 'tab'
        tab = pd.DataFrame({'t': t})
        # Part 1.1: Split into bins
        # Create all bins first (including empty ones)
        max_t = int(tab['t'].max())
        bins = list(range(0, max_t + binwidth + 1, binwidth))
        tab['interval'] = pd.cut(tab['t'], bins=bins, right=True, include_lowest=True, precision=0)
        
        # Fix the first interval label to show (0, binwidth] instead of (-0.001, binwidth]
        cats = list(tab['interval'].cat.categories)
        if len(cats) > 0:
            first_cat_str = str(cats[0])
            if first_cat_str.startswith('(-'):
                upper = first_cat_str.split(', ')[1]
                new_first = f'(0, {upper}'
                rename_map = {cats[0]: new_first}
                tab['interval'] = tab['interval'].cat.rename_categories(rename_map)
        
        # Part 1.2: Tally up observed failures 'r_obs' by bin
        # Get all interval categories (including empty bins)
        all_categories = tab['interval'].cat.categories
        
        # Count observations per bin
        tab_grouped = tab.groupby('interval', dropna=False, observed=True).size().reset_index(name='r_obs')
        
        # Create a DataFrame with all categories and merge counts (filling 0 for empty bins)
        tab = pd.DataFrame({'interval': pd.Categorical(all_categories, categories=all_categories)})
        tab = tab.merge(tab_grouped, on='interval', how='left')
        tab['r_obs'] = tab['r_obs'].fillna(0).astype(int)
        
        # Add bin information first (so we can sort by bin number)
        tab['bin'] = range(1, len(tab) + 1)  # 1-based indexing like R
        tab['lower'] = (tab['bin'] - 1) * binwidth
        tab['upper'] = tab['bin'] * binwidth
        tab['midpoint'] = (tab['lower'] + tab['upper']) / 2
        
        # Sort by bin number (which is already in order, but ensures consistency)
        tab = tab.sort_values('bin').reset_index(drop=True)
        
    # Otherwise, if DataFrame `data` is NOT None
    # Do the cross-tabulated data route
    elif data is not None:
        tab = data.copy()
        tab['bin'] = range(1, len(tab) + 1)
        tab['midpoint'] = (tab['lower'] + tab['upper']) / 2
    else:
        raise ValueError("Either 't' or 'data' must be provided")
    
    # Part 2. Calculate probabilities by interval
    tab['p_upper'] = f(tab['upper'], **kwargs)
    tab['p_lower'] = f(tab['lower'], **kwargs)
    tab['p_fail'] = tab['p_upper'] - tab['p_lower']
    tab['n_total'] = n_total
    tab['r_exp'] = tab['n_total'] * tab['p_fail']
    
    # Part 3-4: Calculate Chi-Squared statistic and p-value
    chisq = ((tab['r_obs'] - tab['r_exp'])**2 / tab['r_exp']).sum()
    nbin = len(tab)
    df = nbin - np - 1
    p_value = chi2.sf(x=chisq, df=df)
    
    output = pd.DataFrame({
        'chisq': [chisq],
        'nbin': [nbin],
        'np': [np],
        'df': [df],
        'p_value': [p_value]
    })
    
    return output