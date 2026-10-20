# slides_lesson_7b_bins.py -- Python twin of slides_lesson_7b_bins.R (pandas + plotnine)
# Run from the repo root:  python functions/slides_lesson_7b_bins.py
import numpy as np
import pandas as pd
from scipy.stats import chi2
from plotnine import *

bulbs = pd.read_csv("workshops/bulb_lifetimes.csv")

# 1. Cross-tabulate into equal intervals
def tab(width, upper):
    breaks = list(range(0, upper + 1, width)) + [np.inf]
    out = (pd.cut(bulbs["days"], bins=breaks, labels=False) + 1).value_counts().reindex(range(1, len(breaks)), fill_value=0).sort_index()  # keep empty intervals
    out = out.rename_axis("bin").reset_index(name="r")
    out["bin_size"] = width
    out["lower"] = (out["bin"] - 1) * width
    out["upper"] = np.where(out["bin"] * width > upper, np.nan, out["bin"] * width)
    out["mid"] = out["lower"] + width / 2
    return out
bins = pd.concat([tab(55, 550), tab(110, 330), tab(100, 400)])[["bin_size", "bin", "lower", "upper", "r", "mid"]]
print(bins.to_string(index=False))

# 2. lambda-hat, complete sample
r, total = len(bulbs), bulbs["days"].sum()
print("complete sample: r =", r, " total =", total, " lambda-hat =", round(r / total, 5))

# 3. lambda-hat, 100-hour cross-tab
b100 = bins[bins["bin_size"] == 100].reset_index(drop=True)
t_sum = (b100["mid"] * b100["r"]).sum()
lam = b100["r"].sum() / t_sum
print("cross-tab: r =", b100["r"].sum(), " t_sum =", t_sum, " lambda-hat =", round(lam, 5))

# 4. Expected counts and chi-squared
edges = np.array([0, 100, 200, 300, 400, 500])
cdf = 1 - np.exp(-lam * edges)
p_exp = np.diff(cdf)
r_exp = p_exp * 100
terms = (b100["r"] - r_exp) ** 2 / r_exp
chisq = terms.sum()
df_ = len(b100) - 1 - 1
print("chi-squared =", round(chisq, 2), " df =", df_, " critical (95%) =", round(chi2.ppf(0.95, df_), 2),
      " p =", float(f"{chi2.sf(chisq, df_):.3g}"))

# 5. Figure
x = np.linspace(0, 900, 300)
curve = pd.DataFrame({"days": x, "d": 0.0074 * np.exp(-0.0074 * x)})
g = (ggplot(bulbs, aes("days"))
     + geom_histogram(aes(y=after_stat("density")), binwidth=55, boundary=0, fill="#B31B1B", color="white", alpha=0.9)
     + geom_line(curve, aes("days", "d"), size=1.4, color="#302050")
     + labs(x="days to failure", y="density")
     + theme_minimal(base_size=24) + theme(figure_size=(7.5, 4.6)))
g.save("docs-v3/images/slides/lesson-7b/gen_bulb_hist_exp_py.png", dpi=100, verbose=False)

# 6. Figure: observed vs expected counts, 100-hour intervals
# observed = carnelian bars; expected = navy outlined bars (exp. model at lambda-hat)
labels = ["0-100", "101-200", "201-300", "301-400", "401+"]
ov = pd.DataFrame({"interval": pd.Categorical(labels, categories=labels, ordered=True),
                   "r": b100["r"].values, "r_exp": r_exp})
g2 = (ggplot(ov, aes(x="interval"))
      + geom_col(aes(y="r"), fill="#B31B1B", width=0.8, alpha=0.9)
      + geom_col(aes(y="r_exp"), fill="none", color="#302050", size=1.6, width=0.8)
      + labs(x="interval (hours)", y="failures")
      + theme_minimal(base_size=24) + theme(figure_size=(7, 4.6)))
g2.save("docs-v3/images/slides/lesson-7b/gen_obs_exp_py.png", dpi=100, verbose=False)
