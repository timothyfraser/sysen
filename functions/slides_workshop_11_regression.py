# slides_workshop_11_regression.py -- Python twin of slides_workshop_11_regression.R
# Run from the repo root. Data: workshops/jp_matching_experiment.csv
import pandas as pd
import statsmodels.formula.api as smf
from plotnine import *

out = "docs-v3/images/slides/workshop-11/"

cities = pd.read_csv("workshops/jp_matching_experiment.csv")
# Treat year and pref as categories; Not Hit is the baseline
cities["year"] = cities["year"].astype("category")
cities["pref"] = cities["pref"].astype("category")
cities["by_tsunami"] = pd.Categorical(cities["by_tsunami"], categories=["Not Hit", "Hit"], ordered=True)

# lm() -> smf.ols(...).fit()
m = smf.ols("social_capital ~ damage_rate", data=cities).fit()
print(m.params.round(4))  # 0.3942 + 0.0749 * damage_rate

g = (ggplot(cities, aes("damage_rate", "social_capital"))
     + geom_point(aes(fill="by_tsunami"), shape="o", size=2.6, alpha=.75, color="#2a1414")
     + geom_smooth(method="lm", color="#B31B1B", fill="#d08080", size=1.6)
     + scale_fill_manual(values={"Not Hit": "#a0c0f0", "Hit": "#f0b068"}, name="")
     + labs(title="As X increases, what happens to Y?", x="Damage rate (X)", y="Social capital (Y)")
     + theme_classic(base_size=14) + theme(legend_position="top", figure_size=(7.5, 5.2)))
g.save(out + "gen_regression_py.png", dpi=110, verbose=False)
