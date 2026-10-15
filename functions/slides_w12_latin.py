# slides_w12_latin.py -- Python twin of slides_w12_latin.R
# Feeds: Workshop 12 slides "Using 2 Types of Blocks: Air Pollution" and
#   "Hyper-Graeco Latin Squares: Martindale Wear Tester"
#   (Box, Hunter & Hunter, Statistics for Experimenters, Tables 4.9-4.12).
# Run from the top of the repo:  python functions/slides_w12_latin.py
# Reads workshops/anova_latin_square.csv and workshops/anova_martindale.csv and
# prints every number shown on those slides (the R script draws the chart).
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

pd.set_option("display.width", 120)

# 1. Latin square: 4 drivers x 4 cars x 4 additives -----------------------------
ls = pd.read_csv("workshops/anova_latin_square.csv")
ls["driver"] = pd.Categorical(ls["driver"], ["I", "II", "III", "IV"])
ls = ls.sort_values(["driver", "car"]).reset_index(drop=True)
grand = ls.y.mean()
print("Latin square grand average =", grand)
for v in ["car", "driver", "additive"]:
    print(ls.groupby(v, observed=True).y.mean())

dv = ls.copy()   # deviations live in their own frame (a column named C would shadow patsy's C())
dv["V"] = dv.y - grand
dv["C"] = dv.groupby("car").y.transform("mean") - grand
dv["D"] = dv.groupby("driver", observed=True).y.transform("mean") - grand
dv["T"] = dv.groupby("additive").y.transform("mean") - grand
dv["R"] = dv["V"] - dv["C"] - dv["D"] - dv["T"]
for k in ["V", "C", "D", "T", "R"]:
    print(f"\n{k} (rows = drivers I-IV, cols = cars 1-4)")
    print(dv[k].to_numpy().reshape(4, 4).astype(int))
print("\nSum of squares:", {k: float((dv[k] ** 2).sum()) for k in ["V", "C", "D", "T", "R"]})

m1 = smf.ols("y ~ C(car) + C(driver) + C(additive)", data=ls).fit()
a1 = sm.stats.anova_lm(m1, typ=1)
print("\nLatin square ANOVA")
print(a1.round(4))

# 2. Martindale wear tester ---------------------------------------------------------
m = pd.read_csv("workshops/anova_martindale.csv")
mg = m.wear.mean()
print("\nMartindale: n =", len(m), " grand average =", round(mg, 1))
r1 = lambda x: np.floor(x * 10 + 0.5) / 10   # the book rounds halves up (307.25 -> 307.3)
for v in ["treatment", "holder", "position", "emery", "cycle", "replicate"]:
    print({k: f"{r1(x):.1f}" for k, x in m.groupby(v).wear.mean().items()})

# Cycle is nested in replicate and emery papers alpha-delta only occur in Replicate I
# (epsilon-kappa in II), so some dummy columns are aliased. R's aov() drops them
# automatically; statsmodels' anova_lm does not, so we compute the sequential
# (type I) sums of squares ourselves: the drop in RSS as each term enters, with the
# degrees of freedom = the rank gained. Same order as the R script.
terms = ["replicate", "cycle", "position", "emery", "holder", "treatment"]
rows, prev_rss, prev_rank, used = [], ((m.wear - mg) ** 2).sum(), 1, []
for t in terms:
    used.append(f"C({t})")
    fit = smf.ols("wear ~ " + " + ".join(used), data=m).fit()
    rank = np.linalg.matrix_rank(fit.model.exog)
    rows.append((t, rank - prev_rank, prev_rss - fit.ssr))
    prev_rss, prev_rank = fit.ssr, rank
dfR = len(m) - prev_rank
a2 = pd.DataFrame(rows + [("residual", dfR, prev_rss)], columns=["term", "df", "sum_sq"]).set_index("term")
a2["mean_sq"] = a2.sum_sq / a2.df
a2["ratio_to_m_R"] = a2.mean_sq / a2.loc["residual", "mean_sq"]
a2["F"] = a2.ratio_to_m_R
from scipy import stats
a2["PR(>F)"] = 1 - stats.f.cdf(a2["F"], a2.df, dfR)
a2.loc["residual", ["F", "PR(>F)", "ratio_to_m_R"]] = np.nan
print("\nMartindale ANOVA")
print(a2.round(2))
print("Total df =", int(a2.df.sum()) - 0, " total SS =", round(a2.sum_sq.sum(), 2))
print("Exact residual SS =", round(a2.loc["residual", "sum_sq"], 4))
print("F for treatments =", round(a2.loc["treatment", "F"], 2),
      "on", int(a2.loc["treatment", "df"]), "and", int(dfR), "df, p =",
      round(a2.loc["treatment", "PR(>F)"], 3))

# Graphical ANOVA dots: (level average - grand average) * sqrt(nu_R / nu_factor)
nuR = a2.loc["residual", "df"]
for f, v in [("Replicates", "replicate"), ("Cycles", "cycle"), ("Emery papers", "emery"),
             ("Positions", "position"), ("Holders", "holder"), ("Treatments", "treatment")]:
    nu = a2.loc[v, "df"]
    dots = ((m.groupby(v).wear.mean() - mg) * np.sqrt(nuR / nu)).round(1)
    print(f, dots.to_dict())
