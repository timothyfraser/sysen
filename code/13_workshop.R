#' @name 13_workshop.R
#' @title Interaction Effects in R
#' @author Tim Fraser

library(dplyr)
library(ggplot2)
library(broom)

# Load in data!
# If you upload it to your workshops folder, read it in like this...
lattes = read_csv("workshops/lattes.csv") %>%
  # Let's shorten our main metric name
  rename(y = tastiness)

# View it
lattes

# Show the types
lattes$machine %>% unique()
lattes$syrup %>% unique()
lattes$art %>% unique()
# Also, looks like we randomly assigned the type of milk too.
# We'll treat this as a control
lattes$milk %>% unique()


# Calculate a standard error the tastiness metric in this factorial experiment
se = lattes %>%
  group_by(machine, syrup, art) %>%
  summarize(s = sd(y), n = n()) %>%
  ungroup() %>%
  summarize(se = sqrt( sum(s^2 / n))) %>%
  # A trick - with() is like the dollar sign - it will let you access se
  with(se)

se



# Example 1: Calculate Direct Effects ########################

# Calculate the direct effect of having a heart vs. foam in your latte
stat = lattes %>%
  reframe(
    name = 'Heart - Foamy',
    xbar1 = mean(y[art == "heart"]),
    xbar0 = mean(y[art == "foamy"]),
    dbar = xbar1 - xbar0,
    se = se,
    z = qnorm(0.975),
    lower = dbar - se * z,
    upper = dbar + se * z
  )


# Visualize it!
ggplot() +
  geom_crossbar(data = stats,
                mapping = aes(x = name, y = dbar, ymin = lower, ymax = upper)) +
  geom_hline(yintercept = 0, linetype = "dashed")
# Is that effect significant with 95% confidence?




# FUNCTIONS ######################################

# When doing really nitty-gritty calculations like this,
# functions will become our friends.

# Let's construct ourselves some functions
dbar_oneway = function(formula, data){
  # formula = y ~ machine
  # data = lattes
  
  frame = model.frame(formula, data) %>%
    select(y = 1, a = 2) %>%
    mutate(a = factor(a)) %>%
    mutate(a = as.integer(a) - 1)
  
  
  frame %>%
    reframe(
      dbar = mean(y[a==1] - y[a ==0]),
    ) %>%
    with(dbar)
}

# Function for a 2^3 factorial experiment's 2-way interaction effects
dbar_twoway = function(formula, data){
  # Testing Values
  # formula = y ~ syrup * art
  # data = lattes
  
  # Extract model frame
  frame = model.frame(formula, data) %>%
    select(y = 1, a = 2, b = 3) %>%
    mutate(a = factor(a), b = factor(b))
  
  levels_a = levels(frame$a)
  levels_b = levels(frame$b)
  
  frame = frame %>%
    mutate(a = as.integer(a),
           b = as.integer(b))
  
  output = frame %>%
    reframe(
      x1 = y[(a==2&b==2)|(a==1&b==1)],
      x0 = y[(a==1&b==2)|(a==2&b==1)]
    ) %>%
    reframe(
      dbar = mean(x1) - mean(x0)
    ) %>%
    with(dbar)
  return(output)
}

# For a true 3-by-3 interaction...
dbar_threeway = function(formula, data){
  # Testing Values
  # formula = y ~  machine * syrup * art
  # data = lattes
  
  frame = model.frame(formula, data) %>%
    select(y = 1, a = 2, b = 3, c = 4) %>%
    mutate(a = factor(a), b = factor(b), c= factor(c)) %>%
    mutate(a = as.integer(a) - 1, b = as.integer(b) - 1, c = as.integer(c) - 1)
  
  differences = frame %>%
    reframe(
      # Get the AC interaction when B = 0
      d1a = y[a==1&b==0&c==1] - y[a==0&b==0&c==1],
      d0a = y[a==1&b==0&c==0] - y[a==0&b==0&c==0],
      # Get the AC interaction when B = 1
      d1b = y[a==1&b==1&c==1] - y[a==0&b==1&c==1],
      d0b = y[a==1&b==1&c==0] - y[a==0&b==1&c==0]
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

se_factorial = function(formula = y ~ machine + syrup + art, data){
  # formula = y ~  machine + syrup + art
  # data = lattes
  
  
  # Get frame of data
  frame = model.frame(formula, data) %>%
    rename(y = 1)
  # Get names of xvaraiables
  xvars = names(frame)[-1]
  
  # Recode values
  # frame = frame %>%
  #   mutate(across(.cols = any_of(xvars), .fns = ~as.integer(factor(.x)) - 1))
  
  
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


# Generate your interaction effects for a 2^3 factorial experiment
dbar_oneway(formula = y ~ machine, data = lattes)
dbar_oneway(formula = y ~ syrup, data = lattes)
dbar_oneway(formula = y ~ art, data = lattes)
dbar_twoway(formula = y ~ machine * syrup, data = lattes)
dbar_twoway(formula = y ~ machine * art, data = lattes)
dbar_threeway(formula = y ~ machine * syrup * art, data = lattes)
se_factorial(formula = y ~ machine + syrup + art, data = lattes)



# Can we stack these?
effects = bind_rows(
  tibble(name = "machine", estimate = dbar_oneway(formula = y ~ machine, data = lattes) ),
  tibble(name = "machine * syrup", estimate = dbar_twoway(formula = y ~ machine * syrup, data = lattes) )
) %>%
  mutate(se = se_factorial(formula = y ~ machine + syrup + art, data = lattes))
  


# What if we want to test the effects of 3 or more levels in one factor?

# Compare the ones that are oatmilk AND from machine B against all the ones that are NOT oatmilk and from machine A
lattes %>%
  mutate(oat = milk == "oat") %>%
  dbar_oneway(formula = y ~ machine * oat)
