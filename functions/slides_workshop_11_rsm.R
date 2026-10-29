# slides_workshop_11_rsm.R
# Regenerates the three RSM exercises on the Workshop 10 deck (slides 28):
#   Exercise 1: predicted yum from the interaction model at the 16 tested recipes
#   Exercise 2: predicted yum, with a 95% confidence interval, at a new recipe
#   Exercise 3: the response surface of the second-order model (tile + contour)
# Run from the repo root:  source("functions/slides_workshop_11_rsm.R")
# Data: workshops/gingerbread_test1.csv
library(dplyr)
library(readr)
library(tidyr)
library(ggplot2)

cookies = read_csv("workshops/gingerbread_test1.csv", show_col_types = FALSE)

# Exercise 1 -- interaction model, predicted at every tested recipe
m2 = cookies %>% lm(formula = yum ~ molasses * ginger)

grid = expand_grid(
  molasses = c(0.5, 0.75, 1, 1.25),
  ginger = c(0.5, 1, 1.5, 2)
) %>%
  mutate(yhat = predict(m2, newdata = tibble(molasses, ginger)))

grid %>% print(n = 16)
grid %>% filter(yhat == max(yhat)) %>% print()
write_csv(grid, "workshops/slides_workshop_11_rsm_grid.csv")

# Exercise 2 -- second-order model, a new recipe that was never tested
m3 = cookies %>% lm(formula = yum ~ molasses * ginger +
                      I(molasses^2) + I(ginger^2))

ci = tibble(molasses = 1.1, ginger = 1.3) %>%
  mutate(predict(m3, newdata = ., se.fit = TRUE,
                 interval = "confidence", level = 0.95) %>%
           with(fit) %>%
           as_tibble())
print(ci)
write_csv(ci, "workshops/slides_workshop_11_rsm_ci.csv")

# Exercise 3 -- the response surface: tile + contour
g3 = expand_grid(molasses = seq(0.5, 1.25, length.out = 50),
                 ginger   = seq(0.5, 2,    length.out = 50)) %>%
  mutate(yhat = predict(m3, newdata = tibble(molasses, ginger))) %>%
  ggplot() +
  geom_tile(mapping = aes(x = molasses, y = ginger, fill = yhat)) +
  geom_contour(mapping = aes(x = molasses, y = ginger, z = yhat),
               color = "white", binwidth = 1) +
  scale_fill_viridis_c(option = "plasma") +
  labs(x = "Molasses (cups)", y = "Ginger (tbsp)", fill = "Predicted\nyum") +
  theme_classic(base_size = 16)

# Where is the surface highest and lowest?
surface = g3$data
surface %>% filter(yhat == max(yhat)) %>% print()
surface %>% filter(yhat == min(yhat)) %>% print()

ggsave("docs-v3/images/slides/workshop-11/ex3_heatmap.png", g3,
       width = 8, height = 5, dpi = 150, bg = "white")
