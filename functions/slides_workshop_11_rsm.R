# slides_workshop_11_rsm.R
# Regenerates the two RSM exercises on the Workshop 10 deck (slides 28):
#   Exercise 1: predicted yum from the interaction model at the 16 tested recipes
#   Exercise 2: predicted yum, with a 95% confidence interval, at a new recipe
# Run from the repo root:  source("functions/slides_workshop_11_rsm.R")
# Data: workshops/gingerbread_test1.csv
library(dplyr)
library(readr)
library(tidyr)

cookies = read_csv("workshops/gingerbread_test1.csv", show_col_types = FALSE)

# Exercise 1 -- interaction model, predicted at every tested recipe
m2 = cookies %>% lm(formula = yum ~ molasses * ginger)

grid = expand_grid(
  molasses = c(0.5, 0.75, 1, 1.25),
  ginger = c(0.5, 1, 1.5, 2)
) %>%
  mutate(yhat = predict(m2, newdata = tibble(molasses, ginger)))

grid %>% slice_max(yhat, n = 1) %>% print()
write_csv(grid, "workshops/slides_workshop_11_rsm_grid.csv")

# Exercise 2 -- second-order model, a new recipe that was never tested
m3 = cookies %>% lm(formula = yum ~ molasses * ginger + I(molasses^2) + I(ginger^2))

ci = predict(m3, newdata = tibble(molasses = 1.1, ginger = 1.3),
             se.fit = TRUE, interval = "confidence", level = 0.95) %>%
  with(fit) %>%
  as_tibble()
print(ci)
write_csv(ci %>% mutate(molasses = 1.1, ginger = 1.3, .before = 1),
          "workshops/slides_workshop_11_rsm_ci.csv")
