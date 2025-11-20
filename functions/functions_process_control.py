# functions_process_control.py
# Script of Python functions for statistical process control.

"""
Functions for Statistical Process Control

This module provides functions for performing statistical process control (SPC) analysis,
including descriptive statistics, control charts, and process monitoring tools.
"""

import pandas as pd
import numpy as np
from scipy import stats
from plotnine import *
try:
    import patchworklib as pw
    PATCHWORK_AVAILABLE = True
except ImportError:
    PATCHWORK_AVAILABLE = False


def describe(x):
    """
    Describe a vector x
    
    Calculates summary statistics including mean, standard deviation, skewness, and kurtosis
    for a numeric vector, and formats them into a caption string.
    
    Parameters
    ----------
    x : array-like
        A numeric vector of observed metric values
    
    Returns
    -------
    pd.DataFrame
        A DataFrame with columns: mean, sd, skew, kurtosis, caption
        The caption column contains a formatted string with all statistics.
    
    Examples
    --------
    >>> import numpy as np
    >>> x = np.random.normal(0, 1, 1000)
    >>> describe(x)
    """
    x = pd.Series(x)
    
    # Calculate summary statistics
    out = pd.DataFrame({
        'mean': [x.mean()],
        'sd': [x.std()],
        'skew': [stats.skew(x.dropna())],
        'kurtosis': [stats.kurtosis(x.dropna())]
    })
    
    # Create caption string
    out['caption'] = (
        "Process Mean: " + out['mean'].round(2).astype(str) + " | " +
        "SD: " + out['sd'].round(2).astype(str) + " | " +
        "Skewness: " + out['skew'].round(2).astype(str) + " | " +
        "Kurtosis: " + out['kurtosis'].round(2).astype(str)
    )
    
    return out


def ggprocess(x, y, xlab='Subgroup', ylab='Metric'):
    """
    Make a Process Overview Diagram in ggplot
    
    Creates a combined visualization showing process behavior over time with a boxplot
    and a side histogram.
    
    Parameters
    ----------
    x : array-like
        Vector of subgroup values (usually time). Must be same length as y.
    y : array-like
        Vector of metric values (e.g., performance). Must be same length as x.
    xlab : str, optional
        Label for x-axis. Default is 'Subgroup'.
    ylab : str, optional
        Label for y-axis. Default is 'Metric'.
    
    Returns
    -------
    ggplot or patchwork object
        A combined plot showing process overview with boxplot and histogram.
        If patchworklib is available, returns a combined plot. Otherwise returns the main plot.
    
    Examples
    --------
    >>> import pandas as pd
    >>> water = pd.read_csv("workshops/onsen.csv")
    >>> ggprocess(x=water['time'], y=water['temp'], xlab="Subgroup", ylab="Metric")
    """
    # Convert vectors to series, and bundle as data.frame
    data = pd.DataFrame({
        'x': pd.Series(x),
        'y': pd.Series(y)
    })
    
    # Get grand mean lines
    stat = pd.DataFrame({'mu': [data['y'].mean()]})
    
    # Describe data
    tab = describe(data['y'])
    
    # Make the initial boxplot
    g1 = (ggplot() +
          # Plot raw points
          geom_jitter(data=data, mapping=aes(x='x', y='y'), height=0, width=0.25) +
          geom_boxplot(data=data, mapping=aes(x='x', y='y', group='x')) +
          # Plot grand mean
          geom_hline(data=stat, mapping=aes(yintercept='mu'), color='lightgrey', size=3) +
          # Add our descriptive stats in the caption!
          labs(x=xlab, y=ylab,
               subtitle="Process Overview",
               caption=tab['caption'].iloc[0]))
    
    # Make the histogram, but tilt it on its side
    g2 = (ggplot() +
          geom_histogram(data=data, mapping=aes(x='y'),
                        bins=15, color="white", fill="grey") +
          theme_void() +  # Clear the theme
          coord_flip())  # tilt on its side
    
    # Then bind them together into 1 plot, horizontally aligned.
    if PATCHWORK_AVAILABLE:
        # Let's combine the plots with patchwork
        p1 = pw.load_ggplot(g1, figsize=(5, 4))
        p2 = pw.load_ggplot(g2, figsize=(1, 4))
        # Bundle them together.
        pp = (p1 | p2)
        return pp
    else:
        # Return just the main plot if patchwork not available
        return g1


def get_stat_s(x, y):
    """
    Get Subgroup Statistics
    
    Calculates within-subgroup statistics including means, ranges, standard deviations,
    and control limits for each subgroup.
    
    Parameters
    ----------
    x : array-like
        Vector of subgroup values (usually time). Must be same length as y.
    y : array-like
        Vector of metric values (e.g., performance). Must be same length as x.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with columns: x, xbar, r, s, nw, df, sigma_s, sigma_t, se, upper, lower
        One row per subgroup.
    
    Examples
    --------
    >>> import pandas as pd
    >>> water = pd.read_csv("workshops/onsen.csv")
    >>> get_stat_s(x=water['time'], y=water['temp'])
    """
    # Make a data.frame
    data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
    
    # Calculate sigma_t direct
    sigma_t = data['y'].std()
    
    # Calculate statistics for each subgroup
    stat_s = (data.groupby('x')
              .agg({
                  'y': ['mean', 'min', 'max', 'std', 'count']
              })
              .reset_index())
    
    # Flatten column names
    stat_s.columns = ['x', 'xbar', 'y_min', 'y_max', 's', 'nw']
    stat_s['r'] = stat_s['y_max'] - stat_s['y_min']
    stat_s['df'] = stat_s['nw'] - 1
    stat_s = stat_s[['x', 'xbar', 'r', 's', 'nw', 'df']]
    
    # Calculate between-group estimates
    stat_s['xbbar'] = stat_s['xbar'].mean()
    # Calculate sigma_s (pooled standard deviation)
    stat_s['sigma_s'] = np.sqrt((stat_s['df'] * stat_s['s']**2).sum() / stat_s['df'].sum())
    stat_s['sigma_t'] = sigma_t
    stat_s['se'] = stat_s['sigma_s'] / np.sqrt(stat_s['nw'])
    stat_s['upper'] = stat_s['xbbar'] + 3 * stat_s['se']
    stat_s['lower'] = stat_s['xbbar'] - 3 * stat_s['se']
    
    return stat_s


