# 00_attribute_charts.py
# Tim Fraser
# Extra: attribute control charts (p, np, c and u charts)
# Chapter: Statistical Process Control in Python
#
#
# The R version writes workshops/inventory.csv, bulbs.csv and accidents.csv;
# those csvs are shared, so this Python twin builds the same data but never writes them.

import numpy as np
import pandas as pd
from plotnine import *

# Fraction defection (p) chart
# # of defective items
# has a binomial distribution
# each of the n itmes being tests is being classified
# into 2 categories: defective or not defective
# the probability p of a defective item is constant for every item.

# inventory example
inventory = pd.DataFrame({
  't': list(range(1, 18)),
  'n': [100, 60, 84, 122, 100, 50, 67, 100, 115, 75, 82, 100, 130, 67, 45, 100, 134],
  'x': [10, 4, 7, 12, 6, 4, 5, 5, 9, 3, 6, 7, 7, 5, 2, 4, 8]
})
# inventory.to_csv("workshops/inventory.csv", index = False)

bulbs = pd.DataFrame({
  'n': [200] * 20,
  'x': [4, 8, 6, 6, 4, 8, 2, 1, 9, 6, 8, 1, 2, 9, 4, 3, 9, 6, 2, 7]
}).assign(t = lambda d: range(1, len(d) + 1))[['t', 'x', 'n']]
# bulbs.to_csv("workshops/bulbs.csv", index = False)

# Defect per product (u) chart
# Assumes # of defects per product follows Poisson Distribution
accidents = pd.DataFrame({
  't': list(range(1, 31)),
  'x': [9, 7, 10, 11, 7, 5, 9, 10, 8, 13,
        8, 3, 4, 14, 10, 12, 15, 9, 6, 14,
        9, 15, 11, 8, 4, 2, 8, 5, 3, 2]
})
# accidents.to_csv("workshops/accidents.csv", index = False)



# If X represents the # of defective items in n items,
# then the probability of finding x defective in n items is:
# from math import factorial
# def px(x, n, p): return factorial(n) / (factorial(x) * factorial(n - x)) * p**x * (1 - p)**(n - x)

# px(x = 5, n = 150, p = 0.50)


def ggp(t, x, n, xlab = "Time (Subgroup)", ylab = "Fraction Defective"):

  # Testing values
  # inventory = pd.read_csv("workshops/inventory.csv")
  # t = inventory.t; x = inventory.x; n = inventory.n; xlab = "Time (Subgroup)"; ylab = "Fraction Defective"

  # Make a data.frame
  data = pd.DataFrame({'t': list(t), 'x': list(x), 'n': list(n)})

  # Get subgroup statistics
  # (one row per subgroup t, so these are row-by-row in pandas)
  stat_s = data.copy()
  # Get probability
  stat_s['p'] = stat_s.x / stat_s.n
  # Mean number of defective items
  stat_s['mu'] = stat_s.n * stat_s.p
  # Standard deviation of defective items
  stat_s['sigma'] = np.sqrt(stat_s.n * stat_s.p * (1 - stat_s.p))

  # Add total traits here
  # get total problems and total items
  stat_s['xsum'] = stat_s.x.sum()
  stat_s['nsum'] = stat_s.n.sum()
  # calculate centerline
  stat_s['pbar'] = stat_s.xsum / stat_s.nsum
  # calculate standard deviation with binomial assumptions
  stat_s['se'] = np.sqrt(stat_s.pbar * (1 - stat_s.pbar) / stat_s.n)
  # Calculate 3-sigma control limits
  stat_s['lower'] = stat_s.pbar - 3*stat_s.se
  stat_s['upper'] = stat_s.pbar + 3*stat_s.se
  # Clip the lower estimate at zero or higher
  stat_s['lower'] = stat_s.lower.clip(lower = 0)

  # Visualize it
  gg = (ggplot() +
    # Draw upper and lower control limits
    geom_ribbon(
      data = stat_s,
      mapping = aes(x = 't', ymin = 'lower', ymax = 'upper'),
      fill = "steelblue", alpha = 0.2) +
    # Draw the grand pbar line
    geom_hline(
      data = stat_s,
      mapping = aes(yintercept = 'pbar'),
      size = 1.5, color = "darkgrey"
    ) +
    # Draw probability over time
    geom_line(data = stat_s, mapping = aes(x = 't', y = 'p')) +
    # Draw probability over time with points
    geom_point(data = stat_s, mapping = aes(x = 't', y = 'p')) +
    # Add labels
    labs(x = xlab, y = ylab, subtitle = "Fraction Defective (p) Chart"))

  # Return result
  return gg

# Testing values
# inv = pd.read_csv("workshops/inventory.csv")
# ggp(t = inv.t, x = inv.x, n = inv.n, xlab = "Time (Subgroups)", ylab = "Fraction Defective")


