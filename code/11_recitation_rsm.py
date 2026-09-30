# 11_recitation_rsm.py
# Tim Fraser
# Recitation 11: Response Surface Methodology (in-class script, further reading)
# Chapter: Response Surface Methodology in Python

# It mirrors 11_recitation_rsm.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.

# Heads up: in R, one line under POLYNOMIALS is deliberately pseudo-code.
# Here it is commented out, so this script runs top to bottom.

import numpy as np                        # math (base R in R)
import pandas as pd                       # data wrangling (dplyr + readr + tidyr in R)
from plotnine import *                    # visuals (ggplot2 + viridis + metR in R)
from scipy import stats                   # qnorm() and qt() in R
import statsmodels.formula.api as smf     # lm() in R
from patsy import stateful_transform      # lets us build R's poly() for formulas


# Helpers: R's poly(), broom's glance() and tidy() ##############

# R's poly(x, 2) makes ORTHOGONAL polynomial columns (x and x^2, rescaled so
# they don't overlap). statsmodels formulas have no poly(), so we build one
# that gives the exact same numbers as R, and remembers the training data so
# that predict() on new data works just like R's predict().
class Poly:
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

poly = stateful_transform(Poly)

# glance() in R: one row of model-level statistics
# (R counts sigma as one more parameter in AIC and BIC, so we add it back
#  to statsmodels' m.aic and m.bic to get R's numbers.)
def glance(m):
    return pd.DataFrame({"r_squared": [m.rsquared], "adj_r_squared": [m.rsquared_adj],
                         "sigma": [np.sqrt(m.scale)], "statistic": [m.fvalue],
                         "p_value": [m.f_pvalue], "df": [m.df_model], "logLik": [m.llf],
                         "AIC": [m.aic + 2], "BIC": [m.bic + np.log(m.nobs)],
                         "df_residual": [m.df_resid], "nobs": [int(m.nobs)]})

# tidy() in R: one row per coefficient
def tidy(m):
    return pd.DataFrame({"term": m.params.index, "estimate": m.params.values,
                         "std_error": m.bse.values, "statistic": m.tvalues.values,
                         "p_value": m.pvalues.values})


## SETUP ---------------------------------

link = "workshops/gingerbread_test3.csv"
cookies = pd.read_csv(link)

print(cookies)

print(cookies.head())

cookies.info()   # glimpse() in R

print(cookies["batch"].nunique())

print(cookies["yum"].min(), cookies["yum"].max())   # range() in R

## MODEL 0 ---------------------------------

m0 = smf.ols("yum ~ molasses + ginger + cinnamon + butter + flour", data=cookies).fit()

print(m0.params)
# yum_predicted = 10.7652 + 5.4716 * molasses +
#  0.44 * ginger +
#  0.07 * cinnamon +
#  0.25 * butter +
# -0.32 * flour


print(glance(m0))



## POLYNOMIALS ---------------------------------

print(glance(smf.ols("yum ~ molasses + ginger + cinnamon + butter + flour", data=cookies).fit()))


# first order polynomial

# y = slope*x

# second order polynomial

# y = slope1 * x + slope2 * x^2


# two second order polynomials
# (pseudo-code from the board - slope1..slope4, x, and z are never defined,
#  so it stays a comment here)
# y = slope1*x + slope2*x**2 + slope3*z + slope4*z**2


print(np.corrcoef(cookies["yum"], cookies["cinnamon"])[0, 1])
print(np.corrcoef(cookies["yum"], cookies["molasses"])[0, 1])
print(np.corrcoef(cookies["yum"], cookies["butter"])[0, 1])
print(np.corrcoef(cookies["yum"], cookies["flour"])[0, 1])

print(smf.ols("yum ~ molasses", data=cookies).fit().params)

print(smf.ols("yum ~ poly(molasses, 2)", data=cookies).fit().params)
# y = 18.66 +
# 672.81 * molasses +
# 179.33 * molasses^2

print(glance(smf.ols("yum ~ poly(molasses, 2)", data=cookies).fit()))

m = smf.ols("yum ~ poly(molasses, 2) + poly(ginger, 2) + poly(cinnamon, 2) + "
            "poly(butter, 2) + poly(flour, 2)", data=cookies).fit()
print(cookies.head())
newdata = pd.DataFrame({
  "molasses": [0.75],
  "ginger": [1],
  "cinnamon": [1],
  "butter": [0.75],
  "flour": [2.75]})
print(newdata.assign(yhat=m.predict(newdata)))


