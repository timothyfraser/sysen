# Feeds Lesson 7 (Useful Life Distributions - Exponential) slides 6-7, 10, 12-13,
#   16, 22, 27 and 30: the charts, the light-bulb frequency table, and the numbers
#   behind the three in-deck exercises (slides 12, 15, 18) and Examples 1-3 (slides 28-30).
# Run from the sigma repo root:  Rscript functions/slides_lesson_7_exponential.R
# Reads  workshops/bulb_lifetimes.csv (100 bulb failure times, transcribed from slide 22).
# Writes gen_*.png (1100x600 px) to docs-v3/images/slides/lesson-7/ and prints every
#   recomputed number to the console. Nothing is random, so reruns are identical.
# Python twin: functions/slides_lesson_7_exponential.py (same parameters, *_py.png copies).
# Notation follows the course: f(t) pdf, F(t) CDF, R(t) reliability, z(t) failure rate
#   (hazard), H(t) cumulative hazard, lambda = constant failure rate, MTTF = 1/lambda.
library(dplyr)
library(ggplot2)
library(readr)
library(tidyr)

out = "docs-v3/images/slides/lesson-7"
red = "#B31B1B"; grey = "grey35"

# functions/functions_reliability.R holds r(), z(), afr() for the exponential, but it
# loads mosaicCalc (not installed everywhere), so the exponential pieces are restated here.
r_exp = function(t, lambda) { exp(-lambda * t) }
f_exp = function(t, lambda) { lambda * exp(-lambda * t) }

theme_deck = function() {
  theme_classic(base_size = 20) +
    theme(plot.margin = margin(8, 16, 4, 4), axis.line = element_line(linewidth = 0.8))
}
save = function(g, file) {
  ggsave(file.path(out, file), g, width = 11, height = 6, dpi = 100, bg = "white")
  cat("wrote", file.path(out, file), "\n")
}

# ---- 1. Bathtub curve (slides 6-7) ---------------------------------------------
# Illustrative z(t) = 1.2 e^(-t/0.5) + 0.25 + 0.25 (t/8)^6 : decreasing burn-in,
# flat useful life, rising wear-out. Period boundaries drawn at t = 1.6 and t = 7.3.
bath = tibble(t = seq(0.02, 10, length.out = 600)) %>%
  mutate(z = 1.2 * exp(-t / 0.5) + 0.25 + 0.25 * (t / 8)^6)
g = ggplot(bath, aes(t, z)) +
  geom_vline(xintercept = c(1.6, 7.3), linetype = "dashed", color = grey) +
  geom_line(color = red, linewidth = 1.8) +
  annotate("text", x = c(0.8, 4.45, 8.65), y = 0.1,
           label = c("Burn-in\nperiod", "Useful life\nperiod", "Wear-out\nperiod"),
           size = 6.5, vjust = 0, lineheight = 0.9) +
  scale_x_continuous(expand = c(0, 0), breaks = NULL) +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 1.5), breaks = NULL) +
  labs(x = "Time t", y = "z(t)") + theme_deck()
save(g, "gen_bathtub.png")

# ---- 2. Mode, median, MTTF (slide 10, left chart) -----------------------------
# The scan's curve is a lognormal with median 10 and MTTF 15: meanlog = ln 10,
# sdlog = sqrt(2 ln 1.5) = 0.9005. Then mode = exp(meanlog - sdlog^2) = 4.44, peak f = 0.066.
ml = log(10); sl = sqrt(2 * log(1.5))
mode_t = exp(ml - sl^2); median_t = exp(ml); mttf_t = exp(ml + sl^2 / 2)
cat(sprintf("Slide 10 lognormal: mode = %.2f, median = %.2f, MTTF = %.2f, f(mode) = %.4f\n",
            mode_t, median_t, mttf_t, dlnorm(mode_t, ml, sl)))
ln = tibble(t = seq(0.01, 25, length.out = 600)) %>% mutate(f = dlnorm(t, ml, sl))
marks = tibble(t = c(mode_t, median_t, mttf_t), lab = c("Mode", "Median", "MTTF")) %>%
  mutate(f = dlnorm(t, ml, sl))
