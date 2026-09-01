# 07b_workshop.py
# Tim Fraser
# Lesson 7B: Statistical Techniques for Exponential Distributions
# Chapter: Statistical Techniques for Exponential Distributions in Python

# Workshop code paired with the textbook chapters
# "Useful Life Distributions (Exponential)" and
# "Statistical Techniques for Exponential Distributions in Python"
# at timothyfraser.com/sigma.

# What this script does:
# Takes a vector of 100 product times-to-failure and works out, step by
# step, how to crosstabulate them into intervals - first by hand with
# pd.cut() and groupby().size(), then as our own crosstab() function, then
# handling the awkward case where an interval holds fewer than 5 failures.
# Those interval counts are what a chi-squared goodness-of-fit test needs.

# Inputs: none from disk for the first half - the failure times are typed in
#         below. The second half loads functions/functions_crosstab.py.
# Packages: pandas, numpy, plotnine

# Load packages
import pandas as pd
import numpy as np
from plotnine import *
import os, sys
sys.path.append(os.path.abspath('functions'))

# 1. Times to failure ##########################################

# Product Times to Failure
hours = [1,2,2,3,4,5,7,8,9,10,
         11,13,15,16,17,17,18,18,18,20,
         20,21,21,24,27,29,30,37,40,40,
         40,41,46,47,48,52,54,54, 55,55,
         64,65,65,65,67,76,76,79,80,80,
         82,86,87,89,94,96,100,101,102,104,
         105,109,109,120,123,141,150,156,156,161,
         164,167,170,178,181,191,193,206,211,212,
         214,236,238,240,265,304,317,328,355,363,
         365,369,389,404,427,435,500,522,547,889]


hours

# 2. Binning continuous times into intervals ###################

# R uses ggplot2::cut_interval(); Python uses pd.cut() with equal-width bins.
# right=True matches R's (a, b] intervals (first bin is [a, b]).

def cut_interval(x, length=55):
    x = np.asarray(x)
    max_x = x.max()
    bins = np.arange(0, max_x + length + 1, length)
    return pd.cut(x, bins=bins, right=True, include_lowest=True)

cut_interval(hours, length=55)

pd.to_numeric(hours)
[str(h) for h in hours]
pd.Categorical(hours)


pd.Categorical(["cats", "birds", "birds", "dogs"])

pd.Categorical(["cats", "birds", "birds", "dogs"],
               categories=["cats", "birds", "dogs"])


tab = pd.DataFrame({'t': hours})
tab['interval'] = cut_interval(hours, length=55)
tab.sort_values('interval', ascending=False)

tmax = 1000

# 3. Tallying up failures per interval #########################

# Three equivalent ways to tally up observations

(pd.DataFrame({'t': hours})
 .assign(interval=cut_interval(hours, length=55))
 .groupby('interval', observed=False)
 .agg(r_obs=('t', 'size'))
 .reset_index())


(pd.DataFrame({'t': hours})
 .assign(interval=cut_interval(hours, length=55))
 .groupby('interval', observed=False)
 .size()
 .reset_index(name='r_obs'))


(pd.DataFrame({'t': hours})
 .assign(interval=cut_interval(hours, length=55))
 .groupby('interval', observed=False)
 .agg(r_obs=('t', lambda t: (t < tmax).sum()))
 .reset_index())



# But if we want to hold onto the categories with zero observations,
# we need observed=False (R's .drop = FALSE)
(pd.DataFrame({'t': hours})
 .assign(interval=cut_interval(hours, length=55))
 .groupby('interval', observed=False)
 .size()
 .reset_index(name='r_obs'))




# 4. Bundling it into a crosstab() function ####################

# We can write ourselves a crosstab() function to do it for us
def crosstab(x, binsize=55):
    return (pd.DataFrame({'t': x})
            .assign(interval=cut_interval(x, length=binsize))
            .groupby('interval', observed=False)
            .size()
            .reset_index(name='r_obs'))

# Yay!
tab = crosstab(hours, binsize=100)

tab

# 5. The r >= 5 problem: merging sparse intervals ##############

# But hang on = some intervals have fewer than 5 failures per interval.

# We could recode the intervals
# and then aggregate the number of failures using the new intervals

# To do so, we can use np.where / a dict — Python's case_when
tab2 = tab.copy()
tab2['interval'] = tab2['interval'].astype(str)
tab2['interval'] = tab2['interval'].replace({
    '(500, 600]': '(400, 500]',
    '(600, 700]': '(400, 500]',
    '(700, 800]': '(400, 500]',
    '(800, 900]': '(400, 500]',
})
# But it needs to be remade into a
# categorical again to remember interval order
levels = ['[0, 100]', '(100, 200]',
          '(200, 300]', '(300, 400]', '(400, 500]',
          '(500, 600]', '(600, 700]',
          '(700, 800]', '(800, 900]']
tab2['interval'] = pd.Categorical(tab2['interval'], categories=levels, ordered=True)

# Then, we can aggregate to the revised intervals
tab3 = (tab2.groupby('interval', observed=False)
        .agg(r_obs=('r_obs', 'sum'))
        .reset_index())

# We could finish up like this
binsize = 100
tab3 = tab3.copy()
tab3['bin'] = tab3['interval'].cat.codes + 1
tab3['lower'] = (tab3['bin'] - 1) * binsize
tab3['upper'] = tab3['bin'] * binsize
tab3['midpoint'] = (tab3['lower'] + tab3['upper']) / 2
tab3



