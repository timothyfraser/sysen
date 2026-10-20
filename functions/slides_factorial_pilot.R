# slides_factorial_pilot.R ---------------------------------------------------
# Feeds: Lesson 13 (Factorial Design) and Workshop 13 slides: the pilot-plant
#   2^3 examples (grid, main, two-way, three-way effects, effects table) and
#   the lattes effects chart.
# Run from the top of the repo:  Rscript functions/slides_factorial_pilot.R
# Reads:  workshops/lattes.csv
# Writes: docs-v3/images/slides/lesson-13/gen_effects_lattes.png (effects plot:
#   one box per effect, "estimate (SE)"); prints outputs.
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
# Effects plot (Tim's 2025 form): one labelled box per effect at its estimate.
# Coded +/-1 factors on the 240 lattes; effect = 2 x coefficient, SE = 2 x SE(coef).
lc = lattes %>% mutate(S = ifelse(syrup == "torani", 1, -1),
                       M = ifelse(machine == "b", 1, -1),
                       A = ifelse(art == "heart", 1, -1))
ml = lm(tastiness ~ S * M * A, data = lc)
est = summary(ml)$coefficients[-1, , drop = FALSE]
# names: S = Syrup (Torani vs Monin), M = Machine (b vs a), A = Art (heart vs foamy)
fx = data.frame(term = rownames(est), estimate = 2 * est[, "Estimate"],
                se = 2 * est[, "Std. Error"], row.names = NULL) %>%
  mutate(effect = recode(term, "S" = "Syrup", "M" = "Machine", "A" = "Art",
                         "S:M" = "S x M", "S:A" = "S x A",
                         "M:A" = "M x A", "S:M:A" = "S x M x A"),
         effect = factor(effect, levels = rev(effect)),
         label = sprintf("%.1f (%.1f)", estimate, se))
print(fx %>% mutate(across(c(estimate, se), ~ round(.x, 2))) %>% select(effect, estimate, se, label))
lim = max(abs(fx$estimate))
g = ggplot(fx, aes(x = estimate, y = effect)) +
  geom_vline(xintercept = 0, colour = "#1f1f1f", linewidth = 0.8) +
  geom_label(aes(label = label, fill = estimate), size = 6.5, fontface = "bold",
             label.padding = unit(0.35, "lines"), label.size = 0.6, colour = "#1f1f1f") +
  scale_fill_gradient2(low = "#3880c0", mid = "#ffffff", high = "#B31B1B", midpoint = 0,
                       limits = c(-lim, lim), name = "Effect") +
  scale_x_continuous(limits = range(fx$estimate) + c(-17, 17)) +
  labs(x = "Effect on tastiness", y = NULL) +
  theme_minimal(base_size = 20) +
  theme(axis.text = element_text(size = 18, colour = "#1f1f1f"),
        panel.grid.minor = element_blank(), legend.key.height = unit(1.4, "lines"))
ggsave("docs-v3/images/slides/lesson-13/gen_effects_lattes.png", g, width = 7, height = 3.6, dpi = 150, bg = "white")
