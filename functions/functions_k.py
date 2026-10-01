# What this file is ----------------------------------------------------------
#
# Another name for functions_kfactors.py. The R k-factor functions live in
# functions_k.R, so this file gives the Python version the same name: load
# either one and you get the same four functions -- qk() for quantiles, pk()
# for cumulative probabilities, dk() for densities, and rk() for random draws.
#
# Load it, from the top of the project folder:
#   import sys
#   sys.path.append("functions")
#   from functions_k import qk
#
# Then try:
#   qk(p = 0.95, r = 20, time = False, failure = False)
#
# One spelling difference from R: R's arguments are .time and .failure;
# Python names cannot start with a dot, so here they are time and failure.
#
# You never need to edit anything below.
#

from functions_kfactors import *  # noqa: F401,F403  (qk, pk, dk, rk)
