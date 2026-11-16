# slides_lesson_9_fit.py -- Python twin of slides_lesson_9_fit.R
# Table and figure for the Lesson 9 "Does It Fit?" slides. Run from the sigma repo root.
# Writes docs-v3/images/slides/lesson-9/gen_fit_observed_expected_py.png
import sys
sys.path.insert(0, "functions")
import numpy as np
import pandas as pd
from plotnine import *
from functions_mle import get_fit, get_expected
from functions_planning import plan_test

out = "docs-v3/images/slides/lesson-9"
red = "#B31B1B"

chips = pd.read_csv("workshops/chips.csv")

# 1. The table: one call, four distributions
fit = get_fit(data=chips, n_total=200, tmax=1500)
print(fit[["dist", "chisq", "df", "p_value", "loglik"]].round(4))

# 2. Expected chips per cell, from each fitted distribution
def expected(row):
    params = {row.par1: row.est1}
    if row.par2 is not None and not pd.isna(row.par2):
        params[row.par2] = row.est2
    e = get_expected(chips, n_total=200, dist=row.dist, **params)
    e["dist"] = row.dist
    return e

exp_all = pd.concat([expected(r) for r in fit.itertuples()])
exp_all["cell"] = np.where(np.isinf(exp_all.upper), "1500+",
                           exp_all.lower.astype(int).astype(str) + "-\n" +
                           exp_all.upper.replace(np.inf, 0).astype(int).astype(str))
cells = list(dict.fromkeys(exp_all.cell))
exp_all["cell"] = pd.Categorical(exp_all.cell, cells)
exp_all["dist"] = pd.Categorical(exp_all.dist, list(fit.dist))
obs = exp_all[exp_all.dist == fit.dist.iloc[0]][["cell", "r_obs"]]

cols = {"lognormal": red, "gamma": "#2B2B2B", "weibull": "#D05050", "exponential": "#8C8C8C"}
g = (ggplot() +
     geom_col(data=obs, mapping=aes(x="cell", y="r_obs"), fill="#E8D5D5", width=0.7) +
     geom_line(data=exp_all, mapping=aes(x="cell", y="r_exp", color="dist", group="dist"), size=1.3) +
     geom_point(data=exp_all, mapping=aes(x="cell", y="r_exp", color="dist"), size=3) +
     scale_color_manual(values=cols) +
     labs(x="Hours on test", y="Chips failing in the cell", color="") +
     theme_classic(base_size=20) +
     theme(legend_position="bottom", legend_margin=0, legend_box_spacing=0.03,
           axis_text_x=element_text(size=15)))
g.save(f"{out}/gen_fit_observed_expected_py.png", width=8.4, height=4.7, dpi=170, verbose=False)

# 3. Planning: chips needed for a lognormal life test (sigma must be assumed)
# sigma = 0.811 is the lognormal fit above; the others show how much the answer leans on it
print(plan_test("lognormal", t=250, r=5, ci=0.90, t50=1000,
                sigma=[0.6, 0.8, 0.811, 1.0, 1.2])[["sigma", "n_up"]])
