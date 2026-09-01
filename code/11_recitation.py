# 11_recitation.py
# Tim Fraser
# Recitation 11: Response Surface Methodology
# Chapter: Response Surface Methodology in Python

# Workshop code paired with the textbook chapter
# "Response Surface Methodology in Python" at timothyfraser.com/sigma.

# What this script does:
# Uses the gingerbread cookie experiment to move from a plain first order
# model up to a second order (polynomial) model with interactions, then
# predicts over a grid of ingredient values and draws the response surface
# as a contour plot to find the mix that maximizes the 'yum' score.

# Inputs: workshops/gingerbread_test3.csv
#         (the gingerbread cookie experiment, read from the repo).
# Packages: pandas, numpy, plotnine, matplotlib, functions_models

# Heads up: the "y = slope1*x + ..." line is deliberately pseudo-code,
# not runnable. Run this script chunk by chunk rather than all at once.

import pandas as pd
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt
from itertools import product
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_models import lm, tidy, glance

# 1. Load the cookie data ######################################

link = "workshops/gingerbread_test3.csv"
cookies = pd.read_csv(link)

cookies

cookies.head()

cookies.info()

cookies['batch'].nunique()

cookies['yum'].min(), cookies['yum'].max()

# 2. First order model #########################################

# Every ingredient gets one straight-line slope.
m0 = lm(formula='yum ~ molasses + ginger + cinnamon + butter + flour',
        data=cookies)

m0.params
# yum_predicted = 10.7652 + 5.4716 * molasses +
#  0.44 * ginger +
#  0.07 * cinnamon +
#  0.25 * butter +
# -0.32 * flour


glance(m0)



glance(lm(formula='yum ~ molasses + ginger + cinnamon + butter + flour',
          data=cookies))


# 3. Why go to second order? ###################################

# first order polynomial

# y = slope*x

# second order polynomial

# y = slope1 * x + slope2 * x^2


# two second order polynomials
# NOTE: the next line is pseudo-code written on the board, not runnable.
# slope1..slope4, x, and z are never defined - skip it when running.
# y = slope1*x + slope2*x**2 + slope3*z + slope4*z**2


# 4. Correlations, and one predictor at a time #################

# I(x**2) adds the square; R's poly(x, 2) does x and x^2 in one go.
# The Python tutorial uses I(molasses**2) in the formula (patsy).
np.corrcoef(cookies['yum'], cookies['cinnamon'])[0, 1]
np.corrcoef(cookies['yum'], cookies['molasses'])[0, 1]
np.corrcoef(cookies['yum'], cookies['butter'])[0, 1]
np.corrcoef(cookies['yum'], cookies['flour'])[0, 1]

lm(formula='yum ~ molasses', data=cookies)

lm(formula='yum ~ molasses + I(molasses**2)', data=cookies)
# y = 18.66 +
# 672.81 * molasses +
# 179.33 * molasses^2

glance(lm(formula='yum ~ molasses + I(molasses**2)', data=cookies))

# 5. Full second order model, and predicting from it ###########

m = lm(formula='yum ~ I(molasses**2) + molasses + I(ginger**2) + ginger + I(cinnamon**2) + cinnamon + I(butter**2) + butter + I(flour**2) + flour',
       data=cookies)
cookies.head()
new = pd.DataFrame({
    'molasses': [0.75],
    'ginger': [1],
    'cinnamon': [1],
    'butter': [0.75],
    'flour': [2.75]
})
new = new.assign(yhat=m.predict(new))
new


# 6. Adding an interaction term ################################

# I(molasses * cinnamon) says the effect of molasses depends on cinnamon.
m = lm(formula='yum ~ molasses + I(molasses**2) + ginger + I(ginger**2) + cinnamon + I(cinnamon**2) + butter + I(butter**2) + flour + I(flour**2) + I(molasses * cinnamon)',
       data=cookies)


# Second order polynomial with interactions
glance(m)
# Interaction effects
# Polynomials (squares)





m = lm(formula='yum ~ molasses * ginger + I(molasses**2) + I(ginger**2)',
       data=cookies)
glance(m)


# 7. Predict across a grid of ingredient values ################

# product() makes every combination of molasses and ginger;
# m.predict() gives the model's yum score at each one.
molasses_seq = np.arange(0, 3.1, 0.1)
ginger_seq = np.arange(0, 3.1, 0.1)
data = pd.DataFrame(list(product(molasses_seq, ginger_seq)),
                    columns=['molasses', 'ginger'])
data = data.assign(yhat=m.predict(data))

data


data[data['yhat'] == data['yhat'].max()]



# 8. Draw the response surface #################################

# geom_tile() paints the predicted surface; the Python tutorial uses
# matplotlib contourf / contour for labeled ridges (R's metR / viridis).
# plotnine 0.15 has no geom_contour — use matplotlib below for the contour overlay.
g = (ggplot() +
     geom_tile(data=data, mapping=aes(x='molasses', y='ginger', fill='yhat')) +
     scale_fill_cmap(cmap_name='plasma'))
g


# matplotlib twin of geom_contour_fill + geom_text_contour
molasses_unique = sorted(data['molasses'].unique())
ginger_unique = sorted(data['ginger'].unique())
M, G = np.meshgrid(molasses_unique, ginger_unique)
yhat_grid = data.pivot_table(values='yhat', index='ginger', columns='molasses',
                             aggfunc='mean').values
fig, ax = plt.subplots(figsize=(8, 6))
cf = ax.contourf(M, G, yhat_grid, levels=15, cmap='plasma', alpha=0.8)
cl = ax.contour(M, G, yhat_grid, levels=10, colors='white', linewidths=0.8)
ax.clabel(cl, inline=True, fontsize=8, fmt='%1.1f')
ax.set_xlabel('Molasses (cups)')
ax.set_ylabel('Ginger (tablespoons)')
plt.colorbar(cf, ax=ax, label='Predicted yum')
# plt.show()
plt.close(fig)



# EXAMPLES FROM PAST YEARS ##########################################

lm(formula='yum ~ molasses + ginger * cinnamon + butter + flour', data=cookies)

# First order model - direct effects
lm(formula='yum ~ molasses + ginger', data=cookies)

# Interaction model
lm(formula='yum ~ molasses * ginger', data=cookies)

# Second order interaction model (**Second order model**)
m1 = lm(formula='yum ~ molasses * ginger + I(molasses**2) + I(ginger**2)',
        data=cookies)

glance(m1)
m1.params

mygrid = pd.DataFrame(list(product(np.arange(0, 3.25, 0.25),
                                   np.arange(0, 4.25, 0.25))),
                      columns=['molasses', 'ginger'])
mygrid = mygrid.assign(yhat=m1.predict(mygrid))

(ggplot() +
    geom_tile(data=mygrid, mapping=aes(x='molasses', y='ginger', fill='yhat')) +
    scale_fill_cmap(cmap_name='plasma'))


# Quantity of interest: optimal predictors
mygrid[mygrid['yhat'] == mygrid['yhat'].max()]
