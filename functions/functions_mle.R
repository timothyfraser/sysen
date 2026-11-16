# What this file is ----------------------------------------------------------
#
# Functions that fit a life distribution (exponential, Weibull, gamma or
# lognormal) to failure data by maximum likelihood, and then test the fit with
# chi-squared. They work on a cross-tabulation: a tibble with one row per
# time interval and the columns `lower`, `upper` and `r_obs` (the number of
# failures in that interval). They also work on a vector of exact failure times.
#
# Units still running when the test ended are counted too. Tell the functions
# how many units were on test (`n_total`) and when the test stopped (`tmax`).
#
# The chi-squared test follows the eight steps in Tobias and Trindade, Applied
# Reliability (3rd ed., section 3.8). Its last cell runs from the end of the
# table to infinity and holds every unit that had not failed, so the expected
# counts add up to the number on test. Cells with fewer than 5 expected
# failures are merged with a neighbour before the statistic is added up.
#
# Load it, from the top of the project folder:
#   source("functions/functions_mle.R")
#
# Then try:
#   crops = tibble(lower = seq(0, 160, 40), upper = lower + 40,
#                  r_obs = c(18, 14, 10, 5, 3))
#   get_fit(data = crops, n_total = 75, tmax = 200)  # does each family fit?
#
# You never need to edit anything below.
#
# What is in here:
#   plife(), dlife(), qlife(), rlife(), hlife()  the four distributions
#   get_mle()      fit one distribution
#   get_expected() observed and expected failures, by interval
#   get_chisq()    chi-squared test of a fit
#   get_fit()      fit and test all four distributions at once
#

#' @name functions_mle.R
#' @title Functions for Fitting Life Distributions to Failure Data

library(dplyr)
library(tibble)

# Parameter names, in order, for each distribution
.life_names = list(
  exponential = "lambda",
  weibull = c("m", "c"),
  gamma = c("k", "lambda"),
  lognormal = c("t50", "sigma"))

# Check the distribution name, and pull out its parameters by name
.life_args = function(dist, ...){
  if(length(dist) != 1 || !(dist %in% names(.life_names))){
    stop("Unknown `dist`: '", paste(dist, collapse = ", "),
         "'. Use one of: ", paste(names(.life_names), collapse = ", "), ".", call. = FALSE)
  }
  a = list(...)
  need = .life_names[[dist]]
  miss = setdiff(need, names(a))
  if(length(miss) > 0){
    stop("For dist = '", dist, "', please supply: ", paste(need, collapse = ", "),
         ". Missing: ", paste(miss, collapse = ", "), ".", call. = FALSE)
  }
  a
}

# Failure function, on the scale you ask for
.life_p = function(t, dist, a, lower.tail = TRUE, log.p = FALSE){
  switch(dist,
    exponential = pexp(t, rate = a$lambda, lower.tail = lower.tail, log.p = log.p),
    weibull = pweibull(t, shape = a$m, scale = a$c, lower.tail = lower.tail, log.p = log.p),
    gamma = pgamma(t, shape = a$k, rate = a$lambda, lower.tail = lower.tail, log.p = log.p),
    lognormal = pnorm(log(t / a$t50) / a$sigma, lower.tail = lower.tail, log.p = log.p))
}

#' @name plife
#' @title Failure Function F(t) for Any of the Four Life Distributions
#' @param t a vector of times
#' @param dist one of "exponential", "weibull", "gamma", "lognormal"
#' @param ... the parameters, by course name:
#'   exponential `lambda`; Weibull `m` (shape) and `c` (characteristic life);
#'   gamma `k` (shape) and `lambda` (rate); lognormal `t50` (median) and `sigma`.

# Testing values
# plife(t = 500, dist = "lognormal", t50 = 1000, sigma = 0.8)
plife = function(t, dist, ...){
  a = .life_args(dist, ...)
  .life_p(t, dist, a)
}

#' @name dlife
#' @title Density f(t) for Any of the Four Life Distributions
#' @param t a vector of times
#' @param dist one of "exponential", "weibull", "gamma", "lognormal"
#' @param ... the parameters, by course name (see plife)

