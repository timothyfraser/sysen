# 07_training.py
# Training: System Reliability
# Pairs with R training:
# https://timothyfraser.com/sigma/system_reliability.html
# Tim Fraser

# Getting Started ############################

## Install Packages ############################
# Install main python packages for this script
# !pip install pandas
# !pip install sympy
# !pip install math
# !pip install plotnine
# !pip install os
# !pip install sys

## Load Packages ############################
import pandas as pd # Import pandas functions
import sympy as sp # import mosaicCalc proxy in python for calculus
from plotnine import * # import all plotnine visualization functions
import os
import sys
# Append files in this folder (functions) to the Python Path
sys.path.append(os.path.abspath('functions'))
# Now you can reference them directly
from functions_distributions import *

# Import calculus functions
import sympy as sp
import math


# 1. Concepts ###################################

## 1.1 Life Distributions ########################

# All technologies, operations, etc. have a ‘lifetime distribution’.
# If you took a sample of, say, cars in New York,
# you could measure how long each car functioned properly
# (its life-span), and build a Lifetime Distribution 
# from that vector.

# Let's imagine a normally distributed lifespan 
# for these cars...
lifespan = rnorm(100, mean = 5, sd = 1)
lifespan # View


# The lifetime distribution is the 
# probability density function telling us 
# how frequently each potential lifespan 
# is expected to occur.

# We can build ourself the PDF of our lifetime distribution here
dlife = density(lifespan)
dlife(5) # eg. probability density at time t = 5


# In contrast, the Cumulative Distribution Function (CDF)
# for a lifetime distribution tells us, 
# for any time  t, the probability that 
# a car will fail by time t
 
 # And we can build the CDF here
plife <- lifespan %>% density() %>% tidy() %>% 
  mutate(y = cumsum(y) / sum(y)) %>% approxfun()
plife = tidy_density(density(lifespan))
plife['y'] = plife.y.cumsum() / plife.y.sum()
plife = approxfun(plife)
plife(5) # probability car will fail by time t

# Having built these functions for our cars, 
# we can generate the probability (PDF) 
# and cumulative probability (CDF) of failure 
# across our observed vector of car lifespans, 
# from ~3.21 to ~6.81.

# Reliability or Survival Analysis is concerned
# with the probability that a unit (our car) 
# will still be operating by a specific time t, 
# representing the percentage of all cars 
# that will survive to that point in time. 
# So let’s also calculate 1 - cumulative probability of failure.

# Get sequence of times...
mycars = pd.DataFrame({ 
  'time': seq(lifespan.min(), lifespan.max(), by = 0.1)
})
# Get probability of failing at time time
mycars['prob'] = dlife(mycars.time)
# Get probability of failing at or before time t
mycars['prob_cumulative'] = plife(mycars.time)
# Get probability of surving past time t 
# (NOT failing at or before time t) 
mycars['prob_survival'] = 1 - plife(mycars.time)

mycars # view

# Let’s plot our three curves!

# Assign values to variables
mycars['fill1'] = 'Cumulative Probability'
mycars['fill2'] = 'Reliability (Survival)'
mycars['fill3'] = 'Probability'

(ggplot() +
  # Make one area plot for Cumulative Probability (CDF)
  geom_area(data = mycars, 
            mapping = aes(x = 'time', y = 'prob_cumulative', 
                          fill = 'fill3'), alpha = 0.5) +
  # Make one area plot for Relibability
  geom_area(data = mycars, 
            mapping = aes(x = 'time', y = 'prob_survival', 
                          fill = 'fill2'), alpha = 0.5) +
  # Make one area plot for Probability (PDF)
  geom_area(data = mycars,
            mapping = aes(x = 'time', y = 'prob', 
                          fill = 'fill3'), alpha = 0.5) +
  theme_classic() +
  theme(legend_position = 'bottom') + # notice it is legend_position, not legend.position 
  labs(x = "Lifespan of Car", y = "Probability",
       subtitle = "Example Life Distributions")
)

