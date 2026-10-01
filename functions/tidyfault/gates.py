"""Gate polygons for drawing fault trees: R's gate(), gate_and(), gate_or(),
gate_top() and get_gate(), returning DataFrames with the same columns.

The arithmetic follows the R source operation by operation (R's ``seq()``,
``scales::rescale()``), so coordinates match R to floating-point equality.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

_EPS = np.finfo(float).eps


def _seq(from_, to, length_out):
    """R's ``seq(from, to, length.out = n)`` (seq.default), operation for operation."""
    n = int(length_out)
    if n < 1:
        return np.array([], dtype=float)
    if n > 2:
        if from_ == to:
            return np.full(n, float(from_))
        n1 = n - 1
        mid = from_ + np.arange(1, n1, dtype=float) * ((to - from_) / n1)
        return np.concatenate(([float(from_)], mid, [float(to)]))
    return np.array([from_, to], dtype=float)[:n]


def _zero_range(r, tol=1000 * _EPS):
    """scales::zero_range()."""
    a, b = float(r[0]), float(r[1])
    if a == b:
        return True
    if np.isinf(a) and np.isinf(b):
        return False
    m = min(abs(a), abs(b))
    if m == 0:
        return False
    return abs((a - b) / m) < tol


def _rescale(x, to):
    """scales::rescale(x, to) with from = range(x)."""
    x = np.asarray(x, dtype=float)
    frm = (np.nanmin(x), np.nanmax(x))
    if _zero_range(frm) or _zero_range(to):
        return np.where(np.isnan(x), np.nan, (to[0] + to[1]) / 2)
    return (x - frm[0]) / (frm[1] - frm[0]) * (to[1] - to[0]) + to[0]


def _need_res(res, fn):
    if res is None:
        # R: argument "res" is missing, with no default
        raise TypeError(f'{fn}(): argument "res" is missing, with no default')


def gate_and(size=2, res=None) -> pd.DataFrame:
    """AND gate polygon centred on (0, 0): columns ``x``, ``y``."""
    _need_res(res, "gate_and")
    xmid = size / 2
    x1 = _seq(0, size, 1)
    y1 = np.zeros_like(x1)
    x2 = _seq(size, 0, res)
    with np.errstate(invalid="ignore"):
        y2 = np.where(x2 < xmid, size * np.sqrt(x2) * 2 / 3, size * np.sqrt(size - x2) * 2 / 3)
    x = np.concatenate((x1, x2))
    y = np.concatenate((y1, y2))
    return pd.DataFrame({"x": x - xmid, "y": y - np.nanmax(y) / 2})


def gate_or(size=2, res=None) -> pd.DataFrame:
    """OR gate polygon centred on (0, 0): columns ``x``, ``y``."""
    _need_res(res, "gate_or")
    xmid = size / 2
    x1 = _seq(0, size, res)
    with np.errstate(invalid="ignore"):
        y1 = np.where(x1 < xmid, 1 / (size) * np.sqrt(x1) * 2 / 3, 1 / (size) * np.sqrt(size - x1) * 2 / 3)
    x2 = _seq(size, 0, res)
    with np.errstate(invalid="ignore"):
        y2 = np.where(x2 < xmid, size * np.sqrt(x2) * 2 / 3, size * np.sqrt(size - x2) * 2 / 3)
    x = np.concatenate((x1, x2))
    y = np.concatenate((y1, y2))
    return pd.DataFrame({"x": x - xmid, "y": y - np.nanmax(y) / 2})


def gate_top(size=2, res=None) -> pd.DataFrame:
    """Top-event rectangle centred on (0, 0): columns ``x``, ``y``.
    ``res`` is required for consistency with R but does not change the shape."""
    _need_res(res, "gate_top")
    xmin, xmax, ymin, ymax = 0.0, float(size), 0.0, float(size)
    x = np.array([xmin, xmin, xmin, xmax, xmax, xmax, xmax, xmin])
    y = np.array([ymin, ymax, ymax, ymax, ymax, ymin, ymin, ymin])
    return pd.DataFrame({"x": x - size / 2, "y": y - size / 2})


def _recycle(v, n):
    v = np.asarray(v, dtype=float).ravel()
    return v[0] if v.size == 1 else np.resize(v, n)


def get_gate(x, y, gate, size=1, res=50):
    """Gate polygon of type ``gate`` (``"and"``, ``"or"`` or ``"top"``) centred on
    ``(x, y)``. Returns a DataFrame with ``x``, ``y``; ``None`` for any other type
    (R returns ``NULL``)."""
    gate = pd.unique(pd.Series(np.atleast_1d(np.asarray(gate, dtype=object))).astype(str))[0]
    if gate == "or":
        g = gate_or(size=size, res=res)
    elif gate == "and":
        g = gate_and(size=size, res=res)
    elif gate == "top":
        g = gate_top(size=size, res=res)
        n = len(g)
        # For top gate, preserve R's 3:2 width:height box
        return pd.DataFrame({
            "x": _recycle(x, n) + _rescale(g["x"].to_numpy(), (-1.5 * size, 1.5 * size)),
            "y": _recycle(y, n) + _rescale(g["y"].to_numpy(), (-size, size))})
    else:
        return None
    n = len(g)
    return pd.DataFrame({
        "x": _recycle(x, n) + _rescale(g["x"].to_numpy(), (-size, size)),
        "y": _recycle(y, n) + _rescale(g["y"].to_numpy(), (-size, size))})


def gate(data, group="id", gate="type", size=1, res=50) -> pd.DataFrame:
    """Polygons for every and/or/top node in ``data`` (which needs ``x``, ``y``).

    Returns columns ``group, gate, x, y`` -- one polygon per (group, gate), groups
    in sorted order, like R's ``group_by(group, gate) %>% reframe(get_gate(...))``.
    """
    df = data.rename(columns={group: "group", gate: "gate"})
    df = df[df["gate"].astype(str).isin(["and", "or", "top"])]
    pieces = []
    for (grp, gt), sub in df.groupby(["group", "gate"], sort=True, observed=True):
        poly = get_gate(sub["x"].to_numpy(), sub["y"].to_numpy(), gate=sub["gate"].astype(str).to_numpy(),
                        size=size, res=res)
        if poly is None:
            continue
        poly.insert(0, "gate", gt)
        poly.insert(0, "group", grp)
        pieces.append(poly)
    if not pieces:
        return pd.DataFrame(columns=["group", "gate", "x", "y"])
    out = pd.concat(pieces, ignore_index=True)
    if isinstance(data[gate].dtype, pd.CategoricalDtype):
        out["gate"] = pd.Categorical(out["gate"], categories=data[gate].cat.categories)
    return out
