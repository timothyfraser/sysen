#' @name 13_workshop.R
#' @title Interaction Effects in R
#' @author Tim Fraser

library(readr)
library(dplyr)
library(tidyr)
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


# Calculate the standard error of an effect in this factorial experiment.
# First, pool the variance across every treatment combination (cell)...
s2 = lattes %>%
  group_by(machine, syrup, art) %>%
  summarize(s2 = var(y), n = n()) %>%
  ungroup() %>%
  summarize(s2 = sum((n - 1) * s2) / sum(n - 1)) %>%
  # A trick - with() is like the dollar sign - it will let you access s2
  with(s2)
# ...then each effect compares the mean of the runs at + with the mean of the runs at -,
# so SE = s * sqrt(1 / n_plus + 1 / n_minus). Machine b has 120 runs and machine a has 120.
se = sqrt(s2) * sqrt(1 / 120 + 1 / 120)

se




# Example 1: Calculate Direct Effects ########################

# Calculate the direct effect of having a heart vs. foam in your latte

lattes %>%
  summarize(dbar =  mean(y[machine == "a"]) - mean(y[machine == "b"] ) )


lattes %>%
  reframe(dbar =  mean(y[machine == "a"]) - mean(y[machine == "b"] ) )


lattes %>%
  reframe(dbar =  y[machine == "a"] - y[machine == "b"] )

lattes %>%
  summarize(dbar =  y[machine == "a"] - y[machine == "b"] )



myse = lattes %>%
  group_by(machine, syrup, art) %>%
  summarize(
    s2 = var(y),
    n = n()) %>%
  ungroup() %>%
  summarize(s2 = sum((n - 1) * s2) / sum(n - 1),
            se = sqrt(s2) * sqrt(1 / 120 + 1 / 120))
myse %>%  {.$se}
myse %>%  with(se)

se = myse$se


stat = lattes %>%
  summarize(dbar =  mean(y[machine == "a"]) - mean(y[machine == "b"]) ) %>%
  mutate(se = se) %>%
  mutate(
    name = "Machine A - B",
    z = qnorm(0.975),
    upper = dbar + z * se,
    lower = dbar - z * se)

# pnorm(3)
stat

colors()

ggplot() +
  geom_point(data = stat, mapping = aes(x = name, y = dbar)) +
  geom_crossbar(data = stat, mapping = aes(x = name, y = dbar, ymin = lower, ymax = upper),
                fill = "violetred") +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_text(data = stat, mapping = aes(x = name, y = upper + 2, label = round(upper, 2) )) +
  geom_text(data = stat, mapping = aes(x = name, y = lower - 2, label = round(lower, 2) ))


# stat = lattes %>%
#   reframe(
#     name = 'Heart - Foamy',
#     xbar1 = mean(y[art == "heart"]),
#     xbar0 = mean(y[art == "foamy"]),
#     dbar = xbar1 - xbar0,
#     se = se,
#     z = qnorm(0.975),
#     lower = dbar - se * z,
#     upper = dbar + se * z
#   )
# 

# Visualize it!
ggplot() +
  geom_crossbar(
    data = stat,
    mapping = aes(x = name, y = dbar, ymin = lower, ymax = upper)) +
  geom_hline(yintercept = 0, linetype = "dashed")
# Is that effect significant with 95% confidence?







# FUNCTIONS ######################################

# When doing really nitty-gritty calculations like this,
# functions will become our friends.

# Let's construct ourselves some functions
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


# Generate your interaction effects for a 2^3 factorial experiment
dbar_oneway(formula = y ~ machine, data = lattes)

# Highest alphabeltic level - Lowest Alphabeltical Level
# B - A


lattes$machine %>% unique()
# B - A
dbar_oneway(formula = y ~ machine, data = lattes)

lattes$syrup %>% unique()
# Torani - Monin
dbar_oneway(formula = y ~ syrup, data = lattes)


lattes$art %>% unique()
# Heart - Foamy
dbar_oneway(formula = y ~ art, data = lattes)


# B*Torani - A*Monin
dbar_twoway(formula = y ~ machine * syrup, data = lattes)

