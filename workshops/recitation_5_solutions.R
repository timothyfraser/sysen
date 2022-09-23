# Recitation 5 Solutions
# Dr. Fraser, Fall 2022

# Pairs with Slides 15-17 from this Google Slides
# https://docs.google.com/presentation/d/1cquctoxT4lM15y1wGKL7tEzurMzHP9cjN8M5_RM17zE/edit?usp=sharing

#####################
# Question 1:
#####################


# How often do fireworks spontaneously combust? 
# An independent journalist compiled the following data, 
# and contracted you to analyze it. They gave you a crosstable. 

# By expected, here we want to test the Exponential Distribution
# Expected = exponential
# CDF = 1 - e-t * lambda   pexp()
# Estimate the average failure rate and chi-squared!

# You were provided with this data
# Assume that all fireworks eventually combusted (r=n)
tab <- data.frame(
  label = c("0-5", "5-10", "10-15", "15-20"),
  count = c(2, 5, 4, 8)
)

# Solution:

# Step 1: Get midpoint and cumulative for each interval
crosstab <- tab %>%
  mutate(
    # Estimate the midpoint for each label
    midpoint = c(2.5, 7.5, 12.5, 17.5),
    # And tally up the number of times fireworks exploded cumulatively!
    cumulative = cumsum(count))

# Step 2: Estimate Lambda
stat <- crosstab %>%
  summarize(
    # Tally total units that DID fail
    r = sum(count),
    # Estimate total possible hours they could have failed
    nt = sum(midpoint * count),
    # Get total units (all failed, so r = n)
    n = r,
    # Get latest timestep examined
    tmax =  max(midpoint),
    # Finally, let's estimate lambda!!!
    lambda_hat = r / (nt +  (n - r) * tmax) )

# Step 3: Calculate Chi-squared
end <- crosstab %>%
  mutate(
    # Set the observed cumulative count to be 'o'
    o = cumulative,
    # Estimate the expected cumulative count if Exponential 
    # using CDF of exponential, as 'e'
    # requires we get lambda_hat first
    e = rexp(midpoint, rate = stat$lambda_hat)) %>%
  # Summarize data into 1 row!
  summarize(
    # Calculate chisq statistic
    chisq = sum( (o - e)^2 / e ),
    # Wait, there's more??
    # Not really, but you could estimate the 
    # p-value for chisquared and the 
    # upper and lower confidence interval for lambda_hat
    # Calculate degrees of freedom for chisq
    # number_of_intervals - number_of_parameters (lambda) - 1
    df = n() - 1 - 1,
    # Calculate p-value
    p_value = 1 - pchisq(chisq, df =  df))

# So, we can conclude that the chisquared statistic is HUGE
# and WAY, WAY more extreme than most statistics we'd get 
# due to chance in a distribution matching the traits of our sample (our degrees of freedom)
# a p-value < 0.001 means it was bigger than 99.9% of the distribution,
# and < 0.1% were more extreme.
end
# So, we probably shouldn't use the exponential here
# to approximate this data!

remove(tab, crosstab, stat, end)


#####################
# Question 2:
#####################


# An auto company’s max acceptable failure rate
# is traditionally 0.05, within a 95% confidence interval. 
# You are allow to break 500 products and 
# have crash dummies rented for 1000 hours. 
# How many vehicles should you request for your test?
  
# Max failure rate is  
lambda_upper = 0.0005

# We can break 500 cars
r = 500
# We've got 1000 hours to do the test
t = 1000
# We want to choose a sufficient sample size of cars
# such that we could be 95% certain that
# the failure rate is less than 0.0005, whatever it is.
# ci = 0.95

# We can calculate the chi-squared stat corresponding to the
# 95th percentile of the chi-squared distribution 
# that best fits our data (df)
# Since we don't plan on seeing all the units fail (r != n)
# We need to assume a more conservative estimate for degrees of freedom
# so df = 2*(r+1) for time censored data
chisq = qchisq(0.95, df = 2*(r+1))

# We can calculate k, our weight for getting the upper bound of lambda
# by taking k = chisq / (2*r)
# because no matter what type of data or censoring,
# the relationship between k and chisq is ALWAYS k = chisq / (2*r)
k_upper =  chisq/ (2*r)


# Now, we can solve for n!
# We know that...
# lambda_upper = r / (n * t)   * k_upper
# so...
# n * t * lambda_upper = r * k_upper
# so...
# n = r * k_upper / (t * lambda_upper)

n = r * k_upper / (t * lambda_upper)

# Check it!
n

# Looks like you need a sample size of ~1000 cars
# To design a valid test if you hope to verify whether you
# can stay under that max failure rate.

remove(t, r, n, k_upper, lambda_upper, chisq)



#####################
# Question 3:
#####################

# A ship’s boiler is mandated by law to have 
# a failure rate below 0.001. 

# You have a fleet of 100 ships, are allowed to break 10 boilers, 
# and have 5000 hours to test them. 

# What’s the max level of confidence you 
# could attain that these boilers won’t break?


# Step 1:

# We know that:
# r / (n * t) * k_upper = lambda_upper

# The max failure rate the company will accept is 0.001
# so we'll make that the upper bound of our confidence interval for lambda_hat
lambda_upper = 0.001
# We're allowed to break 10 boilers max, before the company comes after us!
r = 10
# We have a supply of 100 ships' boilers (1 per ship)
n = 100
# They're lending us the ships for 5000 hours of testing each
t = 5000 

# Looks like we're not allowed to test all the way until all units fail,
# so we can write the degrees of freedom as...
# df = 2*(r + 1)
# This creates slightly more conservative chisquared stats.

# We can restate the formula as
# k_upper = lambda_upper / (r / (n*t))
# k_upper = lambda_upper * n*t / r

k_upper = lambda_upper * n* t / r

# Our k value would have to be pretty big
# to accomodate this upper bound
k_upper

# We can get the value of chi-squared by dividing k by (2r)
# note that even though there's type I time censoring,
# we still use 2 * r here
# because the relationship between k and chisquared
# is always by a factor of 2r
chisq = k_upper / (2 * r)

# Let's find what percentage of stats this upper bound chisquared statistic is more extreme than
# THIS is the stage where we use the type I censoring adjusted degrees of freedom.
pchisq(chisq, df = 2*(r+1))

# Who! It's more extreme than **almost all of them** (99.9%)!!!!

# So our confidence rate would be, hypothetically, 99.9% here.

# Interpretation:
# We are ~99.9% confident that a test over 5000 hours where
# 10 boilers out of 100 fail would
# yield a lambda_hat failure rate of 0.001 or lower.


remove(t, r, n, k_upper, lambda_upper, chisq)

# All done!
# Yay!