# Testing values
# dlife(t = 500, dist = "weibull", m = 1.5, c = 1300)
dlife = function(t, dist, ...){
  a = .life_args(dist, ...)
  switch(dist,
    exponential = dexp(t, rate = a$lambda),
    weibull = dweibull(t, shape = a$m, scale = a$c),
    gamma = dgamma(t, shape = a$k, rate = a$lambda),
    lognormal = dlnorm(t, meanlog = log(a$t50), sdlog = a$sigma))
}

#' @name qlife
#' @title Quantile (Time by Which a Share p Has Failed)
#' @param p a vector of probabilities between 0 and 1
#' @param dist one of "exponential", "weibull", "gamma", "lognormal"
#' @param ... the parameters, by course name (see plife)

# Testing values
# qlife(p = 0.5, dist = "lognormal", t50 = 1000, sigma = 0.8)   # the median, 1000
qlife = function(p, dist, ...){
  a = .life_args(dist, ...)
  switch(dist,
    exponential = qexp(p, rate = a$lambda),
    weibull = qweibull(p, shape = a$m, scale = a$c),
    gamma = qgamma(p, shape = a$k, rate = a$lambda),
    lognormal = a$t50 * exp(a$sigma * qnorm(p)))
}

#' @name rlife
#' @title Random Failure Times
#' @param n how many times to draw
#' @param dist one of "exponential", "weibull", "gamma", "lognormal"
#' @param ... the parameters, by course name (see plife)

# Testing values
# set.seed(1); rlife(n = 5, dist = "exponential", lambda = 0.001)
rlife = function(n, dist, ...){
  a = .life_args(dist, ...)
  switch(dist,
    exponential = rexp(n, rate = a$lambda),
    weibull = rweibull(n, shape = a$m, scale = a$c),
    gamma = rgamma(n, shape = a$k, rate = a$lambda),
    lognormal = rlnorm(n, meanlog = log(a$t50), sdlog = a$sigma))
}

#' @name hlife
#' @title Cumulative Hazard H(t) = -log(1 - F(t))
#' @param t a vector of times
#' @param dist one of "exponential", "weibull", "gamma", "lognormal"
#' @param ... the parameters, by course name (see plife)

# Testing values
# hlife(t = 1000, dist = "exponential", lambda = 0.001)   # 1
hlife = function(t, dist, ...){
  a = .life_args(dist, ...)
  # log of the reliability, computed directly so it stays accurate when F is tiny
  -.life_p(t, dist, a, lower.tail = FALSE, log.p = TRUE)
}

# Tidy a crosstab before anything else: right columns, numbers only, no gaps,
# sorted by `lower`, no overlaps. Returns the sorted crosstab.
.clean_crosstab = function(data){
  miss = setdiff(c("lower", "upper", "r_obs"), names(data))
  if(length(miss) > 0){
    stop("`data` is missing the column(s): ", paste(miss, collapse = ", "),
         ". It needs `lower`, `upper` and `r_obs`.", call. = FALSE)
  }
  bad = c("lower", "upper", "r_obs")[!vapply(data[c("lower", "upper", "r_obs")], is.numeric, logical(1))]
  if(length(bad) > 0){
    stop("Column(s) ", paste(bad, collapse = ", "), " must be numbers, not text or factors. ",
         "Convert them with as.numeric().", call. = FALSE)
  }
  if(anyNA(data$lower) || anyNA(data$upper) || anyNA(data$r_obs)){
    stop("`lower`, `upper` and `r_obs` must not have missing (NA) values. Remove or fill those rows.", call. = FALSE)
  }
  if(any(!is.finite(data$upper))){
    stop("`upper` must be finite in every row. Put units still running in `n_total`, ",
         "not in a last open interval.", call. = FALSE)
  }
  if(any(data$r_obs < 0)){
    stop("`r_obs` has a negative count. Failure counts must be 0 or more.", call. = FALSE)
  }
  if(any(data$upper <= data$lower)){
    stop("`upper` must be greater than `lower` in every row (found upper <= lower).", call. = FALSE)
  }
  data = data %>% arrange(lower)
  if(any(data$lower[-1] < data$upper[-nrow(data)])){
    stop("Intervals overlap: a row starts before the previous one ends. ",
         "Each `lower` must be at or after the previous `upper`.", call. = FALSE)
  }
  data
}

