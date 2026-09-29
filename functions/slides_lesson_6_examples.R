# slides_lesson_6_examples.R ------------------------------------------------
#
# Feeds: Lesson 6 slides 28-35 (Example 1 Cpk/Ppk, Example 2 capability and
#   performance indices, the implied-minimum-Cpk table, the design-capability
#   table, and the capability/performance index chart).
# Run from the top of the repo:
#   Rscript functions/slides_lesson_6_examples.R
# Reads:  workshops/product_weights.csv, workshops/capability_example2.csv,
#         workshops/capability_index_chart.csv
# Writes: workshops/capability_min_cpk.csv, workshops/capability_design_targets.csv,
#         docs-v3/images/slides/lesson-6/gen_ex2_xbar_r.png,
#         docs-v3/images/slides/lesson-6/gen_ex_index_plot.png,
#         docs-v3/images/slides/lesson-6/gen_ex1_dist_vs_spec.png,
#         docs-v3/images/slides/lesson-6/gen_ex2_dist_vs_spec.png
#         and prints a summary of Example 1 and Example 2 to the console.

library(dplyr)
library(readr)
library(tidyr)
library(ggplot2)
source("functions/functions_process_control.R")

set.seed(12345)
red = "#B31B1B"
outdir = "docs-v3/images/slides/lesson-6"

# Textbook control-chart constants for subgroups of n = 5
# (dn() and bn() in the helpers simulate these; the book uses the tables)
d2 = 2.326; c4 = 0.94; A2 = 0.577; D3 = 0; D4 = 2.114

# Example 1: product weights (Table 4.1) -----------------------------------
# x = weight - 250 grams, so the declared weight (the lower spec limit,
# 250 g) sits at x = 0. There is no upper spec limit.
weights = read_csv("workshops/product_weights.csv", show_col_types = FALSE)

w_sub = weights %>%
  group_by(subgroup) %>%
  summarize(xbar = mean(x), r = max(x) - min(x), s = sd(x), s2 = var(x))

ex1 = w_sub %>%
  summarize(xbbar = mean(xbar), rbar = mean(r), sbar = mean(s),
            s2_pooled = mean(s2), s_pooled = sqrt(mean(s2))) %>%
  mutate(
    mu = 250 + xbbar,
    sigma_short = rbar / d2,
    sigma_total = sd(weights$x),
    cpk = cpk(mu = mu, sigma_s = sigma_short, lower = 250),
    ppk = ppk(mu = mu, sigma_t = sigma_total, lower = 250))

# Example 2: 16 subgroups x 5 (Cp, Pp, Ppk) --------------------------------
ex2_data = read_csv("workshops/capability_example2.csv", show_col_types = FALSE)
lower = 0.5; upper = 0.9

ex2_sub = ex2_data %>%
  group_by(subgroup) %>%
  summarize(xbar = mean(x), r = max(x) - min(x), s = sd(x))

ex2 = ex2_sub %>%
  summarize(xbbar = mean(xbar), rbar = mean(r), sbar = mean(s)) %>%
  mutate(
    sigma_short = rbar / d2,
    sigma_short_c4 = sbar / c4,
    sigma_total = sd(ex2_data$x),
    cp = cp(sigma_s = sigma_short, upper = upper, lower = lower),
    cpk = cpk(mu = xbbar, sigma_s = sigma_short, lower = lower, upper = upper),
    pp = pp(sigma_t = sigma_total, upper = upper, lower = lower),
    ppk_upper = (upper - xbbar) / (3 * sigma_total),
    ppk_lower = (xbbar - lower) / (3 * sigma_total),
    ppk = ppk(mu = xbbar, sigma_t = sigma_total, lower = lower, upper = upper),
    cp_c4 = cp(sigma_s = sigma_short_c4, upper = upper, lower = lower))

