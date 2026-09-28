# slides_recitation_11_rsm.R
# Recomputes every figure/number on the Recitation 11 (RSM) slides.
# Run from the repo root:  source("functions/slides_recitation_11_rsm.R")
# Data: workshops/gingerbread_test1.csv, workshops/recitation11_textile.csv
library(dplyr)
library(tidyr)
library(readr)
library(ggplot2)
library(broom)

out = "docs-v3/images/slides/recitation-11/"

# ---- Gingerbread: second-order model m3 and its contour ----
cookies = read_csv("workshops/gingerbread_test1.csv", show_col_types = FALSE)
m3 = lm(yum ~ molasses * ginger + I(molasses^2) + I(ginger^2), data = cookies)
print(round(coef(m3), 2))
print(glance(m3) %>% select(r.squared))

grid = expand_grid(molasses = seq(0.75, 1.5, length.out = 100),
                   ginger = seq(0.5, 2, length.out = 100))
grid$yum = predict(m3, newdata = grid)
best = grid %>% slice_max(yum, n = 1)
print(best)

g1 = ggplot(grid, aes(x = molasses, y = ginger, z = yum)) +
  geom_raster(aes(fill = yum)) +
  geom_contour(color = "white", bins = 12) +
  geom_point(data = best, aes(x = molasses, y = ginger), inherit.aes = FALSE, size = 4, color = "black") +
  scale_fill_viridis_c(option = "plasma", name = "Predicted\nYum Factor") +
  labs(title = "Predicted yum, inside the tested range (dot = predicted best)",
       x = "Molasses (cups)", y = "Ginger (tablespoons)") +
  theme_minimal(base_size = 18)
ggsave(paste0(out, "gen_contour_yum.png"), g1, width = 9, height = 5.6, dpi = 110)

# ---- Textiles: models M1-M4 (Table 12.8 / 12.9) ----
d = read_csv("workshops/recitation11_textile.csv", show_col_types = FALSE)
print(max(d$y) / min(d$y))  # 40.4

m1 = lm(y ~ length + amplitude + load + I(length^2) + I(amplitude^2) + I(load^2) +
          length:amplitude + amplitude:load + length:load, data = d)
m2 = lm(log(y) ~ length + amplitude + load, data = d)
m3t = lm(log(y) ~ log(length) + log(amplitude) + log(load), data = d)
# M4: power model with the exponents of M3 rounded: y = k (l/A)^5 L^-3
k = exp(mean(log(d$y) - 5*log(d$length/d$amplitude) + 3*log(d$load)))

d$M1 = fitted(m1)
d$M2 = exp(fitted(m2))
d$M3 = exp(fitted(m3t))
d$M4 = k * (d$length / d$amplitude)^5 * d$load^-3

p = c(10, 4, 4, 4)
rss = sapply(c("M1", "M2", "M3", "M4"), function(m) sum((d$y - d[[m]])^2))
df = c(17, 23, 23, 23)
tab = tibble(model = c("M1", "M2", "M3", "M4"), rss_e3 = rss / 1000, df = df,
             ms = rss_e3 / df * 1000 / 1000 * 1, p = p) %>%
  mutate(ms = rss / df / 1000, avgvar = ms * p / 27)
print(tab %>% mutate(across(where(is.numeric), ~round(., 1))))

long = d %>% mutate(run = row_number()) %>%
  select(run, y, M1, M2, M3, M4) %>%
  pivot_longer(M1:M4, names_to = "model", values_to = "pred")
g2 = ggplot(long, aes(x = y, y = pred)) +
  geom_abline(slope = 1, intercept = 0, color = "grey50") +
  geom_point(size = 2.5, color = "#0b5cad") +
  facet_wrap(~model, nrow = 1) +
  scale_x_log10() + scale_y_continuous(trans = "log10") +
  labs(title = "Predicted vs observed lifetime, 27 textile runs (log axes)",
       x = "Observed lifetime y (cycles)", y = "Predicted") +
  theme_minimal(base_size = 18)
ggsave(paste0(out, "gen_textile_fit.png"), g2, width = 11, height = 4.6, dpi = 110)
