# slides_lesson_5_attribute.R
# Reproduces the attribute-chart figures and numbers on the Lesson 5 slides
# (p chart, np chart, u chart). Run from the top of the sysen folder:
#   Rscript functions/slides_lesson_5_attribute.R            # saves PNGs here
#   Rscript functions/slides_lesson_5_attribute.R <out_dir>  # saves PNGs there

library(dplyr)
library(readr)
library(ggplot2)
source("functions/functions_process_control.R")

args = commandArgs(trailingOnly = TRUE)
out_dir = if (length(args) >= 1) args[1] else "."

# 1. p chart: misplaced inventory items per week (n varies) -----------------
inventory = read_csv("workshops/inventory.csv", show_col_types = FALSE)

# The same math ggp() uses
pstats = inventory %>%
  mutate(p = x / n,
         pbar = sum(x) / sum(n),
         se = sqrt(pbar * (1 - pbar) / n),
         lower = pmax(pbar - 3 * se, 0),
         upper = pmin(pbar + 3 * se, 1))
cat("Total checked =", sum(inventory$n), "; total misplaced =", sum(inventory$x), "\n")
cat("pbar =", round(unique(pstats$pbar), 4), "\n")
print(pstats %>% mutate(across(p:upper, ~ round(.x, 3))), n = Inf)

g_p = ggp(t = inventory$t, x = inventory$x, n = inventory$n,
          xlab = "Week", ylab = "Fraction Misplaced")
ggsave(file.path(out_dir, "gen_p_inventory.png"), g_p, width = 7, height = 4, dpi = 200)

# 2. np chart: needs the SAME n in every subgroup --------------------------
# The hot-spring data: 20 samples per month. A sample "fails" when the
# temperature is outside 42-50 degrees C. x = failures per month, n = 20.
water = read_csv("workshops/onsen.csv", show_col_types = FALSE)
fails = water %>%
  group_by(time) %>%
  summarize(n = n(), x = sum(temp < 42 | temp > 50), .groups = "drop")
npbar = sum(fails$x) / nrow(fails)
pbar_np = sum(fails$x) / sum(fails$n)
cat("\nonsen fails per month:\n"); print(fails)
cat("npbar =", round(npbar, 3), "; pbar =", round(pbar_np, 3),
    "; limits =", round(max(npbar - 3 * sqrt(npbar * (1 - pbar_np)), 0), 3),
    "to", round(npbar + 3 * sqrt(npbar * (1 - pbar_np)), 3), "\n")

g_np = ggnp(t = fails$time, x = fails$x, n = fails$n,
            xlab = "Month", ylab = "Samples outside 42-50 C (of 20)")
ggsave(file.path(out_dir, "gen_np_onsen.png"), g_np, width = 7, height = 4, dpi = 200)

# 3. u chart: accidents per month (one month = one unit, so u = c) --------
accidents = read_csv("workshops/accidents.csv", show_col_types = FALSE)
ubar = sum(accidents$x) / nrow(accidents)
cat("\nTotal accidents =", sum(accidents$x), "over", nrow(accidents), "months\n")
cat("ubar =", round(ubar, 3), "; LCL =", round(max(ubar - 3 * sqrt(ubar), 0), 3),
    "; UCL =", round(ubar + 3 * sqrt(ubar), 3), "\n")

g_u = ggu(t = accidents$t, x = accidents$x,
          xlab = "Month", ylab = "Accidents per Month")
ggsave(file.path(out_dir, "gen_u_accidents.png"), g_u, width = 7, height = 4, dpi = 200)
