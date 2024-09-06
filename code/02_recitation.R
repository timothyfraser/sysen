# Lousiana Parishes ########################################

## Load packages ###########################
library(dplyr)
library(readr)

## Data ###########################
# Read in stuff
la = read_csv("workshops/la_parishes.csv")

## Statistics ###########################

# Percentage of houses damaged by the hurricane
la$pc_damage

sigma = la$pc_damage %>% sd()
# The percentage of houses damaged by the hurricane varies from the average by ~20 (units)
mu = la$pc_damage %>% mean()
# The average county had 51% of houses damaged
n = la$pc_damage %>% length()

mu + sigma
mu - sigma

# mu + sigma*3
# mu - sigma*3


# Coefficient of Variation 
sigma / mu

# Standard Error
se = sigma / sqrt(n)

# Confidence Interval
mu + se*1.96
mu - se*1.96


mu


rm(list = ls())



# Quality Control with Cheese ##########################


## Packages ########################
library(dplyr)

## Data ###########################
a = c(50, 70, 125, 235, 230, 200, 180, 260, 300, 500, 275, 280)
b = c(300, 380, 250, 50, 55, 57, 60, 65, 100, 150, 250, 200, 150, 175, 225, 200, 225, 250)
c= c(400, 300, 400, 300, 350, 200, 250, 300, 330, 375)


## Mean
## Std
## Coefficient of Variation / Standard Error

# Tell me who you'd buy your cheese from and why.


mean(a)
mean(b)
mean(c)

data = data.frame(
  type = c("a", "b", "c"),
  mu = c( mean(a), mean(b), mean(c) ),
  sigma = c( sd(a), sd(b), sd(c)  ),
  n = c( length(a), length(b), length(c) )
)

data$cv = data$sigma / data$mu
data$se = data$sigma / sqrt(data$n)

data$upper = data$mu + data$sigma
data$lower = data$mu - data$sigma
data

library(ggplot2)

ggplot() +
  geom_point(data = data, mapping = aes(x = mu, y = type, color = "Mean")) +
  geom_point(data = data, mapping = aes(x = lower, y = type, color = "-1 sigma")) +
  geom_point(data = data, mapping = aes(x = upper, y = type, color = "+1 sigma")) +
  labs(x = "Time to Failure (hours)")



