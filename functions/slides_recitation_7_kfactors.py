# Recitation 7 -- k-factor tables and every worked example, recomputed (Python twin).
# Run from the top of the repo:  python functions/slides_recitation_7_kfactors.py
import sys
import numpy as np
import pandas as pd
from scipy.stats import chi2
sys.path.append('functions')
from functions_kfactors import qk

ci = [0.60, 0.80, 0.90, 0.95, 0.975, 0.99, 0.999]
rs = range(1, 42)
def q(p, r, **kw): return float(np.asarray(qk(p = p, r = r, **kw)).ravel()[0])

table3 = pd.DataFrame([dict([("r", r)] + [(f"{c*100:g}%", round(q(c, r, time = True), 2)) for c in ci]) for r in rs])
table4 = pd.DataFrame([dict([("r", r)] + [(f"{c*100:g}%", round(q(1 - c, r), 2)) for c in ci]) for r in rs])
zero = pd.DataFrame({"percentile": [50, 60, 80, 90, 95, 97.5, 99]})
zero["k0"] = (-np.log(1 - zero.percentile / 100)).round(4)
table3.to_csv("workshops/recitation7_k_upper.csv", index = False)
table4.to_csv("workshops/recitation7_k_lower.csv", index = False)
zero.to_csv("workshops/recitation7_zero_failure.csv", index = False)

print("Ex1", [round(q(p, 20, time = True), 4) for p in (0.025, 0.975)], [round(q(p, 20, time = True) * 0.002, 6) for p in (0.025, 0.975)])
print("Ex2", round(q(0.95, 20, time = True), 4), round(q(0.95, 20, time = True) * 0.002, 6))
k3 = chi2.ppf(0.95, 30) / 28 * 14 / 15
print("Ex3", round(chi2.ppf(0.95, 30) / 28, 4), round(k3, 4), round(q(0.95, 15, failure = True), 4), round(k3 * 0.004, 6))
k4 = [q(p, 15, failure = True) for p in (0.025, 0.975)]
print("Ex4", [round(k, 4) for k in k4], [round(k * 0.004, 6) for k in k4])
print("Ex Ex1", round(q(0.80, 13, failure = True), 4), round(q(0.80, 13, failure = True) * 0.0015, 6))
e2 = [q(p, 25, time = True) for p in (0.05, 0.95)]
print("Ex Ex2", [round(k, 4) for k in e2], [round(k * 0.01, 6) for k in e2])
e3a = [q(p, 3, time = True) for p in (0.025, 0.975)]; e3b = [q(p, 3, failure = True) for p in (0.025, 0.975)]
print("Ex Ex3", [round(k * 200, 2) for k in e3a], [round(k * 200, 2) for k in e3b])
nT = 200 * 5000 + 200 * 3000
print("Ex5", nT, [round(-np.log(a) / nT * 1e9, 1) for a in (0.5, 0.05, 0.30)])
k6 = q(0.90, 5, time = True); print("Ex6", round(k6, 3), round(5 * k6 / (5000 * 2e-6), 1))
k7 = q(0.95, 10, time = True); print("Ex7", round(k7, 3), round(10 * k7 / (100 * 5e-5)))
print("Ex8", [round(r * q(0.80, r, time = True), 3) for r in range(1, 5)], 5e-5 * 50 * 2000)
print("Ex9", round(-np.log(0.10) * 40000 / 8000, 2))
print("Ex10", round(-np.log(0.20) / (10000 * 10e-9), 1))
