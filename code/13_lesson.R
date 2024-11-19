#' @name 13_lesson.R
#' @title Factorial Design
#' @author Tim Fraser

# Example 1 #################################################

library(dplyr)
library(tidyr)

# Get full factorial grid of combinations
grid = expand_grid(
  # Catalyst K
  k = c("A", "B"),
  # Concentration C
  c = c(20, 40),
  # Temperature t
  t = c(160, 180),
) %>%
  # order columns as shown in the example...
  mutate(run = 1:n()) %>%
  select(run, t, c, k)

# We run the experiment once and get these results
data = grid %>% mutate(y = c(60,72,54,68,52,83,45, 80))

data


# Example 2 ##########################################


# Calculate the direct (one-way) treatment effects
data %>%
  summarize(
    dbar_c = mean( y[c==40] - y[c==20] ),
    dbar_t = mean( y[t== 180] - y[t==160] ),
    dbar_k = mean( y[k== "B"] - y[k=="A"] )
  )



# Example 3 ##########################################

# Calculate the two-way treatment effects
data %>%
  reframe(
    xbar1 = y[ (t==180 & k=="B") | (t==160& k=="A") ] %>% mean(),
    xbar0 = y[ (t==160 & k=="B") | (t==180& k=="A")] %>% mean(),
    dbar = xbar1 - xbar0
  )

# Let's get a clearer  glimpse at that first stage, before we take the means
data %>%
  reframe(
    x1 = y[ (t==180 & k=="B") | (t==160& k=="A") ],
    x0 = y[ (t==160 & k=="B") | (t==180& k=="A")]
  )

# Even narrower...
data %>%
  reframe(
    x1a = y[t==160& k=="A" ],
    x1b = y[t==180 & k=="B" ],
    x0a = y[t==180& k=="A"],
    x0b = y[t==160 & k=="B"],
  )


# Example 4 ######################################################

# Three Way Treatment Effects 

# Get treatment effect for TCK...

# Get the TC interaction when K is A
data %>%
  reframe(
    d1 = y[t==180&k=="A"&c==40] - y[t==160&k=="A"&c==40],
    d0 = y[t==180&k=="A"&c==20] - y[t==160&k=="A"&c==20],
    dbar = (d1 - d0)/2
  )

# Get the TC interaction when K is B
data %>%
  reframe(
    d1 = y[t==180&k=="B"&c==40] - y[t==160&k=="B"&c==40],
    d0 = y[t==180&k=="B"&c==20] - y[t==160&k=="B"&c==20],
    dbar = (d1 - d0)/2
  )

# Now get the average difference between these interactions
data %>%
  reframe(
    # Get the TC interaction when K is A
    d1a = y[t==180&k=="A"&c==40] - y[t==160&k=="A"&c==40],
    d0a = y[t==180&k=="A"&c==20] - y[t==160&k=="A"&c==20],
    dbar_a = (d1a - d0a)/2,
    
    # Get the TC interaction when K is B    
    d1b = y[t==180&k=="B"&c==40] - y[t==160&k=="B"&c==40],
    d0b = y[t==180&k=="B"&c==20] - y[t==160&k=="B"&c==20],
    dbar_b = (d1b - d0b)/2,
    
    # Get three way interaction effect    
    dbar = (dbar_b - dbar_a) / 2
  )



# Example 5 #################################

# We run the experiment twice and get these results
data2 = bind_rows(
  grid %>% mutate(rep = 1, y = c(59,74,50,69,50,81,46,79)),
  grid %>% mutate(rep = 2, y = c(61,70,58,67,54,85,44,81))
)


# Let's construct our table
# Differences of replicate runs
data2 %>%
  group_by(run, t,c,k) %>%
  summarize(d = diff(y) ) %>%
  ungroup()

# Variance across replicate runs for each set of conditions
data2 %>%
  group_by(run, t,c,k) %>%
  summarize(var = var(y),
            v = n() - 1)

# Get pooled standard deviation
stat = data2 %>%
  group_by(run, t,c,k) %>%
  summarize(
    # Variance per run
    var = var(y),
    # Degrees of freedom per run
    v = n() - 1) %>%
  ungroup() %>%
  summarize(
    # Pooled variance
    vp = sum(var) / sum(v),
    # How many scenarios are being evaluates (n differences)
    n_diff = n(),
    # variance of effect
    sv = (1 / n_diff + 1/n_diff)*vp,
    # standard error of effect
    se = sqrt(sv)
    )

stat


