# 02_training.py
# Training: Visualization with ggplot in Python!
# Pairs with R training:
# https://timothyfraser.com/sigma/visualization-with-ggplot-in-r.html
# Tim Fraser


# Getting Started #################################

# Upgrade pip
# !/opt/python/3.8.17/bin/python3.8 -m pip install --upgrade pip

# Install main python packages for this training
# !pip install pandas
# !pip install dfply
# !pip install plotnine
# !pip install os
# !pip install sys
# !pip install gapminder
# !pip install seaborn


# Import packages
import pandas as p # import pandas 
from plotnine import * # import all plotnine visualization functions
# Import gapminder dataset
from gapminder import gapminder as gapminder
# Import diamonds dataset, using seaborn package
from seaborn import load_dataset
diamonds = load_dataset('diamonds')


# Let's view it. (see console below)
gapminder
# Nice, we can see things more concisely.

# Your First Scatterplot #################################
ggplot(data = gapminder, mapping = aes(
  # Let's make the x-axis gross-domestic product per capita (wealth per person)
  x = 'gdpPercap', 
  # Let's make the y-axis country life expectancy
  y = 'lifeExp'))

# We made an empty graph!

# Add + geom_point() to overlay a scatterplot!

( ggplot(data = gapminder, mapping = aes(x = 'gdpPercap', y = 'lifeExp')) +
    geom_point() )
    
    

# What happens when you add alpha, changing its values in the 3 visuals below?
( ggplot(data = gapminder, mapping = aes(x = 'gdpPercap', y = 'lifeExp')) +
    geom_point(alpha = 0.2) )

( ggplot(data = gapminder, mapping = aes(x = 'gdpPercap', y = 'lifeExp')) +
    geom_point(alpha = 0.5) )
    
( ggplot(data = gapminder, mapping = aes(x = 'gdpPercap', y = 'lifeExp')) +
    geom_point(alpha = 1) )
  
  
# We can make it more visually appealing. How would we adjust color?
# If you want to make it a single color, where do you need to write color = ...?
# If you want to make it multiple colors according to a vector, where do you need to write color =?
# Run the following code:

# Version 1
(ggplot(data = gapminder, mapping = aes(x = 'gdpPercap', y = 'lifeExp')) + 
  geom_point(alpha = 0.5, color = "steelblue"))

# Version 2
(ggplot(data = gapminder, mapping = aes(x = 'gdpPercap', y = 'lifeExp', color = 'continent')) +
  geom_point(alpha = 0.5))
  
# Check the textbook for the answer!

# Improving our Visualizations #######################

(ggplot(data = gapminder, mapping = aes(x = 'gdpPercap', y = 'lifeExp', 
  color = 'continent')) +
  geom_point(alpha = 0.5) +
  # Add labels!
  labs(x = "GDP per capita (USD)", # label for x-values
    y = "Life Expectancy (years)", # label for y-values
    color = "Continent", # label for colors
    title = "Does Wealth affect Health?", # overall title
    subtitle = "Global Health Trends by Continent", # subtitle!
    caption = "Points display individual country-year observations.") # caption
 )
 
# We can actually save visualizations as objects too, which can make things faster.
myviz=(ggplot(data = gapminder, mapping = aes(x = 'gdpPercap', y = 'lifeExp', 
                                                color = 'continent')) + 
  geom_point(alpha = 0.5) +
  labs(x = "GDP per capita (USD)", 
       y = "Life Expectancy (years)",
       color = "Continent", 
       title = "Does Wealth affect Health?", # overall title
       subtitle = "Global Health Trends by Continent", # subtitle!
       caption = "Points display individual country-year observations.") # caption
 )

# Run myviz - what happens?
myviz
 
# We can do better, adding things onto our myviz object! Try changing themes. What happens below?
# How about this theme?
myviz + theme_bw()
myviz + theme_dark() # what about this?
myviz + theme_classic()

# Visualizing diamonds data ####################

# Next, let’s use the diamonds dataset, 
# which comes with the seaborn package.
# This is a dataset of over 50,000 diamond sales.

# Check out first three rows
diamonds.head(3)
# Get column names
diamonds.columns
# Get dimensions
diamonds.shape


# Looks like cut is an ordinal variable 
# (fair, good, ideal, etc.), 
# while price is numeric (eg. dollars). 
# A boxplot might be helpful!


(ggplot(data = diamonds, mapping = aes(x = 'cut', y = 'price', group = 'cut')) +
  # notice how we added group = cut, to tell it to use 5 different boxes, one per cut?
  geom_boxplot())

# Huh. How odd. Looks like the cut of diamonds has very little impact on what price they are sold at!

# We can see lots of outliers at the top - really expensive diamonds for that cut.


# Learning Check #######################

# Let’s make this visualization more visually appealing.

# What changed in the code to make these two different visual effects? Why? (Hint: fill.)

(ggplot(data = diamonds, mapping = aes(x = 'cut', y = 'price', group = 'cut')) +
  geom_boxplot(fill = "steelblue"))

(ggplot(data = diamonds, mapping = aes(x = 'cut', y = 'price', group = 'cut', fill = 'cut')) +
  geom_boxplot())


# Visualizing Distributions ##################
# Different geom_ functions use colors in different ways, 
# but this is a good example.

# For example, below is a histogram.
# It visualizes the approximate distribution of a set of values.

# We can see how frequently diamonds are sold for certain prices versus others.

(ggplot(data = diamonds, mapping = aes(x = 'price', group = 'cut', fill = 'cut')) +
  geom_histogram(color = "white") + # notice new function here
  labs(x = "Price (USD)",
    y = "Frequency of Price (Count)",
    title = "US Diamond Sales"))

# Clear environment
globals().clear()

