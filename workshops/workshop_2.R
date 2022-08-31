# Workshop 2: Distributions & Descriptive States


# Load packages!
library(dplyr)
library(ggplot2)
library(MASS) # for fitting distributions
# New package!
library(readr) # for reading in csv files!


# Read in this .csv (spreadsheet) of data about Louisiana Parishes
la <- read_csv("workshops/la_parishes.csv")

# This data.frame contains 7 vectors for 20 Lousiana parishes:

# fips: unique ID for each county (called a "parish")
# pc_damaged: % buildings damaged by hurricane
# pc_severe: % buildings SEVERELY damaged by hurricane
# coastal: (0 or 1) is parish located on coastline?
# pc_poverty: % residents below poverty line
# pc_nonwhite: % nonwhite residents (communities of color)
# unemployment: unemployment rate per 1000 residents


# Check out its vectors!
la %>% head()
