# slides_lesson_5_variable_charts.R -----------------------------------------
#
# Feeds: Lesson 5 slide "Types of Variable Control Charts" (average + standard
#   deviation charts of the product weights; individuals + moving range charts
#   of daily production).
# Run from the top of the repo:
#   Rscript functions/slides_lesson_5_variable_charts.R
# Reads:  workshops/product_weights.csv, workshops/daily_production.csv
# Writes: docs-v3/images/slides/lesson-5/gen_repro_var_xbar.png, gen_repro_var_s.png,
#         gen_repro_var_x.png, gen_repro_var_mr.png
#         (repro_ copies; they do not overwrite the published gen_var_*.png)

library(dplyr)
library(readr)
library(ggplot2)
source("functions/functions_process_control.R")

set.seed(12345) # dn() and bn() simulate the control constants
outdir = "docs-v3/images/slides/lesson-5"
red = "#B31B1B"

weights = read_csv("workshops/product_weights.csv", show_col_types = FALSE)
daily = read_csv("workshops/daily_production.csv", show_col_types = FALSE)

big = theme_classic(base_size = 20)

g_xbar = ggxbar(x = weights$subgroup, y = weights$x, xlab = "Subgroup", ylab = "Average weight - 250 g") + big
g_s = ggs(x = weights$subgroup, y = weights$x, xlab = "Subgroup", ylab = "Standard deviation") + big

# Individuals chart: x-bar +/- 3 mR-bar / d2, with d2 for n = 2
mrbar = mean(abs(diff(daily$production)))
d2_2 = 1.128
ind = tibble(xbar = mean(daily$production),
             lower = xbar - 3 * mrbar / d2_2, upper = xbar + 3 * mrbar / d2_2)
g_x = ggplot(daily, aes(x = day, y = production)) +
  geom_hline(data = ind, aes(yintercept = xbar), color = "grey40") +
  geom_hline(data = ind, aes(yintercept = lower), color = red, linetype = "dashed") +
  geom_hline(data = ind, aes(yintercept = upper), color = red, linetype = "dashed") +
  geom_line() + geom_point(size = 3) +
  labs(x = "Day", y = "Daily production", subtitle = "Individuals Chart") + big
g_mr = ggmr(x = daily$day, y = daily$production, xlab = "Day", ylab = "Moving range") + big

ggsave(file.path(outdir, "gen_repro_var_xbar.png"), g_xbar, width = 8, height = 4, dpi = 150)
ggsave(file.path(outdir, "gen_repro_var_s.png"), g_s, width = 8, height = 4, dpi = 150)
ggsave(file.path(outdir, "gen_repro_var_x.png"), g_x, width = 8, height = 4, dpi = 150)
ggsave(file.path(outdir, "gen_repro_var_mr.png"), g_mr, width = 8, height = 4, dpi = 150)

cat(sprintf("Individuals: x-bar = %.1f, mR-bar = %.1f, LCL = %.0f, UCL = %.0f\n",
            ind$xbar, mrbar, ind$lower, ind$upper))
