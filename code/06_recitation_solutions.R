#' @name recitation_6.R
#' @author Tim Fraser
#' @description Super rad recitation!

library(dplyr)
library(ggplot2)
library(readr)


water = read_csv("workshops/onsen.csv")

# Capability Index (for centered, normal data)
cp = function(sigma_s, upper, lower){  abs(upper - lower) / (6*sigma_s)   }

# Process Performance Index (for centered, normal data)
pp = function(sigma_t, upper, lower){  abs(upper - lower) / (6*sigma_t)   }

# Capability Index (for skewed, uncentered data)
cpk = function(mu, sigma_s, lower = NULL, upper = NULL){
  if(!is.null(lower)){
    a = abs(mu - lower) / (3 * sigma_s)
  }
  if(!is.null(upper)){
    b = abs(upper - mu) /  (3 * sigma_s)
  }
  # We can also write if else statements like this
  # If we got both stats, return the min!
  if(!is.null(lower) & !is.null(upper)){
    min(a,b) %>% return()
    
    # If we got just the upper stat, return b (for upper)
  }else if(is.null(lower)){ return(b) 
    
    # If we got just the lower stat, return a (for lower)
  }else if(is.null(upper)){ return(a) }
}


# Process Performance Index (for skewed, uncentered data)
ppk = function(mu, sigma_t, lower = NULL, upper = NULL){
  if(!is.null(lower)){
    a = abs(mu - lower) / (3 * sigma_t)
  }
  if(!is.null(upper)){
    b = abs(upper - mu) /  (3 * sigma_t)
  }
  # We can also write if else statements like this
  # If we got both stats, return the min!
  if(!is.null(lower) & !is.null(upper)){
    min(a,b) %>% return()
    
    # If we got just the upper stat, return b (for upper)
  }else if(is.null(lower)){ return(b) 
    
    # If we got just the lower stat, return a (for lower)
  }else if(is.null(upper)){ return(a) }
}


# For example
ppk(mu = 2, sigma_t = 2.5, lower = 2.1)




# Theoretical sampling distributions
stat = water %>%
  group_by(time) %>%
  summarize(xbar = mean(temp),
            s = sd(temp),
            n_w = n()) %>%
  summarize(
    xbbar = mean(xbar), # grand mean x-double-bar
    sigma_s = sqrt(mean(s^2)), # sigma_short
    sigma_t = water$temp %>% sd(), # sigma_total!
    n = sum(n_w), # or just n = n()   # Total sample size
    n_w = unique(n_w),
    k = time %>% unique() %>% length())   # Get total subgroups


# Capability Index (for centered, normal data)
cp = function(sigma_s, upper, lower){  abs(upper - lower) / (6*sigma_s)   }



bands = stat %>% 
  summarize(
    limit_lower = 42,
    limit_upper = 50,
    # index
    estimate = cp(sigma_s = sigma_s, lower = limit_lower, upper = limit_upper),
    # Get our extra quantities of interest
    v_short = k*(n_w - 1), # get degrees of freedom
    # Get standard error for estimate
    se = estimate * sqrt(1 / (2*v_short)),
    # Get z score
    z = qnorm(0.975), # get position of 97.5th percentile in normal distribution
    lower = estimate - z * se,
    upper = estimate + z * se)

bands
# Check it!
stat


