# slides_workshop_11_rsm.py -- Python twin of slides_workshop_11_rsm.R
# Run from the repo root, AFTER the R script (it checks its numbers against R's CSVs).
# Data: workshops/gingerbread_test1.csv
import pandas as pd
import statsmodels.formula.api as smf

cookies = pd.read_csv("workshops/gingerbread_test1.csv")

# Exercise 1 -- interaction model, predicted at every tested recipe
m2 = smf.ols("yum ~ molasses * ginger", data=cookies).fit()
grid = pd.MultiIndex.from_product(
    [[0.5, 0.75, 1, 1.25], [0.5, 1, 1.5, 2]],
    names=["molasses", "ginger"]).to_frame(index=False)
grid["yhat"] = m2.predict(grid)
print(grid.nlargest(1, "yhat"))

# Exercise 2 -- second-order model, a new recipe that was never tested
m3 = smf.ols("yum ~ molasses * ginger + I(molasses**2) + I(ginger**2)", data=cookies).fit()
new = pd.DataFrame({"molasses": [1.1], "ginger": [1.3]})
ci = m3.get_prediction(new).summary_frame(alpha=0.05)
print(ci[["mean", "mean_ci_lower", "mean_ci_upper"]])

# Must match R to 0.01
r_grid = pd.read_csv("workshops/slides_workshop_11_rsm_grid.csv")
r_ci = pd.read_csv("workshops/slides_workshop_11_rsm_ci.csv")
assert (grid["yhat"] - r_grid["yhat"]).abs().max() < 0.01, "grid differs from R"
for py, r in [("mean", "fit"), ("mean_ci_lower", "lwr"), ("mean_ci_upper", "upr")]:
    assert abs(ci[py].iloc[0] - r_ci[r].iloc[0]) < 0.01, f"{py} differs from R"
print("Python matches R to 0.01")
