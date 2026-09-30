# 07b_workshop.py
# Tim Fraser
# Lesson 7B: Statistical Techniques for Exponential Distributions
# Chapter: Statistical Techniques for Exponential Distributions in Python

# Workshop code paired with the textbook chapters
# "Useful Life Distributions (Exponential)" and
# "Statistical Techniques for Exponential Distributions in Python"
# at timothyfraser.com/sigma.

# This is the Python twin of 07b_workshop.R, section by section.
# Run it from the top of the sysen folder, so the file paths below work.

# What this script does:
# Takes a vector of 100 product times-to-failure and works out, step by
# step, how to crosstabulate them into intervals - first by hand with
# cut_interval() and a group-by count, then as our own crosstab() function,
# then handling the awkward case where an interval holds fewer than 5 failures.
# Those interval counts are what a chi-squared goodness-of-fit test needs.

# Inputs: none from disk for the first half - the failure times are typed in
#         below. The second half imports functions/functions_crosstab.py.
# Packages: numpy, pandas, plotnine

# Load packages
import sys
import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr in R)
from plotnine import *         # visuals (ggplot2 in R)

# NOTE: `lambda` is a reserved word in Python (it makes tiny anonymous
# functions), so we can't name a variable `lambda`. We write `lambda_` instead.


# ggplot2's cut_interval(t, length = binsize) makes equal-width bins
# that line up on multiples of binsize, closed on the right: [0,100], (100,200], ...
# plotnine has no cut_interval(), so this helper does the same with pd.cut().
# (Same helper as 07_recitation.py, plus R's labels, so that "[0,100]" and
# "(100,200]" read exactly as they do in R - we match on those labels below.)
def cut_interval(t, length):
    lo = np.floor(np.min(t) / length) * length
    hi = np.ceil(np.max(t) / length) * length
    breaks = np.arange(lo, hi + length, length)
    labels = [("[" if i == 0 else "(") + f"{breaks[i]:g},{breaks[i + 1]:g}]"
              for i in range(len(breaks) - 1)]
    return pd.cut(t, bins=breaks, labels=labels, right=True, include_lowest=True)


# 1. Times to failure ##########################################

# Product Times to Failure
hours = np.array([1,2,2,3,4,5,7,8,9,10,
                  11,13,15,16,17,17,18,18,18,20,
                  20,21,21,24,27,29,30,37,40,40,
                  40,41,46,47,48,52,54,54, 55,55,
                  64,65,65,65,67,76,76,79,80,80,
                  82,86,87,89,94,96,100,101,102,104,
                  105,109,109,120,123,141,150,156,156,161,
                  164,167,170,178,181,191,193,206,211,212,
                  214,236,238,240,265,304,317,328,355,363,
                  365,369,389,404,427,435,500,522,547,889])


print(hours)

# 2. Binning continuous times into intervals ###################

# Use our cut_interval() to recode values as categories
print(cut_interval(hours, length=55))

# as.numeric(), as.character() and as.factor() in R
print(hours.astype(float))
print(hours.astype(str))
print(pd.Categorical(hours))


# A factor in R is a Categorical in pandas.
# By default, its levels (categories) are sorted alphabetically...
print(pd.Categorical(["cats", "birds", "birds", "dogs"]))

# ...unless you say what order you want them in.
print(pd.Categorical(["cats", "birds", "birds", "dogs"],
                     categories=["cats", "birds", "dogs"]))


# arrange(desc(interval)) sorts by the category ORDER, not alphabetically
print(pd.DataFrame({"t": hours})
      .assign(interval=lambda df: cut_interval(df["t"], length=55))
      .sort_values("interval", ascending=False, kind="stable"))

tmax = 1000

# 3. Tallying up failures per interval #########################

# Three equivalent ways to tally up observations
# (observed=True drops empty intervals, like group_by() does in R by default)

# length(t) in R
print(pd.DataFrame({"t": hours})
      .assign(interval=lambda df: cut_interval(df["t"], length=55))
      .groupby("interval", observed=True)
      .agg(r_obs=("t", len))
      .reset_index())


# n() in R
print(pd.DataFrame({"t": hours})
      .assign(interval=lambda df: cut_interval(df["t"], length=55))
      .groupby("interval", observed=True)
      .size()
      .reset_index(name="r_obs"))

