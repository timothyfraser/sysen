# 06_workshop_extra.py

# This is the Python twin of 06_workshop_extra.R, section by section.
# Run it from the top of the sysen folder, so the file paths below work.

import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr + readr in R)
from plotnine import *         # visuals (ggplot2 in R)
from scipy import stats        # qnorm() in R is stats.norm.ppf() here


# EXERCISE 1 - Writing a Function #####################3
def f(Eu, El, sd):
    cp = (Eu - El) / (6 * sd)
    return cp

# docstring style commenting for functions
# (R uses roxygen2 #' comments; Python puts the documentation
# inside the function, as a """docstring""".)

def f(Eu, El, sd):
    """
    Cp Process Control Index Function

    Calculate any Cp statistic with just 3 inputs! Yay!

    Parameters
    ----------
    Eu : int   Upper Specification Limit
    El : int   Lower Specification Limit
    sd : int   Sigma-short (average within group standard deviation)
    """
    cp = (Eu - El) / (6 * sd)
    return cp


print(f(Eu=10, El=2, sd=5))

# EXERCISE 2 ###################################
water = pd.read_csv("workshops/onsen.csv")
water.head().info()






# EXERCISE 3 #####################################


# What's bootstrapping?
# Take the existing data
# Sample with Replacement for the entire data
# Calculate a Stat
# Get a stat that has been slightly influenced by random chance




water = pd.read_csv("workshops/onsen.csv")

# (pandas .std() uses n - 1 by default, just like R's sd())
print(pd.DataFrame({"sigma_t": [water["temp"].std()]}))


# We need 1000 standard deviations
# We need 1000 resampled water datasets
# We need 1000 water datasets --- x
# We need a dataframe of 1000 ids -- x

# For each rep, draw len(water) rows WITH replacement,
# then stack all 1000 resampled datasets into one tall data frame.
boot = pd.concat(
    [water.sample(n=len(water), replace=True).assign(rep=rep)
     for rep in range(1, 1001)],
    ignore_index=True)

stat = (boot.groupby("rep")
        .agg(sigma_t=("temp", "std"))
        .reset_index())

# hist() in R draws a quick histogram; here we use plotnine
gg = ggplot(stat, aes(x="sigma_t")) + geom_histogram(bins=30)
gg

estimate = stat["sigma_t"].mean()
se = stat["sigma_t"].std()
print(pd.DataFrame({
    "estimate": [estimate],
    "se": [se],
    "upper": [estimate + se * stats.norm.ppf(0.975)],
    "lower": [estimate - se * stats.norm.ppf(0.975)]
}))
