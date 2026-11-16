# What this file is ----------------------------------------------------------
#
# A short demonstration script. It loads functions_planning.R and runs
# plan_test() a few times, so you can watch the function plan a life test
# before you use it yourself.
#
# Run it from the top of the project folder, a few lines at a time:
# highlight a chunk with your cursor and press CTRL and ENTER
# simultaneously. Change the numbers and run it again -- that is what
# this file is for.
#

# workflow_planning.R
# Simple demonstration script for the test planning function

# Source the function
source("functions/functions_planning.R")

# How many units do I need? Test 5,000 hours, allow 5 failures, 90% confident
plan_test("exponential", t = 5000, r = 5, ci = 0.90, lambda = 1 / 500000)

# Same question for a lognormal life (leave out n, and n is solved for)
plan_test("lognormal", t = 5000, r = 5, ci = 0.90, t50 = 1e5, sigma = 2)

# How long must I test, if I have 200 units? (leave out t)
plan_test("lognormal", n = 200, r = 5, ci = 0.90, t50 = 1e5, sigma = 2)
