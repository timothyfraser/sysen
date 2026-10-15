# slides_w12_anova.R --------------------------------------------------------
#
# Feeds: Workshop 12 (ANOVA & Latin Squares) slides "Case Study: Blood
#   Coagulation Times", "ANOVA: Analysis of Variance", "Calculating Deviations
#   in ANOVA", "Quantities of Interest in ANOVA", "F-statistic in ANOVA",
#   "Example 5" (3+ group means, donuts) and "Example 6" (K^2 and Welch ANOVA).
#   Data: Box, Hunter & Hunter's blood coagulation study (24 animals, 4 diets,
#   run order in the `order` column) and workshops/donuts.csv.
# Run from the top of the repo:
#   Rscript functions/slides_w12_anova.R
# Writes: workshops/anova_coagulation.csv (diet, time, order),
#         docs-v3/images/slides/workshop-12/gen_coag_dots.png
#         docs-v3/images/slides/workshop-12/gen_coag_dots_means.png
#         docs-v3/images/slides/workshop-12/gen_coag_dots_gray.png
#         docs-v3/images/slides/workshop-12/gen_f_curve.png
#         docs-v3/images/slides/workshop-12/gen_donuts_violin.png
#         and prints every number shown on those slides.

library(dplyr)
library(readr)
library(broom)
library(ggplot2)

outdir = "docs-v3/images/slides/workshop-12"

# Palette shared with the slide tables: tones for fills, strong partners for marks
tone   = c(A = "#f0b068", B = "#8878c0", C = "#a0c0f0", D = "#d08080")   # tan, purple, blue, rose
strong = c(A = "#f0c030", B = "#6048a0", C = "#a0c0f0", D = "#B31B1B")   # yellow, purple, light blue, red
dotcol = "#4a3838"
rowof  = c(A = 1, B = 2, C = 3, D = 4)                                    # D at the top

# 1. Data: 24 animals, 4 diets, with the random run order of the testing ------
coag = tibble(
  diet  = rep(c("A", "B", "C", "D"), each = 6),
  time  = c(62, 60, 63, 59, 63, 59,
            63, 67, 71, 64, 65, 66,
            68, 66, 71, 67, 68, 68,
            56, 62, 60, 61, 63, 64),
  order = c(20, 2, 11, 10, 5, 24,
            12, 9, 15, 14, 4, 8,
            16, 7, 1, 17, 13, 21,
            23, 3, 6, 18, 22, 19))
write_csv(coag, "workshops/anova_coagulation.csv")

cat("\n== Run order check: orders 1..24 each used once ==\n")
print(all(sort(coag$order) == 1:24))

# 2. Averages and differences -----------------------------------------------
grand = mean(coag$time)
cat("\n== Treatment averages, grand average, differences ==\n")
avgs = coag %>% group_by(diet) %>%
  summarize(n = n(), mean = mean(time), diff = mean(time) - grand)
print(avgs)
cat("Grand average:", grand, "\n")

# 3. The deviation matrices (rows = observation 1-6, columns = diets A-D) ---
Y = sapply(c("A", "B", "C", "D"), function(d) coag$time[coag$diet == d])
rownames(Y) = 1:6
D = Y - grand                                  # deviations from the grand average of 64
T = matrix(rep(avgs$mean - grand, each = 6), nrow = 6,
           dimnames = dimnames(Y))              # treatment deviations
R = D - T                                      # residuals within treatments
cat("\n== Y: observations ==\n");                                  print(Y)
cat("\n== D = Y - 64: deviations from the grand average ==\n");   print(D)
cat("\n== T: treatment deviations ==\n");                          print(T)
cat("\n== R = D - T: residuals within treatments ==\n");           print(R)

cat("\n== Sums of squares and degrees of freedom ==\n")
cat("SS: D =", sum(D^2), " T =", sum(T^2), " R =", sum(R^2),
    " check D = T + R:", sum(D^2) == sum(T^2) + sum(R^2), "\n")
k = 4; n = 24
cat("df: D =", n - 1, " T =", k - 1, " R =", n - k, "\n")
cat("Mean squares: m_T =", sum(T^2) / (k - 1), " m_R =", sum(R^2) / (n - k),
    " F =", (sum(T^2) / (k - 1)) / (sum(R^2) / (n - k)), "\n")

# 4. The ANOVA ---------------------------------------------------------------
cat("\n== summary(aov(time ~ diet)) ==\n")
fit = aov(time ~ diet, data = coag)
print(summary(fit))
cat("\n== F(3, 20) points: 5%, 1%, 0.1% ==\n")
qf_pts = qf(c(.95, .99, .999), 3, 20)
print(qf_pts)
print(round(qf_pts, 2))

