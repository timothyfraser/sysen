# functions_factorial.R
# Script of R functions for running difference of means tests on factorial experiments.

#' @name se_factorial
#' @title Calculate Standard Error for Factorial Experiments
#' @description Calculates the standard error for a response variable in a factorial experiment by pooling standard deviations across all treatment combinations.
#' @param formula [formula] A formula specifying the response variable and factors (e.g., `y ~ machine + syrup + art`). The first variable should be the response variable.
#' @param data [data.frame] A data frame containing the variables specified in the formula.
#' @return [numeric] A single numeric value representing the pooled standard error.
#' @examples
#' # Load the lattes data
#' lattes = read.csv("workshops/lattes.csv")
#' 
#' # Calculate standard error for a three-factor experiment
#' se_factorial(formula = tastiness ~ machine + syrup + art, data = lattes)
#' 
#' # Calculate standard error for a two-factor experiment
#' se_factorial(formula = tastiness ~ machine + syrup, data = lattes)
se_factorial = function(formula = y ~ machine + syrup + art, data){
  # formula = y ~  machine + syrup + art
  # data = lattes
  require(dplyr, warn.conflicts = FALSE, quietly = TRUE)

  # Get frame of data
  frame = model.frame(formula, data) %>%
    rename(y = 1)
  # Get names of x variables
  xvars = names(frame)[-1]
  
  
  # Calculate a standard error the tastiness metric in this factorial experiment
  output = frame %>%
    group_by(across(any_of(xvars))) %>%
    summarize(s = sd(y), n = n()) %>%
    ungroup() %>%
    summarize(se = sqrt( sum(s^2 / n))) %>%
    # A trick - with() is like the dollar sign - it will let you access se
    with(se)
  return(output)
}

#' @name dbar_oneway
#' @title Calculate One-Way Treatment Effect
#' @description Calculates the mean difference (dbar) between two levels of a single factor in a factorial experiment. The function compares the "High" group (second level) to the "Low" group (first level).
#' @param formula [formula] A formula with a single factor (e.g., `y ~ machine`). The first variable should be the response variable, and the second should be the factor of interest.
#' @param data [data.frame] A data frame containing the variables specified in the formula.
#' @return [numeric] A single numeric value representing the mean difference between the two factor levels.
#' @examples
#' # Load the lattes data
#' lattes = read.csv("workshops/lattes.csv")
#' 
#' # Calculate one-way effect for machine factor
#' dbar_oneway(formula = tastiness ~ machine, data = lattes)
#' 
#' # Calculate one-way effect for syrup factor
#' dbar_oneway(formula = tastiness ~ syrup, data = lattes)
dbar_oneway = function(formula, data){
  # formula = y ~ machine
  # data = lattes
  require(dplyr, warn.conflicts = FALSE, quietly = TRUE)

  frame = model.frame(formula, data) %>%
    select(y = 1, a = 2) %>%
    mutate(a = factor(a)) %>%
    mutate(a = as.integer(a) - 1)
  
  # Compute the one-way effect
  frame %>%
    reframe(
      # The mean difference between the "High" group (a == 1) and the "Low" group (a == 0)
      dbar = mean(y[a == 1] - y[a == 0]),
    ) %>%
    with(dbar)
}

#' @name dbar_twoway
#' @title Calculate Two-Way Interaction Effect
#' @description Calculates the two-way interaction effect (dbar) between two factors in a factorial experiment. The function compares combinations where factors are aligned (both high or both low) versus combinations where factors are opposite (one high, one low).
#' @param formula [formula] A formula with two factors and their interaction (e.g., `y ~ machine * syrup`). The first variable should be the response variable, followed by two factors.
#' @param data [data.frame] A data frame containing the variables specified in the formula.
#' @return [numeric] A single numeric value representing the two-way interaction effect.
#' @examples
#' # Load the lattes data
#' lattes = read.csv("workshops/lattes.csv")
#' 
#' # Calculate two-way interaction between machine and syrup
#' dbar_twoway(formula = tastiness ~ machine * syrup, data = lattes)
#' 
#' # Calculate two-way interaction between machine and art
#' dbar_twoway(formula = tastiness ~ machine * art, data = lattes)
dbar_twoway = function(formula, data){
  # formula = y ~ machine * syrup
  # data = lattes
  
  require(dplyr, warn.conflicts = FALSE, quietly = TRUE)

  # Extract model frame
  frame = model.frame(formula, data) %>%
    # Rename columns as y, a, b
    select(y = 1, a = 2, b = 3) %>%
    mutate(a = factor(a), b = factor(b))
  
  levels_a = levels(frame$a)
  levels_b = levels(frame$b)
  
  # Convert factors to integer codes
  frame = frame %>%
    mutate(a = as.integer(a),
           b = as.integer(b))
  
  # Now pick the combinations for comparison
  output = frame %>%
    reframe(
      # Same factors: HH or LL
      x1 = y[(a == 2 & b == 2) | (a == 1 & b == 1)],
      # Opposite factors: HL or LH
      x0 = y[(a == 1 & b == 2) | (a == 2 & b == 1)]
    ) %>%
    reframe(
      # Calculate dbar
      dbar = mean(x1) - mean(x0)
    ) %>%
    with(dbar)
  return(output)
}

#' @name dbar_threeway
#' @title Calculate Three-Way Interaction Effect
#' @description Calculates the three-way interaction effect (dbar) between three factors in a factorial experiment. The function evaluates the AC interaction at different levels of factor B, then computes the average difference between these interactions.
#' @param formula [formula] A formula with three factors and their interactions (e.g., `y ~ machine * syrup * art`). The first variable should be the response variable, followed by three factors.
#' @param data [data.frame] A data frame containing the variables specified in the formula.
#' @return [numeric] A single numeric value representing the three-way interaction effect.
#' @examples
#' # Load the lattes data
#' lattes = read.csv("workshops/lattes.csv")
#' 
#' # Calculate three-way interaction between machine, syrup, and art
#' dbar_threeway(formula = tastiness ~ machine * syrup * art, data = lattes)
dbar_threeway = function(formula, data){
  # formula = y ~  machine * syrup * art
  # data = lattes
  require(dplyr, warn.conflicts = FALSE, quietly = TRUE)

  frame = model.frame(formula, data) %>%
    select(y = 1, a = 2, b = 3, c = 4) %>%
    mutate(a = factor(a), b = factor(b), c= factor(c)) %>%
    mutate(a = as.integer(a) - 1, b = as.integer(b) - 1, c = as.integer(c) - 1)
  
  differences = frame %>%
    reframe(
      # Get the AC interaction when B = 0
      d1a = y[a == 1 & b == 0 & c == 1] - y[a == 0 & b == 0 & c == 1],
      d0a = y[a == 1 & b == 0 & c == 0] - y[a == 0 & b == 0 & c == 0],
      # Get the AC interaction when B = 1
      d1b = y[a == 1 & b == 1 & c == 1] - y[a == 0 & b == 1 & c == 1],
      d0b = y[a == 1 & b == 1 & c == 0] - y[a == 0 & b == 1 & c == 0]
    )
  
  output = differences %>%
    reframe(
      # Get AC interaction effect when B = 0
      dbar_a = (mean(d1a) - mean(d0a)) / 2,
      # Get AC interaction effect when B = 1
      dbar_b = (mean(d1b) - mean(d0b) ) / 2,
      # Get the average of the two effects 
      dbar = (dbar_b - dbar_a) / 2
    ) %>%
    select(dbar) %>%
    with(dbar)
  return(output)
}
