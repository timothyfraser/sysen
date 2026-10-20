# Code shown on the Lesson 11 (Useful Life Distributions - Exponential) deck: Exercises 1-3 and Examples 1-3.
# Each block below is the exact chunk on its slide; the slide's Show answer is what this prints.
# Run from the sigma repo root:  python3 functions/slides_lesson_7_examples.py
# Charts for the same deck: functions/slides_lesson_7_exponential.py

# ---- ex1 --------------------------------------------------
import numpy as np
from scipy import integrate

# Exercise 1: R(t) = 1 / (0.2t + 1)^2, t in months
r = lambda t: 1 / (0.2 * t + 1) ** 2

# MTTF = integral of R(t) from 0 to infinity
print(integrate.quad(r, 0, np.inf)[0])

# ---- ex2 --------------------------------------------------
import numpy as np
from scipy import integrate

# Exercise 2: z(t) = t / (t + 1), so R(t) = (t + 1) exp(-t)
r = lambda t: (t + 1) * np.exp(-t)
# MTTF, then MRL(t) = (integral of R(x + t) dx) / R(t)
print(round(integrate.quad(r, 0, np.inf)[0], 4))
q = lambda t: integrate.quad(lambda x: r(x + t), 0, np.inf)[0]
print(np.round([q(0) / r(0), q(1) / r(1), q(4) / r(4)], 4))

# ---- ex3 --------------------------------------------------
import numpy as np
# Exercise 3: failure rate 0.08 %/K = 0.08e-5 per hour
lam = 0.08e-5
p1 = 1 - np.exp(-lam * 20000)
print(round(p1, 5))      # 1. one fails by 20,000 hours
print(round(p1**2, 6))   # 2. two fail by 20,000 hours
print(round(-np.log(1 - 0.01) / lam, 1))  # 3. hours to 1%

# ---- pump --------------------------------------------------
import numpy as np

# Example 1: rotary pump, failure rate per hour
lam = 4.28e-4

print(round(np.exp(-lam * 730), 4))      # R(730): survives
print(round(1 / lam, 1))                 # MTTF in hours
print(round(1 - np.exp(-lam * 730), 4))  # fails next month

# ---- first --------------------------------------------------
import numpy as np
from scipy import integrate
# Example 2: failure rates per hour
l1, l2 = 0.002, 0.003
# Pr(T2 > T1): integrate over the time t component 1 fails
f = lambda t: np.exp(-l2 * t) * l1 * np.exp(-l1 * t)
print(round(integrate.quad(f, 0, np.inf)[0], 4))
print(l1 / (l1 + l2))        # closed form
l = np.array([0.002, 0.003, 0.005])   # n = 3 components
print(l / l.sum())           # Pr(component j fails first)

# ---- mix --------------------------------------------------
import numpy as np
# Example 3: fraction p from plant 1, the rest plant 2
p, l1, l2 = 0.4, 1, 3
r = lambda t: p * np.exp(-l1 * t) + (1 - p) * np.exp(-l2 * t)
z = lambda t: (p * l1 * np.exp(-l1 * t) +
               (1 - p) * l2 * np.exp(-l2 * t)) / r(t)
print(p / l1 + (1 - p) / l2)   # MTTF
print(np.round([z(0), z(1), z(5)], 4))   # falls toward l1