# Check the numbers that go with the data (call .clean_crosstab() first for a crosstab)
.check_data = function(data, t, n_total, tmax, np){
  if(is.null(data) && is.null(t)){
    stop("Please supply either `data` (a crosstab) or `t` (a vector of failure times).", call. = FALSE)
  }
  if(!is.numeric(n_total) || length(n_total) != 1 || !is.finite(n_total)){
    stop("`n_total` must be a single number (not NA). Give the number of units on test.", call. = FALSE)
  }
  if(!is.null(data)){
    if(!is.null(tmax) && any(data$r_obs > 0 & data$upper > tmax)){
      stop("`tmax` (", tmax, ") falls before the end of an interval that holds failures. ",
           "`tmax` must be at or after the end of the last interval with failures.", call. = FALSE)
    }
    r = sum(data$r_obs)
    cells = sum(data$r_obs > 0)
  }else{
    if(!is.numeric(t) || anyNA(t)){
      stop("`t` must be numbers with no missing (NA) values.", call. = FALSE)
    }
    if(any(t <= 0)){
      stop("Failure times must be greater than 0. Remove zero or negative values from `t`.", call. = FALSE)
    }
    if(!is.null(tmax) && any(t > tmax)){
      stop("Some failure times in `t` are after `tmax` (", tmax, "). `tmax` must be at or after the last failure.", call. = FALSE)
    }
    r = length(t)
    cells = r
  }
  if(n_total < r){
    stop("`n_total` (", n_total, ") is smaller than the number of failures (", r, "). ",
         "Give the total units on test.", call. = FALSE)
  }
  if(n_total > r){ cells = cells + 1 }
  if(cells < np + 1){
    stop("Too few non-empty cells (", cells, ") to fit ", np, " parameter(s). ",
         "Need at least ", np + 1, " (survivors cell included).", call. = FALSE)
  }
  invisible(TRUE)
}

#' @name get_mle
#' @title Fit a Life Distribution by Maximum Likelihood
#' @param data a tibble with `lower`, `upper`, `r_obs` (one row per interval, in time order)
#' @param t instead of `data`: a vector of exact failure times
#' @param n_total units on test. Default: the number of failures (complete data).
#' @param tmax time the unfailed units were still running. Default: the largest
#'   `upper` (or the largest `t`). Time-censored: the planned end of the test.
#'   Failure-censored: the time of the last failure.
#' @param dist one of "exponential", "weibull", "gamma", "lognormal"
#' @param lik "interval" (default) uses F(upper) - F(lower) for each interval;
#'   "midpoint" uses the density at each interval's midpoint. Ignored if you give `t`.
#'   `loglik` from the two forms cannot be compared with each other.
#' @returns one row: `dist`, the parameters, `loglik`, `np`, `r`, `n_total`,
#'   `tmax`, `lik`, `converged`.

