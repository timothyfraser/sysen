# slides_lesson_11_ls.py -------------------------------------------------------
# Python twin of slides_lesson_11_ls.R (Lesson 10, "Least squares in five steps").
# Run from the top of the repo:  python functions/slides_lesson_11_ls.py
# Reads:  workshops/mydiamonds.csv (first 12 diamonds)
# Writes: docs-v3/images/slides/lesson-11/gen_ls_py.png; prints b0 and b1 from the five steps.
import pandas as pd
from plotnine import *

d = pd.read_csv("workshops/mydiamonds.csv").head(12)
d = d.rename(columns = {"carat": "x", "price": "y"})[["x", "y"]]

# Steps 1-2: x^2 and xy for each point, then the sums
n, sx, sy = len(d), d.x.sum(), d.y.sum()
sxx, sxy = (d.x**2).sum(), (d.x*d.y).sum()
# Step 3: slope;  Step 4: intercept
b1 = (n*sxy - sx*sy) / (n*sxx - sx**2)
b0 = (sy - b1*sx) / n
print(b0, b1)

# Step 5: the line; residual for one point
d["yhat"] = b0 + b1*d.x
d["e"] = d.y - d.yhat
pt = d.loc[[d.e.abs().idxmax()]]

g = (ggplot(d, aes(x = "x", y = "y")) +
  geom_abline(intercept = b0, slope = b1, color = "#b31b1b", size = 1.2) +
  geom_segment(data = pt, mapping = aes(xend = "x", yend = "yhat"), linetype = "dashed", color = "#373737") +
  geom_point(size = 4, color = "#2a5d9f") +
  geom_point(data = pt, mapping = aes(y = "yhat"), size = 4, fill = "#f2c14e", color = "#373737") +
  annotate("text", x = float(pt.x.iloc[0]) - 0.04, y = float((pt.y + pt.yhat).iloc[0] / 2), ha = "right", size = 13,
           label = "residual e = y - y-hat") +
  annotate("text", x = d.x.min(), y = d.y.max(), ha = "left", va = "top", size = 14, color = "#b31b1b",
           label = "y-hat = %.0f + %.0f x" % (b0, b1)) +
  labs(x = "carat (x)", y = "price (y)") +
  theme_classic(base_size = 16))
g.save("docs-v3/images/slides/lesson-11/gen_ls_py.png", width = 6.5, height = 4.5, dpi = 200, verbose = False)
