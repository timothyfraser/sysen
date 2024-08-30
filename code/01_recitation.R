# 01_recitation.R
# Recitation 1: Visualization with ggplot2!

# Today, we're going to practice using ggplot!
# This is a practice script. 
# For the full tutorial, see the textbook
# https://timothyfraser.com/sigma/visualization-with-ggplot-in-r.html

# Load packages
library(ggplot2)
library(dplyr)

# Let's grab a random sample of a thousand rows,
# using dplyr's sample_n() function.
diamonds = ggplot2::diamonds %>% sample_n(1000)

# View first 6 rows...
diamonds %>% head()


# Make a histogram of the price vector in the diamonds dataframe
# good for quick histograms
diamonds$price %>% hist() # equivalent
hist(diamonds$price) # equivalent

# Or, for more detailed plots, use ggplot.

# Make a histogram of the price vector in the diamonds data.frame
ggplot(data = diamonds, 
       mapping = aes(x = price)) +
  geom_histogram()

# Steps

## 1. Make a blank plot
ggplot()

## 2. Connect the diamonds data.frame to the plot
ggplot(data = diamonds)

## 3. Map variables to plot aesthetics (eg. x axis, color)
ggplot(data = diamonds, mapping = aes(x = price))

## 4. Add geometries that use those aesthetics
ggplot(data = diamonds, mapping = aes(x = price)) +
  geom_histogram()


## 5. Alternatively, we can plot LAYER BY LAYER - recommended
#     This maps a data.frame to each layer
ggplot() +
  geom_histogram(data = diamonds, mapping = aes(x = price))

# Stacking layers
# We can stack transparent blue and red to get purple...
ggplot() +
  geom_histogram(data = diamonds, mapping = aes(x = price),
                 fill = "blue", alpha = 0.5) +
  geom_histogram(data = diamonds, mapping = aes(x = price),
                 fill = "red", alpha = 0.5)


# Stacking layers
# Or we can stack histograms of different variables (although that's a weird thing to do)
# ggplot() +
#   geom_histogram(data = diamonds, mapping = aes(x = price)) +
#   geom_histogram(data = diamonds, mapping = aes(x = carat),
#                  color = "pink", alpha = 0.5)

# We can add static traits, like fill, color, size, etc.
# Traits differ for each geom_. Most have color, size, fill, alpha, etc.
ggplot() +
  geom_histogram(data = diamonds, mapping = aes(x = price),
                 fill = "blue", color = "white")

ggplot() +
  geom_histogram(data = diamonds, mapping = aes(x = price),
                 fill = "#373737", color = "white")

# See all the colors in R!
colors()


# Let's try some different colors!
ggplot() +
  geom_histogram(data = diamonds, mapping = aes(x = price),
                 fill = "darksalmon", color = "white")

# Let's make scatterplots with geom_point()
# diamonds$
ggplot() +
  geom_point(data = diamonds, mapping = aes(x = carat, y = price))

# Let's add color as an **aesthetic**,
# so it varies by numeric vector price
ggplot() +
  geom_point(
    data = diamonds, 
    mapping = aes(x = carat, y = price, color = price)
    )

# Let's add color as an **aesthetic**,
# so it variables by categorical vector cut
ggplot() +
  geom_point(
    data = diamonds, 
    mapping = aes(x = carat, y = price, color = cut)
  )

# Adding transparency with alpha helps. 
# alpha = 1 --> solid; 0 --> transparent
ggplot() +
  geom_point(
    data = diamonds, 
    mapping = aes(x = carat, y = price, color = cut),
    alpha = 0.5
  )

ggplot() +
  geom_point(
    data = diamonds, 
    mapping = aes(x = carat, y = price),
    alpha = 0.05
  )

ggplot() +
  geom_point(
    data = diamonds, 
    mapping = aes(x = carat, y = price, color = cut),
    alpha = 0.5, size = 5
  )

ggplot() +
  geom_point(
    data = diamonds, 
    mapping = aes(x = carat, y = price, color = cut),
    alpha = 0.5, size = 5, color = "blue"
  )

ggplot() +
  geom_point(
    data = diamonds, 
    mapping = aes(x = carat, y = price),
    alpha = 0.5, size = 5, color = "blue"
  )


# Other advanced tricks.

# We can map a discrete category to an aesthetic with text.
ggplot() +
  geom_point(
    data = diamonds, 
    mapping = aes(x = carat, y = price, color = "cool rings"),
    alpha = 0.5, size = 5
  )

# We can do this with multiple geometry layers 
# to achieve samples colored differently.
ggplot() +
  geom_point(
    data = diamonds %>% sample_n(500), 
    mapping = aes(x = carat, y = price, color = "sample 1"),
    alpha = 0.5, size = 5
  ) +
  geom_point(
    data = diamonds %>% sample_n(500), 
    mapping = aes(x = carat, y = price, color = "sample 2"),
    alpha = 0.5, size = 5
  )

# If you mark color as an aesthetic and a static trait,
# the static trait takes priority.
gg = ggplot() +
  geom_point(
    data = diamonds, 
    mapping = aes(x = carat, y = price, color = cut),
    alpha = 0.5, size = 5, color = "blue"
  )

# Millions of themes to choose from.
gg + theme_bw()

gg + theme_dark()

gg + theme_minimal()

# Be sure to read the tutorial for more information!
# Great resource throughout term.
