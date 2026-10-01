# 11_recitation.py
# Tim Fraser
# Recitation 11: Response Surface Methodology
# Chapter: Response Surface Methodology in Python

# Workshop code paired with the textbook chapter
# "Response Surface Methodology" at timothyfraser.com/sigma.

# It mirrors 11_recitation.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.

# What this script does:
# Uses the gingerbread cookie experiment to move from a plain first order
# model up to a second order (polynomial) model with interactions, then
# predicts over a grid of ingredient values and draws the response surface
# as a contour plot to find the mix that maximizes the 'yum' score.

# Inputs: workshops/gingerbread_test3.csv
#         (the gingerbread cookie experiment, read from the repo).
# Packages: numpy, pandas, plotnine, statsmodels, patsy
#           (+ the course helpers in functions/functions_models.py)

# Heads up: in R, one line in section 3 is deliberately pseudo-code.
# Here it is commented out, so this script runs top to bottom.

import sys
import numpy as np                        # math (base R in R)
import pandas as pd                       # data wrangling (dplyr + readr + tidyr in R)
from plotnine import *                    # visuals (ggplot2 + viridis + metR in R)
from patsy import stateful_transform      # lets us build R's poly() for formulas
sys.path.append("functions")
from functions_models import lm, tidy, glance  # lm(), plus tidy() and glance() from broom in R


# R's poly(x, 2) makes ORTHOGONAL polynomial columns (x and x^2, rescaled so
# they don't overlap). statsmodels formulas have no poly(), so we build one
# that gives the exact same numbers as R, and remembers the training data so
# that predict() on new data works just like R's predict().
@stateful_transform
class poly:
    def __init__(self):
        self.x = []

    def memorize_chunk(self, x, degree=2):
        self.x.append(np.asarray(x, dtype=float))
        self.degree = degree

    def memorize_finish(self):
        x = np.concatenate(self.x)
        self.alpha, self.norm2 = [x.mean()], [1.0, float(len(x))]
        z_prev, z = np.ones_like(x), x - x.mean()
        for i in range(1, self.degree + 1):
            self.norm2.append(np.sum(z**2))
            a = np.sum(x * z**2) / self.norm2[-1]
            self.alpha.append(a)
            z_prev, z = z, (x - a) * z - (self.norm2[-1] / self.norm2[-2]) * z_prev

    def transform(self, x, degree=2):
        x = np.asarray(x, dtype=float)
        z = [np.ones_like(x), x - self.alpha[0]]
        for i in range(1, degree):
            z.append((x - self.alpha[i]) * z[i] - (self.norm2[i + 1] / self.norm2[i]) * z[i - 1])
        return np.column_stack([z[j] / np.sqrt(self.norm2[j + 1]) for j in range(1, degree + 1)])


# 1. Load the cookie data ######################################

link = "workshops/gingerbread_test3.csv"
cookies = pd.read_csv(link)

print(cookies)

print(cookies.head())

cookies.info()   # glimpse() in R

print(cookies["batch"].nunique())

print(cookies["yum"].min(), cookies["yum"].max())   # range() in R

# 2. First order model #########################################

# Every ingredient gets one straight-line slope.
m0 = lm("yum ~ molasses + ginger + cinnamon + butter + flour", data=cookies)

print(m0.params)
# yum_predicted = 10.7652 + 5.4716 * molasses +
#  0.44 * ginger +
#  0.07 * cinnamon +
#  0.25 * butter +
# -0.32 * flour


print(glance(m0))



print(glance(lm("yum ~ molasses + ginger + cinnamon + butter + flour", data=cookies)))


# 3. Why go to second order? ###################################

# first order polynomial

# y = slope*x

# second order polynomial

# y = slope1 * x + slope2 * x^2


# two second order polynomials
# NOTE: the next line is pseudo-code written on the board, not runnable Python.
# slope1..slope4, x, and z are never defined - so it stays a comment here.
# y = slope1*x + slope2*x**2 + slope3*z + slope4*z**2


# 4. Correlations, and one predictor at a time #################

# poly(x, 2) adds both x and x^2 to the model in one go.
print(np.corrcoef(cookies["yum"], cookies["cinnamon"])[0, 1])
print(np.corrcoef(cookies["yum"], cookies["molasses"])[0, 1])
print(np.corrcoef(cookies["yum"], cookies["butter"])[0, 1])
print(np.corrcoef(cookies["yum"], cookies["flour"])[0, 1])

print(lm("yum ~ molasses", data=cookies).params)

print(lm("yum ~ poly(molasses, 2)", data=cookies).params)
# y = 18.66 +
# 672.81 * molasses +
# 179.33 * molasses^2

print(glance(lm("yum ~ poly(molasses, 2)", data=cookies)))

# 5. Full second order model, and predicting from it ###########

m = lm("yum ~ poly(molasses, 2) + poly(ginger, 2) + poly(cinnamon, 2) + "
       "poly(butter, 2) + poly(flour, 2)", data=cookies)
print(cookies.head())
print(pd.DataFrame({
  "molasses": [0.75],
  "ginger": [1],
  "cinnamon": [1],
  "butter": [0.75],
  "flour": [2.75]
}).assign(yhat=lambda d: m.predict(d)))


