# Workshop 2: Distributions & Descriptive States


# Load packages!
library(dplyr)
library(ggplot2)
# New package!
library(readr) # for reading in csv files!


# Read in this .csv (spreadsheet) of data about Louisiana Parishes
la <- read_csv("workshops/la_parishes.csv")

# This data.frame contains 7 vectors for 20 Lousiana parishes:

# parish: name of each county (called a "parish" in Louisiana)
# code: unique ID 5-digit code for each county
# coastal: (0 or 1) is parish located on coastline?
# pc_damage: % buildings damaged by hurricane
# pc_severe: % buildings SEVERELY damaged by hurricane
# pc_poverty: % residents below poverty line
# pc_nonwhite: % nonwhite residents (communities of color)
# unemployment: unemployment rate per 1000 residents


# Check out its vectors!
la %>% head()
