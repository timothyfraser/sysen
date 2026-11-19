# slides_workshop_9_rectification.R ------------------------------------------
#
# Feeds: Workshop 13 (Parameter Estimation) slide "Linear Rectification: what
# it does". The 25 capacitor failure times (50 on test), before and after the
# Weibull rectification: F(t) curves in t; ln(-ln(1 - F)) is a line in ln t.
# Run from the sigma repo root:  Rscript functions/slides_workshop_9_rectification.R
# Writes docs-v3/images/slides/workshop-9/gen_rectify_curve.png, gen_rectify_line.png

library(dplyr)
library(ggplot2)
library(readr)

red = "#B31B1B"
out = "docs-v3/images/slides/workshop-9/"

# Rectify: median-rank F, then X = ln t and Y = ln(-ln(1 - F)) ---------------
cap = read_csv("workshops/workshop9_capacitors.csv", show_col_types = FALSE) %>%
  mutate(F = (i - 0.3) / (50 + 0.4), X = log(t), Y = log(-log(1 - F)))
fit = lm(Y ~ X, data = cap)
m_hat = unname(coef(fit)[2]); b_hat = unname(coef(fit)[1])
c_hat = exp(-b_hat / m_hat)
print(round(c(m_hat = m_hat, b_hat = b_hat, c_hat = c_hat), 4))

# 1. Before: F(t_i) against t, with the fitted Weibull CDF ------------------
curve = tibble(t = seq(0, 3000, length.out = 400)) %>%
  mutate(F = 1 - exp(-(t / c_hat)^m_hat))
g1 = ggplot() +
  geom_line(data = curve, aes(x = t, y = F), color = red, linewidth = 1.6) +
  geom_point(data = cap, aes(x = t, y = F), size = 4, alpha = 0.85) +
  labs(title = "Before: F(t) curves in t",
       x = "Failure time t (hours)", y = "F(t), fraction failed") +
  theme_classic(base_size = 26) +
  theme(plot.title = element_text(face = "bold"))
ggsave(paste0(out, "gen_rectify_curve.png"), g1, width = 7, height = 5.6, dpi = 150)

# 2. After: Y against X is a straight line; read m and c off it -------------
lab = paste0("slope = m-hat = ", sprintf("%.2f", m_hat), "\n",
             "intercept = b-hat = ", sprintf("%.2f", b_hat), "\n",
             "c-hat = e^(-b/m) = ", sprintf("%.0f", c_hat))
g2 = ggplot(cap, aes(x = X, y = Y)) +
  geom_abline(intercept = b_hat, slope = m_hat, color = red, linewidth = 1.6) +
  geom_point(size = 4, alpha = 0.85) +
  annotate("text", x = -0.4, y = -0.35, label = lab, hjust = 0, vjust = 1,
           size = 7.5, lineheight = 1.1, color = red, fontface = "bold") +
  labs(title = "After: a straight line in ln t",
       x = "X = ln t", y = "Y = ln(-ln(1 - F))") +
  theme_classic(base_size = 26) +
  theme(plot.title = element_text(face = "bold"))
ggsave(paste0(out, "gen_rectify_line.png"), g2, width = 7, height = 5.6, dpi = 150)