g = ggplot(ln, aes(t, f)) +
  geom_segment(data = marks, aes(x = t, xend = t, y = 0, yend = f), linetype = "dashed", color = grey) +
  geom_line(color = red, linewidth = 1.8) +
  geom_text(data = marks, aes(y = f + 0.006, label = lab), size = 6.5, vjust = 0) +
  scale_x_continuous(expand = c(0, 0), breaks = seq(0, 25, 5)) +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 0.085)) +
  labs(x = "Time t", y = "f(t)") + theme_deck()
save(g, "gen_mode_median_mttf.png")

# ---- 3. R(t), z(t), f(t) for Exercise 1's item (slide 10 right chart; slide 12) --
# R(t) = 1/(0.2t+1)^2,  f(t) = 0.4/(0.2t+1)^3,  z(t) = 0.4/(0.2t+1)
ex1 = tibble(t = seq(0, 10, length.out = 400)) %>%
  mutate(`R(t)` = 1 / (0.2 * t + 1)^2, `f(t)` = 0.4 / (0.2 * t + 1)^3, `z(t)` = 0.4 / (0.2 * t + 1)) %>%
  pivot_longer(-t, names_to = "fn", values_to = "y")
lab3 = tibble(fn = c("R(t)", "z(t)", "f(t)"), t = c(1.6, 1.6, 1.6), y = c(0.72, 0.38, 0.1))
g = ggplot(ex1, aes(t, y, linetype = fn)) +
  geom_line(color = red, linewidth = 1.6) +
  geom_text(data = lab3, aes(label = fn), size = 7, hjust = 0, fontface = "italic") +
  scale_linetype_manual(values = c("R(t)" = "solid", "f(t)" = "solid", "z(t)" = "dashed"), guide = "none") +
  scale_x_continuous(expand = c(0, 0), breaks = seq(0, 10, 2)) +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 1.02), breaks = seq(0, 1, 0.2)) +
  labs(x = "Time t (months)", y = NULL) + theme_deck()
save(g, "gen_r_z_f.png")

# Exercise 1 (slide 12): MTTF = integral of R(t) from 0 to infinity
ex1_mttf = integrate(function(t) 1 / (0.2 * t + 1)^2, 0, Inf)$value
cat(sprintf("Exercise 1: MTTF = %.4f months (scan: 5 months)\n", ex1_mttf))

# ---- 4. "MTTF?" shaded pdf (slide 12) ------------------------------------------
# Drawn from Exercise 1's own f(t), with the MTTF (5 months) marked.
pdf1 = tibble(t = seq(0, 25, length.out = 400)) %>% mutate(f = 0.4 / (0.2 * t + 1)^3)
g = ggplot(pdf1, aes(t, f)) +
  geom_area(fill = red, alpha = 0.35) + geom_line(color = red, linewidth = 1.4) +
  geom_vline(xintercept = ex1_mttf, color = red, linewidth = 1) +
  annotate("text", x = ex1_mttf + 0.5, y = 0.3, label = "MTTF = 5", color = red,
           size = 7, fontface = "bold", hjust = 0) +
  scale_x_continuous(expand = c(0, 0)) + scale_y_continuous(expand = c(0, 0), limits = c(0, 0.42)) +
  labs(x = "Months", y = "f(t)") + theme_deck()
save(g, "gen_mttf_shaded.png")

# ---- 5. Age t and extra interval x (slide 13) ----------------------------------
# Same lognormal as chart 2; the item has survived to t = 8 and we ask about t + x = 13.
t0 = 8; x0 = 5
g = ggplot(ln, aes(t, f)) +
  geom_area(fill = red, alpha = 0.18) +
  geom_area(data = filter(ln, t >= t0 + x0), fill = red, alpha = 0.45) +
  geom_line(color = red, linewidth = 1.4) +
  geom_vline(xintercept = c(t0, t0 + x0), color = red, linewidth = 1) +
  annotate("text", x = c(t0, t0 + x0) + 0.3, y = 0.078, label = c("t", "t + x"),
           color = red, size = 8, fontface = "bold", hjust = 0) +
  scale_x_continuous(expand = c(0, 0), breaks = NULL) +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 0.085), breaks = NULL) +
  labs(x = "Months", y = "f(t)") + theme_deck()
save(g, "gen_t_plus_x.png")

