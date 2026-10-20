# Recitation 12 -- the restaurant tracking table (R twin of slides_workshop_8_table.py).
# Run from the top of the repo:  Rscript functions/slides_workshop_8_table.R
library(readr)
library(dplyr)

d = read_csv("workshops/bistro_tracking.csv", show_col_types = FALSE)
print(d)
# Done = TRUE rows are tinted blue, FALSE rows orange (the slide's colour coding)
d %>% count(done)
