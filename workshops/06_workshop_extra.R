# 06_workshop_extra.R


# EXERCISE 1 - Writing a Function #####################3
f = function(Eu, El, sd){     
  cp = (Eu - El) / (6 * sd)  
  return(cp)
}

# roxygen2 style commenting for functions

#' @name f
#' @title Cp Process Control Index Function
#' @description 
#' Calculate any Cp statistic with just 3 inputs! Yay!
#' @param Eu:int Upper Specification Limit
#' @param El:int Lower Specification Limit
#' @param sd:int Sigma-short (average within group standard deviation)
#' @importFrom dplyr `%>%` filter (for example)
f = function(Eu, El, sd){     
  cp = (Eu - El) / (6 * sd)  
  return(cp)
}


f(Eu = 10, El = 2, sd = 5)

# EXERCISE 2 ###################################
library(dplyr)
library(readr)
water = read_csv("workshops/onsen.csv", show_col_types = FALSE)
water %>% head() %>% glimpse()






# EXERCISE 3 #####################################


# What's bootstrapping?
# Take the existing data
# Sample with Replacement for the entire data
# Calculate a Stat
# Get a stat that has been slightly influenced by random chance




library(dplyr)
library(readr)
water = read_csv("workshops/onsen.csv", show_col_types = FALSE)

water %>%
  summarize(sigma_t = sd(temp))


# We need 1000 standard deviations
# We need 1000 resampled water datasets
# We need 1000 water datasets --- x
# We need a dataframe of 1000 ids -- x

boot = tibble(rep = 1:1000) %>%
  group_by(rep) %>%
  reframe(water) %>%
  group_by(rep) %>%
  sample_n(size = n(), replace = TRUE)

stat = boot %>%
  group_by(rep) %>%
  summarize(sigma_t = sd(temp))

stat$sigma_t %>% hist()

stat %>% 
  ungroup() %>%
  summarize(
    estimate = mean(sigma_t),
    se = sd(sigma_t),
    upper = estimate + se*qnorm(0.975),
    lower = estimate - se*qnorm(0.975) 
  )











