# 05_recitation.py
# Tim Fraser
# Recitation 5: Statistical process control practice
# Chapter: Statistical Process Control in Python

# 0. Setup ##################################################
# Load packages
import pandas as pd
from plotnine import *
import os, sys
sys.path.append(os.path.abspath('functions'))

# Load data
water = pd.read_csv("workshops/onsen.csv")


# Exercise 1 ###############################################


# Load functions
# ***You'll need to go add this script for this to work.
# https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py
from functions_process_control import *


# Exercise 2 ###############################################


# Pick a quality metric from our onsen dataset,
# and generate averages, standard deviation, and range plots,
# using our helper functions.

# Describe the process under study.


# Starter (uncomment and fill in a metric):
# ggxbar(x = water['time'], y = water['temp'])
# ggs(x = water['time'], y = water['temp'])
# ggr(x = water['time'], y = water['temp'])
# ggprocess(x = water['time'], y = water['temp'])
