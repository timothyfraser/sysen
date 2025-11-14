# functions_factorial.R
# Script of R functions for running difference of means tests on factorial experiments.

se_factorial = function(formula = y ~ machine + syrup + art, data){
  # formula = y ~  machine + syrup + art
  # data = lattes
  

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

dbar_oneway = function(formula, data){
  # formula = y ~ machine
  # data = lattes
  
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
dbar_twoway = function(formula, data){
  # formula = y ~ machine * syrup
  # data = lattes
  
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

dbar_threeway = function(formula, data){
  # formula = y ~  machine * syrup * art
  # data = lattes
  
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
