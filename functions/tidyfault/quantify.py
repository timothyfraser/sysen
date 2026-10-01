"""R's quantify() (the dispatcher), quantify_binary(), quantify_binary_fast()
and quantify_prob_fast(). In R the "fast" variants are optimised code paths
with the same results; here each pair is one function, so the fast names are
aliases."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .formulate import formal_args
from .quantify_prob import quantify_prob


def _as01(v):
    """R's as.integer(as.logical(x)): TRUE/nonzero -> 1, FALSE/0 -> 0."""
    a = np.asarray(v)
    if a.dtype == bool:
        return a.astype(int)
    return (np.asarray(a, dtype=float) != 0).astype(int)


def quantify_binary(f, newdata):
    """Does the top event occur? ``newdata`` holds 0/1 (or True/False) states.

    A DataFrame (one column per basic event, extra columns ignored) -> numpy bool
    array, one value per row. One scenario (dict / Series, or a list in
    ``formal_args(f)`` order) -> a single bool. Failure means ``f(...) >= 1``.
    """
    fargs = formal_args(f)
    if isinstance(newdata, pd.DataFrame):
        missing = [a for a in fargs if a not in newdata.columns]
        if missing:
            raise ValueError("newdata must contain columns for all basic events. Missing: "
                             + ", ".join(missing))
        args = {a: _as01(newdata[a].to_numpy()) for a in fargs}
        return np.asarray(f(**args) >= 1, dtype=bool)
    if isinstance(newdata, np.ndarray) and newdata.ndim == 2:
        raise ValueError("newdata must contain columns for all basic events: "
                         + ", ".join(fargs) + " (pass a DataFrame)")
    if isinstance(newdata, (dict, pd.Series)):
        nd = dict(newdata)
        if not all(a in nd for a in fargs):
            nd = None
    else:
        nd = None
    if nd is None:
        vals = list(newdata.values()) if isinstance(newdata, dict) else list(np.asarray(newdata).ravel())
        if len(vals) != len(fargs):
            raise ValueError(f"newdata length must match number of basic events ({len(fargs)}).")
        nd = dict(zip(fargs, vals))
    args = {a: int(_as01(nd[a])) for a in fargs}
    return bool(f(**args) >= 1)


quantify_binary_fast = quantify_binary
quantify_prob_fast = quantify_prob


def quantify(f, newdata, prob=False, fast=True):
    """R's quantify(): ``prob=False`` -> quantify_binary() (does the top event
    occur?), ``prob=True`` -> quantify_prob() (its probability). ``fast`` is
    accepted for R compatibility; both settings give identical results here."""
    if not isinstance(prob, (bool, np.bool_)):
        raise ValueError("prob must be a single TRUE/FALSE value.")
    if not isinstance(fast, (bool, np.bool_)):
        raise ValueError("fast must be a single TRUE/FALSE value.")
    if prob:
        return (quantify_prob_fast if fast else quantify_prob)(f, newdata=newdata, truth_table=None)
    return (quantify_binary_fast if fast else quantify_binary)(f, newdata=newdata)