# Testing values
# crops = tibble(lower = seq(0, 160, 40), upper = lower + 40, r_obs = c(18, 14, 10, 5, 3))
# get_mle(data = crops, n_total = 75, tmax = 200, dist = "weibull")   # m 0.832, c 172.9
get_mle = function(data = NULL, t = NULL, n_total = NULL, tmax = NULL,
                   dist = "exponential", lik = "interval"){

  # Check the family first, so a typo gets a clear message
  names_par = .life_names[[if(length(dist) == 1 && dist %in% names(.life_names)) dist else ""]]
  if(is.null(names_par)){ .life_args(dist) }
  np = length(names_par)
  if(!(lik %in% c("interval", "midpoint"))){
    stop("Unknown `lik`: '", lik, "'. Use \"interval\" or \"midpoint\".", call. = FALSE)
  }

  # Defaults for the number of units and the stopping time
  if(!is.null(data)){ data = .clean_crosstab(data) }
  r = if(!is.null(data)) sum(data$r_obs) else length(t)
  if(is.null(n_total)){ n_total = r }
  if(is.null(tmax) && (!is.null(data) || length(t) > 0)){ tmax = if(!is.null(data)) max(data$upper) else max(t[is.finite(t)]) }
  .check_data(data, t, n_total, tmax, np)

  # Points and weights used for the starting values
  if(!is.null(data)){
    pts = (data$lower + data$upper) / 2
    wts = data$r_obs
  }else{
    pts = t
    wts = rep(1, length(t))
  }
  ok = wts > 0 & pts > 0
  pts = pts[ok]; wts = wts[ok]

  # Starting values from the midpoints
  lambda0 = r / (sum(pts * wts) + (n_total - r) * tmax)
  mlog = sum(wts * log(pts)) / sum(wts)
  slog = sqrt(sum(wts * (log(pts) - mlog)^2) / sum(wts))
  start = switch(dist,
    exponential = lambda0,
    weibull = c(1, 1 / lambda0),
    gamma = c(1, lambda0),
    lognormal = c(exp(mlog), max(slog, 0.1)))

  # Log-likelihood, written in terms of log(parameters) so they stay positive
  loglik_fn = function(logpar){
    a = as.list(exp(logpar))
    names(a) = names_par
    # Units still running at tmax: log of the reliability. Dropped if none survive.
    surv = if(n_total > r) (n_total - r) * .life_p(tmax, dist, a, lower.tail = FALSE, log.p = TRUE) else 0
    # Failures
    if(!is.null(data)){
      d = data[data$r_obs > 0, ]
      if(lik == "interval"){
        p = .life_p(d$upper, dist, a) - .life_p(d$lower, dist, a)
        fail = sum(d$r_obs * log(p))
      }else{
        mid = (d$lower + d$upper) / 2
        fail = sum(d$r_obs * log(do.call(dlife, c(list(t = mid, dist = dist), a))))
      }
    }else{
      fail = sum(log(do.call(dlife, c(list(t = t, dist = dist), a))))
    }
    out = fail + surv
    if(!is.finite(out)){ out = -1e10 }
    out
  }

  # Maximise: one parameter, a one-dimensional search; two, optim()'s default search
  if(np == 1){
    o = optim(par = log(start), fn = loglik_fn, method = "Brent",
              lower = log(start) - 10, upper = log(start) + 10,
              control = list(fnscale = -1))
  }else{
    o = optim(par = log(start), fn = loglik_fn,
              control = list(fnscale = -1, reltol = 1e-12, maxit = 5000))
  }

  est = as.list(exp(o$par))
  names(est) = names_par

  bind_cols(
    tibble(dist = dist),
    as_tibble(est),
    tibble(loglik = o$value, np = np,
           r = r, n_total = n_total, tmax = tmax, lik = lik,
           converged = o$convergence == 0 && o$value > -1e10))
}

# The cells of the chi-squared test: the table's intervals in time order, an
# empty cell for any stretch of time the table skips (from 0 to the first
# interval, or between two intervals), and one last cell from the end of the
# table to infinity holding the units that had not failed (n_total - r).
# Expected count = n_total times the chance of failing in the cell, so the
# expected counts add up to n_total.
.chisq_cells = function(tab, n_total, f, ...){
  tab = tab %>% select(lower, upper, r_obs) %>% arrange(lower)
  gaps = tibble(lower = c(0, tab$upper[-nrow(tab)]), upper = tab$lower, r_obs = 0) %>%
    filter(upper > lower)
  last = tibble(lower = max(tab$upper), upper = Inf, r_obs = n_total - sum(tab$r_obs))
  bind_rows(tab, gaps, last) %>%
    arrange(lower) %>%
    mutate(p_upper = ifelse(is.finite(upper), f(upper, ...), 1),
           p_fail = p_upper - f(lower, ...),
           r_exp = n_total * p_fail) %>%
    select(lower, upper, r_obs, p_fail, r_exp)
}

# Merge thin cells: take the last cell with an expected count under 5 and
# join it to the cell before it (the first cell joins the one after it).
# Repeat until every expected count is at least 5, or one cell is left.
.pool_cells = function(cells){
  thin = which(cells$r_exp < 5)
  if(length(thin) == 0 || nrow(cells) == 1){ return(cells) }
  i = max(thin)
  a = if(i == 1) 1 else i - 1
  b = a + 1
  merged = tibble(lower = cells$lower[a], upper = cells$upper[b],
                  r_obs = cells$r_obs[a] + cells$r_obs[b],
                  p_fail = cells$p_fail[a] + cells$p_fail[b],
                  r_exp = cells$r_exp[a] + cells$r_exp[b])
  idx = seq_len(nrow(cells))
  .pool_cells(bind_rows(cells[idx < a, ], merged, cells[idx > b, ]))
}

