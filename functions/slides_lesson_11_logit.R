# slides_lesson_11_logit.R
# Lesson 10 Appendix: binary logistic regression, rebuilt on the course diamonds data.
# Is a diamond above the median price? P(expensive) ~ carat, with an odds-ratio reading.
# Run from the repo root: Rscript functions/slides_lesson_11_logit.R

library(dplyr)
library(readr)
library(broom)

mydiamonds = read_csv("workshops/mydiamonds.csv",
                      show_col_types = FALSE)

# 1 if the diamond costs more than the median price, else 0
d = mydiamonds %>%
  mutate(expensive = as.integer(price > median(price)))

# Logistic regression: log-odds linear in carat
m = glm(expensive ~ carat, data = d, family = binomial)
m %>% tidy()
# Odds ratio for +0.1 carat: exp(beta x 0.1)
exp(coef(m)["carat"] * 0.1)
