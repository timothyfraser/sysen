"""R's quantify_prob(): exact top-event probability from basic-event
probabilities, summed over the failing rows of calculate()'s truth table
(independent basic events)."""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

from .calculate import calculate
from .formulate import formal_args


def _row_probs(tt_mat, P):
    # P: scenarios x events; tt_mat: truth rows x events -> truth rows x scenarios
    terms = np.where(tt_mat[:, None, :] == 1, P[None, :, :], 1 - P[None, :, :])
    return np.prod(terms, axis=2)


def _check_tt(truth_table, fargs):
    cols = [c for c in truth_table.columns if c != "outcome"]
    if not all(a in cols for a in fargs) or "outcome" not in truth_table.columns:
        raise ValueError("truth_table must contain columns for each basic event and 'outcome'.")
    return cols


def quantify_prob(f, newdata, truth_table=None):
    """Probability that the top event occurs.

    ``newdata`` is one scenario (dict / Series / list in ``formal_args(f)`` order /
    one-row DataFrame) -> returns a float; or several (DataFrame with one row per
    scenario and a column per event) -> returns a numpy array, one value per row.
    Pass ``truth_table`` (from calculate()) to skip recomputing it.
    """
    fargs = formal_args(f)
    multi = isinstance(newdata, pd.DataFrame) and len(newdata) > 1
    if isinstance(newdata, np.ndarray) and newdata.ndim == 2:
        if newdata.shape[0] > 1:
            raise ValueError("newdata matrix must have column names matching basic events: "
                             + ", ".join(fargs) + " (pass a DataFrame)")
        newdata = newdata[0]

    if not multi:
        if isinstance(newdata, pd.DataFrame):
            row = newdata.iloc[0]
            newdata = row[fargs] if all(a in newdata.columns for a in fargs) else list(row.to_numpy())
        if isinstance(newdata, dict):
            newdata = pd.Series(newdata, dtype=float)
        if isinstance(newdata, pd.Series):
            missing = [a for a in fargs if a not in newdata.index]
            if missing:
                raise ValueError("newdata must contain values for all basic events. Missing: "
                                 + ", ".join(missing))
            p = newdata.astype(float)
        else:
            vals = np.asarray(newdata, dtype=float).ravel()
            if len(vals) != len(fargs):
                raise ValueError(f"newdata length must match number of basic events ({len(fargs)}).")
            p = pd.Series(vals, index=fargs)
        if ((p < 0) | (p > 1)).any():
            warnings.warn("Some newdata values are outside [0, 1]; result may not be a valid probability.")
        if truth_table is None:
            truth_table = calculate(f)
        cols = _check_tt(truth_table, fargs)
        P = p.reindex(cols).to_numpy(dtype=float)[None, :]
        rows = _row_probs(truth_table[cols].to_numpy(dtype=float), P)[:, 0]
        return float(np.sum(rows[truth_table["outcome"].to_numpy() >= 1]))

    missing = [a for a in fargs if a not in newdata.columns]
    if missing:
        raise ValueError("newdata must contain columns for all basic events. Missing: " + ", ".join(missing))
    P = newdata[fargs].to_numpy(dtype=float)
    if ((P < 0) | (P > 1)).any():
        warnings.warn("Some newdata values are outside [0, 1]; results may not be valid probabilities.")
    if truth_table is None:
        truth_table = calculate(f)
    _check_tt(truth_table, fargs)
    rows = _row_probs(truth_table[fargs].to_numpy(dtype=float), P)
    return rows[truth_table["outcome"].to_numpy() >= 1].sum(axis=0)
