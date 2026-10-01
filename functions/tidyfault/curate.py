"""R's curate(): one row per gate with the set of events immediately below it."""

from __future__ import annotations

import pandas as pd

from .tree import NODE_COLUMNS, EDGE_COLUMNS

_JOIN = {"and": " * ", "or": " + ", "top": " + "}   # top's children are OR'd, as in R


def curate(nodes, edges) -> pd.DataFrame:
    """Columns ``gate, type, class, n, set, items`` exactly as R returns them:
    top event first, then gates in (C-locale) alphabetical order; ``set`` is the
    gate's inputs joined with `` * `` (and) or `` + `` (or/top) and wrapped as
    ``" (...) "``; ``items`` is the list of input event names."""
    for col in NODE_COLUMNS:
        if col not in nodes.columns:
            raise ValueError(f"curate(): nodes is missing column '{col}'")
    for col in EDGE_COLUMNS:
        if col not in edges.columns:
            raise ValueError(f"curate(): edges is missing column '{col}'")

    typ = nodes["type"].astype(str)
    g = nodes.loc[typ.isin(["top", "and", "or"]), ["id", "event", "type"]]
    e = edges[["from", "to"]]
    # left_join(by = c("id" = "from")): left order kept, matches in edges order
    j = g.merge(e, how="left", left_on="id", right_on="from", sort=False)
    names = nodes[["id", "event"]].rename(columns={"id": "to", "event": "to_event"})
    j = j.merge(names, how="left", on="to", sort=False)

    rows = []
    for gate_name in sorted(j["event"].astype(str).unique()):
        sub = j[j["event"].astype(str) == gate_name]
        types = pd.unique(sub["type"].astype(str))
        if len(types) != 1:
            raise ValueError(f"curate(): gate '{gate_name}' appears with several types {list(types)}")
        t = types[0]
        to_event = ["NA" if pd.isna(v) else str(v) for v in sub["to_event"]]
        items = [None if pd.isna(v) else str(v) for v in sub["to_event"]]
        rows.append({
            "gate": gate_name,
            "type": t,
            "class": "top" if t == "top" else "gate",
            "n": len(to_event),
            "set": " (" + _JOIN[t].join(to_event) + ") ",
            "items": items,
        })
    out = pd.DataFrame(rows, columns=["gate", "type", "class", "n", "set", "items"])
    # arrange(class, gate): top first, then gates
    out["_k"] = (out["class"] != "top").astype(int)
    out = out.sort_values(["_k", "gate"], kind="stable").drop(columns="_k").reset_index(drop=True)
    if isinstance(nodes["type"].dtype, pd.CategoricalDtype):
        out["type"] = pd.Categorical(out["type"], categories=nodes["type"].cat.categories)
    out["class"] = pd.Categorical(out["class"], categories=["top", "gate"])
    out["n"] = out["n"].astype("int64")
    return out
