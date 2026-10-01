"""R's equate(): the boolean equation of the whole tree, from curate()'s output."""

from __future__ import annotations

import re

_NAME = r"A-Za-z0-9_."


def _pattern(gate):
    # Whole-token match. R uses the gate name as a regex SUBSTRING (see README,
    # "Deliberate deviations"); the two agree whenever no gate name sits inside
    # another name, which is true of every bundled tree except ai_nodes.
    return re.compile(rf"(?<![{_NAME}]){re.escape(gate)}(?![{_NAME}])")


def _check_acyclic(gates, pats, sets):
    refs = {g: [h for h, p in zip(gates, pats) if p.search(s)] for g, s in zip(gates, sets)}
    state = {}

    def visit(g, path):
        if state.get(g) == 1:
            raise ValueError("equate(): the gates reference each other in a cycle: "
                             + " -> ".join(path + [g]))
        if state.get(g) == 2:
            return
        state[g] = 1
        for h in refs.get(g, ()):
            visit(h, path + [g])
        state[g] = 2

    for g in gates:
        visit(g, [])


def equate(data) -> str:
    """Return the top event's boolean equation as R builds it: repeatedly replace
    each gate name (first occurrence per set, gates in row order) with that gate's
    ``set`` until no gate name remains; the first row's set is the answer. ``*`` is
    AND, ``+`` is OR, and every gate keeps its ``" (...) "`` wrapping, e.g.
    ``" ( ( (B *  (C + D) )  *  (A +  (B * C) ) ) ) "`` for fakenodes/fakeedges."""
    gates = [str(g) for g in data["gate"]]
    sets = [str(s) for s in data["set"]]
    pats = [_pattern(g) for g in gates]
    _check_acyclic(gates, pats, sets)

    def present():
        return sum(1 for p in pats for s in sets if p.search(s))

    while present() > 0:
        for i, p in enumerate(pats):
            rep = sets[i]
            sets = [p.sub(lambda _m, rep=rep: rep, s, count=1) for s in sets]

    equation = sets[0]
    # defensive cleanup, as in R: any leftover | becomes OR
    return equation.replace("|", " + ")
