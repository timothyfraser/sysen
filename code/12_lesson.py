# 12_lesson.py
# Tim Fraser
# Lesson 12: Design of Experiments
# Chapter: Design of Experiments in R (Python twin)

# Load packages
import pandas as pd
import numpy as np
from scipy import stats
from plotnine import *
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_models import lm, tidy, glance

# Read data!
donuts = pd.read_csv("workshops/donuts.csv")

donuts.info()
# Having trouble reading in your data?
# You can also use this code:
# donuts = pd.read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/donuts.csv")


donuts

groups = [g['tastiness'].values for _, g in donuts.groupby('baker')]
stats.f_oneway(*groups)

# tastiness varies significantly between bakers
stats.f_oneway(*groups)

glance(lm(formula='tastiness ~ baker', data=donuts))



donuts3 = donuts[donuts['baker'].isin(['Craig', 'Melanie'])]


a = donuts3.loc[donuts3['baker'] == 'Craig', 'tastiness']
b = donuts3.loc[donuts3['baker'] == 'Melanie', 'tastiness']
stats.ttest_ind(a, b, equal_var=True)



donuts3 = donuts3.copy()
donuts3['baker'] = pd.Categorical(donuts3['baker'],
                                  categories=['Melanie', 'Craig'])

a = donuts3.loc[donuts3['baker'] == 'Melanie', 'tastiness']
b = donuts3.loc[donuts3['baker'] == 'Craig', 'tastiness']
stats.ttest_ind(a, b, equal_var=True)



# Convert type to factor, where treatment group b is first
donuts2 = donuts.copy()
donuts2['type'] = pd.Categorical(donuts2['type'], categories=['b', 'a'])



# Tidy long format
long = (donuts.groupby('type', as_index=False)
        .agg(xbar=('tastiness', 'mean'))
        .assign(testid=1))


# Wide matrix
wide = pd.DataFrame({'xbar_a': [2.84], 'xbar_b': [4.16]})
wide = wide.assign(dbar=lambda df: df['xbar_b'] - df['xbar_a'])


long

long.pivot(index='testid', columns='type', values='xbar').assign(
    dbar=lambda df: df['b'] - df['a']
)



# T-test Examples ##########################################################

donuts2 = donuts.copy()
donuts2['type'] = pd.Categorical(donuts2['type'], categories=['a', 'b'])


a = donuts2.loc[donuts2['type'] == 'a', 'weight']
b = donuts2.loc[donuts2['type'] == 'b', 'weight']
res = stats.ttest_ind(a, b, equal_var=True)
pd.DataFrame({
    'estimate': [a.mean() - b.mean()],
    'statistic': [res.statistic],
    'p_value': [res.pvalue]
})


tidy(lm(formula='weight ~ type', data=donuts2))

(donuts2.groupby('type', as_index=False)
 .agg(xbar=('weight', 'mean')))

# There's a -3.4 gram difference (95% CI is -1.8 ~ -4.9, p < 0.001)
# What if we knew that 1 gram costs us $0.01
# What if we knew that we're going to produce 50,000 donuts
#

dbar = -3.4
dbar_lower = -1.8
n = 50000
cost_per_gram = 0.01
dbar * cost_per_gram * n



(donuts.groupby('type', as_index=False)
 .agg(var=('weight', 'var')))



res = stats.ttest_ind(a, b, equal_var=False)
pd.DataFrame({
    'statistic': [res.statistic],
    'p_value': [res.pvalue]
})




(ggplot() +
    geom_violin(data=donuts2, mapping=aes(x='type', y='weight')) +
    geom_jitter(data=donuts2, mapping=aes(x='type', y='weight')))


(ggplot() +
    geom_boxplot(data=donuts2, mapping=aes(x='type', y='weight')) +
    geom_jitter(data=donuts2, mapping=aes(x='type', y='weight')))






donuts.info()


donuts.groupby('baker').size()


m = lm(formula='tastiness ~ baker', data=donuts)

m.params


tidy(m)


m.params

tidy(m).assign(t=lambda df: (df['estimate'] - 0) / df['se'])


m.summary()


(tidy(m, ci=0.95)
 .pipe(lambda df: ggplot(df, aes(x='term', y='estimate',
                                 ymin='lower', ymax='upper')) +
       geom_linerange() +
       geom_point()))


# Let's see a t distribution with 47 degrees of freedom
from functions_distributions import hist
hist(stats.t.rvs(df=47, size=1000))


# Let's get confidence intervals...
(tidy(m, ci=True)
 .query("term == 'baker[T.Melanie]'")
 [['term', 'lower']])

pd.concat([
    tidy(lm(formula='tastiness ~ baker', data=donuts)).assign(model=1),
    tidy(lm(formula='tastiness ~ baker + weight', data=donuts)).assign(model=2)
]).query("term == 'baker[T.Melanie]'")



donuts_z = donuts.copy()
donuts_z['weight'] = (donuts_z['weight'] - donuts_z['weight'].mean()) / donuts_z['weight'].std(ddof=0)
donuts_z['lifespan'] = (donuts_z['lifespan'] - donuts_z['lifespan'].mean()) / donuts_z['lifespan'].std(ddof=0)
lm(formula='tastiness ~ weight + lifespan + baker', data=donuts_z)

# As weight increased by 1 standard deviation,
# tastiness changes by 0.26

# As lifespan increases by 1 standard deviation,
# tastiness changes by -0.06



# Permutation Test Examples ##################################################

donuts = pd.read_csv("workshops/donuts.csv")


obs_dbar = (donuts.loc[donuts['baker'] == 'Melanie', 'tastiness'].mean() -
            donuts.loc[donuts['baker'] == 'Craig', 'tastiness'].mean())

obs_dbar

donuts.assign(tastiness=lambda df: np.random.permutation(df['tastiness'].values))

def one_perm():
    y = np.random.permutation(donuts['tastiness'].values)
    return (y[donuts['baker'] == 'Melanie'].mean() -
            y[donuts['baker'] == 'Craig'].mean())

mydbar = pd.DataFrame({
    'reps': range(1, 1001),
    'dbar': [one_perm() for _ in range(1000)]
})


(ggplot() +
    geom_histogram(data=mydbar, mapping=aes(x='dbar'), bins=30) +
    geom_vline(xintercept=obs_dbar))


(mydbar['dbar'] > obs_dbar).mean()
