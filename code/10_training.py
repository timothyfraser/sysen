# 10_training.py
# Training: Statistical Process Control
# Pairs with R training:
# https://timothyfraser.com/sigma/indices-and-confidence-intervals-for-statistical-process-control-in-r.html#process-capability-vs.-stability
# Tim Fraser

# Getting Started #################################

# This workshop extends our toolkit developed in the previous training, 
# discussing Process Capability and Stability Indices, 
# and introducing means to calculate confidence intervals for these indices.


## Install Packages ############################
# Install main python packages for this script
# !pip install pandas
# !pip install sympy
# !pip install math
# !pip install plotnine
# !pip install os
# !pip install sys
# !pip install patchworklib

## Load Packages ############################
import pandas as pd # Import pandas functions
from plotnine import * # import all plotnine visualization functions
import os
import sys
# Append files in this folder (functions) to the Python Path
sys.path.append(os.path.abspath('functions'))
# Now you can reference them directly
from functions_distributions import *
# Import math functions
import math


# Our Data #######################

# We’ll be continuing to analyze our quality control data
# from a local hot springs inn (onsen) in sunny Kagoshima
# Prefecture, Japan. Every month, for 15 months, you systematically
# took 20 random samples of hot spring water and
# recorded its temperature, pH, and sulfur levels. How
# might you determine if this onsen is at risk of
# slipping out of one sector of the market (eg. Extra
# Hot!) and into another (just normal Hot Springs?).

# Let’s read in our data from workshops/onsen.csv!

# Let's import our samples of bathwater over time!
water = pd.read_csv('workshops/onsen.csv')
water.head()
water.info()


# Our dataset contains:
# 
# id: unique identifer for each sample of onsen water.
# 
# time: categorical variable describing date of sample
#     (month 1, month 3, … month 15).
# 
# temp: temperature in celsius.
# 
# ph: pH (0 to 14)
# 
# sulfur: milligrams of sulfur ions.




# 10.1 Process Capability vs. Stability

# 10.1.1 Definitions

# Production processes can be categorized in terms of Capability
# (does it meet required specifications?) and Stability (is
# production consistent and predictable?) Both are vital.
# 
# A capable process delivers goods that can actually perform
# their function, like a 20-foot ladder that is actually 20
# feet!
# 
# A stable process delivers products with consistent and
# predictable traits (regardless of whether those traits are
# good).
# 
# We need to maximize both process capability and stability
# to make an effective process, be it in manufacturing, health
# care, local businesses, or social life! Depending on the
# shape and stability of our data, we should choose one of the
# 4 statistics to evaluate our data.


# 10.1.2 Table of Indices

# These statistics rely on some combination of (1) the mean
# μ, (2) the standard deviation σ, and (3) the upper and lower
# “specification limits”; the specification limits are our expected
# values E_upper and E_lower, as compared to our actual observed
# values, summarized by μ and σ.

# See table:
# https://timothyfraser.com/sigma/indices-and-confidence-intervals-for-statistical-process-control-in-r.html#table-of-indices




# 10.2 Index Functions

# Let’s do ourselves a favor and write up some simple functions for these.

# Capability Index (for centered, normal data)
def cp(sigma_s, upper, lower):
    return abs(upper - lower) / (6 * sigma_s)

# Process Performance Index (for centered, normal data)
def pp(sigma_t, upper, lower):
    return abs(upper - lower) / (6 * sigma_t)

# Capability Index (for skewed, uncentered data)
def cpk(mu, sigma_s, lower=None, upper=None):
    # Testing values
    # sigma_s = stat.sigma_s; mu = stat.xbbar; lower = 42; upper = None

    a, b = None, None
    
    # If lower is provided, calculate 'a'
    if lower is not None:
        a = abs(mu - lower) / (3 * sigma_s)
    
    # If upper is provided, calculate 'b'
    if upper is not None:
        b = abs(upper - mu) / (3 * sigma_s)
    
    # If both lower and upper are provided, return the minimum of a and b
    if lower is not None and upper is not None:
        return min(a, b)
    
    # If only upper is provided, return b
    elif lower is None and upper is not None:
        return b
    
    # If only lower is provided, return a
    elif upper is None and lower is not None:
        return a

