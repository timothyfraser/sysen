"""The tidyfault data model: a fault tree is two tidy tables.

``nodes``  one row per node: ``id`` (unique), ``event`` (name; a basic event may
           appear on several nodes, each with its own id), ``type`` (``"top"``,
           ``"and"``, ``"or"`` or ``"not"``; ``"not"`` means "not a gate", i.e. a
           basic event).
``edges``  one row per directed link, ``from`` (parent id) -> ``to`` (child id).

R stores ``type`` as a factor with levels ``top, and, or, not``; here it is a
pandas Categorical with the same categories in the same order. R has no
validator; :func:`validate_tree` is a Python addition that names every problem
it finds instead of letting a malformed tree fail later inside ``curate()``.
"""

from __future__ import annotations

import pandas as pd

NODE_COLUMNS = ("id", "event", "type")
EDGE_COLUMNS = ("from", "to")
NODE_TYPES = ("top", "and", "or", "not")   # R factor levels, in R's order
GATE_TYPES = ("top", "and", "or")          # node types that have children


def _frame(data, what):
    if isinstance(data, pd.DataFrame):
        return data.copy()
    try:
        return pd.DataFrame(data)
    except Exception as exc:  # pragma: no cover - pandas error text is enough
        raise TypeError(f"{what} must be a DataFrame or something pandas can build one from") from exc


def as_nodes(data) -> pd.DataFrame:
    """Return ``data`` as a nodes table: columns ``id, event, type`` (extra columns
    kept), ``type`` as a Categorical with R's levels ``top, and, or, not``."""
    df = _frame(data, "nodes")
    missing = [c for c in NODE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"nodes is missing column(s) {missing}; need {list(NODE_COLUMNS)}")
    bad = sorted(set(df["type"].astype(str)) - set(NODE_TYPES))
    if bad:
        raise ValueError(f"nodes$type has value(s) {bad}; allowed: {list(NODE_TYPES)}")
    df["type"] = pd.Categorical(df["type"].astype(str), categories=list(NODE_TYPES))
    df["event"] = df["event"].astype(str)
    return df


def as_edges(data) -> pd.DataFrame:
    """Return ``data`` as an edges table with columns ``from, to`` (extra columns kept)."""
    df = _frame(data, "edges")
    missing = [c for c in EDGE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"edges is missing column(s) {missing}; need {list(EDGE_COLUMNS)}")
    return df


def validate_tree(nodes, edges) -> bool:
    """Check that ``nodes``/``edges`` describe a well-formed fault tree.

    Fails closed: raises ``ValueError`` listing every problem found, returns
    ``True`` otherwise. Checks: required columns and node types; unique node
    ids; exactly one ``top`` node; every edge endpoint is a known id; every gate
    (``top``/``and``/``or``) has at least one child; basic events (``not``)
    have no children; and the graph has no cycle. A basic event shared by two
    branches is modelled as in R: the same ``event`` name on two distinct ids.
    """
    nodes = as_nodes(nodes)
    edges = as_edges(edges)
    problems = []

    dup = nodes["id"][nodes["id"].duplicated()].tolist()
    if dup:
        problems.append(f"duplicate node id(s): {dup}")

    n_top = int((nodes["type"] == "top").sum())
    if n_top != 1:
        problems.append(f"expected exactly one 'top' node, found {n_top}")

    ids = set(nodes["id"].tolist())
    for col in EDGE_COLUMNS:
        unknown = sorted({v for v in edges[col].tolist() if v not in ids}, key=str)
        if unknown:
            problems.append(f"edges${col} refers to unknown node id(s): {unknown}")

    parents = set(edges["from"].tolist())
    type_of = dict(zip(nodes["id"].tolist(), nodes["type"].astype(str).tolist()))
    childless = [i for i, t in type_of.items() if t in GATE_TYPES and i not in parents]
    if childless:
        problems.append(f"gate/top node id(s) with no children: {childless}")
    leafy = sorted({i for i in parents if type_of.get(i) == "not"}, key=str)
    if leafy:
        problems.append(f"basic-event ('not') node id(s) with children: {leafy}")

    # cycle check (iterative DFS)
    children = {}
    for a, b in zip(edges["from"].tolist(), edges["to"].tolist()):
        children.setdefault(a, []).append(b)
    state = {}
    for start in children:
        if state.get(start):
            continue
        stack = [(start, iter(children.get(start, ())))]
        state[start] = 1
        while stack:
            node, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                state[node] = 2
                stack.pop()
            elif state.get(nxt) == 1:
                problems.append(f"cycle through node id {nxt}")
                stack = []
            elif not state.get(nxt):
                state[nxt] = 1
                stack.append((nxt, iter(children.get(nxt, ()))))
        if problems and problems[-1].startswith("cycle"):
            break

    if problems:
        raise ValueError("invalid fault tree:\n  - " + "\n  - ".join(problems))
    return True
