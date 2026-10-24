# What this file is ----------------------------------------------------------
#
# Helpers for two-level factorial experiments -- the kind where you change two
# or three things at once and want to know how much each one mattered, and
# whether they work differently in combination.
#
#   effects_factorial()  every main effect, two-way and three-way interaction,
#                        with its standard error and confidence interval
#   se_factorial()       the standard error of each effect
#   dbar_oneway(), dbar_twoway(), dbar_threeway()   one effect at a time
#
# Every factor must have two levels. Recode a factor with more levels as a
# yes/no question first, e.g. lattes$oat = lattes$milk == "oat".
# For messy, unbalanced data (say, some runs were lost), use lm() instead.
#
# Load it, from the top of the project folder:
#   source("functions/functions_factorial.R")
#
# Then try:
#   lattes = read.csv("workshops/lattes.csv")
#   effects_factorial(formula = tastiness ~ machine + syrup + art, data = lattes)
#
# You never need to edit anything below.
#

# functions_factorial.R
# Script of R functions for estimating effects and their standard errors in two-level factorial experiments.

library(dplyr, warn.conflicts = FALSE, quietly = TRUE)
library(tibble, warn.conflicts = FALSE, quietly = TRUE)

#' @name se_factorial
#' @title Standard Error of Each Factorial Effect
#' @description Pools the variance over every treatment combination of the
#'   factors, s^2 = sum(v_i * s_i^2) / sum(v_i) with v_i = n_i - 1, then gives each
#'   effect the standard error s * sqrt(sum(c_k^2 / n_k)), summing over the
#'   combinations k of the factors in that effect (n_k runs each; c_k = +/-1 for a
#'   main effect, +/-1/2 for a two-way, +/-1/4 for a three-way). In a balanced
#'   design every effect gets the same standard error, 2s/sqrt(N). Factors must
#'   have two levels; recode others as a yes/no question. For messy, unbalanced
#'   data, use lm() instead.
#' @param formula [formula] The response and the factors, e.g. `y ~ machine + syrup + art`.
#' @param data [data.frame] A data frame containing those variables.
#' @param table [logical] FALSE (default) returns the standard error: one number
#'   when every effect shares it, otherwise one per effect. TRUE returns a table
#'   with each term, its runs at + and -, its se, the pooled variance s2, its
#'   degrees of freedom df, and t_crit for a 95% interval.
#' @return [numeric] or [tibble], as described for `table`.
#' @examples
#' lattes = read.csv("workshops/lattes.csv")
#' se_factorial(formula = tastiness ~ machine + syrup + art, data = lattes)
#' lattes$oat = lattes$milk == "oat"
#' se_factorial(formula = tastiness ~ machine + oat + syrup + art, data = lattes, table = TRUE)
se_factorial = function(formula, data, table = FALSE){
  # Get the response (y) and the factors from the formula
  frame = model.frame(formula, data) %>% rename(y = 1)
  xvars = names(frame)[-1]
  # Every factor must have exactly two levels
  levels_n = sapply(frame[xvars], function(x) length(unique(x)))
  if (any(levels_n != 2)) {
    stop("se_factorial(): ", paste(xvars[levels_n != 2], collapse = ", "),
         " does not have exactly two levels. Recode it as a yes/no question, e.g. oat = milk == \"oat\".")
  }
  # Code each factor -1 (first level) and +1 (second level)
  coded = frame %>% mutate(across(all_of(xvars), ~ ifelse(as.integer(factor(.x)) == 2, 1, -1)))

  # Pooled variance over the treatment combinations of all the factors
  cells = coded %>%
    group_by(across(all_of(xvars))) %>%
    summarize(s2 = var(y), v = n() - 1, .groups = "drop")
  df = sum(cells$v)
  if (df == 0) {
    stop("se_factorial(): no treatment combination has 2 or more runs, so there is no pooled variance; ",
         "judge its effects with a normal plot instead.")
  }
  s2 = sum(cells$v * cells$s2, na.rm = TRUE) / df

  # Every main effect, two-way and three-way interaction among the factors
  terms = unlist(lapply(1:min(3, length(xvars)), function(m) combn(xvars, m, simplify = FALSE)),
                 recursive = FALSE)
  # SE of each effect: s * sqrt(sum of c^2 / n) over the combinations of its factors
  output = tibble(term = sapply(terms, paste, collapse = ":")) %>%
    mutate(
      n_plus = sapply(terms, function(t) sum(apply(coded[t], 1, prod) == 1)),
      n_minus = sapply(terms, function(t) sum(apply(coded[t], 1, prod) == -1)),
      se = sapply(terms, function(t){
        n_k = coded %>% count(across(all_of(t))) %>% pull(n)
        c_k = 1 / 2^(length(t) - 1)
        sqrt(s2) * sqrt(sum(c_k^2 / n_k)) }),
      s2 = s2, df = df, t_crit = qt(0.975, df = df))

  if (table) { return(output) }
  # Balanced: every effect has the same SE, so return that one number
  if (diff(range(output$se)) < 1e-10) { return(output$se[1]) }
  message("se_factorial(): effects have different standard errors; effects_factorial() lists each effect with its own.")
  return(setNames(output$se, output$term))
}