# This new reliability function allows us to 
# calculate 2 quantities of interest:
# - expected (average) number of cars that fail up to time  t
# - total cars expected to still operate after time  t
 
 .
## 1.2 Example: Airplane Propeller Failure ##################
 
# Suppose Lockheed Martin purchases 800 new airplane propellers.
# When asked about the failure rate,
# the seller reports that every 1500 days, 
# 2 of these propellers are expected to break. 
# Using this, we can calculate
# m the mean time to fail!

# see formulas in textbook


# This lets us generate the failure rate  
# F(t), also known as the Cumulative Distribution Function, 
# and we can write it up like this.

def fplane(t):
  return 1 - math.exp(-1*(t/750))


# What’s the probability a propeller will fail 
# by t = 600 days? By t = 5000 days?  

fplane(t = 600)
fplane(t = 5000)

# Looks like 55% will fail by 600 days, 
# and 99% fail by 5000 days.

# What’s the probability a propeller will fail 
# between 600 and 5000 days?

fplane(t = 5000) - fplane(t = 600)

# ~45% more will fail between this period.

# What percentage of new propellers will work
# more than 6000 days?
1 - fplane(t = 6000)

# 0.03% will survive past 6000 days.


# If Lockheed uses 300 propellers, 
# how many will fail in 1 year? In 3 years?

# Given a sample of 300 propellers,
n = 300
# We project n * fplane(t = 362.25) will fail in 1 year (365.25 days)
# that's ~115 propellers.
n*fplane(t = 365.25)
# We also prject that n * fplane(t = 3 * 362.25) will fail in 3 years
# that's ~230 propellers!
n*fplane(t = 3*365.25)

# Pretty powerful!



# Learning Check 1 #############################

# Question

# Hypothetical: Samsung is releasing a new Galaxy phone. 
# But after the 2016 debacle of exploding phones, 
# they want to estimate how likely it is a phone 
# will explode (versus stay intact). Their pre-sale trials 
# suggest that every 500 days, 5 phones are expected 
# to explode. What percentage of phones are expected 
# to work after more than 6 months? 1 year?




# Answer 

# Using the information above, we can calculate 
# the mean time to fail m, the rate of how many days 
# it takes for an average unit to fail.

days = 500
units = 5
m = days / units
# Check it!
m

# We can use m to make our explosion function fexplode(), 
# which in this case, is our (catastrophic) failure function  

def fexplode(days):
  return 1 - math.exp(-1*days*0.01)

# Then, we can calculate  r(t), 
# the cumulative probability that a phone will 
# not explode after t  days.

# Let’s answer our questions!

# What percentage of phone are expected to survive 6 months?
1 - fexplode(365.25 / 2)

# What percentage of phone are expected to survive 1 year?

1 - fexplode(365.25)



# 2. Joint Probabilities ##########################

# Two extra rules of probability can help us understand system reliability.

## 2.1 Multiplication Rule ##########################

# probability that  n units with a reliability function  R(t)
# survive past time  t is multiplied, 
# because of conditional probability, to equal  R(t)^n

# For example, there is a 50% change that 1 coffee cup breaks
# at local coffesshop Coffee Please! every 6 months (180 days)
# The mean number of days to cup failure is m = 180 days / (1 cupy * 0.50 chance) = 360 days
# while the relative frequency (probability) that a cup will break is 50%.
 
def fcup(days):
  return 1 - math.exp(-1 * (days/360))
# The probability that 1 breaks within 100 days is...
fcup(100)

# And let's write out a reliability function too, based on our function for the failure function
# notice how we reference an earlier function fcup? It won't work without it.
def rcup(days):
  return 1 - fcup(days)
# So the probability that 1 *doesn't* break within 100 days is...
rcup(100)

# But the probability that two break within 100 days is...
fcup(100) * fcup(100)


# and the probability that 5 break within 100 days is... very small!
fcup(100)**5


## 8.2 Compliment Rule #################

# The probability that at least 1 of n units 
# fails by time t is 1 - r(t)^n

