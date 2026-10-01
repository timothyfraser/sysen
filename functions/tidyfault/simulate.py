"""R's simulate(): a random two-level fault tree (top -> AND/OR gates -> basic
events) with a failure probability for every basic event. Same arguments, same
checks and the same return shape as R; the random draws come from numpy, so a
seed reproduces Python runs, not R's stream (README, "Deviations from R")."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .tree import NODE_TYPES


def _nodes(event, type_):
    return pd.DataFrame({
        "id": np.arange(1, len(event) + 1, dtype="int64"),
        "event": list(event),
        "type": pd.Categorical(list(type_), categories=list(NODE_TYPES)),
    })


def simulate(n_gates=3, n_basic=8, p_range=(0.01, 0.2), seed=None):
    """Returns ``{"nodes", "edges", "prob"}`` like R's ``list(nodes, edges, prob)``:
    nodes ``id, event, type`` (top "T", gates "G1".., basic events "E1"..),
    edges ``from, to``, prob ``event, probability`` (uniform in ``p_range``).
    Each gate gets at least two basic events, so at most ``n_basic // 2`` gates
    are made. ``seed`` makes the result reproducible."""
    rng = np.random.default_rng(seed)
    p_range = list(p_range)
    if len(p_range) != 2 or not all(np.isfinite(np.asarray(p_range, dtype=float))):
        raise ValueError("p_range must be a numeric vector of length 2 with finite values.")
    lo, hi = float(p_range[0]), float(p_range[1])
    if lo <= 0 or hi >= 1 or lo >= hi:
        raise ValueError("p_range must satisfy 0 < p_range[1] < p_range[2] < 1.")
    try:
        n_gates, n_basic = int(n_gates), int(n_basic)
    except (TypeError, ValueError):
        raise ValueError("n_gates and n_basic must be integers >= 1.") from None
    if n_gates < 1:
        raise ValueError("n_gates must be an integer >= 1.")
    if n_basic < 1:
        raise ValueError("n_basic must be an integer >= 1.")

    basic_events = [f"E{i}" for i in range(1, n_basic + 1)]
    n_eff = min(n_gates, n_basic // 2)
    if n_eff < 1:   # degenerate: the top event sits directly on the basic events
        nodes = _nodes(["T"] + basic_events, ["top"] + ["not"] * n_basic)
        edges = pd.DataFrame({"from": np.ones(n_basic, dtype="int64"),
                              "to": np.arange(2, n_basic + 2, dtype="int64")})
    else:
        gate_types = list(rng.choice(["and", "or"], size=n_eff, replace=True))
        nodes = _nodes(["T"] + [f"G{i}" for i in range(1, n_eff + 1)] + basic_events,
                       ["top"] + gate_types + ["not"] * n_basic)
        gate_ids = np.arange(2, n_eff + 2)
        basic_ids = np.arange(n_eff + 2, n_eff + 2 + n_basic)
        assignment = np.repeat(np.arange(n_eff), 2)             # two basic events per gate
        extra = n_basic - len(assignment)
        if extra > 0:
            assignment = np.concatenate([assignment, rng.integers(0, n_eff, size=extra)])
        edges = pd.DataFrame({
            "from": np.concatenate([np.ones(n_eff, dtype="int64"), gate_ids[assignment]]).astype("int64"),
            "to": np.concatenate([gate_ids, basic_ids]).astype("int64"),
        })
    prob = pd.DataFrame({"event": basic_events,
                         "probability": rng.uniform(lo, hi, size=n_basic)})
    return {"nodes": nodes, "edges": edges, "prob": prob}
