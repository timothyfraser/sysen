# 05_recitation.py
# Tim Fraser
# Recitation 5: Statistical process control practice
# Chapter: Statistical Process Control in Python

# 0. Setup ##################################################
# Load packages
import sys
import pandas as pd            # data wrangling (dplyr + readr in R)
from plotnine import *         # visuals (ggplot2 in R)

# NOTE: R's ggpubr (for arranging several plots together) has no direct
# Python equivalent here; you can show each plotnine chart on its own.

# Load data
# (Run this script from the root of the sysen repo.)
water = pd.read_csv("workshops/onsen.csv")


# Exercise 1 ###############################################


# Load functions
# ***You'll need to go add this script for this to work.
# https://github.com/timothyfraser/sysen/tree/main/functions/functions_process_control.py
# In R, source() runs the helper script. In Python, we add the functions/
# folder to our path and import the helpers we need.
sys.path.append("functions")
from functions_process_control import *


# Exercise 2 ###############################################


# Pick a quality metric from our onsen dataset,
# and generate averages, standard deviation, and range plots,
# using our helper functions.

# Describe the process under study.