# Printed summary -----------------------------------------------------------
cat("\n==== Example 1: product weights (LSL = 250 g, one-sided) ====\n")
cat(sprintf("x-double-bar (x = weight - 250) = %.4f   [scan 3.66]\n", ex1$xbbar))
cat(sprintf("R-bar = %.4f [scan 2.50]  s-bar = %.4f [scan 0.978]\n", ex1$rbar, ex1$sbar))
cat(sprintf("s2_pooled = %.4f [scan 1.067]  s_pooled = %.4f [scan 1.033]\n", ex1$s2_pooled, ex1$s_pooled))
cat(sprintf("mu = %.4f g            [scan 253.66]\n", ex1$mu))
cat(sprintf("sigma_short = Rbar/d2 = %.4f [scan 1.074]\n", ex1$sigma_short))
cat(sprintf("sigma_total = s_total = %.4f [scan 1.098]\n", ex1$sigma_total))
cat(sprintf("Cpk = (mu - 250)/(3 sigma_short) = %.4f\n", ex1$cpk))
cat(sprintf("Ppk = (mu - 250)/(3 sigma_total) = %.4f\n", ex1$ppk))

cat("\n==== Example 2: 16 subgroups x 5, LSL 0.5, USL 0.9 ====\n")
cat(sprintf("x-double-bar = %.4f [scan 0.7375]  R-bar = %.4f [scan 0.1906]\n", ex2$xbbar, ex2$rbar))
cat(sprintf("sigma_short = Rbar/d2 = %.4f [scan 0.0819]\n", ex2$sigma_short))
cat(sprintf("s-bar = %.8f [scan 0.07627613]; s-bar/c4 = %.4f [scan 0.0811]\n", ex2$sbar, ex2$sigma_short_c4))
cat(sprintf("sigma_total = %.6f [scan 0.0817 / 0.081716]\n", ex2$sigma_total))
cat(sprintf("Cp  = %.4f [scan 0.8136]   (Cp with s-bar/c4 = %.4f)\n", ex2$cp, ex2$cp_c4))
cat(sprintf("Cpk = %.4f (not printed on the scan)\n", ex2$cpk))
cat(sprintf("Pp  = %.4f [scan 0.8159]\n", ex2$pp))
cat(sprintf("Ppk = min(%.4f, %.4f) = %.4f [scan min(0.6629, 0.9688) = 0.6629]\n",
            ex2$ppk_upper, ex2$ppk_lower, ex2$ppk))

# Table check: subgroup summaries vs Table 4.1 printed columns --------------
printed = tibble(
  subgroup = 1:22,
  xbar_p = c(3.30,4.30,3.22,3.94,4.16,3.86,3.88,1.60,3.46,4.18,3.38,3.50,3.94,3.16,4.44,3.80,3.36,4.30,4.12,3.66,3.50,3.50),
  r_p = c(2.3,3.5,1.5,3.0,2.3,3.3,3.2,1.0,1.3,2.3,2.9,2.0,1.7,2.0,4.1,2.7,1.2,4.0,1.8,3.3,2.6,2.8),
  s_p = c(1.04,1.34,0.57,1.20,0.92,1.32,1.17,0.40,0.53,0.85,1.11,0.77,0.63,0.75,1.58,1.13,0.50,1.49,0.70,1.30,1.11,1.11),
  s2_p = c(1.08,1.80,0.33,1.45,0.85,1.73,1.37,0.16,0.28,0.73,1.24,0.59,0.39,0.56,2.51,1.28,0.25,2.22,0.50,1.70,1.23,1.24))
chk = w_sub %>% left_join(printed, by = "subgroup") %>%
  mutate(ok_xbar = abs(round(xbar, 2) - xbar_p) < 1e-9, ok_r = abs(round(r, 1) - r_p) < 1e-9,
         ok_s = abs(round(s, 2) - s_p) < 1e-9, ok_s2 = abs(round(s2, 2) - s2_p) < 1e-9)
cat("\n==== Table 4.1 check (22 subgroups): mismatches at printed precision ====\n")
bad = chk %>% filter(!(ok_xbar & ok_r & ok_s & ok_s2))
if(nrow(bad) == 0){ cat("none\n") } else { print(bad %>% select(subgroup, xbar, xbar_p, r, r_p, s, s_p, s2, s2_p), width = 120) }

# Computed table 1: implied minimum Cpk (slide 31) -------------------------
min_cpk = tibble(enclosed = c(0.90, 0.95, 0.99, 0.997, 0.999),
                 printed_two = c(0.55, 0.67, 0.86, 1.00, 1.09),
                 printed_one = c(0.43, 0.55, 0.78, 0.93, 1.03)) %>%
  mutate(two_sided = qnorm(1 - (1 - enclosed) / 2) / 3,
         one_sided = qnorm(enclosed) / 3)
