# slides_lesson_11_rsm.R
# Recomputes the response-surface grids and the confidence interval on the
# Lesson 11 RSM slides (basic model vs second-order model with interaction).
# Run from the repo root:  Rscript functions/slides_lesson_11_rsm.R
# Data:    workshops/gingerbread_test1.csv
# Writes:  workshops/slides_lesson_11_rsm_grid.csv  (model, molasses, ginger, yhat)
#          workshops/slides_lesson_11_rsm_ci.csv    (model, molasses, ginger, fit, lwr, upr)
#          docs-v3/images/slides/lesson-11/gen_contour_yum_tested.png (m3 contour, tested region)
# The slide SVG itself is drawn from the grid CSV by functions/slides_lesson_11_rsm.py
library(dplyr)
library(tidyr)
library(readr)
library(broom)
library(ggplot2)

cookies = read_csv("workshops/gingerbread_test1.csv", show_col_types = FALSE)

# The tested levels: molasses 0.5-1.25 cups, ginger 0.5-2 tbsp
cookies %>% count(molasses, ginger) %>% print()

# ---- Two model specifications ----
m1 = lm(yum ~ molasses + ginger, data = cookies)
m3 = lm(yum ~ molasses * ginger + I(molasses^2) + I(ginger^2), data = cookies)

print(round(coef(m1), 3))
print(round(coef(m3), 3))
fits = bind_rows(glance(m1) %>% mutate(model = "m1"),
                 glance(m3) %>% mutate(model = "m3")) %>%
  select(model, r.squared)
print(fits)
stopifnot(round(glance(m3)$r.squared, 3) == 0.335)

# ---- Predicted yum on a 16 x 16 grid inside the tested region ----
myx = expand_grid(molasses = seq(from = 0.5, to = 1.25, by = 0.05),
                  ginger = seq(from = 0.5, to = 2, by = 0.1))
stopifnot(nrow(myx) == 256)

grid = bind_rows(
  myx %>% mutate(model = "m1", yhat = predict(m1, newdata = myx)),
  myx %>% mutate(model = "m3", yhat = predict(m3, newdata = myx))
) %>%
  select(model, molasses, ginger, yhat) %>%
  mutate(molasses = round(molasses, 2), ginger = round(ginger, 1), yhat = round(yhat, 3))
write_csv(grid, "workshops/slides_lesson_11_rsm_grid.csv")

# ---- Each model's optimum (argmax) ----
best = grid %>% group_by(model) %>% slice_max(yhat, n = 1) %>% ungroup()
print(best)
same = best$molasses[1] == best$molasses[2] & best$ginger[1] == best$ginger[2]
cat(if (same) "The two optima are the SAME recipe.\n" else "The two optima DIFFER.\n")

# ---- Predict with a 95% confidence interval at m3's best recipe ----
best3 = best %>% filter(model == "m3") %>% select(molasses, ginger)
ci = predict(m3, newdata = best3, se.fit = TRUE, interval = "confidence", level = 0.95) %>%
  with(fit) %>%
  as_tibble()
print(ci)
best3 %>%
  bind_cols(ci) %>%
  mutate(model = "m3") %>%
  select(model, molasses, ginger, fit, lwr, upr) %>%
  mutate(across(c(fit, lwr, upr), ~ round(.x, 3))) %>%
  write_csv("workshops/slides_lesson_11_rsm_ci.csv")

# ---- m3 filled contour over the TESTED region (same look as gen_contour_yum.png) ----
fine = expand_grid(molasses = seq(0.5, 1.25, length.out = 100),
                   ginger = seq(0.5, 2, length.out = 100))
fine$yum = predict(m3, newdata = fine)
bestfine = fine %>% slice_max(yum, n = 1)
print(bestfine)
g1 = ggplot(fine, aes(x = molasses, y = ginger, z = yum)) +
  geom_raster(aes(fill = yum)) +
  geom_contour(color = "white", bins = 12) +
  geom_point(data = bestfine, aes(x = molasses, y = ginger), inherit.aes = FALSE, size = 4, color = "black") +
  scale_fill_viridis_c(option = "plasma", name = "Predicted\nYum Factor") +
  labs(title = "Predicted yum (dot = best)",
       x = "Molasses (cups)", y = "Ginger (tablespoons)") +
  theme_minimal(base_size = 20)
ggsave("docs-v3/images/slides/lesson-11/gen_contour_yum_tested.png", g1, width = 7, height = 4.4, dpi = 110)
