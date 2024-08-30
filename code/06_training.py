# 06_training.py
# Training: Probability Functions
# Pairs with R training:
# https://timothyfraser.com/sigma/probability_functions.html
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


# Probability Functions #############################

# To support our python coders, I have developed a script
# called functions_distributions.py in the functions/ folder.
# We loaded it at the start of this script.
# It contains probability functions that mirror the syntax of our R probability functions.
# This should help make it a LOT easier to follow along.

# Example: Ithaca Farmers Market ####################

# Unobserved Distributions ########################

# Randomly sample 500 visits from a poisson distribution with a mean of 5.5
visits = rpois(n = 5000, mu = 5.5)
# Check out the distribution!
hist(visits)


## Density (PDF) #########################
# So, what percentage of customers stopped by 5 stalls?
# Below, dpois() tells us the density() or frequency 
# of your value, given a distribution where the mean = 5.5.
# Get the frequency for 5 visits in the distribution
dpois(5, mu = 5.5)
# Check it!
pd5

### OPTIONAL: Validate this ##############################

# Note: We can validate this using our simulated `visits` from above,
# if we use methods for Observed Probabilities,
# which we learn later in this tutorial. 
# We can calculate the `density()` function,
# extract it using `approxfun()`,
# and then assign it to `dsim()`, our own exact probability density function for our data. It works just like `dpois()`, but you don't need to specify `lambda`, because it only works for this exact distribution!

# Approximate the PDF of our simulated visits,
# and try the function for our simulated data!
density(visits)(5)
# Pretty close to our results from dpois()!


## Cumulative Probabilities (CDF)
# What percentage of customers stopped by at max 5 stalls?
# Get the cumulative frequency for a value (5) in the distribution
cd5 = ppois(5, mu = 5.5)
# Check it!
cd5

# Looks like just 52.9% of customers stopped by 1 stall or fewer.

# What percentage of customers stopped by over 5 stalls?

# Get the probability they will NOT stop at 5 or fewer stalls
1 - cd5


### OPTIONAL: Validate this ###########################
# We can validate our results against our simulated distribution.
# Let's get a density model
m = density(visits)
# Tidy the density model into 1000 estimates 
m = tidy_density(m, n = 1000)
# Get probability densities, in order of x axis
m = m.sort_values(by = 'x')
# Get cumulative probabilities
m = m.assign(y = lambda d: d.y.cumsum() / d.y.sum())
# Turn it into a literal function
psim = approxfun(m)

psim(5) # view it
# pretty close of cdf5!

## Quantiles ################################

# How many visits did people usually make?
# Estimate the interquartile range (25th-75th percentiles) 
# of the unobserved distribution.
q5 = qpois([.25, .75], mu = 5.5)
# Check it!
q5

# Looks like 50% of folks visited between 4 and 7 stalls

### OPTIONAL: Validate this ###########################
# We can compare against our simulated data using quantile().
# Approximate the quantile function of this distribution
# Get a vector of percentiles from 0 to 1, in units of 0.001
qsim = pd.DataFrame({'x': seq(0,1,by =0.001) })
# Using our simulated distribution, 
# get the quantiles (values) at those points from this distribution
qsim['y'] = qsim['x'].apply(lambda x: visits.quantile(x))
# Approximate the function,
# and then simulate quantiles at the 25th and 75th percentile
approxfun(qsim)([.25, .75])



# Learning Check 1 #################################

# Question

# What if we are not certain whether our unobserved vector of 
# visits has a Poisson distribution or not? 
# To give you more practice, please calculate the probability
# that customers will stop at more than 5 stalls,
# using appropriate functions for the
# (1) Normal, (2) Gamma, and (3) Exponential distribution! 
# (See our table above for the list of function names.)

# Answer 

# We know there were n = 500 customers,
# with a mean of 5.5 visits, a median of 5 visits, 
# and a standard deviation of 2.5 visits.

# For a Normal Distribution:

# We learned earlier that rnorm() 
# requires a mean and sd (standard deviation);
# we conveniently have both!

1 - pnorm(5, mean = 5.5, sd = 2.5)

# For a Gamma Distribution:

# We learned earlier that rgamma() requires a 
# shape and scale (or rate); 
# we can calculate these from the 
# mean and sd (standard deviation).

# shape = mean^2 / variance = mean^2 / sd^2
shape = 5.5**2 / 2.5**2
# scale = variance / mean
scale = 2.5**2 / 5.5
# AND
# rate = 1 / scale
rate = 1 / scale

