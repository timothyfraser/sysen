#' @name qk
#' @title k-factor Quantiles
#' @description 
#' Function to return quantiles for k-factors.
#' Intended for estimating confidence intervals for failure rates.
#' @param p:[dbl] vector of probabilities / percentile(s)
#' @param r:int number of failures (non-negative integers; can include zero)
#' @param .time:logical logical; is case time-censored data?
#' @param .failure:logical logical; is case failure-censored data?
#' 
#' @importFrom dplyr `case_when`
qk = function(p, r, .time = FALSE, .failure = FALSE){
  # Testing values
  # p = 0.95; r = 20; .time = FALSE; .failure = FALSE
  
  # Input error handling
  stopifnot(is.numeric(p) & p >= 0 & p <= 1)
  stopifnot(is.numeric(as.integer(r)))
  stopifnot(is.logical(.time))
  stopifnot(is.logical(.failure))
  stopifnot(
    (.time == TRUE & .failure == FALSE) | 
      (.time == FALSE & .failure == FALSE) | 
      (.time == FALSE & .failure == TRUE) )
  stopifnot(
    # R should either be greater than 0
    (r > 0) |
      # OR 
      # zero and the data should be time censored
    (r == 0 & .time == TRUE)
  )
  
  # Evaluate if p is in the upper or lower tail
  .upper = p > 0.5
  
  # Does r == 0?
  .zerofailures = r == 0
  
  
  k = case_when(
    # 1+ failures AND complete data AND UPPER tail  --> Get k-factor for r as normal
    .zerofailures == FALSE & .time == FALSE & .failure == FALSE & .upper == TRUE ~ qchisq(p, df = 2*r) / (2*r),
    # 1+ failures AND complete data AND LOWER tail  --> Get k-factor for r as normal
    .zerofailures == FALSE & .time == FALSE & .failure == FALSE & .upper == FALSE ~ qchisq(p, df = 2*r) / (2*r),
    # 1+ failures AND time-censored data AND UPPER tail --> Get k-factor for r+1
    .zerofailures == FALSE & .time == TRUE & .failure == FALSE & .upper == TRUE ~ qchisq(p, df = 2*(r + 1) ) / (2*r),
    # 1+ failures AND time-censored data AND LOWER tail --> Get k-factor for r as normal
    .zerofailures == FALSE & .time == TRUE & .failure == FALSE & .upper == FALSE ~ qchisq(p, df = 2*(r) ) / (2*r),
    
    # 1+ failures AND time-censored data AND LOWER tail --> Get k-factor with adjustment
    .zerofailures == FALSE & .time == FALSE & .failure == TRUE & .upper == TRUE ~ qchisq(p, df = 2*( (r-1) + 1)) / (2 * (r-1))  *  (r-1)/r,
    # 1+ failures AND time-censored data AND LOWER tail --> Get k-factor with r as normal
    .zerofailures == FALSE & .time == FALSE & .failure == TRUE & .upper == FALSE ~ qchisq(p, df = 2*r) / (2*r),
    
    # If zero failures --> then time-censored --> time = TRUE, and upper/lower distinction doesn't matter.
    .zerofailures == TRUE & .time == TRUE & .failure == FALSE ~ -log(1-p),
    # Otherwise, return NA.
    TRUE ~ NA_real_
  )
  
  if(any(is.na(k))){ message("At least 1 k-factor could not be calculated, due to improper inputs. Review the rules for time-censored, failure-censored, and zero-failure data.")}
    
  return(k) 
}

#' @name rk
#' @title k-factor Random Deviates
#' @description 
#' Get a random sample of k-factor values for simulating sampling distributions of failure rates.
#' @param n:int number of observations.
#' @param r:int number of failures (non-negative integers; can include zero)
#' @param .time:logical logical; is case time-censored data?
#' @param .failure:logical logical; is case failure-censored data?
rk = function(n, r, .time = FALSE, .failure = FALSE){
  
  # Testing values
  # n = 100; r = 20; .time = FALSE; .failure = FALSE
  
  # Input error handling
  stopifnot(is.integer(as.integer(n)) & as.integer(n) > 0)
  stopifnot(is.logical(.time))
  stopifnot(is.logical(.failure))
  stopifnot(
    (.time == TRUE & .failure == FALSE) | 
      (.time == FALSE & .failure == FALSE) | 
      (.time == FALSE & .failure == TRUE) )
  
  # Does r == 0?
  .zerofailures = r == 0
  
  # Generate a uniform distribution of percentiles p
  p_uniform = runif(n = n, min = 0, max = 1)
  
  # Return quantiles for the random percentiles
  k = qk(p = p_uniform, r = r, .time = .time, .failure = .failure)
  return(k)
}

# rk(n = 1000, r = 20) %>% hist()


#' @name pk
#' @title k-factor Cumulative Distribution Function
#' @description 
#' Function to return cumulative probabilities / percentiles given a supplied k-factor quantile `q`.
#' Intended for confidence intervals for failure rates.
#' @param q:[dbl] vector of quantiles (k-factors)
#' @param r:int number of failures (non-negative integers; can include zero)
#' @param .time:logical logical; is case time-censored data?
#' @param .failure:logical logical; is case failure-censored data?
pk = function(q, r, .time = FALSE, .failure = FALSE){
  # Testing values
  # q = 2; r = 20; .time = FALSE; .failure = FALSE
  # We just need to map the function...

  # Construct an approximation function f, which gives the inverse of the Quantile Function,
  # such that you use linear interpolation to return a Probability for any Quantile supplied.
  by = 0.001
  p_range = c(by/10000, by/1000, by/100, by/10, 
              seq(from = 0, to = 1, by = 0.001),
              1 - by/10, 1 - by/100, 1 - by/1000, 1 - by/10000)
  p_range = sort(p_range)
  # Get the quantiles for that range
  q_range = qk(p = p_range, r = r, .time = .time, .failure = .failure)
  # Get the inverse quantile function
  f = approxfun(x = q_range, y = p_range, method = "linear", rule = 2, na.rm = TRUE)
  # Return the expected CDF for that quantile  
  p = f(q)
  return(p)
}


#' @name dk
#' @title k-factor Probability Density Function
#' @description 
#' Function to return probability densities given a supplied k-factor quantile `q`.
#' Intended for visualizing sampling distributions of failure rates.
#' @param x:[dbl] vector of quantiles (k-factors)
#' @param r:int number of failures (non-negative integers; can include zero)
#' @param .time:logical logical; is case time-censored data?
#' @param .failure:logical logical; is case failure-censored data?
dk = function(x, r, .time = FALSE, .failure = FALSE){
  # Testing values  
  # x = 2; r = 20; .time = FALSE; .failure = FALSE
  
  # Construct a range of quantiles corresponding to a range of cumulative probabilities
  by = 0.001
  p_range = c(by/10000, by/1000, by/100, by/10, 
              seq(from = 0, to = 1, by = 0.001),
              1 - by/10, 1 - by/100, 1 - by/1000, 1 - by/10000)
  p_range = sort(p_range)
  # Get the quantiles for that range
  q_range = qk(p = p_range, r = r, .time = .time, .failure = .failure)
  # Fit a density curve to that quantile data, truncated at 0.
  curve = density(q_range, cut = c(0))
  
  # Approximate a function
  f = approxfun(
    density(q_range, cut = c(0)), 
    method = "linear", rule = 2, na.rm = TRUE)
  # Estimate density
  d = f(x)
  return(d)
}
# Example
# dk(x = c(0, 1, 2, 3), r = 21, .time = TRUE, .failure = FALSE)
