"""plot(): draw a fault tree from :func:`tidyfault.illustrate.illustrate` output,
the matplotlib twin of R ``tidyfault::plot()`` (a ggplot).

Same recipe as R: coordinates are normalised into a common box, edges are
black lines, gates are the R polygons (top-event box, AND dome, OR shield)
filled from the viridis palette with their ``event`` label in white, basic
events are circles of a radius taken from the median gate size and labelled in
black, and the legend sits underneath ("Top Event", "And Gate", "Or Gate",
"Basic Event"). Returns a matplotlib ``Figure``; :func:`to_png` saves one.

    ill = illustrate(nodes, edges, type="both")
    fig = plot(ill)
    to_png(fig, "tree.png")
"""

from __future__ import annotations

import numpy as np
import pandas as pd

_LABELS = {"top": "Top Event", "and": "And Gate", "or": "Or Gate", "basic event": "Basic Event"}
_BREAKS = ("top", "and", "or", "basic event")
# ggplot2 linewidth is in mm-ish units: lwd = linewidth * .pt, and 1 lwd = 0.75 pt.
_LW = 72.27 / 25.4 * 0.75


def _seq(a, b, n):
    n = int(n)
    if n > 2:
        return np.concatenate(([a], a + np.arange(1, n - 1) * ((b - a) / (n - 1)), [b]))
    return np.array([a, b], dtype=float)[:n]


def _span(v):
    v = np.asarray(v, dtype=float)
    return float(np.nanmax(v) - np.nanmin(v))


def _viridis(n):
    from matplotlib import colormaps
    cmap = colormaps["viridis"]
    return [cmap(t) for t in (np.linspace(0, 1, n) if n > 1 else [0.0])]


