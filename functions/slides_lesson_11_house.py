# slides_lesson_11_house.py ----------------------------------------------------
# Feeds: Lesson 10 slides, "What is Regression?" (house price in Ithaca).
# Run from the top of the repo:  python functions/slides_lesson_11_house.py
# Reads:  workshops/ithaca_houses.csv (3 houses: square footage and price)
# Writes: docs-v3/images/slides/lesson-11/gen_house_line_py.png; prints the fit
#   and the predicted price of a 1,770 sqft house.
import pandas as pd
import statsmodels.formula.api as smf
from plotnine import *

houses = pd.read_csv("workshops/ithaca_houses.csv")

# Least squares line through the three houses
m = smf.ols("price ~ sqft", data = houses).fit()
print(m.params)

# What should a 1,770 sqft house cost?
newhouse = pd.DataFrame({"sqft": [1770]})
newhouse["price"] = m.predict(newhouse)
print(newhouse)

line = pd.DataFrame({"sqft": [0, 3000]})
line["price"] = m.predict(line)
houses["label"] = ["$" + format(p, ",") for p in houses["price"]]

g = (ggplot(houses, aes(x = "sqft", y = "price")) +
  geom_line(data = line, color = "#2a5d9f", size = 1.2) +
  geom_point(size = 5, color = "#b31b1b") +
  geom_point(data = newhouse, size = 6, fill = "#f2c14e", color = "#373737", stroke = 1.2) +
  geom_text(aes(label = "label"), nudge_y = 45000, size = 12) +
  annotate("text", x = 1880, y = newhouse["price"][0] - 70000, ha = "left", label = "1,770 sqft: ?", size = 12) +
  scale_x_continuous(limits = (0, 3000)) +
  scale_y_continuous(limits = (0, 700000)) +
  labs(x = "Area (sqft)", y = "Price") +
  theme_classic(base_size = 16))

g.save("docs-v3/images/slides/lesson-11/gen_house_line_py.png", width = 5.2, height = 3.1, dpi = 200, verbose = False)
