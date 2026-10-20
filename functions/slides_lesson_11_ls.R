# slides_lesson_11_ls.R --------------------------------------------------------
# Feeds: Lesson 10 slides, "Least squares in five steps".
# Run from the top of the repo:  Rscript functions/slides_lesson_11_ls.R
# Reads:  workshops/mydiamonds.csv (first 12 diamonds)
# Writes: docs-v3/images/slides/lesson-11/gen_ls.png; prints b0 and b1 from the five steps.
library(dplyr)
library(readr)
library(ggplot2)

d = read_csv("workshops/mydiamonds.csv", show_col_types = FALSE) %>%
  slice(1:12) %>% select(x = carat, y = price)

# Steps 1-2: x^2 and xy for each point, then the sums
s = d %>% summarize(n = n(), sx = sum(x), sy = sum(y), sxx = sum(x^2), sxy = sum(x*y))
# Step 3: slope;  Step 4: intercept
b1 = (s$n * s$sxy - s$sx * s$sy) / (s$n * s$sxx - s$sx^2)
b0 = (s$sy - b1 * s$sx) / s$n
print(c(b0 = b0, b1 = b1))
# Same as lm()
print(coef(lm(y ~ x, data = d)))

# Step 5: the line; residual for one point
d = d %>% mutate(yhat = b0 + b1 * x)
pt = d %>% mutate(e = y - yhat) %>% slice_max(abs(e), n = 1)

g = ggplot(d, aes(x = x, y = y)) +
  geom_abline(intercept = b0, slope = b1, color = "#b31b1b", linewidth = 1.2) +
  geom_segment(data = pt, aes(xend = x, yend = yhat), linetype = "dashed", color = "#373737") +
  geom_point(size = 4, color = "#2a5d9f") +
  geom_point(data = pt, aes(y = yhat), size = 4, shape = 21, fill = "#f2c14e", color = "#373737") +
  annotate("text", x = pt$x - 0.04, y = (pt$y + pt$yhat) / 2, hjust = 1, size = 5,
           label = "residual e = y - y-hat") +
  annotate("text", x = min(d$x), y = max(d$y), hjust = 0, vjust = 1, size = 5.5, color = "#b31b1b",
           label = sprintf("y-hat = %.0f + %.0f x", b0, b1)) +
  labs(x = "carat (x)", y = "price (y)") +
  theme_classic(base_size = 16)

ggsave("docs-v3/images/slides/lesson-11/gen_ls.png", g,
       width = 6.5, height = 4.5, dpi = 200, bg = "white")
