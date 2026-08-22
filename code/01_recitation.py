# 01_recitation.py
# Tim Fraser
# Recitation 1: Visualization with plotnine
# Chapter: Visualization with plotnine in Python

# Today, we're going to practice using plotnine!
# plotnine is the Python port of R's ggplot2, so the grammar is the same.
# This is a practice script.
# For the full tutorial, see the textbook.


# Getting Started ---------------------------------------------------------

## Load packages ----
import pandas as p
from plotnine import *
from seaborn import load_dataset
import matplotlib.colors as mcolors

## Load data ----
# R's ggplot2 ships the diamonds data; in Python we get the same data
# from seaborn with load_dataset().
# And instead of dplyr's sample_n(1000), pandas gives us .sample(1000).
diamonds = load_dataset('diamonds').sample(1000)

# View first 5 rows...
diamonds.head()


# Quick Histograms --------------------------------------------------------

# In R, hist() makes a quick, no-frills histogram of a vector.
# pandas gives us the same thing with .hist() on a Series.
diamonds.price.hist()

# Or, for more detailed plots, use plotnine.

# Make a histogram of the price column in the diamonds DataFrame
ggplot(data=diamonds, mapping=aes(x='price')) + geom_histogram()


# Building a Plot, Step by Step -------------------------------------------

## 1. Make a blank plot ----
ggplot()

## 2. Connect the diamonds DataFrame to the plot ----
ggplot(data=diamonds)

## 3. Map variables to plot aesthetics (eg. x axis, color) ----
# Note: in plotnine, aesthetics take the *name* of the column as a string.
ggplot(data=diamonds, mapping=aes(x='price'))

## 4. Add geometries that use those aesthetics ----
ggplot(data=diamonds, mapping=aes(x='price')) + geom_histogram()

## 5. Alternatively, we can plot LAYER BY LAYER - recommended ----
#     This maps a DataFrame to each layer
(ggplot() +
  geom_histogram(data=diamonds, mapping=aes(x='price')))


# Stacking Layers ---------------------------------------------------------

# We can stack transparent blue and red to get purple...
(ggplot() +
  geom_histogram(data=diamonds, mapping=aes(x='price'),
                 fill="blue", alpha=0.5) +
  geom_histogram(data=diamonds, mapping=aes(x='price'),
                 fill="red", alpha=0.5))

# Or we can stack histograms of different variables
# (although that's a weird thing to do)
# (ggplot() +
#   geom_histogram(data=diamonds, mapping=aes(x='price')) +
#   geom_histogram(data=diamonds, mapping=aes(x='carat'),
#                  color="pink", alpha=0.5))


# Static Traits -----------------------------------------------------------

# We can add static traits, like fill, color, size, etc.
# Traits differ for each geom_. Most have color, size, fill, alpha, etc.
(ggplot() +
  geom_histogram(data=diamonds, mapping=aes(x='price'),
                 fill="blue", color="white"))

(ggplot() +
  geom_histogram(data=diamonds, mapping=aes(x='price'),
                 fill="#373737", color="white"))

# R has colors() to list every named color.
# In Python, matplotlib holds that list of named colors.
list(mcolors.CSS4_COLORS)

# Let's try some different colors!
(ggplot() +
  geom_histogram(data=diamonds, mapping=aes(x='price'),
                 fill="darksalmon", color="white"))


# Scatterplots ------------------------------------------------------------

# Let's make scatterplots with geom_point()
(ggplot() +
  geom_point(data=diamonds, mapping=aes(x='carat', y='price')))

## Color as an aesthetic ----

# Let's add color as an **aesthetic**,
# so it varies by the numeric column price
(ggplot() +
  geom_point(
    data=diamonds,
    mapping=aes(x='carat', y='price', color='price')
  ))

# Let's add color as an **aesthetic**,
# so it varies by the categorical column cut
(ggplot() +
  geom_point(
    data=diamonds,
    mapping=aes(x='carat', y='price', color='cut')
  ))

## Transparency and size ----

# Adding transparency with alpha helps.
# alpha = 1 --> solid; 0 --> transparent
(ggplot() +
  geom_point(
    data=diamonds,
    mapping=aes(x='carat', y='price', color='cut'),
    alpha=0.5
  ))

(ggplot() +
  geom_point(
    data=diamonds,
    mapping=aes(x='carat', y='price'),
    alpha=0.05
  ))

(ggplot() +
  geom_point(
    data=diamonds,
    mapping=aes(x='carat', y='price', color='cut'),
    alpha=0.5, size=5
  ))

(ggplot() +
  geom_point(
    data=diamonds,
    mapping=aes(x='carat', y='price'),
    alpha=0.5, size=5, color="blue"
  ))


# Other Advanced Tricks ---------------------------------------------------

## Mapping a constant label ----

# We can map a discrete category to an aesthetic with text.
# In plotnine, the aesthetic is a string of code, so a literal label
# needs its own quotes inside: '"cool rings"'
(ggplot() +
  geom_point(
    data=diamonds,
    mapping=aes(x='carat', y='price', color='"cool rings"'),
    alpha=0.5, size=5
  ))

# We can do this with multiple geometry layers
# to achieve samples colored differently.
(ggplot() +
  geom_point(
    data=diamonds.sample(500),
    mapping=aes(x='carat', y='price', color='"sample 1"'),
    alpha=0.5, size=5
  ) +
  geom_point(
    data=diamonds.sample(500),
    mapping=aes(x='carat', y='price', color='"sample 2"'),
    alpha=0.5, size=5
  ))

## Aesthetic vs. static trait ----

# Careful: in R, if you mark color as an aesthetic AND a static trait,
# the static trait quietly takes priority. plotnine won't let you --
# it raises "Aesthetics {'color'} specified two times." So pick one.
# This errors:
# (ggplot() +
#   geom_point(
#     data=diamonds,
#     mapping=aes(x='carat', y='price', color='cut'),
#     alpha=0.5, size=5, color="blue"
#   ))

# Pick the static trait...
gg = (ggplot() +
  geom_point(
    data=diamonds,
    mapping=aes(x='carat', y='price'),
    alpha=0.5, size=5, color="blue"
  ))


# Themes ------------------------------------------------------------------

# Millions of themes to choose from.
gg + theme_bw()

gg + theme_dark()

gg + theme_minimal()

# Be sure to read the tutorial for more information!
# Great resource throughout term.
