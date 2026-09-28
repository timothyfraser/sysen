# slides_lesson_9_lifedist.R
# Figures and recomputed numbers for the Lesson 9 deck
# (Weibull, Gamma & Lognormal functions). Run from the sigma repo root.
# Writes docs-v3/images/slides/lesson-9/gen_*.png

library(dplyr)
library(tidyr)
library(ggplot2)

out = "docs-v3/images/slides/lesson-9"
red = "#B31B1B"

# --- Gamma: f(t), R(t), z(t) for several k, with lambda = 1 ----------------
gamma_curves = expand_grid(k = c(0.5, 1, 2, 3), t = seq(0.01, 6, by = 0.01)) %>%
  mutate(
    f = dgamma(t, shape = k, rate = 1),
    r = 1 - pgamma(t, shape = k, rate = 1),
    z = f / r
  ) %>%
  pivot_longer(cols = c(f, r, z), names_to = "fn", values_to = "value") %>%
  mutate(fn = factor(fn, levels = c("f", "r", "z"),
                     labels = c("PDF f(t)", "Reliability R(t)", "Failure rate z(t)")),
         k = factor(paste0("k = ", k), levels = paste0("k = ", c(0.5, 1, 2, 3)))) %>%
  filter(value <= 2.5)

g = ggplot(gamma_curves, aes(x = t, y = value, color = k)) +
  geom_line(linewidth = 1.4) +
  facet_wrap(~fn, scales = "free_y") +
  scale_color_manual(values = c("#E8A0A0", "#D05050", red, "#4A0A0A")) +
  labs(x = "Time t (lambda = 1)", y = NULL, color = NULL) +
  theme_classic(base_size = 20) +
  theme(legend.position = "bottom", strip.background = element_blank(),
        strip.text = element_text(face = "bold"))
ggsave(file.path(out, "gen_gamma_functions.png"), g, width = 13, height = 5.2, dpi = 150)

# --- Example 1 / 2: gamma reliability, k = 3, lambda = 0.05, t = 24 --------
k = 3; lambda = 0.05; t = 24
terms = (lambda * t)^(0:(k - 1)) / factorial(0:(k - 1)) * exp(-lambda * t)
print(terms)                                   # n = 0, 1, 2 terms
print(sum(terms))                              # R(24) by hand
print(1 - pgamma(t, shape = k, rate = lambda)) # R(24) via pgamma
print(c(mttf = k / lambda, var = k / lambda^2))

# --- Weibull Example 1: capacitors, c = 20000 hr, m = 0.5, 1, 2 -----------
# CDF in percent, failure rate z(t) = (m / c) * (t / c)^(m - 1) in % per 1000 hr
caps = expand_grid(t = c(100, 1000, 20000, 30000), m = c(0.5, 1, 2)) %>%
  mutate(cdf_pct = 100 * pweibull(t, shape = m, scale = 20000),
         z_pct_khr = 100 * 1000 * (m / 20000) * (t / 20000)^(m - 1))
print(caps, n = Inf)

# --- Rayleigh (Weibull m = 2): arm offset, sigma = 0.1 cm, r = 0.4 cm ------
print(1 - exp(-0.4^2 / (2 * 0.1^2)))

# --- Lognormal example: T50 = 5000, sigma = 0.7, t = 2000 ------------------
print(log(2000 / 5000) / 0.7)
print(plnorm(2000, meanlog = log(5000), sdlog = 0.7))
