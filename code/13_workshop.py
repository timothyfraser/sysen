# 13_workshop.py
# Tim Fraser
# Workshop 13: Interaction Effects in Python
# Chapter: Factorial Design and Interaction Effects in Python

import pandas as pd
import numpy as np
from scipy.stats import norm
from plotnine import *
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_models import lm
from functions_factorial import se_factorial, dbar_oneway, dbar_twoway, dbar_threeway

# Load in data!
# If you upload it to your workshops folder, read it in like this...
lattes = pd.read_csv("workshops/lattes.csv")
# Let's shorten our main metric name
lattes = lattes.rename(columns={'tastiness': 'y'})

# View it
lattes

# Show the types
lattes['machine'].unique()
lattes['syrup'].unique()
lattes['art'].unique()
# Also, looks like we randomly assigned the type of milk too.
# We'll treat this as a control
lattes['milk'].unique()


# Calculate a standard error the tastiness metric in this factorial experiment
grouped = (lattes.groupby(['machine', 'syrup', 'art'])
           .agg(s=('y', 'std'), n=('y', 'size'))
           .reset_index())
se = np.sqrt((grouped['s'] ** 2 / grouped['n']).sum())

se



# Example 1: Calculate Direct Effects ########################

# Calculate the direct effect of having a heart vs. foam in your latte

lattes['y'][lattes['machine'] == 'a'].mean() - lattes['y'][lattes['machine'] == 'b'].mean()


stat = pd.DataFrame({
    'dbar': [lattes.loc[lattes['machine'] == 'a', 'y'].mean() -
             lattes.loc[lattes['machine'] == 'b', 'y'].mean()],
    'se': [se],
    'name': ['Machine A - B']
})
stat['z'] = norm.ppf(0.975)
stat['upper'] = stat['dbar'] + stat['z'] * stat['se']
stat['lower'] = stat['dbar'] - stat['z'] * stat['se']

stat

stat = stat.assign(
    upper_lab=lambda df: (df['upper'] + 2).round(2),
    lower_lab=lambda df: (df['lower'] - 2).round(2)
)
(ggplot() +
    geom_point(data=stat, mapping=aes(x='name', y='dbar')) +
    geom_crossbar(data=stat, mapping=aes(x='name', y='dbar', ymin='lower', ymax='upper'),
                  fill='violetred') +
    geom_hline(yintercept=0, linetype='dashed') +
    geom_text(data=stat, mapping=aes(x='name', y='upper', label='upper_lab')) +
    geom_text(data=stat, mapping=aes(x='name', y='lower', label='lower_lab')))


# Visualize it!
(ggplot() +
    geom_crossbar(
        data=stat,
        mapping=aes(x='name', y='dbar', ymin='lower', ymax='upper')) +
    geom_hline(yintercept=0, linetype='dashed'))
# Is that effect significant with 95% confidence?




# FUNCTIONS ######################################

# When doing really nitty-gritty calculations like this,
# functions will become our friends.

# The Python tutorial writes the same dbar helpers we already ship in
# functions/functions_factorial.py. Load them (done at the top) rather than
# retyping 100 lines. If you want to see how they work, open that file.

# Generate your interaction effects for a 2^3 factorial experiment
dbar_oneway(formula='y ~ machine', data=lattes)

# Highest alphabetic level - Lowest Alphabetical Level
# B - A


lattes['machine'].unique()
# B - A
dbar_oneway(formula='y ~ machine', data=lattes)

lattes['syrup'].unique()
# Torani - Monin
dbar_oneway(formula='y ~ syrup', data=lattes)


lattes['art'].unique()
# Heart - Foamy
dbar_oneway(formula='y ~ art', data=lattes)


# B*Torani - A*Monin
dbar_twoway(formula='y ~ machine * syrup', data=lattes)

# B*Heart - A*Foamy
dbar_twoway(formula='y ~ machine * art', data=lattes)

# B*Heart*Torani - A*Foamy*Monin
dbar_threeway(formula='y ~ machine * syrup * art', data=lattes)


# Get your standard error free of charge
se_factorial(formula='y ~ machine + syrup + art', data=lattes)


