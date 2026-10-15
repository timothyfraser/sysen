# slides_w12_recap.py -------------------------------------------------------
#
# Feeds: Workshop 12 (ANOVA & Latin Squares) slides, Recap section:
#   Example 1 (unpaired t-tests), Example 2 (F-test for two variances),
#   Example 3 (paired t-test), Example 4 (permutation test).
#   Python twin of slides_w12_recap.R.
# Run from the top of the repo:
#   python -X utf8 -P functions/slides_w12_recap.py
# Prints every test result shown on those slides.

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import f

# Example 1 ---------------------------------------------------------------

data = pd.DataFrame({
  'method': ["A"]*10 + ["B"]*10,
  'yield': [89.7, 81.4, 84.5, 84.8, 87.3, 79.7,
            85.1, 81.7, 83.7, 84.5,
            84.7, 86.1, 83.2, 91.9, 86.3, 79.3,
            82.6, 89.1, 83.7, 88.5]})

a = data['yield'][data.method == "A"]
b = data['yield'][data.method == "B"]

# T-test assuming equal variance (unpaired)
print(stats.ttest_ind(a, b, equal_var=True))

# T-test not assuming equal variance (Welch)
print(stats.ttest_ind(a, b, equal_var=False))

# Example 2 ---------------------------------------------------------------

# F test to compare two variances.
stat = a.var(ddof=1) / b.var(ddof=1)
p = 2 * min(f.cdf(stat, len(a)-1, len(b)-1),
            f.sf(stat, len(a)-1, len(b)-1))
print("F =", round(stat, 5), " p =", round(p, 4))

# Are they significantly different? (No --> p = 0.5049)

# Example 3 ---------------------------------------------------------------

# When data comes in pairs, we use paired t-tests.
data2 = pd.DataFrame({
  'yield_a': [89.7, 81.4, 84.5, 84.8, 87.3,
              79.7, 85.1, 81.7, 83.7, 84.5],
  'yield_b': [84.7, 86.1, 83.2, 91.9, 86.3,
              79.3, 82.6, 89.1, 83.7, 88.5]})

print(stats.ttest_rel(data2.yield_a, data2.yield_b))

# Example 4 ---------------------------------------------------------------

# Shuffling is random -- fix the seed so the printed p-value is reproducible.
rng = np.random.default_rng(12345)
y = data['yield'].to_numpy()
is_a = (data.method == "A").to_numpy()

dbar = []
for rep in range(1000):
  z = rng.permutation(y)
  dbar.append(z[is_a].mean() - z[~is_a].mean())
perms = np.array(dbar)

# Get the observed difference of means
obs = y[is_a].mean() - y[~is_a].mean()
print("obs dbar =", round(obs, 2))

# 2-tailed percentage of random stats greater than the observed
print(np.mean(np.abs(perms) >= np.abs(obs)))
