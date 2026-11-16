# slides_lesson_9_fit.R
# Table and figure for the Lesson 9 "Does It Fit?" slides: get_fit() on the
# chips data, then each distribution's expected chips per cell from
# get_expected(). Run from the sigma repo root. Python twin: slides_lesson_9_fit.py
# Writes docs-v3/images/slides/lesson-9/gen_fit_observed_expected.png

library(readr)
library(dplyr)
library(tidyr)
library(purrr)
library(ggplot2)

source("functions/functions_mle.R")
source("functions/functions_planning.R")

out = "docs-v3/images/slides/lesson-9"
red = "#B31B1B"

chips = read_csv("workshops/chips.csv", show_col_types = FALSE)

# 1. The table: one call, four distributions
fit = get_fit(data = chips, n_total = 200, tmax = 1500)
fit %>% select(dist, chisq, df, p_value, loglik) %>% as.data.frame() %>% print()

# 2. Expected chips per cell, from each fitted distribution
expected = function(d, p1, e1, p2, e2){
  args = list(data = chips, n_total = 200, dist = d)
  args[[p1]] = e1
  if(!is.na(p2)){ args[[p2]] = e2 }
  do.call(get_expected, args) %>% mutate(dist = d)
}
exp_all = pmap_dfr(list(fit$dist, fit$par1, fit$est1, fit$par2, fit$est2), expected) %>%
  mutate(cell = ifelse(is.infinite(upper), "1500+", paste0(lower, "-\n", upper)))
cells = unique(exp_all$cell)
exp_all = exp_all %>% mutate(cell = factor(cell, levels = cells),
                             dist = factor(dist, levels = fit$dist))
obs = exp_all %>% filter(dist == fit$dist[1]) %>% select(cell, r_obs)

cols = c(lognormal = red, gamma = "#2B2B2B", weibull = "#D05050", exponential = "#8C8C8C")
g = ggplot() +
  geom_col(data = obs, aes(x = cell, y = r_obs), fill = "#E8D5D5", width = 0.7) +
  geom_line(data = exp_all, aes(x = cell, y = r_exp, color = dist, group = dist), linewidth = 1.3) +
  geom_point(data = exp_all, aes(x = cell, y = r_exp, color = dist), size = 3) +
  scale_color_manual(values = cols) +
  labs(x = "Hours on test", y = "Chips failing in the cell", color = NULL) +
  theme_classic(base_size = 20) +
  theme(legend.position = "bottom", legend.margin = margin(0, 0, 0, 0),
        legend.box.spacing = unit(2, "pt"), axis.text.x = element_text(size = 15))
ggsave(file.path(out, "gen_fit_observed_expected.png"), g, width = 8.4, height = 4.7, dpi = 170)

# 3. Planning: chips needed for a lognormal life test (sigma must be assumed)
# sigma = 0.811 is the lognormal fit above; the others show how much the answer leans on it
plan_test("lognormal", t = 250, r = 5, ci = 0.90, t50 = 1000,
          sigma = c(0.6, 0.8, 0.811, 1.0, 1.2)) %>%
  select(sigma, n_up) %>% as.data.frame() %>% print()
