# What this file is ----------------------------------------------------------
#
# One helper, plan_test(), that plans a reliability life test. Give it the
# life distribution and all but one of the planning pieces, and it solves for
# the missing piece: how many units to test (n), how long to test them (t),
# how many failures you can allow (r), how confident you can be (ci), or the
# life parameter the test is able to demonstrate.
#
# It works for four life distributions: exponential, weibull, gamma, lognormal.
#
# Load it, from the top of the project folder:
#   source("functions/functions_planning.R")
#
# Then try:
#   plan_test("exponential", t = 5000, r = 5, ci = 0.90, lambda = 1 / 500000)
#   plan_test("lognormal", t = 5000, r = 5, ci = 0.90, t50 = 1e5, sigma = 2)
#
# The shape parameter (m, k or sigma) has to be assumed from earlier data.
# Write ci by name, as ci = 0.90.
#
# Set exact = TRUE for the exact method. It counts failures with the binomial
# distribution: each unit either fails during the test or does not.
#
# You never need to edit anything below.
#

library(dplyr)
library(tibble)

# Parameter names for each family.
# Exponential: lambda (scale only). Weibull: m (shape), c (scale).
# Gamma: k (shape), lambda (scale). Lognormal: sigma (shape), t50 (scale).
.plan_shape = c(exponential = NA_character_, weibull = "m", gamma = "k", lognormal = "sigma")
.plan_scale = c(exponential = "lambda", weibull = "c", gamma = "lambda", lognormal = "t50")
# Column order for the life parameters, as the course names them
.plan_order = list(exponential = "lambda", weibull = c("m", "c"), gamma = c("k", "lambda"), lognormal = c("t50", "sigma"))

# Cumulative hazard H(t) = -log(1 - F(t)), written so it stays accurate when F is tiny
.plan_h = function(t, dist, p){
  switch(
    dist,
    exponential = p$lambda * t,
    weibull = (t / p$c)^p$m,
    gamma = -pgamma(t, shape = p$k, rate = p$lambda, lower.tail = FALSE, log.p = TRUE),
    lognormal = -pnorm(log(t / p$t50) / p$sigma, lower.tail = FALSE, log.p = TRUE))
}

# Failure function F(t): the chance a unit has failed by time t
.plan_f = function(t, dist, p){
  switch(
    dist,
    exponential = pexp(t, rate = p$lambda),
    weibull = pweibull(t, shape = p$m, scale = p$c),
    gamma = pgamma(t, shape = p$k, rate = p$lambda),
    lognormal = pnorm(log(t / p$t50) / p$sigma))
}

# Quantile function: the time by which a share f of units have failed
.plan_q = function(f, dist, p){
  switch(
    dist,
    exponential = qexp(f, rate = p$lambda),
    weibull = qweibull(f, shape = p$m, scale = p$c),
    gamma = qgamma(f, shape = p$k, rate = p$lambda),
    lognormal = p$t50 * exp(p$sigma * qnorm(f)))
}

# The scale parameter a test can demonstrate, given the failure share f_need
# it must show by time s = t * af (the shape stays as assumed)
.plan_scale_solve = function(f_need, s, dist, p){
  switch(
    dist,
    exponential = -log1p(-f_need) / s,
    weibull = s / (-log1p(-f_need))^(1 / p$m),
    gamma = qgamma(f_need, shape = p$k, rate = 1) / s,
    lognormal = s / exp(p$sigma * qnorm(f_need)))
}

# A = qchisq(ci, df = 2 * (r + 1)) / 2, vectorized over r and ci.
# For r of 1 or more, A equals r * qk(p = ci, r = r, .time = TRUE).
# For r = 0, A equals -log(1 - ci).
.plan_a = function(ci, r){ qchisq(ci, df = 2 * (r + 1)) / 2 }

