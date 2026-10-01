# 11_workshop.py
# Tim Fraser
# Workshop 11: Multivariate Regression - Effects of Disaster on Social Capital
# Chapter: Multivariate Regression: Modeling Effects of Disaster on Social Capital

# It mirrors 11_workshop.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.


# 0. Getting Started ######################################################

import os, sys
import numpy as np                        # math (base R in R)
import pandas as pd                       # data wrangling (dplyr + readr in R)
from plotnine import *                    # visuals (ggplot2 in R)
from scipy import stats                   # pf() in R
import statsmodels.formula.api as smf     # lm() in R
sys.path.append(os.path.abspath('functions'))
from functions_distributions import qnorm # qnorm() in R

cities = pd.read_csv("workshops/jp_matching_experiment.csv")
# Tell Python to treat year and pref as **ordered categories** (factor() in R)
cities["year"] = cities["year"].astype(str).astype("category")
cities["pref"] = cities["pref"].astype("category")
cities["by_tsunami"] = pd.Categorical(cities["by_tsunami"], categories=["Not Hit", "Hit"])

cities.info()   # glimpse() in R



# 0.1 Importing Data #########################################################


# You can download the data from github, upload it to your project, and then read it in like this
print(pd.read_csv("workshops/jp_matching_experiment.csv").head())

# Or you could just load in the data like this:
# cities = pd.read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/jp_matching_experiment.csv")

cities = pd.read_csv("workshops/jp_matching_experiment.csv")
# Tell Python to treat year and pref as **ordered categories**
cities["year"] = cities["year"].astype(str).astype("category")
cities["pref"] = cities["pref"].astype("category")
cities["by_tsunami"] = pd.Categorical(cities["by_tsunami"], categories=["Not Hit", "Hit"])

# Think that's way easier? We can make a little function to make it easier to get this data.
# I'll add in some defaults like author, repository, and branch to make it easy to download data from our repository
def github_csv(file, author="timothyfraser", repository="sysen", branch="main"):
    return "https://raw.githubusercontent.com/" + author + "/" + repository + "/" + branch + "/" + file

# Boom!
print(pd.read_csv(                                   # read it in
    github_csv("workshops/jp_matching_experiment.csv")  # get csv from github
).head())                                            # see first few lines!


# Check it out!
print(cities.head())

# Each row in this dataset is a city-year, in a prefecture,
# covering city-years in the Tohoku region,
# the region affected by the 2011 earthquake, tsunami, and nuclear disaster in Japan
print(cities[(cities["pref"] == "Fukushima") & (cities["year"] == "2012")])

# I prefer using .info() (glimpse() in R)
# to see the structure of my data
cities.info()

# 1. Modeling #########################################################

# We can make a simple regression model 'm'
m = smf.ols("social_capital ~ damage_rate", data=cities).fit()

# View the equation
print(m.params)
# Write the equation!
# Y (social_capital) = 0.39 + 0.07485 * damage_rate

# We can write a function of our model equation, if we want
def sc(x):
    return 0.394 + 0.0749 * x

# We should first calculate our goodness of fit statistics, which I call 'gof'
# (glance() in R; sigma is the square root of the model's scale)
gof = pd.DataFrame({"r_squared": [m.rsquared], "sigma": [np.sqrt(m.scale)],
                    "statistic": [m.fvalue], "p_value": [m.f_pvalue]})
# View it!
print(gof)

# R2 = % of variation explained --> get to 1
# sigma = residual standard error --> error of our model predictions
# statistic (F) = ratio. how much better is my model than an intercept model
# p-value = p-value of the f-statistic = how extreme is my f statistic?
# p < 0.10. p < 0.05. p < 0.01 = great indicators that F is extreme (model is good / better than nothing)

# We can view model coefficients. (tidy() in R)
print(pd.DataFrame({"estimate": m.params, "std_error": m.bse,
                    "statistic": m.tvalues, "p_value": m.pvalues}))

# (Or if you like underscores, use my tidier() function from the workshop)

# Finally, what's the general range of our main predictor damage_rate?
# (hist() in R)
(ggplot(cities, aes(x="damage_rate")) + geom_histogram(bins=30))

