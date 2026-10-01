"""R's tabulate(): coverage of each minimal cutset over the failing truth-table rows."""

from __future__ import annotations

import re

import pandas as pd

from .calculate import calculate

METHODS = ("mocus_rcpp", "mocus_r", "mocus_original")


def _strip_outer_parens(s):
    s = s.strip()
    while s and s[0] == "(" and s[-1] == ")":
        s = s[1:-1].strip()
    return s


def tabulate(data, formula, method="mocus_rcpp", query=False) -> pd.DataFrame:
    """``data``: minimal cutsets as strings (e.g. ``["B*C", "A*B*D"]``, what
    concentrate() returns); ``formula``: the formulate() function. Returns one row
    per cutset (sorted) with ``mincut, [query,] cutsets, failures, coverage``,
    where ``cutsets`` counts failing truth-table rows that contain the cutset,
    ``failures`` counts all failing rows and ``coverage = cutsets / failures``."""
    if method not in METHODS:
        raise ValueError("'method' should be one of " + ", ".join(repr(m) for m in METHODS))
    if isinstance(data, str):
        data = [data]
    tab = calculate(formula)
    fails = tab[tab["outcome"] == 1]
    rows = []
    for mincut in sorted(set(str(d) for d in data)):
        events = [e.strip() for e in re.split(r"\s*\*\s*", _strip_outer_parens(mincut))]
        labels, mask = [], pd.Series(True, index=fails.index)
        for ev in events:
            value = 0 if "~" in ev else 1
            labels.append(f"{ev} == {value}")
            col = ev.replace("~", "").strip()
            if col not in tab.columns:
                raise ValueError(f"tabulate(): cutset '{mincut}' names '{col}', which is not an event of formula")
            mask &= fails[col] == value
        rows.append({
            "mincut": mincut,
            "query": "filter(" + ", ".join(labels + ["outcome == 1"]) + ")",
            "cutsets": int(mask.sum()),
            "failures": int(len(fails)),
        })
    out = pd.DataFrame(rows, columns=["mincut", "query", "cutsets", "failures"])
    out["cutsets"] = out["cutsets"].astype("int64")
    out["failures"] = out["failures"].astype("int64")
    out["coverage"] = out["cutsets"] / out["failures"]
    if not query:
        out = out.drop(columns="query")
    return out
