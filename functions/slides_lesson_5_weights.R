# slides_lesson_5_weights.R -------------------------------------------------
#
# Feeds: Lesson 5 "Example: Product Weight Data" slides (Table 4.1 summary
#   columns, the four ways to design an X-bar chart) and the Table 4.3
#   individuals / moving-range slides.
# Run from the top of the repo:
#   Rscript functions/slides_lesson_5_weights.R
# Reads:  workshops/product_weights.csv, workshops/daily_production.csv
# Writes: docs-v3/images/slides/lesson-5/gen_repro_weights_individuals.png,
#         gen_repro_weights_mr.png (repro_ copies; published gen_* untouched)
#         and prints the summary columns and control limits.

library(dplyr)
library(readr)
library(ggplot2)
source("functions/functions_process_control.R")

set.seed(12345)
outdir = "docs-v3/images/slides/lesson-5"
red = "#B31B1B"

# Table 4.1: summary columns -------------------------------------------------
weights = read_csv("workshops/product_weights.csv", show_col_types = FALSE)
sub = weights %>%
  group_by(subgroup) %>%
  summarize(xbar = mean(x), r = max(x) - min(x), s = sd(x), s2 = var(x))
print(sub %>% mutate(across(c(xbar, s, s2), ~round(.x, 2)), r = round(r, 1)), n = 22)

tot = sub %>% summarize(xbbar = mean(xbar), rbar = mean(r), sbar = mean(s),
                        s2_pooled = mean(s2), s_pooled = sqrt(mean(s2)),
                        mr_xbar = mean(abs(diff(xbar))))
cat(sprintf("\nx-double-bar = %.2f  R-bar = %.2f  s-bar = %.3f  s2_pooled = %.3f  s_pooled = %.3f\n",
            tot$xbbar, tot$rbar, tot$sbar, tot$s2_pooled, tot$s_pooled))

# Four ways to design an X-bar chart (n = 5; textbook constants) -------------
n = 5; A2 = 0.577; A3 = 1.427; d2_2 = 1.128
cat("\nX-bar chart half-widths (centre", round(tot$xbbar, 2), "):\n")
cat(sprintf("  1. pooled sigma_short: 3 * %.3f / sqrt(5) = %.2f\n", tot$s_pooled, 3 * tot$s_pooled / sqrt(n)))
cat(sprintf("  2. X-bar - R:          %.3f * %.2f = %.2f\n", A2, tot$rbar, A2 * tot$rbar))
cat(sprintf("  3. X-bar - S:          %.3f * %.3f = %.2f\n", A3, tot$sbar, A3 * tot$sbar))
cat(sprintf("  4. X-bar - mR:         3 * %.3f / %.3f = %.2f\n", tot$mr_xbar, d2_2, 3 * tot$mr_xbar / d2_2))

# Table 4.3: individuals and moving range -------------------------------------
daily = read_csv("workshops/daily_production.csv", show_col_types = FALSE) %>%
  mutate(mr = abs(production - lag(production)))
xbar = mean(daily$production); mrbar = mean(daily$mr, na.rm = TRUE)
cat(sprintf("\nDaily production: x-bar = %.0f, mR-bar = %.0f, UCL = x-bar + 2.66 mR-bar = %.0f, LCL = %.0f, mR UCL = 3.268 mR-bar = %.0f\n",
            xbar, mrbar, xbar + 2.66 * mrbar, xbar - 2.66 * mrbar, 3.268 * mrbar))

g_ind = ggplot(daily, aes(x = day, y = production)) +
  geom_hline(yintercept = xbar, color = "grey40") +
  geom_hline(yintercept = 3000, color = "grey60", linetype = "dotted") +
  geom_hline(yintercept = c(xbar - 2.66 * mrbar, xbar + 2.66 * mrbar), color = red, linetype = "dashed") +
  geom_line() + geom_point(size = 3) +
  labs(x = "Day", y = "Daily production") +
  theme_classic(base_size = 20)
g_mr = ggmr(x = daily$day, y = daily$production, xlab = "Day", ylab = "Moving range") +
  theme_classic(base_size = 20)

ggsave(file.path(outdir, "gen_repro_weights_individuals.png"), g_ind, width = 9, height = 5, dpi = 150)
ggsave(file.path(outdir, "gen_repro_weights_mr.png"), g_mr, width = 9, height = 5, dpi = 150)
