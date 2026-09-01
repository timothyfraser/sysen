# 12_workshop.py
# Tim Fraser
# Workshop 12: Design of Experiments
# Chapter: Design of Experiments in R (Python twin — there is no Python DOE chapter;
# we use scipy.stats for t-tests / ANOVA and plotnine for the visuals.)

import pandas as pd
import numpy as np
from scipy import stats
from plotnine import *
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_models import lm, tidy, glance


# Unpaired t-tests ###############################################

data = pd.DataFrame({
    'method': ['A'] * 10 + ['B'] * 10,
    'yield': [89.7, 81.4, 84.5, 84.8, 87.3, 79.7, 85.1, 81.7, 83.7, 84.5,
              84.7, 86.1, 83.2, 91.9, 86.3, 79.3, 82.6, 89.1, 83.7, 88.5]
})

# T-test assuming equal variance (unpaired)
# R: t.test(yield ~ method, data, var.equal = TRUE)
a = data.loc[data['method'] == 'A', 'yield']
b = data.loc[data['method'] == 'B', 'yield']
stats.ttest_ind(a, b, equal_var=True)


# T-test not assuming equal variance
stats.ttest_ind(a, b, equal_var=False)


# Variance F-tests ################################

# How different are the variances?
(data.groupby('method')
 .agg(var=('yield', 'var'))
 .reset_index())

# Is that difference significant?
# F test to compare two variances.
# R: var.test(yield ~ method, data)
# scipy has no named var.test; F = var_a / var_b against F(n_a-1, n_b-1)
f_stat = a.var(ddof=1) / b.var(ddof=1)
p_var = 2 * min(stats.f.cdf(f_stat, len(a) - 1, len(b) - 1),
                1 - stats.f.cdf(f_stat, len(a) - 1, len(b) - 1))
pd.DataFrame({'statistic': [f_stat], 'p_value': [p_var]})
# Are they significantly different? (No --> p around 0.50)


# How would we do this in a 'tidy' way?

def tidy_ttest(a, b, equal_var=True, paired=False):
    if paired:
        res = stats.ttest_rel(a, b)
        estimate = (np.asarray(a) - np.asarray(b)).mean()
    else:
        res = stats.ttest_ind(a, b, equal_var=equal_var)
        estimate = np.asarray(a).mean() - np.asarray(b).mean()
    df = res.df if hasattr(res, 'df') else np.nan
    se = abs(estimate / res.statistic) if res.statistic != 0 else np.nan
    tcrit = stats.t.ppf(0.975, df) if np.isfinite(df) else np.nan
    return pd.DataFrame({
        'estimate': [estimate],
        'statistic': [res.statistic],
        'p_value': [res.pvalue],
        'conf.low': [estimate - tcrit * se],
        'conf.high': [estimate + tcrit * se]
    })

tidy_ttest(a, b, equal_var=True)

# 'statistic' is the t-statistic.
# 'p_value' is the p-value of the t-statistic
# 'estimate' is the difference of means.
# 'conf.low' and 'conf.high' are the 95% confidence intervals
#      around the difference of means.




# Paired t-tests ##################################################

# When data comes in pairs, like this, we use paired t-tests.
data2 = pd.DataFrame({
    'yield_a': [89.7, 81.4, 84.5, 84.8, 87.3, 79.7, 85.1, 81.7, 83.7, 84.5],
    'yield_b': [84.7, 86.1, 83.2, 91.9, 86.3, 79.3, 82.6, 89.1, 83.7, 88.5]
})


# Basic method for paired t-test
stats.ttest_rel(data2['yield_a'], data2['yield_b'])

# Or, do it in a data.frame friendly way like this:
tidy_ttest(data2['yield_a'], data2['yield_b'], paired=True)



# Permutation Test #################################################

# How would we do a permutation test of the difference of means?


# Let's do 1 permutation together.

