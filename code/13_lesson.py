# 13_lesson.py
# Tim Fraser
# Lesson 13: Factorial Design
# Chapter: Factorial Design and Interaction Effects in Python

# Example 1 #################################################

import pandas as pd
import numpy as np
from itertools import product

# Get full factorial grid of combinations
grid = pd.DataFrame(list(product(
    ['A', 'B'],   # Catalyst K
    [20, 40],     # Concentration C
    [160, 180]    # Temperature t
)), columns=['k', 'c', 't'])
# order columns as shown in the example...
grid.insert(0, 'run', range(1, len(grid) + 1))
grid = grid[['run', 't', 'c', 'k']]

# We run the experiment once and get these results
data = grid.copy()
data['y'] = [60, 72, 54, 68, 52, 83, 45, 80]

data


# Example 2 ##########################################

# Calculate the direct (one-way) treatment effects
pd.DataFrame({
    'dbar_c': [(data.loc[data['c'] == 40, 'y'].values -
                data.loc[data['c'] == 20, 'y'].values).mean()],
    'dbar_t': [(data.loc[data['t'] == 180, 'y'].values -
                data.loc[data['t'] == 160, 'y'].values).mean()],
    'dbar_k': [(data.loc[data['k'] == 'B', 'y'].values -
                data.loc[data['k'] == 'A', 'y'].values).mean()]
})



# Example 3 ##########################################

# Calculate the two-way treatment effects
x1 = data.loc[((data['t'] == 180) & (data['k'] == 'B')) |
              ((data['t'] == 160) & (data['k'] == 'A')), 'y']
x0 = data.loc[((data['t'] == 160) & (data['k'] == 'B')) |
              ((data['t'] == 180) & (data['k'] == 'A')), 'y']
pd.DataFrame({
    'xbar1': [x1.mean()],
    'xbar0': [x0.mean()],
    'dbar': [x1.mean() - x0.mean()]
})

# Let's get a clearer glimpse at that first stage, before we take the means
pd.DataFrame({'x1': x1.values, 'x0': x0.values})

# Even narrower...
pd.DataFrame({
    'x1a': data.loc[(data['t'] == 160) & (data['k'] == 'A'), 'y'].values,
    'x1b': data.loc[(data['t'] == 180) & (data['k'] == 'B'), 'y'].values,
    'x0a': data.loc[(data['t'] == 180) & (data['k'] == 'A'), 'y'].values,
    'x0b': data.loc[(data['t'] == 160) & (data['k'] == 'B'), 'y'].values
})


# Example 4 ######################################################

# Three Way Treatment Effects

# Get treatment effect for TCK...

# Get the TC interaction when K is A
d1 = (data.loc[(data['t'] == 180) & (data['k'] == 'A') & (data['c'] == 40), 'y'].values -
      data.loc[(data['t'] == 160) & (data['k'] == 'A') & (data['c'] == 40), 'y'].values)
d0 = (data.loc[(data['t'] == 180) & (data['k'] == 'A') & (data['c'] == 20), 'y'].values -
      data.loc[(data['t'] == 160) & (data['k'] == 'A') & (data['c'] == 20), 'y'].values)
pd.DataFrame({'d1': d1, 'd0': d0, 'dbar': (d1 - d0) / 2})

# Get the TC interaction when K is B
d1 = (data.loc[(data['t'] == 180) & (data['k'] == 'B') & (data['c'] == 40), 'y'].values -
      data.loc[(data['t'] == 160) & (data['k'] == 'B') & (data['c'] == 40), 'y'].values)
d0 = (data.loc[(data['t'] == 180) & (data['k'] == 'B') & (data['c'] == 20), 'y'].values -
      data.loc[(data['t'] == 160) & (data['k'] == 'B') & (data['c'] == 20), 'y'].values)
pd.DataFrame({'d1': d1, 'd0': d0, 'dbar': (d1 - d0) / 2})

# Now get the average difference between these interactions
d1a = (data.loc[(data['t'] == 180) & (data['k'] == 'A') & (data['c'] == 40), 'y'].values -
       data.loc[(data['t'] == 160) & (data['k'] == 'A') & (data['c'] == 40), 'y'].values)
d0a = (data.loc[(data['t'] == 180) & (data['k'] == 'A') & (data['c'] == 20), 'y'].values -
       data.loc[(data['t'] == 160) & (data['k'] == 'A') & (data['c'] == 20), 'y'].values)
dbar_a = (d1a - d0a) / 2

d1b = (data.loc[(data['t'] == 180) & (data['k'] == 'B') & (data['c'] == 40), 'y'].values -
       data.loc[(data['t'] == 160) & (data['k'] == 'B') & (data['c'] == 40), 'y'].values)
d0b = (data.loc[(data['t'] == 180) & (data['k'] == 'B') & (data['c'] == 20), 'y'].values -
       data.loc[(data['t'] == 160) & (data['k'] == 'B') & (data['c'] == 20), 'y'].values)
dbar_b = (d1b - d0b) / 2

pd.DataFrame({
    'dbar_a': dbar_a,
    'dbar_b': dbar_b,
    'dbar': (dbar_b - dbar_a) / 2
})



# Example 5 #################################

# We run the experiment twice and get these results
data2 = pd.concat([
    grid.assign(rep=1, y=[59, 74, 50, 69, 50, 81, 46, 79]),
    grid.assign(rep=2, y=[61, 70, 58, 67, 54, 85, 44, 81])
], ignore_index=True)


# Let's construct our table
# Differences of replicate runs
(data2.groupby(['run', 't', 'c', 'k'], as_index=False)
 .agg(d=('y', lambda s: s.diff().iloc[-1])))

# Variance across replicate runs for each set of conditions
(data2.groupby(['run', 't', 'c', 'k'], as_index=False)
 .agg(var=('y', 'var'), v=('y', lambda s: len(s) - 1)))

# Get pooled standard deviation
per_run = (data2.groupby(['run', 't', 'c', 'k'], as_index=False)
           .agg(var=('y', 'var'), v=('y', lambda s: len(s) - 1)))
vp = per_run['var'].sum() / per_run['v'].sum()
n_diff = len(per_run)
sv = (1 / n_diff + 1 / n_diff) * vp
se = np.sqrt(sv)
stat = pd.DataFrame({'vp': [vp], 'n_diff': [n_diff], 'sv': [sv], 'se': [se]})

stat