# Exercise 2 (slide 15): z(t) = t/(t+1)  ->  R(t) = (t+1) e^(-t)
r_ex2 = function(t) (t + 1) * exp(-t)
ex2_mttf = integrate(r_ex2, 0, Inf)$value
mrl = function(t) integrate(function(x) r_ex2(t + x) / r_ex2(t), 0, Inf)$value
H_check = integrate(function(u) u / (u + 1), 0, 2)$value  # should equal -ln R(2)
cat(sprintf("Exercise 2: H(2) = %.4f vs -ln R(2) = %.4f; MTTF = %.4f (scan says 5 months)\n",
            H_check, -log(r_ex2(2)), ex2_mttf))
cat(sprintf("Exercise 2: MRL(t) numeric vs 1 + 1/(t+1): t=0 %.4f/%.4f, t=1 %.4f/%.4f, t=4 %.4f/%.4f\n",
            mrl(0), 1 + 1/1, mrl(1), 1 + 1/2, mrl(4), 1 + 1/5))

# ---- 6. Constant failure rate (slides 16-17) -----------------------------------
g = ggplot(tibble(t = c(0, 10), z = 1), aes(t, z)) +
  geom_line(color = red, linewidth = 2) +
  scale_x_continuous(expand = c(0, 0), breaks = NULL) +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 1.6), breaks = 1, labels = expression(lambda)) +
  labs(x = "t = time", y = "z(t)") + theme_deck()
save(g, "gen_constant_hazard.png")

# Exercise 3 (slide 18): lambda = 0.08 %/K hours = 0.08e-5 per hour
lam3 = 0.08e-5
p1 = 1 - exp(-lam3 * 20000)
t1pct = -log(1 - 0.01) / lam3
cat(sprintf("Exercise 3: F(20000) = %.5f (scan 0.016); two fail = %.6f (scan 0.016^2 = %.6f); t_1%% = %.0f h (scan 12563)\n",
            p1, p1^2, 0.016^2, t1pct))

# Slides 19-20: F(MTTF) and T50
cat(sprintf("Slide 19: F(MTTF) = 1 - 1/e = %.4f; slide 20: ln 2 = %.4f\n", 1 - exp(-1), log(2)))

# ---- 7. Light-bulb data (slide 22) ---------------------------------------------
bulbs = read_csv("workshops/bulb_lifetimes.csv", show_col_types = FALSE)
breaks = c(seq(0, 550, by = 55), Inf)
lam_hat = 1 / mean(bulbs$days)
freq = bulbs %>%
  mutate(cell = cut(days, breaks = breaks, right = TRUE, include.lowest = TRUE)) %>%
  count(cell, .drop = FALSE) %>%
  mutate(lower = head(breaks, -1), upper = tail(breaks, -1),
         expected = 100 * (r_exp(lower, lam_hat) - r_exp(upper, lam_hat)))
scan_counts = c(40, 23, 8, 10, 4, 3, 4, 4, 0, 3, 1)
freq = freq %>% mutate(scan = scan_counts, match = n == scan)
cat(sprintf("Bulbs: n = %d, mean = %.2f, lambda-hat = 1/mean = %.6f per day, total = %d\n",
            nrow(bulbs), mean(bulbs$days), lam_hat, sum(freq$n)))
print(as.data.frame(freq %>% mutate(expected = round(expected, 1))))

# Histogram (percent per 55-day cell) with the fitted exponential overlaid,
# scaled to percent per cell: 100 * 55 * f(t).
hist_d = freq %>% filter(is.finite(upper))
curve_d = tibble(t = seq(0, 600, length.out = 400)) %>% mutate(pct = 100 * 55 * f_exp(t, lam_hat))
g = ggplot() +
  geom_rect(data = hist_d, aes(xmin = lower, xmax = upper, ymin = 0, ymax = n),
            fill = red, alpha = 0.35, color = red, linewidth = 0.6) +
  geom_rect(data = tibble(xmin = 550, xmax = 605, ymax = freq$n[11]),
            aes(xmin = xmin, xmax = xmax, ymin = 0, ymax = ymax),
            fill = red, alpha = 0.35, color = red, linewidth = 0.6) +
  geom_line(data = curve_d, aes(t, pct), color = "black", linewidth = 1.3) +
  scale_x_continuous(expand = c(0, 0), breaks = seq(0, 600, 100)) +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 45), breaks = seq(0, 40, 10)) +
  labs(x = "Days to failure (last bar: > 550)", y = "Frequency (%)") + theme_deck()
