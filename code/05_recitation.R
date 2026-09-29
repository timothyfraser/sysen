# 05_recitation.R
# Tim Fraser
# Recitation 5: Statistical process control practice
# Chapter: Statistical Process Control in R

# This is the WORKED version of recitation 5: every exercise is filled in.
# Run it from the top of the sysen folder, so the file paths below work.

# 0. Setup ##################################################
# Load packages
library(dplyr)
library(readr)
library(ggplot2)
library(ggpubr)

# Load data
water = read_csv("workshops/onsen.csv", show_col_types = FALSE)

# Take a look: each row is one reading from one hot spring sensor,
# taken at a subgroup 'time', with temperature, pH, and sulfur.
water %>% glimpse()


# Exercise 1 ###############################################


# Load functions
# ***You'll need to go add this script for this to work.
# https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.R
source("functions/functions_process_control.R")


# Exercise 2 ###############################################


# Pick a quality metric from our onsen dataset,
# and generate averages, standard deviation, and range plots,
# using our helper functions.

# We'll pick pH. (temp works the same way - swap 'ph' for 'temp'.)

# Averages chart: is the MEAN pH of each subgroup stable over time?
g_avg = ggxbar(x = water$time, y = water$ph,
               xlab = "Time (Subgroups)", ylab = "Average pH")

# Standard deviation chart: is the SPREAD of pH within each subgroup stable?
g_s = ggs(x = water$time, y = water$ph,
          xlab = "Time (Subgroups)", ylab = "SD of pH")

# Range chart: same question as the sd chart, using max - min instead.
g_r = ggr(x = water$time, y = water$ph,
          xlab = "Time (Subgroups)", ylab = "Range of pH")

# View them side by side
ggarrange(g_avg, g_s, g_r, nrow = 1)

# Now get the numbers behind the charts.
# get_stat_s() gives one row per subgroup, with the centerline (xbbar),
# the within-subgroup sigma (sigma_s), and the +/- 3 standard error limits.
stat = get_stat_s(x = water$time, y = water$ph)
stat

# The centerlines and averages-chart limits, summarized in one row
centerlines = stat %>%
  summarize(
    subgroups = n(),
    nw = mean(nw),
    xbbar = mean(xbar),     # centerline of the averages chart
    sbar = sqrt(mean(s^2)), # centerline of the sd chart (pooled sigma_s)
    rbar = mean(r),         # centerline of the range chart
    lower = min(lower),     # averages chart: xbbar - 3 * sigma_s / sqrt(nw)
    upper = max(upper)      # averages chart: xbbar + 3 * sigma_s / sqrt(nw)
  )
centerlines %>% mutate(across(everything(), ~round(.x, 3))) %>% as.data.frame() %>% print()

# The sd and range charts use control constants (B3/B4, D3/D4).
# The helpers estimate them by simulation, so their limits can wobble
# in the second decimal from run to run. One row each:
limits_s(x = water$time, y = water$ph) %>%
  summarize(sbar = mean(sbar), lower = mean(lower), upper = mean(upper))
limits_r(x = water$time, y = water$ph) %>%
  summarize(rbar = mean(rbar), lower = mean(lower), upper = mean(upper))

# How many subgroup averages fall outside the averages-chart limits?
stat %>%
  summarize(out_of_control = sum(xbar > upper | xbar < lower))

# Describe the process under study.

# The onsen sensors record pH several times per subgroup (nw readings each).
# - The averages chart: every subgroup average sits inside xbbar +/- 3 se,
#   so mean pH looks stable over time - no special-cause shifts.
# - The sd and range charts: within-subgroup variation stays inside its
#   limits too, so the spread is stable - the process is 'in control'.
# - In control is not the same as good: it means the process is predictable.
#   Whether pH is acceptable for bathers is a question for spec limits,
#   which is next week's topic (capability indices).


# Exercise 3 ###############################################


# Write your own chart function.
# In workshop 5 we made a jittered process plot (g1) and a sideways
# histogram (g2), then put them together with ggarrange().
# Let's wrap those steps in a function, so any metric is one line.

myprocess = function(x, y, xlab = "Subgroup", ylab = "Metric"){
  # Put the two vectors in one data.frame
  data = tibble(x = x, y = y)

  # Every reading over time, jittered so they don't overlap
  g1 = ggplot() +
    geom_jitter(data = data, mapping = aes(x = x, y = y),
                width = 0.25, height = 0, alpha = 0.5) +
    # add the grand mean as a reference line
    geom_hline(yintercept = mean(data$y), color = "steelblue") +
    labs(x = xlab, y = ylab, subtitle = "Process Over Time")

  # ...and their distribution, on its side
  g2 = ggplot() +
    geom_histogram(data = data, mapping = aes(x = y),
                   bins = 15, fill = "steelblue", color = "white") +
    coord_flip() +
    labs(x = NULL, y = "Count", subtitle = "Distribution")

  # Bundle them together, and return the result
  gg = ggarrange(g1, g2, widths = c(5, 2))
  return(gg)
}

# Try it on pH...
g_ph = myprocess(x = water$time, y = water$ph, xlab = "Time (Subgroups)", ylab = "pH")
g_ph

# ...and on temperature, with no new code
g_temp = myprocess(x = water$time, y = water$temp, xlab = "Time (Subgroups)", ylab = "Temperature (C)")
g_temp

# Compare against the course helper, ggprocess(), which does the same job
ggprocess(x = water$time, y = water$ph, xlab = "Time (Subgroups)", ylab = "pH")
