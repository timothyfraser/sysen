# slides_lesson_5_weights.R
#
# Reproduces the numbers and the figure on the Lesson 5 slides
# "Example: Product Weight Data", "Control Chart Constants",
# "Formula Summary" and "Individual & Moving Range Chart".
#
# Run it from the top of the sysen folder:
#   Rscript functions/slides_lesson_5_weights.R
# Figures are saved into `out_dir` (defaults to the current folder).

library(dplyr)
library(readr)
library(ggplot2)
source("functions/functions_process_control.R")

args = commandArgs(trailingOnly = TRUE)
if (!exists("out_dir")) out_dir = if (length(args) > 0) args[1] else "."
set.seed(12345) # dn() and bn() simulate their constants

# 1. Product weight data (Table 4.1; x = weight - 250) -----------------------
weights = read_csv("workshops/product_weights.csv", show_col_types = FALSE)

# Per-subgroup statistics, as in the table
stat = weights %>%
  group_by(subgroup) %>%
  summarize(xbar = mean(x), r = max(x) - min(x), s = sd(x), v = var(x), n = n())
print(stat, n = 22)

totals = stat %>%
  summarize(xbbar = mean(xbar), rbar = mean(r), sbar = mean(s),
            s2_pooled = mean(v), s_pooled = sqrt(mean(v)))
print(totals)

# 2. Control chart constants for subgroup size n = 5 --------------------------
n = 5
d = dn(n = n)   # d2, d3, D3, D4
b = bn(n = n)   # b2 (= C4), b3, A3, B3, B4
A2 = 3 / (d$d2 * sqrt(n))
print(d); print(b); cat("A2 =", A2, "\n")

# Constants for n = 2..25 (compare with the Table of Control Chart Constants)
constants = tibble(n = 2:25) %>%
  group_by(n) %>%
  reframe(dn(n = n), A2_ = 3 / (dn(n = n)$d2 * sqrt(n)), bn(n = n))
print(constants, n = 24, width = Inf)

# 3. Four ways to set the limits of the average chart -------------------------
# (Table: "Four Ways to Design an X-bar Chart" -- 3.66 +/- 1.39, 1.44, 1.40, 1.83)
xbars = stat$xbar
mr_xbar = mean(abs(diff(xbars)))
four = tibble(
  method = c("1. Pooled sigma_short", "2. X-bar - R", "3. X-bar - S", "4. X-bar - mR"),
  center = totals$xbbar,
  halfwidth = c(3 * totals$s_pooled / sqrt(n),
                A2 * totals$rbar,
                b$A3 * totals$sbar,
                3 * mr_xbar / dn(n = 2)$d2))
print(four)

# The package helpers, for comparison
limits_avg(x = weights$subgroup, y = weights$x) %>% slice(1) %>% print(width = Inf)
limits_s(x = weights$subgroup, y = weights$x) %>% slice(1) %>% print(width = Inf)
limits_r(x = weights$subgroup, y = weights$x) %>% slice(1) %>% print(width = Inf)

# 4. Daily production: individuals & moving range charts (Table 4.3) ---------
prod = read_csv("workshops/daily_production.csv", show_col_types = FALSE)
mr = abs(diff(prod$production))
xbar = mean(prod$production)
mrbar = mean(mr)
d2 = dn(n = 2)$d2                # about 1.128
ucl = xbar + 3 * mrbar / d2      # the textbook's xbar + 2.66 mR-bar
lcl = xbar - 3 * mrbar / d2
cat("xbar =", xbar, " mR-bar =", mrbar, " UCL =", ucl, " LCL =", lcl, "\n")
cat("mR chart UCL (3.268 mR-bar) =", 3.268 * mrbar, "\n")
limits_mr(x = prod$day, y = prod$production) %>% slice(1) %>% print(width = Inf)

# Individuals chart: each day's production against x-bar +/- 2.66 mR-bar
lines = tibble(y = c(ucl, xbar, lcl, 3000),
               label = c(paste0("UCL = ", round(ucl)), paste0("x-bar = ", round(xbar)),
                         paste0("LCL = ", round(lcl)), "Target = 3000"))
g1 = ggplot() +
  geom_ribbon(data = prod, mapping = aes(x = day, ymin = lcl, ymax = ucl),
              fill = "steelblue", alpha = 0.2) +
  geom_hline(data = lines, mapping = aes(yintercept = y),
             color = c("grey40", "grey40", "grey40", "firebrick"),
             linetype = c("solid", "solid", "solid", "dashed")) +
  geom_line(data = prod, mapping = aes(x = day, y = production), linewidth = 1) +
  geom_point(data = prod, mapping = aes(x = day, y = production), size = 3) +
  geom_label(data = lines, mapping = aes(x = 25, y = y, label = label), hjust = 0, size = 3.5) +
  scale_x_continuous(limits = c(1, 30), breaks = seq(0, 25, by = 5)) +
  labs(x = "Day", y = "Daily Production", subtitle = "Individuals Chart") +
  theme_classic(base_size = 14)
ggsave(file.path(out_dir, "gen_weights_individuals.png"), g1, width = 7, height = 4, dpi = 200)

# Moving range chart, straight from the course function
g2 = ggmr(x = prod$day, y = prod$production, xlab = "Day", ylab = "Moving Range") +
  theme_classic(base_size = 14)
ggsave(file.path(out_dir, "gen_weights_mr.png"), g2, width = 7, height = 4, dpi = 200)
