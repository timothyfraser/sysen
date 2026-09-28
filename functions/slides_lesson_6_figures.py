# Feeds Lesson 6 (process capability) slides 4 and 7-9: capable vs not capable, and the four kinds.
# Run from the sigma repo root:  python3 functions/slides_lesson_6_figures.py
# Writes gen_capable_py.png, gen_not_capable_py.png, gen_four_kinds_py.png to
#   docs-v3/images/slides/lesson-6/ (parity check only). Same parameters as the R script;
#   the random draws differ across languages, which is fine. Seeded for identical reruns.
import numpy as np
import pandas as pd
from scipy.stats import norm
from plotnine import *

np.random.seed(6)
out = "docs-v3/images/slides/lesson-6"
red, band = "#B31B1B", "#E3E3E3"
lsl, usl, nominal = 20, 30, 25

# (a) capable vs not capable: density against the spec band
def plot_capability(sd, file):
    d = pd.DataFrame({"x": np.linspace(12, 38, 800)})
    d["y"] = norm.pdf(d["x"], nominal, sd)
    g = (ggplot(d, aes("x", "y"))
         + annotate("rect", xmin=lsl, xmax=usl, ymin=-np.inf, ymax=np.inf, fill=band)
         + geom_area(d[d["x"] <= lsl], fill=red, alpha=0.55)
         + geom_area(d[d["x"] >= usl], fill=red, alpha=0.55)
         + geom_vline(xintercept=nominal, linetype="dashed", size=0.7)
         + geom_line(color=red, size=1.6)
         + scale_x_continuous(breaks=[lsl, nominal, usl],
                              labels=["LSL\n20", "Nominal\n25", "USL\n30"],
                              limits=(12, 38), expand=(0, 0))
         + scale_y_continuous(expand=(0, 0, 0.04, 0))
         + labs(x="Minutes", y="")
         + theme_classic(base_size=10)
         + theme(axis_text_y=element_blank(), axis_ticks_major_y=element_blank(),
                 axis_line_y=element_blank(), figure_size=(5.5, 3.5), dpi=200))
    g.save(f"{out}/{file}", verbose=False)

plot_capability(1.2, "gen_capable_py.png")
plot_capability(3.5, "gen_not_capable_py.png")

# (b) the four kinds: 12 subgroups x 5 points against the spec band
k, n = 12, 5
kinds = ["Stable and capable", "Stable and incapable",
         "Unstable but potentially capable", "Unstable and incapable"]
t = np.arange(1, k + 1)
params = pd.concat([
    pd.DataFrame({"kind": kinds[0], "t": t, "mu": 25.0, "s": 1.2}),
    pd.DataFrame({"kind": kinds[1], "t": t, "mu": 25.0, "s": 3.5}),
    pd.DataFrame({"kind": kinds[2], "t": t, "mu": np.linspace(19.5, 30.5, k), "s": 1.2}),
    pd.DataFrame({"kind": kinds[3], "t": t, "mu": np.linspace(22, 28, k), "s": np.linspace(2, 5, k)}),
])
pts = params.loc[params.index.repeat(n)].reset_index(drop=True)
pts["y"] = np.random.normal(pts["mu"], pts["s"])
pts["kind"] = pd.Categorical(pts["kind"], categories=kinds)
pts["out"] = ((pts["y"] < lsl) | (pts["y"] > usl)).astype(str)
pts["grp"] = pts["kind"].astype(str) + pts["t"].astype(str)
means = pts.groupby(["kind", "t"], observed=True, as_index=False)["y"].mean()

g = (ggplot(pts, aes("t", "y"))
     + annotate("rect", xmin=-np.inf, xmax=np.inf, ymin=lsl, ymax=usl, fill=band)
     + geom_hline(yintercept=nominal, linetype="dashed", size=0.5)
     + geom_boxplot(aes(group="grp"), width=0.55, color="#595959", fill="none",
                    outlier_shape="", size=0.5)
     + geom_point(aes(color="out"), size=1.6, alpha=0.9)
     + geom_line(means, color=red, size=1)
     + scale_color_manual(values={"False": "#4d4d4d", "True": red}, guide=None)
     + scale_x_continuous(breaks=[1, 6, 12], expand=(0, 0.5))
     + scale_y_continuous(breaks=[lsl, nominal, usl])
     + facet_wrap("kind", ncol=2)
     + labs(x="Subgroup (time)", y="Minutes")
     + theme_classic(base_size=9)
     + theme(strip_text=element_text(size=11, weight="bold"),
             strip_background=element_blank(), figure_size=(8, 5), dpi=200))
g.save(f"{out}/gen_four_kinds_py.png", verbose=False)
