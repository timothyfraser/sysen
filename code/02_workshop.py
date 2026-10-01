# 02_workshop.py

# %pip install pandas plotnine scipy
import os, sys
import pandas as p
sys.path.append(os.path.abspath('functions'))
from functions_distributions import *

la = p.read_csv("workshops/la_parishes.csv")

# Percent damaged in Hurricane Katrina
la.pc_damage

# what percentage of houses were damaged
# in an average parish?
la.pc_damage.mean()

# pc_damage = % houses damaged
# pc_severe = % severely damaged
# pc_poverty = % residents living in poverty

# pandas strategy
p.DataFrame({'mu': [la.pc_damage.mean()]})


mu = la.pc_damage.mean()
sigma = la.pc_damage.std()

mu
sigma

sims = rnorm(n=20, mean=mu, sd=sigma)

sims.mean()
mu

sims.std()
sigma

hist(sims)

hist(la.pc_damage)

# rpois()

rexp(n=100, rate=1 / la.pc_damage.mean())

hist(rexp(n=100, rate=1 / mu))
