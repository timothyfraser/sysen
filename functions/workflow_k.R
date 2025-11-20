# workflow_k.R
# Simple demonstration script for the k-factor functions

# Source the function
source("functions/functions_k.R")

# Execute the functions
qk(p = 0.95, r = 20, .time = FALSE, .failure = FALSE)

rk(n = 100, r = 20, .time = FALSE, .failure = FALSE)

pk(q = 2, r = 20, .time = FALSE, .failure = FALSE)

dk(x = c(0, 1, 2, 3), r = 21, .time = TRUE, .failure = FALSE)