# sum(t < tmax) in R
print(pd.DataFrame({"t": hours})
      .assign(interval=lambda df: cut_interval(df["t"], length=55))
      .groupby("interval", observed=True)
      .agg(r_obs=("t", lambda t: (t < tmax).sum()))
      .reset_index())



# But if we want to hold onto the categories with zero observations,
# we need observed = False (the same as .drop = FALSE in R)
print(pd.DataFrame({"t": hours})
      .assign(interval=lambda df: cut_interval(df["t"], length=55))
      .groupby("interval", observed=False)
      .size()
      .reset_index(name="r_obs"))




# 4. Bundling it into a crosstab() function ####################

# We can write ourselves a crosstab() function to do it for us
def crosstab(x, binsize=55):
    return (pd.DataFrame({"t": x})
            .assign(interval=lambda df: cut_interval(df["t"], length=binsize))
            .groupby("interval", observed=False)
            .size()
            .reset_index(name="r_obs"))

# Yay!
tab = crosstab(hours, binsize=100)

print(tab)

# 5. The r >= 5 problem: merging sparse intervals ##############

# But hang on = some intervals have fewer than 5 failures per interval.

# We could recode the intervals
# and then aggregate the number of failures using the new intervals

# To do so, we can use np.select() --> a conditional operator, like case_when() in R
tab2 = tab.copy()
interval = tab2["interval"].astype(str)
tab2["interval"] = np.select(
    [interval == "(500,600]",
     interval == "(600,700]",
     interval == "(700,800]",
     interval == "(800,900]"],
    ["(400,500]",
     "(400,500]",
     "(400,500]",
     "(400,500]"],
    # otherwise, return this thing (TRUE ~ interval in R)
    default=interval)
# But it needs to be remade into a
# categorical again to remember interval order
tab2["interval"] = pd.Categorical(
    tab2["interval"],
    categories=["[0,100]", "(100,200]",
                "(200,300]", "(300,400]", "(400,500]",
                "(500,600]", "(600,700]",
                "(700,800]", "(800,900]"],
    ordered=True)

# Then, we can aggregate to the revised intervals
tab3 = (tab2
        .groupby("interval", observed=True)
        .agg(r_obs=("r_obs", "sum"))
        .reset_index())

# We could finish up like this
# (as.numeric(interval) in R is the category code + 1 in pandas;
# .astype(int) matters - pandas stores codes as tiny int8s that overflow past 127)
binsize = 100
print(tab3
      .assign(bin=lambda df: df["interval"].cat.codes.astype(int) + 1)
      .assign(lower=lambda df: (df["bin"] - 1) * binsize,
              upper=lambda df: df["bin"] * binsize)
      .assign(midpoint=lambda df: (df["lower"] + df["upper"]) / 2))



# We could try to make our own function to do it all...
def crosstab2(x, binsize=100, midpoint_=450, interval_="(400,500]", binid_=5):
    # Testing Values
    # x = hours
    # binsize = 100
    # midpoint_ = 450
    # interval_ = "(400,500]"
    # binid_ = 5

    data = (pd.DataFrame({"t": x})
            .assign(interval=lambda df: cut_interval(df["t"], length=binsize))
            .groupby("interval", observed=False)
            .size()
            .reset_index(name="r_obs"))


    data = (data
            .assign(bin=lambda df: df["interval"].cat.codes.astype(int) + 1)
            .assign(lower=lambda df: (df["bin"] - 1) * binsize,
                    upper=lambda df: df["bin"] * binsize)
            .assign(midpoint=lambda df: (df["lower"] + df["upper"]) / 2))


    data = data.assign(
        interval=lambda df: np.where(df["midpoint"] >= midpoint_,
                                     interval_, df["interval"].astype(str)),
        bin=lambda df: np.where(df["midpoint"] >= midpoint_,
                                binid_, df["bin"]))

    output = (data
              .groupby(["bin", "interval"])
              .agg(r_obs=("r_obs", "sum"))
              .reset_index())

    output = (output
              .assign(lower=lambda df: (df["bin"] - 1) * binsize,
                      upper=lambda df: df["bin"] * binsize)
              .assign(midpoint=lambda df: (df["lower"] + df["upper"]) / 2)
              [["bin", "interval", "midpoint", "r_obs"]])

    return output

