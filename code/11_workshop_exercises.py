# 11_workshop_exercises.py
# Multivariate Regression: Modeling Effects of Disaster on Social Capital
# Tim Fraser

# Practice exercises paired with the textbook chapter
# "Multivariate Regression: Modeling Effects of Disaster on Social Capital"
# at timothyfraser.com/sigma.

# What this script does:
# Four numbered exercises on Japanese municipalities hit by the 2011
# tsunami. You estimate multivariate models of income per capita, practice
# writing up a slope in plain English with its confidence interval, compare
# logged vs. unlogged outcomes, control for time, and then predict across a
# range of damage rates while holding other predictors at chosen values.

# It mirrors 11_workshop_exercises.R section by section.
# Inputs: workshops/jp_matching_experiment.csv
#         Run this from the repo root, so the relative path resolves.
# Packages: numpy, pandas, statsmodels


import numpy as np                        # math (base R in R)
import pandas as pd                       # data wrangling (dplyr + readr in R)
import statsmodels.formula.api as smf     # lm() in R
from statsmodels.iolib.summary2 import summary_col   # screenreg() from texreg in R

cities = pd.read_csv("workshops/jp_matching_experiment.csv")
# Tell Python to treat year and pref as **ordered categories** (factor() in R)
cities["year"] = cities["year"].astype(str).astype("category")
cities["pref"] = cities["pref"].astype("category")
cities["by_tsunami"] = pd.Categorical(cities["by_tsunami"], categories=["Not Hit", "Hit"])

cities.info()   # glimpse() in R

# Show wide tables in full
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)



# Let's write a little stars function... (gtools::stars.pval() in R)
def stars_pval(p):
    return np.select([p < 0.001, p < 0.01, p < 0.05, p < 0.1],
                     ["***", "**", "*", "."], default=" ")

# Let's write a little tidier function..
def tidier(model, ci=0.95, digits=3):
    # for a model object, get a data.frame of coefficients
    # ask for a confidence interval matching the 'ci' above!
    conf = model.conf_int(alpha=1 - ci)
    # A predictor with no variation (like damage_rate in a prefecture the
    # tsunami never reached) cannot be estimated. lm() in R reports NA;
    # statsmodels reports 0 with a standard error of 0, so we blank those out.
    blank = (model.bse == 0).values
    conf = conf.mask(blank.reshape(-1, 1).repeat(2, axis=1))
    # And round and relabel them
    return pd.DataFrame({
      "term": model.params.index,
      # Round numbers to a certain number of 'digits'
      "estimate": model.params.mask(blank).round(digits).values,
      "se": model.bse.mask(blank).round(digits).values,
      "statistic": model.tvalues.mask(blank).round(digits).values,
      "p_value": model.pvalues.mask(blank).round(digits).values,
      # Get stars to show statistical significance
      "stars": np.where(blank, "", stars_pval(model.pvalues.values)),
      # Get better names
      "upper": conf[1].round(digits).values,
      "lower": conf[0].round(digits).values})

# A little glance() function too, for model-level statistics (broom::glance() in R)
def glance(model):
    return pd.DataFrame({"r_squared": [model.rsquared], "adj_r_squared": [model.rsquared_adj],
                         "sigma": [np.sqrt(model.scale)], "statistic": [model.fvalue],
                         "p_value": [model.f_pvalue], "df": [model.df_model],
                         "nobs": [int(model.nobs)]})

# And a screenreg() stand-in: models side by side, with R2 and N at the bottom
def screenreg(l, omit_coef=None):
    table = summary_col(l, stars=True, float_format="%0.2f",
                        model_names=[f"Model {i + 1}" for i in range(len(l))],
                        info_dict={"Num. obs.": lambda x: f"{int(x.nobs)}"})
    if omit_coef is not None:
        t = table.tables[0]
        # Each coefficient takes 2 rows (estimate, then standard error)
        keep = ~pd.Series(t.index, index=t.index).str.contains(omit_coef)
        rows = [i for i, name in enumerate(t.index)
                if keep.iloc[i] and not (name == "" and not keep.iloc[i - 1])]
        table.tables[0] = t.iloc[rows]
    return table




# 1. Estimate the effect of being hit by the tsunami on income per capita,
# controlling for damage rates.
m = smf.ols("income_per_capita ~  damage_rate + by_tsunami", data=cities).fit()
print(tidier(m))

# Report the effect of being hit by the tsunami.
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# This effect has a 95% confidence interval from [A] to [B].
# This effect is statistically [significant? insignificant?] with a p-value of [XXX].



# 2. Estimate the effect of being hit by the tsunami on
# the natural log of income per capita,
# controlling for damage rates.
# Compare this against a model without the natural log.
m1 = smf.ols("income_per_capita ~  damage_rate + by_tsunami", data=cities).fit()
m2 = smf.ols("np.log(income_per_capita) ~  damage_rate + by_tsunami", data=cities).fit()

