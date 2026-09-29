# slides_lesson_6_ci.R ------------------------------------------------------
#
# Feeds: Lesson 6 slide "Using Bootstrapped Sampling Distributions" (myqi).
# Bootstraps Cp for the onsen bathwater exactly as the slides do (1000
# resamples, set.seed(1), spec limits 42-50 C, sigma_short from the
# subgroups by time), then draws the bootstrap distribution with the
# observed Cp against its 2.5th-97.5th percentile interval.
# Run from the top of the repo:
#   Rscript functions/slides_lesson_6_ci.R
# Reads:  workshops/onsen.csv
# Writes: docs-v3/images/slides/lesson-6/gen_boot_ci.png

library(dplyr)
library(readr)
library(ggplot2)

red = "#B31B1B"
outdir = "docs-v3/images/slides/lesson-6"

# Capability index (centered, stable process)
cp = function(sigma_s, upper, lower){  abs(upper - lower) / (6*sigma_s)   }

water = read_csv("workshops/onsen.csv", show_col_types = FALSE)

# Observed Cp from the original sample
bands = water %>%
  group_by(time) %>%
  summarize(s = sd(temp)) %>%
  summarize(sigma_s = sqrt(mean(s^2))) %>%
  mutate(estimate = cp(sigma_s, upper = 50, lower = 42))

# 1000 bootstrap resamples of the whole data.frame
set.seed(1)
myboot = tibble(rep = 1:1000) %>%
  group_by(rep) %>%
  reframe(water) %>%
  sample_n(size = n(), replace = TRUE)

mybootstat = myboot %>%
  group_by(rep, time) %>%
  summarize(sigma_w = sd(temp), .groups = "drop") %>%
  group_by(rep) %>%
  summarize(sigma_s = sqrt(mean(sigma_w^2))) %>%
  mutate(estimate = cp(sigma_s, upper = 50, lower = 42))

myqi = mybootstat %>%
  summarize(
    cp = bands$estimate,
    lower = quantile(estimate, probs = 0.025),
    upper = quantile(estimate, probs = 0.975),
    se = sd(estimate))
print(myqi, digits = 3)

# Figure: bootstrap distribution, 95% percentile interval, observed Cp ------
g = ggplot(mybootstat, aes(x = estimate)) +
  annotate("rect", xmin = myqi$lower, xmax = myqi$upper, ymin = -Inf, ymax = Inf,
           fill = "grey85") +
  geom_histogram(bins = 40, fill = "grey55", color = "white", linewidth = 0.2) +
  geom_vline(xintercept = c(myqi$lower, myqi$upper), color = "grey20",
             linetype = "dashed", linewidth = 0.9) +
  geom_vline(xintercept = myqi$cp, color = red, linewidth = 2) +
  annotate("label", x = myqi$lower, y = Inf, vjust = 1.3, size = 5.5,
           label = sprintf("2.5th\n%.3f", myqi$lower), border.colour = NA) +
  annotate("label", x = myqi$upper, y = Inf, vjust = 1.3, size = 5.5,
           label = sprintf("97.5th\n%.3f", myqi$upper), border.colour = NA) +
  annotate("label", x = myqi$cp, y = Inf, vjust = 2.4, size = 6, color = red,
           fontface = "bold", label = sprintf("observed\nCp = %.3f", myqi$cp),
           border.colour = NA) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.75))) +
  labs(x = "Bootstrapped Cp (1,000 reps)", y = "Count") +
  theme_classic(base_size = 20) +
  theme(plot.margin = margin(4, 12, 4, 4))
ggsave(file.path(outdir, "gen_boot_ci.png"), g, width = 5, height = 4.4, dpi = 150)
cat("Wrote", file.path(outdir, "gen_boot_ci.png"), "\n")
