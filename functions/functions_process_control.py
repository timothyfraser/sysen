# functions_process_control.py

# Functions for statistical process control in Python 
#
# !pip install pandas # for dataframes
# !pip install patchworklib
# !pip install plotnine

import pandas as pd
import patchworklib as pw
from plotnine import *


def ggprocess(x, y, xlab='Subgroup', ylab='Metric'):
  
  # import pandas as pd
  # import patchworklib as pw
  # from plotnine import *
  
  # Testing values
  # x = water.time; y = water.temp; xlab='Subgroup'; ylab='Metric'; path = "code/08_process_overview_example.png"
  
  # Convert vectors to series, and bundle as data.frame
  data = pd.DataFrame({
    'x': pd.Series(x),
    'y': pd.Series(y) })
  
  
  # Get grand mean lines
  stat = pd.DataFrame({'mu':  pd.Series(data.y.mean()) })
  
  # describe data
  tab = describe(data.y)
  
  # Make the initial boxplot...
  g1 = (ggplot() +
    # Plot raw points
    geom_jitter(data = data, mapping = aes(x = 'x', y = 'y'), height = 0, width = 0.25) +
    geom_boxplot(data = data, mapping = aes(x = 'x', y = 'y', group = 'x')) +
    # Plot grand mean
    geom_hline(data = stat, mapping = aes(yintercept = 'mu' ), color = 'lightgrey', size = 3) +
    # Add our descriptive stats in the caption!
    labs(x = xlab, y = ylab,
         subtitle = "Process Overview",
         caption = tab.caption[0])
  )
  
  # Make the histogram, but tilt it on its side
  g2 = (ggplot() +
    geom_histogram(
      data = data, mapping = aes(x = 'y'),
      bins = 15, color = "white", fill = "grey") +
    theme_void() +   # Clear the theme
    coord_flip()  # tilt on its side
  )
  
  # Then bind them together into 1 plot, horizontally aligned.
  
  # Let's combine the plots with patchwork
  p1 = pw.load_ggplot(g1, figsize =(5,4))
  p2 = pw.load_ggplot(g2, figsize = (1,4))
  
  # Bundle them together.
  pp = (p1 | p2)
  

  return pp



# Write a get_stat_s() function for an averages and standard deviation chart
def get_stat_s(x, y):
  # Put x and y into a data.frame
  data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
  
  stat_s = data.groupby('x').apply(lambda g: pd.Series({
    # Return each time
    'time': g['x'].values[0],
    # within group mean
    'xbar': g['y'].mean(),
    # within-group range
    'r': g['y'].max() - g['y'].min(),
    # within group standard deviation
    'sd': g['y'].std(),
    # within group sample size n
    'nw': g['y'].count(),
    # within group degrees of freedom 
    'df': g['y'].count() - 1
  }))
  
# Write a get_stat_t() function for averages and standard deviation chart.
def get_stat_t(x, y):
  # To get between-group estimates....
  stat_t = pd.DataFrame({
    'xbbar': [ stat_s.xbar.mean() ],
    'rbar' : [ stat_s.r.mean() ],
    'sdbar' : [ stat_s.sd.mean() ],
    # We can also recalculate sigma_short here too
    'sigma_s': (sum(stat_s.sd**2) / len(stat_s.sd**2))**0.5,
      # Or we can calculate overall standard deviation 
    'sigma_t': water.temp.std()
  })

  return stat_t

def get_labels(data):
  labels = pd.DataFrame({
    'time': [ stat_s.time.max(), stat_s.time.max(), stat_s.time.max() ],
    'type': ['xbbar', 'upper', 'lower'],
    'name': ['mean', '+3 s', '-3 s'],
    'value': [stat_s.xbar.mean(), stat_s.upper.max(), stat_s.lower.min()]
  })
  labels['value'] = round(labels.value, 2)
  labels['text'] = labels.name + " = " + labels.value.astype(str)
  return labels

