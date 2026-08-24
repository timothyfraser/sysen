# 01_workshop.py
# Tim Fraser
# Workshop 1: Coding in Python
# Chapter: Coding in Python


# Getting Started ---------------------------------------------------------

## Installing packages ----
# Upgrade pip
# !python -m pip install --upgrade pip
#
# This course pins its Python packages in functions/requirements.txt.
# Install them all at once:
# !pip install -r functions/requirements.txt
#
# Or install the main packages for this course one at a time:
# !pip install pandas==2.3.3
# !pip install scipy==1.16.3
# !pip install statsmodels==0.14.5
# !pip install patsy==1.0.2
# !pip install plotnine==0.15.1
# !pip install dfply==0.3.3

# Print hello world!
print("hello world")

## Importing packages ----
import pandas as p # Import pandas
from dfply import * # Import all dfply functions
from plotnine import * # Import all plotnine functions


# Basic Calculations ------------------------------------------------------

# Addition
print(1+2)

# Vector
print([1,2,3,4,5])

# Subtraction
print(5 - 2)

# Multiplication
print(2 * 3)

# Division
print(15 / 5)

# Exponents
print(2**2)

# Square Root
print(16**0.5)

# Order of Operations
print(2 * 2 - 5)

# Use parentheses!
print(2 * (2 - 5))


# Eg.
print(64**.5)
print(64**(1/3))
print(8**2)


# Types of Data in Python -------------------------------------------------

## Values and variables ----

print(2) # this is a value
print("x") # this is a value

myvalue = 2

secondvalue = myvalue + 2

# In Positron, you can just print the values to console,
# without using the print() command.
print(secondvalue)


## Lists (like R vectors) ----
print([1,2,3])
print(["Boston", "New York", "Los Angeles"])


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
print(sw.height + 2)

# Or just make it a series, and then add 2.
print(p.Series(myheights) + 2)


# Element-wise multiplication
print(p.Series(myheights) * p.Series(myheights))
 # or
print(sw.height * sw.height)

# Matrix Multiplication...
print(sw.height.dot(sw.height))


# Common Functions in Python ----------------------------------------------

# Descriptive Stats
print(sw.height.mean())
print(sw.height.median())
print(sw.height.min())
print(sw.height.max())
print(sw.height.mode())
print(sw.height.quantile(q = 0.5))


# The Pipeline ------------------------------------------------------------

# Here's a brief test of using dplyr-style functions
# with dfply
# diamonds is a dataset loaded within dfply

## Select, mutate, summarize ----

# Select just one column
print(sw >> \
  select(X.height))

# Mutate a column
print(sw >> \
  mutate(y = X.height ** X.height))


# Summarize a data.frame
print(sw >>\
  summarize(mean_value = mean(X.height) ))

## Grouping, arranging, filtering ----

# Get the mean price per diamond cut
print(diamonds >>\
  group_by(X.cut) >>\
  summarize(price = mean(X.price )))

print(diamonds >>\
  arrange(X.price, ascending=False) >>\
  head())


# Filtering
print(diamonds >>\
  mask(X.carat < 0.23) >>\
  head())


print(diamonds >>\
  rename(CUT=X.cut, COLOR='color'))


print(diamonds >>\
  arrange('color'))

print(diamonds >>\
  group_by('cut') >>\
  summarize(price = mean(X.price)))

## Reshaping ----

# gather() stacks several columns into key-value pairs.
# Unlike R's tidyr, dfply's gather() requires you to name
# the key column, the value column, and the columns to stack.
print(diamonds >>\
  gather('measure', 'value', ['x', 'y', 'z']) >>\
  head())


# Clear environment
globals().clear()