# So...
# Get 1 - cumulative probability up to 5
1 - pgamma(5, shape = shape, rate = rate)


# For an Exponential Distribution:

# We learned earlier that rexp() requires a rate; 
# we can calculate this from the mean.


# For exponential distribution,
# rate = 1 / mean
rate = 1 / 5.5

# So...
# Get 1 - cumulative probability up to 5
1 - pexp(5, rate = rate)



# Observed Probability Functions ###########################

# Example: Observed Distributions ###################################

# For example, a local hospital wants to make 
# their health care services more affordable,
# given the surge in inflation.

# They measured n = 15 patients who stayed 1 night 
# over the last 7 days, how much were they charged 
# (before insurance)? 
# Let’s call this vector obs (for ‘observed data’).

# A 16th patient received a bill of $3000
# (above the national mean of ~$2500). 
# We’ll record this as stat below.

# Let's record our vector of 15 patients
obs = pd.Series([1126, 1493, 1528, 1713, 1912, 2060, 2541, 2612, 2888, 2915, 3166, 3552, 3692, 3695, 4248])
# And let's get our new patient data point to compare against
stat = 3000


# Here, we know the full observed distribution of values (cost),
# so we can directly compute the p_value from them, 
# using the logical operator >=.


# Which values of in vector obs were greater than or equal to stat?
obs >= stat


# Our code interprets True == 1 & False == 0, 
# so we can take the mean() to get the percentage of values 
# in obs greater than or equal to stat.

# Get p-value, the probability of getting a value greater than or equal to stat
# # This means Total Probability, where probability of each cost is 1/n
sum(obs >= stat) / len(obs)


# Unfortunately, this only takes into account the exact values
# we observed (eg. $1493), but it can’t tell us anything
# about values we didn’t observe (eg. $1500). 
# But logically, we know that the probability of 
# getting a bill of $1500 should be pretty similar 
# to a bill of $1493. So how do we fill in the gaps?


# Observed PDFs (Probability Density Functions) ######################

# Above, we calculated the probability of getting a 
# more extreme hospital bill based on a limited sample of points,
# but for more precise probabilities, 
# we need to fill in the gaps between our observed data points.

# For a vector x, the probability density function is a
# curve providing the probability (y) of each value 
# across the range of x.

# It shows the relative frequency (probability) of each possible value in the range.

# We can ask Python to estimate the probability density function 
# for any observed vector using our custom function density().
# This returns the density (y) of a bunch of hypothetical values 
# (x) matching our distribution’s curve.
# We can access those results using the function_distribution.py script, 
# by tidy_density()-ing it into a data.frame.


tidy_density(density(obs))

# But that’s data, not a function, right? 
# Functions are equations, machines you can pump an input 
# into to get a specific output. Given a data.frame of 2 vectors,
# we can actually approximate the function (equation) connecting
# vector 1 to vector 2 using approxfun(), 
# creating your own function! So cool!

# Let's make dobs(), the probability density function for our observed data. 
dobs  = approxfun(tidy_density(density(obs)))
# Now let's get a sequence (seq()) of costs from 1000 to 3000, in units of 1000....
seq(1000, 3000, by = 1000)


# and let's feed it a range of data to get the frequencies at those costs!
dobs(seq(1000, 3000, by = 1000))

  # Get sequence from min to max, in units of $10
mypd = pd.DataFrame({'cost': seq(obs.min(), obs.max(), by = 10)})
# Get probability densities
mypd['prob_cost_i'] = dobs(mypd.cost)
  # Classify each row as TRUE (1) if cost greater than or equal to stat, or FALSE (0) if not.
  # This is the probability that each row is extreme (1 or 0)
mypd['prob_extreme_i'] = mypd.cost >= stat

mypd # view

# We’ll save it to mypd, naming the x-axis cost and the y-axis prob_cost_i, 
# to show the probability of each cost in row i
# (eg. $1126, $1136, $1146, … n).

# We’ll also calculate prob_extreme_i, the probability that each 
# ith cost is extreme (greater than or equal to our 16th patient’s bill). 
# Either it is extreme (TRUE == 100% = 1) 
# or it isn’t (FALSE == 0% == 0).

# Our density function dobs() estimated prob_cost_i (y), 
# the probability/relative frequency of cost (x) occurring,
# where x represents every possible value of cost.

# We can visualize mypd using geom_area() or geom_line() in ggplot2!