# So, if Coffee Please! buys 2 new cups for
# their store, the probability that at
# least 1 unit breaks within a year is…
1 - rcup(days = 365.25)**2

# While if they buy 5 new cups for their 
# store, the chance at least 1 cup breaks
# within a year is…
1 - rcup(days = 365.25)**5

# 3. Table of Failure Related Functions #################
# See https://timothyfraser.com/sigma/system-reliability.html#table-of-failure-related-functions
# great resource.


# 4. Hazard Rate Function ##################

# But if a unit has survived up until now, 
# shouldn’t its odds of failing change? 
# We can express this as:

# P(fail tomorrow | survive until today) = (F(days + change in days) - F(days) ) / (change in days * R(days))

# Local coffeeshop Coffee Please! 
# also has a lucky mug, which has 
# stayed intact for 5 years, 
# despite being dropped numerous times 
# by patrons. Coffee Please!’s failure rate
# suggests they had a 99.3% chance of it
# breaking to date.

# we call this the Hazard Rate Z
def zcup(days, plus = 1):
  return (fcup(days + plus) - fcup(days)  )  / (plus * rcup(days) )

# It survived for 5 years - what's the change it fails tomorrow?
zcup(days = 5*365.25, plus = 1)


# 5. Accumulative Hazard Function ############3

# - H(t): total accumulated risk of
# experiencing the event of interest
# that has been gained by progressing 
# from 0 to time  t

# - the (instantaneous) hazard rate h(t)
#  can grow or shrink over time, 
# but the cumulative hazard rate 
# only increases or stays constant.

# by log, we mean the natural log; math.log defaults to a base of math.exp(1)
def hcup(days):
  return -1*math.log( rcup(days) )

# This captures the accumulative probability
# ofa hazard (failure) occurring 
# given the number of days past.
hcup(100)


# 6. Average Failure Rate ################

# The hazard rate z(t) varies over time,
# so let's make a single statistic that
# summarizes the distribution of hazard rates
# that z(t) can provide us between 
# times ta --> tz. 
# We'll call this the
# AVerage Failure Rate AFR(T)

def afrcup(t1,t2):
  return (hcup(t2) - hcup(t1) ) / (t2 - t1)

afrcup(0, 5)

# Or, you can write it as....
def afrcup(t1,t2):
  return (math.log(rcup(t1)) - math.log(rcup(t2))) / (t2 - t1)
afrcup(0, 5)

# And if we're going from 0 to time t,
# it simplifies to...
def afrcup(days):
  return hcup(days) / days
  
afrcup(5)

# or to this
def afrcup(days):
  return -1*math.log(rcup(days)) / days

afrcup(5)

# When the probability for a time t is less than 0.10,
# AFR = F(t)/T. This means that...
# F(t) = 1 - e^(-T * AFR(T))
# which approximates
# T x AFR(T) when F(T) < 0.10

def afrcup(days):
  return fcup(days) / days
afrcup(5) # pretty close

# 7. Units ###############################

# Units can be tough with failure rates.
# They get tiny really quick. 
# Here are some common units:

# Percent per thousand hours where %/K = 10^5 x z(t)

# Failure in Time (FIT) per thousand hours,
# also known as Parts per million per Thousand Hours,
# written PPM/K = 10^9 * z(t).
# This equals 10^4 * failure rate in %/K.

# For this lifetime function F(t) = 1 - e^(-1*(t/2000)^0.5),
# what's the failure rate at t = 10, t= 1000, and t= 10,000 hours?
# Convert them into % / K and PPM/K.


## 7.1 Failure Functions ####################

# First, let's write failure function f(t)

def f(t):
  return 1 - math.exp(-1*(t/2000)**0.5)

# Second, let's write the hazard rate z(t), for a 1 unit change in t.

def z(t, change = 1):
  # to help, we can make temporary objects within the function.
  # Get change in failure function
  deltaf = (f(t + change) - f(t) ) / change
  # Get reliability function
  r = 1 - f(t)
  # Get hazard rate
  return deltaf / r