# 5. Charts ------------------------------------------------------------------
base_theme = theme_minimal(base_size = 22) +
  theme(panel.grid = element_blank(),
        axis.title = element_blank(),
        axis.text.y = element_text(face = "italic", size = 24, colour = "#2a1414"),
        axis.text.x = element_text(size = 20, colour = "#2a1414"),
        axis.ticks.x = element_blank(),
        axis.line.x = element_blank(),
        plot.background = element_rect(fill = "white", colour = NA),
        plot.margin = margin(8, 14, 4, 8))

# stack tied observations upward within (diet, time), like a dot plot
dots = coag %>%
  mutate(row = rowof[diet]) %>%
  group_by(diet, time) %>%
  mutate(stack = row_number()) %>%
  ungroup() %>%
  mutate(y = row + 0.14 + 0.24 * (stack - 1))

# soft density blob per diet, drawn on the diet's own row
blobs = bind_rows(lapply(c("A", "B", "C", "D"), function(d) {
  x = coag$time[coag$diet == d]
  dd = density(x, bw = 1.1, from = max(min(x) - 1.6, 55.4), to = min(max(x) + 1.6, 71.6), n = 200)
  tibble(diet = d, x = dd$x, row = rowof[[d]], h = dd$y / max(dd$y) * 0.68)
}))

row_lines = tibble(row = 1:4)
ticks = expand.grid(row = 1:4, x = c(56, 61, 66, 71))

# pieces every dot plot shares: rows, ticks, axes
rows_layer = list(
  geom_segment(data = row_lines, aes(x = 56, xend = 71, y = row, yend = row),
               colour = "#2a1414", linewidth = 0.5, inherit.aes = FALSE),
  geom_segment(data = ticks, aes(x = x, xend = x, y = row - 0.07, yend = row + 0.07),
               colour = "#2a1414", linewidth = 0.5, inherit.aes = FALSE),
  scale_x_continuous(breaks = c(56, 61, 66, 71), limits = c(55.4, 71.6), expand = c(0, 0)),
  scale_y_continuous(breaks = 1:4, labels = c("A", "B", "C", "D")))

blob_layer = geom_ribbon(data = blobs,
                         aes(x = x, ymin = row, ymax = row + h, fill = diet),
                         alpha = 0.55, colour = NA, inherit.aes = FALSE)
dot_layer  = function(size = 5.5) geom_point(data = dots, aes(x = time, y = y),
                                             colour = dotcol, size = size)

# (a) PDF p10: blobs + dots
g1 = ggplot() +
  blob_layer + scale_fill_manual(values = tone, guide = "none") +
  rows_layer + dot_layer(5) +
  coord_cartesian(ylim = c(0.72, 4.8), clip = "off") +
  base_theme
ggsave(file.path(outdir, "gen_coag_dots.png"), g1, width = 7.4, height = 2.5, dpi = 200, bg = "white")

# (b) PDF p11: + grand mean line and a labelled group-mean tick per diet
means = avgs %>% mutate(row = rowof[diet], col = strong[diet])
# side the label sits on, matching the PDF: D and A to the left, C and B to the right
means$hj = c(A = 1, B = 0, C = 0, D = 1)[means$diet]
means$lx = means$mean + ifelse(means$hj == 1, -0.35, 0.35)
g2 = ggplot() +
  blob_layer + scale_fill_manual(values = tone, guide = "none") +
  rows_layer +
  # connectors from each group mean to the grand mean, then the strong ticks
  geom_segment(data = means, aes(x = mean, xend = grand, y = row + 0.62, yend = row + 0.62),
               colour = "#2a1414", linewidth = 0.45, inherit.aes = FALSE) +
  dot_layer(5) +
  geom_segment(aes(x = grand, xend = grand, y = 0.72, yend = 4.95),
               colour = "#4a3838", linewidth = 1.6) +
  annotate("text", x = grand + 0.35, y = 4.95, label = "grand mean",
           hjust = 0, size = 7.4, colour = "#4a3838") +
  geom_segment(data = means, aes(x = mean, xend = mean, y = row, yend = row + 0.62, colour = diet),
               linewidth = 2.2, inherit.aes = FALSE) +
  geom_text(data = means, aes(x = lx, y = row + 0.66, label = "group mean", hjust = hj, colour = diet),
            size = 7.4, vjust = 0, fontface = "plain", inherit.aes = FALSE) +
  scale_colour_manual(values = strong, guide = "none") +
  scale_x_continuous(breaks = c(56, 61, 66, 71), limits = c(55.4, 74.5), expand = c(0, 0)) +
  coord_cartesian(ylim = c(0.72, 5.15), clip = "off") +
  base_theme
ggsave(file.path(outdir, "gen_coag_dots_means.png"), g2, width = 7.4, height = 2.6, dpi = 200, bg = "white")

# (c) PDF p12: plain dark grey dots, no blobs
g3 = ggplot() + rows_layer + dot_layer(4.2) +
  coord_cartesian(ylim = c(0.72, 4.55), clip = "off") +
  base_theme
