#!/usr/bin/env python3
"""Build the inline-ready predict() / sigma diagram for the Recitation 10 (RSM) deck.

Run from the sigma root:   python3 functions/slides_recitation_11_predict.py

Writes docs-v3/images/slides/recitation-11/predict_diagram.svg (inline-ready:
no XML prolog, <title> first, ids prefixed pre-, each box a <g data-tip>).
Python stdlib only. Replaces the 2025 slide's 1794 x 604 PNG screenshot.
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs-v3" / "images" / "slides" / "recitation-11" / "predict_diagram.svg"
INK, BLUE, TAN, LAV, YEL, ROSE = "#1f1f1f", "#dce8f8", "#f8dcc0", "#e2ddf0", "#f8e2a0", "#fbecec"
FONT = "Lato,'Helvetica Neue',Arial,sans-serif"

# (id, label lines, x, y, w, h, fill, tip)
BOX = [
    ("obs", ["observed", "data"], 20, 250, 190, 120, BLUE,
     "observed data: the rows you fit the model on (here, 320 cookies)"),
    ("mod", ["model"], 290, 270, 170, 80, LAV,
     "model: the fitted lm() object, e.g. yum ~ molasses * ginger + I(molasses^2) + I(ginger^2)"),
    ("new", ["newdata"], 290, 30, 190, 80, BLUE,
     "newdata: a grid of molasses and ginger values you have NOT baked, e.g. 100 x 100 combinations"),
    ("prd", ["predict()"], 560, 30, 190, 80, TAN,
     "predict(model, newdata): evaluates the fitted equation at every row of newdata"),
    ("out", ["prediction"], 840, 30, 200, 80, YEL,
     "prediction: the expected yum at each newdata row; the contour plot draws these"),
    ("sig", ["sigma", "(RMSE)"], 560, 250, 190, 120, ROSE,
     "sigma: root mean squared error of the model, the typical size of a cookie's miss from the prediction"),
]


def arrow(x1, y1, x2, y2, mid):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="3" '
            f'marker-end="url(#{mid})"/>')


def build():
    p = ['<svg class="fig" style="width:100%;height:auto;max-height:430px" viewBox="0 0 1060 400" '
         'role="img" aria-labelledby="pre-t pre-d">',
         '<title id="pre-t">How predict() and sigma come from a fitted model</title>',
         '<desc id="pre-d">Observed data feeds a model. The model and newdata feed predict(), which '
         'produces a prediction. The model also yields sigma, the root mean squared error.</desc>',
         f'<defs><marker id="pre-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
         f'markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{INK}"/></marker></defs>']
    p += [arrow(210, 310, 288, 310, "pre-ah"), arrow(480, 70, 558, 70, "pre-ah"),
          arrow(750, 70, 838, 70, "pre-ah"), arrow(430, 268, 600, 112, "pre-ah"),
          arrow(460, 310, 558, 310, "pre-ah")]
    for i, lines, x, y, w, h, fill, tip in BOX:
        cx, cy = x + w / 2, y + h / 2
        p.append(f'<g id="pre-{i}" data-tip="{html.escape(tip, quote=True)}">'
                 f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{INK}" stroke-width="3"/>')
        n = len(lines)
        for k, t in enumerate(lines):
            ty = cy + 11 + (k - (n - 1) / 2) * 38
            p.append(f'<text x="{cx}" y="{ty}" font-family="{FONT}" font-size="34" font-weight="700" '
                     f'text-anchor="middle" fill="{INK}">{html.escape(t)}</text>')
        p.append('</g>')
    p.append('</svg>')
    return "\n".join(p)


if __name__ == "__main__":
    OUT.write_text(build() + "\n", encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT))
