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

# --- Lognormal: f(t) and F(t) for several sigma, t in multiples of T50 -----
# (T50 = 1, so t is in multiples of the median). PDF panel to t = 3 with the
# sigma = 5 spike near zero clipped at 2.5; CDF panel to t = 5.
sigmas = c(0.2, 0.5, 1, 2, 5)
ln_curves = expand_grid(sigma = sigmas,
                        t = c(10^seq(-6, -2.5, by = 0.25), seq(0.005, 5, by = 0.005))) %>%
  mutate(
    f = dlnorm(t, meanlog = log(1), sdlog = sigma),
    cdf = plnorm(t, meanlog = log(1), sdlog = sigma)
  ) %>%
  pivot_longer(cols = c(f, cdf), names_to = "fn", values_to = "value") %>%
  filter(!(fn == "f" & (t > 3 | value > 2.5))) %>%
  mutate(fn = factor(fn, levels = c("f", "cdf"), labels = c("PDF f(t)", "CDF F(t)")),
         sigma = factor(sigma, levels = sigmas, labels = as.character(sigmas)))

g2 = ggplot(ln_curves, aes(x = t, y = value, color = sigma, linetype = sigma)) +
  geom_line(linewidth = 1.2) +
  facet_wrap(~fn, scales = "free") +
  scale_color_manual(values = c("#DE6C68", "#CC4743", red, "#7F1010", "#4A0505")) +
  scale_linetype_manual(values = c("solid", "dashed", "solid", "dashed", "solid")) +
  labs(x = "Time t (multiples of T50)", y = NULL,
       color = "σ", linetype = "σ") +
  theme_classic(base_size = 17) +
  theme(legend.position = "right", strip.background = element_blank(),
        strip.text = element_text(face = "bold", size = rel(1)),
        axis.text = element_text(size = rel(0.9)),
        legend.text = element_text(size = rel(0.9)),
        legend.key.width = unit(1.1, "cm"),
        legend.box.spacing = unit(4, "pt"),
        legend.margin = margin(0, 0, 0, 0),
        plot.margin = margin(2, 2, 2, 2))
# sized for the right-hand third of the slide: little whitespace, so it reads at ~377 px wide
ggsave(file.path(out, "gen_lognormal_functions.png"), g2, width = 5.2, height = 3.15, dpi = 150)

# --- Example 1 / 2: gamma reliability, k = 3, lambda = 0.05, t = 24 --------
k = 3; lambda = 0.05; t = 24
terms = (lambda * t)^(0:(k - 1)) / factorial(0:(k - 1)) * exp(-lambda * t)
print(terms)                                   # n = 0, 1, 2 terms
print(sum(terms))                              # R(24) by hand
print(1 - pgamma(t, shape = k, rate = lambda)) # R(24) via pgamma
print(c(mttf = k / lambda, var = k / lambda^2))

# Example 1 by hand, term by term (the code on the Example 1 slide)
k2 = (0.05*24)^2 / factorial(2) * exp(-0.05*24)
k1 = (0.05*24)^1 / factorial(1) * exp(-0.05*24)
k0 = (0.05*24)^0 / factorial(0) * exp(-0.05*24)
# Key thing to know: factorial of 0 = 1.
print(c(k2, k1, k0))                           # 0.2168598 0.3614331 0.3011942
print(k2 + k1 + k0)                            # 0.8794871

# --- Weibull Example 1: capacitors, c = 20000 hr, m = 0.5, 1, 2 -----------
# CDF in percent, failure rate z(t) = (m / c) * (t / c)^(m - 1) in % per 1000 hr
caps = expand_grid(t = c(100, 1000, 20000, 30000), m = c(0.5, 1, 2)) %>%
  mutate(cdf_pct = 100 * pweibull(t, shape = m, scale = 20000),
         z_pct_khr = 100 * 1000 * (m / 20000) * (t / 20000)^(m - 1))
print(caps, n = Inf)

# --- Weibull Example 2: variable choke valve, m = 2.25, lambda = 1.15e-4 /hr
m = 2.25; lambda = 1.15e-4; t1 = 4380; t2 = 4380     # 6 months = 4380 hrs
print(exp(-(lambda * t1)^m))                         # R(4380): 0.808
print(gamma(1/m + 1) / lambda)                       # MTTF: 7702 hrs
print((1/lambda) * log(2)^(1/m))                     # median life t_m: 7389 hrs
print(exp(-(lambda * (t1 + t2))^m) / exp(-(lambda * t1)^m))  # R(t1 + t2 | t1): 0.448

# --- Rayleigh (Weibull m = 2): arm offset, sigma = 0.1 cm, r = 0.4 cm ------
print(1 - exp(-0.4^2 / (2 * 0.1^2)))

# --- Lognormal properties: MTTF and variance, T50 = 5000, sigma = 0.7 ------
# The course chapter's formulas; the variance is checked by integrating
# (t - MTTF)^2 f(t) over t, so a wrong formula cannot hide here.
t50 = 5000; sigma = 0.7
mttf = t50 * exp(sigma^2 / 2)
variance = t50^2 * exp(sigma^2) * (exp(sigma^2) - 1)
check = integrate(function(t) (t - mttf)^2 * dlnorm(t, meanlog = log(t50), sdlog = sigma),
                  lower = 0, upper = Inf)$value
print(round(c(mttf = mttf, variance = variance, check = check)))

# --- Lognormal example: T50 = 5000, sigma = 0.7, t = 2000 ------------------
print(log(2000 / 5000) / 0.7)
print(plnorm(2000, meanlog = log(5000), sdlog = 0.7))
