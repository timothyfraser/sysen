# 11_workshop_exercises.py
# Multivariate Regression: Modeling Effects of Disaster on Social Capital
# Tim Fraser

# Practice exercises paired with the textbook chapter
# "Multivariate Regression: Modeling Effects of Disaster on Social Capital in Python"
# at timothyfraser.com/sigma.

# What this script does:
# Four numbered exercises on Japanese municipalities hit by the 2011
# tsunami. You estimate multivariate models of income per capita, practice
# writing up a slope in plain English with its confidence interval, compare
# logged vs. unlogged outcomes, control for time, and then predict across a
# range of damage rates while holding other predictors at chosen values.

# Inputs: workshops/jp_matching_experiment.csv
#         Run this from the repo root, so the relative path resolves.
# Packages: pandas, numpy, functions_models (lm, tidy, glance, htmlreg)

import pandas as pd
import numpy as np
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_models import lm, tidy, glance, htmlreg

cities = pd.read_csv("workshops/jp_matching_experiment.csv")
# Tell Python to treat year and pref as **ordered categories**
cities['year'] = cities['year'].astype('category')
cities['pref'] = cities['pref'].astype('category')
cities['by_tsunami'] = pd.Categorical(cities['by_tsunami'],
                                      categories=['Not Hit', 'Hit'])

cities.info()



# Let's write a little tidier function..
def tidier(model, ci=0.95, digits=3):
    out = tidy(model, ci=ci)
    def stars(p):
        if p < 0.001:
            return '***'
        if p < 0.01:
            return '**'
        if p < 0.05:
            return '*'
        if p < 0.1:
            return '.'
        return ''
    out = out.copy()
    out['estimate'] = out['estimate'].round(digits)
    out['se'] = out['se'].round(digits)
    out['statistic'] = out['statistic'].round(digits)
    out['p_value'] = out['p_value'].round(digits)
    out['stars'] = [stars(p) for p in tidy(model, ci=ci)['p_value']]
    out['upper'] = out['upper'].round(digits)
    out['lower'] = out['lower'].round(digits)
    return out[['term', 'estimate', 'se', 'statistic', 'p_value', 'stars', 'upper', 'lower']]



# 1. Estimate the effect of being hit by the tsunami on income per capita,
# controlling for damage rates.
m = lm(formula='income_per_capita ~ damage_rate + by_tsunami', data=cities)
tidier(m)

# Report the effect of being hit by the tsunami.
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# This effect has a 95% confidence interval from [A] to [B].
# This effect is statistically [significant? insignificant?] with a p-value of [XXX].



# 2. Estimate the effect of being hit by the tsunami on
# the natural log of income per capita,
# controlling for damage rates.
# Compare this against a model without the natural log.
m1 = lm(formula='income_per_capita ~ damage_rate + by_tsunami', data=cities)
cities_log = cities.assign(log_income=lambda df: np.log(df['income_per_capita']))
m2 = lm(formula='log_income ~ damage_rate + by_tsunami', data=cities_log)

print(htmlreg([m1, m2]))
# Do your slopes change? Do your units change?
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].






# 3. Model the effect of time on income per capita,
# controlling for relevant traits.
m1 = lm(formula='income_per_capita ~ pop_density + unemployment + damage_rate + by_tsunami + year',
        data=cities)
cities_num = cities.copy()
cities_num['year_num'] = cities_num['year'].astype(int)
m2 = lm(formula='income_per_capita ~ pop_density + unemployment + damage_rate + by_tsunami + year_num',
        data=cities_num)

# View the resulting statistical table.
# How does the information change when we control for year vs. each year?
print(htmlreg([m1, m2]))




# 4. Estimate a model of income per capita, predicted by
#     population density, unemployment, damage rates, and tsunami status.
m = lm(formula='income_per_capita ~ pop_density + unemployment + damage_rate + by_tsunami + year',
       data=cities)

