# What this file is ----------------------------------------------------------
#
# Helpers for two-level factorial experiments -- the kind where you change two
# or three things at once and want to know how much each one mattered, and
# whether they work differently in combination.
#
#   effects_factorial()  every main effect, two-way and three-way interaction,
#                        with its standard error and confidence interval
#   se_factorial()       the standard error of each effect
#   dbar_oneway(), dbar_twoway(), dbar_threeway()   one effect at a time
#
# Every factor must have two levels. Recode a factor with more levels as a
# yes/no question first, e.g. lattes["oat"] = lattes["milk"] == "oat".
# For messy, unbalanced data (say, some runs were lost), use a linear model instead.
#
# Load it, from the top of the project folder:
#   import sys
#   sys.path.append("functions")
#   from functions_factorial import effects_factorial, se_factorial
#
# Then try:
#   import pandas as pd
#   lattes = pd.read_csv("workshops/lattes.csv")
#   effects_factorial(formula = "tastiness ~ machine + syrup + art", data = lattes)
#
# You never need to edit anything below.
#

# functions_factorial.py
# Script of Python functions for estimating effects and their standard errors in two-level factorial experiments.

from itertools import combinations

import numpy as np
import pandas as pd
from scipy import stats


def factorial_frame(formula, data):
    """
    Split a formula like "y ~ a + b" or "y ~ a * b" into a data frame with the
    response renamed to y, plus the list of factor names.
    """
    response, rhs = [part.strip() for part in formula.split("~")]
    xvars = [v.strip() for v in rhs.replace("*", "+").split("+")]
    frame = data[[response] + xvars].rename(columns={response: "y"})
    return frame, xvars


def se_factorial(formula, data, table=False):
    """
    Standard Error of Each Factorial Effect

    Pools the variance over every treatment combination of the factors,
    s^2 = sum(v_i * s_i^2) / sum(v_i) with v_i = n_i - 1, then gives each effect
    the standard error s * sqrt(sum(c_k^2 / n_k)), summing over the combinations
    k of the factors in that effect (n_k runs each; c_k = +/-1 for a main effect,
    +/-1/2 for a two-way, +/-1/4 for a three-way). In a balanced design every
    effect gets the same standard error, 2s/sqrt(N). Factors must have two
    levels; recode others as a yes/no question. For messy, unbalanced data, use
    a linear model instead.

    Parameters
    ----------
    formula : str
        The response and the factors, e.g. "y ~ machine + syrup + art".
    data : pd.DataFrame
        A data frame containing those columns.
    table : bool
        False (default) returns the standard error: one number when every effect
        shares it, otherwise a Series with one per effect. True returns a table
        with each term, its runs at + and -, its se, the pooled variance s2, its
        degrees of freedom df, and t_crit for a 95% interval.

    Examples
    --------
    >>> lattes = pd.read_csv("workshops/lattes.csv")
    >>> se_factorial("tastiness ~ machine + syrup + art", lattes)
    >>> lattes["oat"] = lattes["milk"] == "oat"
    >>> se_factorial("tastiness ~ machine + oat + syrup + art", lattes, table=True)
    """
    frame, xvars = factorial_frame(formula, data)
    # Every factor must have exactly two levels
    n_levels = frame[xvars].nunique()
    if (n_levels != 2).any():
        raise ValueError("se_factorial(): " + ", ".join(n_levels[n_levels != 2].index) +
                         " does not have exactly two levels. Recode it as a yes/no question, "
                         "e.g. lattes['oat'] = lattes['milk'] == 'oat'.")
    # Code each factor -1 (first level) and +1 (second level)
    coded = frame.assign(**{x: np.where(frame[x] == sorted(frame[x].unique())[1], 1, -1) for x in xvars})

    # Pooled variance over the treatment combinations of all the factors
    cells = coded.groupby(xvars)["y"].agg(s2="var", n="count").reset_index()
    cells["v"] = cells["n"] - 1
    df = int(cells["v"].sum())
    if df == 0:
        raise ValueError("se_factorial(): no treatment combination has 2 or more runs, so there is no "
                         "pooled variance; judge its effects with a normal plot instead.")
    s2 = (cells["v"] * cells["s2"].fillna(0)).sum() / df

    # Every main effect, two-way and three-way interaction among the factors
    terms = [list(t) for m in range(1, min(3, len(xvars)) + 1) for t in combinations(xvars, m)]

    # SE of each effect: s * sqrt(sum of c^2 / n) over the combinations of its factors
    def se_term(t):
        n_k = coded.groupby(t).size()
        c_k = 1 / 2 ** (len(t) - 1)
        return np.sqrt(s2) * np.sqrt((c_k ** 2 / n_k).sum())

    output = pd.DataFrame({
        "term": [":".join(t) for t in terms],
        "n_plus": [int((coded[t].prod(axis=1) == 1).sum()) for t in terms],
        "n_minus": [int((coded[t].prod(axis=1) == -1).sum()) for t in terms],
        "se": [se_term(t) for t in terms]})
    output = output.assign(s2=s2, df=df, t_crit=stats.t.ppf(0.975, df))

    if table:
        return output
    # Balanced: every effect has the same SE, so return that one number
    if np.ptp(output["se"]) < 1e-10:
        return float(output["se"].iloc[0])
    print("se_factorial(): effects have different standard errors; effects_factorial() lists each effect with its own.")
    return pd.Series(output["se"].values, index=output["term"])