# It works so-so.
print(crosstab2(x=hours, binsize=100,
                midpoint_=450, interval_="(400,500]", binid_=5))




# 6. Use the packaged helper instead ###########################

# I went on to update this and have provided a helper function under
# functions/functions_crosstab.py
# Try it out!
sys.path.append("functions")
from functions_crosstab import crosstab


# Product Times to Failure
hours = np.array([1,2,2,3,4,5,7,8,9,10,
                  11,13,15,16,17,17,18,18,18,20,
                  20,21,21,24,27,29,30,37,40,40,
                  40,41,46,47,48,52,54,54, 55,55,
                  64,65,65,65,67,76,76,79,80,80,
                  82,86,87,89,94,96,100,101,102,104,
                  105,109,109,120,123,141,150,156,156,161,
                  164,167,170,178,181,191,193,206,211,212,
                  214,236,238,240,265,304,317,328,355,363,
                  365,369,389,404,427,435,500,522,547,889])

# By default, it applies no cutoff.
# (The Python helper lists only intervals that hold failures, so the empty
# (600,700] and (700,800] rows that R shows are not printed here.)
print(crosstab(x=hours, binsize=100))
# But if you add a cutoff, it will aggregate categories past that cutoff
print(crosstab(x=hours, binsize=100, cutoff=450))





# Extra Examples ##############################################


# Try starting bin size of 55
print(pd.DataFrame({"t": hours})
      .assign(label=lambda df: cut_interval(df["t"], length=55))
      .groupby("label", observed=False)
      .size()
      .reset_index(name="r_obs")
      .assign(bin=lambda df: df["label"].cat.codes.astype(int) + 1)
      .assign(lower=lambda df: (df["bin"] - 1) * 55,
              upper=lambda df: df["bin"] * 55)
      .assign(midpoint=lambda df: (df["lower"] + df["upper"]) / 2)
      [["bin", "label", "midpoint", "r_obs"]])


# Let's functionify this...

def crosstab(x, binsize=55):
    return (pd.DataFrame({"t": x})
            .assign(label=lambda df: cut_interval(df["t"], length=binsize))
            .groupby("label", observed=False)
            .size()
            .reset_index(name="r_obs")
            .assign(bin=lambda df: df["label"].cat.codes.astype(int) + 1)
            .assign(lower=lambda df: (df["bin"] - 1) * binsize,
                    upper=lambda df: df["bin"] * binsize)
            .assign(midpoint=lambda df: (df["lower"] + df["upper"]) / 2)
            [["bin", "label", "midpoint", "lower", "upper", "r_obs"]])



tab = crosstab(hours, binsize=100)

# Edit your categories

tab = tab.assign(
    label=lambda df: np.where(df["midpoint"] >= 450,
                              "(400,900]", df["label"].astype(str)),
    bin=lambda df: np.where(df["midpoint"] >= 450, 5, df["bin"]))

print(tab)
tab = (tab
       .groupby(["bin", "label"])
       .agg(r_obs=("r_obs", "sum"))
       .reset_index()
       .assign(lower=lambda df: (df["bin"] - 1) * 100,
               upper=lambda df: df["bin"] * 100)
       .assign(midpoint=lambda df: (df["lower"] + df["upper"]) / 2)
       [["bin", "label", "midpoint", "lower", "upper", "r_obs"]])


lambda_hat = 0.00725
n = 100
print(tab["r_obs"].sum())
def f(t, lambda_):
    return 1 - np.exp(-lambda_ * t)
ingredients = (tab
               .assign(f2=lambda df: f(df["upper"], lambda_hat),
                       f1=lambda df: f(df["lower"], lambda_hat))
               .assign(prob=lambda df: df["f2"] - df["f1"])
               .assign(r_exp=lambda df: df["prob"] * n))

print(ingredients[["label", "f2", "f1", "prob", "r_exp"]])

# Try bin size of 100
print(pd.DataFrame({"t": hours})
      .assign(label=lambda df: cut_interval(df["t"], length=100))
      .groupby("label", observed=False)
      .size()
      .reset_index(name="r_obs"))

# Try bin size of...
print(pd.DataFrame({"t": hours})
      .assign(label=lambda df: cut_interval(df["t"], length=150))
      .groupby("label", observed=False)
      .size()
      .reset_index(name="r_obs"))
