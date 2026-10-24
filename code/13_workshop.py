# 13_workshop.py
# Tim Fraser
# Workshop 13: Interaction Effects in Python
# Chapter: Factorial Design in Python

# It mirrors 13_workshop.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.

import os, sys, re
import itertools                          # expand_grid() in R
import numpy as np                        # math (base R in R)
import pandas as pd                       # data wrangling (dplyr + readr in R)
from plotnine import *                    # visuals (ggplot2 in R)
import statsmodels.formula.api as smf     # lm() in R
from statsmodels.stats.oneway import anova_oneway  # oneway.test() in R
sys.path.append(os.path.abspath('functions'))
from functions_distributions import qnorm # qnorm() in R

# Load in data!
# If you upload it to your workshops folder, read it in like this...
lattes = (pd.read_csv("workshops/lattes.csv")
          # Let's shorten our main metric name
          .rename(columns={"tastiness": "y"}))

# View it
print(lattes)

# Show the types
print(lattes["machine"].unique())
print(lattes["syrup"].unique())
print(lattes["art"].unique())
# Also, looks like we randomly assigned the type of milk too.
# We'll treat this as a control
print(lattes["milk"].unique())


# Calculate the standard error of an effect in this factorial experiment.
# First, pool the variance across every treatment combination (cell)...
cells = lattes.groupby(["machine", "syrup", "art"], as_index=False).agg(s2=("y", "var"), n=("y", "size"))
s2 = ((cells["n"] - 1) * cells["s2"]).sum() / (cells["n"] - 1).sum()
# ...then each effect compares the mean of the runs at + with the mean of the runs at -,
# so SE = s * sqrt(1 / n_plus + 1 / n_minus). Machine b has 120 runs and machine a has 120.
se = np.sqrt(s2) * np.sqrt(1 / 120 + 1 / 120)

print(se)



# Example 1: Calculate Direct Effects ########################

# Calculate the direct effect of having a heart vs. foam in your latte

# .loc[condition, "y"] is like y[condition] in R: the y values where condition is True
print(pd.DataFrame({"dbar": [lattes.loc[lattes["machine"] == "a", "y"].mean() -
                             lattes.loc[lattes["machine"] == "b", "y"].mean()]}))

# reframe() in R gives the same single row here
print(pd.DataFrame({"dbar": [lattes.loc[lattes["machine"] == "a", "y"].mean() -
                             lattes.loc[lattes["machine"] == "b", "y"].mean()]}))


# Without mean(), you get one difference per pair of rows (120 of them)
print(pd.DataFrame({"dbar": lattes.loc[lattes["machine"] == "a", "y"].to_numpy() -
                            lattes.loc[lattes["machine"] == "b", "y"].to_numpy()}))



myse = (lattes.groupby(["machine", "syrup", "art"], as_index=False)
        .agg(s2=("y", "var"),
             n=("y", "size"))
        .pipe(lambda df: pd.DataFrame({"s2": [((df["n"] - 1) * df["s2"]).sum() / (df["n"] - 1).sum()]}))
        .assign(se=lambda df: np.sqrt(df["s2"]) * np.sqrt(1 / 120 + 1 / 120)))
# myse %>% {.$se} and myse %>% with(se) in R both pull out the value
print(myse["se"].iloc[0])

se = myse["se"].iloc[0]


stat = (pd.DataFrame({"dbar": [lattes.loc[lattes["machine"] == "a", "y"].mean() -
                               lattes.loc[lattes["machine"] == "b", "y"].mean()]})
        .assign(se=se)
        .assign(
          name="Machine A - B",
          z=qnorm(0.975),
          upper=lambda df: df["dbar"] + df["z"] * df["se"],
          lower=lambda df: df["dbar"] - df["z"] * df["se"]))

# pnorm(3)
print(stat)

# colors() in R lists the named colors; plotnine uses matplotlib's named colors
# (see matplotlib.colors.CSS4_COLORS)