write_csv(min_cpk %>% select(enclosed, two_sided, one_sided, printed_two, printed_one),
          "workshops/capability_min_cpk.csv")

# Computed table 2: design capability targets (slide 32) -------------------
# Sigma level k: design Cp = k/3; manufacturing Cpk = Cp - 0.5 (a 1.5-sigma
# mean shift); nonconforming PPM = both tails of the shifted normal;
# characteristics for system acceptance = floor(log(P) / log(conforming)).
design = tibble(sigma_level = c(3, 4, 5, 5.5, 6),
                printed_ppm = c(66800, 6210, 233, 63, 3.4),
                printed_n99 = c(0, 1, 43, 159, 2955),
                printed_n999 = c(0, 0, 4, 15, 294)) %>%
  mutate(cp = sigma_level / 3,
         cpk = cp - 0.5,
         ppm = 1e6 * (pnorm(-(sigma_level - 1.5)) + pnorm(-(sigma_level + 1.5))),
         pct_conforming = 100 - ppm / 1e4,
         n_99 = floor(log(0.99) / log(1 - ppm / 1e6)),
         n_999 = floor(log(0.999) / log(1 - ppm / 1e6)))
write_csv(design %>% select(sigma_level, cp, cpk, ppm, pct_conforming, n_99, n_999,
                            printed_ppm, printed_n99, printed_n999),
          "workshops/capability_design_targets.csv")

cat("\n==== Implied minimum Cpk: computed vs printed ====\n")
print(min_cpk %>% mutate(across(c(two_sided, one_sided), ~round(.x, 2))), width = 120)
cat("\n==== Design capability: computed vs printed ====\n")
print(design %>% mutate(ppm = signif(ppm, 4)) %>%
        select(sigma_level, cp, cpk, ppm, printed_ppm, n_99, printed_n99, n_999, printed_n999),
      width = 120)

# Figure: Example 2 X-bar and R chart pair ---------------------------------
ex2_long = ex2_sub %>%
  select(subgroup, xbar, r) %>%
  pivot_longer(c(xbar, r), names_to = "chart", values_to = "value") %>%
  mutate(chart = factor(chart, levels = c("xbar", "r"),
                        labels = c("Average (X-bar) chart", "Range (R) chart")))
ex2_lim = tibble(
  chart = factor(c("Average (X-bar) chart", "Range (R) chart")),
  center = c(ex2$xbbar, ex2$rbar),
  lcl = c(ex2$xbbar - A2 * ex2$rbar, D3 * ex2$rbar),
  ucl = c(ex2$xbbar + A2 * ex2$rbar, D4 * ex2$rbar))

g1 = ggplot(ex2_long, aes(x = subgroup, y = value)) +
  geom_hline(data = ex2_lim, aes(yintercept = center), color = "grey40") +
  geom_hline(data = ex2_lim, aes(yintercept = lcl), color = red, linetype = "dashed") +
  geom_hline(data = ex2_lim, aes(yintercept = ucl), color = red, linetype = "dashed") +
  geom_line(color = "grey20") +
  geom_point(size = 3, color = red) +
  facet_wrap(~chart, ncol = 1, scales = "free_y") +
  labs(x = "Subgroup", y = NULL) +
  theme_classic(base_size = 20) +
  theme(strip.background = element_blank(), strip.text = element_text(face = "bold", hjust = 0),
        plot.margin = margin(4, 8, 4, 4))
ggsave(file.path(outdir, "gen_ex2_xbar_r.png"), g1, width = 9, height = 7, dpi = 150)

# Figure: capability / performance index chart (slide 35) -------------------
idx = read_csv("workshops/capability_index_chart.csv", show_col_types = FALSE) %>%
  mutate(index = factor(index, levels = c("Cp", "Cpk", "Pp", "Ppk")))
spans = idx %>% group_by(characteristic) %>% summarize(lo = min(value), hi = max(value))

