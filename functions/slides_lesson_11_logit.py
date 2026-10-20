# slides_lesson_11_logit.py
# Lesson 10 Appendix: binary logistic regression, rebuilt on the course diamonds data.
# Is a diamond above the median price? P(expensive) ~ carat, with an odds-ratio reading.
# Run from the repo root: python functions/slides_lesson_11_logit.py

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

mydiamonds = pd.read_csv("workshops/mydiamonds.csv")

# 1 if the diamond costs more than the median price, else 0
med = mydiamonds.price.median()
mydiamonds["expensive"] = (mydiamonds.price > med).astype(int)

# Logistic regression: log-odds linear in carat
m = smf.logit("expensive ~ carat",
              data = mydiamonds).fit(disp = 0)
print(m.params)
# Odds ratio for +0.1 carat: exp(beta x 0.1)
print(np.exp(m.params["carat"] * 0.1))
