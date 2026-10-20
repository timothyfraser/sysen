# slides_factorial_replicates.R ---------------------------------------------
# Feeds: the factorial-design decks' "standard error of an effect" slide.
#   Data: Box, Hunter & Hunter pilot plant 2^3, each run made twice (BHH
#   Table 5.3); the run means are the yields 60, 72, 54, 68, 52, 83, 45, 80.
# Run from the top of the repo:  Rscript functions/slides_factorial_replicates.R
# Reads:  workshops/pilot_plant_replicates.csv (run, t, c, k, y1, y2)
# Writes: nothing; prints d, d^2/2, s^2, Var(effect) and SE(effect).
library(dplyr)
library(readr)

reps = read_csv("workshops/pilot_plant_replicates.csv", show_col_types = FALSE)

# Each run's two yields give a 1-df variance estimate: s_i^2 = d^2 / 2
reps = reps %>% mutate(ybar = (y1 + y2) / 2, d = y1 - y2, d2_half = d^2 / 2)
print(reps)

# Pool the eight estimates; an effect is a difference of two means of 8 runs
out = reps %>% summarize(
  s2 = sum(d2_half) / n(),
  var_effect = (1/8 + 1/8) * s2,
  se_effect = round(sqrt(var_effect), 2))
print(out)