# One filled circle (shape 21) per index; the four indices differ by fill
# colour only (course red, dark blue, gold, grey-green), with a thin outline.
idx_fills = c(Cp = red, Cpk = "#1F4E79", Pp = "#E0A526", Ppk = "#6B8E7F")
g2 = ggplot() +
  geom_hline(yintercept = c(1, 1.5, 2), linetype = "dashed", color = "grey60") +
  geom_linerange(data = spans, aes(x = characteristic, ymin = lo, ymax = hi), color = "grey30") +
  geom_point(data = idx, aes(x = characteristic, y = value, fill = index),
             shape = 21, size = 5, stroke = 0.6, color = "grey15",
             position = position_dodge(width = 0.5)) +
  scale_fill_manual(values = idx_fills) +
  scale_y_continuous(limits = c(0, 3), breaks = seq(0, 3, 0.5)) +
  labs(x = "Characteristic", y = "Capability / performance index", fill = NULL) +
  theme_classic(base_size = 20) +
  theme(legend.position = "top", plot.margin = margin(4, 8, 4, 4))
ggsave(file.path(outdir, "gen_ex_index_plot.png"), g2, width = 7.5, height = 5.5, dpi = 150)


# Figure: Example 1 observed distribution vs the spec limit (slide 24) -----
# One-sided: the declared weight (LSL = 250 g) is the only limit.
w_plot = weights %>% mutate(weight = 250 + x)
g3 = ggplot(w_plot, aes(x = weight)) +
  annotate("rect", xmin = -Inf, xmax = 250, ymin = -Inf, ymax = Inf, fill = red, alpha = 0.12) +
  geom_histogram(binwidth = 0.5, boundary = 250, fill = "grey60", color = "white") +
  geom_vline(xintercept = 250, color = red, linewidth = 1.6) +
  geom_vline(xintercept = ex1$mu, color = "grey15", linetype = "dashed", linewidth = 1.1) +
  annotate("label", x = 250, y = Inf, vjust = 1.2, hjust = 0.5, size = 6.5, color = red,
           fontface = "bold", label = "LSL 250", border.colour = NA) +
  annotate("label", x = ex1$mu, y = Inf, vjust = 1.2, size = 6.5, color = "grey15",
           label = sprintf("mean %.2f", ex1$mu), border.colour = NA) +
  scale_x_continuous(limits = c(248.5, 257), breaks = seq(248, 257, 1)) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.2))) +
  labs(x = "Weight (g), 110 units", y = "Count") +
  theme_classic(base_size = 20) +
  theme(plot.margin = margin(4, 12, 4, 4))
ggsave(file.path(outdir, "gen_ex1_dist_vs_spec.png"), g3, width = 6, height = 4.4, dpi = 150)

# Figure: Example 2 observed distribution vs the spec limits (slide 26) ----
g4 = ggplot(ex2_data, aes(x = x)) +
  annotate("rect", xmin = -Inf, xmax = lower, ymin = -Inf, ymax = Inf, fill = red, alpha = 0.12) +
  annotate("rect", xmin = upper, xmax = Inf, ymin = -Inf, ymax = Inf, fill = red, alpha = 0.12) +
  geom_histogram(binwidth = 0.05, center = 0.5, fill = "grey60", color = "white") +
  geom_vline(xintercept = c(lower, upper), color = red, linewidth = 1.6) +
  geom_vline(xintercept = ex2$xbbar, color = "grey15", linetype = "dashed", linewidth = 1.1) +
  annotate("label", x = c(lower, upper), y = Inf, vjust = 1.2, size = 6.5, color = red,
           fontface = "bold", label = c("LSL 0.5", "USL 0.9"), border.colour = NA) +
  annotate("label", x = ex2$xbbar, y = Inf, vjust = 1.2, size = 6.5, color = "grey15",
           label = sprintf("mean %.3f", ex2$xbbar), border.colour = NA) +
  scale_x_continuous(limits = c(0.4, 1.0), breaks = seq(0.4, 1.0, 0.1)) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.2))) +
  labs(x = sprintf("Measurement, %d units", nrow(ex2_data)), y = "Count") +
  theme_classic(base_size = 20) +
  theme(plot.margin = margin(4, 12, 4, 4))
ggsave(file.path(outdir, "gen_ex2_dist_vs_spec.png"), g4, width = 6, height = 3.9, dpi = 150)

cat("\nWrote", file.path(outdir, c("gen_ex2_xbar_r.png", "gen_ex_index_plot.png",
    "gen_ex1_dist_vs_spec.png", "gen_ex2_dist_vs_spec.png")), sep = "\n")
