# slides_recitation_6_ci.R ---------------------------------------------------
# Feeds: Recitation 6 slides 6 and 8 (Why Confidence Intervals? / Z-scores).
# Run from the repo root:  Rscript functions/slides_recitation_6_ci.R
# Data: workshops/onsen.csv (onsen water temperature, 8 subgroups of 20).
# Output: prints the z-score tibble, saves docs-v3/images/slides/recitation-6/gen_cp_ci.png
library(dplyr)
library(readr)
library(ggplot2)

water = read_csv("workshops/onsen.csv", show_col_types = FALSE)

# Capability Index (for centered, normal data)
cp = function(sigma_s, upper, lower){ abs(upper - lower) / (6*sigma_s) }

# Subgroup statistics (as in the chapter)
stat = water %>%
  group_by(time) %>%
  summarize(xbar = mean(temp), sd = sd(temp), n_w = n()) %>%
  summarize(
    xbbar = mean(xbar),
    sigma_s = sqrt(mean(sd^2)),
    n = sum(n_w),
    n_w = unique(n_w),
    k = n())

# Slide 8: the z-score confidence interval for Cp
bands = stat %>%
  summarize(
    # index
    estimate = cp(sigma_s = sigma_s, lower = 42, upper = 50),
    # Get our extra quantities of interest
    v_short = k*(n_w - 1), # get degrees of freedom
    # Get standard error for cp
    se = estimate * sqrt(1 / (2*v_short)),
    # Get z score
    z = qnorm(0.975), # get position of 97.5th percentile in normal distribution
    # Get upper and lower confidence interval!
    lower = estimate - z * se,
    upper = estimate + z * se)
print(bands)

# Slide 6: the chart
mychart = bands %>%
  ggplot(mapping = aes(x = "Cp Index", y = estimate,
                       ymin = lower, ymax = upper)) +
  # Get draw us some benchmarks to make our chart meaningful
  geom_hline(yintercept = c(0,1,2), color = c("grey", "black", "grey")) +
  # Draw the points!
  geom_point() +
  geom_linerange() +
  # Add theming
  theme_classic(base_size = 14) +
  coord_flip() +
  labs(y = "Index Value", x = NULL)

out = "docs-v3/images/slides/recitation-6/gen_cp_ci.png"
ggsave(out, plot = mychart, width = 6, height = 3, dpi = 150)