save(g, "gen_bulb_histogram_pdf.png")

# Generic exponential pdf f(t) = lambda e^(-lambda t), starting at lambda (slide 22)
g = ggplot(tibble(t = seq(0, 5, length.out = 300)) %>% mutate(f = f_exp(t, 1)), aes(t, f)) +
  geom_line(color = red, linewidth = 1.8) +
  scale_x_continuous(expand = c(0, 0), breaks = NULL) +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 1.1), breaks = 1, labels = expression(lambda)) +
  labs(x = "t", y = "f(t)") + theme_deck()
save(g, "gen_exponential_pdf.png")

# ---- 8. Piecewise exponential (slide 27) ---------------------------------------
# Illustrative decreasing z(t) = 0.35 + 1.4 e^(-t/1.3); each interval [t_(i-1), t_i]
# is approximated by a constant rate equal to the average failure rate over it.
zp = function(t) 0.35 + 1.4 * exp(-t / 1.3)
steps = tibble(lo = 0:4, hi = 1:5) %>%
  rowwise() %>% mutate(afr = integrate(zp, lo, hi)$value / (hi - lo)) %>% ungroup()
g = ggplot() +
  geom_rect(data = steps, aes(xmin = lo, xmax = hi, ymin = 0, ymax = afr),
            fill = red, alpha = 0.15, color = red, linewidth = 0.9) +
  geom_line(data = tibble(t = seq(0, 5.4, length.out = 300)) %>% mutate(z = zp(t)),
            aes(t, z), color = "black", linewidth = 1.4) +
  scale_x_continuous(expand = c(0, 0), breaks = 0:5,
                     labels = c("0", expression(t[1]), expression(t[2]), expression(t[3]),
                                expression(t[4]), expression(t[5]))) +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 1.8), breaks = NULL) +
  labs(x = "Time", y = "z(t)") + theme_deck()
save(g, "gen_piecewise.png")

# Example 1 (slide 28): rotary pump, lambda = 4.28e-4 per hour, t = 730 h
lam_p = 4.28e-4
cat(sprintf("Example 1: R(730) = %.4f (scan 0.732); MTTF = %.1f h = %.2f months of 730 h (scan 2336 h = 3.2); Pr(fail in next 730 | survived) = %.4f (scan 0.268)\n",
            r_exp(730, lam_p), 1 / lam_p, 1 / lam_p / 730, 1 - r_exp(730, lam_p)))

# Example 2 (slide 29): Pr(T2 > T1) = lambda1 / (lambda1 + lambda2); check numerically
l1 = 0.002; l2 = 0.003
num = integrate(function(t) r_exp(t, l2) * f_exp(t, l1), 0, Inf)$value
cat(sprintf("Example 2 (lambda1 = %.3f, lambda2 = %.3f): integral = %.4f, closed form = %.4f\n",
            l1, l2, num, l1 / (l1 + l2)))

# ---- 9. Mixture of two exponentials (slide 30) ---------------------------------
# p = 0.4 from plant 1 (lambda1 = 1), 0.6 from plant 2 (lambda2 = 3): z(0) = 2.2,
# falling to lambda1 = 1 -- the shape and values in the scan.
p = 0.4; lam1 = 1; lam2 = 3
zmix = function(t) (p * lam1 * exp(-lam1 * t) + (1 - p) * lam2 * exp(-lam2 * t)) /
  (p * exp(-lam1 * t) + (1 - p) * exp(-lam2 * t))
cat(sprintf("Example 3: z(0) = %.3f, z(1) = %.3f, z(2) = %.3f, z(5) = %.3f; MTTF = p/l1 + (1-p)/l2 = %.4f\n",
            zmix(0), zmix(1), zmix(2), zmix(5), p / lam1 + (1 - p) / lam2))
g = ggplot(tibble(t = seq(0, 5, length.out = 400)) %>% mutate(z = zmix(t)), aes(t, z)) +
  geom_line(color = red, linewidth = 1.8) +
  scale_x_continuous(expand = c(0, 0), breaks = 0:5) +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 2.4), breaks = seq(0, 2, 0.5)) +
  labs(x = "Time t", y = "z(t)") + theme_deck()
save(g, "gen_mixture_hazard.png")
