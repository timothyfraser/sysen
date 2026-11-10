# Code shown on the Lesson 12 (Useful Life Distributions - Exponential) deck: Examples 1-7.
# Each block below is the exact chunk on its slide; the slide's Show answer is what this prints.
# Run from the sigma repo root:  Rscript functions/slides_lesson_7_examples.R
# Charts for the same deck: functions/slides_lesson_7_exponential.R

library(mosaicCalc)

# ---- ex1 --------------------------------------------------
# Example 1: R(t) = 1 / (0.2t + 1)^2, t in months
r = function(t) { 1 / (0.2 * t + 1)^2 }

# MTTF = integral of R(t), from 0 to infinity
mttf = antiD(tilde = r(t) ~ t)
mttf(t = Inf)

# ---- ex2 --------------------------------------------------
# Example 2: z(t) = t / (t + 1), so R(t) = (t + 1) exp(-t)
r = function(t) { (t + 1) * exp(-t) }
# Antiderivative of R(x): a function we can reuse
integral = antiD(tilde = r(x) ~ x)
# MTTF: from 0 up to a large x, standing in for infinity
integral(x = 1000) - integral(x = 0)
# MRL(t): from t onward, divided by R(t)
mrl = function(t) {
  (integral(x = 1000) - integral(x = t)) / r(t) }
c(mrl(0), mrl(1), mrl(4))

# ---- ex3 --------------------------------------------------
# Example 3: failure rate 0.08 %/K = 0.08e-5 per hour
lambda = 0.08e-5

p1 = 1 - exp(-lambda * 20000)
p1                       # 1. one fails by 20,000 hours
p1^2                     # 2. two fail by 20,000 hours
-log(1 - 0.01) / lambda  # 3. hours until 1% have failed

# ---- pump --------------------------------------------------
# Example 5: rotary pump, failure rate per hour
lambda = 4.28e-4

exp(-lambda * 730)      # R(730): survives one month
1 / lambda              # MTTF in hours
1 - exp(-lambda * 730)  # fails in the next month

# ---- first --------------------------------------------------
# Example 6: failure rates per hour
l1 = 0.002; l2 = 0.003
# Pr(T2 > T1): integrate over the time t component 1 fails
f = function(t, l1, l2) { exp(-l2 * t) * l1 * exp(-l1 * t) }
p = antiD(tilde = f(t, l1, l2) ~ t)
p(t = Inf, l1 = l1, l2 = l2)
l1 / (l1 + l2)               # closed form
l = c(0.002, 0.003, 0.005)   # n = 3 components
l / sum(l)                   # Pr(component j fails first)

# ---- mix --------------------------------------------------
# Example 7: fraction p from plant 1, the rest plant 2
p = 0.4; l1 = 1; l2 = 3
r = function(t) p * exp(-l1 * t) + (1 - p) * exp(-l2 * t)
z = function(t) {
  (p * l1 * exp(-l1 * t) + (1 - p) * l2 * exp(-l2 * t)) / r(t)
}
p / l1 + (1 - p) / l2    # MTTF
c(z(0), z(1), z(5))      # falls toward lambda1
