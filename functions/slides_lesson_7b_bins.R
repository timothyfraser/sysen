# slides_lesson_7b_bins.R -- bin tables, expected counts and the histogram + exponential figure
# for the Lesson 11B deck (cross-tabulated data, chi-squared goodness of fit).
# Run from the repo root:  Rscript functions/slides_lesson_7b_bins.R
library(dplyr)
library(readr)
library(ggplot2)

bulbs = read_csv("workshops/bulb_lifetimes.csv", show_col_types = FALSE)

# 1. Cross-tabulate the 100 bulb times into equal intervals ---------------
tab = function(width, upper) {
  breaks = c(seq(0, upper, by = width), Inf)
  bulbs %>%
    mutate(bin = cut(days, breaks = breaks, labels = FALSE)) %>%
    count(bin, name = "r") %>%
    tidyr::complete(bin = seq_along(breaks[-1]), fill = list(r = 0L)) %>%   # keep empty intervals (441-495 has 0)
    mutate(bin_size = width,
           lower = (bin - 1) * width,
           upper = ifelse(bin * width > upper, NA, bin * width),
           mid = lower + width / 2)
}
bins = bind_rows(tab(55, 550), tab(110, 330), tab(100, 400)) %>%
  select(bin_size, bin, lower, upper, r, mid)
write_csv(bins, "workshops/lesson7b_bins.csv")
print(bins, n = 30)

# 2. Example: lambda-hat from the complete sample -------------------------
r = nrow(bulbs); total = sum(bulbs$days)
cat("complete sample: r =", r, " total =", total, " lambda-hat =", round(r / total, 5), "\n")

# 3. Example: lambda-hat from the 100-hour cross-tab ----------------------
b100 = bins %>% filter(bin_size == 100)
t_sum = sum(b100$mid * b100$r)
lam = sum(b100$r) / t_sum
cat("cross-tab: r =", sum(b100$r), " t_sum =", t_sum, " lambda-hat =", round(lam, 5), "\n")

# 4. Expected counts and chi-squared (the last interval is 401-500) -------
edges = c(0, 100, 200, 300, 400, 500)
p_exp = diff(1 - exp(-lam * edges))
exp_tbl = tibble(interval = c("0-100", "101-200", "201-300", "301-400", ">=401"),
                 r = b100$r, F2 = (1 - exp(-lam * edges))[-1], F1 = (1 - exp(-lam * edges))[-6],
                 p_exp = p_exp, r_exp = p_exp * 100) %>%
  mutate(term = (r - r_exp)^2 / r_exp)
print(exp_tbl %>% mutate(across(where(is.numeric), ~ round(.x, 4))))
chisq = sum(exp_tbl$term)
df_ = nrow(exp_tbl) - 1 - 1
cat("chi-squared =", round(chisq, 2), " df =", df_, " critical (95%) =", round(qchisq(0.95, df_), 2),
    " p =", signif(1 - pchisq(chisq, df_), 3), "\n")

# 5. Figure: histogram (percent) with the fitted exponential density -------
lam55 = 0.0074
g = ggplot(bulbs, aes(x = days)) +
  geom_histogram(aes(y = after_stat(density)), binwidth = 55, boundary = 0,
                 fill = "#B31B1B", colour = "white", alpha = 0.9) +
  stat_function(fun = dexp, args = list(rate = lam55), linewidth = 1.4, colour = "#302050") +
  labs(x = "days to failure", y = "density") +
  theme_minimal(base_size = 24)
ggsave("docs-v3/images/slides/lesson-7b/gen_bulb_hist_exp.png", g, width = 7.5, height = 4.6, dpi = 150)

# 6. Figure: observed vs expected counts, 100-hour intervals ---------------
# observed = carnelian bars; expected = navy outlined bars (exp. model at lambda-hat)
ov = exp_tbl %>%
  mutate(interval = factor(interval, levels = interval, labels = c("0-100", "101-200", "201-300", "301-400", "401+")))
g2 = ggplot(ov, aes(x = interval)) +
  geom_col(aes(y = r), fill = "#B31B1B", width = 0.8, alpha = 0.9) +
  geom_col(aes(y = r_exp), fill = NA, colour = "#302050", linewidth = 1.6, width = 0.8) +
  labs(x = "interval (hours)", y = "failures") +
  theme_minimal(base_size = 24) + theme(axis.text.x = element_text(size = 17))   # slide 14 shows it beside a table: big type
ggsave("docs-v3/images/slides/lesson-7b/gen_obs_exp.png", g2, width = 7, height = 4.6, dpi = 150)
