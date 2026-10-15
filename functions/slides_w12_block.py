# slides_w12_block.py -------------------------------------------------------
#
# Python twin of slides_w12_block.R. Feeds: Workshop 12 (ANOVA & Latin Squares)
#   slides "Randomized Block Design" and "Randomized Block Design (2)" (the
#   penicillin experiment, Box, Hunter & Hunter).
# Run from the top of the repo:
#   python -X utf8 -P functions/slides_w12_block.py
# Reads:  workshops/anova_penicillin.csv  (blend, treatment, order, yield)
# Prints: block and treatment averages, the decomposition matrices, the sums
#         of squares and the ANOVA table (the R script draws the charts).

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

pen = pd.read_csv("workshops/anova_penicillin.csv")
assert len(pen) == 20

grand = pen["yield"].mean()
pen["bavg"] = pen.groupby("blend")["yield"].transform("mean")
pen["tavg"] = pen.groupby("treatment")["yield"].transform("mean")
pen["dev"] = pen["yield"] - grand
pen["bdev"] = pen["bavg"] - grand
pen["tdev"] = pen["tavg"] - grand
pen["resid"] = pen["yield"] - pen["bavg"] - pen["tavg"] + grand
pen["fitted"] = pen["yield"] - pen["resid"]

print("Grand average:", grand)
print("\nBlock averages and deviations")
print(pen.groupby("blend")[["bavg", "bdev"]].first())
print("\nTreatment averages and deviations")
print(pen.groupby("treatment")[["tavg", "tdev"]].first())

# rows = blends 1-5, columns = treatments A-D
def mat(col):
    return pen.pivot(index="blend", columns="treatment", values=col).astype(int)

labels = [("yield", "Observations y_bt"),
          ("dev", "Deviations from grand average y_bt - ybar"),
          ("bdev", "Block deviations ybar_b - ybar"),
          ("tdev", "Treatment deviations ybar_t - ybar"),
          ("resid", "Residuals y_bt - ybar_b - ybar_t + ybar")]
for col, label in labels:
    print("\n" + label)
    print(mat(col))

SD, SB, ST, SR = [(pen[c] ** 2).sum() for c in ("dev", "bdev", "tdev", "resid")]
print(f"\nVector sums of squares: S_D = {SD:.0f}  S_B = {SB:.0f}  S_T = {ST:.0f}  S_R = {SR:.0f}")
print(f"  check S_D = S_B + S_T + S_R: {SD:.0f} = {SB + ST + SR:.0f}")
print("Degrees of freedom: nu_D = 19, nu_B = 4, nu_T = 3, nu_R = 12  (19 = 4 + 3 + 12)")

# "yield" is a Python keyword, so patsy needs Q() around the column name
fit = smf.ols("Q('yield') ~ C(blend) + C(treatment)", data=pen).fit()
tab = anova_lm(fit)
tab["mean_sq"] = tab["sum_sq"] / tab["df"]
print("\nanova_lm(smf.ols(\"Q('yield') ~ C(blend) + C(treatment)\", data=pen).fit())")
print(tab.round(4))
mB, mT, mR = tab["mean_sq"].iloc[:3]
print(f"\nMean squares: m_B = {mB:.1f}  m_T = {mT:.1f}  m_R = {mR:.1f}")
print(f"F ratios (exact): F_4,12 = {tab['F'].iloc[0]:.3f}  F_3,12 = {tab['F'].iloc[1]:.3f}")
print(f"F ratios from rounded mean squares (textbook): F_4,12 = {66.0 / 18.8:.2f}  F_3,12 = {23.3 / 18.8:.2f}")
print(f"p-values: blocks = {tab['PR(>F)'].iloc[0]:.4f}  treatments = {tab['PR(>F)'].iloc[1]:.4f}")

assert (SD, SB, ST, SR) == (560, 264, 70, 226)
assert round(mB, 1) == 66.0 and round(mT, 1) == 23.3 and round(mR, 1) == 18.8
