# Feeds Lesson 6 (process capability) slides 4 and 7-9: capable vs not capable, and the four kinds.
# Run from the sigma repo root:  Rscript functions/slides_lesson_6_figures.R
# Writes gen_capable.png, gen_not_capable.png (1100x700) and gen_four_kinds.png (1600x1000)
#   to docs-v3/images/slides/lesson-6/. Seeded, so reruns are identical.
# Python twin: functions/slides_lesson_6_figures.py (same parameters, different random draws).
library(dplyr)
library(ggplot2)

set.seed(6)
out = "docs-v3/images/slides/lesson-6"
red = "#B31B1B"; band = "#E3E3E3"
lsl = 20; usl = 30; nominal = 25

# ---- (a) capable vs not capable: density against the spec band ----
# Size is in inches x dpi = pixels; base_size 10 at 200 dpi reads like 20pt at 100 dpi.
plot_capability = function(sd, file) {
  d = tibble(x = seq(12, 38, length.out = 800)) %>%
    mutate(y = dnorm(x, nominal, sd))
  g = ggplot(d, aes(x = x, y = y)) +
    annotate("rect", xmin = lsl, xmax = usl, ymin = -Inf, ymax = Inf, fill = band) +
    geom_area(data = filter(d, x <= lsl), fill = red, alpha = 0.55) +
    geom_area(data = filter(d, x >= usl), fill = red, alpha = 0.55) +
    geom_vline(xintercept = nominal, linetype = "dashed", linewidth = 0.7) +
    geom_line(color = red, linewidth = 1.6) +
    scale_x_continuous(breaks = c(lsl, nominal, usl),
                       labels = c("LSL\n20", "Nominal\n25", "USL\n30"),
                       limits = c(12, 38), expand = c(0, 0)) +
    scale_y_continuous(expand = expansion(mult = c(0, 0.04))) +
    labs(x = "Minutes", y = NULL) +
    theme_classic(base_size = 10) +
    theme(axis.text.y = element_blank(), axis.ticks.y = element_blank(),
          axis.line.y = element_blank(), plot.margin = margin(2, 4, 2, 2))
  ggsave(file.path(out, file), g, width = 5.5, height = 3.5, dpi = 200, bg = "white")
}
plot_capability(1.2, "gen_capable.png")
plot_capability(3.5, "gen_not_capable.png")

# ---- (b) the four kinds: 12 subgroups x 5 points against the spec band ----
k = 12; n = 5
kinds = c("Stable and capable", "Stable and incapable",
          "Unstable but potentially capable", "Unstable and incapable")
params = bind_rows(
  tibble(kind = kinds[1], t = 1:k, mu = 25,                     s = 1.2),
  tibble(kind = kinds[2], t = 1:k, mu = 25,                     s = 3.5),
  tibble(kind = kinds[3], t = 1:k, mu = seq(19.5, 30.5, length.out = k), s = 1.2),
  tibble(kind = kinds[4], t = 1:k, mu = seq(22, 28, length.out = k),     s = seq(2, 5, length.out = k))
)
pts = params %>%
  slice(rep(1:n(), each = n)) %>%
  mutate(y = rnorm(n(), mu, s), kind = factor(kind, levels = kinds),
         out = y < lsl | y > usl)
means = pts %>% group_by(kind, t) %>% summarize(y = mean(y), .groups = "drop")

g = ggplot(pts, aes(x = t, y = y)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = lsl, ymax = usl, fill = band) +
  geom_hline(yintercept = nominal, linetype = "dashed", linewidth = 0.5) +
  geom_boxplot(aes(group = t), width = 0.55, color = "grey35", fill = NA,
               outlier.shape = NA, linewidth = 0.5) +
  geom_point(aes(color = out), size = 1.6, alpha = 0.9) +
  geom_line(data = means, color = red, linewidth = 1) +
  scale_color_manual(values = c("FALSE" = "grey30", "TRUE" = red), guide = "none") +
  scale_x_continuous(breaks = c(1, 6, 12), expand = expansion(add = 0.5)) +
  scale_y_continuous(breaks = c(lsl, nominal, usl)) +
  facet_wrap(~kind, ncol = 2) +
  labs(x = "Subgroup (time)", y = "Minutes") +
  theme_classic(base_size = 9) +
  theme(strip.text = element_text(size = 11, face = "bold"),
        strip.background = element_blank(), panel.spacing = unit(0.6, "lines"),
        plot.margin = margin(2, 4, 2, 2))
ggsave(file.path(out, "gen_four_kinds.png"), g, width = 8, height = 5, dpi = 200, bg = "white")
