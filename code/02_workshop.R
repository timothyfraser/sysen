# 02_workshop.R

#install.packages(c("dplyr", "readr"))
library(readr)
library(dplyr)

la = read_csv("workshops/la_parishes.csv")

# Percent damaged in Hurricane Katrina
la$pc_damage

# what percentage of houses were damaged
# in an average parish?
la$pc_damage %>% mean()

# pc_damage = % houses damaged
# pc_severe = % severely damaged 
# pc_poverty = % residents living in poverty

# dplyr strategy
la %>% summarize(mu = mean(pc_damage))


mu = la$pc_damage %>% mean()
sigma = la$pc_damage %>% sd()

mu
sigma

sims = rnorm(n = 20, mean = mu, sd = sigma)

sims %>% mean()
mu

sims %>% sd()
sigma

sims %>% hist()

la$pc_damage %>% hist()

# rpoisson()

rexp(n = 100, rate = 1 / mean(la$pc_damage))

rexp(n = 100, rate = 1 / mu) %>% hist()



