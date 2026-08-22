# 01_workshop.py
# Tim Fraser
# Workshop 1: Coding in Python
# Chapter: Coding in Python


# Getting Started ---------------------------------------------------------

## Installing packages ----
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

## Importing packages ----
import pandas as p # Import pandas
from dfply import * # Import all dfply functions
from plotnine import * # Import all plotnine functions


# Basic Calculations ------------------------------------------------------

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


# Types of Data in Python -------------------------------------------------

## Values and variables ----

2 # this is a value
"x" # this is a value

myvalue = 2

secondvalue = myvalue + 2

# In Positron, you can just print the values to console,
# without using the print() command.
secondvalue


## Lists (like R vectors) ----
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


## DataFrames with pandas ----

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


# Common Functions in Python ----------------------------------------------

# Descriptive Stats
sw.height.mean()
sw.height.median()
sw.height.min()
sw.height.max()
sw.height.mode()
sw.height.quantile(q = 0.5)


# The Pipeline ------------------------------------------------------------

# Here's a brief test of using dplyr-style functions
# with dfply
# diamonds is a dataset loaded within dfply

## Select, mutate, summarize ----

# Select just one column
sw >> \
  select(X.height)

# Mutate a column
sw >> \
  mutate(y = X.height ** X.height)


# Summarize a data.frame
sw >>\
  summarize(mean_value = mean(X.height) )

## Grouping, arranging, filtering ----

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

## Reshaping ----

# gather() stacks several columns into key-value pairs.
# Unlike R's tidyr, dfply's gather() requires you to name
# the key column, the value column, and the columns to stack.
diamonds >>\
  gather('measure', 'value', ['x', 'y', 'z']) >>\
  head()


# Clear environment
globals().clear()
