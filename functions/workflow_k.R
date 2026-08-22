# What this file is ----------------------------------------------------------
#
# A short demonstration script. It loads functions_k.R and calls each of the
# four k-factor functions once, so you can see the shape of what each one
# returns.
#
# Run it from the top of the project folder, a few lines at a time:
# highlight a chunk with your cursor and press CTRL and ENTER
# simultaneously. Change the numbers and run it again -- that is what
# this file is for.
#

# workflow_k.R
# Simple demonstration script for the k-factor functions

# Source the function
source("functions/functions_k.R")

# Execute the functions
qk(p = 0.95, r = 20, .time = FALSE, .failure = FALSE)

rk(n = 100, r = 20, .time = FALSE, .failure = FALSE)

pk(q = 2, r = 20, .time = FALSE, .failure = FALSE)

dk(x = c(0, 1, 2, 3), r = 21, .time = TRUE, .failure = FALSE)

