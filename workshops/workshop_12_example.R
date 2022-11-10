# workshop_12_example.R
# Dr. Fraser, Fall 2022

# Load packages, to get our dplyr, ggplot, tibble, and readr functions
library(tidyverse)
library(broom) # get our tidy() function

# Read data!
donuts = read_csv("/cloud/project/workshops/donuts.csv")

# Having trouble reading in your data?
# You can also use this code:
donuts = read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/donuts.csv")

# Convert type to factor, where treatment group b is first
donuts2 = donuts %>%
  mutate(type = factor(type, levels = c("b", "a")))

# Let's code a basic t.test
t.test(formula = tastiness ~ type, data = donuts2)

# I generally prefer to tidy() the result into a data.frame, and put it inside summarize()
stat = donuts2 %>%
  summarize(t.test(tastiness ~ type) %>% tidy())

# View results
stat
# Let's note our main quantities of interest in 'stat'

# dbar (estimate) = says donuts of type B are 1.32 points tastier than type A

# estimate1 = 4.16
# estimate2 = 2.84

# statistic (t-statistic) 2.61
stat %>% 
  mutate(se = estimate / statistic) %>%
  select(estimate, se, statistic, p.value, conf.low, conf.high)

# Donuts from machine B are 1.32 point tastier. But due to random sampling error,
# depending on the batch, donuts from machine B 
# might be anywhere from 0.298 points tastier to 2.34 points tastier,
# assuming a 95% confidence level.

# There is less than a 1% chance (p = 0.01) that our difference of means 
# is only so extreme due to chance. It is more extreme than 99% of random statistics
# we would otherwise find if type was not related to tastiness.

# Many variables, so it might be easier to just glimpse() it
stat %>% 
  glimpse()


# We can code an analysis of variance (ANOVA) with the aov() function
donuts %>% 
  summarize( aov(tastiness ~ baker) %>% tidy())
# F statistic
# 0 - model is not effective - ESS / RSS
# Inf - model is effective - ESS / RSS 

# Confidence in this F-statistic given this p-value
# p = 0.00704 --> >99.3% confident



# Here are some examples of alternative outcomes you could test
donuts %>% 
  summarize( aov(tastiness ~ baker) %>% tidy())


donuts %>% 
  summarize( aov(lifespan ~ baker) %>% tidy())


donuts2 %>% 
  summarize( t.test(lifespan ~ type) %>% tidy())


donuts2 %>% 
  summarize( t.test(weight ~ type) %>% tidy())


donuts2 %>% 
  summarize( aov(weight ~ type) %>% tidy())

donuts %>%
  lm(formula = tastiness ~ baker) %>%
  glance()

# Instructions:
# Choose another variable (weight or lifespan) and investigate,
# 1. what is the relationship between your variable and 'type' of machine? (t-test)
# 2. what is the relationship between your variable and 'baker'? (anova)
# Please grab your (1) statistic, (2) p-value, and (3) 95% confidence interval (it defaults to 95)

# Check it out!
donuts %>% glimpse()


# We can visualize distributions really quickly using jitter plots too!
donuts %>%
  ggplot(mapping = aes(x = type, y = tastiness)) +
  geom_jitter(width = 0.25, height = 0)


donuts %>%
  ggplot(mapping = aes(x = baker, y = tastiness)) +
  geom_jitter(width = 0.25, height = 0)


