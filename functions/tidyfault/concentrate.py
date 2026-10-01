"""R's concentrate(): the minimal cut sets of a fault tree, as strings like
``"A*B"``. R runs MOCUS and then admisc::simplify(); every cut set here is a
product of plain (un-negated) basic events, so the minimal sum of products is
exactly the cut sets left after dropping duplicates and supersets (absorption),
which is what this port computes."""

from __future__ import annotations

from .formulate import r_sort
from .mocus import METHODS, _mocus


def _minimal(cutsets):
    sets = []
    for cs in cutsets:
        s = frozenset(cs)
        if s not in sets:
            sets.append(s)
    return [s for s in sets if not any(o < s for o in sets)]


def concentrate(data, method="mocus_rcpp", top="or"):
    """Minimal cut sets of the tree in ``data`` (the output of curate()).

    Returns a list of strings, one per minimal cut set, events joined by ``*``
    in R's sorted order, sets ordered as admisc::simplify() orders them: fewer
    events first, then by the events' positions in the sorted event list.
    ``top`` is passed to mocus(): ``"or"`` (default) follows the equation,
    ``"and"`` reproduces R's current output (README, "Deviations from R").
    """
    if method not in METHODS:
        raise ValueError("'method' should be one of " + ", ".join(repr(m) for m in METHODS))
    cutsets = _mocus(data, top=top)
    names = r_sort(list(dict.fromkeys(e for cs in cutsets for e in cs)))
    pos = {n: i for i, n in enumerate(names)}
    keyed = [sorted(s, key=pos.__getitem__) for s in _minimal(cutsets)]
    keyed.sort(key=lambda s: (len(s), [pos[e] for e in s]))
    return ["*".join(s) for s in keyed]