def get_stat_t(x, y):
    """
    Get Total Statistics
    
    Calculates overall process statistics summarizing behavior across all subgroups.
    
    Parameters
    ----------
    x : array-like
        Vector of subgroup values (usually time). Must be same length as y.
    y : array-like
        Vector of metric values (e.g., performance). Must be same length as x.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with columns: xbbar, rbar, sbar, sigma_s, sigma_t, n
        One row with overall statistics.
    
    Examples
    --------
    >>> import pandas as pd
    >>> water = pd.read_csv("workshops/onsen.csv")
    >>> get_stat_t(x=water['time'], y=water['temp'])
    """
    # Make a data.frame
    data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
    
    # Get total standard deviation
    sigma_t = data['y'].std()
    
    # Get statistics for each subgroup
    stat_s = (data.groupby('x')
              .agg({
                  'y': ['mean', 'min', 'max', 'std', 'count']
              })
              .reset_index())
    
    stat_s.columns = ['x', 'xbar', 'y_min', 'y_max', 's', 'nw']
    stat_s['r'] = stat_s['y_max'] - stat_s['y_min']
    stat_s['df'] = stat_s['nw'] - 1
    
    # Now calculate one row of total statistics
    output = pd.DataFrame({
        # average average
        'xbbar': [stat_s['xbar'].mean()],
        # average range
        'rbar': [stat_s['r'].mean()],
        # average standard deviation
        'sbar': [stat_s['s'].mean()],
        # average within-group standard deviation
        'sigma_s': [np.sqrt((stat_s['s']**2 * stat_s['nw']).sum() / stat_s['nw'].sum())],
        # overall standard deviation
        'sigma_t': [sigma_t],
        # total sample size
        'n': [stat_s['nw'].sum()]
    })
    
    return output


def get_labels(data):
    """
    Get Labels from Subgroup Statistics
    
    Creates labels for control charts showing mean, upper, and lower control limits.
    
    Parameters
    ----------
    data : pd.DataFrame
        Output of get_stat_s() function
    
    Returns
    -------
    pd.DataFrame
        DataFrame with columns: x, type, name, value, text
        Three rows for xbbar, upper, and lower labels.
    
    Examples
    --------
    >>> import pandas as pd
    >>> water = pd.read_csv("workshops/onsen.csv")
    >>> stat_s = get_stat_s(x=water['time'], y=water['temp'])
    >>> get_labels(data=stat_s)
    """
    labels = pd.DataFrame({
        'x': [data['x'].max(), data['x'].max(), data['x'].max()],
        'type': ['xbbar', 'upper', 'lower'],
        'name': ['mean', '+3 s', '-3 s'],
        'value': [data['xbbar'].iloc[0], data['upper'].max(), data['lower'].min()]
    })
    labels['value'] = labels['value'].round(2)
    labels['text'] = labels['name'] + " = " + labels['value'].astype(str)
    
    return labels


def rnorm(n, mean=0, sd=1):
    """
    Generate random normal values
    
    Python equivalent of R's rnorm() function.
    
    Parameters
    ----------
    n : int
        Number of observations
    mean : float, optional
        Mean of the distribution. Default is 0.
    sd : float, optional
        Standard deviation of the distribution. Default is 1.
    
    Returns
    -------
    pd.Series
        Series of random normal values
    """
    output = stats.norm.rvs(loc=mean, scale=sd, size=n)
    output = pd.Series(output)
    return output


def dn(n, reps=10000):
    """
    Calculate control constants for range charts
    
    Simulates ranges from normal distributions to calculate d2, d3, D3, and D4 constants
    used in range control charts.
    
    Parameters
    ----------
    n : int
        Subgroup size
    reps : int, optional
        Number of simulation replicates. Default is 10000.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with columns: d2, d3, D3, D4
    
    Examples
    --------
    >>> dn(n=12)
    """
    sims = pd.DataFrame({'rep': pd.Series(range(reps)) + 1, 'n': n})
    
    # For each replicate, simulate the ranges of n values
    def calc_range(g):
        r = rnorm(n=int(g['n'].iloc[0]), mean=0, sd=1)
        return pd.Series({'r': r.max() - r.min()})
    
    sims = sims.groupby('rep').apply(calc_range).reset_index(drop=True)
    
    # Calculate statistics
    stats_df = pd.DataFrame({
        # mean range
        'd2': [sims['r'].mean()],
        # standard deviation of ranges
        'd3': [sims['r'].std()]
    })
    
    # and constants for obtaining lower and upper ci for rbar
    stats_df['D3'] = 1 - 3 * stats_df['d3'] / stats_df['d2']
    stats_df['D4'] = 1 + 3 * stats_df['d3'] / stats_df['d2']
    # Sometimes D3 goes negative; we need to bound it at zero
    stats_df.loc[stats_df['D3'] < 0, 'D3'] = 0
    
    return stats_df


def bn(n, reps=10000):
    """
    Calculate control constants for standard deviation charts
    
    Simulates standard deviations from normal distributions to calculate b2, b3, C4, A3,
    B3, and B4 constants used in standard deviation control charts.
    
    Parameters
    ----------
    n : int
        Subgroup size
    reps : int, optional
        Number of simulation replicates. Default is 10000.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with columns: b2, b3, C4, A3, B3, B4
    
    Examples
    --------
    >>> stat = bn(n=12)
    >>> sbar = 2.5
    >>> # Lower Control Limit
    >>> sbar * stat['B3'].iloc[0]
    >>> # Upper control limit
    >>> sbar * stat['B4'].iloc[0]
    """
    sims = pd.DataFrame({'rep': pd.Series(range(reps)) + 1, 'n': n})
    
    # For each replicate, simulate the standard deviations of n values
    def calc_sd(g):
        s = rnorm(n=int(g['n'].iloc[0]), mean=0, sd=1)
        return pd.Series({'s': s.std()})
    
    sims = sims.groupby('rep').apply(calc_sd).reset_index(drop=True)
    
    # Calculate statistics
    stats_df = pd.DataFrame({
        # mean standard deviation
        'b2': [sims['s'].mean()],
        # standard deviation of standard deviations
        'b3': [sims['s'].std()]
    })
    
    stats_df['C4'] = stats_df['b2']  # sometimes called C4
    stats_df['A3'] = 3 / (stats_df['b2'] * np.sqrt(n))
    # and constants for obtaining lower and upper ci
    stats_df['B3'] = 1 - 3 * stats_df['b3'] / stats_df['b2']
    stats_df['B4'] = 1 + 3 * stats_df['b3'] / stats_df['b2']
    # Sometimes B3 goes negative; we need to bound it at zero
    stats_df.loc[stats_df['B3'] < 0, 'B3'] = 0
    
    return stats_df


