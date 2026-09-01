# 11_workshop.py
# Tim Fraser
# Workshop 11: Multivariate Regression - Effects of Disaster on Social Capital
# Chapter: Multivariate Regression: Modeling Effects of Disaster on Social Capital in Python



# 0. Getting Started ######################################################

import pandas as pd
import numpy as np
from plotnine import *
from scipy.stats import norm
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_models import lm, tidy, glance, htmlreg
from functions_distributions import hist, rnorm

cities = pd.read_csv("workshops/jp_matching_experiment.csv")
# Tell Python to treat year and pref as **ordered categories**
cities['year'] = cities['year'].astype('category')
cities['pref'] = cities['pref'].astype('category')
cities['by_tsunami'] = pd.Categorical(cities['by_tsunami'],
                                      categories=['Not Hit', 'Hit'])

cities.info()



# 0.1 Importing Data #########################################################


# You can download the data from github, upload it, and then read it in like this
pd.read_csv("workshops/jp_matching_experiment.csv").head()

# Or you could just load in the data like this:
# cities = pd.read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/jp_matching_experiment.csv")

cities = pd.read_csv("workshops/jp_matching_experiment.csv")
cities['year'] = cities['year'].astype('category')
cities['pref'] = cities['pref'].astype('category')
cities['by_tsunami'] = pd.Categorical(cities['by_tsunami'],
                                      categories=['Not Hit', 'Hit'])

# Think that's way easier? We can make a little function to make it easier to get this data.
# I'll add in some defaults like author, repository, and branch to make it easy to download data from our repository
def github_csv(file, author="timothyfraser", repository="sysen", branch="main"):
    return ("https://raw.githubusercontent.com/" +
            author + "/" + repository + "/" + branch + "/" + file)

# Boom!
pd.read_csv(github_csv("workshops/jp_matching_experiment.csv")).head()


# Check it out!
cities.head()

# Each row in this dataset is a city-year, in a prefecture,
# covering city-years in the Tohoku region,
# the region affected by the 2011 earthquake, tsunami, and nuclear disaster in Japan
(cities
 .query("pref == 'Fukushima'")
 .query("year == 2012"))

# I prefer using .info() from pandas
# to see the structure of my data
cities.info()

# 1. Modeling #########################################################

# We can make a simple regression model 'm'
# The Python tutorial uses functions_models.lm() — R-style formulas on a DataFrame.
m = lm(formula='social_capital ~ damage_rate', data=cities)

# View the equation
m.params
# Write the equation!
# Y (social_capital) = 0.39 + 0.07485 * damage_rate

# We can write a function of our model equation, if we want
def sc(x):
    return 0.394 + 0.0749 * x

# We should first calculate our goodness of fit statistics, which I call 'gof'
gof = glance(m)[['rsq', 'sigma', 'statistic', 'p_value']]
# View it!
gof

# R2 = % of variation explained --> get to 1
# sigma = residual standard error --> error of our model predictions
# statistic (F) = ratio. how much better is my model than an intercept model
# p-value = p-value of the f-statistic = how extreme is my f statistic?
# p < 0.10. p < 0.05. p < 0.01 = great indicators that F is extreme (model is good / better than nothing)

# We can view model coefficients.
tidy(m)

# Finally, what's the general range of our main predictor damage_rate?
hist(cities['damage_rate'])

# Let's predict, as the damage rate in a city increases, how does its social capital change?
pd.DataFrame({
    'damage_rate': np.arange(0, 0.61, 0.01),
    # We can predict it using our hand-made function sc()
    'yhat': sc(np.arange(0, 0.61, 0.01))
}).head()


# 2. Prediction ########################################################

# Or (preferably, we can use m.predict() to make predictions straight from the model object
damage_grid = np.arange(0, 0.61, 0.01)
dat_base = pd.DataFrame({
    'damage_rate': damage_grid,
    'yhat': m.predict(pd.DataFrame({'damage_rate': damage_grid})),
    'sigma': glance(m)['sigma'].iloc[0]
})

rows = []
for _, row in dat_base.iterrows():
    ysim = rnorm(n=1000, mean=row['yhat'], sd=row['sigma'])
    rows.append({
        'damage_rate': row['damage_rate'],
        'median': np.median(ysim),
        'lower': np.quantile(ysim, 0.025),
        'upper': np.quantile(ysim, 0.975)
    })
dat_sim = pd.DataFrame(rows)


(dat_sim
 .pipe(lambda df: ggplot(df, aes(x='damage_rate', y='median', ymin='lower', ymax='upper')) +
       geom_ribbon() +
       labs(x='Damage Rate', y='Predicted Social Capital (Simulated 95% CIs)')))


# What IS the residual standard error sigma?
# Well, we can approximate it pretty decently by taking the standard deviation of our models' residuals.
# A residual is the observed minus predicted value for each data point
pd.DataFrame({
    'sd': [m.resid.std()],
    'se': [glance(m)['sigma'].iloc[0]]
})


