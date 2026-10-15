# slides_w12_latin.R -------------------------------------------------------
#
# Feeds: Workshop 12 (ANOVA & Latin Squares) slides "Using 2 Types of Blocks:
#   Air Pollution" (Latin square, deviation matrices, ANOVA) and "Hyper-Graeco
#   Latin Squares: Martindale Wear Tester" (averages, ANOVA, graphical ANOVA).
#   Data: Box, Hunter & Hunter, Statistics for Experimenters, Tables 4.9-4.12.
# Run from the top of the repo:
#   Rscript functions/slides_w12_latin.R
# Reads:  workshops/anova_latin_square.csv, workshops/anova_martindale.csv
# Writes: docs-v3/images/slides/workshop-12/gen_martindale_effects.png
#         and prints every number shown on those slides.

library(dplyr)
library(tidyr)
library(ggplot2)

outdir = "docs-v3/images/slides/workshop-12"
options(width = 120)

# Helper: print a matrix with row / column names ---------------------------------
show = function(label, m) { cat("\n", label, "\n", sep = ""); print(m) }

# ==========================================================================
# 1. Latin square: 4 drivers (rows) x 4 cars (columns) x 4 additives
# ==========================================================================
ls = read.csv("workshops/anova_latin_square.csv", stringsAsFactors = FALSE) %>%
  mutate(driver = factor(driver, levels = c("I","II","III","IV")),
         car = factor(car), additive = factor(additive)) %>%
  arrange(driver, car)

grand = mean(ls$y)
cat("Latin square: grand average =", grand, "\n")

# letters as printed in the design (rows = drivers, cols = cars)
show("Additive letters (rows = drivers I-IV, cols = cars 1-4)",
     matrix(as.character(ls$additive), 4, 4, byrow = TRUE,
            dimnames = list(levels(ls$driver), levels(ls$car))))

# averages table
cat("\nAverages\n")
print(ls %>% group_by(car) %>% reframe(cars = mean(y)))
print(ls %>% group_by(driver) %>% reframe(drivers = mean(y)))
print(ls %>% group_by(additive) %>% reframe(additives = mean(y)))

# the five deviation matrices  Y - 20 = C + D + T + R
ls = ls %>%
  group_by(car) %>% mutate(C = mean(y) - grand) %>% ungroup() %>%
  group_by(driver) %>% mutate(D = mean(y) - grand) %>% ungroup() %>%
  group_by(additive) %>% mutate(T = mean(y) - grand) %>% ungroup() %>%
  mutate(V = y - grand, R = V - C - D - T)

mat = function(x) matrix(x, 4, 4, byrow = TRUE,
                         dimnames = list(levels(ls$driver), levels(ls$car)))
show("Observations y (rows = drivers, cols = cars)", mat(ls$y))
show("V: deviations from grand average (20)", mat(ls$V))
show("C: columns (cars)", mat(ls$C))
show("D: rows (drivers)", mat(ls$D))
show("T: treatments (additives)", mat(ls$T))
show("R: residuals", mat(ls$R))

cat("\nSum of squares: V =", sum(ls$V^2), " C =", sum(ls$C^2), " D =", sum(ls$D^2),
    " T =", sum(ls$T^2), " R =", sum(ls$R^2), "\n")
cat("Check 312 = 24 + 216 + 40 + 32:", sum(ls$C^2) + sum(ls$D^2) + sum(ls$T^2) + sum(ls$R^2), "\n")
cat("Degrees of freedom: 15 = 3 + 3 + 3 + 6\n")

fit_ls = aov(y ~ car + driver + additive, data = ls)
cat("\nLatin square ANOVA\n")
print(summary(fit_ls))
tab = summary(fit_ls)[[1]]
mR = tab[["Mean Sq"]][4]
cat("\nMean squares and ratios (F_3,6 = m / m_R):\n")
print(data.frame(source = c("Cars", "Drivers", "Additives", "Residuals"),
                 SS = tab[["Sum Sq"]], df = tab[["Df"]],
                 MS = round(tab[["Mean Sq"]], 2),
                 F = round(tab[["Mean Sq"]] / mR, 1),
                 p = round(tab[["Pr(>F)"]], 3)))