# Third, let's write the average hazard rate afr(t1,t2)

def afr(t1,t2):
  # Let's get the survival rate r(t)
  r1 = 1 - f(t1)
  r2 = 1 - f(t2)
  # Let's get the accumulative hazard rate h(t)
  h1 = -math.log(r1)
  h2 = -math.log(r2)
  # And let's calculate the average failure rate!
  afr = (h2 - h1) / (t2 - t1)
  
  # and retrun it!
  return afr

## 7.2 Conversion Functions ##################

# Fourth, let's write some functions 
# to convert out results into %/K and PPM/K,
# so we can be lazy!

# % per 1000 hours
def pk(rate):
  return rate * 100 * 10**3
# PPM/1000 hours
def ppmk(rate):
  return rate * 10**9

## 7.3 Converting Estimates #####################

# Let's compare hazard rates when t = 10, 
# per hour, in % per 1000 hours and PPM per 1000 hours.

# Per hour. 
z(t = 10)

# % per 1000 hours!
pk(z(t = 10))
# PPM per 1000 hours!
ppmk(z(t = 10))

# Finally, let's calculate the average failure rate between 1000 and 10000 hours,
# in %/K
pk(afr(1000, 10000))

ppmk(afr(1000,10000))



# Learning Check 2 #######################3


## Question ###########################

# A food safety inspector is investigating
# the average shelf life of instant ramen noodles.
# A company estimates the average shelf life
# of a package of ramen noodles at 
# ~240 days per package. 
# In a moment of poor judgement, 
# she hires a team of hungry college students
# to taste-test old packages of 
# that company’s ramen noodles, 
# randomly sampled from a warehouse. 
# When a student comes down with food poisoning, 
# she records that product as having gone bad
# after XX days. 
# She treats the record of
# ramen food poisonings as a sample of 
# the lifespan of ramen products.

ramen = pd.Series([163, 309, 215, 211, 246, 198, 281, 180, 317, 291, 
           238, 281, 215, 208, 212, 300, 231, 240, 285, 232, 
           252, 261, 310, 226, 282, 140, 208, 280, 237, 270, 
           185, 409, 293, 164, 231, 237, 269, 233, 246, 287, 
           187, 232, 180, 227, 215, 260, 236, 229, 263, 220])

ramen

# Using this data, please calculate:

# 1. What's the cumulative probability of a pack of ramen
# going bad after 240 days? Are the company's predictions accurate?

# 2. What's the average failure rate lambda
# for the period between 8 months  (240 days)
# to 1 year?

# 3. What's the mean time to failure (m) for 
# the period between 8 months and 1 year?



## Answer ########################


# First, we take her ramen lifespan data, 
# estimate the PDF with density(), 
# and make the failure function (CDF), which I’ve called framen() below

# Get failure function f(t) = CDF of ramen failure
framen = tidy_density(density(ramen))
framen['y'] = framen.y.cumsum() / framen.y.sum()
framen = approxfun(framen)

framen(1)
# Values will vary slightly from R version because we interpolate out 1000 points in python.

# Alternatively, you may have approximated the lifespan distribution,
# like so:
# lam = 1 / ramen.mean()
# def framen(days, lam):
#   return 1 - math.exp(-1*t**lam)  


# Second we calculate the reliability function rramen()

# Get survival function r(t) = 1 - f(t)

def rramen(days):
  return 1 - framen(days)

# Third, we can shortcut to the 
# average failure rate, called 
# afrramen() below, by using the 
# reliability function rramen() to 
# make our hazard rates at time 1 (h1) and time 2 (h2).

def afrramen(days1, days2):
  h1 = -1*math.log(rramen(days1))
  h2 = -1*math.log(rramen(days2))
  return (h2 - h1) / (days2 - days1)


# 1. What's the cumulative probability of a pack of ramen
# going bad after 240 days? Are the company's predictions accurate?

framen(240)

