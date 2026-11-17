# 09_lesson_fit_and_plan_solutions.py
# Tim Fraser
# Worked solutions for Lesson 13, Example 8: Fit and Plan. Try the questions first.
#
# Run it from the top of the project folder:
#   python code/09_lesson_fit_and_plan_solutions.py
# or chunk by chunk. Every answer is printed.

# Load packages
import sys
import numpy as np
import pandas as pd
pd.set_option("display.width", 200)

# Load our helper functions
sys.path.append("functions")
from functions_mle import get_fit, get_mle, plife, qlife
from functions_planning import plan_test

# A small p-value (under 0.05) rules a distribution out.
# Among the rest, the highest log-likelihood fits best.


# Example 8a. Fit the bearings #######################################

# 200 bearings went on test; the test stopped at 1,400 hours.
bearings = pd.read_csv("workshops/bearings.csv")
fit_b = get_fit(data = bearings, n_total = 200, tmax = 1400)
print(fit_b[["dist", "est1", "est2", "loglik", "p_value"]])

# Which distributions does the test rule out?
print("8a ruled out:", " ".join(fit_b.query("p_value < 0.05")["dist"]))

# get_fit() sorts by log-likelihood, so the best one left is the first kept row.
win_b = fit_b.query("p_value >= 0.05").iloc[0]
print("8a best fit:", win_b["dist"], "with log-likelihood", round(win_b["loglik"], 2))


# Example 8b. Fit the displays #######################################

# 180 displays went on test; the test stopped at 1,750 hours.
displays = pd.read_csv("workshops/displays.csv")
fit_d = get_fit(data = displays, n_total = 180, tmax = 1750)
print(fit_d[["dist", "est1", "est2", "loglik", "p_value"]])

# Which distributions does the test rule out?
print("8b ruled out:", " ".join(fit_d.query("p_value < 0.05")["dist"]))

# The best one left.
win_d = fit_d.query("p_value >= 0.05").iloc[0]
print("8b best fit:", win_d["dist"], "with log-likelihood", round(win_d["loglik"], 2))


# Example 8c. Use the fit ############################################

# Fit the bearings' winner on its own.
mle = get_mle(data = bearings, n_total = 200, tmax = 1400, dist = "weibull")
m = float(mle["m"].iloc[0])
c = float(mle["c"].iloc[0])
print("8c shape m =", f"{m:.4g}", " characteristic life c =", f"{c:.4g}", "hours")

# Share of bearings failed by 500 hours.
print("8c share failed by 500 hours:", f"{np.asarray(plife(500, dist = 'weibull', m = m, c = c)).item():.4g}")

# Time by which 10% have failed.
print("8c time for 10% to fail:", f"{np.asarray(qlife(0.10, dist = 'weibull', m = m, c = c)).item():.4g}", "hours")


# Example 8d. Plan a test ############################################

# Test for 300 hours, allow up to 2 failures, 90% confidence, c as fitted.
# Try the fitted shape, then 0.5 lower and 0.5 higher.
# The note about F_t for the lowest shape is expected.
plans = plan_test("weibull", t = 300, r = 2, ci = 0.90, m = [m - 0.5, m, m + 0.5], c = c)
print(plans[["m", "c", "F_t", "n_up"]])
print("8d units needed (m - 0.5, m, m + 0.5):", " ".join(str(int(v)) for v in plans["n_up"]))

# A higher shape means fewer early failures, so a short test sees less and needs more units.
# If the shape is only assumed, the answer can be off by a factor of two or more.