# Let's get the 6-sigma range
dat_se = pd.DataFrame({
    'damage_rate': damage_grid,
    'yhat': m.predict(pd.DataFrame({'damage_rate': damage_grid})),
    'sigma': glance(m)['sigma'].iloc[0]
})
dat_se['lower'] = dat_se['yhat'] - 3 * dat_se['sigma']
dat_se['upper'] = dat_se['yhat'] + 3 * dat_se['sigma']
# They are almost identical!

(dat_se
 .pipe(lambda df: ggplot(df, aes(x='damage_rate', y='yhat')) +
       geom_ribbon(aes(ymin='lower', ymax='upper'),
                   fill='steelblue', alpha=0.5) +
       geom_line(linetype='dashed') +
       theme_classic() +
       labs(x='Damage Rate', y='Predicted Social Capital (6 sigmas)')))


# We can also compute confidence intervals for our predictions
# for any specified percentile.
dat_q = pd.DataFrame({
    'damage_rate': damage_grid,
    'yhat': m.predict(pd.DataFrame({'damage_rate': damage_grid})),
    'se': glance(m)['sigma'].iloc[0],
    'z': norm.ppf(0.975)
})
dat_q['upper'] = dat_q['yhat'] + dat_q['se'] * dat_q['z']
dat_q['lower'] = dat_q['yhat'] - dat_q['se'] * dat_q['z']


(dat_q
 .pipe(lambda df: ggplot(df, aes(x='damage_rate', y='yhat')) +
       geom_ribbon(aes(ymin='lower', ymax='upper'),
                   fill='steelblue', alpha=0.5) +
       geom_line(linetype='dashed') +
       theme_classic() +
       labs(x='Damage Rate', y='Predicted Social Capital (95% CI)')))



# Let's compare all three!

(ggplot() +
    geom_ribbon(
        data=dat_se,
        mapping=aes(x='damage_rate', ymin='lower', ymax='upper',
                    fill='"6 sigma"'), alpha=0.5) +
    geom_ribbon(
        data=dat_q,
        mapping=aes(x='damage_rate', ymin='lower', ymax='upper',
                    fill='"95% CI"'), alpha=0.5) +
    geom_ribbon(
        data=dat_sim,
        mapping=aes(x='damage_rate', ymin='lower', ymax='upper',
                    fill='"Simulated 95% CI"'), alpha=0.5) +
    geom_line(
        data=dat_se,
        mapping=aes(x='damage_rate', y='yhat'), linetype='dashed') +
    scale_fill_manual(values=['steelblue', 'goldenrod', 'firebrick']) +
    theme_classic() +
    labs(x='Damage Rate', y='Predicted Social Capital', fill='CI Type') +
    theme(legend_position='bottom'))



# 3. Key Stats of Interest #########################

m = lm(formula='income_per_capita ~ damage_rate', data=cities)

def get_stat(m):
    return glance(m)[['rsq', 'sigma', 'statistic', 'p_value']]

get_stat(m)


m.params
m.fittedvalues



d = pd.DataFrame({
    # predicted or expected
    'yhat': m.fittedvalues,
    # observed
    'y': m.model.endog
})
d['residuals'] = d['y'] - d['yhat']


d_stats = pd.DataFrame({
    # all the variation in your data
    'tss': [((d['y'] - d['y'].mean()) ** 2).sum()],
    # sum of squared deviations
    'rss': [((d['y'] - d['yhat']) ** 2).sum()]
})
d_stats['ess'] = d_stats['tss'] - d_stats['rss']
d_stats['rsq'] = d_stats['ess'] / d_stats['tss']
d_stats['rsq_alt'] = 1 - d_stats['rss'] / d_stats['tss']
d_stats


# F-statistic







pd.DataFrame({
    'tss': [((d['y'] - d['y'].mean()) ** 2).sum()],
    'rss': [((d['y'] - d['yhat']) ** 2).sum()],
})


n = len(d)
p = 2
rss = ((d['y'] - d['yhat']) ** 2).sum()
tss = ((d['y'] - d['y'].mean()) ** 2).sum()
ess = tss - rss
mean_squares_due_to_regression = ess / (p - 1)
mean_squared_error = rss / (n - p)
sigma = np.sqrt(mean_squared_error)
f_statistic = mean_squares_due_to_regression / mean_squared_error
from scipy.stats import f as f_dist
p_value = 1 - f_dist.cdf(f_statistic, dfn=p - 1, dfd=n - p)
pd.DataFrame({
    'residual_sum_of_squares': [rss],
    'total_sum_of_squares': [tss],
    'n': [n],
    'p': [p],
    'ess': [ess],
    'mean_squares_due_to_regression': [mean_squares_due_to_regression],
    'mean_squared_error': [mean_squared_error],
    'sigma': [sigma],
    'f_statistic': [f_statistic],
    'p_value': [p_value]
})

# IF our p-value is less than 5%,
# that's often a good indication
# that our model fits better than a simple intercept (mean) would.
# a good f-statistic
1 - f_dist.cdf(15, dfn=2 - 1, dfd=1057 - 2)

d.info()

glance(m)


glance(m)['sigma'].iloc[0]
m.resid.std()