# 2. What's the average failure rate lambda
# for the period between 8 months  (240 days)
# to 1 year?
afrramen(240, 365)

# 3. What's the mean time to failure (m) for 
# the period between 8 months and 1 year?

# Calculate inverse of failure rate lambda
m = 1 / afrramen(240, 365)
m


# Note: Values will vary slightly from R version because 
# our empirical CDF interpolates out 1000 points in python, 
# compared to a different number in R.





# 8. System Reliability ######################



# Reliability rates become extremely useful 
# when we look at an entire system! 
# This is where system reliability analysis 
# can really improve the lives of ordinary people, 
# decision-makers, and day-to-day users, 
# because we can give them the knowledge 
# they need to make decisions.

# So what knowledge do users usually need?

# How likely is the system as a whole to survive or fail over time?


## 8.1 Series Systems ####################

# In a series system, we have a set of n components,
# which get utilized sequentially:
# A domino train, for example, is a series system.
# It only takes 1 component to fail to stop the entire system (causing system failure)
# The overall reliability of a series system is defined as:
# the success of every individual component A AND B AND C.


# Series Reliability = R_s = R1 * R2 * R3 * ... Rn

# We can visualize it like so:

# R1 ---- R2 ----- R3


# In a parallel system (redundant system),
# we have n components,
# but just 1 component needs to function for the system to function.

# The overall reliability of a parallel system is 
# defined as the success of any individual component
# A OR B OR (A AND B)

# Parallel Reliability = R_p = 1 - (F_1 * F_2 * ... F_n)
# Parallel Reliability = R_p = 1 - ((1 - R_1) * (1 - R_2) * ... (1 - R_n))


# See https://timothyfraser.com/sigma/system-reliability.html#parallel-systems
# for visualization


# 8.3 Combined Systems #######################

# Most systems involve combining probabilities of multiple subsystems.

# When combining configurations, we calculate probabilities of each subsystem,
# then calculate the overall probability of the final system,
# treating each subsystem as a node.


# See https://timothyfraser.com/sigma/system-reliability.html#combined-systems
# for visual and explanation....


# ...
# ...

# 8.4 Example: Business Reliability ################

# Local businesses deal heavily with
# series system reliability, even if they don’t 
# regularly model it. You’ve been hired to analyze 
# the system reliability of our local coffee shop 
# Coffee Please! Our coffee shop’s ability to 
# serve cold brew coffee relies on 5 components, 
# each with its own constant chance of failure.

# Water: Access to clean tap water. (Water outages occur ~ 3 days a year.)

# Coffee Grounds: Sufficient coffee grounds supply. (Ran out of stock 5 days in the last year).

# Refrigerator: Refrigerate coffee for 12 hours. (1% fail in a year.)

# Dishwasher: Run dishwasher on used cups (failed 2 times in last 60 days).

# Register: Use Cash Register to process transaction and give change (Failed 5 times in the 3 months)

# We can represent this as this series system:

# Water --- Coffee Grounds -- Refrigerator -- Dishwasher --- Register


# We can extract the average daily failure rate lambda
# for each of these components

# Water outage occrred 3 days in last 365 days
lambda_water = 3 / 365
# Ran out of stock 5 days in last 365 days
lambda_grounds = 5 / 365
# 1% of refrigerators fail within a 365 days
lambda_refrigerator = 0.01 / 365
# Failed 2 times in last 60 days
lambda_dishwasher = 2 / 60
# Failed 5 times in last 90 days
lambda_cash = 5 / 90

# Assuming a constant chance of failure, 
# we can write ourselves a quick failure function f 
# and reliability function r for an exponential distribution.

def r(t, lam):
  return math.exp(-1*t*lam)
math.exp(-1*2*0.3)

# And we can calculate the overall reliability 
# of this coffeeshop’s series system in 1 day 
# by multiplying these reliability rates together.

r(1, lambda_water) * r(1, lambda_grounds) * r(1, lambda_refrigerator) * r(1, lambda_dishwasher) * r(1, lambda_cash)

