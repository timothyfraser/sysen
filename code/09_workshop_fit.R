# 09_workshop_fit.R
# Tim Fraser
# Workshop 13: Does it fit? Fitting and testing life distributions from a crosstab
# Chapter: Useful Life Distributions (Weibull, Gamma, & Lognormal) in R
#
# The data in workshops/chips.csv is simulated. These lines made it:
#   set.seed(5300)
#   t = rlnorm(200, meanlog = log(1000), sdlog = 0.8)   # 200 chips, median life 1,000 hours
#   edges = seq(0, 1500, by = 250)                       # we read out every 250 hours
#   r_obs = as.integer(table(cut(t, breaks = edges)))    # failures in each interval
# Run this file from the top of the project folder, chunk by chunk.

# Load packages
library(dplyr)
library(tibble)
library(readr)
library(ggplot2)

# Load our helper functions
source("functions/functions_mle.R")
source("functions/functions_planning.R")


# 1. The crosstab ####################################################

# A crosstab counts failures in each time interval.
chips = read_csv("workshops/chips.csv")
chips

# n_total is how many chips we put on test.
n_total = 200

# tmax is the hour the test stopped; chips still running then are the survivors.
tmax = 1500

# 137 chips failed, so 63 are survivors.
n_total - sum(chips$r_obs)


# 2. The exponential, by hand ########################################

# r is the number of failures we saw.
r = sum(chips$r_obs)

# Midpoint of each interval, times its failures, stands in for the failure times.
tab = chips %>% mutate(midpoint = (lower + upper) / 2)

# Total hours on test: failures count at their midpoints.
# Survivors count at tmax.
hours = sum(tab$midpoint * tab$r_obs) + (n_total - r) * tmax

# Lambda-hat is failures divided by total hours.
lambda_hat = r / hours
lambda_hat

# The chi-squared test follows Tobias and Trindade, Applied Reliability, section 3.8.
# Steps 1 and 2 are done: we grouped failures into intervals and estimated lambda.

# Step 3: the chance of failing in each interval is F(upper) - F(lower).
# Step 4: expected failures are n_total times that chance.
tab = tab %>%
  mutate(p_fail = pexp(upper, rate = lambda_hat) - pexp(lower, rate = lambda_hat),
         r_exp = n_total * p_fail)

# Step 4, continued: one last cell runs from tmax to infinity.
# It holds the chips still running: observed n_total - r, expected n_total x (1 - F(tmax)).
last = tibble(lower = tmax, upper = Inf, r_obs = n_total - r,
              p_fail = 1 - pexp(tmax, rate = lambda_hat)) %>%
  mutate(r_exp = n_total * p_fail)
cells = tab %>% select(lower, upper, r_obs, p_fail, r_exp) %>% bind_rows(last)
cells

# The expected counts add up to n_total.
sum(cells$r_exp)

# Step 5: every expected count must be at least 5.
# Otherwise we merge a thin cell with its neighbour; get_chisq() does this for you.
min(cells$r_exp)

# Step 6: chi-squared adds up (observed - expected)^2 / expected over the cells.
chisq = cells %>% summarize(chisq = sum((r_obs - r_exp)^2 / r_exp)) %>% pull(chisq)
chisq

# Step 7: degrees of freedom: cells, minus 1, minus 1 for the parameter we estimated.
df = nrow(cells) - 1 - 1
df

# Step 8: the p-value is the chance of a chi-squared this big if the exponential were true.
1 - pchisq(chisq, df = df)

# get_chisq() gives the same number.
get_chisq(data = chips, n_total = n_total, f = pexp, np = 1, rate = lambda_hat)

# Tiny p-value: the exponential does not fit these chips.


# 3. The lognormal likelihood, written out ###########################

# The log-likelihood adds up the log chance of what we saw in each interval.
# Chips that failed in an interval contribute r_obs times log(F(upper) - F(lower)).
# Survivors contribute (n - r) times log(1 - F(tmax)).
ll = function(par, data, n_total, tmax){
  t50 = exp(par[1])
  sigma = exp(par[2])
  p_fail = plnorm(data$upper, meanlog = log(t50), sdlog = sigma) -
    plnorm(data$lower, meanlog = log(t50), sdlog = sigma)
  p_survive = 1 - plnorm(tmax, meanlog = log(t50), sdlog = sigma)
  sum(data$r_obs * log(p_fail)) + (n_total - sum(data$r_obs)) * log(p_survive)
}

# We search over log(t50) and log(sigma).
# That way optim() can never try a negative value.
# optim() minimizes by default.
# So fnscale = -1 makes it maximize.
# We start from rough guesses: t50 = 1000 hours, sigma = 1.
fit = optim(par = c(log(1000), log(1)), fn = ll, data = chips,
            n_total = n_total, tmax = tmax,
            control = list(fnscale = -1, reltol = 1e-12, maxit = 1000))

# Undo the logs to get t50 and sigma back.
exp(fit$par)
fit$value


# 4. get_mle() gives the same numbers ################################

# get_mle() does the same work for any of the four distributions.
get_mle(data = chips, n_total = n_total, tmax = tmax, dist = "lognormal")

# For the exponential, its lambda differs slightly from step 2.
# The helper uses the chance of failing inside each interval.
# Step 2 used the midpoint shortcut.
get_mle(data = chips, n_total = n_total, tmax = tmax, dist = "exponential")