# Example of usage
cpk(mu=5, sigma_s=2, lower=3, upper=7)
cpk(mu=5, sigma_s=2, lower=3, upper=None)
cpk(mu=5, sigma_s=2, lower=None, upper=3)
cpk(mu=pd.Series(5), sigma_s=pd.Series(2), lower=None, upper=3)


def ppk(mu, sigma_t, lower=None, upper=None):
    
    a, b = None, None
    
    # If lower is provided, calculate 'a'
    if lower is not None:
        a = abs(mu - lower) / (3 * sigma_t)
    
    # If upper is provided, calculate 'b'
    if upper is not None:
        b = abs(upper - mu) / (3 * sigma_t)
    
    # If both lower and upper are provided, return the minimum of a and b
    if lower is not None and upper is not None:
        return min(a, b)
    
    # If only upper is provided, return b
    elif lower is None and upper is not None:
        return b
    
    # If only lower is provided, return a
    elif upper is None and lower is not None:
        return a

# Example of usage
ppk(mu=5, sigma_t=1.5, lower=2, upper=8)

# How might we use these indices to describe our process data?
# For example, recall that our onsen operator needs to be
# sure that their hot springs water is consistently falling
# into the temperature bins for Extra Hot Springs, which start
# at 42 degrees Celsius (and go as high as 80). Let’s use
# those as our specification limits (pretty easy-going limits,
# I might add).

# Let’s start by calculating our quantities of interest.

# Calculate these statistics of interest!
stat_s = water.groupby('time').apply(lambda g: pd.Series({
  # Return each time
  'time': g['time'].values[0],
  # within group mean
  'xbar': g['temp'].mean(),
  # within group standard deviation
  'sd': g['temp'].std(),
  # within group sample size n
  'nw': g['temp'].count()
}))

# To get between-group estimates....
stat = pd.DataFrame({
  'xbbar': [ stat_s.xbar.mean() ], # get grand mean
  'sigma_s': (sum(stat_s.sd**2) / len(stat_s.sd**2))**0.5, # get sigma_short
  'sigma_t': water.temp.std(),    # get sigma_t
  'n': stat_s.nw.sum(), # total observations
  'n_w': stat_s.nw.unique(), # size of subgroups
  'k': stat_s.shape[0] # number of subgroups
})
# Check it!
stat


# 10.2.1 Capacity Index C_p

# Our C_p Capacity index says, assuming that the distribution
# is centered and stable, how many times wider are our
# limits than our approximate observed distribution (6σ_short)?

mycp = cp(sigma_s = stat.sigma_s.values, lower = 42, upper = 80)
mycp

# Great! This says, our observed variation is many times 
# (3.1887098 times) narrower than the expected specification limits.


# 10.2.2 Process Performance Index P_p


# Our P_p Process Performance Index asks, even if the
# distribution is not stable (meaning it varies not just due
# to common causes), how many times wider are our specification
# limits than our approximate observed distribution (6σ_total)?

mypp = pp(sigma_t = stat.sigma_t.values, lower = 42, upper = 80)
mypp

# Much like before, the specification limit range remains
# quite bigger than the observed distribution.




# 10.2.3 Capacity Index C_pk

# Our C_pk Capacity index says, assuming the distribution
# is pretty stable across subgroups, how many times wider is
# (a) the distance from the tail of interest to the mean
# than (b) our approximate observed tail (3 sigma)? This
# always looks at the shorter tail.
 
mycpk = cpk(mu=stat.xbbar.values, sigma_s = stat.sigma_s.values, lower = 42, upper = 80)

# If we only care about one of the tails, eg. the lower
# specification limit of 42, which is much closer than the
# upper limit of 80, we can just write the lower limit only.
 
cpk(sigma_s = stat.sigma_s.values, mu = stat.xbbar.values, lower = 42)

# This says, our observed variation is much wider than the
# lower specification limit, since C_pk is far from 1,
# which shows equality.

# 10.2.4 Process Performance Index P_pk

