## Workshop 8
## Class example
## Tim Fraser, Fall 2020

# Install tidyfault package
devtools::install_github("timothyfraser/tidyfault")

# Load packages
library(tidyverse)
library(tidyfault)

# Get some data to work with
data("fakenodes")
data("fakeedges")

# View our dataframes
fakenodes %>% View()
fakeedges %>% View()

# Curate us a data.frame of all our gates
g = curate(nodes = fakenodes, edges = fakeedges)

# We can technically also make a list object,
# which is a bundle of data.frames.
gg = list(nodes = fakenodes, edges = fakeedges)

# You can see the inside of a list object using the '$' symbol
gg$nodes
gg$edges

# Get coordinates and save the coordinates for our nodes and edeges
# as a list object.
gg = illustrate(nodes = fakenodes, edges = fakeedges,
           node_key = "id", type = "both")

# Plot our edges and nodes from 'gg', which now have coordinates!
ggplot() +
  geom_line(data = gg$edges,
            mapping = aes(x = x, y = y, group = edge_id)) +
  geom_point(data = gg$nodes,
             mapping = aes(x = x, y = y, 
                           fill = type,
                           shape = type),
             size = 10, color = "white") +
  # Add labels!
  geom_text(data = gg$nodes,
            mapping = aes(x = x, y = y,
                          label = event)) +
  # Add shapes! See workshop for more explanation about shapes
  scale_shape_manual(values = c(21, 22, 23, 24)) +
  theme_void(base_size = 14) +
  theme(legend.position = "bottom") 

# Or, gather stats about your fault tree

# Curate gives us a data.frame where each row is a gate
g = curate(fakenodes, fakeedges)

# Equate tells us the boolean equation for the fault tree
g %>% equate()

# Formualate turns that equation into a function
f = g %>% equate() %>% formulate()

# We can use that function to compute probabilities
f(A = 0.1, B = 0.3, C = 0.2, D = 0.8)

# Concentreate runs the mocus algorithm to get minimal cutsets
q = curate(fakenodes, fakeedges) %>%
  concentrate(method = "mocus")

# Tabulate gives us some statistics summarizing our minimal cutsets
# (described further in workshop tutorial)
q %>%
  tabulate(formula = f)

# We can also run simulations!!!
tibble(
  # Simulate the probability of A 100 times, drawing from a normal distribution
  A = rnorm(n = 100, mean = 0.1, sd = 0.3),
  # and so on
  B = rnorm(n = 100, mean = 0.5, sd = 0.4),
  C = rnorm(n = 100, mean = 0.3, sd = 0.5),
  D = rnorm(n = 100, mean = 0.2, sd = 0.1),
  # Calculate probability of T for each of our 100 simulations!
  T = f(A,B,C,D)
) %>%
  # Calculate some quantities of interest!
  summarize(
    # Mean occurence (probability)
    mean = mean(T),
    # standard deviation
    sd = sd(T),
    # standard error
    se = sd(T) / sqrt(n()),
    # Confidence intervals for 95% interval!
    lower = qnorm(0.025, mean, sd = se),
    upper = qnorm(0.975, mean, sd = se)
  )


# Yay! Go simulate some fault trees!


