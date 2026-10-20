# slides_recitation_7_lambda.R ------------------------------------------------
# Feeds: Recitation 11 (file 19_slides_recitation_7), "Choosing the percentile and the k factor".
# Draws the sampling distribution of lambda with the 2.5th and 97.5th percentile
# bounds marked, for r = 20 failures and lambda-hat = 0.002 (Example 1).
# Run from the repo root:  Rscript functions/slides_recitation_7_lambda.R
# Output: docs-v3/images/slides/recitation-7/gen_sampling_ci.png
library(dplyr)
library(ggplot2)
source("functions/functions_k.R")

r = 20
lambda_hat = 0.002
# k factors: lower uses r, upper uses r + 1 (Table 2, time-censored)
k = qk(p = c(0.025, 0.975), r = r, .time = TRUE)
bounds = k * lambda_hat   # 0.00122, 0.00309

# Sampling distribution of lambda: lambda-hat x chi-square(2r) / 2r
curve = data.frame(lambda = seq(0, 0.0055, length.out = 400)) %>%
  mutate(density = dchisq(lambda * 2 * r / lambda_hat, df = 2 * r) * 2 * r / lambda_hat)

marks = data.frame(
  lambda = c(bounds[1], lambda_hat, bounds[2]),
  label = c("lambda[2.5]", "hat(lambda)", "lambda[97.5]"))
top = max(curve$density)

mychart = ggplot(curve, aes(x = lambda, y = density)) +
  geom_area(data = curve %>% filter(lambda >= bounds[1], lambda <= bounds[2]),
            fill = "#fbecec") +
  geom_line(color = "#B31B1B", linewidth = 1.2) +
  geom_segment(data = marks, aes(x = lambda, xend = lambda, y = 0, yend = top * 1.08),
               inherit.aes = FALSE, color = "#2a1414") +
  geom_text(data = marks, aes(x = lambda, y = top * 1.18, label = label),
            inherit.aes = FALSE, parse = TRUE, size = 7) +
  scale_x_continuous(breaks = c(bounds[1], lambda_hat, bounds[2]),
                     labels = c("0.0012", "0.002", "0.0031")) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.05))) +
  theme_classic(base_size = 18) +
  theme(axis.text.y = element_blank(), axis.ticks.y = element_blank(), axis.line.y = element_blank()) +
  labs(x = "Failure rate per hour", y = NULL,
       caption = "r = 20 failures, alpha = 0.05, Type I (time) censoring")

ggsave("docs-v3/images/slides/recitation-7/gen_sampling_ci.png", plot = mychart,
       width = 7, height = 4.2, dpi = 150)
print(round(bounds, 5))