# Our P_pk process performance index says, even if the
# distribution is neither stable nor centered, how much
# wider is the observed variation (3σ_total) than the
# distance from the tail of interest to the mean? We use
# σ_total here to account for instability (considerable
# variation between subgroups) and one-tailed testing to
# account for the uncentered distribution.
# 
myppk = ppk(sigma_t = stat.sigma_t.values, mu = stat.xbbar.values, lower = 42, upper = 80)
myppk

 
# 10.2.5 Equality

# A final reason why these quantities are neat is that
# these 4 indices are related; if you know 3 of them, we
# can always calculate the 4th! See the identity below:
# 
# P_p × C_pk = P_pk × C_p
# 
# whaaaaaat? They're equal!!!!
mypp * mycpk == myppk * mycp



# Learning Check 1

# Question
# 
# Let’s apply this to some tasty examples! A manufacturer
# of granola bars is aiming for a weight of 2 ounces
# (oz), plus or minus 0.5 oz. Suppose the standard
# deviation of our granola bar machine is 0.02 oz, and
# the mean weight is 2.01 oz.
# 
# What’s the process capability index? (I.e. How many times
# greater is the expected variation than the observed
# variation?)

lower = 2 + 0.05
upper = 2 - 0.05
sigma = 0.02
mu = 2.01

cp(sigma_s= 0.02, upper = 2.05, lower = 1.95)

cpk(mu = 2.01, sigma_s = 0.02, lower = 1.95, upper = 2.05)



# 10.3 Confidence Intervals

# Any statistic is really just 1 of the many possible values
# of statistics you could have gotten from your sample, had
# you taken just a slightly different random sample. So,
# when we calculate our indices, we should be prepared that
# our indices might vary due to chance (sampling error), so
# we should build in confidence intervals. This helps us
# benchmark how trustworthy any given index is.

# 10.3.1 Confidence Intervals show us Sampling Distributions
# Let’s quickly go over what confidence intervals are trying
# to show us!
# 
# Suppose we take a statistic like the mean μ to describe
# our vector temp.

water.temp.mean()

# We might have gotten a slightly different statistic had we
# had a slightly different sample. We can approximate what
# slightly different sample might look like by using
# bootstrapped resamples. This means, randomly sampling a
# bunch of observations from our dataframe water, sometimes
# taking the same observation multiple times, sometimes
# leaving out some observations by chance. We can use the
# sample(x, size = ..., replace = TRUE) function to take
# a bootstrapped sample.


# Bootstrapping and calculating the mean
water['temp'].sample(n=len(water), replace=True).mean()


# Get a vector of ids from 1 to 1000
myboot = pd.DataFrame({'rep': list(range(1,1000))})
# For each replicate,
# Get a random bootstrapped sample of temperatures
myboot['boot'] =  [water['temp'].sample(n=len(water), replace=True).mean() for _ in myboot.rep]

# View them!
hist(myboot.boot)


# We can see above the latent distribution of 1000 statistics
# we could have gotten due to random sampling error. This
# is called a sampling distribution. Whenever we make
# confidence intervals, we are always drawing from a sampling
# distribution.

 
# 10.3.2 Bootstrapped or Theoretical Sampling Distributions?

# The question is, are you relying on a bootstrapped sampling
# distribution or a theoretical sampling distribution?
# 
# If we assume a perfectly normal distribution, then we’re
# relying on a theoretical sampling distribution, and we need
# formulas to calculate our confidence intervals. This is a
# big assumption!
# 
# If we are comfortable with computing 1000 or more replicates,
# then we can bootstrap those confidence intervals instead,
# gaining accuracy at the expense of computational power.
# 
# Let’s learn how to make confidence intervals for our indices
# from (1) a theoretical sampling distribution, and then we’ll
# learn to make them from (2) a bootstrapped sampling
# distribution.

# 10.3.3 Confidence Intervals with Theoretical Sampling

# Distributions
# Suppose our lower and upper specification limits - the
# expectations of the market and/or regulators - are that our
# onsen’s temperature should be between 42 and 50 degrees
# Celsius if we advertise ourselves as an Extra Hot Onsen.
# 
# For any index, you’ll need to get the ingredients needed to
# calculate the index and to calculate its standard error (the
# standard deviation of the sampling distribution you’re trying
# to approximate).
# 
# So, let’s first get our ingredients…