def plot(x, type_col="type", gate_types=("and", "or", "top"), edge_linewidth=1, gate_linewidth=0.8,
         gate_alpha=1, point_radius=None, point_n=100, point_linewidth=0.8, outline_colour="black",
         gate_fill=None, coord_fixed=True, theme_void=True, expand=0.2, normalize=True,
         basic_radius_ratio=0.18, figsize=(7, 6), ax=None, **kwargs):
    """Draw ``x`` (a dict from ``illustrate(..., type="both")`` or ``"all"``).

    Arguments follow R's ``plot()``: ``gate_fill`` is an optional dict of colours
    keyed by ``"top"``, ``"and"``, ``"or"``, ``"basic event"`` (default: the
    viridis palette over the categories present, as ``scale_fill_viridis_d``);
    ``point_radius=None`` sizes basic-event circles at ``basic_radius_ratio``
    times the median gate extent, clamped to [0.03, 0.28]. ``figsize`` and
    ``ax`` are matplotlib extras. Returns the ``Figure``.
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch, Polygon

    if not isinstance(x, dict) or not {"nodes", "edges", "gates"} <= set(x):
        raise ValueError('x must be a dict from illustrate(..., type="both") or type="all" '
                         "with elements nodes, edges, and gates.")
    nodes = x["nodes"].copy()
    edges = x["edges"].copy()
    gates = x["gates"].copy()
    if type_col not in nodes.columns:
        raise ValueError(f'type_col "{type_col}" not found in x["nodes"].')
    if "event" not in nodes.columns:
        raise ValueError('x["nodes"] must contain an "event" column (as returned by illustrate()).')

    if normalize:
        all_x = np.concatenate([nodes["x"].to_numpy(float), gates["x"].to_numpy(float)])
        all_y = np.concatenate([nodes["y"].to_numpy(float), gates["y"].to_numpy(float)])
        x_r, y_r = _span(all_x), _span(all_y)
        x_r = 1 if x_r < 1e-10 else x_r
        y_r = 1 if y_r < 1e-10 else y_r
        fac = 2 / max(x_r, y_r)
        x_mid = (np.nanmin(all_x) + np.nanmax(all_x)) / 2
        y_mid = (np.nanmin(all_y) + np.nanmax(all_y)) / 2
        for df in (nodes, edges, gates):
            df["x"] = (df["x"].astype(float) - x_mid) * fac
            df["y"] = (df["y"].astype(float) - y_mid) * fac

    is_gate = nodes[type_col].astype(str).isin(list(gate_types))
    basic = nodes[~is_gate]
    if len(nodes) <= 6 and expand > 0.1:
        expand = 0.1

    if point_radius is None:
        point_radius = 0.05
        if len(gates) > 0:
            agg = gates.groupby("group", sort=True).agg(
                x0=("x", "min"), x1=("x", "max"), y0=("y", "min"), y1=("y", "max"))
            ext = ((agg["x1"] - agg["x0"]) + (agg["y1"] - agg["y0"])) / 2
            med = float(np.nanmedian(ext.to_numpy(float))) if len(ext) else np.nan
            if np.isfinite(med) and med > 1e-10:
                point_radius = max(0.03, min(0.28, med * basic_radius_ratio))

    theta = _seq(0, 2 * np.pi, point_n)
    circles = [(bx + point_radius * np.cos(theta), by + point_radius * np.sin(theta))
               for bx, by in zip(basic["x"].to_numpy(float), basic["y"].to_numpy(float))]

    present = set(gates["gate"].astype(str)) if len(gates) else set()
    if len(basic):
        present.add("basic event")
    if isinstance(gates.get("gate", pd.Series(dtype=object)).dtype, pd.CategoricalDtype):
        order = [str(c) for c in gates["gate"].cat.categories if str(c) in present]
    else:
        order = [b for b in _BREAKS if b in present] + sorted(present - set(_BREAKS))
    if len(basic) and "basic event" not in order:
        order.append("basic event")
    if gate_fill is None:
        fills = dict(zip(order, _viridis(len(order)))) if order else {}
    else:
        fills = dict(gate_fill)

    def fill_of(cat):
        return fills.get(cat, "#B3B3B3")  # na.value = "gray70"

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    for _, seg in edges.groupby("edge_id", sort=True):
        ax.plot(seg["x"].to_numpy(float), seg["y"].to_numpy(float), color="black",
                linewidth=edge_linewidth * _LW, solid_capstyle="butt", zorder=1)
    for (grp, gt), poly in gates.groupby(["group", "gate"], sort=False, observed=True):
        ax.add_patch(Polygon(np.column_stack([poly["x"].to_numpy(float), poly["y"].to_numpy(float)]),
                             closed=True, facecolor=fill_of(str(gt)), edgecolor=outline_colour,
                             linewidth=gate_linewidth * _LW, alpha=gate_alpha, zorder=2))
    for cx, cy in circles:
        ax.add_patch(Polygon(np.column_stack([cx, cy]), closed=True, facecolor=fill_of("basic event"),
                             edgecolor=outline_colour, linewidth=point_linewidth * _LW, zorder=3))

    # ggplot2 text size is in mm; 1 mm = 72.27 / 25.4 pt
    if len(gates) > 0 and "id" in nodes.columns:
        for _, r in nodes[is_gate].iterrows():
            ax.text(r["x"], r["y"], str(r["event"]), ha="center", va="center", color="white",
                    fontsize=3 * 72.27 / 25.4, zorder=4)
    for _, r in basic.iterrows():
        ax.text(r["x"], r["y"], str(r["event"]), ha="center", va="center", color="black",
                fontsize=2.5 * 72.27 / 25.4, zorder=4)

    xs = [nodes["x"].to_numpy(float), gates["x"].to_numpy(float)] + [c[0] for c in circles]
    ys = [nodes["y"].to_numpy(float), gates["y"].to_numpy(float)] + [c[1] for c in circles]
    all_x, all_y = np.concatenate(xs), np.concatenate(ys)
    ax.set_xlim(np.nanmin(all_x) - expand, np.nanmax(all_x) + expand)
    ax.set_ylim(np.nanmin(all_y) - expand, np.nanmax(all_y) + expand)
    if coord_fixed:
        ax.set_aspect("equal", adjustable="box")
    if theme_void:
        ax.set_axis_off()

    breaks = [b for b in _BREAKS if b in present] or [b for b in order]
    if breaks:
        handles = [Patch(facecolor=fill_of(b), edgecolor=outline_colour, label=_LABELS.get(b, b)) for b in breaks]
        ax.legend(handles=handles, title="Gate", loc="upper center", bbox_to_anchor=(0.5, -0.02),
                  ncol=len(handles), frameon=False)
    fig.tight_layout()
    return fig


def to_png(fig, path, dpi=300):
    """Save a figure from :func:`plot` as a PNG (R's ``ggsave(path, p, dpi = 300)``);
    returns ``path``."""
    fig.savefig(path, dpi=dpi, format="png", bbox_inches="tight")
    return path
