"""illustrate(): R tidyfault's tree layout for drawing a fault tree.

R builds a ``tidygraph`` graph and calls ``ggraph::create_layout(layout = "tree")``,
which is igraph's Reingold-Tilford layout (``igraph::layout_as_tree``, mode
``"out"``, ``flip.y = TRUE``). This module ports that layout step by step:

1. **Root.** The one node nothing points to (the top event). igraph picks the
   source of a directed tree the same way.
2. **Depth (y).** Breadth-first search from the root, neighbours in node-row
   order; each node's parent is whoever reached it first and its level is the
   parent's plus one. ``flip.y`` then sets ``y = max(level) - level``, so the
   top event sits highest and the deepest leaves sit at ``y = 0``.
3. **Width (x).** A post-order pass places each node's subtrees side by side in
   node-row order: the first child at offset 0, every later child as close to
   the previous ones as the contours allow with a minimum gap of 1, threading
   the contours where one subtree is deeper than its neighbour. The parent is
   then centred on the **mean** of its children's offsets.
4. **Coordinates.** A pre-order pass adds the offsets down from the root at
   ``x = 0``.

The result has the same columns as R's: ``nodes`` (``x, y`` plus every column of
``nodes``), ``edges`` (``edge_id, direction, id, x, y``; two rows per edge, ready
for a line plot), ``gates`` (``group, gate, x, y`` polygons from
:func:`tidyfault.gates.gate`) and, for ``type="all"``, ``pairwise`` (the edge
table plus ``from_x, from_y, to_x, to_y, edge_id``). R returns a list; this
returns a dict with the same names.

Only ``layout="tree"`` (R's default) is ported; any other layout raises.
"""

from __future__ import annotations

from collections import deque

import numpy as np
import pandas as pd

from .gates import gate as _gate

_TYPES = ("nodes", "edges", "both", "all")
_MINSEP = 1.0


def _edge_positions(nodes, edges, node_key):
    """0-based node rows for each edge's ends, the way tidygraph::tbl_graph does it:
    numeric ``from``/``to`` are 1-based row numbers; character ones are matched
    against ``nodes[node_key]``."""
    key = nodes[node_key] if node_key in nodes.columns else nodes.iloc[:, 0]
    lookup = {k: i for i, k in enumerate(key.astype(str))}
    out = []
    for col in ("from", "to"):
        v = edges[col]
        if pd.api.types.is_numeric_dtype(v):
            pos = v.to_numpy(dtype=float) - 1
        else:
            pos = np.array([lookup.get(str(s), np.nan) for s in v], dtype=float)
        if np.isnan(pos).any() or (pos < 0).any() or (pos >= len(nodes)).any():
            bad = edges.loc[np.isnan(pos) | (pos < 0) | (pos >= len(nodes)), col].tolist()
            raise ValueError(f"illustrate(): edges${col} values {bad!r} do not name a node")
        out.append(pos.astype(int))
    return out[0], out[1]


