# 01_training.py
# Training: Coding in Python!
# Pairs with R training:
# https://timothyfraser.com/sigma/coding-in-r.html
# Tim Fraser

# Upgrade pip
# !/opt/python/3.8.17/bin/python3.8 -m pip install --upgrade pip
#
# Install main python packages for this course

# !pip install sys
# !pip install os
# !pip install scipy
# !pip install dplython
# !pip install dfply
# !pip install statsmodels
# !pip install pybroom
# !pip install plotnine

# Let's try a test!
print("hello world")

# Okay! let's get into the habit of 
# importing our packages, functions, 
# and data at the top of your script.

# Packages #################################
import pandas as p  # import pandas
from dfply import * # import dplyr equivalent and pipeline

# Basic Calculations in Python ########################

# Addition
1+5

# Subtraction
5 - 2

# Multiplication
2 * 3

# Division
15 / 5

# Exponents
2**2
# Eg.
64**.5
64**(1/3)
8**2


# Square Root
16**0.5


# Order of Operations
2 * 2 - 5

# Use parentheses!
2 * (2 - 5)


# Types of Values in Python #####################

# Numeric Values
15000

# Character Strings 
'Coding!'

# Types of Data #############################

2 # this is a value

'x' # is also a value

# You can save a value as an object
myvalue = 2
# Highlight the next line, press CTRL ENTER, and see what pops out!
myvalue

# In RStudio, you can just print the values to console, 
# without using the print() command.

# That's right - we can access the contents of our objects by 'calling' their name.

# You can overwrite values
myvalue = 'I overwrote it!'
myvalue # test it



# We can remove a single object using 'del'
del myvalue

# Or clear everything using globals().clear()
# globals().clear()


# Vectors ########################

# Python contains values in vectors, which are sets of values

# This is numeric vector
[1,4,8]

# This is a character vector
["Boston", "New York", "Los Angeles"]

# In Python, you CAN mix numeric and character values in the same vector...
# but it doesn't really make sense. Try to avoid.
[1, "Boston", 2]

# Series ##############################
# You'll probably need to convert your vector into a Pandas Series to do operations on it.
p.Series([1,2,3,4] ) * 2

p.Series([1,2,3,4] ) + 2

# We can save vectors as objects too....

# Here's a vector of (hypothetical) seawall heights in 10 towns.
myheights = p.Series([4, 4.5, 5, 5, 5, 5.5, 5.5, 6, 6.5, 6.5])
# And here's a list of hypothetical names for those towns
mytowns = ["Gloucester", "Newburyport", "Provincetown", 
             "Plymouth", "Marblehead", "Chatham", "Salem", 
             "Ipswich", "Falmouth", "Boston"]
# And here's a list of years when those seawalls were each built.
myyears = p.Series([1990, 1980, 1970, 1930, 1975, 1975, 1980, 1920, 1995, 2000])

# Plus, we can still do operations on entire vectors!
myyears + 1

# Dataframes ################################################3

# Then, you can bundle vectors into pandas DataFrames.

# Must be vectors of equal length
p.DataFrame({ 'height': myheights, 'town': mytowns, 'year': myyears })

# Let's name our data.frame about seawalls 'sw'
sw = p.DataFrame({ 'height': myheights, 'town': mytowns, 'year': myyears })

# Check contents 
sw


# Although, we could do this too, and it would be equivalent:
sw = p.DataFrame({
 # It's okay to split code across multiple lines.
 # It keeps things readable.
 'height': p.Series([4, 4.5, 5, 5, 5, 
            5.5, 5.5, 6, 6.5, 6.5]),
 'town': ["Gloucester", "Newburyport", "Provincetown", 
          "Plymouth", "Marblehead", "Chatham", "Salem",
          "Ipswich", "Falmouth", "Boston"],
 'year': p.Series( [1990, 1980, 1970, 1930, 1975, 
          1975, 1980, 1920, 1995, 2000]) 
          })
sw # view it


# But what if we want to work with the vectors again? 
sw.height # access height vector
# Edit
sw.height + 1

# Update
# sw.height = sw.height + 1
sw


