"""R's calculate(): the full truth table of a formulate() function."""

from __future__ import annotations

import itertools

import numpy as np
import pandas as pd

from .formulate import formal_args


def calculate(f) -> pd.DataFrame:
    """One column per argument of ``f`` (0/1) plus ``outcome`` (1 = top event
    fails, i.e. ``f(...) >= 1``), 2^n rows in ``tidyr::expand_grid()`` order (last
    event varies fastest), then stably sorted by ``outcome`` descending -- R's
    ``arrange(desc(outcome))``. All columns are float, like R's <dbl>."""
    fargs = formal_args(f)
    grid = np.array(list(itertools.product((0.0, 1.0), repeat=len(fargs))), dtype=float)
    grid = grid.reshape(2 ** len(fargs), len(fargs))
    value = f(*[grid[:, j] for j in range(len(fargs))])
    outcome = np.broadcast_to(np.asarray(value, dtype=float) >= 1, (grid.shape[0],)).astype(float)
    tab = pd.DataFrame(grid, columns=fargs)
    tab["outcome"] = outcome
    return tab.sort_values("outcome", ascending=False, kind="stable").reset_index(drop=True)