# 6. Adding an interaction term ################################

# I(molasses * cinnamon) says the effect of molasses depends on cinnamon.
m = lm("yum ~ poly(molasses, 2) + poly(ginger, 2) + poly(cinnamon, 2) + "
       "poly(butter, 2) + poly(flour, 2) + I(molasses * cinnamon)", data=cookies)


# Second order polynomial with interactions
print(glance(m))
# Interaction effects
# Polynomials (squares)





m = lm("yum ~ poly(molasses, 2) + poly(ginger, 2) + I(molasses * ginger)",
       data=cookies)
print(glance(m))


# 7. Predict across a grid of ingredient values ################

# expand_grid() in R makes every combination of molasses and ginger;
# here pd.MultiIndex.from_product() does the same.
# predict() gives the model's yum score at each one.
data = pd.MultiIndex.from_product(
  [np.round(np.arange(0, 3.01, 0.1), 1), np.round(np.arange(0, 3.01, 0.1), 1)],
  names=["molasses", "ginger"]).to_frame(index=False)
data["yhat"] = m.predict(data)

print(data)


print(data[data["yhat"] == data["yhat"].max()])


# 8. Draw the response surface #################################

# geom_tile() paints the predicted surface; contours label the ridges.
# plotnine has no geom_contour() (or metR's geom_contour_fill()), so we
# cut yhat into bands of 1 or 2 yum points and fill the tiles by band -
# each colour edge is a contour line.
data["band1"] = np.floor(data["yhat"] / 1) * 1

(ggplot() +
  geom_tile(data=data, mapping=aes(x="molasses", y="ginger", fill="yhat")) +
  scale_fill_cmap("plasma"))

# Contour bands of width 1 (geom_contour_fill(binwidth = 1) in R)
(ggplot() +
  geom_tile(data=data, mapping=aes(x="molasses", y="ginger", fill="band1")) +
  scale_fill_cmap("plasma"))

# Contour bands of width 2, with one label per band (geom_text_contour() in R);
# each label sits on one tile picked from inside its band.
data["band2"] = np.floor(data["yhat"] / 2) * 2

(ggplot() +
  geom_tile(data=data, mapping=aes(x="molasses", y="ginger", fill="band2")) +
  scale_fill_cmap("plasma") +
  geom_label(data=data.groupby("band2").sample(n=1, random_state=1),
             mapping=aes(x="molasses", y="ginger", label="band2"),
             color="black", fill="white", size=8))







# EXAMPLES FROM PAST YEARS ##########################################

print(lm("yum ~ molasses + ginger * cinnamon + butter + flour", data=cookies).params)

# ginger = +0.63402
# cinnamon = +0.42118
# ginger:cinnamon = -0.15599
# As both increase by 1, we expect XXXX less of the outcome.

print(10.32645 + 5.47159 * 0 +
  0*0.25065 + -0.31940*0 +
  # effect of ginger
  0.63402 * 1 +
  # Effect of cinnamon
  0.42118 * 2 +
  # Effect of both
  -0.15599 * (1 * 2))



# yum_predicted = 10.3264 +
#  5.47 * molasses +
#  0.63 * ginger +
#  0.42 * cinnamon +
#  0.25 * butter +
# -0.32 * flour +
# -0.156 * ginger * cinnamon


print(tidy(lm("yum ~ molasses + ginger + cinnamon + butter + flour", data=cookies)))


print(tidy(lm("yum ~ molasses + ginger + cinnamon + butter + flour", data=cookies)))




# First order model - direct effects
print(lm("yum ~ molasses + ginger", data=cookies).params)



# Interaction model
print(lm("yum ~ molasses * ginger", data=cookies).params)

# First order interaction model
print(lm("yum ~ molasses + ginger + I(molasses * ginger)", data=cookies).params)






# Second order model
# (R's I(molasses^2) is I(molasses**2) in Python)
print(lm("yum ~ molasses + I(molasses**2) + ginger + I(ginger**2)", data=cookies).params)









# Second order interaction model (**Second order model**)
m1 = lm("yum ~ molasses + I(molasses**2) + ginger + I(ginger**2) + "
        "I(molasses * ginger)", data=cookies)

print(glance(m1))
print(m1.params)

# Built in function
# (R's rsm package draws contour(m1, ~molasses + ginger, image = TRUE).
#  Python has no rsm, so we predict over the observed range and tile it.)
(ggplot(pd.MultiIndex.from_product(
    [np.linspace(cookies["molasses"].min(), cookies["molasses"].max(), 50),
     np.linspace(cookies["ginger"].min(), cookies["ginger"].max(), 50)],
    names=["molasses", "ginger"]).to_frame(index=False).assign(yhat=lambda d: m1.predict(d))) +
  geom_tile(mapping=aes(x="molasses", y="ginger", fill="yhat")) +
  scale_fill_cmap("plasma"))






# As molasses increases, yum increases!!!!

# As ginger increases, yum increases!!

# The effect of an increase in molasses is bigger than
# the effect of an increase in ginger