# Calculate these statistics of interest!
stat_s = water.groupby('time').apply(lambda g: pd.Series({
  # Return each time
  'time': g['time'].values[0],
  # within group mean
  'xbar': g['temp'].mean(),
  # within group standard deviation
  'sd': g['temp'].std(),
  # within group sample size n
  'nw': g['temp'].count()
}))

# To get between-group estimates....
stat = pd.DataFrame({
  'xbbar': [ stat_s.xbar.mean() ], # get grand mean
  'sigma_s': (sum(stat_s.sd**2) / len(stat_s.sd**2))**0.5, # get sigma_short
  'sigma_t': water.temp.std(),    # get sigma_t
  'n': stat_s.nw.sum(), # total observations
  'n_w': stat_s.nw.unique(), # size of subgroups
  'k': stat_s.shape[0] # number of subgroups
})
# Check it!
stat


# Now, let’s calculate our Capability Index C_p,
# which assumes a process centered between the upper
# and lower specification limits and a stable process.


# Capability Index (for centered, normal data)
def cp(sigma_s, upper, lower):
    return abs(upper - lower) / (6 * sigma_s)



bands = pd.DataFrame({
  'limit_lower': pd.Series(42),
  'limit_upper': pd.Series(50)
})

bands['estimate'] = cp(sigma_s = stat.sigma_s, lower = bands.limit_lower, upper = bands.limit_upper)

bands # view

# That was surprisingly painless!
# 
# Now, let’s estimate the two-sided, 95% confidence interval
# of our sampling distribution for the statistic c_p,
# assuming that this sampling distribution has a normal shape.
# 
# We’re getting the interval that spans 95%, so it’s got
# to start at 2.5% and end at 97.5%, covering the 95%
# most frequently occurring statistics in the sampling
# distribution.

# Get extra quantities of interest...
# degrees of freedom
bands['v_short'] = stat.k*(stat.n_w - 1) 
# standard error
bands['se'] = bands.estimate * (1 / (2*bands.v_short))**0.5
# Get z-score
bands['z'] = qnorm(0.975) # get position of 97.5th percentile
# Now if z, the 97.5th percentile,
# is 1.96 standard deviations from the mean in the normal,
# Then so too is the 2.5th percentile in the normal.
# Give me 1.96 standard deviations above cp 
# in the sampling distribution of cp!
# Get upper and lower confidence interval!
bands['lower'] = bands.estimate - bands.z * bands.se
bands['upper'] = bands.estimate + bands.z * bands.se

bands     # View
    
# 10.3.4 Visualizing Confidence Intervals

# Were we to visualize this, it might look like…    

bands['x'] = 'Cp Index'
lines = pd.DataFrame({'yintercept': [0,1,2], 'color': ['thresholds', 'benchmark', 'thresholds']})
(
  ggplot() + 
    # Get draw us some benchmarks to make our chart meaningful
    geom_hline(data = lines, mapping = aes(yintercept = 'yintercept', color = 'color')) +
    scale_color_manual(values = ["black", "grey"]) +
    
    # Draw points
    geom_point(data = bands, mapping = aes(x = 'x', y = 'estimate')) +
    # Draw lineranges
    geom_linerange(data = bands, mapping = aes(x = 'x', ymin = 'lower', ymax = 'upper')) +
    # Add theming
    theme_classic(base_size = 14) +
    coord_flip() +
    labs(y ='Index Value', x = "")
)

# It’s not the most exciting plot, but it does show very
# clearly that the value of C_p and its 95% confidence
# interval are nowhere even close to 1.0, the key threshold.
# This means we can say with 95% confidence that the true
# value of C_p is less than 1.


# 10.3.5 Bootstrapping C_p

# How might we estimate this using the bootstrap?
# 
# Well, we could…

# Initialize an empty list to store bootstrapped samples
nreps = 1000
myboot = []