# Randomly shuffle the outcomes across groups
shuffled = data.copy()
shuffled['yield'] = np.random.permutation(shuffled['yield'].values)

# Get back the means for A and B, and the difference
shuffled = data.copy()
shuffled['yield'] = np.random.permutation(shuffled['yield'].values)
pd.DataFrame({
    'xbar_a': [shuffled.loc[shuffled['method'] == 'A', 'yield'].mean()],
    'xbar_b': [shuffled.loc[shuffled['method'] == 'B', 'yield'].mean()]
}).assign(dbar=lambda df: df['xbar_a'] - df['xbar_b'])


# Let's try it 1000 times!

def one_perm(data):
    y = np.random.permutation(data['yield'].values)
    xbar_a = y[data['method'] == 'A'].mean()
    xbar_b = y[data['method'] == 'B'].mean()
    return xbar_a - xbar_b

perms = pd.DataFrame({
    'rep': range(1, 1001),
    'dbar': [one_perm(data) for _ in range(1000)]
})
perms

# Get the observed difference of means
obs = pd.DataFrame({
    'xbar_a': [data.loc[data['method'] == 'A', 'yield'].mean()],
    'xbar_b': [data.loc[data['method'] == 'B', 'yield'].mean()]
}).assign(dbar=lambda df: df['xbar_a'] - df['xbar_b'])


# Now, what percentage of random stats were greater than the observed?
# That's our p-value!

# 1-tailed test
(perms['dbar'] >= obs['dbar'].iloc[0]).mean()

# 2-tailed test --> turn all dbars positive
(np.abs(perms['dbar']) >= abs(obs['dbar'].iloc[0])).mean()


# Or in a tidy way...
pd.DataFrame({
    'estimate': [obs['dbar'].iloc[0]],
    'p_value': [(np.abs(perms['dbar']) >= abs(obs['dbar'].iloc[0])).mean()]
})

# Visualize it!


(ggplot() +
    geom_histogram(data=perms, mapping=aes(x='dbar'), fill='dodgerblue', color='white', bins=30) +
    geom_vline(data=obs, mapping=aes(xintercept='dbar')) +
    geom_label(data=obs, mapping=aes(y=50, x='dbar', label='dbar'), ha='left'))



# ANOVA ###################################################

donuts = pd.read_csv("workshops/donuts.csv")
# Or from github:
# donuts = pd.read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/donuts.csv")

# Use lm()...
glance(lm(formula='weight ~ baker', data=donuts))[['sigma', 'statistic', 'p_value', 'df']]

# Or use scipy.stats.f_oneway()...
groups = [g['weight'].values for _, g in donuts.groupby('baker')]
f_oneway = stats.f_oneway(*groups)
pd.DataFrame({'statistic': [f_oneway.statistic], 'p_value': [f_oneway.pvalue]})

# Visualize the difference
means = (donuts.groupby('baker', as_index=False)
         .agg(xbar=('weight', 'mean')))

(ggplot() +
    geom_violin(data=donuts, mapping=aes(x='baker', y='weight')) +
    geom_point(data=donuts, mapping=aes(x='baker', y='weight')) +
    geom_point(data=means, mapping=aes(x='baker', y='xbar'), color='dodgerblue', size=5) +
    geom_hline(yintercept=donuts['weight'].mean(), color='dodgerblue') +
    coord_flip())


# Unequal Variances #####################################

# Are the variances of my 3+ groups significantly different?
# Homogeneity of Variance - Bartlett's test for K^2
stats.bartlett(*groups)

# K-squared is a ratio showing how different are the variances, from 0 to infinity.
# If K-squared is not significant, the differences are not significant.

# Looks like the differences in variance are quite significant.
# Best **not** to assume equal variance.

# You can do an ANOVA without the equal variance assumption.
# R: oneway.test(..., var.equal = FALSE) is Welch's ANOVA.
# scipy.stats.alexandergovern is the closest named test; f_oneway assumes equal variance.
stats.alexandergovern(*groups)