# B*Heart - A*Foamy
dbar_twoway(formula = y ~ machine * art, data = lattes)

# B*Heart*Torani - A*Foamy*Monin
dbar_threeway(formula = y ~ machine * syrup * art, data = lattes)


# Get your standard error free o charge
se_factorial(formula = y ~ machine + syrup + art, data = lattes)


# Every main effect and interaction, each with its standard error and a 95% interval
effects = effects_factorial(formula = y ~ machine + syrup + art, data = lattes) %>%
  rename(name = term, estimate = effect)

effects
gg = ggplot() +
  geom_crossbar(data = effects,
                mapping = aes(x = name, y = estimate, ymin = lower, ymax = upper,
                              fill = name)) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  theme(legend.position = "none") +
  coord_flip() 

gg = ggplot() +
  geom_crossbar(data = effects,
                mapping = aes(x = name, y = estimate, ymin = lower, ymax = upper,
                              fill = estimate)) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  theme(legend.position = "none") +
  coord_flip()  +
  scale_fill_gradient2(high = "royalblue", low = "salmon", mid = "white", midpoint = 0)

gg


# # Can we stack these?
# effects = bind_rows(
#   tibble(name = "machine", estimate = dbar_oneway(formula = y ~ machine, data = lattes) ),
#   tibble(name = "machine * syrup", estimate = dbar_twoway(formula = y ~ machine * syrup, data = lattes) )
# ) %>%
#   mutate(se = se_factorial(formula = y ~ machine + syrup + art, data = lattes))
#   
# 


# MULTIPLE LEVELS IN A FACTOR ####################################

# What if we want to test the effects of 3 or more levels in one factor?

lattes$milk %>% unique()

lattes %>%
  lm(formula = y ~ milk)

lattes %>%
  oneway.test(formula = y ~ milk)













lattes %>%
  mutate(oat = milk == "oat") %>%
  dbar_oneway(formula = y ~ oat)







# Compare the ones that are oatmilk vs. not
lattes %>%
  mutate(oat = milk == "oat") %>%
  dbar_oneway(formula = y ~ oat)

# Compare the ones that are skim vs. not
lattes %>%
  mutate(skim = milk == "skim") %>%
  dbar_oneway(formula = y ~ skim)





# Compare the ones that are whole vs. not
lattes %>%
  mutate(whole = milk == "whole") %>%
  dbar_oneway(formula = y ~ whole)








# Compare the ones that are oatmilk AND from machine B against all the ones that are NOT oatmilk and from machine A
lattes %>%
  mutate(oat = milk == "oat") %>%
  dbar_twoway(formula = y ~ machine * oat)

# Or get every effect at once. Oat lattes are a third of the runs,
# so effects involving oat get their own, larger standard error
lattes %>%
  mutate(oat = milk == "oat") %>%
  effects_factorial(formula = y ~ machine + oat + syrup + art)






# interactions with lm() #############################


m = lattes %>%
  lm(formula = y ~ machine * art) 
# Tastiness = 54 + -26 * (machine B?) + 15 * (heart?) - 8 * (machineB?)(heart?)
# Tastiness = 54 + -26 * (1) + 15 * (0) - 8 * (1)(0)
# Tastiness = 54 + -26 * (1) + 15 * (1) - 8 * (1)(1)
# Tastiness = 54 + -26 * (0) + 15 * (0) - 8 * (0)(0)

tibble(
  machine = "b",
  art = "heart",
  y = predict(m, newdata = tibble(machine, art))
)


predict(m, newdata = tibble(machine = "b", art = "heart"), se.fit = TRUE) %>%
  as_tibble() %>%
  select(yhat = fit, se = se.fit)


grid = expand_grid(
  machine = c("a", "b"),
  art = c("heart", "foamy")
)

# Use each prediction's own standard error (se.fit), not the overall
# factorial standard error computed earlier in this script
effects = predict(m, newdata = grid, se.fit = TRUE) %>%
  as_tibble() %>%
  mutate(grid) %>%
  mutate(se = se.fit,
         z = qnorm(0.975),
         upper = fit + se * z,
         lower = fit - se * z)



