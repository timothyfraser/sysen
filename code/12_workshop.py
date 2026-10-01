# 12_workshop.py
# Tim Fraser
# Workshop 12: t-tests, F-tests, permutation tests, and ANOVA
# Chapter: Comparing Groups in Python

# It mirrors 12_workshop.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.

import numpy as np                        # math (base R in R)
import pandas as pd                       # data wrangling (dplyr in R)
from plotnine import *                    # visuals (ggplot2 in R)
from scipy import stats                   # t.test(), var.test(), bartlett.test() in R


# Unpaired t-tests ###############################################

data = pd.DataFrame({
  "method": ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A",
             "B", "B", "B", "B", "B", "B", "B", "B", "B", "B"],
  "yield": [89.7, 81.4, 84.5, 84.8, 87.3, 79.7, 85.1, 81.7, 83.7, 84.5,
            84.7, 86.1, 83.2, 91.9, 86.3, 79.3, 82.6, 89.1, 83.7, 88.5]})

# T-test assuming equal variance (unpaired)
# (yield ~ method in R: method A's yields vs method B's. R prints the 95%
#  confidence interval with the test; the lambda names the result res just
#  long enough to print it with res.confidence_interval(), the same way.)
(lambda res: print(res, res.confidence_interval(0.95)))(stats.ttest_ind(
  data["yield"][data["method"] == "A"], data["yield"][data["method"] == "B"], equal_var=True))


# T-test not assuming equal variance
(lambda res: print(res, res.confidence_interval(0.95)))(stats.ttest_ind(
  data["yield"][data["method"] == "A"], data["yield"][data["method"] == "B"], equal_var=False))


# Variance F-tests ################################

# How different are the variances?
print(data.groupby("method", as_index=False).agg(var=("yield", "var")))

# Is that difference significant?
# F test to compare two variances. (var.test() in R; scipy has no one-liner,
# so we build it: F = var(A) / var(B), on (nA - 1, nB - 1) degrees of freedom.)
print(data.pipe(lambda d: pd.DataFrame({
    "statistic": [d["yield"][d["method"] == "A"].var() / d["yield"][d["method"] == "B"].var()],
    "num_df": [(d["method"] == "A").sum() - 1],
    "den_df": [(d["method"] == "B").sum() - 1]}))
  .assign(p_value=lambda x: 2 * np.minimum(stats.f.cdf(x.statistic, x.num_df, x.den_df),
                                           stats.f.sf(x.statistic, x.num_df, x.den_df))))
# Are they significantly different? (No --> p = 0.5049)


# How would we do this in a 'tidy' way?

# Put the result into a data.frame, like broom's tidy() function
# (the group means, xbar, give the estimates; the test result, res, the rest)
(lambda res: print(data.groupby("method")["yield"].mean()
  .pipe(lambda xbar: pd.DataFrame({
    "estimate": [xbar["A"] - xbar["B"]], "estimate1": [xbar["A"]], "estimate2": [xbar["B"]],
    "statistic": [res.statistic], "p_value": [res.pvalue], "parameter": [res.df],
    "conf_low": [res.confidence_interval(0.95).low],
    "conf_high": [res.confidence_interval(0.95).high]}))))(stats.ttest_ind(
  data["yield"][data["method"] == "A"], data["yield"][data["method"] == "B"], equal_var=True))

# 'statistic' is the t-statistic.
# 'p_value' is the p-value of the t-statistic
# 'estimate' is the difference of means.
# 'conf_low' and 'conf_high' are the 95% confidence intervals
#      around the difference of means.





# Paired t-tests ##################################################

# When data comes in pairs, like this, we use paired t-tests.
data2 = pd.DataFrame({
  "yield_a": [89.7, 81.4, 84.5, 84.8, 87.3, 79.7, 85.1, 81.7, 83.7, 84.5],
  "yield_b": [84.7, 86.1, 83.2, 91.9, 86.3, 79.3, 82.6, 89.1, 83.7, 88.5]})


# Basic method for paired t-test
(lambda res: print(res, res.confidence_interval(0.95)))(
  stats.ttest_rel(data2["yield_a"], data2["yield_b"]))

# Or, do it in a data.frame friendly way like this:
(lambda res: print(pd.DataFrame({
  "estimate": [(data2["yield_a"] - data2["yield_b"]).mean()],
  "statistic": [res.statistic], "p_value": [res.pvalue], "parameter": [res.df],
  "conf_low": [res.confidence_interval(0.95).low],
  "conf_high": [res.confidence_interval(0.95).high]})))(
  stats.ttest_rel(data2["yield_a"], data2["yield_b"]))



# Permutation Test #################################################

# How would we do a permutation test of the difference of means?


# Let's do 1 permutation together.

# Randomly shuffle the outcomes across groups
# (sample(yield) in R; "yield" is quoted because it is a reserved word in Python)
print(data.assign(**{"yield": lambda x: np.random.permutation(x["yield"].values)}))