#' @name get_expected
#' @title Observed and Expected Failures by Cell
#' @param data a tibble with `lower`, `upper`, `r_obs`
#' @param n_total units on test. Default: the number of failures.
#' @param dist one of "exponential", "weibull", "gamma", "lognormal"
#' @param ... the parameters, by course name (see plife)
#' @param pooled if FALSE (default), one row per interval, plus a row for any
#'   time the table skips and a last row (`upper` = Inf) for the units that had
#'   not failed. If TRUE, the cells after merging, exactly as get_chisq() uses them.
#' @returns `lower`, `upper`, `r_obs`, `p_fail`, `r_exp`. The `r_exp` column adds up to `n_total`.

# Testing values
# crops = tibble(lower = seq(0, 160, 40), upper = lower + 40, r_obs = c(18, 14, 10, 5, 3))
# get_expected(crops, n_total = 75, dist = "exponential", lambda = 0.00595)
get_expected = function(data, n_total = NULL, dist, ..., pooled = FALSE){
  a = .life_args(dist, ...)
  data = .clean_crosstab(data)
  if(is.null(n_total)){ n_total = sum(data$r_obs) }
  .check_data(data, NULL, n_total, NULL, 0)

  f = function(t){ .life_p(t, dist, a) }
  cells = .chisq_cells(data, n_total = n_total, f = f)
  if(pooled){ cells = .pool_cells(cells) }
  cells
}

#' @name get_chisq
#' @title Function to Get Chi-Squared!
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
#' The test follows Tobias and Trindade, Applied Reliability (3rd ed., section 3.8):
#' a last cell from the end of the table to infinity holds the units that had not failed,
#' and cells with fewer than 5 expected failures are merged before adding up.
#' Censored test? Pass a crosstab (`data`) whose last interval ends when the test stopped,
#' or use get_fit(), which trims the table at `tmax` for you.
#' @returns `chisq`, `nbin` (cells after merging), `np`, `df`, `p_value`, and `min_exp` (the smallest expected count)

# Testing values
# masks = read_csv("workshops/masks.csv")
# t = masks$left_earloop; n_total = 50; binwidth = 5; f = pexp; np = 1
# get_chisq(t = t, binwidth = 5, n_total = 50, f = pexp, np = 1, rate = 1 / mean(t))
get_chisq = function(t = NULL, binwidth = 5, data = NULL,
                     n_total, f, np = 1, ...){

  # Part 1: Count failures by interval
  # If vector `t` is NOT NULL, do the raw data route
  if(!is.null(t)){
    # Split into bins of width `binwidth`, starting at 0, and tally failures 'r_obs' by bin
    tab = tibble(t = t) %>%
      mutate(interval = cut(t, breaks = seq(0, ceiling(max(t) / binwidth) * binwidth, by = binwidth),
                            include.lowest = TRUE)) %>%
      group_by(interval, .drop = FALSE) %>%
      summarize(r_obs = n()) %>%
      mutate(bin = 1:n(),
             lower = (bin - 1) * binwidth,
             upper = bin * binwidth)
    # Otherwise, if data.frame `data` is NOT NULL, do the cross-tabulated data route
  }else if(!is.null(data)){
    tab = .clean_crosstab(data)
  }else{
    stop("Please supply either `t` (failure times) or `data` (a crosstab).", call. = FALSE)
  }
  if(n_total < sum(tab$r_obs)){
    stop("`n_total` (", n_total, ") is smaller than the number of failures (", sum(tab$r_obs), ").", call. = FALSE)
  }

  # Part 2: Expected failures in each cell, plus a last cell (to infinity)
  # for the n_total - r units that had not failed
  cells = .chisq_cells(tab, n_total = n_total, f = f, ...)

  # Part 3: Merge cells until every expected count is at least 5
  cells = .pool_cells(cells)

  # Part 4: Calculate Chi-Squared statistic, degrees of freedom and p-value
  output = cells %>%
    summarize(
      chisq = sum((r_obs - r_exp)^2 / r_exp),
      nbin = n(),
      np = np,
      df = nbin - np - 1,
      p_value = if(df >= 1) pchisq(q = chisq, df = df, lower.tail = FALSE) else NA_real_,
      min_exp = min(r_exp))

  # A test needs at least one degree of freedom
  if(output$df < 1){
    message("Only ", output$df, " degrees of freedom after merging cells, so p_value is NA. ",
            "Use narrower intervals or a longer test, so more cells hold 5 or more expected failures.")
  }

  return(output)
}