#' @name effects_factorial
#' @title Table of Factorial Effects
#' @description Every main effect, two-way and three-way interaction among the
#'   factors, each with its standard error (from se_factorial()) and a t
#'   confidence interval on the pooled degrees of freedom. Factors must have two
#'   levels. For messy, unbalanced data, use lm() instead.
#' @param formula [formula] The response and the factors, e.g. `y ~ machine + syrup + art`.
#' @param data [data.frame] A data frame containing those variables.
#' @param conf [numeric] Confidence level for the interval (default 0.95).
#' @return [tibble] One row per term: term, effect, se, lower, upper.
#' @examples
#' lattes = read.csv("workshops/lattes.csv")
#' effects_factorial(formula = tastiness ~ machine + syrup + art, data = lattes)
effects_factorial = function(formula, data, conf = 0.95){
  # Standard errors (and the two-level check) come from se_factorial()
  ses = se_factorial(formula, data, table = TRUE)
  frame = model.frame(formula, data) %>% rename(y = 1)

  ses %>%
    mutate(
      # Each effect from the matching dbar function
      effect = sapply(strsplit(term, ":"), function(t){
        f = as.formula(paste("y ~", paste(t, collapse = " * ")))
        switch(length(t), dbar_oneway(f, frame), dbar_twoway(f, frame), dbar_threeway(f, frame)) }),
      # t interval on the pooled degrees of freedom
      t_crit = qt(1 - (1 - conf) / 2, df = df),
      lower = effect - t_crit * se,
      upper = effect + t_crit * se) %>%
    select(term, effect, se, lower, upper)
}

#' @name dbar_oneway
#' @title One-Way (Main) Effect
#' @description The mean of the runs at the factor's second ("high") level minus
#'   the mean of the runs at its first ("low") level.
#' @param formula [formula] A formula with one factor, e.g. `y ~ machine`.
#' @param data [data.frame] A data frame containing those variables.
#' @return [numeric] The effect.
#' @examples
#' lattes = read.csv("workshops/lattes.csv")
#' dbar_oneway(formula = tastiness ~ machine, data = lattes)
dbar_oneway = function(formula, data){
  # formula = y ~ machine
  # data = lattes

  frame = model.frame(formula, data) %>%
    select(y = 1, a = 2) %>%
    mutate(a = as.integer(factor(a)) - 1)

  # Compute the one-way effect from the cell means
  frame %>%
    # One mean per level of a
    group_by(a) %>%
    summarize(xbar = mean(y)) %>%
    # The "High" level (a == 1) minus the "Low" level (a == 0)
    summarize(dbar = mean(xbar[a == 1]) - mean(xbar[a == 0])) %>%
    with(dbar)
}

#' @name dbar_twoway
#' @title Two-Way Interaction Effect
#' @description Averages the means of the four combinations of two factors:
#'   same-direction combinations (high-high, low-low) minus opposite-direction
#'   combinations (high-low, low-high).
#' @param formula [formula] A formula with two factors, e.g. `y ~ machine * syrup`.
#' @param data [data.frame] A data frame containing those variables.
#' @return [numeric] The effect.
#' @examples
#' lattes = read.csv("workshops/lattes.csv")
#' dbar_twoway(formula = tastiness ~ machine * syrup, data = lattes)
dbar_twoway = function(formula, data){
  # formula = y ~ machine * syrup
  # data = lattes

  # Extract model frame, with y and the two factors coded 0 (low) and 1 (high)
  frame = model.frame(formula, data) %>%
    select(y = 1, a = 2, b = 3) %>%
    mutate(a = as.integer(factor(a)) - 1,
           b = as.integer(factor(b)) - 1)

  output = frame %>%
    # One mean per cell (each combination of a and b)
    group_by(a, b) %>%
    summarize(xbar = mean(y), .groups = "drop") %>%
    # Same-direction cells (HH or LL) minus opposite-direction cells (HL or LH)
    summarize(dbar = mean(xbar[a == b]) - mean(xbar[a != b])) %>%
    with(dbar)
  return(output)
}

#' @name dbar_threeway
#' @title Three-Way Interaction Effect
#' @description Averages the means of the eight combinations of three factors:
#'   combinations whose signs multiply to + minus those whose signs multiply to -.
#' @param formula [formula] A formula with three factors, e.g. `y ~ machine * syrup * art`.
#' @param data [data.frame] A data frame containing those variables.
#' @return [numeric] The effect.
#' @examples
#' lattes = read.csv("workshops/lattes.csv")
#' dbar_threeway(formula = tastiness ~ machine * syrup * art, data = lattes)
dbar_threeway = function(formula, data){
  # formula = y ~  machine * syrup * art
  # data = lattes

  # Extract model frame, with y and the three factors coded 0 (low) and 1 (high)
  frame = model.frame(formula, data) %>%
    select(y = 1, a = 2, b = 3, c = 4) %>%
    mutate(a = as.integer(factor(a)) - 1,
           b = as.integer(factor(b)) - 1,
           c = as.integer(factor(c)) - 1)

  output = frame %>%
    # One mean per cell (each combination of a, b and c)
    group_by(a, b, c) %>%
    summarize(xbar = mean(y), .groups = "drop") %>%
    # The sign of each cell in the three-way contrast: + or -
    mutate(sign = (2 * a - 1) * (2 * b - 1) * (2 * c - 1)) %>%
    # Average of the + cells minus average of the - cells
    summarize(dbar = mean(xbar[sign == 1]) - mean(xbar[sign == -1])) %>%
    with(dbar)
  return(output)
}
