#' @name recitation_7
#' @author Tim Fraser

library(dplyr)
library(readr)
library(ggplot2)
library(mosaicCalc)

masks <- read_csv("workshops/masks.csv")

#' @name get_chisq
#' @title Function to Get Chi-Squared!
#' @name Tim Fraser
#' If observed vector...
#' @param t a vector of times to failure
#' @param binwidth size of intervals (eg. 5 hours) (Only if t is provided)
#' If cross-tabulated data...
#' @param data a data.frame with the vectors `lower`, `upper`, and `r_obs`
#' Common Parameters:
#' @param n_total total number of units.
#' @param f specific failure function, such as `f = f(t, lambda)`
#' @param np total number of parameters in your function (eg. if exponential, 1 (lambda))
#' @param ... fill in here any named parameters you need, like `lambda = 2.4` or `rate = 2.3` or `mean = 0, sd = 2`

# TESTING VALUES
t = masks$fabric
n_total = 50
binwidth = 750
f = function(t, lambda){1 - exp(-t*lambda) }
np = 1

  
get_chisq = function(t = NULL, binwidth = 5, data = NULL, 
                     n_total, f, np = 1, ...){
  
  # If vector `t` is NOT NULL
  # Do the raw data route
  if(!is.null(t)){
    
    # Make a tibble called 'tab'
    tab = tibble(t = t) %>%
      # Part 1.1: Split into bins
      mutate(interval = cut_interval(t, length = binwidth)) %>%
      # Part 1.2: Tally up observed failures 'r_obs' by bin
      group_by(interval, .drop = FALSE) %>%
      summarize(r_obs = n()) %>%
      # Let's repeat our process from before!
      mutate(
        bin = 1:n(),
        lower = (bin - 1) * binwidth, 
        upper = bin * binwidth,
        midpoint = (lower + upper) / 2) 
    
    # Otherwise, if data.frame `data` is NOT NULL
    # Do the cross-tabulated data route
  }else if(!is.null(data)){
    tab = data %>%
      mutate(bin = 1:n(),
             midpoint = (lower + upper) / 2)
  }
  
  # Part 2. Calculate probabilities by interval
  output = tab %>% 
    mutate(
      p_upper = f(upper, ...), # supplied parameters
      p_lower = f(lower, ...), # supplied parameters
      p_fail = p_upper - p_lower,
      n_total = n_total,
      r_exp = n_total * p_fail) %>%
    # Part 3-4: Calculate Chi-Squared statistic and p-value
    summarize(
      chisq = sum((r_obs - r_exp)^2 / r_exp),
      nbin = n(),
      np = np,
      df = nbin - np - 1,
      p_value = 1 - pchisq(q = chisq, df = df) )
  
  return(output)
}

lambda  = 1 / masks$fabric %>% mean()
dat = get_chisq(t = masks$fabric, binwidth = 750, n_total = 50, f = f, np = 1, lambda = lambda) %>%
  select(interval, r_obs, p_fail, n_total, r_exp)



ggplot() +
  geom_col(data = dat, mapping = aes(x = interval, y = r_obs)) +
  geom_point(data = dat, mapping = aes(x = interval, y = r_obs)) +
  geom_col(data = dat, mapping = aes(x = interval, y = r_exp), 
           alpha = 0.5, fill = "darksalmon") +
  geom_point(data = dat, mapping = aes(x = interval, y = r_exp), 
             alpha = 0.5, fill = "darksalmon")


dat %>%
  summarize(chisq = sum((r_obs - r_exp)^2 / r_exp))
  

f = function(t, lambda){1 - exp(-t*lambda) }
lambda = 1 / masks$fabric %>% mean()
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

get_chisq(data = dat, n_total = 50, f = f, np = 1, lambda = 0.01)
get_chisq(data = dat, n_total = 50, f = pexp, np = 1, rate = 0.01)
get_chisq(data = dat, n_total = 50, f = ppois, np = 1, lambda = mean(masks$fabric))
get_chisq(data = dat, n_total = 50, f = pnorm, np = 2, 
          mean = mean(masks$fabric), sd = sd(masks$fabric))
get_chisq(data = dat, n_total = 50, f = pweibull, np = 2, 
          shape = 0.01, scale = mean(masks$fabric))



