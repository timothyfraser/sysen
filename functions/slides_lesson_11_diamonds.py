# slides_lesson_11_diamonds.py -------------------------------------------------
# Python twin of slides_lesson_11_diamonds.R: the same coefficient table.
# Run from the top of the repo:  python functions/slides_lesson_11_diamonds.py
# Reads:  workshops/mydiamonds.csv (1,000 diamonds: price, carat, cut)
import pandas as pd
import statsmodels.formula.api as smf

mydiamonds = pd.read_csv("workshops/mydiamonds.csv")

# Read ~ as "explained by"
m = smf.ols(formula = "price ~ carat", data = mydiamonds).fit()

# One row per coefficient: estimate, standard error, t statistic, p-value
coefs = pd.DataFrame({"estimate": m.params, "std.error": m.bse,
                      "statistic": m.tvalues, "p.value": m.pvalues})
print(coefs)
