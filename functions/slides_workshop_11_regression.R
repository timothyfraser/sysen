# slides_workshop_11_regression.R
# Regenerates the chart on the Workshop 10 "Coding Demo" divider: the simple
# regression of social capital on tsunami damage, with its line of best fit.
# Run from the repo root:  source("functions/slides_workshop_11_regression.R")
# Data: workshops/jp_matching_experiment.csv
library(dplyr)
library(readr)
library(ggplot2)

out = "docs-v3/images/slides/workshop-11/"

cities = read_csv("workshops/jp_matching_experiment.csv", show_col_types = FALSE) %>%
  # Tell R to treat year and pref as **ordered categories**
  mutate(year = factor(year),
         pref = factor(pref),
         by_tsunami = factor(by_tsunami, levels = c("Not Hit", "Hit")))

# A simple regression model 'm'
m = cities %>% lm(formula = social_capital ~ damage_rate)
print(round(coef(m), 4))  # 0.3942 + 0.0749 * damage_rate

g = ggplot(cities, aes(x = damage_rate, y = social_capital)) +
  geom_point(aes(fill = by_tsunami), shape = 21, size = 2.6, alpha = .75, color = "#2a1414") +
  geom_smooth(method = "lm", formula = y ~ x, color = "#B31B1B", fill = "#d08080", linewidth = 1.6) +
  scale_fill_manual(values = c("Not Hit" = "#a0c0f0", "Hit" = "#f0b068"), name = NULL) +
  labs(title = "As X increases, what happens to Y?",
       x = "Damage rate (X)", y = "Social capital (Y)") +
  theme_classic(base_size = 20) +
  theme(legend.position = "top")
ggsave(paste0(out, "gen_regression.png"), g, width = 7.5, height = 5.2, dpi = 110, bg = "white")
