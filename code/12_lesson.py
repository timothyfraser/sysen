# 12_lesson.py
# Tim Fraser
# Lesson 12: t-tests, ANOVA, regression and permutation tests on donuts
# Chapter: Comparing Groups in Python

# It mirrors 12_lesson.R section by section.
# Run it from the top of the sysen folder, so the file paths below work.

# Load packages, to get our data wrangling, plotting, and model functions
import numpy as np                        # math (base R in R)
import pandas as pd                       # data wrangling (dplyr + readr in R)
from plotnine import *                    # visuals (ggplot2 in R)
from scipy import stats                   # t.test(), oneway.test() in R
import statsmodels.formula.api as smf     # lm() and aov() in R
import statsmodels.api as sm              # anova tables
from statsmodels.stats.oneway import anova_oneway  # oneway.test() in R

# Read data!
donuts = pd.read_csv("workshops/donuts.csv")

donuts.info()
# Having trouble reading in your data?
# You can also use this code:
# donuts = pd.read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/donuts.csv")


print(donuts)

# aov(tastiness ~ baker) in R
print(sm.stats.anova_lm(smf.ols("tastiness ~ baker", data=donuts).fit()))

# oneway.test(tastiness ~ baker, var.equal = TRUE) in R
print(anova_oneway(donuts["tastiness"], groups=donuts["baker"], use_var="equal"))
# tastiness varies significantly between bakers

# lm(...) %>% glance() in R: the model-level statistics
m0 = smf.ols("tastiness ~ baker", data=donuts).fit()
print(pd.DataFrame({"r_squared": [m0.rsquared], "adj_r_squared": [m0.rsquared_adj],
                    "sigma": [np.sqrt(m0.scale)], "statistic": [m0.fvalue],
                    "p_value": [m0.f_pvalue], "df": [m0.df_model],
                    "nobs": [m0.nobs]}))



donuts3 = donuts[donuts["baker"].isin(["Craig", "Melanie"])]


# A helper that plays the role of t.test(y ~ group) %>% tidy() in R.
# R's formula t-test subtracts the SECOND factor level from the FIRST,
# so 'levels' decides the sign of the estimate.
def t_test_tidy(data, y, group, levels, equal_var=True):
    a = data.loc[data[group] == levels[0], y]
    b = data.loc[data[group] == levels[1], y]
    res = stats.ttest_ind(a, b, equal_var=equal_var)
    ci = res.confidence_interval(0.95)
    return pd.DataFrame({"estimate": [a.mean() - b.mean()],
                         "estimate1": [a.mean()], "estimate2": [b.mean()],
                         "statistic": [res.statistic], "p_value": [res.pvalue],
                         "parameter": [res.df],
                         "conf_low": [ci.low], "conf_high": [ci.high]})

# By default R orders factor levels alphabetically: Craig, then Melanie
print(t_test_tidy(donuts3, "tastiness", "baker", ["Craig", "Melanie"]))



# Put Melanie first, and the sign of the estimate flips
print(t_test_tidy(donuts3, "tastiness", "baker", ["Melanie", "Craig"]))



print(t_test_tidy(donuts3, "tastiness", "baker", ["Melanie", "Craig"]))



# Convert type to factor, where treatment group b is first
donuts2 = donuts.assign(type=pd.Categorical(donuts["type"], categories=["b", "a"]))




# donuts["tastiness"].unique()





#

donuts = pd.read_csv("workshops/donuts.csv")

donuts.info()


# Tidy long format
long = (donuts.groupby("type", as_index=False)
        .agg(xbar=("tastiness", "mean"))
        .assign(testid=1))


# Wide matrix
wide = pd.DataFrame({"xbar_a": [2.84], "xbar_b": [4.16]})
wide["dbar"] = wide["xbar_b"] - wide["xbar_a"]


print(long)

# tidyr::pivot_wider() in R
long_wide = long.pivot(index="testid", columns="type", values="xbar").reset_index()
long_wide["dbar"] = long_wide["b"] - long_wide["a"]
print(long_wide)


# T-test Examples ##########################################################

donuts2 = donuts.assign(type=pd.Categorical(donuts["type"], categories=["a", "b"]))


# Run our t-test using the data from donuts, then tidy it into a data.frame
print(t_test_tidy(donuts2, "weight", "type", ["a", "b"]))


# lm(weight ~ type) %>% tidy() in R
print(smf.ols("weight ~ type", data=donuts2).fit().summary().tables[1])

print(donuts2.groupby("type", observed=True, as_index=False).agg(xbar=("weight", "mean")))

