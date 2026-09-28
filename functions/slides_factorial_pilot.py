# slides_factorial_pilot.py --------------------------------------------------
# Python twin of slides_factorial_pilot.R (Lesson 13 / Workshop 13 slides).
# Run from the top of the repo:  python functions/slides_factorial_pilot.py
# Reads:  workshops/lattes.csv
# Writes: docs-v3/images/slides/lesson-13/gen_effects_lattes_py.png; prints outputs.
import pandas as pd
import itertools
import statsmodels.formula.api as smf
from plotnine import *

# Example 1
grid = pd.DataFrame(itertools.product(["A", "B"], [20, 40], [160, 180]),
                    columns=["k", "c", "t"])
grid["run"] = range(1, len(grid) + 1)
grid = grid[["run", "t", "c", "k"]]
data = grid.assign(y=[60, 72, 54, 68, 52, 83, 45, 80])
print(data.to_string(index=False))

# Example 2
d, y = data, data["y"]
print(pd.DataFrame({
  "dbar_c": [(y[d.c == 40].values - y[d.c == 20].values).mean()],
  "dbar_t": [(y[d.t == 180].values - y[d.t == 160].values).mean()],
  "dbar_k": [(y[d.k == "B"].values - y[d.k == "A"].values).mean()]}))

# Example 3
xbar1 = y[((d.t == 180) & (d.k == "B")) | ((d.t == 160) & (d.k == "A"))].mean()
xbar0 = y[((d.t == 160) & (d.k == "B")) | ((d.t == 180) & (d.k == "A"))].mean()
print(pd.DataFrame({"xbar1": [xbar1], "xbar0": [xbar0], "dbar": [xbar1 - xbar0]}))

# Example 4
def at(t, k, c):
  return y[(d.t == t) & (d.k == k) & (d.c == c)].iat[0]
d1a = at(180, "A", 40) - at(160, "A", 40)
d0a = at(180, "A", 20) - at(160, "A", 20)
dbar_a = (d1a - d0a) / 2
d1b = at(180, "B", 40) - at(160, "B", 40)
d0b = at(180, "B", 20) - at(160, "B", 20)
dbar_b = (d1b - d0b) / 2
dbar = (dbar_b - dbar_a) / 2
print(pd.DataFrame({"d1a": [d1a], "d0a": [d0a], "dbar_a": [dbar_a],
                    "d1b": [d1b], "d0b": [d0b], "dbar_b": [dbar_b], "dbar": [dbar]}))

# Effects table
coded = data.assign(T=(data.t == 180) * 2 - 1, C=(data.c == 40) * 2 - 1,
                    K=(data.k == "B") * 2 - 1)
m = smf.ols("y ~ T*C*K", data=coded).fit()
print((2 * m.params.drop("Intercept")).round(2))

# Lattes chart
lattes = pd.read_csv("workshops/lattes.csv")
def eff(v, hi, lo):
  return lattes.tastiness[lattes[v] == hi].mean() - lattes.tastiness[lattes[v] == lo].mean()
dd = pd.DataFrame({"effect": ["Syrup: Torani - Monin", "Machine: B - A", "Art: heart - foam"],
                   "dbar": [eff("syrup", "torani", "monin"), eff("machine", "b", "a"),
                            eff("art", "heart", "foamy")]})
print(dd.round(2))
dd["effect"] = pd.Categorical(dd.effect, categories=dd.sort_values("dbar").effect)
dd["pos"] = dd.dbar > 0
g = (ggplot(dd, aes(x="dbar", y="effect", fill="pos")) + geom_col(width=0.6) +
     geom_vline(xintercept=0) +
     scale_fill_manual(values={True: "#B31B1B", False: "#5b6b7a"}, guide=None) +
     labs(x="Difference in mean tastiness", y="", title="Direct effects, lattes experiment") +
     theme_minimal(base_size=16))
g.save("docs-v3/images/slides/lesson-13/gen_effects_lattes_py.png", width=7, height=3.6, dpi=150, verbose=False)