def limits_avg(x, y):
    """
    Get Upper and Lower Control Limits for an Averages Chart, using Control Constants
    
    Calculates control limits for an X-bar (averages) chart using control constants A3.
    
    Parameters
    ----------
    x : array-like
        Vector of subgroup values (usually time). Must be same length as y.
    y : array-like
        Vector of metric values (e.g., performance). Must be same length as x.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with subgroup statistics and control limits (upper, lower)
        One row per subgroup.
    
    Examples
    --------
    >>> import pandas as pd
    >>> water = pd.read_csv("workshops/onsen.csv")
    >>> limits_avg(x=water['time'], y=water['temp'])
    """
    # Make a data.frame
    data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
    
    # Get within-group stats
    stat_s = (data.groupby('x')
              .agg({
                  'y': ['mean', 'std', 'count']
              })
              .reset_index())
    
    stat_s.columns = ['x', 'xbar', 's', 'nw']
    stat_s['df'] = stat_s['nw'] - 1
    
    # For each different subgroup sample size, calculate control constant A3
    constants = (stat_s[['nw']]
                 .drop_duplicates()
                 .apply(lambda row: pd.Series({
                     'A3': bn(n=int(row['nw']), reps=10000)['A3'].iloc[0]
                 }), axis=1))
    constants['nw'] = stat_s[['nw']].drop_duplicates()['nw'].values
    
    # Join in the control constants
    stat_s = stat_s.merge(constants, on='nw', how='left')
    
    # Add in sbar and xbbar
    stat_s['sbar'] = np.sqrt((stat_s['df'] * stat_s['s']**2).sum() / stat_s['df'].sum())
    stat_s['xbbar'] = stat_s['xbar'].mean()
    
    # Calculate upper and lower control limits
    stat_s['lower'] = stat_s['xbbar'] - stat_s['A3'] * stat_s['sbar']
    stat_s['upper'] = stat_s['xbbar'] + stat_s['A3'] * stat_s['sbar']
    
    return stat_s


def limits_s(x, y):
    """
    Get Upper and Lower Control Limits for a Standard Deviation Chart, using Control Constants
    
    Calculates control limits for an S (standard deviation) chart using control constants B3 and B4.
    
    Parameters
    ----------
    x : array-like
        Vector of subgroup values (usually time). Must be same length as y.
    y : array-like
        Vector of metric values (e.g., performance). Must be same length as x.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with subgroup statistics and control limits (upper, lower)
        One row per subgroup.
    
    Examples
    --------
    >>> import pandas as pd
    >>> water = pd.read_csv("workshops/onsen.csv")
    >>> limits_s(x=water['time'], y=water['temp'])
    """
    # Make a data.frame
    data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
    
    # Get within-group stats
    stat_s = (data.groupby('x')
              .agg({
                  'y': ['std', 'count']
              })
              .reset_index())
    
    stat_s.columns = ['x', 's', 'nw']
    stat_s['df'] = stat_s['nw'] - 1
    
    # For each different subgroup sample size, calculate control constants
    constants_list = []
    for nw in stat_s['nw'].unique():
        bn_stats = bn(n=int(nw), reps=10000)
        constants_list.append({
            'nw': nw,
            'B3': bn_stats['B3'].iloc[0],
            'B4': bn_stats['B4'].iloc[0]
        })
    constants = pd.DataFrame(constants_list)
    
    # Join in the control constants
    stat_s = stat_s.merge(constants, on='nw', how='left')
    
    # Add in sbar
    stat_s['sbar'] = np.sqrt((stat_s['df'] * stat_s['s']**2).sum() / stat_s['df'].sum())
    
    # Calculate upper and lower control limits
    stat_s['lower'] = stat_s['B3'] * stat_s['sbar']
    stat_s['upper'] = stat_s['B4'] * stat_s['sbar']
    
    return stat_s


def limits_r(x, y):
    """
    Get Upper and Lower Control Limits for a Range Chart, using Control Constants
    
    Calculates control limits for an R (range) chart using control constants D3 and D4.
    
    Parameters
    ----------
    x : array-like
        Vector of subgroup values (usually time). Must be same length as y.
    y : array-like
        Vector of metric values (e.g., performance). Must be same length as x.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with subgroup statistics and control limits (upper, lower)
        One row per subgroup.
    
    Examples
    --------
    >>> import pandas as pd
    >>> water = pd.read_csv("workshops/onsen.csv")
    >>> limits_r(x=water['time'], y=water['temp'])
    """
    # Make a data.frame
    data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
    
    # Get within-group stats
    stat_s = (data.groupby('x')
              .agg({
                  'y': ['min', 'max', 'count']
              })
              .reset_index())
    
    stat_s.columns = ['x', 'y_min', 'y_max', 'nw']
    stat_s['r'] = stat_s['y_max'] - stat_s['y_min']
    stat_s['df'] = stat_s['nw'] - 1
    
    # For each different subgroup sample size, calculate control constants
    constants_list = []
    for nw in stat_s['nw'].unique():
        dn_stats = dn(n=int(nw), reps=10000)
        constants_list.append({
            'nw': nw,
            'D3': dn_stats['D3'].iloc[0],
            'D4': dn_stats['D4'].iloc[0]
        })
    constants = pd.DataFrame(constants_list)
    
    # Join in the control constants
    stat_s = stat_s.merge(constants, on='nw', how='left')
    
    # Add in rbar
    stat_s['rbar'] = stat_s['r'].mean()
    
    # Calculate upper and lower control limits
    stat_s['lower'] = stat_s['D3'] * stat_s['rbar']
    stat_s['upper'] = stat_s['D4'] * stat_s['rbar']
    
    return stat_s


