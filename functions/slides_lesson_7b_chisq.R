# slides_lesson_7b_chisq.R -- numbers + figure for the Lesson 7B deck.
# Run from the repo root:  Rscript functions/slides_lesson_7b_chisq.R
library(dplyr)
library(readr)
library(ggplot2)

# 1. Lambda from the complete bulb sample ---------------------------------
bulbs = read_csv("workshops/bulb_lifetimes.csv", show_col_types = FALSE)
r = nrow(bulbs)          # every bulb failed, so r = n = 100
total = sum(bulbs$days)  # total unit test time
lambda_hat = r / total
cat("r =", r, " total =", total, "\n")
cat("lambda-hat =", round(lambda_hat, 6), "-> rounded", round(lambda_hat, 4), "\n")
cat("MTTF = 1/lambda-hat =", round(1 / lambda_hat, 2), " ; 1/0.0074 =", round(1/0.0074, 2),
    " ; sample mean =", mean(bulbs$days), "\n")

# 2. Critical values: qchisq(p = ci, df) ----------------------------------
cis = c(0.005, 0.025, 0.80, 0.90, 0.95, 0.975, 0.98, 0.99, 0.995, 0.998, 0.999)
crit = expand.grid(df = 1:21, ci = cis) %>%
  mutate(chisq = qchisq(p = ci, df = df))
crit_wide = crit %>% mutate(ci = paste0("ci_", ci * 100)) %>%
  tidyr::pivot_wider(names_from = ci, values_from = chisq)
write_csv(crit_wide, "workshops/lesson7b_chisq_critical.csv")
print(crit %>% filter(df <= 10, ci %in% c(0.90, 0.95, 0.99)) %>%
        mutate(chisq = round(chisq, 2)) %>% tidyr::pivot_wider(names_from = ci, values_from = chisq))

# 3. Figure: chi-squared density with the 5% critical region (df = 5) -----
df_ = 5
cut = qchisq(0.95, df_)
d = tibble(x = seq(0, 25, length.out = 500)) %>% mutate(y = dchisq(x, df_))
g = ggplot(d, aes(x = x, y = y)) +
  geom_area(data = d %>% filter(x >= cut), fill = "#B31B1B", alpha = 0.8) +
  geom_line(linewidth = 1.3) +
  geom_vline(xintercept = cut, linetype = "dashed") +
  annotate("text", x = cut + 0.6, y = 0.12, hjust = 0, size = 7,
           label = paste0("critical value = ", round(cut, 2))) +
  annotate("text", x = 2, y = 0.05, size = 7, label = "95% of cases\nby chance") +
  annotate("text", x = 14, y = 0.02, size = 7, colour = "#B31B1B", label = "5% tail:\nsignificant") +
  labs(x = "chi-squared statistic (df = 5)", y = "density") +
  theme_minimal(base_size = 20)
dir.create("docs-v3/images/slides/lesson-7b", showWarnings = FALSE, recursive = TRUE)
ggsave("docs-v3/images/slides/lesson-7b/gen_density_df5.png", g, width = 7, height = 4.2, dpi = 150)
cat("wrote figure, cut =", round(cut, 4), "\n")
