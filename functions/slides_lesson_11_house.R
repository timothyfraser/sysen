# slides_lesson_11_house.R -----------------------------------------------------
# Feeds: Lesson 10 slides, "What is Regression?" (house price in Ithaca).
# Run from the top of the repo:  Rscript functions/slides_lesson_11_house.R
# Reads:  workshops/ithaca_houses.csv (3 houses: square footage and price)
# Writes: docs-v3/images/slides/lesson-11/gen_house_line.png; prints the fit
#   and the predicted price of a 1,770 sqft house.
library(dplyr)
library(readr)
library(ggplot2)

houses = read_csv("workshops/ithaca_houses.csv", show_col_types = FALSE)

# Least squares line through the three houses
m = lm(price ~ sqft, data = houses)
print(coef(m))

# What should a 1,770 sqft house cost?
newhouse = tibble(sqft = 1770)
newhouse = newhouse %>% mutate(price = predict(m, newdata = newhouse))
print(newhouse)

g = ggplot(houses, aes(x = sqft, y = price)) +
  geom_smooth(method = "lm", formula = y ~ x, se = FALSE,
              color = "#2a5d9f", linewidth = 1.2, fullrange = TRUE) +
  geom_point(size = 5, color = "#b31b1b") +
  geom_point(data = newhouse, size = 6, shape = 21, fill = "#f2c14e", color = "#373737", stroke = 1.2) +
  geom_text(aes(label = paste0("$", format(price, big.mark = ","))),
            nudge_y = 45000, size = 5) +
  annotate("text", x = 1880, y = newhouse$price - 70000, hjust = 0, label = "1,770 sqft: ?", size = 5) +
  scale_x_continuous(limits = c(0, 3000), labels = scales::comma) +
  scale_y_continuous(limits = c(0, 700000), labels = scales::dollar) +
  labs(x = "Area (sqft)", y = "Price") +
  theme_classic(base_size = 16)

ggsave("docs-v3/images/slides/lesson-11/gen_house_line.png", g,
       width = 5.2, height = 3.1, dpi = 200, bg = "white")
