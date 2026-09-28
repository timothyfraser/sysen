# slides_workshop_9_estimation.R --------------------------------------------
#
# Feeds: Workshop 9 (Parameter Estimation) slides: Weibull PDF shapes,
# the log-likelihood peak for crops.csv, and Example 1 (Weibull rectification
# of the capacitor failure times, workshops/workshop9_capacitors.csv).
# Run from the sigma repo root:  Rscript functions/slides_workshop_9_estimation.R
# Writes docs-v3/images/slides/workshop-9/gen_weibull_pdf.png, gen_loglik.png

library(dplyr)
library(ggplot2)
library(readr)

red = "#B31B1B"
out = "docs-v3/images/slides/workshop-9/"

# 1. Weibull densities for several shapes (c = 1) --------------------------
w = expand.grid(x = seq(0.01, 3, length.out = 300), m = c(0.5, 1, 2, 4, 10)) %>%
  mutate(density = dweibull(x, shape = m, scale = 1), m = factor(m))
g1 = ggplot(w, aes(x = x, y = density, color = m)) +
  geom_line(linewidth = 1.3) + coord_cartesian(ylim = c(0, 2.5)) +
  scale_color_manual(values = c("#B31B1B", "#E8833A", "#2A9D8F", "#457B9D", "#6D597A")) +
  labs(x = "Time (multiples of characteristic life c)", y = "Density f(t)", color = "Shape m") +
  theme_classic(base_size = 20) + theme(legend.position = "right")
ggsave(paste0(out, "gen_weibull_pdf.png"), g1, width = 7, height = 4.2, dpi = 160)

# 2. Log-likelihood of an exponential fitted to crops.csv --------------------
crops = read_csv("workshops/crops.csv", show_col_types = FALSE)
ll = function(data, lambda){ dexp(data, rate = lambda) %>% log() %>% sum() }
grid = tibble(lambda = seq(0.004, 0.04, length.out = 300)) %>%
  mutate(loglik = sapply(lambda, function(l) ll(crops$days, l)))
best = 1 / mean(crops$days)
g2 = ggplot(grid, aes(x = lambda, y = loglik)) +
  geom_line(color = red, linewidth = 1.3) +
  geom_vline(xintercept = best, linetype = "dashed") +
  annotate("text", x = best, y = min(grid$loglik), label = round(best, 5), hjust = -0.1, size = 6) +
  labs(x = "Rate parameter lambda", y = "Log-likelihood") +
  theme_classic(base_size = 20)
ggsave(paste0(out, "gen_loglik.png"), g2, width = 7, height = 4.2, dpi = 160)
cat("crops MLE lambda =", best, " loglik =", ll(crops$days, best), "\n")

# 3. Example 1: linear rectification of the Weibull -------------------------
cap = read_csv("workshops/workshop9_capacitors.csv", show_col_types = FALSE) %>%
  mutate(F = (i - 0.3) / (50 + 0.4), X = log(t), Y = log(-log(1 - F)))
fit = lm(Y ~ X, data = cap)
m_hat = unname(coef(fit)[2]); b_hat = unname(coef(fit)[1])
c_hat = exp(-b_hat / m_hat)
print(round(c(m_hat = m_hat, b_hat = b_hat, c_hat = c_hat), 4))
