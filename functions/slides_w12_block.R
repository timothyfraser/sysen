# slides_w12_block.R ---------------------------------------------------------
#
# Feeds: Workshop 12 (ANOVA & Latin Squares) slides "Randomized Block Design",
#   "Randomized Block Design (2)" and "Randomized Block Design (4) - Diagnostic
#   Tests" (the penicillin experiment, Box, Hunter & Hunter).
# Run from the top of the repo:
#   Rscript functions/slides_w12_block.R
# Reads:  workshops/anova_penicillin.csv  (blend, treatment, order, yield)
# Writes: docs-v3/images/slides/workshop-12/gen_pen_resid_dots.png
#         docs-v3/images/slides/workshop-12/gen_pen_resid_fitted.png
#         and prints every number shown on those slides (block and treatment
#         averages, deviations, the decomposition matrices, the ANOVA table).

library(dplyr)
library(ggplot2)

outdir = "docs-v3/images/slides/workshop-12"
pen = read.csv("workshops/anova_penicillin.csv") %>%
  mutate(treatment = factor(treatment))
stopifnot(nrow(pen) == 20)

# Averages and deviations ------------------------------------------------------
grand = mean(pen$yield)
blk = pen %>% group_by(blend) %>%
  summarize(average = mean(yield)) %>% mutate(deviation = average - grand)
trt = pen %>% group_by(treatment) %>%
  summarize(average = mean(yield)) %>% mutate(deviation = average - grand)
cat("Grand average:", grand, "\n\n")
cat("Block (blend) averages and deviations\n"); print(as.data.frame(blk))
cat("\nTreatment averages and deviations\n"); print(as.data.frame(trt))
stopifnot(grand == 86,
          blk$average == c(92, 83, 85, 88, 82), blk$deviation == c(6, -3, -1, 2, -4),
          trt$average == c(84, 85, 89, 86),     trt$deviation == c(-2, -1, 3, 0))

# Decomposition: y_bt = grand + block dev + treatment dev + residual -------------
pen = pen %>%
  left_join(blk %>% select(blend, bdev = deviation), by = "blend") %>%
  left_join(trt %>% select(treatment, tdev = deviation), by = "treatment") %>%
  mutate(dev    = yield - grand,
         fitted = grand + bdev + tdev,
         resid  = yield - fitted)

# rows = blends 1-5, columns = treatments A-D
mat = function(col) {
  m = matrix(pen[[col]], nrow = 5, byrow = TRUE)   # CSV is sorted blend, then A-D
  dimnames(m) = list(paste("Blend", 1:5), levels(pen$treatment)); m
}
Y = mat("yield"); D = mat("dev"); B = mat("bdev"); T = mat("tdev"); R = mat("resid")
cat("\nObservations y_bt\n");                        print(Y)
cat("\nDeviations from grand average y_bt - ybar\n"); print(D)
cat("\nBlock deviations ybar_b - ybar\n");            print(B)
cat("\nTreatment deviations ybar_t - ybar\n");        print(T)
cat("\nResiduals y_bt - ybar_b - ybar_t + ybar\n");   print(R)
stopifnot(all(D == B + T + R),
          D[1, ] == c(3, 2, 11, 8), D[5, ] == c(-7, -5, -6, 2),
          R[1, ] == c(-1, -3, 2, 2), R[2, ] == c(3, -5, 6, -4),
          R[3, ] == c(-2, 3, -1, 0), R[4, ] == c(1, 5, -2, -4),
          R[5, ] == c(-1, 0, -5, 6))

SD = sum(D^2); SB = sum(B^2); ST = sum(T^2); SR = sum(R^2)
cat("\nVector sums of squares:  S_D =", SD, " S_B =", SB, " S_T =", ST, " S_R =", SR,
    "\n  check S_D = S_B + S_T + S_R:", SD, "=", SB + ST + SR, "\n")
cat("Degrees of freedom:  nu_D = 19, nu_B = 4, nu_T = 3, nu_R = 12  (19 = 4 + 3 + 12)\n")
stopifnot(SD == 560, SB == 264, ST == 70, SR == 226)

# ANOVA table ---------------------------------------------------------------------
cat("\naov(yield ~ factor(blend) + treatment, data = pen)\n")
fit = aov(yield ~ factor(blend) + treatment, data = pen)
print(summary(fit))
tab = summary(fit)[[1]]
cat("\nMean squares: m_B =", round(tab[1, "Mean Sq"], 1), " m_T =", round(tab[2, "Mean Sq"], 1),
    " m_R =", round(tab[3, "Mean Sq"], 1), "\n")
