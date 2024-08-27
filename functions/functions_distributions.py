# Import scipy functions
# !pip install scipy
from scipy.stats import norm, expon, gamma, weibull_min, poisson, uniform, binom

# Probability Distribution Functions ####################

## Normal Distribution ##########################
def dnorm(x, mean=0, sd=1):
    return norm.pdf(x, loc=mean, scale=sd)
def pnorm(x, mean=0, sd=1):
    return norm.cdf(x, loc=mean, scale=sd)
def qnorm(x, mean=0, sd=1):
    return norm.ppf(x, loc=mean, scale=sd)
def rnorm(n, mean=0, sd=1):
    return norm.rvs(loc = mean, scale = sd, size=n)

## Exponential Distribution ##########################
def dexp(x, rate = 0.01):
    return expon.pdf(x, loc=0, scale=1/rate)
def pexp(x, rate = 0.01):
    return expon.cdf(x, loc=0, scale=1/rate)
def qexp(x, rate = 0.01):
    return expon.ppf(x, loc=0, scale=1/rate)
def rexp(n, rate = 0.01):
    return expon.rvs(loc=0, scale=1/rate, size = n)

## Weibull Distribution ##########################
def dweibull(x, shape = 2, scale = 1):
  return weibull_min.pdf(x, c = shape, scale = scale)
def pweibull(x, shape = 2, scale = 1):
  return weibull_min.cdf(x, c = shape, scale = scale)
def qweibull(x, shape = 2, scale = 1):
  return weibull_min.ppf(x, c = shape, scale = scale)
def rweibull(n, shape = 2, scale = 1):
  return weibull_min.rvs(c = shape, scale = scale, size = n)

## Gamma Distribution ##########################
def dgamma(x, shape = 2, rate = 1):
  return gamma.pdf(x, a = shape, scale = 1/rate)
def pgamma(x, shape = 2, rate = 1):
  return gamma.cdf(x, a = shape, scale = 1/rate)
def qgamma(x, shape = 2, rate = 1):
  return gamma.ppf(x, a = shape, scale = 1/rate)
def rgamma(n, shape = 2, rate = 1):
  return gamma.rvs(a = shape, scale = 1/rate, size=n)

## Poisson Distribution ##########################
def dpois(x, mu = 1):
  return poisson.pmf(x, mu=1)
def ppois(x, mu = 1):
  return poisson.cdf(x, mu=1)
def qpois(x, mu = 1):
  return poisson.ppf(x, mu=1)
def rpois(n, mu = 1):
  return poisson.rvs(mu = 1, size = n)

## Binomial Distribution ##########################
def dbinom(x, size = 1, prob = 0.5):
  return binom.pmf(x, n=size, p=prob)
def pbinom(x, size = 1, prob = 0.5):
  return binom.cdf(x, n=size, p=prob)
def qbinom(x, size = 1, prob = 0.5):
  return binom.ppf(x, n=size, p=prob)
def rbinom(n, size = 1, prob = 0.5):
  return binom.rvs(n=size, p=prob, size = n)

## Uniform Distribution ##########################
def dunif(x, min=0, max=1):
  return uniform.pdf(x, loc=min, scale=max)
def punif(x, min=0, max=1):
  return uniform.cdf(x, loc=min, scale=max)
def qunif(x, min=0, max=1):
  return uniform.ppf(x, loc=min, scale=max)
def runif(n, min=0, max=1):
  return uniform.rvs(loc=min, scale=max, size = n)
