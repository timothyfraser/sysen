# slides_factorial_pilot.py --------------------------------------------------
# Python twin of slides_factorial_pilot.R (Lesson 13 / Workshop 13 slides).
# Run from the top of the repo:  python functions/slides_factorial_pilot.py
# Reads:  workshops/lattes.csv
# Writes: docs-v3/images/slides/lesson-13/gen_effects_lattes_py.png (effects plot:
#   one box per effect, "estimate (SE)"); prints outputs.
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
# Effects plot (Tim's 2025 form): one labelled box per effect at its estimate.
# Coded +/-1 factors; effect = 2 x coefficient, SE = 2 x SE(coef).
lc = lattes.assign(S=(lattes.syrup == "torani") * 2 - 1, M=(lattes.machine == "b") * 2 - 1,
                   A=(lattes.art == "heart") * 2 - 1)
ml = smf.ols("tastiness ~ S * M * A", data=lc).fit()
names = {"S": "Syrup", "M": "Machine", "A": "Art", "S:M": "S x M",
         "S:A": "S x A", "M:A": "M x A", "S:M:A": "S x M x A"}
fx = pd.DataFrame({"term": list(names)})
fx["estimate"] = [2 * ml.params[t] for t in fx.term]
fx["se"] = [2 * ml.bse[t] for t in fx.term]
fx["effect"] = pd.Categorical([names[t] for t in fx.term],
                              categories=[names[t] for t in reversed(list(names))])
fx["label"] = [f"{e:.1f} ({s:.1f})" for e, s in zip(fx.estimate, fx.se)]
print(fx[["effect", "estimate", "se", "label"]].round(2).to_string(index=False))
lim = fx.estimate.abs().max()
span = fx.estimate.max() - fx.estimate.min()
g = (ggplot(fx, aes(x="estimate", y="effect")) +
     geom_vline(xintercept=0, color="#1f1f1f", size=0.8) +
     geom_label(aes(label="label", fill="estimate"), size=15, fontweight="bold",
                color="#1f1f1f", label_padding=0.35) +
     scale_fill_gradient2(low="#3880c0", mid="#ffffff", high="#B31B1B", midpoint=0,
                          limits=(-lim, lim), name="Effect") +
     scale_x_continuous(limits=(fx.estimate.min() - 17, fx.estimate.max() + 17)) +
     labs(x="Effect on tastiness", y="") +
     theme_minimal(base_size=20) +
     theme(axis_text=element_text(size=16, color="#1f1f1f"), panel_grid_minor=element_blank(),
           legend_title=element_text(size=16), legend_text=element_text(size=14),
           legend_key_height=150))
g.save("docs-v3/images/slides/lesson-13/gen_effects_lattes_py.png", width=7, height=3.6, dpi=150, verbose=False)