def limits_mr(x, y):
    """
    Get Upper and Lower Control Limits for a Moving Range Chart, using Control Constants
    
    Calculates control limits for a moving range chart when subgroup size n=1.
    
    Parameters
    ----------
    x : array-like
        Vector of subgroup values (usually time). Must be same length as y.
    y : array-like
        Vector of metric values (e.g., performance). Must be same length as x.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with moving range statistics and control limits
    
    Examples
    --------
    >>> import pandas as pd
    >>> water = pd.read_csv("workshops/onsen.csv")
    >>> # Suppose we sample just the first out of each our months
    >>> indiv = water[water['id'].isin([1, 21, 41, 61, 81, 101, 121, 141])]
    >>> limits_mr(x=indiv['time'], y=indiv['temp'])
    """
    # Make a data.frame
    data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
    
    # Convert our original dataset into a set of moving ranges
    data2 = pd.DataFrame({
        'x': data['x'].iloc[1:].values,
        'mr': np.abs(np.diff(data['y'].values))
    })
    
    # Estimate d2 when subgroup size n = 1
    d2 = np.mean(np.abs(np.diff(rnorm(n=10000, mean=0, sd=1).values)))
    
    # Get average moving range
    mrbar = data2['mr'].mean()
    
    # approximate sigma s
    sigma_s = mrbar / d2
    # Our subgroup size was 1, right?
    n = 1
    # so this means sigma_s just equals the standard error here
    se = sigma_s / np.sqrt(n)
    # compute upper 3-se bound
    upper = mrbar + 3 * se
    # and lower ALWAYS equals 0 for moving range
    lower = 0
    
    stat = pd.DataFrame({
        'x': data2['x'].values,
        'mr': data2['mr'].values,
        'mrbar': [mrbar] * len(data2),
        'd2': [d2] * len(data2),
        'sigma_s': [sigma_s] * len(data2),
        'n': [n] * len(data2),
        'se': [se] * len(data2),
        'upper': [upper] * len(data2),
        'lower': [lower] * len(data2)
    })
    
    return stat


def ggxbar(x, y, xlab="Time (Subgroups)", ylab="Average"):
    """
    Average Control Chart with ggplot
    
    Creates an X-bar (averages) control chart showing subgroup means over time with
    control limits and center line.
    
    Parameters
    ----------
    x : array-like
        Vector of subgroup values (usually time). Must be same length as y.
    y : array-like
        Vector of metric values (e.g., performance). Must be same length as x.
    xlab : str, optional
        Label for x-axis. Default is "Time (Subgroups)".
    ylab : str, optional
        Label for y-axis. Default is "Average".
    
    Returns
    -------
    ggplot
        A control chart visualization
    
    Examples
    --------
    >>> import pandas as pd
    >>> water = pd.read_csv("workshops/onsen.csv")
    >>> ggxbar(x=water['time'], y=water['ph'], xlab="Time (Subgroups)", ylab="Average pH")
    """
    data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
    
    # Get statistics for each subgroup
    stat_s = get_stat_s(x=data['x'], y=data['y'])
    
    # Generate labels
    labels = get_labels(stat_s)
    
    # Get overall statistics
    stat_t = get_stat_t(x=x, y=y)
    
    # Generate plot
    gg = (ggplot() +
          geom_hline(data=stat_t, mapping=aes(yintercept='xbbar'), color="lightgrey") +
          geom_ribbon(data=stat_s, mapping=aes(x='x', ymin='lower', ymax='upper'),
                      fill="steelblue", alpha=0.2) +
          geom_line(data=stat_s, mapping=aes(x='x', y='xbar'), size=1) +
          geom_point(data=stat_s, mapping=aes(x='x', y='xbar'), size=5) +
          geom_label(data=labels, mapping=aes(x='x', y='value', label='text'),
                    ha='right') +  # horizontally justify the labels
          labs(x=xlab, y=ylab, subtitle="Average Chart"))
    
    return gg


def ggs(x, y, xlab="Time (Subgroups)", ylab="Standard Deviation"):
    """
    Standard Deviation Chart with ggplot
    
    Creates an S (standard deviation) control chart showing subgroup standard deviations
    over time with control limits and center line.
    
    Parameters
    ----------
    x : array-like
        Vector of subgroup values (usually time). Must be same length as y.
    y : array-like
        Vector of metric values (e.g., performance). Must be same length as x.
    xlab : str, optional
        Label for x-axis. Default is "Time (Subgroups)".
    ylab : str, optional
        Label for y-axis. Default is "Standard Deviation".
    
    Returns
    -------
    ggplot
        A control chart visualization
    
    Examples
    --------
    >>> import pandas as pd
    >>> water = pd.read_csv("workshops/onsen.csv")
    >>> ggs(x=water['time'], y=water['temp'], xlab="Time (Subgroups)", ylab="Standard Deviation")
    """
    # Make data.frame of input vectors
    data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
    
    # Get subgroup statistics, with UCL and LCL for standard deviation
    stat_s = limits_s(x=data['x'], y=data['y'])
    
    # Get overall (total) statistics
    stat_t = get_stat_t(x=data['x'], y=data['y'])
    
    # Get labels
    labels = pd.DataFrame({
        'x': [stat_s['x'].max(), stat_s['x'].max(), stat_s['x'].max()],
        'type': ['sbar', 'upper', 'lower'],
        'name': ['sbar', '+3 s', '-3 s'],
        'value': [stat_s['sbar'].iloc[0], stat_s['upper'].max(), stat_s['lower'].min()]
    })
    labels['value'] = labels['value'].round(2)
    labels['text'] = labels['name'] + " = " + labels['value'].astype(str)
    
    # Make visual
    gg = (ggplot() +
          geom_hline(data=stat_t, mapping=aes(yintercept='sbar'), color="lightgrey") +
          geom_ribbon(data=stat_s, mapping=aes(x='x', ymin='lower', ymax='upper'),
                     fill="steelblue", alpha=0.2) +
          geom_line(data=stat_s, mapping=aes(x='x', y='s'), size=1) +
          geom_point(data=stat_s, mapping=aes(x='x', y='s'), size=5) +
          geom_label(data=labels, mapping=aes(x='x', y='value', label='text'),
                    ha='right') +  # horizontally justify labels
          labs(x=xlab, y=ylab, subtitle="Standard Deviation Chart"))
    
    return gg