# ==========================================================================
# 2. Martindale wear tester: 8 cycles x 4 positions, 4 treatments, 4 holders,
#    8 emery papers (alpha-delta in Replicate I, epsilon-kappa in Replicate II)
# ==========================================================================
emery_order = c("alpha","beta","gamma","delta","epsilon","xi","theta","kappa")
m = read.csv("workshops/anova_martindale.csv", stringsAsFactors = FALSE) %>%
  mutate(replicate = factor(replicate, levels = c("I","II")),
         cycle = factor(cycle, levels = paste0("C", 1:8)),
         position = factor(position, levels = paste0("P", 1:4)),
         emery = factor(emery, levels = emery_order),
         treatment = factor(treatment), holder = factor(holder))

mg = mean(m$wear)
cat("\n\nMartindale: n =", nrow(m), " grand average =", round(mg, 1), "\n")

# the book rounds halves up (307.25 -> 307.3); R/Python round halves to even
r1 = function(x) sprintf("%.1f", floor(x * 10 + 0.5) / 10)
avg = function(v) m %>% group_by(.data[[v]]) %>% reframe(avg = r1(mean(wear)))
cat("\nAverages (Table 4.13)\n")
for (v in c("treatment", "holder", "position", "emery", "cycle", "replicate")) print(avg(v))

fit_m = aov(wear ~ replicate + cycle + position + emery + holder + treatment, data = m)
cat("\nMartindale ANOVA\n")
print(summary(fit_m))

tm = summary(fit_m)[[1]]
mRm = tm[["Mean Sq"]][7]
cat("\nANOVA table as printed on the slide (total, then each source):\n")
out = data.frame(source = c("Total", "Replications", "Cycles", "Positions", "Emery papers",
                            "Holders", "Treatments", "Residuals"),
                 df = c(sum(tm[["Df"]]), tm[["Df"]]),
                 SS = c(sum(tm[["Sum Sq"]]), tm[["Sum Sq"]]),
                 MS = c(NA, tm[["Mean Sq"]]),
                 ratio = c(NA, tm[["Mean Sq"]] / mRm))
out$ratio[8] = NA
print(out %>% mutate(SS = round(SS, 2), MS = round(MS, 2), ratio = round(ratio, 2)))
cat("\nExact residual SS =", format(tm[["Sum Sq"]][7], digits = 8),
    "(the book prints 949.04: it subtracts the rounded parts from the rounded total)\n")
cat("F for treatments =", round(tm[["F value"]][6], 2), " on", tm[["Df"]][6], "and", tm[["Df"]][7],
    "df, p =", round(tm[["Pr(>F)"]][6], 3), "\n")

# Check the transcription: these are the printed values from the textbook
want = c(603.78, 14770.44, 2217.34, 6108.94, 109.09, 1705.34, 949.04)
cat("Transcription check (max abs difference vs printed SS):",
    round(max(abs(round(tm[["Sum Sq"]], 2) - want)), 2), "\n")

# --- Graphical ANOVA (BHH Figure 4.14) -------------------------------------
# Each level is plotted at (level average - grand average), scaled by
# sqrt(nu_R / nu_factor) so that every dot is on the scale of a residual.
nuR = tm[["Df"]][7]
rows = tribble(
  ~factor,      ~var,        ~nu,
  "Replicates", "replicate", 1,
  "Cycles",     "cycle",     6,
  "Emery papers", "emery",   6,
  "Positions",  "position",  3,
  "Holders",    "holder",    3,
  "Treatments", "treatment", 3)