def _reingold_tilford(n, src, dst):
    """igraph's Reingold-Tilford tree layout for a single-rooted directed graph.
    Returns ``(x, level)`` as float arrays, one entry per node row."""
    children_out = [[] for _ in range(n)]
    indeg = np.zeros(n, dtype=int)
    for f, t in zip(src, dst):
        children_out[f].append(t)
        indeg[t] += 1
    for nb in children_out:
        nb.sort()  # igraph's adjacency list is sorted by vertex id
    roots = [i for i in range(n) if indeg[i] == 0]
    if len(roots) != 1:
        raise ValueError(
            f"illustrate(): a fault tree needs exactly one top event (a node with no incoming edge); "
            f"found {len(roots)}: rows {roots}")
    root = roots[0]

    # Step 1: BFS levels and parents.
    parent = [-1] * n
    level = [-1] * n
    parent[root] = root
    level[root] = 0
    q = deque([root])
    while q:
        act = q.popleft()
        for nb in children_out[act]:
            if parent[nb] >= 0:
                continue
            parent[nb] = act
            level[nb] = level[act] + 1
            q.append(nb)
    unreached = [i for i in range(n) if level[i] < 0]
    if unreached:
        raise ValueError(f"illustrate(): node rows {unreached} cannot be reached from the top event")
    kids = [[i for i in range(n) if i != v and parent[i] == v] for v in range(n)]

    offset = [0.0] * n
    lc = [-1] * n
    rc = [-1] * n
    off_lc = [0.0] * n
    off_rc = [0.0] * n
    lx = list(range(n))
    rx = list(range(n))
    off_lx = [0.0] * n
    off_rx = [0.0] * n

    # Step 2: post-order placement of subtrees (igraph_i_layout_reingold_tilford_postorder).
    def postorder(node):
        for i in kids[node]:
            postorder(i)
        if not kids[node]:
            return
        leftroot = -1
        avg = 0.0
        for j, i in enumerate(kids[node]):
            if leftroot >= 0:
                lnode, rnode = leftroot, i
                rootsep = offset[leftroot] + _MINSEP
                loffset = offset[leftroot]
                roffset = loffset + _MINSEP
                rc[node] = i
                off_rc[node] = rootsep
                while lnode >= 0 and rnode >= 0:
                    # next level on the right contour of the left subtree
                    if rc[lnode] >= 0:
                        loffset += off_rc[lnode]
                        lnode = rc[lnode]
                    else:
                        if lc[rnode] >= 0:
                            # left subtree ended: thread its contours onto the right subtree
                            aux = lx[node]
                            newoffset = (off_rx[node] - off_lx[node]) + _MINSEP + off_lc[rnode]
                            lc[aux] = lc[rnode]
                            rc[aux] = lc[rnode]
                            off_lc[aux] = off_rc[aux] = newoffset
                            lx[node] = lx[i]
                            rx[node] = rx[i]
                            off_lx[node] = off_lx[i] + rootsep
                            off_rx[node] = off_rx[i] + rootsep
                        else:
                            # both subtrees end together: only the right extreme moves
                            rx[node] = rx[i]
                            off_rx[node] = off_rx[i] + rootsep
                        lnode = -1
                    # next level on the left contour of the right subtree
                    if lc[rnode] >= 0:
                        roffset += off_lc[rnode]
                        rnode = lc[rnode]
                    else:
                        if lnode >= 0:
                            # right subtree ended: thread its contours onto the left subtree
                            aux = rx[i]
                            newoffset = loffset - rootsep - off_rx[i]
                            lc[aux] = lnode
                            rc[aux] = lnode
                            off_lc[aux] = off_rc[aux] = newoffset
                        rnode = -1
                    if lnode >= 0 and rnode >= 0 and (roffset - loffset < _MINSEP):
                        rootsep += _MINSEP - roffset + loffset
                        roffset = loffset + _MINSEP
                        off_rc[node] = rootsep
                offset[i] = rootsep
                off_rc[node] = rootsep
                avg = (avg * j) / (j + 1) + rootsep / (j + 1)
                leftroot = i
            else:
                # first child sits directly under the parent
                leftroot = i
                lc[node] = i
                rc[node] = i
                off_lc[node] = 0.0
                off_rc[node] = 0.0
                lx[node] = lx[i]
                rx[node] = rx[i]
                off_lx[node] = off_lx[i]
                off_rx[node] = off_rx[i]
                avg = offset[i]
        # centre the parent over its children
        off_lc[node] -= avg
        off_rc[node] -= avg
        off_lx[node] -= avg
        off_rx[node] -= avg
        for i in kids[node]:
            offset[i] -= avg

    postorder(root)

    # Step 3: pre-order coordinates (igraph_i_layout_reingold_tilford_calc_coords).
    x = np.zeros(n, dtype=float)
    stack = [(root, offset[root])]
    while stack:
        node, xpos = stack.pop()
        x[node] = xpos
        for i in kids[node]:
            stack.append((i, xpos + offset[i]))
    return x, np.asarray(level, dtype=float)