# Common Functions in Python

## Measures of Central Tendency 

# Mean seawall height
sw.height.mean()

# Median seawall height
sw.height.median()

# total meters of seawall height!
sw.height.sum()


## Measures of Dispersion 

# Smallest seawall height
sw.height.min()

# Tallest seawall height
sw.height.max()

# Modal seawall height
sw.height.mode()

# Range
[sw.height.min(), sw.height.max()]


# Percentiles
sw.height.quantile(q = 0.25) # 25th percentile
sw.height.quantile(q = 0.75) # 75th percentile

# Standard deviation of seawall heights
sw.height.std()

# Variance of seawall heights
sw.height.var()

## Other Good Functions ###############################

# Length of a pandas series
len(sw.height)
# Total rows in a pandas data.frame
len(sw)

# Dimensions of a pandas data.frame, as a vector
sw.shape

sw.shape[0] # zeroth element is rows
sw.shape[1] # first element is columns

# Missing Data ######################################

# Creating a Pandas Series with missing data using p.NA (or whatever you call pandas)
p.Series([4, 4.5, 5, 5, 5, 5.5, 5.5, 6, 6.5, 6.5, p.NA])

# Pandas is smart though, so it can still calculate the mean while containing NAs.
p.Series([4, 4.5, 5, 5, 5, 5.5, 5.5, 6, 6.5, 6.5, p.NA]).mean()


# Pipelines ############################################

# In Python, there's not really a clear equivalent for the pipeline from R.
# We'll mostly use the . syntax from pandas.


# Visualizing Data with Histograms #######################

# In this course, we're going to use plotnine for visualization.
# This is a direct port of ggplot into Python.
# We use it because it's a super duper powerful visualization tool,
# with a very logical syntax.

# At the top of this script, you installed your packages using pip.
# Let's load a few.

import pandas as p  # import pandas
from dfply import * # import dplyr equivalent and pipeline
from plotnine import * # import ggplot equivalent


# Create 30 cities, ten per state (MA, RI, ME)
allsw = p.DataFrame({
  'height': [4, 4.5, 5, 5, 5.5, 5.5, 5.5, 6, 6, 6.5,
             4, 4,4, 4, 4.5, 4.5, 4.5, 5, 5, 6,
             5.5, 6, 6.5, 6.5, 7, 7, 7, 7.5, 7.5, 8],
  'states': ["MA","MA","MA","MA","MA","MA","MA","MA","MA","MA",
             "RI","RI","RI","RI","RI","RI","RI","RI","RI","RI",
             "ME","ME","ME","ME","ME","ME","ME","ME","ME","ME"]
})

allsw # view


# Let's make a quick histogram using ggplot (plotnine)

# Make a blank plot with ggplot(), mapping variables to aesthetics (eg. x)
ggplot(data = allsw, mapping = aes(x = 'height')) + \
  # line break with \
  # then plot features onto those aesthetics
  geom_histogram()

# Or for short:
ggplot(allsw, aes('height')) + geom_histogram()

# Let's make a more extended histogram!

# For long ones, it might be helpful 
# to wrap the whole expression in parentheses.

# Tell the ggplot function to...
(ggplot(
  # draw data from the 'allsw' data.frame 
  data = allsw, 
  # and 'map' the vector 'height' to be an 'aes'thetic on the 'x'-axis.
  mapping = aes(x = 'height')) + \
  
  # make histograms of distribution, 
  geom_histogram(
    # With white outlines
    color = "white",
    # With blue inside fill
    fill = "steelblue", 
    # where every half meter gets a bin (binwidth = 0.5)
    binwidth = 0.5) + \
  # add labels
  labs(x = "Seawall Height", y = "Frequency (# of cities)") 
) 
    
# Repeat code from before...
(
ggplot(data = allsw, mapping = aes(x = 'height')) +
  geom_histogram(color = "white", fill = "steelblue", binwidth = 0.5) +
  labs(x = "Seawall Height", y = "Frequency (# of cities)") +
    # But split into multiple panels by state!
  facet_wrap(facets = '~states')
) 


# Clear environment
globals().clear()
