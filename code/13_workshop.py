# 13_workshop.py
# Tim Fraser
# Workshop 13: Interaction Effects in Python
# Chapter: Factorial Design in Python

# It mirrors 13_workshop.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.

import itertools                          # expand_grid() in R
import numpy as np                        # math (base R in R)
import pandas as pd                       # data wrangling (dplyr + readr in R)
from plotnine import *                    # visuals (ggplot2 in R)
from scipy import stats                   # qnorm() in R
import statsmodels.formula.api as smf     # lm() in R
from statsmodels.stats.oneway import anova_oneway  # oneway.test() in R

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


# Calculate a standard error the tastiness metric in this factorial experiment
cells = (lattes.groupby(["machine", "syrup", "art"], as_index=False)
         .agg(s=("y", "std"), n=("y", "size")))
se = np.sqrt((cells["s"]**2 / cells["n"]).sum())
# (In R, with() pulls the se value out of the data.frame. Here it's already a number.)

print(se)



# Example 1: Calculate Direct Effects ########################

# Calculate the direct effect of having a heart vs. foam in your latte

# A tiny helper, like y[condition] in R: the y values where condition is True
def yw(df, condition):
  return df.loc[condition, "y"].to_numpy()

print(pd.DataFrame({"dbar": [yw(lattes, lattes["machine"] == "a").mean() -
                             yw(lattes, lattes["machine"] == "b").mean()]}))

# reframe() in R gives the same single row here
print(pd.DataFrame({"dbar": [yw(lattes, lattes["machine"] == "a").mean() -
                             yw(lattes, lattes["machine"] == "b").mean()]}))


# Without mean(), you get one difference per pair of rows (120 of them)
print(pd.DataFrame({"dbar": yw(lattes, lattes["machine"] == "a") -
                            yw(lattes, lattes["machine"] == "b")}))



myse = pd.DataFrame({"se": [np.sqrt((cells["s"]**2 / cells["n"]).sum())]})
# myse %>% {.$se} and myse %>% with(se) in R both pull out the value
print(myse["se"].iloc[0])

se = myse["se"].iloc[0]


dbar = yw(lattes, lattes["machine"] == "a").mean() - yw(lattes, lattes["machine"] == "b").mean()
z = stats.norm.ppf(0.975)                 # qnorm(0.975) in R
stat = pd.DataFrame({"dbar": [dbar], "se": [se], "name": ["Machine A - B"], "z": [z],
                     "upper": [dbar + z * se], "lower": [dbar - z * se]})

# stats.norm.cdf(3)
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

# model.frame(formula, data) in R: pull the y column and the x columns named
# in a formula string like "y ~ machine * syrup", in that order.
def model_frame(formula, data):
  lhs, rhs = formula.replace(" ", "").split("~")
  xvars = rhs.replace("*", "+").split("+")
  return data[[lhs] + xvars]

# factor(x) %>% as.integer() - 1 in R: levels sorted alphabetically, coded 0, 1, ...
def code(x):
  levels = sorted(x.unique())
  return x.map({lev: i for i, lev in enumerate(levels)})

# Let's construct ourselves some functions
def dbar_oneway(formula, data):
  # formula = "y ~ machine"
  # data = lattes

  frame = model_frame(formula, data)
  frame.columns = ["y", "a"]
  frame = frame.assign(a=code(frame["a"]))

  # R subtracts y[a==0] from y[a==1] element by element, recycling the shorter
  # vector; for balanced groups that is the same as a difference of means.
  dbar = frame.loc[frame["a"] == 1, "y"].mean() - frame.loc[frame["a"] == 0, "y"].mean()
  return dbar

# Function for a 2^3 factorial experiment's 2-way interaction effects
def dbar_twoway(formula, data):
  # Testing Values
  # formula = "y ~ syrup * art"
  # data = lattes

  # Extract model frame
  frame = model_frame(formula, data)
  frame.columns = ["y", "a", "b"]

  # (R codes the levels 1 and 2; we code them 0 and 1)
  a, b = code(frame["a"]), code(frame["b"])

  x1 = frame.loc[((a == 1) & (b == 1)) | ((a == 0) & (b == 0)), "y"]
  x0 = frame.loc[((a == 0) & (b == 1)) | ((a == 1) & (b == 0)), "y"]
  output = x1.mean() - x0.mean()
  return output

