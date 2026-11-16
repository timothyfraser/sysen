# 09_workshop_fit.py
# Tim Fraser
# Workshop 13: Does it fit? Fitting and testing life distributions from a crosstab
# Chapter: Useful Life Distributions (Weibull, Gamma, & Lognormal) in Python
#
# This is the Python twin of 09_workshop_fit.R, section by section.
#
# The data in workshops/chips.csv is simulated. These lines made it:
#   rng = np.random.default_rng(5300)
#   t = rng.lognormal(mean = np.log(1000), sigma = 0.8, size = 200)  # 200 chips, median life 1,000 hours
#   edges = np.arange(0, 1501, 250)                                   # we read out every 250 hours
#   r_obs = np.histogram(t, bins = edges)[0]                          # failures in each interval
# (The random numbers differ from R's, so both tracks read the same csv.)
# Run this file from the top of the project folder, chunk by chunk.

# Load packages
import sys
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import chi2, lognorm
from plotnine import *
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

# Load our helper functions
sys.path.append("functions")
from functions_distributions import pexp
from functions_mle import get_mle, get_chisq, get_fit, get_expected
from functions_planning import plan_test

# NOTE: `lambda` is a reserved word in Python, so we write `lambda_` instead.


# 1. The crosstab ####################################################

# A crosstab counts failures in each time interval.
chips = pd.read_csv("workshops/chips.csv")
print(chips)

# n_total is how many chips we put on test.
n_total = 200

# tmax is the hour the test stopped; chips still running then are the survivors.
tmax = 1500

# 137 chips failed, so 63 are survivors.
print(n_total - chips["r_obs"].sum())


# 2. The exponential, by hand ########################################

# r is the number of failures we saw.
r = chips["r_obs"].sum()

# Midpoint of each interval, times its failures, stands in for the failure times.
tab = chips.assign(midpoint = (chips["lower"] + chips["upper"]) / 2)

# Total hours on test: failures count at their midpoints.
# Survivors count at tmax.
hours = (tab["midpoint"] * tab["r_obs"]).sum() + (n_total - r) * tmax

# Lambda-hat is failures divided by total hours.
lambda_hat = r / hours
print(lambda_hat)

# The chi-squared test follows Tobias and Trindade, Applied Reliability, section 3.8.
# Steps 1 and 2 are done: we grouped failures into intervals and estimated lambda.

# Step 3: the chance of failing in each interval is F(upper) - F(lower).
# Step 4: expected failures are n_total times that chance.
tab = tab.assign(p_fail = pexp(tab["upper"], rate = lambda_hat) - pexp(tab["lower"], rate = lambda_hat))
tab = tab.assign(r_exp = n_total * tab["p_fail"])

# Step 4, continued: one last cell runs from tmax to infinity.
# It holds the chips still running: observed n_total - r, expected n_total x (1 - F(tmax)).
p_last = float(1 - pexp(tmax, rate = lambda_hat).iloc[0])
last = pd.DataFrame({"lower": [tmax], "upper": [np.inf], "r_obs": [n_total - r],
                     "p_fail": [p_last], "r_exp": [n_total * p_last]})
cells = pd.concat([tab[["lower", "upper", "r_obs", "p_fail", "r_exp"]], last], ignore_index = True)
print(cells)

# The expected counts add up to n_total.
print(cells["r_exp"].sum())

# Step 5: every expected count must be at least 5.
# Otherwise we merge a thin cell with its neighbour; get_chisq() does this for you.
print(cells["r_exp"].min())

# Step 6: chi-squared adds up (observed - expected)^2 / expected over the cells.
chisq = ((cells["r_obs"] - cells["r_exp"]) ** 2 / cells["r_exp"]).sum()
print(chisq)

# Step 7: degrees of freedom: cells, minus 1, minus 1 for the parameter we estimated.
df = len(cells) - 1 - 1
print(df)

# Step 8: the p-value is the chance of a chi-squared this big if the exponential were true.
print(1 - chi2.cdf(chisq, df = df))