# Plan one test (one row of inputs). `x` is a list holding n, t, r, ci, af and
# the life parameters; the missing piece is NA and `solved` names it.
.plan_one = function(x, dist, solved, exact){
  # Testing values
  # x = list(n = NA, t = 5000, r = 5, ci = 0.9, af = 1, lambda = 1/500000)
  # dist = "exponential"; solved = "n"; exact = FALSE
  p = x[.plan_order[[dist]]]
  n = x$n; t = x$t; r = x$r; ci = x$ci; af = x$af

  if(solved == "n"){
    h = .plan_h(t * af, dist, p)
    if(!exact){
      n = .plan_a(ci, r) / h
    }else{
      # smallest n whose binomial chance of r or fewer failures is at most 1 - ci
      f = .plan_f(t * af, dist, p)
      top = ceiling(4 * .plan_a(ci, r) / h) + 100
      stopifnot("the exact search needs too many units; try a longer test" = top < 1e7)
      cand = (r + 1):top
      n = cand[which(pbinom(r, cand, f) <= 1 - ci)[1]]
    }
  }
  if(solved == "t"){
    f_need = if(!exact){ -expm1(-.plan_a(ci, r) / n) }else{ qbeta(ci, r + 1, n - r) }
    t = .plan_q(f_need, dist, p) / af
  }
  if(solved == "r"){
    h = .plan_h(t * af, dist, p)
    cand = 0:floor(n)
    if(!exact){
      ok = .plan_a(ci, cand) <= n * h
    }else{
      ok = suppressWarnings(pbinom(cand, n, .plan_f(t * af, dist, p))) <= 1 - ci
    }
    r = if(any(ok)){ max(cand[ok]) }else{ NA_real_ }
    if(is.na(r)){
      message("No number of allowed failures meets this plan; use more units, a longer test, or less confidence.")
    }
  }
  if(solved == "ci"){
    if(!exact){
      ci = pchisq(2 * n * .plan_h(t * af, dist, p), df = 2 * (r + 1))
    }else{
      ci = 1 - pbinom(r, n, .plan_f(t * af, dist, p))
    }
  }
  if(solved %in% .plan_scale){
    f_need = if(!exact){ -expm1(-.plan_a(ci, r) / n) }else{ qbeta(ci, r + 1, n - r) }
    p[[solved]] = .plan_scale_solve(f_need, t * af, dist, p)
  }

  n_up = ceiling(n - 1e-9)
  if(solved == "n" && !is.na(n) && n <= r){
    n_up = r + 1
    message("The plan needs more units than allowed failures (n is at or below r), so n_up is set to r + 1.")
  }
  f_t = .plan_f(t * af, dist, p)
  tibble::as_tibble(c(
    list(dist = dist), p,
    list(n = n, n_up = n_up, t = t, r = r, ci = ci, af = af, F_t = f_t,
         A = if(is.na(r) | is.na(ci)){ NA_real_ }else{ .plan_a(ci, r) },
         solved = solved, method = if(exact){ "exact" }else{ "k-factor" })))
}

