# slides_workshop_10_density.R ----------------------------------------------
#
# Feeds: Lesson 13 (Physical Acceleration Models) slides, the "stress gap" chart.
# Lifespan under stress is a Weibull; lifespan under normal use is the SAME
# distribution stretched by the linear acceleration rule
#   f_U(t) = (1/AF) * f_S(t/AF)      (AF = 3 here)
# Run from the top of the repo:
#   Rscript functions/slides_workshop_10_density.R
# Writes: docs-v3/images/slides/workshop-10/gen_density_stress.png

library(dplyr)
library(ggplot2)

af = 3
f_s = function(t){ dweibull(t, shape = 1.2, scale = 4500) }   # density under stress
f_u = function(t){ (1 / af) * f_s(t / af) }                   # density under normal use

data = tibble(t = seq(1, 12500, length.out = 400)) %>%
  mutate(Stress = f_s(t), `Normal Usage` = f_u(t)) %>%
  tidyr::pivot_longer(cols = c(Stress, `Normal Usage`), names_to = "Conditions", values_to = "density")

print(data %>% group_by(Conditions) %>% summarize(peak = max(density), at_t = t[which.max(density)]))

g = ggplot(data, aes(x = t, y = density, color = Conditions, linetype = Conditions)) +
  geom_line(linewidth = 1.6) +
  scale_color_manual(values = c(Stress = "#3880c0", `Normal Usage` = "#B31B1B")) +
  scale_linetype_manual(values = c(Stress = "solid", `Normal Usage` = "dashed")) +
  labs(x = "Airbag lifespan in hours (t)", y = "Density, f(t)") +
  theme_minimal(base_size = 22) + theme(legend.position = "bottom")

ggsave(g, filename = "docs-v3/images/slides/workshop-10/gen_density_stress.png",
       width = 7, height = 4.6, dpi = 200, bg = "white")