# 5. Does it fit? All four at once ###################################

# get_fit() fits and tests all four distributions, highest log-likelihood first.
# The log-likelihood measures how likely the data are under each fitted distribution; higher is better.
get_fit(data = chips, n_total = n_total, tmax = tmax) %>%
  select(dist, est1, est2, loglik, chisq, df, p_value) %>% as.data.frame()

# A small p-value (under 0.05) rules a distribution out.
# Among those left, the highest log-likelihood fits best.

# The test includes a last cell for the chips still running, as in step 2.
# It also merges cells with fewer than 5 expected failures.


# 6. Observed against expected #######################################

# Keep the fitted estimates for later.
fits = get_fit(data = chips, n_total = n_total, tmax = tmax)

# For one family, get_expected() takes its parameters by name.
get_expected(chips, n_total = n_total, dist = "lognormal", t50 = 1009.9, sigma = 0.81089)

# Do that for all four families, then stack the results.
expected = lapply(fits$dist, function(d){
  row = fits %>% filter(dist == d)
  pars = list(row$est1, row$est2)
  names(pars) = c(row$par1, row$par2)
  pars = pars[!is.na(names(pars))]
  do.call(get_expected, c(list(data = chips, n_total = n_total, dist = d), pars)) %>%
    mutate(dist = d)
}) %>%
  bind_rows() %>%
  mutate(cell = ifelse(is.finite(upper), paste0(lower, "-", upper), "survivors"))

# Keep the cells in time order for the plot.
expected = expected %>% mutate(cell = factor(cell, levels = unique(cell)))

# Bars are what we observed; lines and points are what each distribution expects.
gg = ggplot() +
  geom_col(data = expected %>% filter(dist == "lognormal"),
           mapping = aes(x = cell, y = r_obs), fill = "grey80") +
  geom_line(data = expected, mapping = aes(x = cell, y = r_exp, color = dist, group = dist), linewidth = 1) +
  geom_point(data = expected, mapping = aes(x = cell, y = r_exp, color = dist), size = 2) +
  theme_classic(base_size = 14) +
  labs(x = "Hours on test", y = "Number of chips", color = "Distribution")
print(gg)

# The lognormal line hugs the bars best, which matches its highest log-likelihood.


# 7. Censoring #######################################################

# Time-censored means we stop at a set hour.
# Failure-censored means we stop at the r-th failure.
# Either way, you just pass the stopping time as tmax.
# Here we stop at 1000 hours.
# We keep the first four intervals, and the other chips are survivors.
chips_1000 = chips %>% filter(upper <= 1000)
get_mle(data = chips_1000, n_total = n_total, tmax = 1000, dist = "lognormal")

# With less data the estimates move a bit.


# 8. Planning a life test ############################################

# plan_test() solves for whichever piece you leave out.
# Here it is n, the number of units.
# First the exponential: 5,000 hours, up to 5 failures, 90% confident, lambda = 1/500,000.
plan_test("exponential", t = 5000, r = 5, ci = 0.90, lambda = 1 / 500000)

# Now plan for our chips.
# The next lot must show a median life (t50) of at least 1,000 hours.
# We can test for 250 hours, allow up to 5 failures, and want 90% confidence.
# How many chips?
# The shape parameter (sigma) cannot be solved for, so we borrow it from the fit in step 5.
sigma_fit = fits %>% filter(dist == "lognormal") %>% pull(est2)
sigma_fit
plan_test("lognormal", t = 250, r = 5, ci = 0.90, t50 = 1000, sigma = sigma_fit) %>%
  select(sigma, F_t, n_up) %>% as.data.frame()

# The answer leans on the sigma we assumed.
# So try several at once (sigma can be a vector).
# The message below is expected.
# F_t is the chance one chip fails during the test.
# A big F_t makes the shortcut formula loose.
plan_test("lognormal", t = 250, r = 5, ci = 0.90, t50 = 1000, sigma = c(0.6, 0.8, 1.0, 1.2)) %>%
  select(sigma, F_t, n_up) %>% as.data.frame()

# exact = TRUE skips the shortcut formula and uses the binomial distribution instead.
# Each chip either fails during the test or does not.
# The binomial distribution counts how many fail.
plan_test("lognormal", t = 250, r = 5, ci = 0.90, t50 = 1000, sigma = sigma_fit, exact = TRUE) %>%
  select(sigma, F_t, n_up) %>% as.data.frame()

# No failures allowed: r = 0.
plan_test("lognormal", t = 250, r = 0, ci = 0.90, t50 = 1000, sigma = sigma_fit) %>%
  select(sigma, F_t, n_up) %>% as.data.frame()

# Only 100 chips available?
# Leave out t and give n = 100.
# Then t is solved for: how long to test.
plan_test("lognormal", n = 100, r = 5, ci = 0.90, t50 = 1000, sigma = sigma_fit) %>%
  select(sigma, n, t) %>% as.data.frame()

# Acceleration: a hot test where each hour counts as 50 hours of normal use (af = 50).
# Leave out t50 and give n = 208 and t = 250.
# Then t50 is solved for.
# It is the median life at normal use that this test shows.
# We will meet acceleration factors properly in next week's lesson.
plan_test("lognormal", n = 208, t = 250, r = 5, ci = 0.90, sigma = sigma_fit, af = 50) %>%
  select(sigma, n, t, af, t50) %>% as.data.frame()