m = smf.ols("yum ~ poly(molasses, 2) + poly(ginger, 2) + poly(cinnamon, 2) + "
            "poly(butter, 2) + poly(flour, 2) + I(molasses * cinnamon)", data=cookies).fit()


# Second order polynomial with interactions
print(glance(m))
# Interaction effects
# Polynomials (squares)





m = smf.ols("yum ~ poly(molasses, 2) + poly(ginger, 2) + I(molasses * ginger)",
            data=cookies).fit()
print(glance(m))


## PREDICTION ---------------------------------

### NEWDATA ------------------------

# expand_grid() in R; pd.MultiIndex.from_product() here
data = pd.MultiIndex.from_product(
  [np.round(np.arange(0, 3.01, 0.1), 1), np.round(np.arange(0, 3.01, 0.1), 1)],
  names=["molasses", "ginger"]).to_frame(index=False)
data["yhat"] = m.predict(data)

print(data)

### OPTIMIZING ------------------------

# Find max
print(data[data["yhat"] == data["yhat"].max()])

### ERROR ------------------------

# Make the grid...
newdata = pd.MultiIndex.from_product(
  [np.round(np.arange(0, 3.01, 0.1), 1), np.round(np.arange(0, 3.01, 0.1), 1)],
  names=["molasses", "ginger"]).to_frame(index=False)

# Extract a standard error for each prediction
# (predict(m, se.fit = TRUE) in R; get_prediction() in statsmodels)
p = m.get_prediction(newdata)
print(newdata.assign(fit=p.predicted_mean, se_fit=p.se_mean,
                     df=m.df_resid, residual_scale=np.sqrt(m.scale)))
# fit = yhat
# se_fit = standard error for that prediction

# Make a confidence interval for each prediction
ci = newdata.assign(fit=p.predicted_mean, se_fit=p.se_mean,
                    df=m.df_resid, residual_scale=np.sqrt(m.scale))
# Use a z-score from normal distribution to get 95% CIs
ci["lower"] = ci["fit"] - ci["se_fit"] * stats.norm.ppf(0.975)
ci["upper"] = ci["fit"] + ci["se_fit"] * stats.norm.ppf(0.975)
# Notice that you could use a t-score from t-distribution,
# but it's usually very very very very close to the z-score
ci["lower2"] = ci["fit"] - ci["se_fit"] * stats.t.ppf(0.975, df=ci["df"])
print(ci)

### TRANSFORMATIONS ----------------------------

# What if we add a transformation?
mlog = smf.ols("np.sqrt(yum) ~ poly(molasses, 2) + poly(ginger, 2) + I(molasses * ginger)",
               data=cookies).fit()
print(glance(mlog))

# Now, our predictions and se come back in logs!
# We must simulate, backtransform, and recompute confidence intervals
p = mlog.get_prediction(newdata)
print(newdata.assign(fit=p.predicted_mean, se_fit=p.se_mean))

rng = np.random.default_rng()
back = newdata.assign(fit=p.predicted_mean, se_fit=p.se_mean)
back["id"] = np.arange(1, len(back) + 1)
# Simulate, backtransform, and grab the standard deviation of that sampling distribution (se)
# (one row per prediction, 1000 simulated draws per row)
sims = rng.normal(loc=back["fit"].values[:, None], scale=back["se_fit"].values[:, None],
                  size=(len(back), 1000))
back["se"] = (sims**2).std(axis=1, ddof=1)
back["lower"] = back["fit"] - back["se"] * stats.norm.ppf(0.975)
back["upper"] = back["fit"] + back["se"] * stats.norm.ppf(0.975)
print(back)


## RSM HEATMAP ---------------------------------

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