ggsave(file.path(outdir, "gen_coag_dots_gray.png"), g3, width = 7.4, height = 2.5, dpi = 200, bg = "white")

# (d) PDF p14: the F(3, 20) curve with its 5 %, 1 %, 0.1 % points and the observed ratio
xs = seq(0.02, 14.5, length.out = 600)
curve = tibble(x = xs, y = df(xs, 3, 20))
pts = tibble(q = qf_pts, lab = c("5% point", "1% point", "0.1% point"),
             ytop = c(0.30, 0.20, 0.12), dens = df(qf_pts, 3, 20))
g4 = ggplot(curve, aes(x, y)) +
  geom_line(linewidth = 1.3, colour = "black") +
  geom_segment(data = pts, aes(x = q, xend = q, y = ytop - 0.02, yend = dens + 0.012),
               arrow = arrow(length = unit(0.16, "in"), type = "closed"),
               linewidth = 0.9, colour = "#2a1414", inherit.aes = FALSE) +
  geom_text(data = pts, aes(x = q, y = ytop, label = lab), vjust = 0, size = 6.4,
            colour = "#2a1414", inherit.aes = FALSE) +
  annotate("segment", x = 13.6, xend = 13.6, y = 0.27, yend = 0.045,
           arrow = arrow(length = unit(0.16, "in"), type = "closed"),
           linewidth = 0.9, colour = "#B31B1B") +
  annotate("point", x = 13.6, y = 0.0, size = 4.5, colour = "#B31B1B") +
  annotate("text", x = 14.4, y = 0.285, label = "Observed ratio = 13.6", hjust = 1, vjust = 0,
           size = 6.4, colour = "#B31B1B") +
  scale_x_continuous(breaks = seq(0, 14, 2), limits = c(0, 14.6), expand = c(0, 0)) +
  scale_y_continuous(limits = c(-0.01, 0.74), expand = c(0, 0)) +
  labs(x = "F", y = NULL) +
  theme_minimal(base_size = 22) +
  theme(panel.grid = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks.x = element_line(colour = "#2a1414"),
        axis.line.x = element_line(colour = "#2a1414"),
        plot.background = element_rect(fill = "white", colour = NA))
ggsave(file.path(outdir, "gen_f_curve.png"), g4, width = 7, height = 3.8, dpi = 200, bg = "white")

# 6. Examples 5 and 6: donuts (Tim's slide code) ----------------------------
donuts = read_csv("workshops/donuts.csv", show_col_types = FALSE)

cat("\n== Example 5: lm() route ==\n")
donuts %>%
  summarize(lm(weight ~ baker) %>% glance()) %>%
  select(sigma, statistic, p.value, df) %>%
  print()

cat("\n== Example 5: aov() route ==\n")
donuts %>%
  reframe(aov(weight ~ baker) %>% tidy()) %>%
  print()

cat("\n== Example 6: Bartlett's K^2 test ==\n")
bartlett.test(weight ~ baker, data = donuts) %>% print()

cat("\n== Example 6: Welch's ANOVA (no equal-variance assumption) ==\n")
donuts %>%
  summarize(oneway.test(weight ~ baker, data = donuts, var.equal = FALSE) %>% tidy()) %>%
  print()

cat("\n== Donut baker means, grand mean, n ==\n")
dm = donuts %>% group_by(baker) %>% summarize(n = n(), mean = mean(weight), sd = sd(weight))
print(dm)
dgrand = mean(donuts$weight)
cat("Grand mean:", dgrand, "\n")

# (e) PDF p15: violins per baker, Craig at the bottom
donuts = donuts %>% mutate(baker = factor(baker, levels = c("Craig", "Kim", "Melanie")))
dm = dm %>% mutate(baker = factor(baker, levels = levels(donuts$baker)))
set.seed(12)
g5 = ggplot(donuts, aes(x = weight, y = baker)) +
  geom_vline(xintercept = dgrand, colour = "#3880c0", linewidth = 1) +
  geom_violin(orientation = "y", fill = "white", colour = "black", linewidth = 0.7, scale = "area") +
  geom_jitter(width = 0, height = 0.05, size = 1.8, colour = "black") +
  geom_point(data = dm, aes(x = mean, y = baker), colour = "#3880c0", size = 6) +
  labs(x = "weight", y = "baker") +
  theme_minimal(base_size = 20) +
  theme(panel.grid.minor = element_blank(),
        panel.grid.major = element_line(colour = "#e4e4e4"),
        plot.background = element_rect(fill = "white", colour = NA))
ggsave(file.path(outdir, "gen_donuts_violin.png"), g5, width = 3.4, height = 5.7, dpi = 200, bg = "white")

cat("\nDone: wrote workshops/anova_coagulation.csv and five PNGs in", outdir, "\n")
