# 09_lesson_fit_and_plan_solutions.R
# Tim Fraser
# Worked solutions for Lesson 13, Example 8: Fit and Plan. Try the questions first.
#
# Run it from the top of the project folder:
#   Rscript code/09_lesson_fit_and_plan_solutions.R
# or chunk by chunk in RStudio. Every answer is printed.

# Load packages
library(dplyr)
library(readr)

# Load our helper functions
source("functions/functions_mle.R")
source("functions/functions_planning.R")

# A small p-value (under 0.05) rules a distribution out.
# Among the rest, the highest log-likelihood fits best.


# Example 8a. Fit the bearings #######################################

# 200 bearings went on test; the test stopped at 1,400 hours.
bearings = read_csv("workshops/bearings.csv", show_col_types = FALSE)
fit_b = get_fit(data = bearings, n_total = 200, tmax = 1400)
fit_b %>% select(dist, est1, est2, loglik, p_value) %>% as.data.frame() %>% print()

# Which distributions does the test rule out?
cat("8a ruled out:", fit_b %>% filter(p_value < 0.05) %>% pull(dist), "\n")

# get_fit() sorts by log-likelihood, so the best one left is the first kept row.
win_b = fit_b %>% filter(p_value >= 0.05) %>% slice(1)
cat("8a best fit:", win_b$dist, "with log-likelihood", round(win_b$loglik, 2), "\n")


# Example 8b. Fit the displays #######################################

# 180 displays went on test; the test stopped at 1,750 hours.
displays = read_csv("workshops/displays.csv", show_col_types = FALSE)
fit_d = get_fit(data = displays, n_total = 180, tmax = 1750)
fit_d %>% select(dist, est1, est2, loglik, p_value) %>% as.data.frame() %>% print()

# Which distributions does the test rule out?
cat("8b ruled out:", fit_d %>% filter(p_value < 0.05) %>% pull(dist), "\n")

# The best one left.
win_d = fit_d %>% filter(p_value >= 0.05) %>% slice(1)
cat("8b best fit:", win_d$dist, "with log-likelihood", round(win_d$loglik, 2), "\n")


# Example 8c. Use the fit ############################################

# Fit the bearings' winner on its own.
mle = get_mle(data = bearings, n_total = 200, tmax = 1400, dist = "weibull")
m = mle$m
c = mle$c
cat("8c shape m =", signif(m, 4), " characteristic life c =", signif(c, 4), "hours\n")

# Share of bearings failed by 500 hours.
cat("8c share failed by 500 hours:", signif(plife(500, dist = "weibull", m = m, c = c), 4), "\n")

# Time by which 10% have failed.
cat("8c time for 10% to fail:", signif(qlife(0.10, dist = "weibull", m = m, c = c), 4), "hours\n")


# Example 8d. Plan a test ############################################

# Test for 300 hours, allow up to 2 failures, 90% confidence, c as fitted.
# Try the fitted shape, then 0.5 lower and 0.5 higher.
# The note about F_t for the lowest shape is expected.
plans = plan_test("weibull", t = 300, r = 2, ci = 0.90, m = m + c(-0.5, 0, 0.5), c = c)
plans %>% select(m, c, F_t, n_up) %>% as.data.frame() %>% print()
cat("8d units needed (m - 0.5, m, m + 0.5):", plans$n_up, "\n")

# A higher shape means fewer early failures, so a short test sees less and needs more units.
# If the shape is only assumed, the answer can be off by a factor of two or more.
