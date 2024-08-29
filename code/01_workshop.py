# Upgrade pip
# !/opt/python/3.8.17/bin/python3.8 -m pip install --upgrade pip
#
# Install main python packages for this course
# !pip install pandas
# !pip install scipy
# !pip install statsmodels
# !pip install patsy
# !pip install plotnine
# !pip install dplython
# !pip install dfply

# Print hello world!
print("hello world")

# Import libraries
import pandas as p # Import pandas 
from dfply import * # Import all dfply functions
from plotnine import * # Import all plotnine functions


# Addition
1+2

# Vector
[1,2,3,4,5]

# Subtraction
5 - 2

# Multiplication
2 * 3

# Division
15 / 5

# Exponents
2**2

# Square Root
16**0.5

# Order of Operations
2 * 2 - 5

# Use parentheses!
2 * (2 - 5)


# Eg.
64**.5
64**(1/3)
8**2

# Types of Data in R


2 # this is a value
"x" # this is a vlue

myvalue = 2

secondvalue = myvalue + 2

# In RStudio, you can just print the values to console, 
# without using the print() command.
secondvalue


# Vectors
[1,2,3]
["Boston", "New York", "Los Angeles"]


# Here's a vector of (hypothetical) seawall heights in 10 towns.
myheights = [4, 4.5, 5, 5, 5, 5.5, 5.5, 6, 6.5, 6.5]

# And here's a list of hypothetical names for those towns
mytowns = ["Gloucester", "Newburyport", "Provincetown", 
             "Plymouth", "Marblehead", "Chatham", "Salem", 
             "Ipswich", "Falmouth", "Boston"]

# And here's a list of years when those seawalls were each built.
myyears = [1990, 1980, 1970, 1930, 1975, 1975, 1980, 1920, 1995, 2000]

# To manipulate them, we'll need to bundle them into pandas objects.


# let's bundle them into a data.frame with pandas.
sw = p.DataFrame({'height': myheights, 'town': mytowns, 'year':myyears})
# Add 2 to all the heights
sw.height + 2

# Or just make it a series, and then add 2.
p.Series(myheights) + 2


# Element-wise multiplication
p.Series(myheights) * p.Series(myheights)
 # or
sw.height * sw.height

# Matrix Multiplication...
sw.height.dot(sw.height)


# Descriptive Stats
sw.height.mean()
sw.height.median()
sw.height.min()
sw.height.max()
sw.height.mode()
sw.height.quantile(q = 0.5)




# Here's a brief test of using dplyr-style functions
# with dfply
# diamonds is a dataset loaded within dfply

# Select just one column
sw >> \
  select(X.height)

# Mutate a column
sw >> \
  mutate(y = X.height ** X.height)


# Summarize a data.frame
sw >>\
  summarize(mean_value = mean(X.height) ) 

# Get the mean price per diamond cut
diamonds >>\ 
  group_by(X.cut) >>\
  summarize(price = mean(X.price ))

diamonds >>\
  arrange(X.price, ascending=False) >>\
  head()


# Filtering
diamonds >>\
  mask(X.carat < 0.23) >>\
  head()


diamonds >>\
  rename(CUT=X.cut, COLOR='color')


diamonds >>\
  arrange('color')
  
diamonds >>\
  group_by('cut') >>\
  summarize(price = mean(X.price))

diamonds >>\
  gather()


# Clear environment
globals().clear()