# And 89.5% of this system fully functioning on 1 day!


## 9. Renewal Rates via Bayes Rule ################3


# We would hope that failed parts often get replaced, 
#so we might want to adjust our functions accordingly.

# Renewal Rate:  r(t) reflects the mean number of 
# failures per unit at time   t
 .
# Example:

# Let’s say that…

# For 10 units, we calculated how many days
# post production they lasted till failure (failure) 
# as well as how many days post production till
# they were replaced (replace). 
# Using this, we can calculate the lag-time, 
# or the time taken for renewal.

units = pd.DataFrame({
  'id': seq(1,15, by=1),
  'failure': [10, 200, 250, 300, 350, 
        375, 525, 525, 525, 525,
        600, 650, 650, 675, 725],
  'replacement': [100, 250, 350, 440, 550, 
        390, 600, 625, 660, 605, 
        700, 700, 700, 725, 750]
})
units

units['renewal'] = units.replacement - units.failure
units.replacement
units.failure
units

# Let's get the failure function
# by calculating the observed CDF

# Approximate PDF of failure
mf = tidy_density(density(units.failure))
# Get CDF
mf['y'] = mf.y.cumsum() / mf.y.sum()
# Turn into function
mf = approxfun(mf)
# Unfortunately, our approximated CDF relies on
# extrapolated data, not the perfect function,
# so we need to clip our CDF at 0 and 1.
def f(time):
  probs = mf(time)
  probs[ probs < 0 ] = 0
  probs[ probs > 1] = 1
  return probs

# Calculate CDF of replacement
mfr = tidy_density(density(units.replacement))
mfr['y'] = mfr.y.cumsum() / mfr.y.sum()
mfr = approxfun(mfr)
def fr(time):
  probs = mfr(time)
  probs[ probs < 0 ] = 0
  probs[ probs > 1] = 1
  return probs




# Above, we made the function fr(), 
# which represents the cumulative probability 
# of replacement, unrelated to failure. 
# But what we really want to know is a
# conditional probability, specifically: 
# how likely is a unit to get replaced at time  b, 
# given that it failed at time  a?
# Fortunately, we can use Bayes’ Rule to deduce this

# First, let’s make a function f_fr(), 
# meaning the cumulative probability of failure 
# given replacement. This should (probably) be 
# the same probability of failure as usual, 
# but we need to restart the clock after replacement,
# so we’ll set the time as  time_failure - time_replacement

def f_fr(time, time_replacement):
  return f(time - time_replacement)

# Next, we’ll use Bayes Rule to get the 
# cumulative probability of replacement given failure, 
# estimated in a function fr_f().


# Probability of replacement given failure
def fr_f(time, time_replacement):
  # Estimate conditional probability of Failure given Replacement times Replacement
  top = f_fr(time, time_replacement) * fr(time_replacement)
  # Estimate total probability of Failure
  bottom = f_fr(time, time_replacement) * fr(time_replacement)  +  (1 - f_fr(time, time_replacement)) * (1 - fr(time_replacement))
  # Divide them, and voila!
  return top/bottom


# Finally, what do these functions actually look like?
# Let’s simulate failure and replacement over time, in a dataset of fakeunits.


# As time increases from 0 to 1100
fakeunits = pd.DataFrame({'time': seq(0,1100, by = 1)})
# Let's get probabiltiy of failure at that time
fakeunits['prob_f'] = f(fakeunits.time)
# Our failure function might produce some non-sensical negative probabilities, because it's an interpolated function. Let's cut those
# Let's get probability of replacement at time t + 10
fakeunits['prob_fr_10'] = fr_f(time = fakeunits.time, time_replacement = fakeunits.time + 10)
# Let's get probability of replacement at time t + 50
fakeunits['prob_fr_50'] = fr_f(time = fakeunits.time, time_replacement = fakeunits.time + 50)


# I admit, this code is still a little wonky. Let me know if you have any issues,
# and we'll troubleshoot.

globals().clear()