def dbar_oneway(formula, data):
    """
    One-Way (Main) Effect: the mean of the runs at the factor's second ("high")
    level minus the mean of the runs at its first ("low") level.

    >>> dbar_oneway("tastiness ~ machine", lattes)
    """
    frame, (a,) = factorial_frame(formula, data)
    frame = frame.assign(a=(frame[a] == sorted(frame[a].unique())[1]).astype(int))
    # One mean per level of a, then high minus low
    xbar = frame.groupby("a")["y"].mean()
    return xbar[1] - xbar[0]


def dbar_twoway(formula, data):
    """
    Two-Way Interaction Effect: averages the means of the four combinations of
    two factors, same-direction combinations (high-high, low-low) minus
    opposite-direction combinations (high-low, low-high).

    >>> dbar_twoway("tastiness ~ machine * syrup", lattes)
    """
    frame, (a, b) = factorial_frame(formula, data)
    frame = frame.assign(a=(frame[a] == sorted(frame[a].unique())[1]).astype(int),
                         b=(frame[b] == sorted(frame[b].unique())[1]).astype(int))
    # One mean per combination of a and b
    cells = frame.groupby(["a", "b"])["y"].mean().reset_index()
    same = cells["a"] == cells["b"]
    return cells.loc[same, "y"].mean() - cells.loc[~same, "y"].mean()


def dbar_threeway(formula, data):
    """
    Three-Way Interaction Effect: averages the means of the eight combinations
    of three factors, combinations whose signs multiply to + minus those whose
    signs multiply to -.

    >>> dbar_threeway("tastiness ~ machine * syrup * art", lattes)
    """
    frame, (a, b, c) = factorial_frame(formula, data)
    frame = frame.assign(a=(frame[a] == sorted(frame[a].unique())[1]).astype(int),
                         b=(frame[b] == sorted(frame[b].unique())[1]).astype(int),
                         c=(frame[c] == sorted(frame[c].unique())[1]).astype(int))
    # One mean per combination of a, b and c, with its sign in the contrast
    cells = frame.groupby(["a", "b", "c"])["y"].mean().reset_index()
    sign = (2 * cells["a"] - 1) * (2 * cells["b"] - 1) * (2 * cells["c"] - 1)
    return cells.loc[sign == 1, "y"].mean() - cells.loc[sign == -1, "y"].mean()


def effects_factorial(formula, data, conf=0.95):
    """
    Table of Factorial Effects

    Every main effect, two-way and three-way interaction among the factors, each
    with its standard error (from se_factorial()) and a t confidence interval on
    the pooled degrees of freedom. Factors must have two levels. For messy,
    unbalanced data, use a linear model instead.

    Returns a DataFrame with one row per term: term, effect, se, lower, upper.

    >>> effects_factorial("tastiness ~ machine + syrup + art", lattes)
    """
    # Standard errors (and the two-level check) come from se_factorial()
    ses = se_factorial(formula, data, table=True)
    frame, xvars = factorial_frame(formula, data)
    # Each effect from the matching dbar function
    dbar = {1: dbar_oneway, 2: dbar_twoway, 3: dbar_threeway}
    effect = np.array([dbar[len(t.split(":"))]("y ~ " + " * ".join(t.split(":")), frame)
                       for t in ses["term"]])
    # t interval on the pooled degrees of freedom
    t_crit = stats.t.ppf(1 - (1 - conf) / 2, ses["df"].iloc[0])
    return pd.DataFrame({"term": ses["term"], "effect": effect, "se": ses["se"],
                         "lower": effect - t_crit * ses["se"], "upper": effect + t_crit * ses["se"]})