# Contour bands of width 2, with one label per band (geom_text_contour() in R)
data["band2"] = np.floor(data["yhat"] / 2) * 2
labels = data.groupby("band2", as_index=False).apply(
  lambda d: d.iloc[[len(d) // 2]], include_groups=False).reset_index(drop=True)
labels["band2"] = np.floor(labels["yhat"] / 2) * 2

(ggplot() +
  geom_tile(data=data, mapping=aes(x="molasses", y="ginger", fill="band2")) +
  scale_fill_cmap("plasma") +
  geom_label(data=labels, mapping=aes(x="molasses", y="ginger", label="band2"),
             color="black", fill="white", size=8))







# EXAMPLES FROM PAST YEARS ##########################################

print(smf.ols("yum ~ molasses + ginger * cinnamon + butter + flour", data=cookies).fit().params)

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


print(tidy(smf.ols("yum ~ molasses + ginger + cinnamon + butter + flour", data=cookies).fit()))


print(tidy(smf.ols("yum ~ molasses + ginger + cinnamon + butter + flour", data=cookies).fit()))




# First order model - direct effects
print(smf.ols("yum ~ molasses + ginger", data=cookies).fit().params)



# Interaction model
print(smf.ols("yum ~ molasses * ginger", data=cookies).fit().params)

# First order interaction model
print(smf.ols("yum ~ molasses + ginger + I(molasses * ginger)", data=cookies).fit().params)






# Second order model
# (R's I(molasses^2) is I(molasses**2) in Python)
print(smf.ols("yum ~ molasses + I(molasses**2) + ginger + I(ginger**2)", data=cookies).fit().params)









# Second order interaction model (**Second order model**)
m1 = smf.ols("yum ~ molasses + I(molasses**2) + ginger + I(ginger**2) + "
             "I(molasses * ginger)", data=cookies).fit()

print(glance(m1))
print(m1.params)

# Built in function
# (R's rsm package draws contour(m1, ~molasses + ginger, image = TRUE).
#  Python has no rsm, so we predict over the observed range and tile it.)
quick = pd.MultiIndex.from_product(
  [np.linspace(cookies["molasses"].min(), cookies["molasses"].max(), 50),
   np.linspace(cookies["ginger"].min(), cookies["ginger"].max(), 50)],
  names=["molasses", "ginger"]).to_frame(index=False)
quick["yhat"] = m1.predict(quick)
(ggplot() +
  geom_tile(data=quick, mapping=aes(x="molasses", y="ginger", fill="yhat")) +
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
edges = np.arange(np.floor(grid["yhat"].min() / 10) * 10,
                  np.ceil(grid["yhat"].max() / 10) * 10 + 10, 10)
bins = (grid.assign(bin=pd.cut(grid["yhat"], bins=edges, include_lowest=True))
        .groupby("bin", observed=True, as_index=False)
        .agg(count=("yhat", "size")))
bins["total"] = bins["count"].sum()
bins["percent"] = bins["count"] / bins["total"]
print(bins)




(ggplot() +
  geom_point(data=mygrid, mapping=aes(x="molasses", y="ginger", color="yhat")))

(ggplot() +
  geom_tile(data=mygrid, mapping=aes(x="molasses", y="ginger", fill="yhat")))




# Second order interaction model (**Second order model**)
m1 = smf.ols("yum ~ molasses + I(molasses**2) + ginger + I(ginger**2) + "
             "I(molasses * ginger)", data=cookies).fit()


# Miniature example
mygrid = pd.MultiIndex.from_product(
  [np.arange(0, 3.01, 0.25), np.arange(0, 4.01, 0.25)],
  names=["molasses", "ginger"]).to_frame(index=False)
mygrid["yhat"] = m1.predict(mygrid)

# Contour bands of 5 yum points stand in for geom_contour_fill();
# one label per band stands in for geom_text_contour().
grid["band"] = np.floor(grid["yhat"] / 5) * 5
labels = grid.groupby("band", as_index=False).apply(
  lambda d: d.iloc[[len(d) // 2]], include_groups=False).reset_index(drop=True)
labels["band"] = np.floor(labels["yhat"] / 5) * 5

(ggplot() +
  geom_tile(data=grid, mapping=aes(x="ginger", y="molasses", fill="band"),
            color="white", size=0.1) +
  geom_label(data=labels, mapping=aes(x="ginger", y="molasses", label="band"),
             fill="white", size=8) +
  scale_fill_cmap("plasma"))


# Extended example
mygrid["band"] = np.floor(mygrid["yhat"] / 5) * 5
labels = mygrid.groupby("band", as_index=False).apply(
  lambda d: d.iloc[[len(d) // 2]], include_groups=False).reset_index(drop=True)
labels["band"] = np.floor(labels["yhat"] / 5) * 5

(ggplot() +
  # Real code
  geom_tile(data=mygrid, mapping=aes(x="molasses", y="ginger", fill="band"),
            color="white", size=0.75) +
  geom_label(data=labels, mapping=aes(x="molasses", y="ginger", label="band"),
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
m2 = smf.ols("yum ~ molasses + ginger + cinnamon + butter + flour + "
             "I(molasses**2) + I(ginger**2) + I(cinnamon**2) + "
             "I(butter**2) + I(flour**2) + "
             "molasses * ginger * cinnamon * butter * flour", data=cookies).fit()

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
