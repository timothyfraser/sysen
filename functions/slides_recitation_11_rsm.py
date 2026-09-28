# slides_recitation_11_rsm.py -- Python twin of slides_recitation_11_rsm.R
# Run from the repo root. Data: workshops/gingerbread_test1.csv, workshops/recitation11_textile.csv
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from plotnine import *

out = "docs-v3/images/slides/recitation-11/"

# ---- Gingerbread ----
cookies = pd.read_csv("workshops/gingerbread_test1.csv")
m3 = smf.ols("yum ~ molasses * ginger + I(molasses**2) + I(ginger**2)", data=cookies).fit()
print(m3.params.round(2)); print(round(m3.rsquared, 3))

mm, gg = np.meshgrid(np.linspace(0.75, 1.5, 100), np.linspace(0.5, 2, 100))
grid = pd.DataFrame({"molasses": mm.ravel(), "ginger": gg.ravel()})
grid["yum"] = m3.predict(grid)
grid["band"] = (grid["yum"] // 5) * 5
best = grid.loc[[grid["yum"].idxmax()]]
print(best)

g1 = (ggplot(grid, aes("molasses", "ginger"))
      + geom_tile(aes(fill="band"))  # plotnine has no geom_contour: 5-point yum bands instead
      + geom_point(data=best, mapping=aes("molasses", "ginger"), size=4, color="black", inherit_aes=False)
      + scale_fill_cmap("plasma", name="Predicted\nYum Factor")
      + labs(title="Predicted yum, inside the tested range (dot = predicted best)",
             x="Molasses (cups)", y="Ginger (tablespoons)")
      + theme_minimal(base_size=14) + theme(figure_size=(9, 5.6)))
g1.save(out + "gen_contour_yum_py.png", dpi=110, verbose=False)

# ---- Textiles ----
d = pd.read_csv("workshops/recitation11_textile.csv")
print(d.y.max() / d.y.min())
m1 = smf.ols("y ~ length + amplitude + load + I(length**2) + I(amplitude**2) + I(load**2)"
             " + length:amplitude + amplitude:load + length:load", data=d).fit()
m2 = smf.ols("np.log(y) ~ length + amplitude + load", data=d).fit()
m3t = smf.ols("np.log(y) ~ np.log(length) + np.log(amplitude) + np.log(load)", data=d).fit()
k = np.exp(np.mean(np.log(d.y) - 5*np.log(d.length/d.amplitude) + 3*np.log(d.load)))
d["M1"] = m1.fittedvalues
d["M2"] = np.exp(m2.fittedvalues)
d["M3"] = np.exp(m3t.fittedvalues)
d["M4"] = k * (d.length/d.amplitude)**5.0 * d.load**-3.0

rows = []
for m, df_, p in [("M1", 17, 10), ("M2", 23, 4), ("M3", 23, 4), ("M4", 23, 4)]:
    rss = ((d.y - d[m])**2).sum()
    rows.append({"model": m, "rss_e3": rss/1000, "df": df_, "ms": rss/df_/1000, "p": p,
                 "avgvar": rss/df_/1000*p/27})
print(pd.DataFrame(rows).round(1))

long = d.assign(run=range(1, 28)).melt(id_vars=["run", "y"], value_vars=["M1", "M2", "M3", "M4"],
                                       var_name="model", value_name="pred")
g2 = (ggplot(long, aes("y", "pred"))
      + geom_abline(slope=1, intercept=0, color="grey")
      + geom_point(size=2.5, color="#0b5cad")
      + facet_wrap("~model", nrow=1)
      + scale_x_log10() + scale_y_log10()
      + labs(title="Predicted vs observed lifetime, 27 textile runs (log axes)",
             x="Observed lifetime y (cycles)", y="Predicted")
      + theme_minimal(base_size=14) + theme(figure_size=(11, 4.6)))
g2.save(out + "gen_textile_fit_py.png", dpi=110, verbose=False)
