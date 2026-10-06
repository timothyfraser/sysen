# slides_lesson_12_shoes.R
# Replication script for Lesson 12 Slide 16 (Example 2 - Paired Samples: the Data)
# Recreates Box, Hunter & Hunter Figure 3.5:
# Amount of wear for 10 boys comparing Material A vs Material B
# Writes to docs-v3/images/slides/lesson-12/gen_boys_shoes_scatter.png

library(dplyr)
library(ggplot2)

red = "#B31B1B"
outdir = "docs-v3/images/slides/lesson-12"
if (!dir.exists(outdir)) dir.create(outdir, recursive = TRUE)

# Data from Slide 15 / BHH Table 3.5
shoes_data = tibble(
  boy = 1:10,
  wear_A = c(13.2, 8.2, 10.9, 14.3, 10.7, 6.6, 9.5, 10.8, 8.8, 13.3),
  wear_B = c(14.0, 8.8, 11.2, 14.2, 11.8, 6.4, 9.8, 11.3, 9.3, 13.6)
)

shoes_long = bind_rows(
  shoes_data %>% transmute(boy, material = "Material A", wear = wear_A),
  shoes_data %>% transmute(boy, material = "Material B", wear = wear_B)
)

# Plot: boy on x-axis (1 to 10), wear on y-axis, connected pairs + dots
p = ggplot(shoes_data) +
  geom_segment(aes(x = boy, xend = boy, y = wear_A, yend = wear_B),
               color = "grey60", linewidth = 0.8, linetype = "dashed") +
  geom_point(data = shoes_long, aes(x = boy, y = wear, color = material, shape = material),
             size = 4, stroke = 1.2) +
  scale_color_manual(values = c("Material A" = "grey25", "Material B" = red)) +
  scale_shape_manual(values = c("Material A" = 16, "Material B" = 1)) +
  scale_x_continuous(breaks = 1:10, expand = expansion(add = 0.6)) +
  scale_y_continuous(breaks = seq(6, 16, by = 2), limits = c(5.5, 15.5)) +
  labs(
    title = "Boys' Shoes: Sole Wear by Boy (Matched Pairs)",
    x = "Boy",
    y = "Sole Wear",
    color = "Treatment",
    shape = "Treatment"
  ) +
  theme_classic(base_size = 15) +
  theme(
    plot.title = element_text(face = "bold", size = 15, hjust = 0.5),
    axis.title = element_text(face = "bold"),
    axis.text = element_text(color = "black"),
    legend.position = "bottom",
    legend.title = element_text(face = "bold")
  )

ggsave(file.path(outdir, "gen_boys_shoes_scatter.png"), p, width = 6.8, height = 4.8, dpi = 200, bg = "white")
cat("Generated boys shoes scatter plot successfully.\n")