# For a true 3-by-3 interaction...
def dbar_threeway(formula, data):
  # Testing Values
  # formula = "y ~  machine * syrup * art"
  # data = lattes

  frame = model_frame(formula, data)
  frame.columns = ["y", "a", "b", "c"]
  a, b, c = code(frame["a"]), code(frame["b"]), code(frame["c"])

  def ycell(aa, bb, cc):
    return frame.loc[(a == aa) & (b == bb) & (c == cc), "y"].to_numpy()

  # Get the AC interaction when B = 0
  d1a = ycell(1, 0, 1) - ycell(0, 0, 1)
  d0a = ycell(1, 0, 0) - ycell(0, 0, 0)
  # Get the AC interaction when B = 1
  d1b = ycell(1, 1, 1) - ycell(0, 1, 1)
  d0b = ycell(1, 1, 0) - ycell(0, 1, 0)

  # Get AC interaction effect when B = 0
  dbar_a = (d1a.mean() - d0a.mean()) / 2
  # Get AC interaction effect when B = 1
  dbar_b = (d1b.mean() - d0b.mean()) / 2
  # Get the average of the two effects
  output = (dbar_b - dbar_a) / 2
  return output

def se_factorial(formula="y ~ machine + syrup + art", data=None):
  # formula = "y ~  machine + syrup + art"
  # data = lattes

  # Get frame of data
  frame = model_frame(formula, data)
  frame = frame.rename(columns={frame.columns[0]: "y"})
  # Get names of xvaraiables
  xvars = list(frame.columns[1:])

  # Calculate a standard error the tastiness metric in this factorial experiment
  cells = frame.groupby(xvars, as_index=False).agg(s=("y", "std"), n=("y", "size"))
  output = np.sqrt((cells["s"]**2 / cells["n"]).sum())
  return output


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


se_all = se_factorial(formula="y ~ machine + syrup + art", data=lattes)
effects = pd.DataFrame({
  "name": ["Torani - Monin", "Heart - Foam", "Machine B - A",
           "Machine * Art", "Machine * Syrup", "Syrup * Art",
           "Machine * Syrup * Art"],
  "estimate": [dbar_oneway(formula="y ~ syrup", data=lattes),
               dbar_oneway(formula="y ~ art", data=lattes),
               dbar_oneway(formula="y ~ machine", data=lattes),
               dbar_twoway(formula="y ~ machine * art", data=lattes),
               dbar_twoway(formula="y ~ machine * syrup", data=lattes),
               dbar_twoway(formula="y ~ syrup * art", data=lattes),
               dbar_threeway(formula="y ~ machine * syrup * art", data=lattes)],
  "se": se_all})
effects["z"] = stats.norm.ppf(0.975)
effects["upper"] = effects["estimate"] + effects["se"] * effects["z"]
effects["lower"] = effects["estimate"] - effects["se"] * effects["z"]

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






# interactions with lm() #############################


m = smf.ols("y ~ machine * art", data=lattes).fit()
print(m.params)
# Tastiness = 54 + -26 * (machine B?) + 15 * (heart?) - 8 * (machineB?)(heart?)
# Tastiness = 54 + -26 * (1) + 15 * (0) - 8 * (1)(0)
# Tastiness = 54 + -26 * (1) + 15 * (1) - 8 * (1)(1)
# Tastiness = 54 + -26 * (0) + 15 * (0) - 8 * (0)(0)

newdata = pd.DataFrame({"machine": ["b"], "art": ["heart"]})
print(newdata.assign(y=m.predict(newdata).to_numpy()))


# predict(..., se.fit = TRUE) in R: get_prediction() gives the fit and its standard error
pred = m.get_prediction(newdata).summary_frame()
print(pred[["mean", "mean_se"]].rename(columns={"mean": "yhat", "mean_se": "se"}))


grid = pd.DataFrame(
  list(itertools.product(["a", "b"], ["heart", "foamy"])),
  columns=["machine", "art"])

pred = m.get_prediction(grid).summary_frame()
effects = grid.assign(fit=pred["mean"].to_numpy(), se=pred["mean_se"].to_numpy())
effects["z"] = stats.norm.ppf(0.975)
effects["upper"] = effects["fit"] + effects["se"] * effects["z"]
effects["lower"] = effects["fit"] - effects["se"] * effects["z"]

print(effects)