def _layout_nodes(nodes, edges, node_key, layout):
    if layout != "tree":
        raise NotImplementedError(
            f"illustrate(): only layout='tree' (R's default, igraph Reingold-Tilford) is ported; got {layout!r}")
    nodes = pd.DataFrame(nodes).reset_index(drop=True)
    edges = pd.DataFrame(edges).reset_index(drop=True)
    src, dst = _edge_positions(nodes, edges, node_key)
    x, level = _reingold_tilford(len(nodes), src, dst)
    y = level.max() - level if len(level) else level  # igraph flip.y = TRUE
    out = nodes.drop(columns=[c for c in ("x", "y") if c in nodes.columns])
    out.insert(0, "y", y)
    out.insert(0, "x", x)
    return out


def illustrate(nodes, edges, type="nodes", node_key="id", layout="tree", size=0.25,
               scale_size=False, res=50):
    """Lay a fault tree out for drawing, like R ``tidyfault::illustrate()``.

    Parameters
    ----------
    nodes, edges : DataFrame
        The fault tree: ``nodes`` with ``id`` (or ``node_key``), ``event`` and
        ``type``; ``edges`` with ``from`` and ``to``.
    type : {"nodes", "edges", "both", "all"}
        What to return. ``"nodes"`` (R's actual default -- its ``match.arg``
        takes the first choice even though R's help page says ``"both"``) gives
        the node table; ``"edges"`` the line segments; ``"both"`` a dict with
        ``nodes``, ``edges`` and ``gates``; ``"all"`` adds ``pairwise``. Use
        ``"both"`` to feed :func:`tidyfault.plot.plot`.
    node_key : str
        Column of ``nodes`` that ``edges`` refer to.
    layout : str
        Only ``"tree"`` is ported.
    size, scale_size, res
        Gate polygon size and resolution, passed to :func:`tidyfault.gates.gate`.
        With ``scale_size=True`` the size is multiplied by
        ``min(x range, y range) / 4`` of the layout, as in R.
    """
    if type not in _TYPES:
        raise ValueError(f"illustrate(): 'type' should be one of {', '.join(map(repr, _TYPES))}; got {type!r}")
    gnodes = _layout_nodes(nodes, edges, node_key, layout)
    if type == "nodes":
        return gnodes

    if scale_size:
        xr = np.nanmax(gnodes["x"]) - np.nanmin(gnodes["x"])
        yr = np.nanmax(gnodes["y"]) - np.nanmin(gnodes["y"])
        extent = min(xr, yr)
        if extent < 1e-6:
            extent = 1
        size = size * extent / 4

    edges = pd.DataFrame(edges).reset_index(drop=True)
    xmap = pd.Series(gnodes["x"].to_numpy(), index=gnodes[node_key].to_numpy())
    ymap = pd.Series(gnodes["y"].to_numpy(), index=gnodes[node_key].to_numpy())
    gpairs = edges.copy()
    gpairs["from_x"] = edges["from"].map(xmap).astype(float)
    gpairs["from_y"] = edges["from"].map(ymap).astype(float)
    gpairs["to_x"] = edges["to"].map(xmap).astype(float)
    gpairs["to_y"] = edges["to"].map(ymap).astype(float)
    gpairs["edge_id"] = np.arange(1, len(edges) + 1)

    m = len(gpairs)
    gedges = pd.DataFrame({
        "edge_id": np.repeat(gpairs["edge_id"].to_numpy(), 2),
        "direction": np.tile(np.array(["from", "to"], dtype=object), m),
        "id": np.column_stack([gpairs["from"].to_numpy(), gpairs["to"].to_numpy()]).ravel(),
        "x": np.column_stack([gpairs["from_x"].to_numpy(), gpairs["to_x"].to_numpy()]).ravel(),
        "y": np.column_stack([gpairs["from_y"].to_numpy(), gpairs["to_y"].to_numpy()]).ravel(),
    })

    ggates = _gate(gnodes, group="id", gate="type", size=size, res=res)

    if type == "edges":
        return gedges
    if type == "both":
        return {"nodes": gnodes, "edges": gedges, "gates": ggates}
    return {"nodes": gnodes, "edges": gedges, "gates": ggates, "pairwise": gpairs}
