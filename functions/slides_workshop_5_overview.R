# slides_workshop_5_overview.R
#
# Draws the process overview chart on the Workshop 5 slides
# ("Coding Demo" -- the hot-spring data before the Q1-Q11 questions).
#
# Run it from the top of the sysen folder:
#   Rscript functions/slides_workshop_5_overview.R
# Figures are saved into `out_dir` (defaults to the current folder).

library(dplyr)
library(readr)
library(ggplot2)
source("functions/functions_process_control.R")
set_theme()

args = commandArgs(trailingOnly = TRUE)
if (!exists("out_dir")) out_dir = if (length(args) > 0) args[1] else "."

# Hot-spring (onsen) data: 20 samples per month, 8 months --------------------
water = read_csv("workshops/onsen.csv", show_col_types = FALSE)
print(water %>% group_by(time) %>% summarize(n = n(), xbar = mean(temp), s = sd(temp)))

# Process overview: boxplot per subgroup + the histogram on its side ---------
g = ggprocess(x = water$time, y = water$temp,
              xlab = "Subgroup (month)", ylab = "Temperature (C)")

ggsave(file.path(out_dir, "gen_onsen_overview.png"), g, width = 8, height = 4, dpi = 200)
