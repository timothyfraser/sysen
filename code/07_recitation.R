# 07_recitation.R
# Tim Fraser
# Recitation 7: Chi-squared goodness-of-fit tests
# Chapter: Statistical Techniques for Exponential Distributions in R

library(dplyr)
library(readr)
library(ggplot2)
library(mosaicCalc)

masks <- read_csv("workshops/masks.csv")

# get_chisq() and the helpers it calls live in this file
source("functions/functions_mle.R")

# TESTING VALUES
t = masks$fabric
n_total = 50
binwidth = 750
f = function(t, lambda){1 - exp(-t*lambda) }
np = 1
lambda = 1 / mean(masks$fabric)

# get_chisq() hands back only the TEST result: chisq, nbin, np, df, p_value, min_exp.
# To plot observed against expected we need the table of cells itself:
# Step 1 (crosstab), Step 2-3 (expected counts, plus a last cell to infinity
# for the units that had not failed), Step 4 (merge cells until each expects at least 5).
tab = tibble(t = t) %>%
  mutate(interval = cut_interval(t, length = binwidth)) %>%
  group_by(interval, .drop = FALSE) %>%
  summarize(r_obs = n()) %>%
  mutate(bin = 1:n(),
         lower = (bin - 1) * binwidth,
         upper = bin * binwidth)

dat = tab %>%
  .chisq_cells(n_total = n_total, f = f, lambda = lambda) %>%
  .pool_cells() %>%
  mutate(cell = paste0(lower, "-", upper))

ggplot() +
  geom_col(data = dat, mapping = aes(x = reorder(cell, lower), y = r_obs)) +
  geom_point(data = dat, mapping = aes(x = reorder(cell, lower), y = r_obs)) +
  geom_col(data = dat, mapping = aes(x = reorder(cell, lower), y = r_exp), 
           alpha = 0.5, fill = "darksalmon") +
  geom_point(data = dat, mapping = aes(x = reorder(cell, lower), y = r_exp), 
             alpha = 0.5, fill = "darksalmon") +
  labs(x = "cell", y = "units")

# Step 5: Chi-squared statistic from the merged cells
dat %>%
  summarize(chisq = sum((r_obs - r_exp)^2 / r_exp))

# The same test in one call
get_chisq(t = masks$fabric, binwidth = 750, 
          n_total = 50, f = f, np = 1, lambda = lambda)

# chisq
# n_total - total number of observation
# np - total # of parameters
# lambda - our parameter (failure rate)
# f - exponential - CDF - failure function
# binwidth - size of interval 
# df - 
# p_value


# Reminders
# TA Evals


rchisq(n = 1000, df = 3) %>% hist()



ggplot() +
  geom_histogram(data = tibble(x = rchisq(n = 1000, df = 3)),
                 mapping = aes(x = x)) +
  geom_vline(xintercept = 10, color = "red")



dat = dplyr::tribble(
  ~lower, ~upper, ~r_obs,
  0,      100,    50,
  100,    200,    43,
  200,    300,    20,
  300,    400,    10,
  400,    500,    5
)

dat = tibble(
  lower = c(0, 100, 200, 300, 400),
  upper = c(100, 200, 300, 400, 500),
  r_obs = c(50, 43, 20, 10, 5)
)

get_chisq(data = dat, n_total = 128, f = f, np = 1, lambda = 0.01)
get_chisq(data = dat, n_total = 128, f = pexp, np = 1, rate = 0.01)
get_chisq(data = dat, n_total = 128, f = ppois, np = 1, lambda = mean(masks$fabric))
get_chisq(data = dat, n_total = 128, f = pnorm, np = 2, 
          mean = mean(masks$fabric), sd = sd(masks$fabric))
get_chisq(data = dat, n_total = 128, f = pweibull, np = 2, 
          shape = 0.01, scale = mean(masks$fabric))



