# slides_lesson_11_diamonds.R --------------------------------------------------
# Feeds: Lesson 10 slides, "Say it in a sentence" (the coefficient table).
# Run from the top of the repo:  Rscript functions/slides_lesson_11_diamonds.R
# Reads:  workshops/mydiamonds.csv (1,000 diamonds: price, carat, cut)
# Writes: workshops/slides_lesson_11_diamonds_coef.csv; prints the table.
library(dplyr)
library(readr)
library(broom)

mydiamonds = read_csv("workshops/mydiamonds.csv", show_col_types = FALSE)

# Read ~ as "explained by"
m = mydiamonds %>% lm(formula = price ~ carat)

# One row per coefficient: estimate, standard error, t statistic, p-value
coefs = m %>% tidy()
print(coefs)

coefs %>% write_csv("workshops/slides_lesson_11_diamonds_coef.csv")