cat("F ratios (exact):  F_4,12 =", round(tab[1, "F value"], 3), "  F_3,12 =", round(tab[2, "F value"], 3), "\n")
# The textbook divides the ROUNDED mean squares (66.0 / 18.8), so it prints 3.51
# where the unrounded ratio is 3.504; the slide follows the textbook.
cat("F ratios from rounded mean squares (textbook):  F_4,12 =", round(66.0 / 18.8, 2),
    "  F_3,12 =", round(23.3 / 18.8, 2), "\n")
cat("p-values:  blocks =", signif(tab[1, "Pr(>F)"], 3), "  treatments =", signif(tab[2, "Pr(>F)"], 3), "\n")
stopifnot(round(tab[1, "Mean Sq"], 1) == 66.0, round(tab[2, "Mean Sq"], 1) == 23.3,
          round(tab[3, "Mean Sq"], 1) == 18.8,
          round(66.0 / 18.8, 2) == 3.51, round(tab[2, "F value"], 2) == 1.24,
          round(tab[1, "F value"], 2) == 3.50)

# Figure 4.9: residual dot plots ---------------------------------------------------
ink  = "#4a3838"
tick = "#b8a8a8"
step = 1.4                 # vertical gap between stacked dots
stack = function(df, y0) {  # stack equal residuals upward from the row baseline y0
  df %>% group_by(r = resid) %>% mutate(k = row_number() - 1) %>% ungroup() %>%
    transmute(x = r, y = y0 + 0.9 + k * step)
}
rows = bind_rows(
  stack(pen, 44) %>% mutate(row = "all"),
  bind_rows(lapply(1:5, function(b) stack(pen %>% filter(blend == b), 36 - 4 * (b - 1)))),
  bind_rows(lapply(1:4, function(t) {
    stack(pen %>% filter(treatment == levels(pen$treatment)[t]), 14 - 4 * (t - 1))
  })))
baselines = c(44, 36 - 4 * (0:4), 14 - 4 * (0:3))
labels    = c("", paste("Block", 1:5), paste("Treatment", 1:4))
ruler = do.call(rbind, lapply(baselines, function(y0) {
  data.frame(x = -6:6, y0 = y0, h = ifelse((-6:6) %% 2 == 0, 1.0, 0.6))
}))
axis_labs = data.frame(x = seq(-6, 6, 2), y = 49.6, lab = seq(-6, 6, 2))
ptxt = 18 / .pt   # 18 pt labels

g1 = ggplot() +
  geom_segment(data = data.frame(y0 = baselines), aes(x = -6.4, xend = 6.4, y = y0, yend = y0),
               color = tick, linewidth = 0.6) +
  geom_segment(data = ruler, aes(x = x, xend = x, y = y0, yend = y0 + h),
               color = tick, linewidth = 0.6) +
  geom_point(data = rows, aes(x = x, y = y), color = ink, size = 3.4) +
  geom_text(data = axis_labs, aes(x = x, y = y, label = lab), color = ink, size = ptxt) +
  annotate("text", x = -6.8, y = baselines[-1] + 0.5, label = labels[-1], hjust = 1,
           color = ink, size = ptxt) +
  annotate("text", x = 0, y = 41.4, label = "(a)", color = ink, size = ptxt, fontface = "italic") +
  annotate("text", x = 0, y = -1.4, label = "(b)", color = ink, size = ptxt, fontface = "italic") +
  scale_x_continuous(limits = c(-12.2, 6.9), expand = c(0, 0)) +
  scale_y_continuous(limits = c(-3.2, 52), expand = c(0, 0)) +
  theme_void(base_size = 22) +
  theme(plot.background = element_rect(fill = "white", color = NA),
        plot.margin = margin(4, 8, 4, 4))
ggsave(file.path(outdir, "gen_pen_resid_dots.png"), g1, width = 5.8, height = 4.8, dpi = 200)

# Figure 4.10: residuals against predicted values ------------------------------------
g2 = ggplot(pen, aes(x = fitted, y = resid)) +
  geom_hline(yintercept = 0, color = ink, linewidth = 0.6) +
  geom_point(color = ink, size = 4.5) +
  scale_x_continuous(limits = c(79, 96), breaks = seq(80, 95, 5)) +
  scale_y_continuous(limits = c(-7, 7), breaks = seq(-6, 6, 2)) +
  labs(x = expression(hat(y)[bt]), y = expression(y[bt] - hat(y)[bt])) +
  theme_minimal(base_size = 22) +
  theme(panel.grid.minor = element_blank(),
        panel.grid.major = element_line(color = "#eddad6"),
        plot.background = element_rect(fill = "white", color = NA))
ggsave(file.path(outdir, "gen_pen_resid_fitted.png"), g2, width = 6.4, height = 4.8, dpi = 200)

cat("\nResiduals (all 20), sorted:", sort(pen$resid), "\n")
cat("Fitted range:", range(pen$fitted), "\n")
cat("Wrote gen_pen_resid_dots.png and gen_pen_resid_fitted.png\n")
