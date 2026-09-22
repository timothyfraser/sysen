# slides_lesson_5_variable_charts.R
# Reproduces the "Types of Variable Control Charts" figures on the Lesson 5 slides:
#   left:  average (X-bar) and standard deviation (S) charts for the product weight data
#   right: individual (X) and moving range (mR) charts for the daily production data
# Run from the top of the sysen folder:
#   Rscript functions/slides_lesson_5_variable_charts.R            # saves PNGs here
#   Rscript functions/slides_lesson_5_variable_charts.R <out_dir>  # saves PNGs there
library(dplyr)
library(readr)
library(ggplot2)
source("functions/functions_process_control.R")
args = commandArgs(trailingOnly = TRUE)
out_dir = if (length(args) > 0) args[1] else "."
set_theme()

# Product weights: 22 subgroups of 5 (x = weight - 250 grams)
weights = read_csv("workshops/product_weights.csv", show_col_types = FALSE)
g1 = ggxbar(x = weights$subgroup, y = weights$x, xlab = "Subgroup", ylab = "Average weight (x)")
g2 = ggs(x = weights$subgroup, y = weights$x, xlab = "Subgroup", ylab = "Std. dev. of weight")
ggsave(file.path(out_dir, "gen_var_xbar.png"), g1, width = 7, height = 3.2, dpi = 200)
ggsave(file.path(out_dir, "gen_var_s.png"), g2, width = 7, height = 3.2, dpi = 200)

# Daily production: one measurement per day
prod = read_csv("workshops/daily_production.csv", show_col_types = FALSE)

# Individuals (X) chart: center = mean, limits = mean +/- 3 * sigma_short, sigma_short = mRbar / d2 (d2 = 1.128 for n = 2)
mr = abs(diff(prod$production))
stat = tibble(center = mean(prod$production), mrbar = mean(mr)) %>%
  mutate(sigma_s = mrbar / 1.128, upper = center + 3 * sigma_s, lower = center - 3 * sigma_s)
g3 = ggplot(prod, aes(x = day, y = production)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = stat$lower, ymax = stat$upper, fill = "steelblue", alpha = 0.2) +
  geom_hline(yintercept = stat$center, color = "lightgrey") +
  geom_line(linewidth = 1) + geom_point(size = 3) +
  labs(x = "Day", y = "Daily production", subtitle = "Individuals Chart",
       caption = sprintf("mean = %.0f | UCL = %.0f | LCL = %.0f", stat$center, stat$upper, stat$lower))
g4 = ggmr(x = prod$day, y = prod$production, xlab = "Day", ylab = "Moving range")
ggsave(file.path(out_dir, "gen_var_x.png"), g3, width = 7, height = 3.2, dpi = 200)
ggsave(file.path(out_dir, "gen_var_mr.png"), g4, width = 7, height = 3.2, dpi = 200)
