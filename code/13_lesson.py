# 13_lesson.py
# Tim Fraser
# Lesson 13: Factorial Design
# Chapter: Factorial Design in Python

# It mirrors 13_lesson.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.

# Example 1 #################################################

import itertools                          # expand_grid() in R
import numpy as np                        # math (base R in R)
import pandas as pd                       # data wrangling (dplyr + tidyr in R)

# Get full factorial grid of combinations
# (itertools.product varies the LAST factor fastest, just like expand_grid())
grid = pd.DataFrame(
  list(itertools.product(
    # Catalyst K
    ["A", "B"],
    # Concentration C
    [20, 40],
    # Temperature t
    [160, 180])),
  columns=["k", "c", "t"])
# order columns as shown in the example...
grid["run"] = np.arange(1, len(grid) + 1)
grid = grid[["run", "t", "c", "k"]]

# We run the experiment once and get these results
data = grid.assign(y=[60, 72, 54, 68, 52, 83, 45, 80])

print(data)


# Example 2 ##########################################

# A tiny helper, like y[condition] in R: the y values where condition is True
def yw(df, condition):
  return df.loc[condition, "y"].to_numpy()

# Calculate the direct (one-way) treatment effects
print(pd.DataFrame({
  "dbar_c": [np.mean(yw(data, data["c"] == 40) - yw(data, data["c"] == 20))],
  "dbar_t": [np.mean(yw(data, data["t"] == 180) - yw(data, data["t"] == 160))],
  "dbar_k": [np.mean(yw(data, data["k"] == "B") - yw(data, data["k"] == "A"))]}))



# Example 3 ##########################################

t, c, k = data["t"], data["c"], data["k"]

# Calculate the two-way treatment effects
xbar1 = yw(data, ((t == 180) & (k == "B")) | ((t == 160) & (k == "A"))).mean()
xbar0 = yw(data, ((t == 160) & (k == "B")) | ((t == 180) & (k == "A"))).mean()
print(pd.DataFrame({"xbar1": [xbar1], "xbar0": [xbar0], "dbar": [xbar1 - xbar0]}))

# Let's get a clearer  glimpse at that first stage, before we take the means
print(pd.DataFrame({
  "x1": yw(data, ((t == 180) & (k == "B")) | ((t == 160) & (k == "A"))),
  "x0": yw(data, ((t == 160) & (k == "B")) | ((t == 180) & (k == "A")))}))

# Even narrower...
print(pd.DataFrame({
  "x1a": yw(data, (t == 160) & (k == "A")),
  "x1b": yw(data, (t == 180) & (k == "B")),
  "x0a": yw(data, (t == 180) & (k == "A")),
  "x0b": yw(data, (t == 160) & (k == "B"))}))


# Example 4 ######################################################

# Three Way Treatment Effects

# Get treatment effect for TCK...

# A helper for the single y value at one set of conditions, like y[t==180&k=="A"&c==40] in R
def y1(tt, cc, kk):
  return yw(data, (t == tt) & (c == cc) & (k == kk))[0]

# Get the TC interaction when K is A
d1 = y1(180, 40, "A") - y1(160, 40, "A")
d0 = y1(180, 20, "A") - y1(160, 20, "A")
print(pd.DataFrame({"d1": [d1], "d0": [d0], "dbar": [(d1 - d0) / 2]}))

# Get the TC interaction when K is B
d1 = y1(180, 40, "B") - y1(160, 40, "B")
d0 = y1(180, 20, "B") - y1(160, 20, "B")
print(pd.DataFrame({"d1": [d1], "d0": [d0], "dbar": [(d1 - d0) / 2]}))

# Now get the average difference between these interactions
# Get the TC interaction when K is A
d1a = y1(180, 40, "A") - y1(160, 40, "A")
d0a = y1(180, 20, "A") - y1(160, 20, "A")
dbar_a = (d1a - d0a) / 2

# Get the TC interaction when K is B
d1b = y1(180, 40, "B") - y1(160, 40, "B")
d0b = y1(180, 20, "B") - y1(160, 20, "B")
dbar_b = (d1b - d0b) / 2

# Get three way interaction effect
dbar = (dbar_b - dbar_a) / 2

print(pd.DataFrame({"d1a": [d1a], "d0a": [d0a], "dbar_a": [dbar_a],
                    "d1b": [d1b], "d0b": [d0b], "dbar_b": [dbar_b],
                    "dbar": [dbar]}))



# Example 5 #################################

# We run the experiment twice and get these results
data2 = pd.concat([
  grid.assign(rep=1, y=[59, 74, 50, 69, 50, 81, 46, 79]),
  grid.assign(rep=2, y=[61, 70, 58, 67, 54, 85, 44, 81])], ignore_index=True)


# Let's construct our table
# Differences of replicate runs (diff(y) in R: replicate 2 minus replicate 1)
print(data2.sort_values(["run", "rep"])
      .groupby(["run", "t", "c", "k"], as_index=False)
      .agg(d=("y", lambda y: y.iloc[1] - y.iloc[0])))

# Variance across replicate runs for each set of conditions
print(data2.groupby(["run", "t", "c", "k"], as_index=False)
      .agg(var=("y", "var"), v=("y", lambda y: len(y) - 1)))

# Get pooled standard deviation
per_run = (data2.groupby(["run", "t", "c", "k"], as_index=False)
           # Variance per run, and degrees of freedom per run
           .agg(var=("y", "var"), v=("y", lambda y: len(y) - 1)))

# Pooled variance
vp = per_run["var"].sum() / per_run["v"].sum()
# How many scenarios are being evaluates (n differences)
n_diff = len(per_run)
# variance of effect
sv = (1 / n_diff + 1 / n_diff) * vp
# standard error of effect
se = np.sqrt(sv)

stat = pd.DataFrame({"vp": [vp], "n_diff": [n_diff], "sv": [sv], "se": [se]})

print(stat)