# There's a -3.4 gram difference (95% CI is -1.8 ~ -4.9, p < 0.001)
# What if we knew that 1 gram costs us $0.01
# What if we knew that we're going to produce 50,000 donuts
#

dbar = -3.4
dbar_lower = -1.8
n = 50000
cost_per_gram = 0.01
print(dbar * cost_per_gram * n)



print(donuts.groupby("type", as_index=False).agg(var=("weight", "var")))



print(t_test_tidy(donuts2, "weight", "type", ["a", "b"], equal_var=False))




(ggplot() +
  geom_violin(data=donuts2, mapping=aes(x="type", y="weight")) +
  geom_jitter(data=donuts2, mapping=aes(x="type", y="weight")))


(ggplot() +
  geom_boxplot(data=donuts2, mapping=aes(x="type", y="weight")) +
  geom_jitter(data=donuts2, mapping=aes(x="type", y="weight")))





donuts.info()


print(donuts.groupby("baker").size())


m = smf.ols("tastiness ~ baker", data=donuts).fit()

print(m.params)


# broom::tidy(m) in R: one row per coefficient
tidy_m = pd.DataFrame({"term": m.params.index, "estimate": m.params.values,
                       "std_error": m.bse.values, "statistic": m.tvalues.values,
                       "p_value": m.pvalues.values})
print(tidy_m)


print(m.params)

tidy_m["t"] = (tidy_m["estimate"] - 0) / tidy_m["std_error"]
print(tidy_m)

# stats.t.sf(7.20, df=47) / 2
print(m.summary())


# broom::tidy(m, conf.int = TRUE) in R
ci = m.conf_int(0.05)
tidy_ci = tidy_m.assign(conf_low=ci[0].values, conf_high=ci[1].values)

(ggplot(tidy_ci, aes(x="term", y="estimate", ymin="conf_low", ymax="conf_high")) +
  geom_linerange() +
  geom_point())


# Let's see a t distribution with 47 degrees of freedom
(ggplot(pd.DataFrame({"t": stats.t.rvs(df=47, size=1000)}), aes(x="t")) +
  geom_histogram(bins=20))


# Let's get confidence intervals...
print(tidy_ci.loc[tidy_ci["term"] == "baker[T.Melanie]", ["term", "conf_low"]])

# bind_rows() of two models' coefficients in R
m1 = smf.ols("tastiness ~ baker", data=donuts).fit()
m2 = smf.ols("tastiness ~ baker + weight", data=donuts).fit()
both = pd.concat([
  pd.DataFrame({"term": m1.params.index, "estimate": m1.params.values,
                "std_error": m1.bse.values, "model": 1}),
  pd.DataFrame({"term": m2.params.index, "estimate": m2.params.values,
                "std_error": m2.bse.values, "model": 2})
])
print(both[both["term"] == "baker[T.Melanie]"])



# scale() in R: subtract the mean, divide by the standard deviation
scaled = donuts.assign(
  weight=(donuts["weight"] - donuts["weight"].mean()) / donuts["weight"].std(),
  lifespan=(donuts["lifespan"] - donuts["lifespan"].mean()) / donuts["lifespan"].std())
print(smf.ols("tastiness ~ weight + lifespan + baker", data=scaled).fit().params)

# As weight increased by 1 standard deviation,
# tastiness changes by 0.26

# As lifespan increases by 1 standard deviation,
# tastiness changes by -0.06














# Permutation Test Examples ##################################################
# (The packages are already loaded above.)

# Read data!
donuts = pd.read_csv("workshops/donuts.csv")


def dbar_of(d):
    return (d.loc[d["baker"] == "Melanie", "tastiness"].mean() -
            d.loc[d["baker"] == "Craig", "tastiness"].mean())

obs = pd.DataFrame({"dbar": [dbar_of(donuts)]})

print(obs["dbar"].iloc[0])

rng = np.random.default_rng()
print(donuts.assign(tastiness=rng.permutation(donuts["tastiness"].values)))

# Get 1000 identical datasets, shuffle the quality metric within each,
# and get the difference of means for each rep
mydbar = pd.DataFrame({
  "reps": range(1, 1001),
  "dbar": [dbar_of(donuts[["baker", "tastiness"]].assign(
             tastiness=rng.permutation(donuts["tastiness"].values)))
           for _ in range(1000)]})


(ggplot() +
  geom_histogram(data=mydbar, mapping=aes(x="dbar"), bins=30) +
  geom_vline(xintercept=obs["dbar"].iloc[0]))


print((mydbar["dbar"] > obs["dbar"].iloc[0]).mean())





####################################################
# Deprecated content
# (kept as comments in 12_lesson.R; see that file)