eff = bind_rows(lapply(seq_len(nrow(rows)), function(i) {
  v = rows$var[i]
  m %>% group_by(level = as.character(.data[[v]])) %>%
    reframe(dev = mean(wear) - mg) %>%
    mutate(factor = rows$factor[i], x = dev * sqrt(nuR / rows$nu[i]))
}))

# residuals of the fitted model (raw scale)
res = tibble(factor = "Residuals", level = "", dev = resid(fit_m), x = resid(fit_m))
cat("\nGraphical ANOVA dots (level, deviation, scaled x):\n")
print(eff %>% mutate(dev = round(dev, 1), x = round(x, 1)) %>%
        select(factor, level, dev, x), n = 40)
cat("Residuals: range", round(min(res$x), 1), "to", round(max(res$x), 1),
    " sd =", round(sd(res$x), 2), "\n")

order_rows = c("Replicates", "Cycles", "Emery papers", "Positions", "Holders",
               "Treatments", "Residuals")
# uneven row spacing: the residual strip needs the most room
row_y = setNames(c(18.3, 15.5, 12.7, 9.9, 7.1, 5.0, 1), order_rows)

# plotmath labels (subscripts, Greek)
label_for = function(f, l) {
  if (f == "Cycles") return(paste0("C[", sub("C", "", l), "]"))
  if (f == "Positions") return(paste0("P[", sub("P", "", l), "]"))
  if (f == "Emery papers") return(l)   # plotmath understands alpha, beta, ..., kappa
  l
}

# stack labels / dots that sit within `gap` x-units of one another
stack_tier = function(x, gap) {
  o = order(x); tier = integer(length(x)); last = list()
  for (i in o) {
    t = 0
    while (length(last) > t && abs(x[i] - last[[t + 1]]) < gap) t = t + 1
    tier[i] = t
    last[[t + 1]] = x[i]
  }
  tier
}

pts = bind_rows(
  eff %>% group_by(factor) %>% mutate(tier = stack_tier(x, 4.6)) %>% ungroup(),
  res %>% mutate(x = round(x / 2.3) * 2.3) %>%   # dot-plot bins, as in the book
    group_by(x) %>% mutate(tier = row_number() - 1) %>% ungroup())
pts = pts %>%
  mutate(row = row_y[factor],
         y = row + 0.09 + ifelse(factor == "Residuals", 0.48, 1.25) * tier,
         lab = ifelse(factor == "Residuals", NA, mapply(label_for, factor, level)))

ticks = expand.grid(row = row_y, x = seq(-30, 40, 10))

g = ggplot() +
  geom_segment(data = tibble(row = row_y), aes(x = -32, xend = 42, y = row, yend = row),
               color = "#c9b3ae", linewidth = 0.6) +
  geom_segment(data = ticks, aes(x = x, xend = x, y = row - 0.08, yend = row + 0.08),
               color = "#8a6a6a", linewidth = 0.5) +
  geom_point(data = pts, aes(x = x, y = y), size = 3.2, color = "#B31B1B") +
  geom_text(data = pts %>% filter(!is.na(lab)),
            aes(x = x, y = y + 0.30, label = lab), parse = TRUE,
            size = 5.6, color = "#2a1414", vjust = 0) +
  scale_x_continuous(breaks = seq(-30, 40, 10), limits = c(-33, 46)) +
  scale_y_continuous(breaks = row_y, labels = names(row_y), limits = c(0.4, 19.9)) +
  labs(x = NULL, y = NULL) +
  theme_minimal(base_size = 22) +
  theme(text = element_text(family = "sans"),
        panel.grid = element_blank(),
        axis.text = element_text(color = "#2a1414", size = 18),
        axis.text.y = element_text(hjust = 1),
        plot.background = element_rect(fill = "white", color = NA),
        panel.background = element_rect(fill = "white", color = NA))

ggsave(file.path(outdir, "gen_martindale_effects.png"), g,
       width = 8, height = 6, dpi = 200, bg = "white")
cat("\nWrote", file.path(outdir, "gen_martindale_effects.png"), "\n")
