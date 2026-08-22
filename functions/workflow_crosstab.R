# What this file is ----------------------------------------------------------
#
# A short demonstration script. It loads functions_crosstab.R and runs
# crosstab() once on a sample of times to failure, so you can watch the
# function work on real numbers before you use it yourself.
#
# Run it from the top of the project folder, a few lines at a time:
# highlight a chunk with your cursor and press CTRL and ENTER
# simultaneously. Change the numbers and run it again -- that is what
# this file is for.
#

# workflow_crosstab.R
# Simple demonstration script for the crosstab function

# Source the function
source("functions/functions_crosstab.R")

# Example data: Product Times to Failure
x = c(1,2,2,3,4,5,7,8,9,10,
      11,13,15,16,17,17,18,18,18,20,
      20,21,21,24,27,29,30,37,40,40,
      40,41,46,47,48,52,54,54,55,55,
      64,65,65,65,67,76,76,79,80,80,
      82,86,87,89,94,96,100,101,102,104,
      105,109,109,120,123,141,150,156,156,161,
      164,167,170,178,181,191,193,206,211,212,
      214,236,238,240,265,304,317,328,355,363,
      365,369,389,404,427,435,500,522,547,889)

# Execute the function
crosstab(x, binsize = 100, cutoff = 450)

