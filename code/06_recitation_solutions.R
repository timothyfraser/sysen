# 06_recitation_solutions.R
# Tim Fraser
# Recitation 6: Capability and performance indices (worked solutions)
# Chapter: Indices and Confidence Intervals for Statistical Process Control in R

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


# Why qnorm(0.975) rather than qnorm(0.95)? ###############################
# A TWO-sided 95% interval splits alpha = 0.05 across both tails
# (0.025 low + 0.025 high), so each end sits at the 97.5th percentile:
# qnorm(0.975), about 1.96. That is what `bands` above computes.
#
# But the question we actually care about here is ONE-directional:
# "is Cp below 1?" For that, report a one-sided UPPER bound (a ceiling):
# put ALL of alpha in the upper tail, so use qnorm(0.95), about 1.645.
# (A floor - "Cp is at least..." - would be a one-sided LOWER bound,
# estimate - z * se, with the same qnorm(0.95).)
# See the chapter's "One-Sided Bounds" subsection:
# https://timothyfraser.com/sigma/chapters/indices-and-confidence-intervals-for-statistical-process-control-in-r.html#one-sided-bounds

alpha = 0.05 # 95% confidence

ceiling_cp = stat %>%
  summarize(
    estimate = cp(sigma_s = sigma_s, lower = 42, upper = 50),
    v_short = k*(n_w - 1), # degrees of freedom
    se = estimate * sqrt(1 / (2*v_short)),
    # ALL of alpha in one tail: the 95th percentile, not the 97.5th
    z = qnorm(1 - alpha), # about 1.645
    upper = estimate + z * se) # a ceiling: "Cp is at most..."

ceiling_cp
# The 95% one-sided upper bound (about 0.735) is still well below 1,
# so we are 95% confident the true Cp is LESS THAN 1: not capable.
# It is a little tighter than the two-sided upper end in `bands`
# (about 0.747), because no alpha was spent on the low tail.