# We can add geom_vline() to draw a vertical line 
# at the location of stat on the xintercept.

(ggplot(data = mypd, mapping = aes(x = 'cost', y = 'prob_cost_i', fill = 'prob_extreme_i')) +
  # Fill in the area from 0 to y along x
  geom_area() +
  # Or just draw curve with line
  geom_line() +
  # add vertical line
  geom_vline(xintercept = stat, color = "red", size = 3) +
  # Add theme and labels
  theme_classic() +
  labs(x = "Range of Patient Costs (n = 15)",
       y = "Probability",
       subtitle = "Probability Density Function of Hospital Stay Costs") +
  # And let's add a quick label
  annotate("text", x = 3500, y = 1.5e-4, label = "(%) Area\nunder\ncurve??", size = 5)
)



# Using PDFs (Probability Density Functions) ######################

# Great! We can view the probability density function now above. 
# But how do we translate that into a single probability
# that measures how extreme Patient 16’s bill is?

# We have the probability prob_cost_i at points cost 
# estimated by the probability density function 
# saved in mypd.

# We can calculate the total probability or p_value
# that a value of cost will be greater than 
# our statistic stat, using our total probability formula. 
# We can even restate it, so that it looks a little more 
# like the weighted average it truly is.

# (see textbook)

# Calculate the conditional probability of each cost occurring given that condition
mypd['prob_cost_extreme_i'] = mypd.prob_cost_i * mypd.prob_extreme_i

  # Next, let's summarize these probabilities
p = pd.DataFrame({
  # Add up all probabilities of each cost given its condition in row i
  'prob_cost_extreme': [ sum(mypd.prob_cost_extreme_i)],
  # Add up all probabilities of each cost in any row i
  'prob_cost': [ sum(mypd.prob_cost_i)]
})

# Calculate the weighted average, or total probability of getting an extreme cost
# by dividing these two sums!
p['prob_extreme'] = p.prob_cost_extreme / p.prob_cost

p # view

# What's visually happening here?
num = str(round(p.prob_extreme, 2).values[0])
label = ("P(Extreme)" + "\n" + " = " + num)
(ggplot() +
  geom_area(data = mypd, mapping = aes(x = 'cost', y = 'prob_cost_i', fill = 'prob_extreme_i')) +
  geom_vline(xintercept = stat, color = "red", size = 3) +
  theme_classic() +
  labs(x = "Range of Patient Costs (n = 15)",
       y = "Probability",
       subtitle = "Probability Density Function of Hospital Stay Costs") +
  annotate("text", x = 3500, y = 1.5e-4, 
           label = label, size = 5)
)

del num,label

# Observed CDFs (Cumulative Distribution Functions) ###########################


# Alternatively, we can calculate that p-value for prob_extreme
# a different way, by looking at the cumulative probability.

# To add a values/probabilities in a vector together sequentially, 
# we can use cumsum() (short for cumulative sum). 
# For example:
# Let's imagine a normally distributed lifespan for these cars...
# Normally
seq(1,5,by=1)

# Cumulatively summed
seq(1,5,by=1).cumsum()

# Same as
[1, 2+1, 3+2+1, 4+3+2+1, 5+4+3+2+1]


# Every probability density function (PDF) can also be 
# represented as a cumulative distribution function (CDF).
# Here, we calculate the cumulative total probability of 
# receiving each cost, applying cumsum() to the
# probability (prob_cost) of each value (cost). 
# In this case, we’re basically saying, 
# we’re interested in all the costs, so don’t discount any.

# For instance, we can do the first step here,
# taking the cumulative probability of costs i through j....
mypd['prob_cost_cumulative'] = mypd.prob_cost_i.cumsum()
mypd.head(3)

# Our prob_cost_cumulative in row 3 
# above shows the total probability of n = 3 patients
# receiving a cost of 1126 OR 1136 OR 1146. 
# But, we want an average estimate for 1 patient.
# So, like in a weighted average, 
# we can divide by the total probability of
# all (n) hypothetical patients in the probability density
# function receiving any of these costs. 
# This gives us our revised prob_cost_cumulative, 
# which ranges from 0 to 1!

# For instance, we can do the first step here,
mycd = mypd
# taking the cumulative probability of costs i through j....
mycd['prob_cost_cumulative'] = mycd.prob_cost_i.cumsum() / mycd.prob_cost_i.sum()
# We can also then identify the segment that is extreme!
mycd['prob_extreme'] = mycd.prob_cost_cumulative * mycd.prob_extreme_i

