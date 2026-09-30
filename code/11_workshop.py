# 11_workshop.py
# Tim Fraser
# Workshop 11: Multivariate Regression - Effects of Disaster on Social Capital
# Chapter: Multivariate Regression: Modeling Effects of Disaster on Social Capital

# It mirrors 11_workshop.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.


# 0. Getting Started ######################################################

import numpy as np                        # math (base R in R)
import pandas as pd                       # data wrangling (dplyr + readr in R)
from plotnine import *                    # visuals (ggplot2 in R)
from scipy import stats                   # qnorm() and pf() in R
import statsmodels.formula.api as smf     # lm() in R

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
damage_rate = np.round(np.arange(0, 0.6 + 0.001, 0.01), 2)   # seq(0, 0.6, by = 0.01) in R
print(pd.DataFrame({
  "damage_rate": damage_rate,
  # We can predict it using our hand-made function sc()
  "yhat": sc(damage_rate)})
  # See first few
  .head())


# 2. Prediction ########################################################

# Or (preferrably, we can use .predict() to do make predictions straight from the model object
rng = np.random.default_rng()
newdata = pd.DataFrame({"damage_rate": damage_rate})
dat_sim = newdata.assign(
  # Get predictions
  yhat=m.predict(newdata).values,
  # get sigma
  sigma=np.sqrt(m.scale))
# Simulate 1000 outcomes per damage rate (reframe(rnorm(...)) in R)
dat_sim = pd.DataFrame({
  "damage_rate": np.repeat(dat_sim["damage_rate"].values, 1000),
  "ysim": rng.normal(loc=np.repeat(dat_sim["yhat"].values, 1000),
                     scale=np.repeat(dat_sim["sigma"].values, 1000))})
dat_sim = (dat_sim.groupby("damage_rate", as_index=False)
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
dat_se = newdata.assign(
  # Get predictions
  yhat=m.predict(newdata).values,
  # get sigma
  sigma=np.sqrt(m.scale))
dat_se["lower"] = dat_se["yhat"] - 3 * dat_se["sigma"]
dat_se["upper"] = dat_se["yhat"] + 3 * dat_se["sigma"]
# They are almost identical!

(ggplot(dat_se, aes(x="damage_rate", y="yhat")) +
  geom_ribbon(mapping=aes(x="damage_rate", ymin="lower", ymax="upper"),
              fill="steelblue", alpha=0.5) +
  geom_line(linetype="dashed") +
  theme_classic() +
  labs(x="Damage Rate", y="Predicted Social Capital (6 sigmas)"))


# We can also compute confidence intervals for our predictions
# for any specified percentile.
dat_q = newdata.assign(
  yhat=m.predict(newdata).values,
  # Get residual standard error 'se'
  se=np.sqrt(m.scale),
  # Calculate the z-score on a normal distribution for the 97.5th percentile
  z=stats.norm.ppf(0.975))
# Give me an upper 95% confidence interval at the 97.5th percentile
dat_q["upper"] = dat_q["yhat"] + dat_q["se"] * dat_q["z"]
# Give me a lower 95% confidence interval at the 2.5th percentile
dat_q["lower"] = dat_q["yhat"] - dat_q["se"] * dat_q["z"]


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



d = pd.DataFrame({
  # predicted or expected
  "yhat": m.fittedvalues,
  # observed
  "y": m.model.endog})
# calculate the difference between the observed and expected...
d["residuals"] = d["y"] - d["yhat"]


y, yhat = d["y"], d["yhat"]
# all the variation in your data
tss = ((y - y.mean())**2).sum()
# sum of squared deviations
rss = ((y - yhat)**2).sum()
# EXPLAINED SUM OF SQUARES
ess = tss - rss
# PERCENTAGE OF VARIATION EXPLAINED, out of TOTAL VARIATION
rsq = ess / tss
rsq = 1 - rss / tss
print(pd.DataFrame({"tss": [tss], "rss": [rss], "ess": [ess], "rsq": [rsq]}))


# F-statistic







print(pd.DataFrame({
  "tss": [((y - y.mean())**2).sum()],
  "rss": [((y - yhat)**2).sum()],
  "rsq": [1 - ((y - yhat)**2).sum() / ((y - y.mean())**2).sum()]}))


# Calculate residual sum of squares
residual_sum_of_squares = ((y - yhat)**2).sum()
# Calculate total sum of squares
total_sum_of_squares = ((y - y.mean())**2).sum()
# Get sample size
n = len(d)
# Calculate number of variables in your model
p = 2
# Calculate explained sum of squares
ess = total_sum_of_squares - residual_sum_of_squares

# Mean Squares due to Regression, given the no. of predictors
mean_squares_due_to_regression = ess / (p - 1)
# Mean Squared Error
# How much variation was NOT explained, given the sample size and no. of variables
mean_squared_error = residual_sum_of_squares / (n - p)
# sigma-squared
# RMSE = sigma
sigma = np.sqrt(mean_squared_error)

# Compute the F-statistic, which is a ratio of explained vs. unexplained variation
f_statistic = mean_squares_due_to_regression / mean_squared_error
# Finally, throw it into stats.f.sf() (pf(..., lower.tail = FALSE) in R),
# which plots a theoretical null distribution
# based on the number of variables and sample size,
# and identifies how extreme our F-statistic is compared to one we'd get by chance
# Computes p-value
p_value = stats.f.sf(f_statistic, p - 1, n - p)

print(pd.Series({
  "residual_sum_of_squares": residual_sum_of_squares,
  "total_sum_of_squares": total_sum_of_squares, "n": n, "p": p, "ess": ess,
  "mean_squares_due_to_regression": mean_squares_due_to_regression,
  "mean_squared_error": mean_squared_error, "sigma": sigma,
  "f_statistic": f_statistic, "p_value": p_value}))

# IF our p-value is less than 5%,
# that's often a good indication
# that our model fits better than a simple intercept (mean) would.
# a good f-statistic
print(stats.f.sf(15, 2 - 1, 1057 - 2))

d.info()

print(get_stat(m))


print(np.sqrt(m.scale))   # glance(m)$sigma in R
print(m.resid.std())      # m$residuals %>% sd() in R