# Get back the means for A and B, and the difference
print(data.assign(**{"yield": lambda x: np.random.permutation(x["yield"].values)})
  .pipe(lambda d: pd.DataFrame({
    "xbar_a": [d["yield"][d["method"] == "A"].mean()],
    "xbar_b": [d["yield"][d["method"] == "B"].mean()]}))
  .assign(dbar=lambda x: x.xbar_a - x.xbar_b))


# Let's try it 1000 times!

# Get the dataset, 1000 times
print(pd.concat([data.assign(rep=r) for r in range(1, 1001)], ignore_index=True))


# Shuffle the outcome for each replicated dataset...
print(pd.concat([data.assign(rep=r) for r in range(1, 1001)], ignore_index=True)
  .assign(**{"yield": lambda x: x.groupby("rep")["yield"]
                                 .transform(lambda y: np.random.permutation(y.values))}))


# Do it all!
perms = (pd.concat([data.assign(rep=r) for r in range(1, 1001)], ignore_index=True)
  .assign(**{"yield": lambda x: x.groupby("rep")["yield"]
                                 .transform(lambda y: np.random.permutation(y.values))})
  .groupby("rep")[["method", "yield"]]
  .apply(lambda d: pd.Series({
    "xbar_a": d["yield"][d["method"] == "A"].mean(),
    "xbar_b": d["yield"][d["method"] == "B"].mean()}))
  .assign(dbar=lambda x: x.xbar_a - x.xbar_b)
  .reset_index())
print(perms)

# Get the observed difference of means
obs = (data.pipe(lambda d: pd.DataFrame({
    "xbar_a": [d["yield"][d["method"] == "A"].mean()],
    "xbar_b": [d["yield"][d["method"] == "B"].mean()]}))
  .assign(dbar=lambda x: x.xbar_a - x.xbar_b))


# Now, what percentage of random stats were greater than the observed?
# That's our p-value!

# 1-tailed test
print((perms["dbar"] >= obs["dbar"].iloc[0]).mean())

# 2-tailed test --> turn all dbars positive
print((perms["dbar"].abs() >= abs(obs["dbar"].iloc[0])).mean())


# Or in a tidy way...
print(perms.pipe(lambda d: pd.DataFrame({"estimate": obs["dbar"].values})
  .assign(p_value=lambda x: (d["dbar"].abs() >= abs(x.estimate[0])).mean())))

# Visualize it!


(ggplot() +
  geom_histogram(data=perms, mapping=aes(x="dbar"), fill="dodgerblue", color="white", bins=30) +
  geom_vline(data=obs, mapping=aes(xintercept="dbar")) +
  geom_label(data=obs.assign(y=50), mapping=aes(y="y", x="dbar", label="dbar"), ha="left"))




# ANOVA ###################################################

import sys
sys.path.append("functions")
from functions_models import lm, glance   # lm() in R, and glance() from broom
import statsmodels.api as sm              # anova tables (tidy(aov()) in R)
from statsmodels.stats.oneway import anova_oneway  # oneway.test() in R

donuts = pd.read_csv("workshops/donuts.csv")
# Or, straight from GitHub:
# donuts = pd.read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/donuts.csv")

# Use lm()...
print(glance(lm(formula="weight ~ baker", data=donuts))[["sigma", "statistic", "p_value", "df"]])

# Or use aov()...
print(sm.stats.anova_lm(lm(formula="weight ~ baker", data=donuts)))

# Visualize the difference

(ggplot() +
  geom_violin(data=donuts, mapping=aes(x="baker", y="weight")) +
  geom_point(data=donuts, mapping=aes(x="baker", y="weight")) +
  geom_point(
    data=donuts.groupby("baker", as_index=False).agg(xbar=("weight", "mean")),
    mapping=aes(x="baker", y="xbar"), color="dodgerblue", size=5) +
  geom_hline(yintercept=donuts["weight"].mean(), color="dodgerblue") +
  coord_flip())


# Unequal Variances #####################################

# Are the variances of my 3+ groups significantly different?
# Homogeneity of Variance - Barlett's test for K^2
# (weight ~ baker in R: one array of weights per baker, handed to bartlett())
print(stats.bartlett(*[g["weight"].values for _, g in donuts.groupby("baker")]))

# K-squared is a ratio showing how different are the variances, from 0 to infinity.
# If K-squared is not significant, the differences are not significant.

# Looks like the differences in variance are quite significant.
# Best **not** to assume equal variance.

# You can do an ANOVA without the equal variance assumption using oneway.test()
print(anova_oneway(donuts["weight"], groups=donuts["baker"], use_var="unequal"))

(lambda w: print(pd.DataFrame({"num_df": [w.df_num], "den_df": [w.df_denom],
                               "statistic": [w.statistic], "p_value": [w.pvalue]})))(
  anova_oneway(donuts["weight"], groups=donuts["baker"], use_var="unequal"))
