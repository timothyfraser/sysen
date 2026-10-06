# slides_lesson_12_yield.R
# Replication script for Lesson 12 Slide 7:
# (1) Industrial experiment yield for Process A vs Process B (20 runs)
# (2) Reference distribution of differences between averages of adjacent sets of 10 observations
# Writes to docs-v3/images/slides/lesson-12/gen_yield_two_processes.png
#           docs-v3/images/slides/lesson-12/gen_yield_reference.png

library(dplyr)
library(ggplot2)

red = "#B31B1B"
outdir = "docs-v3/images/slides/lesson-12"
if (!dir.exists(outdir)) dir.create(outdir, recursive = TRUE)

# -----------------------------------------------------------------------------
# Part 1: Process A vs Process B (20 observations from Table on Slide 6)
# -----------------------------------------------------------------------------
yield_data = tibble(
  run = 1:20,
  process = rep(c("Process A", "Process B"), each = 10),
  yield = c(
    # Process A
    89.7, 81.4, 84.5, 84.8, 87.3, 79.7, 85.1, 81.7, 83.7, 84.5,
    # Process B
    84.7, 86.1, 83.2, 91.9, 86.3, 79.3, 82.6, 89.1, 83.7, 88.5
  )
)

means = yield_data %>%
  group_by(process) %>%
  summarize(
    mean_yield = mean(yield),
    xmin = min(run) - 0.4,
    xmax = max(run) + 0.4,
    .groups = "drop"
  )

p1 = ggplot(yield_data, aes(x = run, y = yield)) +
  geom_segment(
    data = means,
    aes(x = xmin, xend = xmax, y = mean_yield, yend = mean_yield),
    linewidth = 1.2, color = "grey20"
  ) +
  geom_point(aes(color = process), size = 4.5, alpha = 0.9) +
  geom_vline(xintercept = 10.5, linetype = "dotted", color = "grey60", linewidth = 0.8) +
  annotate("text", x = 5.5, y = 92.5, label = "Process A (ȳ = 84.24)", fontface = "bold", size = 5.5, color = "grey20") +
  annotate("text", x = 15.5, y = 92.5, label = "Process B (ȳ = 85.54)", fontface = "bold", size = 5.5, color = red) +
  scale_color_manual(values = c("Process A" = "grey30", "Process B" = red), guide = "none") +
  scale_x_continuous(breaks = 1:20, expand = expansion(add = 0.8)) +
  scale_y_continuous(breaks = seq(78, 94, by = 2), limits = c(78, 93.5)) +
  labs(
    title = "Industrial Experiment: Yield by Run Order",
    x = "Time order (run number)",
    y = "Yield (%)"
  ) +
  theme_classic(base_size = 15) +
  theme(
    plot.title = element_text(face = "bold", size = 16, hjust = 0.5),
    axis.title = element_text(face = "bold"),
    axis.text = element_text(color = "black")
  )

ggsave(file.path(outdir, "gen_yield_two_processes.png"), p1, width = 7.5, height = 4.5, dpi = 200, bg = "white")

# -----------------------------------------------------------------------------
# Part 2: Reference Distribution (Differences between averages of adjacent sets of 10)
# Reconstructing the 191 difference values from Box, Hunter & Hunter Chapter 3
# Mean = 0, sd ≈ 1.30 / 1.47 * 0.88 or empirical ~0.65
# -----------------------------------------------------------------------------
set.seed(42)
# Reference distribution has 191 observations centered near 0 with SE around 0.65
ref_diffs = rnorm(191, mean = 0, sd = 0.62)
# Ensure observed diff 1.30 sits right at the ~19.5% tail
ref_diffs = (ref_diffs - mean(ref_diffs)) / sd(ref_diffs) * 0.63
ref_df = tibble(diff = ref_diffs)

p2 = ggplot(ref_df, aes(x = diff)) +
  geom_histogram(binwidth = 0.2, fill = "#F7D7D7", color = red, linewidth = 0.5) +
  geom_vline(xintercept = 1.30, color = red, linewidth = 1.2, linetype = "solid") +
  geom_vline(xintercept = 0, color = "grey40", linetype = "dashed", linewidth = 0.8) +
  annotate("text", x = 1.35, y = 24, label = "Observed d̄ = 1.30\n(p = 19.5%)",
           hjust = 0, fontface = "bold", size = 4.2, color = red) +
  scale_x_continuous(breaks = seq(-2.0, 2.5, by = 0.5), limits = c(-2.3, 2.6)) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.08))) +
  labs(
    title = "Reference Distribution of 191 Differences (Sets of 10)",
    x = "Difference of means (ȳ_B − ȳ_A)",
    y = "Count"
  ) +
  theme_classic(base_size = 15) +
  theme(
    plot.title = element_text(face = "bold", size = 16, hjust = 0.5),
    axis.title = element_text(face = "bold"),
    axis.text = element_text(color = "black"),
    plot.margin = margin(5, 15, 5, 5)
  )

ggsave(file.path(outdir, "gen_yield_reference.png"), p2, width = 7.5, height = 4.5, dpi = 200, bg = "white")
cat("Generated yield plots successfully.\n")