def ggr(x, y, xlab="Time (Subgroups)", ylab="Range"):
    """
    Range Chart with ggplot
    
    Creates an R (range) control chart showing subgroup ranges over time with
    control limits and center line.
    
    Parameters
    ----------
    x : array-like
        Vector of subgroup values (usually time). Must be same length as y.
    y : array-like
        Vector of metric values (e.g., performance). Must be same length as x.
    xlab : str, optional
        Label for x-axis. Default is "Time (Subgroups)".
    ylab : str, optional
        Label for y-axis. Default is "Range".
    
    Returns
    -------
    ggplot
        A control chart visualization
    
    Examples
    --------
    >>> import pandas as pd
    >>> water = pd.read_csv("workshops/onsen.csv")
    >>> ggr(x=water['time'], y=water['temp'], xlab="Time (Subgroups)", ylab="Range")
    """
    # Make data.frame of input vectors
    data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
    
    # Get subgroup statistics, with UCL and LCL for range
    stat_s = limits_r(x=data['x'], y=data['y'])
    
    # Get overall (total) statistics
    stat_t = get_stat_t(x=data['x'], y=data['y'])
    
    # Get labels
    labels = pd.DataFrame({
        'x': [stat_s['x'].max(), stat_s['x'].max(), stat_s['x'].max()],
        'type': ['rbar', 'upper', 'lower'],
        'name': ['rbar', '+3 s', '-3 s'],
        'value': [stat_s['rbar'].iloc[0], stat_s['upper'].max(), stat_s['lower'].min()]
    })
    labels['value'] = labels['value'].round(2)
    labels['text'] = labels['name'] + " = " + labels['value'].astype(str)
    
    # Make visual
    gg = (ggplot() +
          geom_hline(data=stat_t, mapping=aes(yintercept='rbar'), color="lightgrey") +
          geom_ribbon(data=stat_s, mapping=aes(x='x', ymin='lower', ymax='upper'),
                     fill="steelblue", alpha=0.2) +
          geom_line(data=stat_s, mapping=aes(x='x', y='r'), size=1) +
          geom_point(data=stat_s, mapping=aes(x='x', y='r'), size=5) +
          geom_label(data=labels, mapping=aes(x='x', y='value', label='text'),
                    ha='right') +  # horizontally justify labels
          labs(x=xlab, y=ylab, subtitle="Range Chart"))
    
    return gg


def ggmr(x, y, xlab="Time (Subgroups)", ylab="Moving Range"):
    """
    Moving Range Chart with ggplot
    
    Creates a moving range control chart for individual measurements (n=1).
    
    Parameters
    ----------
    x : array-like
        Vector of subgroup values (usually time). Must be same length as y.
    y : array-like
        Vector of metric values (e.g., performance). Must be same length as x.
    xlab : str, optional
        Label for x-axis. Default is "Time (Subgroups)".
    ylab : str, optional
        Label for y-axis. Default is "Moving Range".
    
    Returns
    -------
    ggplot
        A control chart visualization
    
    Examples
    --------
    >>> import pandas as pd
    >>> water = pd.read_csv("workshops/onsen.csv")
    >>> # Suppose we sample just the first out of each our months
    >>> indiv = water[water['id'].isin([1, 21, 41, 61, 81, 101, 121, 141])]
    >>> ggmr(x=indiv['time'], y=indiv['temp'], xlab="Time (Subgroups)", ylab="Moving Range")
    """
    # Make data.frame of input vectors
    data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
    
    # Obtain moving range
    data2 = pd.DataFrame({
        'x': data['x'].iloc[1:].values,
        'mr': np.abs(np.diff(data['y'].values))
    })
    
    # Get subgroup statistics, with UCL and LCL for moving range
    stat_s = limits_mr(x=data['x'], y=data['y'])
    
    # Get labels
    labels = pd.DataFrame({
        'x': [stat_s['x'].max(), stat_s['x'].max(), stat_s['x'].max()],
        'type': ['mrbar', 'upper', 'lower'],
        'name': ['mrbar', '+3 s', '-3 s'],
        'value': [stat_s['mrbar'].iloc[0], stat_s['upper'].max(), stat_s['lower'].min()]
    })
    labels['value'] = labels['value'].round(2)
    labels['text'] = labels['name'] + " = " + labels['value'].astype(str)
    
    # Get one value for grand moving range
    stat_t = pd.DataFrame({'mrbar': [stat_s['mrbar'].iloc[0]]})
    
    # Make visual
    gg = (ggplot() +
          geom_hline(data=stat_t, mapping=aes(yintercept='mrbar'), color="lightgrey") +
          geom_ribbon(data=stat_s, mapping=aes(x='x', ymin='lower', ymax='upper'),
                     fill="steelblue", alpha=0.2) +
          geom_line(data=data2, mapping=aes(x='x', y='mr'), size=1) +
          geom_point(data=stat_s, mapping=aes(x='x', y='mr'), size=5) +
          geom_label(data=labels, mapping=aes(x='x', y='value', label='text'),
                    ha='right') +  # horizontally justify labels
          labs(x=xlab, y=ylab, subtitle="Moving Range Chart"))
    
    return gg


def ggp(t, x, n, xlab="Time (Subgroup)", ylab="Fraction Defective"):
    """
    Fraction Defective (p) Chart in ggplot
    
    Creates a p-chart showing the fraction of defective items over time with
    control limits based on binomial distribution assumptions.
    
    Parameters
    ----------
    t : array-like
        Vector of time/subgroup values
    x : array-like
        Vector of number of defective items in each subgroup
    n : array-like
        Vector of sample sizes for each subgroup
    xlab : str, optional
        Label for x-axis. Default is "Time (Subgroup)".
    ylab : str, optional
        Label for y-axis. Default is "Fraction Defective".
    
    Returns
    -------
    ggplot
        A control chart visualization
    
    Examples
    --------
    >>> import pandas as pd
    >>> inventory = pd.read_csv("workshops/inventory.csv")
    >>> ggp(t=inventory['t'], x=inventory['x'], n=inventory['n'],
    ...     xlab="Time (Subgroup)", ylab="Fraction Defective")
    """
    # Make a data.frame
    data = pd.DataFrame({'t': pd.Series(t), 'x': pd.Series(x), 'n': pd.Series(n)})
    
    # Get subgroup statistics
    stat_s = data.copy()
    stat_s['p'] = stat_s['x'] / stat_s['n']
    stat_s['mu'] = stat_s['n'] * stat_s['p']
    stat_s['sigma'] = np.sqrt(stat_s['n'] * stat_s['p'] * (1 - stat_s['p']))
    
    # Add total traits here
    stat_s['xsum'] = stat_s['x'].sum()
    stat_s['nsum'] = stat_s['n'].sum()
    # calculate centerline
    stat_s['pbar'] = stat_s['xsum'] / stat_s['nsum']
    # calculate standard deviation with binomial assumptions
    stat_s['se'] = np.sqrt(stat_s['pbar'] * (1 - stat_s['pbar']) / stat_s['n'])
    # Calculate 3-sigma control limits
    stat_s['lower'] = stat_s['pbar'] - 3 * stat_s['se']
    stat_s['upper'] = stat_s['pbar'] + 3 * stat_s['se']
    # Clip the lower estimate at zero or higher
    stat_s.loc[stat_s['lower'] < 0, 'lower'] = 0
    
    # Visualize it
    gg = (ggplot() +
          # Draw upper and lower control limits
          geom_ribbon(data=stat_s, mapping=aes(x='t', ymin='lower', ymax='upper'),
                     fill="steelblue", alpha=0.2) +
          # Draw the grand pbar line
          geom_hline(data=stat_s, mapping=aes(yintercept='pbar'),
                    size=1.5, color="darkgrey") +
          # Draw probability over time
          geom_line(data=stat_s, mapping=aes(x='t', y='p')) +
          # Draw probability over time with points
          geom_point(data=stat_s, mapping=aes(x='t', y='p')) +
          # Add labels
          labs(x=xlab, y=ylab, subtitle="Fraction Defective (p) Chart"))
    
    return gg


