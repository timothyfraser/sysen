# slides_w12_anova.py -- Python twin of slides_w12_anova.R
# Run from the top of the repo:  python functions/slides_w12_anova.py
# Reads workshops/anova_coagulation.csv (diet, time, order) and workshops/donuts.csv
# and prints every number shown on the Workshop 12 slides for the Blood
# Coagulation case study (Box, Hunter & Hunter) and Examples 5 and 6 (donuts).
# The R script is the chart of record; this one reproduces the numbers.
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

# 1. Coagulation: averages, deviations, decomposition --------------------------
coag = pd.read_csv("workshops/anova_coagulation.csv")
grand = coag.time.mean()
avgs = coag.groupby("diet").time.agg(n="count", mean="mean")
avgs["diff"] = avgs["mean"] - grand
print("== Treatment averages, grand average, differences ==")
print(avgs)
print("Grand average:", grand)

# rows = observation 1-6, columns = diets A-D
Y = np.column_stack([coag.time[coag.diet == d].to_numpy() for d in "ABCD"])
D = Y - grand
T = np.tile(avgs["mean"].to_numpy() - grand, (6, 1))
R = D - T
for name, M in [("Y", Y), ("D = Y - 64", D), ("T", T), ("R = D - T", R)]:
    print(f"\n== {name} ==")
    print(M.astype(int))
print("\nSS: D =", (D**2).sum(), " T =", (T**2).sum(), " R =", (R**2).sum())
print("df: D =", 23, " T =", 3, " R =", 20)
print("m_T =", (T**2).sum() / 3, " m_R =", (R**2).sum() / 20,
      " F =", ((T**2).sum() / 3) / ((R**2).sum() / 20))

# 2. The ANOVA and the F(3, 20) points ------------------------------------------
m = smf.ols("time ~ C(diet)", data=coag).fit()
print("\n== anova_lm(time ~ C(diet)) ==")
print(sm.stats.anova_lm(m, typ=1))
q = stats.f.ppf([.95, .99, .999], 3, 20)
print("\n== F(3, 20) points: 5%, 1%, 0.1% ==")
print(q, q.round(2))

# 3. Example 5: donuts, lm() route and aov() route -------------------------------
donuts = pd.read_csv("workshops/donuts.csv")
m = smf.ols("weight ~ baker", data=donuts).fit()
print("\n== Example 5: sigma, statistic, p.value, df ==")
print(m.mse_resid ** 0.5, m.fvalue, m.f_pvalue, m.df_model)
print("\n== Example 5: anova_lm ==")
print(sm.stats.anova_lm(m, typ=2))

# 4. Example 6: Bartlett's K^2 and Welch's ANOVA ---------------------------------
g = [d["weight"].to_numpy() for _, d in donuts.groupby("baker")]
print("\n== Example 6: Bartlett ==")
print(stats.bartlett(*g))
n = np.array([len(x) for x in g])
mu = np.array([x.mean() for x in g])
w = n / np.array([x.var(ddof=1) for x in g])
mw = (w * mu).sum() / w.sum()
k = len(g)
lam = ((1 - w / w.sum())**2 / (n - 1)).sum()
num = (w * (mu - mw)**2).sum() / (k - 1)
stat = num / (1 + 2 * (k - 2) / (k**2 - 1) * lam)
df2 = 1 / (3 / (k**2 - 1) * lam)
print("\n== Example 6: Welch's ANOVA (num.df, den.df, statistic, p.value) ==")
print(k - 1, df2, stat, stats.f.sf(stat, k - 1, df2))