(ggplot() +
  geom_point(data=stat, mapping=aes(x="name", y="dbar")) +
  geom_crossbar(data=stat, mapping=aes(x="name", y="dbar", ymin="lower", ymax="upper"),
                fill="mediumvioletred") +
  geom_hline(yintercept=0, linetype="dashed") +
  geom_text(data=stat.assign(ylab=stat["upper"] + 2, lab=stat["upper"].round(2)),
            mapping=aes(x="name", y="ylab", label="lab")) +
  geom_text(data=stat.assign(ylab=stat["lower"] - 2, lab=stat["lower"].round(2)),
            mapping=aes(x="name", y="ylab", label="lab")))


# xbar1 = yw(lattes, lattes["art"] == "heart").mean()
# xbar0 = yw(lattes, lattes["art"] == "foamy").mean()
# stat = pd.DataFrame({"name": ["Heart - Foamy"], "xbar1": [xbar1], "xbar0": [xbar0],
#                      "dbar": [xbar1 - xbar0], "se": [se], "z": [z]})
# stat["lower"] = stat["dbar"] - stat["se"] * stat["z"]
# stat["upper"] = stat["dbar"] + stat["se"] * stat["z"]
#

# Visualize it!
(ggplot() +
  geom_crossbar(
    data=stat,
    mapping=aes(x="name", y="dbar", ymin="lower", ymax="upper")) +
  geom_hline(yintercept=0, linetype="dashed"))
# Is that effect significant with 95% confidence?







# FUNCTIONS ######################################

# When doing really nitty-gritty calculations like this,
# functions will become our friends.

# Let's construct ourselves some functions
from itertools import combinations
from scipy import stats  # qt() in R


def factorial_frame(formula, data):
    response, rhs = [part.strip() for part in formula.split("~")]
    xvars = [v.strip() for v in rhs.replace("*", "+").split("+")]
    frame = data[[response] + xvars].rename(columns={response: "y"})
    return frame, xvars


def se_factorial(formula, data, table=False):
    frame, xvars = factorial_frame(formula, data)
    # Every factor must have exactly two levels
    n_levels = frame[xvars].nunique()
    if (n_levels != 2).any():
        raise ValueError("se_factorial(): " + ", ".join(n_levels[n_levels != 2].index) +
                         " does not have exactly two levels. Recode it as a yes/no question, "
                         "e.g. lattes['oat'] = lattes['milk'] == 'oat'.")
    # Code each factor -1 (first level) and +1 (second level)
    coded = frame.assign(**{x: np.where(frame[x] == sorted(frame[x].unique())[1], 1, -1) for x in xvars})

    # Pooled variance over the treatment combinations of all the factors
    cells = coded.groupby(xvars)["y"].agg(s2="var", n="count").reset_index()
    cells["v"] = cells["n"] - 1
    df = int(cells["v"].sum())
    if df == 0:
        raise ValueError("se_factorial(): no treatment combination has 2 or more runs, so there is no "
                         "pooled variance; judge its effects with a normal plot instead.")
    s2 = (cells["v"] * cells["s2"].fillna(0)).sum() / df

    # Every main effect, two-way and three-way interaction among the factors
    terms = [list(t) for m in range(1, min(3, len(xvars)) + 1) for t in combinations(xvars, m)]

    # SE of each effect: s * sqrt(sum of c^2 / n) over the combinations of its factors
    def se_term(t):
        n_k = coded.groupby(t).size()
        c_k = 1 / 2 ** (len(t) - 1)
        return np.sqrt(s2) * np.sqrt((c_k ** 2 / n_k).sum())

    output = pd.DataFrame({
        "term": [":".join(t) for t in terms],
        "n_plus": [int((coded[t].prod(axis=1) == 1).sum()) for t in terms],
        "n_minus": [int((coded[t].prod(axis=1) == -1).sum()) for t in terms],
        "se": [se_term(t) for t in terms]})
    output = output.assign(s2=s2, df=df, t_crit=stats.t.ppf(0.975, df))

    if table:
        return output
    # Balanced: every effect has the same SE, so return that one number
    if np.ptp(output["se"]) < 1e-10:
        return float(output["se"].iloc[0])
    print("se_factorial(): effects have different standard errors; effects_factorial() lists each effect with its own.")
    return pd.Series(output["se"].values, index=output["term"])


