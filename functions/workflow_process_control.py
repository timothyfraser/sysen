# workflow_process_control.py
# Simple demonstration script for the process control functions

# Import the functions
from functions.functions_process_control import (
    describe, ggprocess, get_stat_s, get_stat_t, get_labels,
    dn, bn, limits_avg, limits_s, limits_r, limits_mr,
    ggxbar, ggs, ggr, ggmr, ggp, ggnp, ggu,
    cp, pp, cpk, ppk, get_index
)
import numpy as np
import pandas as pd


# Load example data
water = pd.read_csv("workshops/onsen.csv")

# Example 1: describe
x = np.random.normal(0, 1, 1000)
describe(x)

# Example 2: ggprocess
ggprocess(x=water['time'], y=water['temp'], xlab="Subgroup", ylab="Metric")

# Example 3: get_stat_s
get_stat_s(x=water['time'], y=water['temp'])

# Example 4: get_stat_t
get_stat_t(x=water['time'], y=water['temp'])

# Example 5: get_labels
stat_s = get_stat_s(x=water['time'], y=water['temp'])
get_labels(data=stat_s)

# Example 6: dn
dn(n=12, reps=10000)

# Example 7: bn
bn(n=12, reps=10000)

# Example 8: limits_avg
limits_avg(x=water['time'], y=water['temp'])

# Example 9: limits_s
limits_s(x=water['time'], y=water['temp'])

# Example 10: limits_r
limits_r(x=water['time'], y=water['temp'])

# Example 11: limits_mr
limits_mr(x=water['time'], y=water['temp'])

# Example 12: ggxbar
result = ggxbar(x=water['time'], y=water['temp'], xlab="Time (Subgroups)", ylab="Average")
result.show()



# Example 13: ggs
result = ggs(x=water['time'], y=water['temp'], xlab="Time (Subgroups)", ylab="Standard Deviation")
result.show()



# Example 14: ggr
result = ggr(x=water['time'], y=water['temp'], xlab="Time (Subgroups)", ylab="Range")
result.show()

# Example 15: ggmr --> not applicable to this dataset
# result = ggmr(x=water['time'], y=water['temp'], xlab="Time (Subgroups)", ylab="Moving Range")
# result.show()

# Example 16: ggp
# Note: requires t (time), x (defectives), n (sample size)
t = np.arange(1, 11)
x = np.array([2, 3, 1, 4, 2, 3, 1, 2, 3, 2])
n = np.repeat(100, 10)
result = ggp(t=t, x=x, n=n, xlab="Time (Subgroup)", ylab="Fraction Defective")
result.show()

# Example 17: ggnp
result = ggnp(t=t, x=x, n=n, xlab="Time (Subgroups)", ylab="Number of Defectives (np)")
result.show()

# Example 18: ggu
# Note: requires t (time), x (defects)
t2 = np.arange(1, 11)
x2 = np.array([5, 7, 4, 8, 6, 7, 5, 6, 8, 7])
result = ggu(t=t2, x=x2, xlab="Time (Subgroups)", ylab="Number of Defects (u)")
result.show()

# Example 19: cp
cp(sigma_s=2, upper=100, lower=80)

# Example 20: pp
pp(sigma_t=2.5, upper=100, lower=80)

# Example 21: cpk
cpk(mu=90, sigma_s=2, lower=80, upper=100)

# Example 22: ppk
ppk(mu=90, sigma_t=2.5, lower=80, upper=100)

# Example 23: get_index
get_index(x=water['time'], y=water['temp'], index="cp", upper=100, lower=80)
