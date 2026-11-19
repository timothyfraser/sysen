# slides_workshop_9_planning.py ---------------------------------------------
#
# Python twin of slides_workshop_9_planning.R. Feeds: Workshop 9 slide
# "Planning a Life Test: when it is not exponential", the Exponential and
# Weibull tabs. Fits the chips data (200 chips on test, stopped at 1500 hours),
# then plans a 250-hour test allowing 5 failures at 90% confidence.
# Run from the sigma repo root:
#   python functions/slides_workshop_9_planning.py
# Prints the numbers the slide shows; writes nothing.

import sys
sys.path.insert(0, "functions")
import pandas as pd
from functions_mle import get_mle
from functions_planning import plan_test

chips = pd.read_csv("workshops/chips.csv")

# 1. Fit each family to the chips
fit_exp = get_mle(data = chips, n_total = 200, tmax = 1500, dist = "exponential")
fit_wei = get_mle(data = chips, n_total = 200, tmax = 1500, dist = "weibull")
print(fit_exp)
print(fit_wei)

lam = float(fit_exp["lambda"].iloc[0])
m_fit = float(fit_wei["m"].iloc[0])
c_fit = float(fit_wei["c"].iloc[0])

# 2. Exponential plan: one number, no shape to assume
p_exp = plan_test("exponential", t = 250, r = 5, ci = 0.90, **{"lambda": lam})
print("\nExponential plan: lambda =", round(lam, 7), " n_up =", int(p_exp["n_up"].iloc[0]))

# 3. Weibull plan: the shape must be assumed, so try a grid around the fit
grid = [round(m_fit + d, 2) for d in (-0.5, -0.25, 0, 0.25, 0.5)]
p_wei = pd.concat([plan_test("weibull", t = 250, r = 5, ci = 0.90, c = c_fit, m = m)
                   for m in grid], ignore_index = True)
print("Weibull plan: c =", round(c_fit, 1), " fitted m =", round(m_fit, 2))
print(p_wei[["m", "c", "n_up"]])