se_val = se_factorial(formula='y ~ machine + syrup + art', data=lattes)
effects = pd.concat([
    pd.DataFrame({'name': ['Torani - Monin'],
                  'estimate': [dbar_oneway(formula='y ~ syrup', data=lattes)],
                  'se': [se_val]}),
    pd.DataFrame({'name': ['Heart - Foam'],
                  'estimate': [dbar_oneway(formula='y ~ art', data=lattes)],
                  'se': [se_val]}),
    pd.DataFrame({'name': ['Machine B - A'],
                  'estimate': [dbar_oneway(formula='y ~ machine', data=lattes)],
                  'se': [se_val]}),
    pd.DataFrame({'name': ['Machine * Art'],
                  'estimate': [dbar_twoway(formula='y ~ machine * art', data=lattes)],
                  'se': [se_val]}),
    pd.DataFrame({'name': ['Machine * Syrup'],
                  'estimate': [dbar_twoway(formula='y ~ machine * syrup', data=lattes)],
                  'se': [se_val]}),
    pd.DataFrame({'name': ['Syrup * Art'],
                  'estimate': [dbar_twoway(formula='y ~ syrup * art', data=lattes)],
                  'se': [se_val]}),
    pd.DataFrame({'name': ['Machine * Syrup * Art'],
                  'estimate': [dbar_threeway(formula='y ~ machine * syrup * art', data=lattes)],
                  'se': [se_val]})
], ignore_index=True)
effects['z'] = norm.ppf(0.975)
effects['upper'] = effects['estimate'] + effects['se'] * effects['z']
effects['lower'] = effects['estimate'] - effects['se'] * effects['z']

effects
gg = (ggplot() +
      geom_crossbar(data=effects,
                    mapping=aes(x='name', y='estimate', ymin='lower', ymax='upper',
                                fill='name')) +
      geom_hline(yintercept=0, linetype='dashed') +
      theme(legend_position='none') +
      coord_flip())

gg = (ggplot() +
      geom_crossbar(data=effects,
                    mapping=aes(x='name', y='estimate', ymin='lower', ymax='upper',
                                fill='estimate')) +
      geom_hline(yintercept=0, linetype='dashed') +
      theme(legend_position='none') +
      coord_flip() +
      scale_fill_gradient2(high='royalblue', low='salmon', mid='white', midpoint=0))

gg


# MULTIPLE LEVELS IN A FACTOR ####################################

# What if we want to test the effects of 3 or more levels in one factor?

lattes['milk'].unique()

lm(formula='y ~ milk', data=lattes)

from scipy.stats import f_oneway
milk_groups = [g['y'].values for _, g in lattes.groupby('milk')]
f_oneway(*milk_groups)









# Compare the ones that are oatmilk vs. not
lattes_oat = lattes.assign(oat=lambda df: df['milk'] == 'oat')
dbar_oneway(formula='y ~ oat', data=lattes_oat)

# Compare the ones that are skim vs. not
lattes_skim = lattes.assign(skim=lambda df: df['milk'] == 'skim')
dbar_oneway(formula='y ~ skim', data=lattes_skim)


# Compare the ones that are whole vs. not
lattes_whole = lattes.assign(whole=lambda df: df['milk'] == 'whole')
dbar_oneway(formula='y ~ whole', data=lattes_whole)





# Compare the ones that are oatmilk AND from machine B against all the ones that are NOT oatmilk and from machine A
dbar_twoway(formula='y ~ machine * oat', data=lattes_oat)





# interactions with lm() #############################


m = lm(formula='y ~ machine * art', data=lattes)
# Tastiness = 54 + -26 * (machine B?) + 15 * (heart?) - 8 * (machineB?)(heart?)
m.params

pd.DataFrame({
    'machine': ['b'],
    'art': ['heart'],
    'y': m.predict(pd.DataFrame({'machine': ['b'], 'art': ['heart']}))
})


pred = m.get_prediction(pd.DataFrame({'machine': ['b'], 'art': ['heart']}))
pd.DataFrame({'yhat': pred.predicted, 'se': pred.se})


from itertools import product
grid = pd.DataFrame(list(product(['a', 'b'], ['heart', 'foamy'])),
                    columns=['machine', 'art'])

pred = m.get_prediction(grid)
effects = grid.copy()
effects['fit'] = pred.predicted
effects['se'] = pred.se
effects['z'] = norm.ppf(0.975)
effects['upper'] = effects['fit'] + effects['se'] * effects['z']
effects['lower'] = effects['fit'] - effects['se'] * effects['z']

effects
