# 11_recitation_rsm.py
# Tim Fraser
# Recitation 11: Response Surface Methodology (in-class script, further reading)
# Chapter: Response Surface Methodology in Python

# Heads up: the "y = slope1*x + ..." line is deliberately pseudo-code,
# not runnable. Run this script chunk by chunk rather than all at once.

## SETUP ---------------------------------

import pandas as pd
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt
from itertools import product
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_models import lm, tidy, glance

link = "workshops/gingerbread_test3.csv"
cookies = pd.read_csv(link)

cookies

cookies.head()

cookies.info()

cookies['batch'].nunique()

cookies['yum'].min(), cookies['yum'].max()

## MODEL 0 ---------------------------------

m0 = lm(formula='yum ~ molasses + ginger + cinnamon + butter + flour',
        data=cookies)

m0.params
# yum_predicted = 10.7652 + 5.4716 * molasses +
#  0.44 * ginger +
#  0.07 * cinnamon +
#  0.25 * butter +
# -0.32 * flour


glance(m0)



## POLYNOMIALS ---------------------------------

glance(lm(formula='yum ~ molasses + ginger + cinnamon + butter + flour',
          data=cookies))


# first order polynomial

# y = slope*x

# second order polynomial

# y = slope1 * x + slope2 * x^2


# two second order polynomials
# y = slope1*x + slope2*x**2 + slope3*z + slope4*z**2


np.corrcoef(cookies['yum'], cookies['cinnamon'])[0, 1]
np.corrcoef(cookies['yum'], cookies['molasses'])[0, 1]
np.corrcoef(cookies['yum'], cookies['butter'])[0, 1]
np.corrcoef(cookies['yum'], cookies['flour'])[0, 1]

lm(formula='yum ~ molasses', data=cookies)

lm(formula='yum ~ molasses + I(molasses**2)', data=cookies)
# y = 18.66 +
# 672.81 * molasses +
# 179.33 * molasses^2

# Second order interaction model (**Second order model**)
m1 = lm(formula='yum ~ molasses * ginger + I(molasses**2) + I(ginger**2)',
        data=cookies)

glance(m1)
m1.params

# As molasses increases, yum increases!!!!

# As ginger increases, yum increases!!

# The effect of an increase in molasses is bigger than
# the effect of an increase in ginger

# the effect of ginger on yum
# DEPENDS on the level of molasses
# AN INTERACTION

mygrid = pd.DataFrame(list(product(np.arange(0, 3.25, 0.25),
                                   np.arange(0, 4.25, 0.25))),
                      columns=['molasses', 'ginger'])
mygrid = mygrid.assign(yhat=m1.predict(mygrid))

grid = pd.DataFrame(list(product(np.arange(0, 3.1, 0.1),
                                 np.arange(0, 3.1, 0.1))),
                    columns=['molasses', 'ginger'])
grid = grid.assign(yhat=m1.predict(grid))


cookies['molasses'].min(), cookies['molasses'].max()
cookies['ginger'].min(), cookies['ginger'].max()

# Quantity of interest: optimal predictors
grid[grid['yhat'] == grid['yhat'].max()]


(ggplot() +
    geom_point(data=mygrid,
               mapping=aes(x='molasses', y='ginger', color='yhat')))

(ggplot() +
    geom_tile(data=mygrid,
              mapping=aes(x='molasses', y='ginger', fill='yhat')) +
    scale_fill_cmap(cmap_name='plasma'))


# matplotlib contour (Python tutorial) — labeled ridges, plasma colormap
molasses_unique = sorted(grid['molasses'].unique())
ginger_unique = sorted(grid['ginger'].unique())
M, G = np.meshgrid(molasses_unique, ginger_unique)
yhat_grid = grid.pivot_table(values='yhat', index='ginger', columns='molasses',
                             aggfunc='mean').values
fig, ax = plt.subplots(figsize=(8, 6))
cf = ax.contourf(M, G, yhat_grid, levels=15, cmap='plasma', alpha=0.8)
cl = ax.contour(M, G, yhat_grid, levels=10, colors='white', linewidths=0.8)
ax.clabel(cl, inline=True, fontsize=8, fmt='%1.1f')
ax.set_xlabel('Molasses (cups)')
ax.set_ylabel('Ginger (tablespoons)')
ax.set_title('Hey come look at my cool contour plot!')
plt.colorbar(cf, ax=ax, label='Predicted\nYum\nFactor')
plt.close(fig)


# Extended second-order model with all five ingredients
m2 = lm(formula='yum ~ molasses * ginger * cinnamon * butter * flour + I(molasses**2) + I(ginger**2) + I(cinnamon**2) + I(butter**2) + I(flour**2)',
        data=cookies)

glance(m2)

tidy(m2)



from itertools import product as prod
mygrid = pd.DataFrame(
    [{'molasses': mol, 'ginger': gin, 'cinnamon': cin, 'butter': 1, 'flour': 1}
     for mol, gin, cin in prod(np.arange(0, 5.5, 0.5),
                               np.arange(0, 4.5, 0.5),
                               [0, 1, 2])]
)
mygrid = mygrid.assign(yhat=m2.predict(mygrid))


(ggplot() +
    geom_tile(data=mygrid,
              mapping=aes(x='molasses', y='ginger', fill='yhat')) +
    facet_wrap('~cinnamon') +
    scale_fill_cmap(cmap_name='plasma') +
    labs(x='Molasses (cups)',
         y='Ginger (tablespoons)',
         title='Hey come look at my cool contour plot!',
         fill='Predicted\nYum\nFactor') +
    theme_classic(base_size=14))