# For each repetition, sample from the water DataFrame
for rep in range(1, 1000 + 1):
    sample = water.sample(n=len(water), replace=True)  # Bootstrapped sample
    sample['rep'] = rep  # Add repetition identifier
    myboot.append(sample)  # Store the sample

# Concatenate all bootstrapped samples into a single DataFrame
myboot = pd.concat(myboot, ignore_index=True)


# This produces a very, very big data.frame!

# Let’s now, for each rep, calculate our statistics from before!
mybootstat_s = myboot.groupby(['rep', 'time']).apply(lambda df: pd.Series({
  'xbar': df.temp.mean(), # get within group mean
  'sigma_w': df.temp.std(), # get within group sigma
  'n_w': df.temp.shape[0] # get sample size
}))
# For each rep...
mybootstat = mybootstat_s.groupby('rep').apply(
  lambda df: pd.Series({
    'limit_upper': 42,
    'limit_lower': 50,
    'xbbar': df.xbar.mean(), # grand mean
    'sigma_s': (sum(df.sigma_w**2) / len(df.sigma_w))**0.5, # sigma short
    'n': df.n_w.sum()
  })
)
x = mybootstat.groupby('rep').apply(
  lambda df: pd.Series({
    'estimate': cp(sigma_s = df.sigma_s, upper = df.limit_upper, lower = df.limit_lower)
    })
  ).explode('estimate')

# Bundle in your estimates
mybootstat = pd.concat([mybootstat, x], axis=1)

# Clear out extra data
del myboot
del mybootstat_s


# So cool! We’ve now generated the sampling distributions for xbbar, sigma_s, and cp!

# We can even visualize the raw distributions now! Look at those wicked cool bootstrapped sampling distributions!!!

# So last, let’s take our bootstrapped C_p statistics in
# mybootstat$cp and estimate a confidence interval and
# standard error for this sampling distribution.
# 
# Because we have the entire distribution, we can extract
# values at specific percentiles in the distribution using
# quantiles(), rather than qnorm() or such theoretical
# distributions.

myqi = pd.DataFrame({
  'cp': bands.estimate,
  'lower': mybootstat.estimate.quantile(q = 0.025),
  'upper': mybootstat.estimate.quantile(q = 0.975),
    # We can even get the standard error,
    # which is *literally* the standard deviation of this sampling distribution
  'se': mybootstat.estimate.std()
})


# This suggests a wider confidence interval than our normal
# distribution assumes by default - interesting!
# 
# We can perform bootstrapping to estimate confidence
# intervals for any statistic, including C_p, C_pk, P_p,
# or P_pk. The only limit is your computational power!
# Wheee!
# 
# Note: Whenever you bootstrap, it’s important that you
# clear out your Python environment to keep things running
# quickly, because you tend to accumulate a lot of
# really big data.frames. You can use del to do this.



# 10.4 CIs for any Index!

# Let’s practice calculating confidence intervals (CIs) for each of these indices.


# 10.4.1 CIs for Cp
# Now that we have our ingredients, let’s get our index and its confidence intervals!



# Capability Index (for centered, normal data)
def cp(sigma_s, upper, lower):
    return abs(upper - lower) / (6 * sigma_s)

bands = pd.DataFrame({
  'limit_lower': pd.Series(42),
  'limit_upper': pd.Series(50)
})
# get index
bands['estimate'] = cp(sigma_s = stat.sigma_s, lower = bands.limit_lower, upper = bands.limit_upper)
# degrees of freedom
bands['v_short'] = stat.k*(stat.n_w - 1) 
# standard error
bands['se'] = bands.estimate * (1 / (2*bands.v_short))**0.5
# Get z-score
bands['z'] = qnorm(0.975) # get position of 97.5th percentile
# Now if z, the 97.5th percentile,
# is 1.96 standard deviations from the mean in the normal,
# Then so too is the 2.5th percentile in the normal.
# Give me 1.96 standard deviations above cp 
# in the sampling distribution of cp!
# Get upper and lower confidence interval!
bands['lower'] = bands.estimate - bands.z * bands.se
bands['upper'] = bands.estimate + bands.z * bands.se

bands     # View
    
    


# 10.4.2 CIs for Cpk

