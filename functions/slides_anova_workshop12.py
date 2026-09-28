# slides_anova_workshop12.py -- Python twin of slides_anova_workshop12.R
# Run from the top of the repo:  python functions/slides_anova_workshop12.py
# Reads workshops/anova_coagulation.csv and workshops/anova_latin_square.csv
# (written by the R script) and prints every number shown on the slides.
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from plotnine import *

coag = pd.read_csv("workshops/anova_coagulation.csv")
grand = coag.time.mean()
g = coag.groupby("diet").time.agg(["count", "mean"])
g["diff"] = g["mean"] - grand
print(g)
m = smf.ols("time ~ C(diet)", data=coag).fit()
print(sm.stats.anova_lm(m, typ=1))

p = (ggplot(coag, aes(x="time", y="diet")) + geom_vline(xintercept=grand, linetype="dashed")
     + geom_point(size=4, alpha=0.8, color="#B31B1B") + theme_minimal())
p.save("/tmp/coag_dotplot_py.png", width=6, height=4, dpi=150, verbose=False)

ls = pd.read_csv("workshops/anova_latin_square.csv")
print("Grand average:", ls.y.mean())
for v in ["car", "driver", "additive"]:
    print(ls.groupby(v).y.mean())
m2 = smf.ols("y ~ C(car) + C(driver) + C(additive)", data=ls).fit()
print(sm.stats.anova_lm(m2, typ=1))