print(screenreg(l=[m1, m2]))
# Do your slopes change? Do your units change?
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].






# 3. Model the effect of time on income per capita,
# controlling for relevant traits.
m1 = smf.ols("income_per_capita ~ pop_density + unemployment + "
             "damage_rate + by_tsunami + C(year)", data=cities).fit()
# (as.numeric(year) in R turns the year categories into 1, 2, 3, ...
#  year.cat.codes + 1 does the same here)
m2 = smf.ols("income_per_capita ~ pop_density + unemployment + "
             "damage_rate + by_tsunami + I(year.cat.codes + 1)", data=cities).fit()

# View the resulting statistical table.
# How does the information change when we control for year vs. each year?
print(screenreg(l=[m1, m2]))





# 4. Estimate a model of income per capita, predicted by
#     population density, unemployment, damage rates, and tsunami status.
m = smf.ols("income_per_capita ~ pop_density + unemployment + "
            "damage_rate + by_tsunami + year", data=cities).fit()

# Now predict the level of income per capita as damage rates increase
# from their min to their max.
# Choose MEANINGFUL levels to set other predictors to. Here's starter values.
newdata = pd.DataFrame({
  "pop_density": [10],
  "unemployment": [20],
  "damage_rate": [1],
  "by_tsunami": ["Hit"],
  "year": ["2012"]})
print(newdata.assign(yhat=m.predict(newdata).values))




# 5. Normalize these demographic covariates
# (mean = 0, in units of standard deviation from the mean)
# Now model them.
def scale(x):
    # scale() in R: subtract the mean, divide by the standard deviation
    return (x - x.mean()) / x.std()

print(smf.ols("income_per_capita ~ pop_density + unemployment + "
              "damage_rate + by_tsunami + year",
              data=cities.assign(pop_density=scale(cities["pop_density"]),
                                 unemployment=scale(cities["unemployment"]),
                                 damage_rate=scale(cities["damage_rate"]))).fit().params)

# Report the population density vs. unemployment, damage_rate
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# Which effect size is largest?
# Which effect sizes can you NOT compare?


# 6. Compare these 5 models, which each add extra covariates.
m1 = smf.ols("income_per_capita ~ damage_rate + by_tsunami", data=cities).fit()
m2 = smf.ols("income_per_capita ~ damage_rate + by_tsunami + "
             "year", data=cities).fit()
m3 = smf.ols("income_per_capita ~ damage_rate + by_tsunami + "
             "year + "
             "pop_density + unemployment", data=cities).fit()
m4 = smf.ols("income_per_capita ~ damage_rate + by_tsunami + "
             "year + "
             "pop_density + unemployment + "
             "exp_dis_relief_per_capita + pop_women + pop_over_age_65", data=cities).fit()
m5 = smf.ols("income_per_capita ~ damage_rate + by_tsunami + "
             "year + "
             "pop_density + unemployment + "
             "exp_dis_relief_per_capita + pop_women + pop_over_age_65 + "
             "pref", data=cities).fit()
# Show models but omit vars that contain year or prefecture, for clearer viewing
print(screenreg(l=[m1, m2, m3, m4, m5], omit_coef="pref|year"))

# How does the explanatory power change by model? (R2)
# Which covariates add the **most** explanatory power?





# 7. Which Year can we model best? Which has the Highest Explanatory Power?
# For each year, make a model and return a data.frame glance()-ing the model
print(cities.groupby("year", observed=True)
      .apply(lambda g: glance(smf.ols("income_per_capita ~ damage_rate + by_tsunami + "
                                      "pop_density + pref", data=g).fit()),
             include_groups=False)
      .reset_index(level=1, drop=True)
      .reset_index())
# Hint: look at r_squared.



# 8. In which prefecture (region) did the damage_rate have the worst effect?
# Get the model effects
data = (cities.groupby("pref", observed=True)
        .apply(lambda g: tidier(smf.ols("income_per_capita ~ damage_rate + pop_density + year",
                                        data=g).fit()),
               include_groups=False)
        .reset_index(level=1, drop=True)
        .reset_index())
# Filter the model effects
print(data[data["term"] == "damage_rate"])

# Report the effects.
# Disaster damage had the most negative effect [BETA] on wealth in [XXX] (p < VALUE),
# but the least negative effect [BETA] on wealth in [YYY] (p < VALUE)





# 9. Compare these two data.frames.
# What does it mean to estimate an intercept-only model?

# Intercept-only model
print(smf.ols("income_per_capita ~ 1", data=cities).fit().params)
# Descriptive Stats
print(pd.DataFrame({"mean": [cities["income_per_capita"].mean()]}))



# 10. Model the effect of each year on income.
# Which year is not represented? The intercept represents that baseline category.
print(cities["year"].unique())
m = smf.ols("income_per_capita ~ year", data=cities).fit()
print(m.params)
# Calculate the predicted income per capita from 2011 to 2017.