# Let's predict, as the damage rate in a city increases, how does its social capital change?
print(pd.DataFrame({
  # seq(from = 0, to = 0.6, by = 0.01) in R
  "damage_rate": np.round(np.arange(0, 0.6 + 0.001, 0.01), 2)})
  # We can predict it using our hand-made function sc()
  .assign(yhat=lambda df: sc(df["damage_rate"]))
  # See first few
  .head())


# 2. Prediction ########################################################

# Or (preferrably, we can use .predict() to do make predictions straight from the model object
dat_sim = (pd.DataFrame({
  "damage_rate": np.round(np.arange(0, 0.6 + 0.001, 0.01), 2)})
  .assign(
    # Get predictions
    yhat=lambda df: m.predict(df).values,
    # get sigma
    sigma=np.sqrt(m.scale))
  # Simulate 1000 outcomes per damage rate (group_by() + reframe(rnorm(...)) in R)
  .loc[lambda df: df.index.repeat(1000)]
  .assign(ysim=lambda df: np.random.default_rng().normal(loc=df["yhat"], scale=df["sigma"]))
  .groupby("damage_rate", as_index=False)
  .agg(median=("ysim", "median"),
       lower=("ysim", lambda y: y.quantile(0.025)),
       upper=("ysim", lambda y: y.quantile(0.975))))


(ggplot(dat_sim, aes(x="damage_rate", y="median", ymin="lower", ymax="upper")) +
  geom_ribbon() +
  labs(x="Damage Rate", y="Predicted Social Capital (Simulated 95% CIs)"))


# What IS the residual standard error sigma?
# Well, we can approximate it pretty decently by taking the standard deviation of our models' residuals.
# A residual is the observed minus predicted value for each data point
print(pd.DataFrame({
  # Get the standard deviation of residuals
  "sd": [m.resid.std()],
  # Return the model's residual standard error (which is calculated with just one or two extra steps)
  "se": [np.sqrt(m.scale)]}))


# Let's get the 6-sigma range
dat_se = (pd.DataFrame({
  "damage_rate": np.round(np.arange(0, 0.6 + 0.001, 0.01), 2)})
  .assign(
    # Get predictions
    yhat=lambda df: m.predict(df).values,
    # get sigma
    sigma=np.sqrt(m.scale),

    lower=lambda df: df["yhat"] - 3 * df["sigma"],
    upper=lambda df: df["yhat"] + 3 * df["sigma"]))
# They are almost identical!

(ggplot(dat_se, aes(x="damage_rate", y="yhat")) +
  geom_ribbon(mapping=aes(x="damage_rate", ymin="lower", ymax="upper"),
              fill="steelblue", alpha=0.5) +
  geom_line(linetype="dashed") +
  theme_classic() +
  labs(x="Damage Rate", y="Predicted Social Capital (6 sigmas)"))


# We can also compute confidence intervals for our predictions
# for any specified percentile.
dat_q = (pd.DataFrame({
  "damage_rate": np.round(np.arange(0, 0.6 + 0.001, 0.01), 2)})
  .assign(
    yhat=lambda df: m.predict(df).values,
    # Get residual standard error 'se'
    se=np.sqrt(m.scale),
    # Calculate the z-score on a normal distribution for the 97.5th percentile
    z=qnorm(0.975),
    # Give me an upper 95% confidence interval at the 97.5th percentile
    upper=lambda df: df["yhat"] + df["se"] * df["z"],
    # Give me a lower 95% confidence interval at the 2.5th percentile
    lower=lambda df: df["yhat"] - df["se"] * df["z"]))


(ggplot(dat_q, aes(x="damage_rate", y="yhat")) +
  geom_ribbon(mapping=aes(x="damage_rate", ymin="lower", ymax="upper"),
              fill="steelblue", alpha=0.5) +
  geom_line(linetype="dashed") +
  theme_classic() +
  labs(x="Damage Rate", y="Predicted Social Capital (95% CI)"))




# Let's compare all three!