def ggnp(t, x, n, xlab="Time (Subgroups)", ylab="Number of Defectives (np)"):
    """
    Number of Defects (np) Chart in ggplot
    
    Creates an np-chart showing the number of defective items over time with
    control limits based on binomial distribution assumptions.
    
    Parameters
    ----------
    t : array-like
        Vector of time/subgroup values
    x : array-like
        Vector of number of defective items in each subgroup
    n : array-like
        Vector of sample sizes for each subgroup
    xlab : str, optional
        Label for x-axis. Default is "Time (Subgroups)".
    ylab : str, optional
        Label for y-axis. Default is "Number of Defectives (np)".
    
    Returns
    -------
    ggplot
        A control chart visualization
    
    Examples
    --------
    >>> import pandas as pd
    >>> inv = pd.read_csv("workshops/inventory.csv")
    >>> ggnp(t=inv['t'], x=inv['x'], n=inv['n'],
    ...      xlab="Time (Subgroups)", ylab="Number of Defectives")
    """
    # Make a data.frame
    data = pd.DataFrame({'t': pd.Series(t), 'x': pd.Series(x), 'n': pd.Series(n)})
    
    # Get subgroup statistics
    stat_s = data.copy()
    stat_s['p'] = stat_s['x'] / stat_s['n']
    stat_s['np'] = stat_s['n'] * stat_s['p']
    
    # Add total traits here
    stat_s['xsum'] = stat_s['x'].sum()
    stat_s['nsum'] = stat_s['n'].sum()
    # calculate centerline
    stat_s['npbar'] = (stat_s['n'] * stat_s['p']).sum() / len(stat_s)
    stat_s['pbar'] = (stat_s['n'] * stat_s['p']).sum() / stat_s['n'].sum()
    # calculate standard error
    stat_s['se'] = np.sqrt(stat_s['npbar'] * (1 - stat_s['pbar']))
    # Calculate 3-sigma control limits
    stat_s['lower'] = stat_s['npbar'] - 3 * stat_s['se']
    stat_s['upper'] = stat_s['npbar'] + 3 * stat_s['se']
    # Clip the lower estimate at zero or higher
    stat_s.loc[stat_s['lower'] < 0, 'lower'] = 0
    
    labels = pd.DataFrame({
        't': [stat_s['t'].max(), stat_s['t'].max(), stat_s['t'].max()],
        'type': ['npbar', 'upper', 'lower'],
        'name': ['npbar', '+3 s', '-3 s'],
        'value': [stat_s['npbar'].iloc[0], stat_s['upper'].max(), stat_s['lower'].min()]
    })
    labels['value'] = labels['value'].round(2)
    labels['text'] = labels['name'] + " = " + labels['value'].astype(str)
    
    # Visualize it
    gg = (ggplot() +
          # Draw upper and lower control limits
          geom_ribbon(data=stat_s, mapping=aes(x='t', ymin='lower', ymax='upper'),
                     fill="steelblue", alpha=0.2) +
          # Draw the grand npbar line
          geom_hline(data=stat_s, mapping=aes(yintercept='npbar'),
                    size=1.5, color="darkgrey") +
          # Draw np over time
          geom_line(data=stat_s, mapping=aes(x='t', y='np')) +
          # Draw np over time with points
          geom_point(data=stat_s, mapping=aes(x='t', y='np')) +
          # Add text
          geom_label(data=labels, mapping=aes(x='t', y='value', label='text'), ha='right') +
          # Add labels
          labs(x=xlab, y=ylab, subtitle="Mean Defective (np) Chart"))
    
    return gg


def ggu(t, x, xlab="Time (Subgroups)", ylab="Number of Defects (u)"):
    """
    Defects per Product (u) Chart in ggplot
    
    Creates a u-chart showing the number of defects per unit over time with
    control limits based on Poisson distribution assumptions.
    
    Parameters
    ----------
    t : array-like
        Vector of time/subgroup values
    x : array-like
        Vector of number of defects observed in each subgroup
    xlab : str, optional
        Label for x-axis. Default is "Time (Subgroups)".
    ylab : str, optional
        Label for y-axis. Default is "Number of Defects (u)".
    
    Returns
    -------
    ggplot
        A control chart visualization
    
    Examples
    --------
    >>> import pandas as pd
    >>> acc = pd.read_csv("workshops/accidents.csv")
    >>> ggu(t=acc['t'], x=acc['x'], xlab="Time", ylab="Number of Defects")
    """
    data = pd.DataFrame({'t': pd.Series(t), 'x': pd.Series(x)})
    
    stat_s = (data.groupby('t')
              .agg({
                  'x': ['sum', 'count']
              })
              .reset_index())
    stat_s.columns = ['t', 'u', 'nw']
    
    # Calculate centerline
    stat_s['ubar'] = stat_s['u'].sum() / stat_s['nw'].sum()
    stat_s['se'] = np.sqrt(stat_s['ubar'] / stat_s['nw'])
    stat_s['lower'] = stat_s['ubar'] - 3 * stat_s['se']
    stat_s['upper'] = stat_s['ubar'] + 3 * stat_s['se']
    # Curb lower to be no lower than 0
    stat_s.loc[stat_s['lower'] < 0, 'lower'] = 0
    
    labels = pd.DataFrame({
        't': [stat_s['t'].max(), stat_s['t'].max(), stat_s['t'].max()],
        'type': ['ubar', 'upper', 'lower'],
        'name': ['ubar', '+3 s', '-3 s'],
        'value': [stat_s['ubar'].iloc[0], stat_s['upper'].max(), stat_s['lower'].min()]
    })
    labels['value'] = labels['value'].round(2)
    labels['text'] = labels['name'] + " = " + labels['value'].astype(str)
    
    # Visualize
    gg = (ggplot() +
          # Draw upper and lower control limits
          geom_ribbon(data=stat_s, mapping=aes(x='t', ymin='lower', ymax='upper'),
                     fill="steelblue", alpha=0.2) +
          # Draw the grand ubar line
          geom_hline(data=stat_s, mapping=aes(yintercept='ubar'),
                    size=1.5, color="darkgrey") +
          # Draw u over time
          geom_line(data=stat_s, mapping=aes(x='t', y='u')) +
          # Draw u over time with points
          geom_point(data=stat_s, mapping=aes(x='t', y='u')) +
          # Add text
          geom_label(data=labels, mapping=aes(x='t', y='value', label='text'), ha='right') +
          # Add labels
          labs(x=xlab, y=ylab, subtitle="Number of Defects (u) Chart"))
    
    return gg


