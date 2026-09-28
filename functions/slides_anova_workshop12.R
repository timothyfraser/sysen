# slides_anova_workshop12.R -------------------------------------------------
#
# Feeds: Workshop 12 (ANOVA & Latin Squares) slides "Case Study: Blood
#   Coagulation Times", "Two Types of Blocks: Air Pollution" (design, data, ANOVA).
# Run from the top of the repo:
#   Rscript functions/slides_anova_workshop12.R
# Writes: workshops/anova_coagulation.csv, workshops/anova_latin_square.csv,
#         docs-v3/images/slides/workshop-12/gen_coag_dotplot.png
#         and prints every number shown on those slides.

library(dplyr)
library(ggplot2)

outdir = "docs-v3/images/slides/workshop-12"

# Case study: 24 animals, 4 diets (Box, Hunter & Hunter coagulation data) -----
coag = tibble(
  diet = rep(c("A","B","C","D"), each = 6),
  time = c(62,60,63,59,63,59,
           63,67,71,64,65,66,
           68,66,71,67,68,68,
           56,62,60,61,63,64))
write.csv(coag, "workshops/anova_coagulation.csv", row.names = FALSE)

grand = mean(coag$time)
coag %>% group_by(diet) %>%
  summarize(n = n(), mean = mean(time), diff = mean(time) - grand) %>% print()

fit = aov(time ~ diet, data = coag)
print(summary(fit))

# A dot plot of the four diets, in place of the scanned figure
g = ggplot(coag, aes(x = time, y = diet)) +
  geom_vline(xintercept = grand, linetype = "dashed", color = "grey40") +
  geom_point(size = 4, alpha = 0.8, color = "#B31B1B") +
  labs(x = "Coagulation time (s)", y = "Diet",
       caption = paste0("dashed line = grand mean (", grand, ")")) +
  theme_minimal(base_size = 22)
ggsave(file.path(outdir, "gen_coag_dotplot.png"), g, width = 6, height = 4, dpi = 150)

# Latin square: 4 drivers x 4 cars x 4 additives (emissions) ------------------
ls = tibble(
  driver = rep(c("I","II","III","IV"), each = 4),
  car = rep(1:4, times = 4),
  additive = c("A","B","D","C",
               "D","C","A","B",
               "B","D","C","A",
               "C","A","B","D"),
  y = c(19,24,23,26,
        23,24,19,30,
        15,14,15,16,
        19,18,19,16)) %>%
  mutate(car = factor(car))
write.csv(ls, "workshops/anova_latin_square.csv", row.names = FALSE)

cat("\nGrand average:", mean(ls$y), "\n")
for(v in c("car","driver","additive")) {
  print(ls %>% group_by(.data[[v]]) %>% summarize(mean = mean(y)))
}
fit2 = aov(y ~ car + driver + additive, data = ls)
print(summary(fit2))
