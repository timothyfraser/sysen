# 05_recitation.py
# Tim Fraser
# Recitation 5: Statistical process control practice
# Chapter: Statistical Process Control in Python

# This is the WORKED version of recitation 5: every exercise is filled in.
# It mirrors 05_recitation.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.

# 0. Setup ##################################################
# Load packages
import sys
import numpy as np             # math (base R in R)
import pandas as pd            # data wrangling (dplyr + readr in R)
from plotnine import *         # visuals (ggplot2 in R)

# NOTE: R's ggpubr (for arranging several plots together) has no direct
# Python equivalent here; we show each plotnine chart on its own.

# Load data
water = pd.read_csv("workshops/onsen.csv")

# Take a look: each row is one reading from one hot spring sensor,
# taken at a subgroup 'time', with temperature, pH, and sulfur.
water.info()


# Exercise 1 ###############################################


# Load functions
# ***You'll need to go add this script for this to work.
# https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py
# In R, source() runs the helper script. In Python, we add the functions/
# folder to our path and import the helpers we need.
sys.path.append("functions")
from functions_process_control import *


# Exercise 2 ###############################################


# Pick a quality metric from our onsen dataset,
# and generate averages, standard deviation, and range plots,
# using our helper functions.

# We'll pick pH. (temp works the same way - swap 'ph' for 'temp'.)

# Averages chart: is the MEAN pH of each subgroup stable over time?
g_avg = ggxbar(x=water['time'], y=water['ph'],
               xlab="Time (Subgroups)", ylab="Average pH")

# Standard deviation chart: is the SPREAD of pH within each subgroup stable?
g_s = ggs(x=water['time'], y=water['ph'],
          xlab="Time (Subgroups)", ylab="SD of pH")

# Range chart: same question as the sd chart, using max - min instead.
g_r = ggr(x=water['time'], y=water['ph'],
          xlab="Time (Subgroups)", ylab="Range of pH")

# View them one at a time (type the name in Jupyter / a REPL to draw it)
g_avg
g_s
g_r

# Now get the numbers behind the charts.
# get_stat_s() gives one row per subgroup, with the centerline (xbbar),
# the within-subgroup sigma (sigma_s), and the +/- 3 standard error limits.
stat = get_stat_s(x=water['time'], y=water['ph'])
print(stat)

# The centerlines and averages-chart limits, summarized in one row
centerlines = pd.DataFrame({
    'subgroups': [len(stat)],
    'nw': [stat['nw'].mean()],
    'xbbar': [stat['xbar'].mean()],                # centerline of the averages chart
    'sbar': [np.sqrt((stat['s'] ** 2).mean())],    # centerline of the sd chart (pooled sigma_s)
    'rbar': [stat['r'].mean()],                    # centerline of the range chart
    'lower': [stat['lower'].min()],                # averages chart: xbbar - 3 * sigma_s / sqrt(nw)
    'upper': [stat['upper'].max()],                # averages chart: xbbar + 3 * sigma_s / sqrt(nw)
})
print(centerlines.round(3))

# The sd and range charts use control constants (B3/B4, D3/D4).
# The helpers estimate them by simulation, so their limits can wobble
# in the second decimal from run to run. One row each:
ls = limits_s(x=water['time'], y=water['ph'])
print(ls[['sbar', 'lower', 'upper']].mean().to_frame().T)
lr = limits_r(x=water['time'], y=water['ph'])
print(lr[['rbar', 'lower', 'upper']].mean().to_frame().T)

# How many subgroup averages fall outside the averages-chart limits?
out_of_control = ((stat['xbar'] > stat['upper']) | (stat['xbar'] < stat['lower'])).sum()
print(pd.DataFrame({'out_of_control': [out_of_control]}))

# Describe the process under study.

# The onsen sensors record pH several times per subgroup (nw readings each).
# - The averages chart: every subgroup average sits inside xbbar +/- 3 se,
#   so mean pH looks stable over time - no special-cause shifts.
# - The sd and range charts: within-subgroup variation stays inside its
#   limits too, so the spread is stable - the process is 'in control'.
# - In control is not the same as good: it means the process is predictable.
#   Whether pH is acceptable for bathers is a question for spec limits,
#   which is next week's topic (capability indices).


# Exercise 3 ###############################################


# Write your own chart function.
# In workshop 5 we made a jittered process plot (g1) and a sideways
# histogram (g2). plotnine has no ggarrange(), so our function
# returns both plots, and we draw them in turn.

def myprocess(x, y, xlab="Subgroup", ylab="Metric"):
    # Put the two vectors in one data.frame
    data = pd.DataFrame({'x': pd.Series(x).values, 'y': pd.Series(y).values})

    # Every reading over time, jittered so they don't overlap
    g1 = (ggplot()
          + geom_jitter(data=data, mapping=aes(x='x', y='y'),
                        width=0.25, height=0, alpha=0.5)
          # add the grand mean as a reference line
          + geom_hline(yintercept=data['y'].mean(), color="steelblue")
          + labs(x=xlab, y=ylab, subtitle="Process Over Time"))

    # ...and their distribution, on its side
    g2 = (ggplot()
          + geom_histogram(data=data, mapping=aes(x='y'),
                           bins=15, fill="steelblue", color="white")
          + coord_flip()
          + labs(x="", y="Count", subtitle="Distribution"))

    # Return both plots
    return g1, g2

# Try it on pH...
g_ph = myprocess(x=water['time'], y=water['ph'], xlab="Time (Subgroups)", ylab="pH")
g_ph[0]
g_ph[1]

# ...and on temperature, with no new code
g_temp = myprocess(x=water['time'], y=water['temp'], xlab="Time (Subgroups)", ylab="Temperature (C)")
g_temp[0]
g_temp[1]

# Compare against the course helper, ggprocess(), which does the same job
ggprocess(x=water['time'], y=water['ph'], xlab="Time (Subgroups)", ylab="pH")
