# What this file is ----------------------------------------------------------
#
# A short demonstration script. It loads functions_factorial.R and calls each
# of its four functions once on the lattes data, so you can see what each one
# gives back.
#
# Run it from the top of the project folder, a few lines at a time:
# highlight a chunk with your cursor and press CTRL and ENTER
# simultaneously. Change the numbers and run it again -- that is what
# this file is for.
#

# workflow_factorial.R
# Simple demonstration script for the factorial functions

# Source the function
source("functions/functions_factorial.R")

# Load the lattes data
lattes = read.csv("workshops/lattes.csv")

# Execute the functions
se_factorial(formula = tastiness ~ machine + syrup + art, data = lattes)

dbar_oneway(formula = tastiness ~ machine, data = lattes)

dbar_twoway(formula = tastiness ~ machine * syrup, data = lattes)

dbar_threeway(formula = tastiness ~ machine * syrup * art, data = lattes)