# the effect of ginger on yum
# DEPENDS on the level of molasses
# AN INTERACTION

# As molasses AND ginger increase, yum increases
print(m1.params)



mygrid = pd.MultiIndex.from_product(
  [np.arange(0, 3.01, 0.25), np.arange(0, 4.01, 0.25)],
  names=["molasses", "ginger"]).to_frame(index=False)
mygrid["yhat"] = m1.predict(mygrid)


# expand_grid (tidyr in R; pd.MultiIndex.from_product() here)

grid = pd.MultiIndex.from_product(
  [np.round(np.arange(0, 3.01, 0.1), 1), np.round(np.arange(0, 3.01, 0.1), 1)],
  names=["molasses", "ginger"]).to_frame(index=False)
grid["yhat"] = m1.predict(grid)


print(cookies["molasses"].min(), cookies["molasses"].max())
print(cookies["ginger"].min(), cookies["ginger"].max())

# Quantity of interest: optimal predictors
print(grid[grid["yhat"] == grid["yhat"].max()])


# cut_interval(yhat, length = 10) in R: bins 10 yum points wide
print(grid
  .assign(bin=lambda d: pd.cut(d["yhat"], include_lowest=True, bins=np.arange(
    np.floor(d["yhat"].min() / 10) * 10, np.ceil(d["yhat"].max() / 10) * 10 + 10, 10)))
  .groupby("bin", observed=True, as_index=False)
  .agg(count=("yhat", "size"))
  .assign(total=lambda d: d["count"].sum(),
          percent=lambda d: d["count"] / d["total"]))




(ggplot() +
  geom_point(data=mygrid, mapping=aes(x="molasses", y="ginger", color="yhat")))

(ggplot() +
  geom_tile(data=mygrid, mapping=aes(x="molasses", y="ginger", fill="yhat")))




# Second order interaction model (**Second order model**)
m1 = lm("yum ~ molasses + I(molasses**2) + ginger + I(ginger**2) + "
        "I(molasses * ginger)", data=cookies)


# Miniature example
mygrid = pd.MultiIndex.from_product(
  [np.arange(0, 3.01, 0.25), np.arange(0, 4.01, 0.25)],
  names=["molasses", "ginger"]).to_frame(index=False)
mygrid["yhat"] = m1.predict(mygrid)

# Contour bands of 5 yum points stand in for geom_contour_fill();
# one label per band stands in for geom_text_contour().
grid["band"] = np.floor(grid["yhat"] / 5) * 5

(ggplot() +
  geom_tile(data=grid, mapping=aes(x="ginger", y="molasses", fill="band"),
            color="white", size=0.1) +
  geom_label(data=grid.groupby("band").sample(n=1, random_state=1),
             mapping=aes(x="ginger", y="molasses", label="band"),
             fill="white", size=8) +
  scale_fill_cmap("plasma"))


# Extended example
mygrid["band"] = np.floor(mygrid["yhat"] / 5) * 5

(ggplot() +
  # Real code
  geom_tile(data=mygrid, mapping=aes(x="molasses", y="ginger", fill="band"),
            color="white", size=0.75) +
  geom_label(data=mygrid.groupby("band").sample(n=1, random_state=1),
             mapping=aes(x="molasses", y="ginger", label="band"),
             fill="white", size=8) +
  # fluff
  scale_fill_cmap("plasma") +
  labs(x="Molasses (cups)",
       y="Ginger (tablespoons)",
       title="Hey come look at my cool contour plot!",
       subtitle="No really, look at my cool contour plot!",
       caption="By the way, hello",
       fill="Predicted\nYum\nFactor") +
  theme_classic(base_size=14) +
  theme(axis_line=element_blank()))




# Second order interaction model (**Second order model**)
m2 = lm("yum ~ molasses + ginger + cinnamon + butter + flour + "
        "I(molasses**2) + I(ginger**2) + I(cinnamon**2) + "
        "I(butter**2) + I(flour**2) + "
        "molasses * ginger * cinnamon * butter * flour", data=cookies)

print(glance(m2))

print(tidy(m2))



mygrid = pd.MultiIndex.from_product(
  [np.arange(0, 5.01, 0.5), np.arange(0, 4.01, 0.5), [0, 1, 2], [1], [1]],
  names=["molasses", "ginger", "cinnamon", "butter", "flour"]).to_frame(index=False)
mygrid["yhat"] = m2.predict(mygrid)
mygrid["band"] = np.floor(mygrid["yhat"] / 5) * 5


(ggplot() +
  # Real code
  geom_tile(data=mygrid, mapping=aes(x="molasses", y="ginger", fill="band"),
            color="white", size=0.75) +

  facet_wrap("~cinnamon") +

  # fluff
  scale_fill_cmap("plasma") +
  labs(x="Molasses (cups)",
       y="Ginger (tablespoons)",
       title="Hey come look at my cool contour plot!",
       subtitle="No really, look at my cool contour plot!",
       caption="By the way, hello",
       fill="Predicted\nYum\nFactor") +
  theme_classic(base_size=14) +
  theme(axis_line=element_blank()))