# Now predict the level of income per capita as damage rates increase
# from their min to their max.
# Choose MEANINGFUL levels to set other predictors to. Here's starter values.
newdata = pd.DataFrame({
    'pop_density': [10],
    'unemployment': [20],
    'damage_rate': [1],
    'by_tsunami': ['Hit'],
    'year': [2012]
})
newdata['year'] = newdata['year'].astype(cities['year'].dtype)
newdata['by_tsunami'] = pd.Categorical(newdata['by_tsunami'],
                                       categories=cities['by_tsunami'].cat.categories)
newdata = newdata.assign(yhat=m.predict(newdata))
newdata




# 5. Normalize these demographic covariates
# (mean = 0, in units of standard deviation from the mean)
# Now model them.
rescaled = cities.copy()
for var in ['pop_density', 'unemployment', 'damage_rate']:
    rescaled[var] = (rescaled[var] - rescaled[var].mean()) / rescaled[var].std(ddof=0)

lm(formula='income_per_capita ~ pop_density + unemployment + damage_rate + by_tsunami + year',
   data=rescaled)

# Report the population density vs. unemployment, damage_rate
# As [X] increases by 1 [unit], [Y] increases by [BETA] [units].
# Which effect size is largest?
# Which effect sizes can you NOT compare?


# 6. Compare these 5 models, which each add extra covariates.
m1 = lm(formula='income_per_capita ~ damage_rate + by_tsunami', data=cities)
m2 = lm(formula='income_per_capita ~ damage_rate + by_tsunami + year', data=cities)
m3 = lm(formula='income_per_capita ~ damage_rate + by_tsunami + year + pop_density + unemployment',
        data=cities)
m4 = lm(formula='income_per_capita ~ damage_rate + by_tsunami + year + pop_density + unemployment + exp_dis_relief_per_capita + pop_women + pop_over_age_65',
        data=cities)
m5 = lm(formula='income_per_capita ~ damage_rate + by_tsunami + year + pop_density + unemployment + exp_dis_relief_per_capita + pop_women + pop_over_age_65 + pref',
        data=cities)
# Show models. htmlreg() is the Python twin of texreg::screenreg().
print(htmlreg([m1, m2, m3, m4, m5]))

# How does the explanatory power change by model? (R2)
# Which covariates add the **most** explanatory power?





# 7. Which Year can we model best? Which has the Highest Explanatory Power?
# For each year, make a model and return a data.frame glance()-ing the model
rows = []
for year, grp in cities.groupby('year', observed=True):
    g = glance(lm(formula='income_per_capita ~ damage_rate + by_tsunami + pop_density + pref',
                  data=grp))
    g.insert(0, 'year', year)
    rows.append(g)
pd.concat(rows, ignore_index=True)
# Hint: look at rsq.



# 8. In which prefecture (region) did the damage_rate have the worst effect?
# Get the model effects
rows = []
for pref, grp in cities.groupby('pref', observed=True):
    t = tidier(lm(formula='income_per_capita ~ damage_rate + pop_density + year', data=grp))
    t.insert(0, 'pref', pref)
    rows.append(t)
data = pd.concat(rows, ignore_index=True)
# Filter the model effects
data[data['term'] == 'damage_rate']

# Report the effects.
# Disaster damage had the most negative effect [BETA] on wealth in [XXX] (p < VALUE),
# but the least negative effect [BETA] on wealth in [YYY] (p < VALUE)




# 9. Compare these two data.frames.
# What does it mean to estimate an intercept-only model?

# Intercept-only model
lm(formula='income_per_capita ~ 1', data=cities).params
# Descriptive Stats
cities['income_per_capita'].mean()



# 10. Model the effect of each year on income.
# Which year is not represented? The intercept represents that baseline category.
cities['year'].unique()
m = lm(formula='income_per_capita ~ year', data=cities)
m.params
# Calculate the predicted income per capita from 2011 to 2017.