#' @name plan_test
#' @title Plan a Reliability Life Test
#' @description
#' Leave out exactly one of n, t, r, ci, or the scale parameter, and it is solved for.
#' The shape parameter (m, k, sigma) can never be the one left out.
#' @param dist:chr "exponential", "weibull", "gamma", or "lognormal"
#' @param n:dbl number of units on test
#' @param t:dbl test time (in the same units as the life parameters)
#' @param r:int number of failures allowed during the test (0 or more)
#' @param ci:dbl confidence level, between 0 and 1 (name it: ci = 0.90)
#' @param ...:dbl the life parameters, by name:
#'   exponential: lambda; weibull: m (shape), c (scale);
#'   gamma: k (shape), lambda (rate); lognormal: t50 (median life), sigma (shape)
#' @param af:dbl acceleration factor; t hours at stress count as t * af hours of use
#' @param exact:logical use the exact answer instead of the k-factor formula?
#'   The exact method counts failures with the binomial distribution
#'   (each unit either fails during the test or does not).
#' @returns one row per plan: dist, the life parameters, n, n_up (n rounded up),
#'   t, r, ci, af, F_t, A, solved, method
#'
#' @importFrom dplyr `bind_rows`
plan_test = function(dist = "exponential", n = NULL, t = NULL, r = NULL, ..., ci = NULL, af = 1, exact = FALSE){
  # ci sits after the dots on purpose: otherwise c = 20000 (the Weibull scale) would be read as ci
  # Testing values
  # dist = "lognormal"; n = NULL; t = 5000; r = 5; ci = 0.90; af = 1; exact = FALSE
  # (and in the dots: t50 = 1e5, sigma = 2)

  # Input error handling
  stopifnot("dist must be one of exponential, weibull, gamma, lognormal" =
              is.character(dist) && length(dist) == 1 && dist %in% names(.plan_scale))
  stopifnot("exact must be TRUE or FALSE" = is.logical(exact) && length(exact) == 1 && !is.na(exact))
  dots = list(...)
  shape = .plan_shape[[dist]]
  scale = .plan_scale[[dist]]
  need = c(stats::na.omit(c(shape, scale)))
  extra = setdiff(names(dots), need)
  if(length(extra) > 0 || (length(dots) > 0 && is.null(names(dots)))){
    stop("For dist = \"", dist, "\", the life parameters are: ", paste(need, collapse = ", "),
         ". Name each one, e.g. ", scale, " = 1000.")
  }
  if(!is.na(shape) && !(shape %in% names(dots))){
    stop("The shape parameter ", shape, " is missing. It cannot be solved for; assume a value for ", shape, ".")
  }

  # Which one piece is missing?
  given = list(n = n, t = t, r = r, ci = ci)
  given[[scale]] = dots[[scale]]
  is_null = vapply(given, is.null, logical(1))
  missing = c(names(is_null)[is_null], if(is.null(dots[[scale]])){ scale })
  missing = unique(missing)
  if(length(missing) != 1){
    stop("Leave out exactly one of n, t, r, ci, or ", scale, ", and it will be solved for. ",
         "You left out ", length(missing), ".")
  }
  solved = missing

  # Put all inputs side by side; vectors recycle to one row each
  inputs = c(given[!is_null], dots[setdiff(names(dots), scale)], list(af = af))
  inputs = tibble::as_tibble(inputs)
  ok_num = vapply(inputs, function(v){ is.numeric(v) && all(is.finite(v)) }, logical(1))
  if(!all(ok_num)){
    stop("Every input must be a finite number, with no NA, NaN, Inf or text. Check: ",
         paste(names(inputs)[!ok_num], collapse = ", "), ".")
  }
  inputs[[solved]] = NA_real_
  inputs = inputs %>% dplyr::mutate(dplyr::across(dplyr::everything(), as.numeric))
  if(any(inputs[["n"]] <= 0, na.rm = TRUE)){ stop("n must be greater than 0. Change n to at least 1 unit.") }
  if(any(inputs[["t"]] <= 0, na.rm = TRUE)){ stop("t must be greater than 0. Change t to a positive test time.") }
  life = intersect(need, names(inputs))
  if(any(vapply(life, function(v){ any(inputs[[v]] <= 0, na.rm = TRUE) }, logical(1)))){
    stop("The life parameters (", paste(need, collapse = ", "), ") must all be greater than 0.")
  }
  if(any(inputs[["n"]] <= inputs[["r"]], na.rm = TRUE)){
    stop("n must be larger than r: you cannot allow as many failures as units. Raise n or lower r.")
  }
  if(exact && any(inputs[["n"]] != round(inputs[["n"]]), na.rm = TRUE)){
    stop("With exact = TRUE, n must be a whole number.")
  }
  if(any(inputs[["af"]] <= 0, na.rm = TRUE)){ stop("af must be positive.") }
  if(any(inputs[["ci"]] <= 0 | inputs[["ci"]] >= 1, na.rm = TRUE)){ stop("ci must be between 0 and 1.") }
  if(any(inputs[["r"]] < 0 | inputs[["r"]] != round(inputs[["r"]]), na.rm = TRUE)){ stop("r must be a whole number, 0 or more.") }

  out = lapply(seq_len(nrow(inputs)), function(i){
    .plan_one(as.list(inputs[i, ]), dist = dist, solved = solved, exact = exact)
  }) %>% dplyr::bind_rows()

  if(!exact && any(out$F_t > 0.10, na.rm = TRUE)){
    message("F_t is above 0.10 (many units fail during the test), so the k-factor formula is loose. ",
            "Try exact = TRUE for the exact binomial answer.")
  }
  out
}

# Examples
# plan_test("exponential", t = 5000, r = 5, ci = 0.90, lambda = 1 / 500000)     # solves n
# plan_test("exponential", n = 100, r = 10, ci = 0.95, lambda = 1 / 20000)      # solves t
# plan_test("exponential", n = 50, t = 2000, ci = 0.80, lambda = 0.00005)       # solves r
# plan_test("lognormal", t = 5000, r = 5, ci = 0.90, t50 = 1e5, sigma = 2)      # solves n
# plan_test("lognormal", t = 5000, r = 5, ci = 0.90, t50 = 1e5, sigma = 2, exact = TRUE)
# plan_test("lognormal", t = 5000, r = 5, ci = 0.90, t50 = 1e5, sigma = c(1.5, 2, 2.5))
