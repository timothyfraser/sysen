# slides_factorial_pilot.R ---------------------------------------------------
# Feeds: Lesson 13 (Factorial Design) and Workshop 13 slides: the pilot-plant
#   2^3 examples (grid, main, two-way, three-way effects, effects table) and
#   the lattes effects chart.
# Run from the top of the repo:  Rscript functions/slides_factorial_pilot.R
# Reads:  workshops/lattes.csv
# Writes: docs-v3/images/slides/lesson-13/gen_effects_lattes.png; prints outputs.
library(dplyr)
library(tidyr)
library(ggplot2)

# Example 1: grid + outcomes ---------------------------------------------------
grid = expand_grid(k = c("A", "B"), c = c(20, 40), t = c(160, 180)) %>%
  mutate(run = 1:n()) %>% select(run, t, c, k)
data = grid %>% mutate(y = c(60,72,54,68,52,83,45,80))
print(data)

# Example 2: direct effects ----------------------------------------------------
print(data %>% summarize(
  dbar_c = mean(y[c==40] - y[c==20]),
  dbar_t = mean(y[t==180] - y[t==160]),
  dbar_k = mean(y[k=="B"] - y[k=="A"])))

# Example 3: two-way T x K -------------------------------------------------------
print(data %>% reframe(
  xbar1 = y[(t==180 & k=="B") | (t==160 & k=="A")] %>% mean(),
  xbar0 = y[(t==160 & k=="B") | (t==180 & k=="A")] %>% mean(),
  dbar = xbar1 - xbar0))

# Example 4: three-way ----------------------------------------------------------
print(data %>% reframe(
  d1a = y[t==180&k=="A"&c==40] - y[t==160&k=="A"&c==40],
  d0a = y[t==180&k=="A"&c==20] - y[t==160&k=="A"&c==20],
  dbar_a = (d1a - d0a)/2,
  d1b = y[t==180&k=="B"&c==40] - y[t==160&k=="B"&c==40],
  d0b = y[t==180&k=="B"&c==20] - y[t==160&k=="B"&c==20],
  dbar_b = (d1b - d0b)/2,
  dbar = (dbar_b - dbar_a) / 2))

# Effects table: coded +/-1 factors, effect = 2 x coefficient -----------------------
coded = data %>% mutate(T = ifelse(t==180,1,-1), C = ifelse(c==40,1,-1), K = ifelse(k=="B",1,-1))
m = lm(y ~ T*C*K, data = coded)
print(round(2*coef(m)[-1], 2))

# Lattes effects chart ------------------------------------------------------------
lattes = read.csv("workshops/lattes.csv")
eff = function(v, hi, lo) mean(lattes$tastiness[lattes[[v]]==hi]) - mean(lattes$tastiness[lattes[[v]]==lo])
d = data.frame(
  effect = c("Syrup: Torani - Monin", "Machine: B - A", "Art: heart - foam"),
  dbar = c(eff("syrup","torani","monin"), eff("machine","b","a"), eff("art","heart","foamy")))
print(d %>% mutate(dbar = round(dbar, 2)))
g = ggplot(d, aes(x = dbar, y = reorder(effect, dbar), fill = dbar > 0)) +
  geom_col(width = 0.6) + geom_vline(xintercept = 0) +
  scale_fill_manual(values = c("TRUE" = "#B31B1B", "FALSE" = "#5b6b7a"), guide = "none") +
  labs(x = "Difference in mean tastiness", y = NULL, title = "Direct effects, lattes experiment") +
  theme_minimal(base_size = 16)
ggsave("docs-v3/images/slides/lesson-13/gen_effects_lattes.png", g, width = 7, height = 3.6, dpi = 150)
