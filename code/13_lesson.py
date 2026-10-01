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
grid = (pd.DataFrame(
  list(itertools.product(
    # Catalyst K
    ["A", "B"],
    # Concentration C
    [20, 40],
    # Temperature t
    [160, 180])),
  columns=["k", "c", "t"])
  # order columns as shown in the example...
  .assign(run=lambda x: np.arange(1, len(x) + 1))
  .loc[:, ["run", "t", "c", "k"]])

# We run the experiment once and get these results
data = grid.assign(y=[60, 72, 54, 68, 52, 83, 45, 80])

print(data)


# Example 2 ##########################################


# Calculate the direct (one-way) treatment effects
# (.pipe(lambda d: ...) is %>% in R, and d.y[...].values is y[...])
print(data.pipe(lambda d: pd.DataFrame({
  "dbar_c": [np.mean(d.y[d.c == 40].values - d.y[d.c == 20].values)],
  "dbar_t": [np.mean(d.y[d.t == 180].values - d.y[d.t == 160].values)],
  "dbar_k": [np.mean(d.y[d.k == "B"].values - d.y[d.k == "A"].values)]})))



# Example 3 ##########################################

# Calculate the two-way treatment effects
print(data.pipe(lambda d: pd.DataFrame({
  "xbar1": [d.y[((d.t == 180) & (d.k == "B")) | ((d.t == 160) & (d.k == "A"))].mean()],
  "xbar0": [d.y[((d.t == 160) & (d.k == "B")) | ((d.t == 180) & (d.k == "A"))].mean()]}))
  .assign(dbar=lambda x: x.xbar1 - x.xbar0))

# Let's get a clearer  glimpse at that first stage, before we take the means
print(data.pipe(lambda d: pd.DataFrame({
  "x1": d.y[((d.t == 180) & (d.k == "B")) | ((d.t == 160) & (d.k == "A"))].values,
  "x0": d.y[((d.t == 160) & (d.k == "B")) | ((d.t == 180) & (d.k == "A"))].values})))

# Even narrower...
print(data.pipe(lambda d: pd.DataFrame({
  "x1a": d.y[(d.t == 160) & (d.k == "A")].values,
  "x1b": d.y[(d.t == 180) & (d.k == "B")].values,
  "x0a": d.y[(d.t == 180) & (d.k == "A")].values,
  "x0b": d.y[(d.t == 160) & (d.k == "B")].values})))


# Example 4 ######################################################

# Three Way Treatment Effects

# Get treatment effect for TCK...

# Get the TC interaction when K is A
print(data.pipe(lambda d: pd.DataFrame({
  "d1": d.y[(d.t == 180) & (d.k == "A") & (d.c == 40)].values - d.y[(d.t == 160) & (d.k == "A") & (d.c == 40)].values,
  "d0": d.y[(d.t == 180) & (d.k == "A") & (d.c == 20)].values - d.y[(d.t == 160) & (d.k == "A") & (d.c == 20)].values}))
  .assign(dbar=lambda x: (x.d1 - x.d0) / 2))

# Get the TC interaction when K is B
print(data.pipe(lambda d: pd.DataFrame({
  "d1": d.y[(d.t == 180) & (d.k == "B") & (d.c == 40)].values - d.y[(d.t == 160) & (d.k == "B") & (d.c == 40)].values,
  "d0": d.y[(d.t == 180) & (d.k == "B") & (d.c == 20)].values - d.y[(d.t == 160) & (d.k == "B") & (d.c == 20)].values}))
  .assign(dbar=lambda x: (x.d1 - x.d0) / 2))

# Now get the average difference between these interactions
print(data.pipe(lambda d: pd.DataFrame({
  # Get the TC interaction when K is A
  "d1a": d.y[(d.t == 180) & (d.k == "A") & (d.c == 40)].values - d.y[(d.t == 160) & (d.k == "A") & (d.c == 40)].values,
  "d0a": d.y[(d.t == 180) & (d.k == "A") & (d.c == 20)].values - d.y[(d.t == 160) & (d.k == "A") & (d.c == 20)].values})
  .assign(dbar_a=lambda x: (x.d1a - x.d0a) / 2,

    # Get the TC interaction when K is B
    d1b=d.y[(d.t == 180) & (d.k == "B") & (d.c == 40)].values - d.y[(d.t == 160) & (d.k == "B") & (d.c == 40)].values,
    d0b=d.y[(d.t == 180) & (d.k == "B") & (d.c == 20)].values - d.y[(d.t == 160) & (d.k == "B") & (d.c == 20)].values,
    dbar_b=lambda x: (x.d1b - x.d0b) / 2,

    # Get three way interaction effect
    dbar=lambda x: (x.dbar_b - x.dbar_a) / 2)))



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
stat = (data2.groupby(["run", "t", "c", "k"], as_index=False)
  .agg(
    # Variance per run
    var=("y", "var"),
    # Degrees of freedom per run
    v=("y", lambda y: len(y) - 1))
  .pipe(lambda x: pd.DataFrame({
    # Pooled variance (x["var"], since x.var is the .var() method)
    "vp": [x["var"].sum() / x["v"].sum()],
    # How many scenarios are being evaluates (n differences)
    "n_diff": [len(x)]}))
  .assign(
    # variance of effect
    sv=lambda x: (1 / x.n_diff + 1 / x.n_diff) * x.vp,
    # standard error of effect
    se=lambda x: np.sqrt(x.sv)))

print(stat)