#' @name get_fit
#' @title Fit and Test Each Life Distribution
#' @param data a tibble with `lower`, `upper`, `r_obs`
#' @param n_total units on test. Default: the number of failures.
#' @param tmax time the unfailed units were still running. Default: the largest `upper`.
#' @param dist one or more of "exponential", "weibull", "gamma", "lognormal" (default: all four)
#' @param lik "interval" (default) or "midpoint" (see get_mle)
#' @returns one row per distribution, sorted by `loglik`, highest first: `dist`, `par1`, `est1`, `par2`,
#'   `est2`, `loglik`, `chisq`, `nbin`, `np`, `df`, `p_value`, `min_exp`, `converged`.
#'   A small p_value rules a distribution out. Among those left, the highest `loglik` fits best (here the lowest chi-squared usually agrees).

# Testing values
# crops = tibble(lower = seq(0, 160, 40), upper = lower + 40, r_obs = c(18, 14, 10, 5, 3))
# get_fit(data = crops, n_total = 75, tmax = 200)
get_fit = function(data, n_total = NULL, tmax = NULL,
                   dist = c("exponential", "weibull", "gamma", "lognormal"),
                   lik = "interval"){

  data = .clean_crosstab(data)
  if(is.null(n_total)){ n_total = sum(data$r_obs) }
  if(is.null(tmax)){ tmax = max(data$upper) }
  .check_data(data, NULL, n_total, tmax, 0)
  # Keep only rows that end by tmax (the rest are empty), so the last cell
  # of the chi-squared test begins where the likelihood censors
  data = data[data$upper <= tmax, ]
  if(nrow(data) == 0){
    stop("No interval ends by `tmax`. Check `tmax` and the `upper` column.", call. = FALSE)
  }
  if(data$lower[1] > 0){
    message("The first interval starts at ", data$lower[1], ", not 0: the chi-squared test adds an empty cell from 0.")
  }

  one = function(d){
    m = get_mle(data = data, n_total = n_total, tmax = tmax, dist = d, lik = lik)
    pars = .life_names[[d]]
    est = unlist(m[1, pars])
    pl = as.list(est)
    # Failure function at the fitted parameters
    f = function(t, ...){ do.call(plife, c(list(t = t, dist = d), pl)) }
    ch = suppressMessages(get_chisq(data = data, n_total = n_total, f = f, np = length(pars)))
    # A test needs at least one degree of freedom
    if(ch$df < 1){
      message("Only ", ch$df, " degrees of freedom for ", d, " after merging cells: p_value set to NA.")
    }
    tibble(dist = d,
           par1 = pars[1], est1 = unname(est[1]),
           par2 = if(length(pars) > 1) pars[2] else NA_character_,
           est2 = if(length(pars) > 1) unname(est[2]) else NA_real_,
           loglik = m$loglik) %>%
      bind_cols(ch %>% select(chisq, nbin, np, df, p_value, min_exp)) %>%
      mutate(converged = m$converged)
  }

  # One family that cannot be fitted must not stop the others
  failed_row = function(d, why){
    message("Could not fit ", d, ": ", why)
    pars = .life_names[[d]]
    out = tibble(dist = d,
                 par1 = if(is.null(pars)) NA_character_ else pars[1], est1 = NA_real_,
                 par2 = if(length(pars) > 1) pars[2] else NA_character_, est2 = NA_real_,
                 loglik = NA_real_, chisq = NA_real_, nbin = NA_integer_,
                 np = NA_integer_, df = NA_real_, p_value = NA_real_, min_exp = NA_real_,
                 converged = FALSE)
    attr(out, "why") = why
    out
  }
  rows = lapply(dist, function(d){
    tryCatch(one(d), error = function(e){ failed_row(d, conditionMessage(e)) })
  })
  whys = lapply(rows, function(x) attr(x, "why"))
  if(all(!vapply(whys, is.null, logical(1)))){
    stop(whys[[1]], call. = FALSE)
  }

  rows %>%
    bind_rows() %>%
    arrange(desc(loglik))
}