# Keep ggavg for backward compatibility (alias for ggxbar)
def ggavg(x, y, xlab="Time (Subgroups)", ylab="Average"):
    """
    Average Control Chart with ggplot (alias for ggxbar)
    
    This function is kept for backward compatibility. It calls ggxbar().
    """
    return ggxbar(x, y, xlab=xlab, ylab=ylab)


def cp(sigma_s, upper, lower):
    """
    Capability Index (for centered, stable processes)
    
    Calculates the process capability index Cp, which measures the potential capability 
    of a centered, stable process. Cp compares the process spread (6*sigma_s) to the 
    specification width.
    
    Parameters
    ----------
    sigma_s : float
        Within-subgroup standard deviation (short-term variation)
    upper : float
        Upper specification limit
    lower : float
        Lower specification limit
    
    Returns
    -------
    float
        A single numeric value representing the Cp index. Values > 1 indicate the 
        process spread is smaller than the specification width.
    
    Examples
    --------
    >>> # Calculate Cp for a process with sigma_s = 2, USL = 100, LSL = 80
    >>> cp(sigma_s=2, upper=100, lower=80)
    >>> # Cp = (100 - 80) / (6 * 2) = 20 / 12 = 1.67
    """
    return abs(upper - lower) / (6*sigma_s)


def pp(sigma_t, upper, lower):
    """
    Process Performance Index (for centered, unstable processes)
    
    Calculates the process performance index Pp, which measures the potential performance 
    of a centered process using total variation. Pp compares the process spread (6*sigma_t) 
    to the specification width.
    
    Parameters
    ----------
    sigma_t : float
        Total standard deviation (long-term variation)
    upper : float
        Upper specification limit
    lower : float
        Lower specification limit
    
    Returns
    -------
    float
        A single numeric value representing the Pp index. Values > 1 indicate the 
        process spread is smaller than the specification width.
    
    Examples
    --------
    >>> # Calculate Pp for a process with sigma_t = 2.5, USL = 100, LSL = 80
    >>> pp(sigma_t=2.5, upper=100, lower=80)
    >>> # Pp = (100 - 80) / (6 * 2.5) = 20 / 15 = 1.33
    """
    return abs(upper - lower) / (6*sigma_t)


def cpk(mu, sigma_s, lower=None, upper=None):
    """
    Capability Index (for uncentered, stable processes)
    
    Calculates the process capability index Cpk, which measures the actual capability 
    of a stable process that may not be centered. Cpk considers both the process mean 
    location and within-subgroup variation.
    
    Parameters
    ----------
    mu : float
        Process mean
    sigma_s : float
        Within-subgroup standard deviation (short-term variation)
    lower : float, optional
        Lower specification limit. If None, only upper limit is used.
    upper : float, optional
        Upper specification limit. If None, only lower limit is used.
    
    Returns
    -------
    float
        A single numeric value representing the Cpk index. Returns the minimum of the 
        upper and lower capability ratios if both limits are provided, otherwise returns 
        the appropriate one-sided ratio. Values > 1 indicate the process is capable.
    
    Examples
    --------
    >>> # Calculate Cpk with both limits
    >>> cpk(mu=90, sigma_s=2, lower=80, upper=100)
    >>> 
    >>> # Calculate Cpk with only upper limit
    >>> cpk(mu=90, sigma_s=2, upper=100)
    >>> 
    >>> # Calculate Cpk with only lower limit
    >>> cpk(mu=90, sigma_s=2, lower=80)
    """
    a = None
    b = None
    if lower is not None:
        a = abs(mu - lower) / (3*sigma_s)
    if upper is not None:
        b = abs(upper - mu) / (3*sigma_s)
    if (lower is not None) and (upper is not None):
        return min(a, b)
    return a if upper is None else b


def ppk(mu, sigma_t, lower=None, upper=None):
    """
    Process Performance Index (for uncentered, unstable processes)
    
    Calculates the process performance index Ppk, which measures the actual performance 
    of a process that may not be centered or stable. Ppk considers both the process mean 
    location and total variation.
    
    Parameters
    ----------
    mu : float
        Process mean
    sigma_t : float
        Total standard deviation (long-term variation)
    lower : float, optional
        Lower specification limit. If None, only upper limit is used.
    upper : float, optional
        Upper specification limit. If None, only lower limit is used.
    
    Returns
    -------
    float
        A single numeric value representing the Ppk index. Returns the minimum of the 
        upper and lower performance ratios if both limits are provided, otherwise returns 
        the appropriate one-sided ratio. Values > 1 indicate the process is performing 
        within specifications.
    
    Examples
    --------
    >>> # Calculate Ppk with both limits
    >>> ppk(mu=90, sigma_t=2.5, lower=80, upper=100)
    >>> 
    >>> # Calculate Ppk with only upper limit
    >>> ppk(mu=90, sigma_t=2.5, upper=100)
    >>> 
    >>> # Calculate Ppk with only lower limit
    >>> ppk(mu=90, sigma_t=2.5, lower=80)
    """
    a = None
    b = None
    if lower is not None:
        a = abs(mu - lower) / (3*sigma_t)
    if upper is not None:
        b = abs(upper - mu) / (3*sigma_t)
    if (lower is not None) and (upper is not None):
        return min(a, b)
    return a if upper is None else b