def dbar_oneway(formula, data):
    frame, (a,) = factorial_frame(formula, data)
    frame = frame.assign(a=(frame[a] == sorted(frame[a].unique())[1]).astype(int))
    # One mean per level of a, then high minus low
    xbar = frame.groupby("a")["y"].mean()
    return xbar[1] - xbar[0]


def dbar_twoway(formula, data):
    frame, (a, b) = factorial_frame(formula, data)
    frame = frame.assign(a=(frame[a] == sorted(frame[a].unique())[1]).astype(int),
                         b=(frame[b] == sorted(frame[b].unique())[1]).astype(int))
    # One mean per combination of a and b
    cells = frame.groupby(["a", "b"])["y"].mean().reset_index()
    same = cells["a"] == cells["b"]
    return cells.loc[same, "y"].mean() - cells.loc[~same, "y"].mean()


def dbar_threeway(formula, data):
    frame, (a, b, c) = factorial_frame(formula, data)
    frame = frame.assign(a=(frame[a] == sorted(frame[a].unique())[1]).astype(int),
                         b=(frame[b] == sorted(frame[b].unique())[1]).astype(int),
                         c=(frame[c] == sorted(frame[c].unique())[1]).astype(int))
    # One mean per combination of a, b and c, with its sign in the contrast
    cells = frame.groupby(["a", "b", "c"])["y"].mean().reset_index()
    sign = (2 * cells["a"] - 1) * (2 * cells["b"] - 1) * (2 * cells["c"] - 1)
    return cells.loc[sign == 1, "y"].mean() - cells.loc[sign == -1, "y"].mean()


def effects_factorial(formula, data, conf=0.95):
    # Standard errors (and the two-level check) come from se_factorial()
    ses = se_factorial(formula, data, table=True)
    frame, xvars = factorial_frame(formula, data)
    # Each effect from the matching dbar function
    dbar = {1: dbar_oneway, 2: dbar_twoway, 3: dbar_threeway}
    effect = np.array([dbar[len(t.split(":"))]("y ~ " + " * ".join(t.split(":")), frame)
                       for t in ses["term"]])
    # t interval on the pooled degrees of freedom
    t_crit = stats.t.ppf(1 - (1 - conf) / 2, ses["df"].iloc[0])
    return pd.DataFrame({"term": ses["term"], "effect": effect, "se": ses["se"],
                         "lower": effect - t_crit * ses["se"], "upper": effect + t_crit * ses["se"]})


# Generate your interaction effects for a 2^3 factorial experiment
print(dbar_oneway(formula="y ~ machine", data=lattes))

# Highest alphabeltic level - Lowest Alphabeltical Level
# B - A


print(lattes["machine"].unique())
# B - A
print(dbar_oneway(formula="y ~ machine", data=lattes))

print(lattes["syrup"].unique())
# Torani - Monin
print(dbar_oneway(formula="y ~ syrup", data=lattes))


print(lattes["art"].unique())
# Heart - Foamy
print(dbar_oneway(formula="y ~ art", data=lattes))


# B*Torani - A*Monin
print(dbar_twoway(formula="y ~ machine * syrup", data=lattes))

# B*Heart - A*Foamy
print(dbar_twoway(formula="y ~ machine * art", data=lattes))

# B*Heart*Torani - A*Foamy*Monin
print(dbar_threeway(formula="y ~ machine * syrup * art", data=lattes))


# Get your standard error free o charge
print(se_factorial(formula="y ~ machine + syrup + art", data=lattes))


# Every main effect and interaction, each with its standard error and a 95% interval
effects = (effects_factorial(formula="y ~ machine + syrup + art", data=lattes)
           .rename(columns={"term": "name", "effect": "estimate"}))

print(effects)
gg = (ggplot() +
  geom_crossbar(data=effects,
                mapping=aes(x="name", y="estimate", ymin="lower", ymax="upper",
                            fill="name")) +
  geom_hline(yintercept=0, linetype="dashed") +
  theme(legend_position="none") +
  coord_flip())

