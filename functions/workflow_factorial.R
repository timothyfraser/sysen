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