def get_index(x, y, index="cp", upper=None, lower=None,
              bootstrap_reps=1000, ci_level=0.95,
              by_subgroup=True):
    """
    Bootstrap Process Capability/Performance Index with Confidence Intervals
    
    Calculates a process capability or performance index (cp, pp, cpk, ppk) and bootstraps 
    it to provide confidence intervals. Supports both subgroup-level and individual-level 
    resampling.
    
    Parameters
    ----------
    x : array-like
        Vector of subgroup values (usually time). Must be same length as y.
    y : array-like
        Vector of metric values (e.g., performance). Must be same length as x.
    index : str, optional
        One of "cp", "pp", "cpk", "ppk". Default is "cp".
    upper : float, optional
        Upper specification limit. Required for cp/pp, optional for cpk/ppk.
    lower : float, optional
        Lower specification limit. Required for cp/pp, optional for cpk/ppk.
    bootstrap_reps : int, optional
        Number of bootstrap replicates. Default is 1000. A warning is issued if < 500.
    ci_level : float, optional
        Confidence level for intervals. Default is 0.95.
    by_subgroup : bool, optional
        If True, resample subgroups with replacement (preserves subgroup structure). 
        If False, resample individual observations. Default is True.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with columns: term, estimate, se, lower, upper
    
    Examples
    --------
    >>> import pandas as pd
    >>> water = pd.read_csv("workshops/onsen.csv")
    >>> 
    >>> # Bootstrap Cp index with subgroup resampling
    >>> get_index(x=water['time'], y=water['temp'], index="cp", 
    ...           upper=80, lower=42, bootstrap_reps=1000)
    >>> 
    >>> # Bootstrap Cpk index with individual resampling
    >>> get_index(x=water['time'], y=water['temp'], index="cpk", 
    ...           upper=80, lower=42, by_subgroup=False)
    """
    import warnings
    
    # Validate index
    if index not in ["cp", "pp", "cpk", "ppk"]:
        raise ValueError("index must be one of: cp, pp, cpk, ppk")
    
    # Validate specification limits
    if index in ["cp", "pp"]:
        if upper is None or lower is None:
            raise ValueError("upper and lower specification limits are required for cp and pp")
    else:
        if upper is None and lower is None:
            raise ValueError("at least one of upper or lower specification limit is required for cpk and ppk")
    
    # Warn if bootstrap_reps < 500
    if bootstrap_reps < 500:
        warnings.warn("bootstrap_reps < 500 may result in unreliable confidence intervals", 
                     UserWarning)
    
    # Make a data.frame
    data = pd.DataFrame({'x': pd.Series(x), 'y': pd.Series(y)})
    
    # Calculate observed index
    if index == "cp":
        stat_s = get_stat_s(x=x, y=y)
        sigma_s = stat_s['sigma_s'].iloc[0]
        estimate = cp(sigma_s=sigma_s, upper=upper, lower=lower)
    elif index == "pp":
        stat_t = get_stat_t(x=x, y=y)
        sigma_t = stat_t['sigma_t'].iloc[0]
        estimate = pp(sigma_t=sigma_t, upper=upper, lower=lower)
    elif index == "cpk":
        stat_s = get_stat_s(x=x, y=y)
        stat_t = get_stat_t(x=x, y=y)
        mu = stat_t['xbbar'].iloc[0]
        sigma_s = stat_s['sigma_s'].iloc[0]
        estimate = cpk(mu=mu, sigma_s=sigma_s, 
                      upper=upper, lower=lower)
    elif index == "ppk":
        stat_t = get_stat_t(x=x, y=y)
        mu = stat_t['xbbar'].iloc[0]
        sigma_t = stat_t['sigma_t'].iloc[0]
        estimate = ppk(mu=mu, sigma_t=sigma_t,
                      upper=upper, lower=lower)
    
    # Bootstrap loop
    boot_values = []
    
    for i in range(bootstrap_reps):
        if by_subgroup:
            # Resample subgroups with replacement
            subgroups = data['x'].unique()
            sampled_subgroups = np.random.choice(subgroups, size=len(subgroups), replace=True)
            
            # Create bootstrap sample by combining sampled subgroups
            boot_data_list = []
            for sg in sampled_subgroups:
                sg_data = data[data['x'] == sg].copy()
                boot_data_list.append(sg_data)
            boot_data = pd.concat(boot_data_list, ignore_index=True)
        else:
            # Resample individual observations with replacement
            boot_data = data.sample(n=len(data), replace=True).reset_index(drop=True)
        
        # Calculate index for bootstrap sample
        if index == "cp":
            boot_stat_s = get_stat_s(x=boot_data['x'], y=boot_data['y'])
            boot_sigma_s = boot_stat_s['sigma_s'].iloc[0]
            boot_values.append(cp(sigma_s=boot_sigma_s, upper=upper, lower=lower))
        elif index == "pp":
            boot_stat_t = get_stat_t(x=boot_data['x'], y=boot_data['y'])
            boot_sigma_t = boot_stat_t['sigma_t'].iloc[0]
            boot_values.append(pp(sigma_t=boot_sigma_t, upper=upper, lower=lower))
        elif index == "cpk":
            boot_stat_s = get_stat_s(x=boot_data['x'], y=boot_data['y'])
            boot_stat_t = get_stat_t(x=boot_data['x'], y=boot_data['y'])
            boot_mu = boot_stat_t['xbbar'].iloc[0]
            boot_sigma_s = boot_stat_s['sigma_s'].iloc[0]
            boot_values.append(cpk(mu=boot_mu, sigma_s=boot_sigma_s,
                                  upper=upper, lower=lower))
        elif index == "ppk":
            boot_stat_t = get_stat_t(x=boot_data['x'], y=boot_data['y'])
            boot_mu = boot_stat_t['xbbar'].iloc[0]
            boot_sigma_t = boot_stat_t['sigma_t'].iloc[0]
            boot_values.append(ppk(mu=boot_mu, sigma_t=boot_sigma_t,
                                  upper=upper, lower=lower))
    
    # Calculate standard error and confidence intervals
    boot_values = np.array(boot_values)
    se = boot_values.std()
    alpha = 1 - ci_level
    ci_bounds = np.quantile(boot_values, [alpha/2, 1 - alpha/2])
    
    # Return tidy DataFrame
    output = pd.DataFrame({
        'term': [index],
        'estimate': [estimate],
        'se': [se],
        'lower': [ci_bounds[0]],
        'upper': [ci_bounds[1]]
    })
    
    return output
    