gg = (ggplot() +
  geom_crossbar(data=effects,
                mapping=aes(x="name", y="estimate", ymin="lower", ymax="upper",
                            fill="estimate")) +
  geom_hline(yintercept=0, linetype="dashed") +
  theme(legend_position="none") +
  coord_flip() +
  scale_fill_gradient2(high="royalblue", low="salmon", mid="white", midpoint=0))

gg


# # Can we stack these?
# effects = pd.DataFrame({
#   "name": ["machine", "machine * syrup"],
#   "estimate": [dbar_oneway(formula="y ~ machine", data=lattes),
#                dbar_twoway(formula="y ~ machine * syrup", data=lattes)]})
# effects["se"] = se_factorial(formula="y ~ machine + syrup + art", data=lattes)
#
#


# MULTIPLE LEVELS IN A FACTOR ####################################

# What if we want to test the effects of 3 or more levels in one factor?

print(lattes["milk"].unique())

# lm(formula = y ~ milk) in R: print the coefficients
print(smf.ols("y ~ milk", data=lattes).fit().params)

# oneway.test(formula = y ~ milk) in R (Welch's version, the default there)
print(anova_oneway(lattes["y"], groups=lattes["milk"], use_var="unequal"))













print(dbar_oneway(formula="y ~ oat", data=lattes.assign(oat=lattes["milk"] == "oat")))







# Compare the ones that are oatmilk vs. not
print(dbar_oneway(formula="y ~ oat", data=lattes.assign(oat=lattes["milk"] == "oat")))

# Compare the ones that are skim vs. not
print(dbar_oneway(formula="y ~ skim", data=lattes.assign(skim=lattes["milk"] == "skim")))





# Compare the ones that are whole vs. not
print(dbar_oneway(formula="y ~ whole", data=lattes.assign(whole=lattes["milk"] == "whole")))








# Compare the ones that are oatmilk AND from machine B against all the ones that are NOT oatmilk and from machine A
print(dbar_twoway(formula="y ~ machine * oat", data=lattes.assign(oat=lattes["milk"] == "oat")))

# Or get every effect at once. Oat lattes are a third of the runs,
# so effects involving oat get their own, larger standard error
print(effects_factorial(formula="y ~ machine + oat + syrup + art", data=lattes.assign(oat=lattes["milk"] == "oat")))






# interactions with lm() #############################


m = smf.ols("y ~ machine * art", data=lattes).fit()
print(m.params)
# Tastiness = 54 + -26 * (machine B?) + 15 * (heart?) - 8 * (machineB?)(heart?)
# Tastiness = 54 + -26 * (1) + 15 * (0) - 8 * (1)(0)
# Tastiness = 54 + -26 * (1) + 15 * (1) - 8 * (1)(1)
# Tastiness = 54 + -26 * (0) + 15 * (0) - 8 * (0)(0)

print(pd.DataFrame({"machine": ["b"], "art": ["heart"]})
      .assign(y=lambda df: m.predict(df).to_numpy()))


# predict(..., se.fit = TRUE) in R: get_prediction() gives the fit and its standard error
print(m.get_prediction(pd.DataFrame({"machine": ["b"], "art": ["heart"]})).summary_frame()
      [["mean", "mean_se"]].rename(columns={"mean": "yhat", "mean_se": "se"}))


grid = pd.DataFrame(
  list(itertools.product(["a", "b"], ["heart", "foamy"])),
  columns=["machine", "art"])

# Use each prediction's own standard error (se.fit), not the overall
# factorial standard error computed earlier in this script
effects = (m.get_prediction(grid).summary_frame()
  # mean is fit, mean_se is se.fit; put them next to the grid
  .pipe(lambda pred: grid.assign(fit=pred["mean"].to_numpy(), se=pred["mean_se"].to_numpy()))
  .assign(z=qnorm(0.975),
          upper=lambda df: df["fit"] + df["se"] * df["z"],
          lower=lambda df: df["fit"] - df["se"] * df["z"]))

print(effects)
