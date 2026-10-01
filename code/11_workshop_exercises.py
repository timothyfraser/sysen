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
# Packages: numpy, pandas, statsmodels, plus functions/functions_models.py


import numpy as np                        # math (base R in R)
import pandas as pd                       # data wrangling (dplyr + readr in R)
from statsmodels.iolib.summary2 import summary_col   # screenreg() from texreg in R
from functions_models import lm, tidy, glance        # lm(), plus tidy() and glance() from broom in R
# Show wide tables in full
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

cities = pd.read_csv("workshops/jp_matching_experiment.csv")
# Tell Python to treat year and pref as **ordered categories** (factor() in R)
cities["year"] = cities["year"].astype(str).astype("category")
cities["pref"] = cities["pref"].astype("category")
cities["by_tsunami"] = pd.Categorical(cities["by_tsunami"], categories=["Not Hit", "Hit"])

cities.info()   # glimpse() in R



# Let's write a little tidier function..
def tidier(model, ci=0.95, digits=3):
    # for a model object, get data.frame of coefficients
    # ask for a confidence interval matching the 'ci' above!
    t = tidy(model, ci=ci)
    # A predictor with no variation (like damage_rate in a prefecture the
    # tsunami never reached) cannot be estimated. lm() in R reports NA;
    # statsmodels reports 0 with a standard error of 0, so we blank those out.
    blank = t["se"] == 0
    t.loc[blank, ["estimate", "se", "statistic", "p_value", "lower", "upper"]] = np.nan
    # And round and relabel them
    return pd.DataFrame({
      "term": t["term"],
      # Round numbers to a certain number of 'digits'
      "estimate": t["estimate"].round(digits),
      "se": t["se"].round(digits),
      "statistic": t["statistic"].round(digits),
      "p_value": t["p_value"].round(digits),
      # Get stars to show statistical significance (gtools::stars.pval() in R)
      "stars": np.where(blank, "", np.select([t["p_value"] < 0.001, t["p_value"] < 0.01,
                                              t["p_value"] < 0.05, t["p_value"] < 0.1],
                                             ["***", "**", "*", "."], default=" ")),
      # Get better names
      "upper": t["upper"].round(digits),
      "lower": t["lower"].round(digits)})

# texreg's screenreg() has no Python twin, so a small stand-in:
# models side by side, with R2 and N at the bottom
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
m = lm(formula="income_per_capita ~  damage_rate + by_tsunami", data=cities)
print(tidier(m))

# Report the effect of being hit by the tsunami.
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# This effect has a 95% confidence interval from [A] to [B].
# This effect is statistically [significant? insignificant?] with a p-value of [XXX].



# 2. Estimate the effect of being hit by the tsunami on
# the natural log of income per capita,
# controlling for damage rates.
# Compare this against a model without the natural log.
m1 = lm(formula="income_per_capita ~  damage_rate + by_tsunami", data=cities)
# (log() goes inside the formula in R; here we log the outcome as a column first)
m2 = lm(formula="log_income ~  damage_rate + by_tsunami",
        data=cities.assign(log_income=np.log(cities["income_per_capita"])))

print(screenreg(l=[m1, m2]))
# Do your slopes change? Do your units change?
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].






# 3. Model the effect of time on income per capita,
# controlling for relevant traits.
m1 = lm(formula="income_per_capita ~ pop_density + unemployment + "
                "damage_rate + by_tsunami + C(year)", data=cities)
# (as.numeric(year) in R turns the year categories into 1, 2, 3, ...
#  year.cat.codes + 1 does the same here)
m2 = lm(formula="income_per_capita ~ pop_density + unemployment + "
                "damage_rate + by_tsunami + I(year.cat.codes + 1)", data=cities)

# View the resulting statistical table.
# How does the information change when we control for year vs. each year?
print(screenreg(l=[m1, m2]))





# 4. Estimate a model of income per capita, predicted by
#     population density, unemployment, damage rates, and tsunami status.
m = lm(formula="income_per_capita ~ pop_density + unemployment + "
               "damage_rate + by_tsunami + year", data=cities)

# Now predict the level of income per capita as damage rates increase
# from their min to their max.
# Choose MEANINGFUL levels to set other predictors to. Here's starter values.
print(pd.DataFrame({
  "pop_density": [10],
  "unemployment": [20],
  "damage_rate": [1],
  "by_tsunami": ["Hit"],
  "year": ["2012"]})
  .assign(yhat=lambda d: m.predict(d).values))




# 5. Normalize these demographic covariates
# (mean = 0, in units of standard deviation from the mean)
# Now model them.
print(lm(formula="income_per_capita ~ pop_density + unemployment + "
                 "damage_rate + by_tsunami + year",
         # scale() in R: subtract the mean, divide by the standard deviation
         data=cities.assign(
           pop_density=lambda d: (d["pop_density"] - d["pop_density"].mean()) / d["pop_density"].std(),
           unemployment=lambda d: (d["unemployment"] - d["unemployment"].mean()) / d["unemployment"].std(),
           damage_rate=lambda d: (d["damage_rate"] - d["damage_rate"].mean()) / d["damage_rate"].std()))
      .params)

# Report the population density vs. unemployment, damage_rate
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# Which effect size is largest?
# Which effect sizes can you NOT compare?


# 6. Compare these 5 models, which each add extra covariates.
m1 = lm(formula="income_per_capita ~ damage_rate + by_tsunami", data=cities)
m2 = lm(formula="income_per_capita ~ damage_rate + by_tsunami + "
                "year", data=cities)
m3 = lm(formula="income_per_capita ~ damage_rate + by_tsunami + "
                "year + "
                "pop_density + unemployment", data=cities)
m4 = lm(formula="income_per_capita ~ damage_rate + by_tsunami + "
                "year + "
                "pop_density + unemployment + "
                "exp_dis_relief_per_capita + pop_women + pop_over_age_65", data=cities)
m5 = lm(formula="income_per_capita ~ damage_rate + by_tsunami + "
                "year + "
                "pop_density + unemployment + "
                "exp_dis_relief_per_capita + pop_women + pop_over_age_65 + "
                "pref", data=cities)
# Show models but omit vars that contain year or prefecture, for clearer viewing
print(screenreg(l=[m1, m2, m3, m4, m5], omit_coef="pref|year"))

# How does the explanatory power change by model? (R2)
# Which covariates add the **most** explanatory power?





# 7. Which Year can we model best? Which has the Highest Explanatory Power?
# For each year, make a model and return a data.frame glance()-ing the model
print(cities.groupby("year", observed=True)
      .apply(lambda g: glance(lm(formula="income_per_capita ~ damage_rate + by_tsunami + "
                                         "pop_density + pref", data=g)),
             include_groups=False)
      .reset_index(level=1, drop=True)
      .reset_index())
# Hint: look at rsq (r.squared in R).



# 8. In which prefecture (region) did the damage_rate have the worst effect?
# Get the model effects
data = (cities.groupby("pref", observed=True)
        .apply(lambda g: tidier(lm(formula="income_per_capita ~ damage_rate + pop_density + year",
                                   data=g)),
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
print(lm(formula="income_per_capita ~ 1", data=cities).params)
# Descriptive Stats
print(pd.DataFrame({"mean": [cities["income_per_capita"].mean()]}))



# 10. Model the effect of each year on income.
# Which year is not represented? The intercept represents that baseline category.
print(cities["year"].unique())
m = lm(formula="income_per_capita ~ year", data=cities)
print(m.params)
# Calculate the predicted income per capita from 2011 to 2017.