# get_chisq() gives the same number.
print(get_chisq(data = chips, n_total = n_total, f = pexp, np = 1, rate = lambda_hat))

# Tiny p-value: the exponential does not fit these chips.


# 3. The lognormal likelihood, written out ###########################

# scipy writes the lognormal as lognorm(s = sigma, scale = t50).
def plnorm(t, t50, sigma):
    return lognorm.cdf(t, s = sigma, scale = t50)

# The log-likelihood adds up the log chance of what we saw in each interval.
# Chips that failed in an interval contribute r_obs times log(F(upper) - F(lower)).
# Survivors contribute (n - r) times log(1 - F(tmax)).
def ll(par, data, n_total, tmax):
    t50 = np.exp(par[0])
    sigma = np.exp(par[1])
    p_fail = plnorm(data["upper"], t50, sigma) - plnorm(data["lower"], t50, sigma)
    p_survive = 1 - plnorm(tmax, t50, sigma)
    return (data["r_obs"] * np.log(p_fail)).sum() + (n_total - data["r_obs"].sum()) * np.log(p_survive)

# We search over log(t50) and log(sigma).
# That way minimize() can never try a negative value.
# minimize() minimizes, so we hand it the negative log-likelihood.
# Minimizing that is the same as maximizing the log-likelihood.
# We start from rough guesses: t50 = 1000 hours, sigma = 1.
fit = minimize(fun = lambda par: -ll(par, chips, n_total, tmax),
               x0 = [np.log(1000), np.log(1)], method = "Nelder-Mead",
               options = {"xatol": 1e-10, "fatol": 1e-12, "maxiter": 2000})

# Undo the logs to get t50 and sigma back.
print(np.exp(fit.x))
print(-fit.fun)


# 4. get_mle() gives the same numbers ################################

# get_mle() does the same work for any of the four distributions.
print(get_mle(data = chips, n_total = n_total, tmax = tmax, dist = "lognormal"))

# For the exponential, its lambda differs slightly from step 2.
# The helper uses the chance of failing inside each interval.
# Step 2 used the midpoint shortcut.
print(get_mle(data = chips, n_total = n_total, tmax = tmax, dist = "exponential"))


# 5. Does it fit? All four at once ###################################

# get_fit() fits and tests all four distributions, highest log-likelihood first.
# The log-likelihood measures how likely the data are under each fitted distribution; higher is better.
print(get_fit(data = chips, n_total = n_total, tmax = tmax)[["dist", "est1", "est2", "loglik", "chisq", "df", "p_value"]])

# A small p-value (under 0.05) rules a distribution out.
# Among those left, the highest log-likelihood fits best.

# The test includes a last cell for the chips still running, as in step 2.
# It also merges cells with fewer than 5 expected failures.


# 6. Observed against expected #######################################

# Keep the fitted estimates for later.
fits = get_fit(data = chips, n_total = n_total, tmax = tmax)

# For one family, get_expected() takes its parameters by name.
print(get_expected(chips, n_total = n_total, dist = "lognormal", t50 = 1009.9, sigma = 0.81089))

# Do that for all four families, then stack the results.
# get_expected() wants the rate called lambda_, so we rename it.
def expected_for(row):
    pars = {row["par1"].replace("lambda", "lambda_"): row["est1"]}
    if isinstance(row["par2"], str):
        pars[row["par2"].replace("lambda", "lambda_")] = row["est2"]
    return get_expected(chips, n_total = n_total, dist = row["dist"], **pars).assign(dist = row["dist"])

expected = pd.concat([expected_for(row) for _, row in fits.iterrows()], ignore_index = True)
is_cell = np.isfinite(expected["upper"])
expected = expected.assign(cell = np.where(is_cell,
                                           expected["lower"].astype(int).astype(str) + "-" + expected["upper"].replace(np.inf, 0).astype(int).astype(str),
                                           "survivors"))