def ggavgsd(x, y):
  # Put x and y into a data.frame
  data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
  
  stat_s = data.groupby('x').apply(lambda g: pd.Series({
    # Return each time
    'time': g['x'].values[0],
    # within group mean
    'xbar': g['y'].mean(),
    # within-group range
    'r': g['y'].max() - g['y'].min(),
    # within group standard deviation
    'sd': g['y'].std(),
    # within group sample size n
    'nw': g['y'].count(),
    # within group degrees of freedom 
    'df': g['y'].count() - 1
  }))

  # Last, we'll calculate sigma_short (within-group variance)
  stat_s = stat_s.assign(sigma_s = lambda g: (sum(g.sd**2)/len(g.sd**2))**0.5)
  
  # And get standard error (in a way that retains each subgroup's sample size!)
  stat_s = stat_s.assign(se = lambda g: g.sigma_s / g.nw**0.5)
  
  # Calculate 6-sigma control limits!
  stat_s = stat_s.assign(upper = lambda g: g.xbar.mean() + 3*g.se)
  stat_s = stat_s.assign(lower = lambda g: g.xbar.mean() - 3*g.se)

  # Generate labels!
  labels = pd.DataFrame({
    'time': [ stat_s.time.max(), stat_s.time.max(), stat_s.time.max() ],
    'type': ['xbbar', 'upper', 'lower'],
    'name': ['mean', '+3 s', '-3 s'],
    'value': [stat_s.xbar.mean(), stat_s.upper.max(), stat_s.lower.min()]
  })
  labels['value'] = round(labels.value, 2)
  labels['text'] = labels.name + " = " + labels.value.astype(str)


  # Calculate the grand mean
  extra = pd.DataFrame({'xbbar': [stat_s.xbar.mean()] })

  # Generate plot
  gg = (ggplot() +
    geom_hline(
      data = extra,
      mapping = aes(yintercept = 'xbbar'), color = "lightgrey") +
    geom_ribbon(
      data = stat_s, 
      mapping = aes(x = 'time', ymin = 'lower', ymax = 'upper'),
      fill = "steelblue", alpha = 0.2) +
    geom_line(
      data = stat_s, 
      mapping = aes(x = 'time', y = 'xbar'), size = 1) +
    geom_point(
      data = stat_s,
      mapping = aes(x = 'time', y = 'xbar'), size = 5)  +
    geom_label(
      data = labels, 
      mapping = aes(x = 'time', y = 'value', label = 'text'),
      # notice that hjust = 1 is instead in python 'ha = "right"'
      ha = 'right') +
     labs(x = "Time (Subgroups)", y = "Average",
           subtitle = "Average and Standard Deviation Chart")
    )
  
  return gg



def rnorm(n, mean=0, sd=1):
    from scipy.stats import norm
    from pandas import Series
    output = norm.rvs(loc = mean, scale = sd, size=n)
    output = Series(output)
    return output



def dn(n, reps = 10000):
  
  import pandas as pd
  # Depends on rnorm() above
  
  # testing values
  # n = 3; reps = 10000

  sims = pd.DataFrame({'rep':  pd.Series(range(reps))+1, 'n': n })

  # For each replicate, simulate the ranges of n values
  sims = sims.groupby('rep').apply(lambda g: pd.Series({ 
    'r': rnorm(n = g.n, mean = 0, sd = 1).quantile(q = [0,1]).diff().abs().dropna()
    })
    # Pivot result into a data.frame
  ).explode('r')
  
  # Calculate
  stats = pd.DataFrame({
    # mean range
    'd2': sims.mean(),
    # standard deviation of ranges
    'd3': sims.std()
  })
  # and constants for obtaining lower and upper ci for rbar
  stats['D3'] = 1 - 3*stats.d3/stats.d2  
  stats['D4'] = 1 + 3*stats.d3/stats.d2  
  # Sometimes D3 goes negative; we need to bound it at zero
  # For any cases where D3 goes negative, bound it at zero.
  stats['D3'][stats['D3'] < 0] = 0
  
  return stats


def bn(n, reps = 10000):
  # testing values
  # n = 3; reps = 10000

  sims = pd.DataFrame({'rep':  pd.Series(range(reps))+1, 'n': n })

  # For each replicate, simulate the ranges of n values
  sims = sims.groupby('rep').apply(lambda g: pd.Series({ 
    's': rnorm(n = g.n, mean = 0, sd = 1).std()
    })
    # Pivot result into a data.frame
  ).explode('s')
  
  # Calculate
  stats = pd.DataFrame({
    # mean range
    'b2': sims.mean(),
    # standard deviation of ranges
    'b3': sims.std()
  })
  
  stats['C4'] = stats.b2 # sometimes called C4
  stats['A3'] = 3 / (stats.b2 * n**0.5)
  # and constants for obtaining lower and upper ci for rbar
  stats['B3'] = 1 - 3*stats.b3/stats.b2  
  stats['B4'] = 1 + 3*stats.b3/stats.b2  
  # Sometimes B3 goes negative; we need to bound it at zero
  # For any cases where D3 goes negative, bound it at zero.
  stats['B3'][stats['B3'] < 0] = 0
  
  return stats

