# slides_lesson_7b_chisq.py -- Python twin of slides_lesson_7b_chisq.R
# Run from the repo root:  python functions/slides_lesson_7b_chisq.py
import pandas as pd
import numpy as np
from scipy.stats import chi2
from plotnine import *

bulbs = pd.read_csv("workshops/bulb_lifetimes.csv")
r = len(bulbs)
total = bulbs["days"].sum()
lambda_hat = r / total
print("r =", r, " total =", total)
print("lambda-hat =", round(lambda_hat, 6), "-> rounded", round(lambda_hat, 4))
print("MTTF = 1/lambda-hat =", round(1 / lambda_hat, 2), "; 1/0.0074 =", round(1 / 0.0074, 2),
      "; sample mean =", bulbs["days"].mean())

cis = [0.90, 0.95, 0.99]
crit = pd.DataFrame({"df": range(1, 11)})
for ci in cis:
    crit[f"ci_{int(ci*100)}"] = chi2.ppf(ci, crit["df"]).round(2)
print(crit)

df_ = 5
cut = chi2.ppf(0.95, df_)
d = pd.DataFrame({"x": np.linspace(0, 25, 500)})
d["y"] = chi2.pdf(d["x"], df_)
g = (ggplot(d, aes("x", "y"))
     + geom_area(data=d[d["x"] >= cut], fill="#B31B1B", alpha=0.8)
     + geom_line(size=1.3)
     + geom_vline(xintercept=cut, linetype="dashed")
     + annotate("text", x=cut + 0.6, y=0.13, ha="left", size=16, label=f"critical value\n= {cut:.2f}")
     + annotate("text", x=5, y=0.022, size=12, label="95% of cases\nby chance")
     + annotate("text", x=cut + 3, y=0.05, ha="left", size=16, color="#B31B1B", label="5% tail:\nsignificant")
     + labs(x="chi-squared statistic (df = 5)", y="density")
     + theme_minimal(base_size=22) + theme(figure_size=(6.2, 4.6)))
g.save("docs-v3/images/slides/lesson-7b/gen_density_df5_py.png", dpi=100, verbose=False)
print("cut =", round(cut, 4))
