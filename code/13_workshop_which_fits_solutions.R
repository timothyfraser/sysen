#' @name 13_workshop_which_fits_solutions.R
#' @title Which Distribution Fits? Worked Solutions
#' @author Tim Fraser

# For each lifespan data set, fit the exponential, Weibull, gamma and lognormal
# with get_mle(), and compare the four log-likelihoods.
# Run from the top of the project folder.

library(dplyr)
library(readr)
source("functions/functions_mle.R")

dists = c("exponential", "weibull", "gamma", "lognormal")

# One function: fit all four distributions to a vector of failure times.
# Give n_total and tmax if some units had not failed when the test stopped.
compare = function(t, n_total = NULL, tmax = NULL){
  tibble(dist = dists) %>%
    rowwise() %>%
    mutate(loglik = if(is.null(n_total)){
      get_mle(t = t, dist = dist)$loglik
    } else {
      get_mle(t = t, n_total = n_total, tmax = tmax, dist = dist)$loglik
    }) %>%
    ungroup() %>%
    arrange(desc(loglik)) %>%
    mutate(gap = loglik - lead(loglik))
}

# Read in the data ##################################################
crops = read_csv("workshops/crops.csv")
bulbs = read_csv("workshops/bulb_lifetimes.csv")
masks = read_csv("workshops/masks.csv")
batteries = read_csv("workshops/batteries.csv")
drones = read_csv("workshops/drones.csv")
capacitors = read_csv("workshops/workshop9_capacitors.csv")
pumps = read_csv("workshops/pumps.csv")
fans = read_csv("workshops/fans.csv")
valves = read_csv("workshops/valves.csv")

# Fit all four, one data set at a time ###############################
results = bind_rows(
  compare(crops$days) %>% mutate(data = "crops"),
  compare(bulbs$days) %>% mutate(data = "bulb lifetimes"),
  compare(masks$left_earloop) %>% mutate(data = "masks, left earloop"),
  compare(masks$fabric) %>% mutate(data = "masks, fabric"),
  compare(batteries %>% filter(battery_type == "alkaline") %>% pull(life_hours)) %>% mutate(data = "alkaline batteries"),
  compare(batteries %>% filter(battery_type == "lithium") %>% pull(life_hours)) %>% mutate(data = "lithium batteries"),
  compare(drones$flight_time) %>% mutate(data = "drones"),
  # 50 on test, 25 failed, test stopped at the last failure
  compare(capacitors$t, n_total = 50, tmax = max(capacitors$t)) %>% mutate(data = "capacitors"),
  compare(pumps$hours) %>% mutate(data = "pumps"),
  compare(fans$hours) %>% mutate(data = "fans"),
  compare(valves$hours) %>% mutate(data = "valves")
) %>%
  select(data, dist, loglik, gap)

# Print the four log-likelihoods per data set, best first
results %>%
  group_by(data) %>%
  summarize(
    best = first(dist),
    gap = round(first(gap), 1),
    verdict = if_else(first(gap) >= 2, "clear win", "tie: prefer the simpler model"),
    loglik = paste(dist, round(loglik, 1), collapse = ", ")
  ) %>%
  arrange(match(data, unique(results$data))) %>%
  print(width = Inf)

# One line per fit, for checking against the key
results %>% mutate(loglik = round(loglik, 1)) %>% print(n = Inf)
