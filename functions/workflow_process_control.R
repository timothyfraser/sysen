# workflow_process_control.R
# Simple demonstration script for the process control functions

# Source the function
source("functions/functions_process_control.R")

# Load example data
water = read_csv("workshops/onsen.csv")

# Example 1: set_theme
set_theme()

# Example 2: describe
describe(x = rnorm(1000, 0, 1))

# Example 3: ggprocess
ggprocess(x = water$time, y = water$temp, xlab = "Subgroup", ylab = "Metric")

# Example 4: get_stat_s
get_stat_s(x = water$time, y = water$temp)

# Example 5: get_stat_t
get_stat_t(x = water$time, y = water$temp)

# Example 6: get_labels
stat_s = get_stat_s(x = water$time, y = water$temp)
get_labels(data = stat_s)

# Example 7: dn
dn(n = 12, reps = 1e4)

# Example 8: bn
bn(n = 12, reps = 1e4)

# Example 9: limits_avg
limits_avg(x = water$time, y = water$temp)

# Example 10: limits_s
limits_s(x = water$time, y = water$temp)

# Example 11: limits_r
limits_r(x = water$time, y = water$temp)

# Example 12: limits_mr
limits_mr(x = water$time, y = water$temp)

# Example 13: ggxbar
ggxbar(x = water$time, y = water$temp, xlab = "Time (Subgroups)", ylab = "Average")

# Example 14: ggs
ggs(x = water$time, y = water$temp, xlab = "Time (Subgroups)", ylab = "Standard Deviation")

# Example 15: ggr
ggr(x = water$time, y = water$temp, xlab = "Time (Subgroups)", ylab = "Range")

# Example 16: ggmr --> not applicable to this dataset
# ggmr(x = water$time, y = water$temp, xlab = "Time (Subgroups)", ylab = "Moving Range")

# Example 17: ggp
# Note: requires t (time), x (defectives), n (sample size)
# Using example data structure
t = 1:10
x = c(2, 3, 1, 4, 2, 3, 1, 2, 3, 2)
n = rep(100, 10)
ggp(t = t, x = x, n = n, xlab = "Time (Subgroup)", ylab = "Fraction Defective")

# Example 18: ggnp
ggnp(t = t, x = x, n = n, xlab = "Time (Subgroups)", ylab = "Number of Defectives (np)")

# Example 19: ggu
# Note: requires t (time), x (defects)
t2 = 1:10
x2 = c(5, 7, 4, 8, 6, 7, 5, 6, 8, 7)
ggu(t = t2, x = x2, xlab = "Time (Subgroups)", ylab = "Number of Defects (u)")

# Example 20: cp
cp(sigma_s = 2, upper = 100, lower = 80)

# Example 21: pp
pp(sigma_t = 2.5, upper = 100, lower = 80)

# Example 22: cpk
cpk(mu = 90, sigma_s = 2, lower = 80, upper = 100)

# Example 23: ppk
ppk(mu = 90, sigma_t = 2.5, lower = 80, upper = 100)

# Example 24: get_index
get_index(x = water$time, y = water$temp, index = "cp", upper = 100, lower = 80)
