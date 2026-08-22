# What this file is ----------------------------------------------------------
#
# One helper for grouping times-to-failure into bins you can actually run a
# chi-squared test on. It bins the data at a fixed width, then merges the
# thin bins in the tail together until every bin holds at least 5
# observations.
#
# Load it, from the top of the project folder:
#   import sys
#   sys.path.append("functions")
#   from functions_crosstab import crosstab
#
# Then try:
#   x = [1, 5, 20, 45, 90, 130, 260, 410, 520, 700,
#        15, 33, 88, 140, 255, 390, 505, 660, 12, 44]
#   crosstab(x = x, binsize = 100, cutoff = 450)
#
# You never need to edit anything below.
#

# functions_crosstab.py
# Script of Python functions for crosstabulating data into intervals.

"""
Functions for Crosstabulating Data

This module provides functions for creating crosstabulations of data into intervals,
with support for reaggregating bins after a cutoff point.
"""

import pandas as pd
import numpy as np


def crosstab(x, binsize=100, cutoff=np.inf):
    """
    Crosstabulate Data into intervals where r >= 5
    
    Creates a crosstabulation of times to failure (or other numeric data) into
    intervals of a specified size, with optional reaggregation after a cutoff point.
    
    Parameters
    ----------
    x : array-like
        A vector of times to failure (or other numeric values)
    binsize : numeric, optional
        A single integer describing the size of each interval/bin. Default is 100.
    cutoff : numeric, optional
        A single number describing the cutoff after which to reaggregate the bins.
        Default is np.inf (no cutoff).
    
    Returns
    -------
    pd.DataFrame
        DataFrame with columns: bin, interval, midpoint, r_obs
        - bin: Bin number (1-based)
        - interval: Interval label (e.g., "[0, 100)")
        - midpoint: Midpoint of the interval
        - r_obs: Number of observations in the interval
    
    Examples
    --------
    >>> # Product Times to Failure
    >>> x = [1,2,2,3,4,5,7,8,9,10,
    ...      11,13,15,16,17,17,18,18,18,20,
    ...      20,21,21,24,27,29,30,37,40,40,
    ...      40,41,46,47,48,52,54,54,55,55,
    ...      64,65,65,65,67,76,76,79,80,80,
    ...      82,86,87,89,94,96,100,101,102,104,
    ...      105,109,109,120,123,141,150,156,156,161,
    ...      164,167,170,178,181,191,193,206,211,212,
    ...      214,236,238,240,265,304,317,328,355,363,
    ...      365,369,389,404,427,435,500,522,547,889]
    >>> crosstab(x, binsize=100, cutoff=450)
    """
    # Testing Values
    # Product Times to Failure
    # x = [1,2,2,3,4,5,7,8,9,10,
    #           11,13,15,16,17,17,18,18,18,20,
    #           20,21,21,24,27,29,30,37,40,40,
    #           40,41,46,47,48,52,54,54, 55,55,
    #           64,65,65,65,67,76,76,79,80,80,
    #           82,86,87,89,94,96,100,101,102,104,
    #           105,109,109,120,123,141,150,156,156,161,
    #           164,167,170,178,181,191,193,206,211,212,
    #           214,236,238,240,265,304,317,328,355,363,
    #           365,369,389,404,427,435,500,522,547,889]
    # binsize = 100
    # cutoff = 450
    
    # Initial crosstabulation
    data = pd.DataFrame({'t': pd.Series(x)})
    
    # R's cut_interval with length parameter creates intervals of equal width (binsize)
    # starting from 0, with right=TRUE (intervals are (a, b] except first is [a, b])
    min_val = data['t'].min()
    max_val = data['t'].max()
    
    # Calculate bin number for each value
    # With right=TRUE: values 0-100 go in bin 1 [0, 100], values 101-200 go in bin 2 (100, 200], etc.
    # Formula: for t > 0, bin = floor((t - 1) / binsize) + 1; for t = 0, bin = 1
    def get_bin(t_val):
        if t_val == 0:
            return 1
        # For t > 0: values 1-100 -> bin 1, values 101-200 -> bin 2, etc.
        return int(np.floor((t_val - 1) / binsize)) + 1
    
    data['bin'] = data['t'].apply(get_bin)
    
    # Group by bin and count observations
    data = (data.groupby('bin', as_index=False)
            .agg(r_obs=('t', 'count')))
    
    # Calculate lower, upper, and midpoint based on bin number
    # R code uses: lower = (bin - 1) * binsize, upper = bin * binsize
    data['lower'] = (data['bin'] - 1) * binsize
    data['upper'] = data['bin'] * binsize
    data['midpoint'] = (data['lower'] + data['upper']) / 2
    
    # Create interval labels to match R's format
    # R creates intervals like [0,100], (100,200], (200,300], etc.
    def create_interval_label(row):
        lower_val = int(row['lower'])
        upper_val = int(row['upper'])
        if row['bin'] == 1:
            return f"[{lower_val},{upper_val}]"
        else:
            return f"({lower_val},{upper_val}]"
    
    data['interval'] = data.apply(create_interval_label, axis=1)
    
    # Sort by bin to ensure correct order, then create categorical
    data = data.sort_values('bin').reset_index(drop=True)
    # Convert interval to string explicitly to avoid any Interval object issues
    data['interval'] = data['interval'].astype(str)
    data['interval'] = pd.Categorical(data['interval'], categories=data['interval'].tolist(), ordered=True)
    
    # Find all rows past the time interval cutoff
    end_rows = data[data['midpoint'] >= cutoff]
    
    # If there are any rows past the time interval cutoff, reaggregate
    if len(end_rows) > 0:
        # Get the first row that meets the cutoff
        end = end_rows.iloc[0]
        
        # Revise the interval name and bin id
        data2 = data.copy()
        # Assign all rows with midpoint >= cutoff to the same interval and bin as the first matching row
        mask = data2['midpoint'] >= cutoff
        data2.loc[mask, 'interval'] = end['interval']
        data2.loc[mask, 'bin'] = end['bin']
        
        # Get the unique levels out - need to preserve order
        # Get unique intervals in their original order
        unique_intervals = []
        seen = set()
        for interval in data2['interval']:
            if interval not in seen:
                unique_intervals.append(interval)
                seen.add(interval)
        
        # Update the interval categorical levels to preserve order
        data2['interval'] = pd.Categorical(data2['interval'], categories=unique_intervals, ordered=True)
        
        # Aggregate to the new interval levels
        data4 = (data2.groupby(['bin', 'interval'], observed=True)
                 .agg(r_obs=('r_obs', 'sum'))
                 .reset_index())
        
        # Recalculate the midpoints based on bin numbers
        data5 = data4.copy()
        data5['lower'] = (data5['bin'] - 1) * binsize
        data5['upper'] = data5['bin'] * binsize
        data5['midpoint'] = (data5['lower'] + data5['upper']) / 2
        
        # Select final columns
        output = data5[['bin', 'interval', 'midpoint', 'r_obs']].copy()
        
    else:
        # If there are no rows past the time interval cutoff, just output the result
        output = data[['bin', 'interval', 'midpoint', 'r_obs']].copy()
    
    return output