# We could try to make our own function to do it all...
def crosstab2(x, binsize=100, midpoint=450, interval='(400,500]', binid=5):
    data = (pd.DataFrame({'t': x})
            .assign(interval=cut_interval(x, length=binsize))
            .groupby('interval', observed=False)
            .size()
            .reset_index(name='r_obs'))

    data['bin'] = data['interval'].cat.codes + 1
    data['lower'] = (data['bin'] - 1) * binsize
    data['upper'] = data['bin'] * binsize
    data['midpoint'] = (data['lower'] + data['upper']) / 2

    mask = data['midpoint'] >= midpoint
    data['interval'] = data['interval'].astype(str)
    data.loc[mask, 'interval'] = interval
    data.loc[mask, 'bin'] = binid

    output = (data.groupby(['bin', 'interval'], observed=True)
              .agg(r_obs=('r_obs', 'sum'))
              .reset_index())

    output['lower'] = (output['bin'] - 1) * binsize
    output['upper'] = output['bin'] * binsize
    output['midpoint'] = (output['lower'] + output['upper']) / 2
    return output[['bin', 'interval', 'midpoint', 'r_obs']]

# It works so-so.
crosstab2(x=hours, binsize=100,
          midpoint=450, interval='(400,500]', binid=5)




# 6. Use the packaged helper instead ###########################

# I went on to update this and have provided a helper function under
# functions/functions_crosstab.py
# Try it out!
from functions_crosstab import crosstab


# Product Times to Failure
hours = [1,2,2,3,4,5,7,8,9,10,
         11,13,15,16,17,17,18,18,18,20,
         20,21,21,24,27,29,30,37,40,40,
         40,41,46,47,48,52,54,54, 55,55,
         64,65,65,65,67,76,76,79,80,80,
         82,86,87,89,94,96,100,101,102,104,
         105,109,109,120,123,141,150,156,156,161,
         164,167,170,178,181,191,193,206,211,212,
         214,236,238,240,265,304,317,328,355,363,
         365,369,389,404,427,435,500,522,547,889]

# By default, it applies no cutoff.
crosstab(x=hours, binsize=100)
# But if you add a cutoff, it will aggregate categories past that cutoff
crosstab(x=hours, binsize=100, cutoff=450)





# Extra Examples ##############################################


# Try starting bin size of 55
extra = pd.DataFrame({'t': hours})
extra['label'] = cut_interval(extra['t'], length=55)
extra = (extra.groupby('label', observed=False)
         .size()
         .reset_index(name='r_obs'))
extra['bin'] = extra['label'].cat.codes + 1
extra['lower'] = (extra['bin'] - 1) * 55
extra['upper'] = extra['bin'] * 55
extra['midpoint'] = (extra['lower'] + extra['upper']) / 2
extra[['bin', 'label', 'midpoint', 'r_obs']]


# Let's functionify this...

def crosstab_hand(x, binsize=55):
    data = pd.DataFrame({'t': x})
    data['label'] = cut_interval(data['t'], length=binsize)
    data = (data.groupby('label', observed=False)
            .size()
            .reset_index(name='r_obs'))
    data['bin'] = data['label'].cat.codes + 1
    data['lower'] = (data['bin'] - 1) * binsize
    data['upper'] = data['bin'] * binsize
    data['midpoint'] = (data['lower'] + data['upper']) / 2
    return data[['bin', 'label', 'midpoint', 'lower', 'upper', 'r_obs']]



tab = crosstab_hand(hours, binsize=100)

# Edit your categories

tab = tab.copy()
tab['label'] = tab['label'].astype(str)
tab.loc[tab['midpoint'] >= 450, 'label'] = '(400,900]'
tab.loc[tab['midpoint'] >= 450, 'bin'] = 5

tab
tab = (tab.groupby(['bin', 'label'], observed=True)
       .agg(r_obs=('r_obs', 'sum'))
       .reset_index())
tab['lower'] = (tab['bin'] - 1) * 100
tab['upper'] = tab['bin'] * 100
tab['midpoint'] = (tab['lower'] + tab['upper']) / 2
tab = tab[['bin', 'label', 'midpoint', 'lower', 'upper', 'r_obs']]


lambda_hat = 0.00725
n = 100
tab['r_obs'].sum()

def f(t, lambda_):
    return 1 - np.exp(-lambda_ * t)

ingredients = tab.copy()
ingredients['f2'] = f(ingredients['upper'], lambda_hat)
ingredients['f1'] = f(ingredients['lower'], lambda_hat)
ingredients['prob'] = ingredients['f2'] - ingredients['f1']
ingredients['r_exp'] = ingredients['prob'] * n

ingredients[['label', 'f2', 'f1', 'prob', 'r_exp']]

# Try bin size of 100
(pd.DataFrame({'t': hours})
 .assign(label=lambda d: cut_interval(d['t'], length=100))
 .groupby('label', observed=False)
 .size()
 .reset_index(name='r_obs'))

# Try bin size of...
(pd.DataFrame({'t': hours})
 .assign(label=lambda d: cut_interval(d['t'], length=150))
 .groupby('label', observed=False)
 .size()
 .reset_index(name='r_obs'))
