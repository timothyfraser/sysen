"""R's mocus(), mocus_r(), mocus_rcpp() / mocus_cpp(): MOCUS (Method of Obtaining
Cutsets). Pure Python; the queue algorithm is R's mocus_r() / the C++ in
mocus_rcpp() step for step, so cut sets come back in R's order.

One deliberate deviation (README, "Deviations from R"): R expands the TOP event
like an AND gate, while curate() and equate() join the top event's children
with OR. By default this port follows the equation (``top="or"``), so the cut
sets agree with equate() and formulate(); ``top="and"`` reproduces R exactly.
"""

from __future__ import annotations

from collections import deque

METHODS = ("mocus_rcpp", "mocus_r", "mocus_original")
TOP_MODES = ("or", "and")


def _gate_table(data):
    for col in ("gate", "type", "class", "items"):
        if col not in data.columns:
            raise ValueError(f"mocus(): data is missing column '{col}' (pass the output of curate())")
    table = {}
    for gate, typ, items in zip(data["gate"].astype(str), data["type"].astype(str), data["items"]):
        children = [str(i) for i in (items if items is not None else []) if i is not None]
        table[gate] = (typ, children)
    tops = [g for g, c in zip(data["gate"].astype(str), data["class"].astype(str)) if c == "top"]
    if not tops:
        raise ValueError("mocus(): data has no row with class == 'top'")
    return table, tops[0]


def _mocus(data, top="or"):
    if top not in TOP_MODES:
        raise ValueError("top must be 'or' (the equation's semantics) or 'and' (R's current mocus)")
    table, top_gate = _gate_table(data)
    and_types = {"and"} | ({"top"} if top == "and" else set())

    queue = deque([[top_gate]])
    results = []
    while queue:
        cutset = queue.popleft()
        and_pos, or_pos = [], []
        for p, tok in enumerate(cutset):
            if tok in table:
                (and_pos if table[tok][0] in and_types else or_pos).append(p)
        if not and_pos and not or_pos:
            results.append(list(dict.fromkeys(cutset)))     # R's unique(): first occurrence order
            continue
        if and_pos:                                         # expand every AND gate in one pass
            drop = set(and_pos)
            nc = [t for p, t in enumerate(cutset) if p not in drop]
            for p in and_pos:
                nc.extend(table[cutset[p]][1])
            queue.append(nc)
        else:                                               # branch on the first OR gate
            p0 = or_pos[0]
            rest = [t for p, t in enumerate(cutset) if p != p0]
            for child in table[cutset[p0]][1]:
                queue.append(rest + [child])
    return results


def mocus(data, method="mocus_rcpp", top="or"):
    """Every cut set of the tree in ``data`` (the output of curate()).

    Returns a list of lists of basic-event names, one list per cut set (not yet
    minimal; concentrate() minimises). ``method`` takes R's labels; all three run
    the same pure-Python queue algorithm, which reproduces mocus_rcpp() and
    mocus_r() element for element ("mocus_original", R's historical loop, is
    accepted as a label only). ``top="or"`` (default) expands the top event as
    OR, as equate() does; ``top="and"`` expands it as AND, exactly as R's
    mocus() does today.
    """
    if method not in METHODS:
        raise ValueError("'method' should be one of " + ", ".join(repr(m) for m in METHODS))
    return _mocus(data, top=top)


def mocus_r(data, top="or"):
    """R's mocus_r(): the pure queue-based MOCUS. Same output as mocus()."""
    return _mocus(data, top=top)


def mocus_rcpp(data, top="or"):
    """R's mocus_rcpp(): compiled in R, pure Python here. Same output as mocus()."""
    return _mocus(data, top=top)


mocus_cpp = mocus_rcpp
