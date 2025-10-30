# ZZ_financial_impacts.R

# A script to help you do financial impact analysis!

# Load packages!
library(dplyr)
library(readr)
source("functions/functions_process_control.R")


# Get my data
data = read_csv("workshops/onsen.csv")
cost = 50 # cost of refund per visit that is too cold

data %>% glimpse()


# Create some function that will perform an analysis and return a data.frame....

#' @name ggxbar2
#' @title Modified Average Control Chart with ggplot
#' @param x [numeric] vector of subgroup values (usually time). Must be same length as `y`.
#' @param y [numeric] vector of metric values (eg. performance). Must be same length as `x`.
#' @note Dependency: `get_stat_t()`, `get_stat_s()`, `get_labels()` functions
ggxbar2 = function(x,y, xlab = "Time (Subgroups)", ylab = "Average"){
  
  # Testing values 
  # water = read_csv("workshops/onsen.csv");
  # x = water$time; y = water$temp; xlab = "Time (Subgroups)"; ylab = "Average"
  data = tibble(x = x, y = y)
  
  # Get statistics for each subgroup
  stat_s = get_stat_s(x = data$x, y = data$y)
  
  return(stat_s)
}

# STEP 2: Write a jumbo function f that calculates an n-failures statistic
# or some single statistic of interest for your dataset

# averages plot of temperature, focusing on lower control limit
f = function(data){
  stat = ggxbar2(x = data$time, y = data$temp, xlab = "Stuff", ylab = "More Stuff") %>%
    select(x, lower)
  
  # If they are all the same...
  # lcl = stat$lower[1]
  result = data %>%
    left_join(by = c("time" = "x"), y = stat) %>%
    mutate(fail = temp < lower) %>%
    summarize(n_fail = sum(fail))
   
  return(result) 
}

# STEP 3: Test it! Does bootstrapping (sampling with replacement) change it?
data %>% f()
data %>% sample_n(size = n(), replace = TRUE) %>% f()

# STEP 4: ITERATE WITH for-loop

# STEP 4A: for-loop version
holder = data.frame()
for(i in 1:1000){
  data_i = data %>% sample_n(size = n(), replace = TRUE) %>% f()
  holder = bind_rows(holder, data_i)
}
boot = holder

# STEP 4B: ITERATE WITH group_by
# Alternatively, use a tibble with group_by
boot = tibble(rep = 1:1000) %>%
  group_by(rep) %>%
  reframe(data) %>%
  group_by(rep) %>%
  sample_n(size = n(), replace = TRUE) %>%
  group_by(rep) %>%
  summarize(  f(data = tibble(time, temp))  )

# STEP 5: COST & CONFIDENCE INTERVALS
# Calculate cost and uncertainty
boot %>%
  mutate(total_cost = n_fail * cost) %>%
  summarize(
    estimate = quantile(total_cost, prob = 0.50),
    se = sd(total_cost),
    lower = quantile(total_cost, prob = 0.025),
    upper = quantile(total_cost, prob = 0.975)
  )


# STEP 6: FUNCTIONIFY IT!
# Write a qi() function to return your quantities of interest 
# any time your input dataframe data changes!
qi = function(data){
  
  # Alternatively, use a tibble with group_by
  boot = tibble(rep = 1:1000) %>%
    group_by(rep) %>%
    reframe(data) %>%
    group_by(rep) %>%
    sample_n(size = n(), replace = TRUE) %>%
    group_by(rep) %>%
    summarize(  f(data = tibble(time, temp))  )
  
  # Calculate cost and uncertainty
  df = boot %>%
    mutate(total_cost = n_fail * cost) %>%
    summarize(
      estimate = quantile(total_cost, prob = 0.50),
      se = sd(total_cost),
      lower = quantile(total_cost, prob = 0.025),
      upper = quantile(total_cost, prob = 0.975)
    )
  
  return(df)
  
}


# STEP 7: COMPARE SCENARIOS!

# Baseline scenario
s1 = data %>% qi()

# Suppose you made a specific change to the system
s2 = data %>%
  # eg. you modify the ph, driving up the temperature
  mutate(temp = if_else(ph > 6, true = temp * 1.6, false = temp)) %>%
  # Recompute the cost.
  qi()

# Compare the result!
bind_rows(s1, s2)


