# slides_w12_recap.R --------------------------------------------------------
#
# Feeds: Workshop 12 (ANOVA & Latin Squares) slides, Recap section:
#   Example 1 (unpaired t-tests, equal and unequal variance),
#   Example 2 (F-test for two variances), Example 3 (paired t-test),
#   Example 4 (permutation test for a difference of means).
# Run from the top of the repo:
#   Rscript functions/slides_w12_recap.R
# Writes: docs-v3/images/slides/workshop-12/gen_perm_hist.png
#         and prints every test result shown on those slides.

library(dplyr)
library(broom)
library(ggplot2)

# Example 1 ---------------------------------------------------------------

data = tibble(
  method = c("A", "A", "A", "A", "A", "A", "A", "A", "A", "A",
          "B", "B", "B", "B", "B", "B", "B", "B", "B", "B"),
  yield = c(89.7, 81.4, 84.5, 84.8, 87.3, 79.7, 85.1, 81.7, 83.7, 84.5,
        84.7, 86.1, 83.2, 91.9, 86.3, 79.3, 82.6, 89.1, 83.7, 88.5)  )

# T-test assuming equal variance (unpaired)
t.test(formula = yield ~ method, data = data, var.equal = TRUE) %>% print()

# T-test not assuming equal variance
t.test(formula = yield ~ method, data = data, var.equal = FALSE) %>% print()

# Example 2 ---------------------------------------------------------------

# F test to compare two variances.
var.test(formula = yield ~ method, data = data) %>% print()

# Are they significantly different? (No --> p = 0.5049)

# Example 3 ---------------------------------------------------------------

# When data comes in pairs, like this, we use paired t-tests.
data2 = tibble(
  yield_a = c(89.7, 81.4, 84.5, 84.8, 87.3, 79.7, 85.1, 81.7, 83.7, 84.5),
  yield_b = c(84.7, 86.1, 83.2, 91.9, 86.3, 79.3, 82.6, 89.1, 83.7, 88.5)
)

# Basic method for paired t-test
t.test(data2$yield_a, data2$yield_b, paired = TRUE, var.equal = TRUE) %>% print()

# Example 4 ---------------------------------------------------------------

# Shuffling is random; fix the seed so the printed p-value is reproducible.
set.seed(12345)

perms = tibble(rep = 1:1000) %>%
  group_by(rep) %>%
  reframe(data) %>%
  group_by(rep) %>%
  mutate(yield = sample(yield, size = n(), replace = FALSE)) %>%
  group_by(rep) %>%
  summarize( dbar = mean( yield[method == "A"] )  -  mean( yield[method == "B"])  )

# Get the observed difference of means
obs = data %>%
  summarize(dbar = mean( yield[method == "A"] )  -  mean( yield[method == "B"])  )
print(obs)

# 2-tailed percentage of random stats greater than the observed
mean( abs(perms$dbar) >= abs(obs$dbar) ) %>% print()

# Histogram of the 1000 shuffled differences, observed value marked ---------
outdir = "docs-v3/images/slides/workshop-12"
lab = round(obs$dbar, 1)

g = ggplot(perms, aes(x = dbar)) +
  geom_histogram(bins = 30, fill = "#3880c0", color = "white") +
  geom_vline(xintercept = obs$dbar, color = "#B31B1B", linewidth = 1.4) +
  annotate("label", x = obs$dbar, y = Inf, label = as.character(lab),
           color = "#B31B1B", fill = "white", size = 8, vjust = 1.3,
           hjust = 1.1) +
  labs(x = "dbar", y = "count") +
  theme_minimal(base_size = 22) +
  theme(plot.background = element_rect(fill = "white", color = NA),
        panel.background = element_rect(fill = "white", color = NA))

ggsave(file.path(outdir, "gen_perm_hist.png"), g,
       width = 6, height = 4.2, dpi = 200, bg = "white")