# Take a peek at the tail!
mycd.tail(3)


# Let’s visualize mycd, our cumulative probabilities!


viz_cd = ( ggplot() +
  # Show the cumulative probability of each cost, 
  # shaded by whether it is "extreme" (cost >= stat)  or not
  geom_area(data = mycd, mapping = aes(x = 'cost', y = 'prob_cost_cumulative', fill = 'prob_extreme_i')) +
  # Show cumulative probability of getting an extreme cost
  geom_area(data = mycd, mapping = aes(x = 'cost', y = 'prob_extreme', fill = 'prob_extreme_i'))  +
  # Show the 16th patient's cost
  geom_vline(xintercept = stat, color = "red", size = 3) +
  # Add formatting
  theme_classic() +
  labs(x = "Cost of Hospital Stays (n = 15)", y = "Cumulative Probability of Cost",
       fill = "P(Extreme i)",
       title = "Cumulative Distribution Function for Cost of Hospital Stays",
       subtitle = "Probability of Cost more Extreme than $3000 = 0.36")
)

viz_cd
# (Note: I've added some more annotation to mine in the textbook 
# than your image will have - don't worry!)


# But wouldn’t it be handy if we could just
# make a literal cumulative distribution function, 
# just like we did for the probability density function dobs()?

pobs = tidy_density(density(obs), n = 1000)
# Sort from smallest to largest
pobs = pobs.sort_values(by='x')
# take cumulative sum, divided by total probability
pobs['y'] = pobs.y.cumsum() / pobs.y.sum()
# Make cumulative distribution function pobs()!
pobs = approxfun(pobs)
# Test it out!
1 - pobs(3000)

# Pretty close to our probability we calculated before!


# Clean up
del stat, mycd, p, viz_cd




# Using Calculus #############################

# We can write that up in a function, which we will call pdf.
# For every x value we supply, it will compute that equation 
# to pedict that value’s relative refequency/probability.

# Write out our nice polynomial function
def pdf(x):
  return -2/10**7 + 25/10**8*x + -45/10**12*x**2

# Check it!
x = pd.Series([2000, 3000])
pdf(x)

# The figure below demonstrates that it approximates 
# the true density relatively closely.

# We're going to add another column to our mypd dataset,
# approximating the probability of each cost with our new pdf()
mypd['prob_cost_i2'] = pdf(mypd.cost)
mypd['color1'] = 'from raw data'
mypd['color2'] = 'from function'
(ggplot() +
  geom_line(data = mypd, mapping = aes(x = 'cost', y = 'prob_cost_i', color = "color1")) +
  geom_line(data = mypd, mapping = aes(x = 'cost', y = 'prob_cost_i2', color = "color2")) +
  theme_classic() +
  labs(x = "Cost", y = "Probability", color = "Type")
)


# So how do we generate the cumulative density function? 
# The sympy package can help us.

# D() computes the derivative of a function (Eg. CDF -> PDF)
# antiD() computes its integral (Eg. PDF -> CDF)

lifespan = rnorm(100, mean = 5, sd = 1)

# Make x symbolic
x = sp.symbols('x')
# Get symbolic density function in terms of x
d = pdf(x)

# Get integral of d(x) with regards to x
cdf = sp.integrate(d, x)

# Solve for x = 2, by substituting 2 for x then evaluating the function.
cdf.subs(x, 2).evalf()
# Multiple values of x? Then try a apply() or a for-loop.
# Using apply...
obs.apply( pd.Series( lambda value: cdf.subs(x, value).evalf()     )  )
# Using a for-loop...
pd.Series([cdf.subs(x, value).evalf() for value in obs])
# (Note: Our function is not a perfect fit for the data, so probabilities exceed 1!)

# Let's compare our cdf() function made with calculus with pobs(), our computationally-generated CDF function. 
pobs(obs)
# Pretty similar results. The differences are due the fact that our original function is just an approximation,
# rather than dobs(), which is a perfect fit for our densities.


# And we can also take the derivative of our cdf() function with D() to get back our pdf(),
# which we’ll call pdf2().

# Make x symbolic
x = sp.symbols('x')
# Get derivative of cdf(x) with regards to x
pdf2 = sp.diff(cdf, x)

# compare results
pdf(obs[0]) # original PDF
pdf2.subs(x, obs[0]).evalf() # calculus-based PDF 

