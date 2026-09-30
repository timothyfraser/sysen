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
import statsmodels.formula.api as smf     # lm() and aov() in R
import statsmodels.api as sm              # anova tables (tidy(aov()) in R)
from statsmodels.stats.oneway import anova_oneway  # oneway.test() in R


# Unpaired t-tests ###############################################

data = pd.DataFrame({
  "method": ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A",
             "B", "B", "B", "B", "B", "B", "B", "B", "B", "B"],
  "yield": [89.7, 81.4, 84.5, 84.8, 87.3, 79.7, 85.1, 81.7, 83.7, 84.5,
            84.7, 86.1, 83.2, 91.9, 86.3, 79.3, 82.6, 89.1, 83.7, 88.5]})

a = data.loc[data["method"] == "A", "yield"]
b = data.loc[data["method"] == "B", "yield"]

# T-test assuming equal variance (unpaired)
res = stats.ttest_ind(a, b, equal_var=True)
print(res, res.confidence_interval(0.95))


# T-test not assuming equal variance
res = stats.ttest_ind(a, b, equal_var=False)
print(res, res.confidence_interval(0.95))


# Variance F-tests ################################

# How different are the variances?
print(data.groupby("method", as_index=False).agg(var=("yield", "var")))

# Is that difference significant?
# F test to compare two variances. (var.test() in R; scipy has no one-liner,
# so we build it: F = var(A) / var(B), on (nA - 1, nB - 1) degrees of freedom.)
f = a.var() / b.var()
df1, df2 = len(a) - 1, len(b) - 1
p = 2 * min(stats.f.cdf(f, df1, df2), stats.f.sf(f, df1, df2))
print(pd.DataFrame({"statistic": [f], "num_df": [df1], "den_df": [df2], "p_value": [p]}))
# Are they significantly different? (No --> p = 0.5049)


# How would we do this in a 'tidy' way?

# Put the result into a data.frame, like broom's tidy() function
res = stats.ttest_ind(a, b, equal_var=True)
ci = res.confidence_interval(0.95)
print(pd.DataFrame({"estimate": [a.mean() - b.mean()], "estimate1": [a.mean()],
                    "estimate2": [b.mean()], "statistic": [res.statistic],
                    "p_value": [res.pvalue], "parameter": [res.df],
                    "conf_low": [ci.low], "conf_high": [ci.high]}))

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
res = stats.ttest_rel(data2["yield_a"], data2["yield_b"])
print(res, res.confidence_interval(0.95))

# Or, do it in a data.frame friendly way like this:
ci = res.confidence_interval(0.95)
print(pd.DataFrame({"estimate": [(data2["yield_a"] - data2["yield_b"]).mean()],
                    "statistic": [res.statistic], "p_value": [res.pvalue],
                    "parameter": [res.df], "conf_low": [ci.low], "conf_high": [ci.high]}))



# Permutation Test #################################################

# How would we do a permutation test of the difference of means?

rng = np.random.default_rng()

def diff_means(d):
    xbar_a = d.loc[d["method"] == "A", "yield"].mean()
    xbar_b = d.loc[d["method"] == "B", "yield"].mean()
    return pd.Series({"xbar_a": xbar_a, "xbar_b": xbar_b, "dbar": xbar_a - xbar_b})

# Let's do 1 permutation together.

# Randomly shuffle the outcomes across groups
print(data.assign(**{"yield": rng.permutation(data["yield"].values)}))

# Get back the means for A and B, and the difference
print(diff_means(data.assign(**{"yield": rng.permutation(data["yield"].values)})))


# Let's try it 1000 times!

# Get the dataset, 1000 times
reps = pd.concat([data.assign(rep=r) for r in range(1, 1001)], ignore_index=True)
print(reps)


# Shuffle the outcome for each replicated dataset...
reps["yield"] = reps.groupby("rep")["yield"].transform(lambda y: rng.permutation(y.values))
print(reps)


# Do it all!
perms = (reps.groupby("rep")[["method", "yield"]]
         .apply(diff_means)
         .reset_index())
print(perms)

# Get the observed difference of means
obs = diff_means(data).to_frame().T


# Now, what percentage of random stats were greater than the observed?
# That's our p-value!

# 1-tailed test
print((perms["dbar"] >= obs["dbar"].iloc[0]).mean())

# 2-tailed test --> turn all dbars positive
print((perms["dbar"].abs() >= abs(obs["dbar"].iloc[0])).mean())


# Or in a tidy way...
estimate = obs["dbar"].iloc[0]
print(pd.DataFrame({"estimate": [estimate],
                    "p_value": [(perms["dbar"].abs() >= abs(estimate)).mean()]}))

# Visualize it!


(ggplot() +
  geom_histogram(data=perms, mapping=aes(x="dbar"), fill="dodgerblue", color="white", bins=30) +
  geom_vline(data=obs, mapping=aes(xintercept="dbar")) +
  geom_label(data=obs.assign(y=50), mapping=aes(y="y", x="dbar", label="dbar"), ha="left"))




# ANOVA ###################################################

donuts = pd.read_csv("workshops/donuts.csv")
# Or, straight from GitHub:
# donuts = pd.read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/donuts.csv")

# Use lm()... (glance() in R: model-level statistics)
m = smf.ols("weight ~ baker", data=donuts).fit()
print(pd.DataFrame({"sigma": [np.sqrt(m.scale)], "statistic": [m.fvalue],
                    "p_value": [m.f_pvalue], "df": [m.df_model]}))

# Or use aov()...
print(sm.stats.anova_lm(m))

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
groups = [g["weight"].values for _, g in donuts.groupby("baker")]
print(stats.bartlett(*groups))

# K-squared is a ratio showing how different are the variances, from 0 to infinity.
# If K-squared is not significant, the differences are not significant.

# Looks like the differences in variance are quite significant.
# Best **not** to assume equal variance.

# You can do an ANOVA without the equal variance assumption using oneway.test()
w = anova_oneway(donuts["weight"], groups=donuts["baker"], use_var="unequal")
print(w)

print(pd.DataFrame({"num_df": [w.df_num], "den_df": [w.df_denom],
                    "statistic": [w.statistic], "p_value": [w.pvalue]}))