# Keep the cells in time order for the plot.
expected["cell"] = pd.Categorical(expected["cell"], categories = expected["cell"].unique())

# Bars are what we observed; lines and points are what each distribution expects.
gg = (ggplot()
      + geom_col(data = expected.query("dist == 'lognormal'"),
                 mapping = aes(x = "cell", y = "r_obs"), fill = "lightgrey")
      + geom_line(data = expected, mapping = aes(x = "cell", y = "r_exp", color = "dist", group = "dist"), size = 1)
      + geom_point(data = expected, mapping = aes(x = "cell", y = "r_exp", color = "dist"), size = 2)
      + theme_classic(base_size = 14)
      + labs(x = "Hours on test", y = "Number of chips", color = "Distribution"))
print(gg)
# In a script the plot does not pop up by itself; save it to see it.
# gg.save("chips_fit.png", width = 8, height = 5, dpi = 150)

# The lognormal line hugs the bars best, which matches its highest log-likelihood.


# 7. Censoring #######################################################

# Time-censored means we stop at a set hour.
# Failure-censored means we stop at the r-th failure.
# Either way, you just pass the stopping time as tmax.
# Here we stop at 1000 hours.
# We keep the first four intervals, and the other chips are survivors.
chips_1000 = chips.query("upper <= 1000")
print(get_mle(data = chips_1000, n_total = n_total, tmax = 1000, dist = "lognormal"))

# With less data the estimates move a bit.


# 8. Planning a life test ############################################

# plan_test() solves for whichever piece you leave out.
# Here it is n, the number of units.
# First the exponential: 5,000 hours, up to 5 failures, 90% confident, lambda = 1/500,000.
print(plan_test("exponential", t = 5000, r = 5, ci = 0.90, lambda_ = 1 / 500000))

# Now plan for our chips.
# The next lot must show a median life (t50) of at least 1,000 hours.
# We can test for 250 hours, allow up to 5 failures, and want 90% confidence.
# How many chips?
# The shape parameter (sigma) cannot be solved for, so we borrow it from the fit in step 5.
sigma_fit = fits.query("dist == 'lognormal'")["est2"].iloc[0]
print(sigma_fit)
print(plan_test("lognormal", t = 250, r = 5, ci = 0.90, t50 = 1000, sigma = sigma_fit)[["sigma", "F_t", "n_up"]])

# The answer leans on the sigma we assumed.
# So try several at once (sigma can be a list).
# A warning below is expected.
# F_t is the chance one chip fails during the test.
# A big F_t makes the shortcut formula loose.
print(plan_test("lognormal", t = 250, r = 5, ci = 0.90, t50 = 1000, sigma = [0.6, 0.8, 1.0, 1.2])[["sigma", "F_t", "n_up"]])

# exact = True skips the shortcut formula and uses the binomial distribution instead.
# Each chip either fails during the test or does not.
# The binomial distribution counts how many fail.
print(plan_test("lognormal", t = 250, r = 5, ci = 0.90, t50 = 1000, sigma = sigma_fit, exact = True)[["sigma", "F_t", "n_up"]])

# No failures allowed: r = 0.
print(plan_test("lognormal", t = 250, r = 0, ci = 0.90, t50 = 1000, sigma = sigma_fit)[["sigma", "F_t", "n_up"]])

# Only 100 chips available?
# Leave out t and give n = 100.
# Then t is solved for: how long to test.
print(plan_test("lognormal", n = 100, r = 5, ci = 0.90, t50 = 1000, sigma = sigma_fit)[["sigma", "n", "t"]])

# Acceleration: a hot test where each hour counts as 50 hours of normal use (af = 50).
# Leave out t50 and give n = 208 and t = 250.
# Then t50 is solved for.
# It is the median life at normal use that this test shows.
# We will meet acceleration factors properly in next week's lesson.
print(plan_test("lognormal", n = 208, t = 250, r = 5, ci = 0.90, sigma = sigma_fit, af = 50)[["sigma", "n", "t", "af", "t50"]])