del mypd, pdf, pdf2, cdf, obs



# Learning Check 2 #################################

#Question

# A month has gone by, and our hospital has now billed 30 patients. 
# You’ve heard that hospital bills at or above $3000 a day may somewhat
# deter people from seeking future medical care, while bills at or above $4000 
# may greatly deter people from seeking future care. (These numbers are hypothetical.)

# Using the vectors below, please calculate the following, using a PDF or CDF.
# 
# What’s the probability that a bill might somewhat deter a patient from going to the hospital?
# 
# What’s the probability that a bill might greatly deter a patient from going to the hospital?
# 
# What’s the probability that a patient might be somewhat deterred but not greatly deterred from going to the hospital?
# 
# Note: Assume that the PDF matches the range of observed patients.
# 

# Let's record our vector of 30 patients
patients = [1126, 1493, 1528, 1713, 1912, 2060, 2541, 2612, 2888, 2915, 3166, 3552, 3692, 3695, 4248,
         3000, 3104, 3071, 2953, 2934, 2976, 2902, 2998, 3040, 3030, 3021, 3028, 2952, 3013, 3047]
# And let's get our statistics to compare against
somewhat = 3000
greatly = 4000

# Pandify it
patients = pd.Series(patients)
# Get probability density function for our new data
dobs2 = approxfun(tidy_density(density(patients)))

# Get probability densities
mypd2 = pd.DataFrame({'cost': seq(patients.min(), patients.max(), by = 10)})
mypd2['prob_cost_i'] = dobs2(mypd2.cost)

# Calculate probability of being somewhat deterred
mypd2['prob_somewhat_i'] = mypd2.cost >= somewhat
mypd2['prob_greatly_i'] = mypd2.cost >= greatly
mypd2['prob_somewhat_not_greatly_i'] = (mypd2.cost >= somewhat) & (mypd2.cost < greatly)
mypd2


# To calculate these probabilities straight from the probability densities, do like so:

pd.DataFrame({
  'prob_somewhat': [ sum(mypd2.prob_cost_i * mypd2.prob_somewhat_i) / sum(mypd2.prob_cost_i) ],
  'prob_greatly': [ sum(mypd2.prob_cost_i * mypd2.prob_greatly_i) / sum(mypd2.prob_cost_i) ],
  'prob_somewhat_not_greatly': [ sum(mypd2.prob_cost_i * mypd2.prob_somewhat_not_greatly_i) / sum(mypd2.prob_cost_i) ]
})

# To calculate these probabilities from the cumulative distribution functions, we can do the following:

mycd2 = mypd2 
mycd2['prob_somewhat'] = mycd2.prob_cost_i.cumsum() * mycd2.prob_somewhat_i / sum(mycd2.prob_cost_i)
mycd2['prob_greatly'] = mycd2.prob_cost_i.cumsum() * mycd2.prob_greatly_i / sum(mycd2.prob_cost_i)
mycd2['prob_somewhat_not_greatly'] = mycd2.prob_cost_i.cumsum() * mycd2.prob_somewhat_not_greatly_i / sum(mycd2.prob_cost_i)

mycd2.tail(3)

mycd2['color1'] = 'Very Little'
mycd2['color2'] = 'Somewhat-not-Greatly'
mycd2['color3'] = 'Greatly'
mycd2['prob_cost_cumulative_i'] = mycd2.prob_cost_i.cumsum() / mycd2.prob_cost_i.sum()

(ggplot() +
  # Get cumulative probability generally
  geom_area(data = mycd2, mapping = aes(x = 'cost', y = 'prob_cost_cumulative_i',
                                         fill = "color1")) +
  # Get cumulative probability if somewhat but not greatly
  geom_area(data = mycd2, mapping = aes(x = 'cost', y = 'prob_somewhat_not_greatly', 
                                         fill = "color2")) +
  # Get cumulative probability if greatly
  geom_area(data = mycd2, mapping = aes(x = 'cost', y = 'prob_greatly', 
                                         fill = "color3")) +
  theme_classic() +
  labs(x = "Cost of Hospital Stay (n = 30)",
       y = "Cumulative Probability",
       subtitle = "Probability of Hospital Bill Deterring Future Hospital Visits",
       fill = "Deter Future Visits")
)


# Conclusion
# And that’s a wrap! Nice work! 
# You can now figure out a lot of things about the world 
# if you (a) can guess their distribution and 
# (b) have one or two statistics about that distribution. Here we go!

globals().clear()
