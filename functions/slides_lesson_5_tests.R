#' @name slides_lesson_5_tests.R
#' @title The 8 visual tests for special-cause variation, drawn in ggplot
#' @description
#' Reproduces the "8 visual tests" figure from Lesson 5 (Control Charts).
#' Each test gets a small simulated control chart: a centerline, light zone
#' lines at +/- 1 and 2 sigma (zones C, B, A), dashed control limits at
#' +/- 3 sigma (UCL / LCL), and the points that trip the test in red.
#'
#' Run from the top of the sysen folder:
#'   Rscript functions/slides_lesson_5_tests.R            # saves to "."
#'   Rscript functions/slides_lesson_5_tests.R images     # saves to images/
#'
#' Every series is in sigma units (centerline = 0, sigma = 1), so zone A is
#' between 2 and 3 sigma, zone B between 1 and 2, zone C within 1.

library(dplyr)
library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)
out_dir <- if (length(args) > 0) args[1] else "."

set.seed(5300)

# The test titles, verbatim from the figure ##################################
titles <- c(
  "Test 1. One Point Beyond Zone A",
  "Test 2. Two Out of Three Points in a Row Beyond Zone B",
  "Test 3. Four Out of Five Points in a Row Beyond Zone C",
  "Test 4. Eight Points in a Row on the Same Side of Centerline",
  "Test 5. Six Points in a Row Steadily Increasing or Decreasing",
  "Test 6. Fifteen Points in a Row in Zone C (Above and Below Centerline)",
  "Test 7. Eight Points in a Row on Both Sides of the Centerline with None in Zone C",
  "Test 8. Fourteen Points in a Row Alternating Up and Down"
)

# Background noise that stays well inside the limits
calm <- function(n, width = 0.8) pmax(pmin(rnorm(n, 0, 0.5), width), -width)

# Build each series: y = values, flag = TRUE for the points that trip the test
series <- list()

# Test 1: one point above the UCL, one point below the LCL
y <- calm(16, 1.6); y[5] <- 3.45; y[13] <- -3.45
series[[1]] <- tibble(t = seq_along(y), y = y, flag = t %in% c(5, 13))

# Test 2: 2 of 3 in a row beyond zone B (past 2 sigma), same side
y <- calm(16, 1.3)
y[3:5] <- c(2.4, 1.2, 2.6)
y[11:13] <- c(-2.3, -0.8, -2.6)
series[[2]] <- tibble(t = seq_along(y), y = y, flag = t %in% c(3, 5, 11, 13))

# Test 3: 4 of 5 in a row beyond zone C (past 1 sigma), same side
y <- calm(17, 0.8)
y[3:7] <- c(1.5, 0.4, 1.7, 1.3, 2.1)
y[11:15] <- c(-1.4, -1.8, -1.3, -0.5, -1.6)
series[[3]] <- tibble(t = seq_along(y), y = y, flag = t %in% c(3, 5, 6, 7, 11, 12, 13, 15))

# Test 4: 8 in a row on the same side of the centerline
y <- calm(16, 1.2)
y[5:12] <- -(abs(rnorm(8, 0.6, 0.35)) + 0.15)
y[4] <- 0.5; y[13] <- 0.7   # neighbours above, so the run is exactly 8
series[[4]] <- tibble(t = seq_along(y), y = y, flag = t %in% 5:12)

# Test 5: 6 in a row steadily increasing, then 6 steadily decreasing
y <- calm(17, 0.8)
y[2:7] <- seq(-1.9, 1.8, length.out = 6)
y[10:15] <- seq(1.6, -2.0, length.out = 6)
series[[5]] <- tibble(t = seq_along(y), y = y, flag = t %in% c(2:7, 10:15))

# Test 6: 15 in a row hugging the centerline (zone C, both sides)
y <- c(1.7, runif(15, -0.8, 0.8), -1.6, 1.4)
series[[6]] <- tibble(t = seq_along(y), y = y, flag = t %in% 2:16)

# Test 7: 8 in a row on both sides, none in zone C (all past 1 sigma)
y <- calm(12, 0.7)
y[3:10] <- c(-1.6, 1.8, 1.5, 2.1, -1.4, -1.9, 1.7, 1.4)
series[[7]] <- tibble(t = seq_along(y), y = y, flag = t %in% 3:10)

# Test 8: 14 in a row alternating up and down
y <- calm(17, 0.6)
y[2:15] <- 0.2 * sin(seq(0, 3, length.out = 14)) +
  (-1)^(1:14) * runif(14, 0.45, 1.1)
y[1] <- y[2] - 0.3    # breaks the zig-zag before the run (t2 is a trough)
y[16] <- y[15] + 0.3  # ... and after it
series[[8]] <- tibble(t = seq_along(y), y = y, flag = t %in% 2:15)

# One control chart ############################################################
plot_test <- function(k, title = TRUE) {
  d <- series[[k]]
  n <- nrow(d)
  zones <- tibble(
    y = c(-2.5, -1.5, -0.5, 0.5, 1.5, 2.5),
    label = c("A", "B", "C", "C", "B", "A"))
  g <- ggplot(d, aes(x = t, y = y)) +
    # zone lines (light) and centerline
    geom_hline(yintercept = c(-2, -1, 1, 2), color = "#e3cfcb", linewidth = 0.6) +
    geom_hline(yintercept = 0, color = "#8a6a6a", linewidth = 0.8) +
    # control limits at +/- 3 sigma
    annotate("segment", x = -1.2, xend = n + 0.5, y = c(-3, 3), yend = c(-3, 3),
             color = "#B31B1B", linetype = "dashed", linewidth = 0.9) +
    annotate("text", x = -0.6, y = zones$y, label = zones$label,
             size = 5.2, color = "#8a6a6a", fontface = "bold") +
    annotate("text", x = n + 0.8, y = c(3, -3), label = c("UCL", "LCL"), hjust = 0,
             size = 5, color = "#B31B1B", fontface = "bold") +
    geom_line(color = "#9a8a8a", linewidth = 0.8) +
    geom_point(data = filter(d, !flag), size = 3.4, color = "#4a3a3a") +
    geom_point(data = filter(d, flag), size = 4.4, color = "#B31B1B") +
    scale_x_continuous(limits = c(-1.2, n + 3.6), expand = c(0, 0)) +
    scale_y_continuous(limits = c(-3.9, 3.9), expand = c(0, 0)) +
    theme_void(base_size = 18) +
    theme(plot.margin = margin(4, 4, 4, 4),
          plot.title = element_text(face = "bold", size = 16, hjust = 0))
  if (title) g <- g + labs(title = titles[k])
  g
}

# Save #########################################################################
# The slide prints each title in HTML above the chart, so the slide copies are
# saved without the ggplot title. Set title = TRUE to get the titled versions.
for (k in 1:8) {
  ggsave(file.path(out_dir, paste0("gen_test", k, ".png")),
         plot_test(k, title = FALSE),
         width = 4, height = 1.8, dpi = 200, bg = "white")
}

# e.g. print(plot_test(7)) to see one with its title