def ggnp(t, x, n, xlab = "Time (Subgroups)", ylab = "Number of Defectives (np)"):

  # Testing values
  # inv = pd.read_csv("workshops/inventory.csv")
  # t = inv.t; x = inv.x; n = inv.n;  xlab = "Time (Subgroups)"; ylab = "Number of Defective (np)"

  # Make a data.frame
  data = pd.DataFrame({'t': list(t), 'x': list(x), 'n': list(n)})

  # Get subgroup statistics
  stat_s = data.copy()
  # Get probability
  stat_s['p'] = stat_s.x / stat_s.n
  # Mean number of defective items
  stat_s['np'] = stat_s.n * stat_s.p

  # Add total traits here
  # get total problems and total items
  stat_s['xsum'] = stat_s.x.sum()
  stat_s['nsum'] = stat_s.n.sum()
  # calculate centerline
  # (R's n() is the number of rows, len() in Python)
  stat_s['npbar'] = (stat_s.n * stat_s.p).sum() / len(stat_s)
  stat_s['pbar'] = (stat_s.n * stat_s.p).sum() / stat_s.n.sum()
  # calculate standard error
  stat_s['se'] = np.sqrt(stat_s.npbar * (1 - stat_s.pbar))
  # Calculate 3-sigma control limits
  stat_s['lower'] = stat_s.npbar - 3*stat_s.se
  stat_s['upper'] = stat_s.npbar + 3*stat_s.se
  # Clip the lower estimate at zero or higher
  stat_s['lower'] = stat_s.lower.clip(lower = 0)

  labels = pd.DataFrame({
    't': [stat_s.t.max()] * 3,
    'type': ["npbar", "upper", "lower"],
    'name': ["npbar", "+3 s", "-3 s"],
    'value': [stat_s.npbar.mean(), stat_s.upper.max(), stat_s.lower.min()]
  })
  labels['value'] = labels.value.round(2)
  labels['text'] = labels.name + " = " + labels.value.map(lambda v: f"{v:g}")

  # Visualize it
  gg = (ggplot() +
    # Draw upper and lower control limits
    geom_ribbon(
      data = stat_s,
      mapping = aes(x = 't', ymin = 'lower', ymax = 'upper'),
      fill = "steelblue", alpha = 0.2) +
    # Draw the grand pbar line
    geom_hline(
      data = stat_s,
      mapping = aes(yintercept = 'npbar'),
      size = 1.5, color = "darkgrey"
    ) +
    # Draw probability over time
    geom_line(data = stat_s, mapping = aes(x = 't', y = 'np')) +
    # Draw probability over time with points
    geom_point(data = stat_s, mapping = aes(x = 't', y = 'np')) +
    # Add text
    # NOTE: R's hjust = 1 (right-aligned) is ha = 'right' in plotnine.
    geom_label(data = labels, mapping = aes(x = 't', y = 'value', label = 'text'), ha = 'right') +
    # Add labels
    labs(x = xlab, y = ylab, subtitle = "Mean Defective (np) Chart"))

  return gg

# Example
# inv = pd.read_csv("workshops/inventory.csv")
# ggnp(t = inv.t, x = inv.x, n = inv.n, xlab = "Time (Subgroups)", ylab = "Number of Defectives")

# Example
# bulbs = pd.read_csv("workshops/bulbs.csv")
# ggnp(t = bulbs.t, x = bulbs.x, n = bulbs.n, xlab = "Time (Subgroups)", ylab = "Number of Defectives")

# More info here:
# https://sixsigmastudyguide.com/attribute-chart-np-chart/


def ggu(t, x, xlab = "Time (Subgroups)", ylab = "Number of Defects (u)"):

  data = pd.DataFrame({'t': list(t), 'x': list(x)})
  # For each time stamp...
  stat_s = data.copy()
  # get total accidents per time stamp
  stat_s['u'] = stat_s.groupby('t').x.transform('sum')
  # within-group sample size
  stat_s['nw'] = stat_s.groupby('t').x.transform('size')
  # Calculate centerline
  stat_s['ubar'] = stat_s.u.sum() / stat_s.nw.sum()
  stat_s['se'] = np.sqrt(stat_s.ubar / stat_s.nw)
  stat_s['lower'] = stat_s.ubar - 3*stat_s.se
  stat_s['upper'] = stat_s.ubar + 3*stat_s.se
  # Curb lower to be no lower than 0
  stat_s['lower'] = stat_s.lower.clip(lower = 0)

  labels = pd.DataFrame({
    't': [stat_s.t.max()] * 3,
    'type': ["ubar", "upper", "lower"],
    'name': ["ubar", "+3 s", "-3 s"],
    'value': [stat_s.ubar.mean(), stat_s.upper.max(), stat_s.lower.min()]
  })
  labels['value'] = labels.value.round(2)
  labels['text'] = labels.name + " = " + labels.value.map(lambda v: f"{v:g}")

  # Visualize
  gg = (ggplot() +
    # Draw upper and lower control limits
    geom_ribbon(
      data = stat_s,
      mapping = aes(x = 't', ymin = 'lower', ymax = 'upper'),
      fill = "steelblue", alpha = 0.2) +
    # Draw the grand pbar line
    geom_hline(
      data = stat_s,
      mapping = aes(yintercept = 'ubar'),
      size = 1.5, color = "darkgrey"
    ) +
    # Draw probability over time
    geom_line(data = stat_s, mapping = aes(x = 't', y = 'u')) +
    # Draw probability over time with points
    geom_point(data = stat_s, mapping = aes(x = 't', y = 'u')) +
    # Add text
    geom_label(data = labels, mapping = aes(x = 't', y = 'value', label = 'text'), ha = 'right') +
    # Add labels
    labs(x = xlab, y = ylab, subtitle = "Number of Defects (u) Chart"))

  return gg

# Example
# acc = pd.read_csv("workshops/accidents.csv")
# ggu(t = acc.t, x = acc.x, xlab = "Time", ylab = "Number of Defects")
