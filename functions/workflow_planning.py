# What this file is ----------------------------------------------------------
#
# A short demonstration script. It loads functions_planning.py and runs
# plan_test() a few times, so you can watch the function plan a life test
# before you use it yourself.
#
# Run it from the top of the project folder, a few lines at a time:
# highlight a chunk with your cursor and run it. Change the numbers and run
# it again -- that is what this file is for.
#

# workflow_planning.py
# Simple demonstration script for the test planning function

import sys
import pandas as pd
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

# Import the function
sys.path.append("functions")
from functions_planning import plan_test

# How many units do I need? Test 5,000 hours, allow 5 failures, 90% confident
print(plan_test("exponential", t = 5000, r = 5, ci = 0.90, lambda_ = 1 / 500000))

# Same question for a lognormal life (leave out n, and n is solved for)
print(plan_test("lognormal", t = 5000, r = 5, ci = 0.90, t50 = 1e5, sigma = 2))

# How long must I test, if I have 200 units? (leave out t)
print(plan_test("lognormal", n = 200, r = 5, ci = 0.90, t50 = 1e5, sigma = 2))