# Write the function and generate the confidence interval for  Cpk

# Capability Index (for skewed, uncentered data)
def cpk(mu, sigma_s, lower=None, upper=None):
    # Testing values
    # sigma_s = stat.sigma_s; mu = stat.xbbar; lower = 42; upper = None

    a, b = None, None
    
    # If lower is provided, calculate 'a'
    if lower is not None:
        a = abs(mu - lower) / (3 * sigma_s)
    
    # If upper is provided, calculate 'b'
    if upper is not None:
        b = abs(upper - mu) / (3 * sigma_s)
    
    # If both lower and upper are provided, return the minimum of a and b
    if lower is not None and upper is not None:
        return min(a, b)
    
    # If only upper is provided, return b
    elif lower is None and upper is not None:
        return b
    
    # If only lower is provided, return a
    elif upper is None and lower is not None:
        return a

bands = pd.DataFrame({
  'limit_lower': pd.Series(42),
  'limit_upper': pd.Series(50)
})
# get index
bands['estimate'] = cpk(mu = stat.xbbar.values, sigma_s = stat.sigma_s.values, lower = bands.limit_lower.values, upper = bands.limit_upper.values)
# degrees of freedom
bands['v_short'] = stat.k*(stat.n_w - 1) 
# standard error
bands['se'] = bands.estimate * (   1 / (2*bands.v_short) + 1 / (9 * stat.n * bands.estimate**2) )**0.5
# Get z-score
bands['z'] = qnorm(0.975) # get position of 97.5th percentile
# Get upper and lower confidence interval!
bands['lower'] = bands.estimate - bands.z * bands.se
bands['upper'] = bands.estimate + bands.z * bands.se

bands     # View


# 10.4.3 CIs for Pp

bands = pd.DataFrame({
  'limit_lower': pd.Series(42),
  'limit_upper': pd.Series(50)
})
# get index
bands['estimate'] = pp(sigma_t = stat.sigma_t, lower = bands.limit_lower, upper = bands.limit_upper)
# degrees of freedom
bands['v_total'] = stat.n_w*stat.k - 1 
# standard error
bands['se'] = bands.estimate * (1 / (2*bands.v_total))**0.5
# Get z-score
bands['z'] = qnorm(0.975) # get position of 97.5th percentile
# Get upper and lower confidence interval!
bands['lower'] = bands.estimate - bands.z * bands.se
bands['upper'] = bands.estimate + bands.z * bands.se

bands     # View


# 10.4.4 CIs for Ppk

def ppk(mu, sigma_t, lower=None, upper=None):
    
    a, b = None, None
    
    # If lower is provided, calculate 'a'
    if lower is not None:
        a = abs(mu - lower) / (3 * sigma_t)
    
    # If upper is provided, calculate 'b'
    if upper is not None:
        b = abs(upper - mu) / (3 * sigma_t)
    
    # If both lower and upper are provided, return the minimum of a and b
    if lower is not None and upper is not None:
        return min(a, b)
    
    # If only upper is provided, return b
    elif lower is None and upper is not None:
        return b
    
    # If only lower is provided, return a
    elif upper is None and lower is not None:
        return a


bands = pd.DataFrame({
  'limit_lower': pd.Series(42),
  'limit_upper': pd.Series(50)
})
# get index
bands['estimate'] = ppk(mu = stat.xbbar.values, sigma_t = stat.sigma_t.values, lower = bands.limit_lower.values, upper = bands.limit_upper.values)
# degrees of freedom
bands['v_total'] = stat.n_w*stat.k - 1 
# standard error
bands['se'] = bands.estimate * (   1 / (2*bands.v_total) + 1 / (9 * stat.n * bands.estimate**2) )**0.5
# Get z-score
bands['z'] = qnorm(0.975) # get position of 97.5th percentile
# Get upper and lower confidence interval!
bands['lower'] = bands.estimate - bands.z * bands.se
bands['upper'] = bands.estimate + bands.z * bands.se

bands     # View




# Conclusion

# Alright! You are now a confidence interval wizard!

# Go forth and make confidence intervals!



# Clean up
globals().clear()