(ggplot() +
  geom_ribbon(
    data=dat_se.assign(type="6 sigma"),
    mapping=aes(x="damage_rate", ymin="lower", ymax="upper", fill="type"), alpha=0.5) +
  geom_ribbon(
    data=dat_q.assign(type="95% CI"),
    mapping=aes(x="damage_rate", ymin="lower", ymax="upper", fill="type"), alpha=0.5) +
  geom_ribbon(
    data=dat_sim.assign(type="Simulated 95% CI"),
    mapping=aes(x="damage_rate", ymin="lower", ymax="upper", fill="type"), alpha=0.5) +
  geom_line(
    data=dat_se,
    mapping=aes(x="damage_rate", y="yhat"), linetype="dashed") +
  scale_fill_manual(values=["steelblue", "goldenrod", "firebrick"]) +
  theme_classic() +
  labs(x="Damage Rate", y="Predicted Social Capital", fill="CI Type") +
  theme(legend_position="bottom"))



# 3. Key Stats of Interest #########################

m = smf.ols("income_per_capita ~ damage_rate", data=cities).fit()

def get_stat(m):
    # glance() in R, trimmed to four columns
    return pd.DataFrame({"r_squared": [m.rsquared], "sigma": [np.sqrt(m.scale)],
                         "statistic": [m.fvalue], "p_value": [m.f_pvalue]})

print(get_stat(m))



print(m.params)          # m$coefficients in R
print(m.fittedvalues)    # m$fitted.values in R



d = (pd.DataFrame({
  # predicted or expected
  "yhat": m.fittedvalues,
  # observed
  "y": m.model.endog})
  # calculate the difference between the observed and expected...
  .assign(residuals=lambda df: df["y"] - df["yhat"]))


print(pd.DataFrame({
  # all the variation in your data
  "tss": [((d["y"] - d["y"].mean())**2).sum()],
  # sum of squared deviations
  "rss": [((d["y"] - d["yhat"])**2).sum()]})
  # EXPLAINED SUM OF SQUARES
  .assign(ess=lambda s: s["tss"] - s["rss"])
  # PERCENTAGE OF VARIATION EXPLAINED, out of TOTAL VARIATION
  .assign(rsq=lambda s: s["ess"] / s["tss"])
  .assign(rsq=lambda s: 1 - s["rss"] / s["tss"]))


# F-statistic







print(pd.DataFrame({
  "tss": [((d["y"] - d["y"].mean())**2).sum()],
  "rss": [((d["y"] - d["yhat"])**2).sum()]})
  .assign(rsq=lambda s: 1 - s["rss"] / s["tss"]))


print(pd.DataFrame({
  # Calculate residual sum of squares
  "residual_sum_of_squares": [((d["y"] - d["yhat"])**2).sum()],
  # Calculate total sum of squares
  "total_sum_of_squares": [((d["y"] - d["y"].mean())**2).sum()],
  # Get sample size
  "n": [len(d)],
  # Calculate number of variables in your model
  "p": [2]})
  # Calculate explained sum of squares
  .assign(ess=lambda s: s["total_sum_of_squares"] - s["residual_sum_of_squares"])
  .assign(
    # Mean Squares due to Regression, given the no. of predictors
    mean_squares_due_to_regression=lambda s: s["ess"] / (s["p"] - 1),
    # Mean Squared Error
    # How much variation was NOT explained, given the sample size and no. of variables
    mean_squared_error=lambda s: s["residual_sum_of_squares"] / (s["n"] - s["p"]),
    # sigma-squared
    # RMSE = sigma
    sigma=lambda s: np.sqrt(s["mean_squared_error"]))

  # Compute the F-statistic, which is a ratio of explained vs. unexplained variation
  .assign(f_statistic=lambda s: s["mean_squares_due_to_regression"] / s["mean_squared_error"])
  # Finally, throw it into stats.f.sf() (pf(..., lower.tail = FALSE) in R),
  # which plots a theoretical null distribution
  # based on the number of variables and sample size,
  # and identifies how extreme our F-statistic is compared to one we'd get by chance
  # Computes p-value
  .assign(p_value=lambda s: stats.f.sf(s["f_statistic"], s["p"] - 1, s["n"] - s["p"]))
  # glimpse() in R: one row, shown as a column
  .iloc[0].rename(None))

# IF our p-value is less than 5%,
# that's often a good indication
# that our model fits better than a simple intercept (mean) would.
# a good f-statistic
print(stats.f.sf(15, 2 - 1, 1057 - 2))

d.info()

print(get_stat(m))


print(np.sqrt(m.scale))   # glance(m)$sigma in R
print(m.resid.std())      # m$residuals %>% sd() in R
