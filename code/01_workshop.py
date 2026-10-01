# 01_workshop.py
# Tim Fraser
# Workshop 1: Introduction - basic operations in Python
# Chapter: Coding in Python
#
# HOW TO RUN: run this script LINE BY LINE, not all at once - it contains three
# DELIBERATE errors (they are the point: they teach you to read Python's error
# messages). Here each one sits inside try/except, so the whole file still runs.
#
# Check out timothyfraser.com/sigma for more.

# Let's load some packages
# !pip install pandas # install pandas
# !pip install dfply # install dfply
import pandas as p # turn on pandas
from dfply import * # turn on dfply

# Comments!
# This is addition!
1+2

1+2
1*5
2**3
(2*3)
((2*2)+3)

4**0.5
4**(1/2)
4**(1/3)
p.Series([4]).pow(0.5)





myobject = p.Series([1,2,3,4,5])

myobject

myobject + 1

myobject *2

# Heads up: this next line is SUPPOSED to fail. Run it anyway, and read what Python
# says back to you - you can't add 1 to words. That error message is the lesson.
try:
    p.Series(["corgi", "dalmatian", "terriers"]) + 1
except TypeError as e:
    print(e)
["corgi", "dalmatian", "terriers", 1]



d = p.DataFrame({
  'doggies': ["corgis", "dalmatians", "terriers"],
  'count': [5, 3, 2]
})

d['count']
d['count'] + 1
d['count'] + d['count']

d['count'] = d['count'] + 1

# Not this!
# d = d['count'] + 1

# dataframe.iloc[row,column]
d.iloc[0,0]
d.iloc[2,1]
d.iloc[2, :]
d.iloc[:, 1]

# adding columns
d['weight'] = [100, 40, 20]

d['weight2'] = [100, 40, None]

# using pandas function concat()
p.concat([
  p.DataFrame({'x': [1,2], 'y': [3,4]}),
  p.DataFrame({'x': [3,4], 'y': [5,6]})
])
p.concat([
  p.DataFrame({'x': [1,2], 'y': [3,4], 'z': [3,4]}),
  p.DataFrame({'x': [3,4], 'y': [5,6]})
])
# from pandas package
p.DataFrame(
  {'x': [1,2], 'y': [3,4], 'z': [3,4]}
)


d = d.drop(columns = 'weight2')

# Heads up: this next line is SUPPOSED to fail too. We just deleted weight2
# above, so there is nothing left to drop. Python tells you exactly that:
# "not found in axis." Deleting a column is permanent -
# that error is how you find out you already did it.
try:
    d.drop(columns = 'weight2')
except KeyError as e:
    print(e)






[1,2,3,4]

# Heads up: this next line is SUPPOSED to fail, for the same reason as the one
# up at the top. Dividing is arithmetic, and these are words - it fails
# no matter what. Compare it to the line just below it.
try:
    p.Series(["corgi", "dalmatian"]) / 2
except TypeError as e:
    print(e)

p.Series([1,2,3,4]) * 2

p.Series([1,2,3,4]) * p.Series([1,2,3,4])

p.Series([1,2,3,4]).dot(p.Series([1,2,3,4]))


64**0.5
64**(1/3)
8**2






coffee = p.Series([2, 4, 5, 6, 7, 3,2, 3,4])
coffee

sales = p.Series([3.4,2.5, 3.2, 6.3, 4, 3, 6, 7, 8])
sales

coffee * 2

# coffees per dollar
coffee / sales
# dollars per coffee
sales / coffee



# Let's try working with DataFrames.

p.DataFrame({'coffee': coffee, 'sales': sales})

dat = p.DataFrame({'coffee': coffee, 'sales': sales})

dat

# We can index specific values, rows, and columns...
dat.iloc[:,0]
dat.iloc[0,:]
dat.iloc[0:3,:]
dat.iloc[:, 0:2]




# And we can use dfply functions to do actions to dataframes.
#    >>



dat[['coffee']]
dat >> select(X.coffee)

dat.head(2)
dat >> select(X.coffee) >> head(2)


dat >> \
  select(X.coffee) >> \
  head(2)


dat >> \
  select(X.coffee) >> \
  row_slice([0, 1])

dat >> \
  select(X.coffee) >> \
  mask(X.coffee > 4)


dat >> \
  mask(X.coffee == 4)
dat >> \
  mask(X.coffee >= 4)
dat >> \
  mask(X.coffee <= 4)

dat >> \
  mask(X.coffee.isin([4, 5]))

dat >> \
  summarize(avg = mean(X.coffee))

# find the average and the standard deviation - yeah!
dat >> \
  summarize(avg = mean(X.coffee),
            stdev = sd(X.coffee))

p.DataFrame({
  'adorable': [1, 0],
  'glasses': ["yes", "no"]
})

# get 2000 values
nums = p.DataFrame({'x': range(1, 2001)})
nums # only shows the first and last few values
# if you assign you get no output...
num2 = nums >> row_slice(list(range(999, 1003)))


# Clear my environment
# WARNING: this WIPES everything you have made so far. Skip it if you want to
# keep the objects above.
globals().clear()

# Here's a brief test of using dplyr-style functions
# with dfply
# diamonds is a dataset loaded within dfply
import pandas as p
from dfply import *

# Get the mean price per diamond cut
diamonds >> \
  group_by(X.cut) >> \
  summarize(price = mean(X.price ))

# Arranging
diamonds >> \
  arrange(X.price) >> \
  head()


# Filtering
diamonds >> \
  mask(X.carat < 0.23) >> \
  head()


diamonds >> \
  rename(CUT = X.cut, COLOR='color')


diamonds >> \
  arrange(X.color)

diamonds >> \
  group_by(X.cut) >> \
  summarize(price = mean(X.price))



# We can clean up using globals().clear()
# WARNING: this WIPES everything you have made so far. Skip it if you want to
# keep the objects above.
globals().clear()
