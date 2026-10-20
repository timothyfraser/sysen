#!/usr/bin/env python3
"""Build the four inline-ready Latin-square SVGs for the lesson 12b deck.

Run from the sigma root:   python3 functions/slides_latin_squares.py

Writes docs-v3/images/slides/latin/{latin_4x4,graeco_4x4,youden_7x7,martindale_cell}.svg

Data are READ, never retyped:
  workshops/anova_latin_square.csv   driver, car, additive, y
  workshops/anova_youden.csv         block, treatment, position, wear
  workshops/anova_martindale.csv     replicate, cycle, position, emery, treatment, holder, wear
  docs-v3/slides/42_slides_lesson_12b.html   the Graeco-Latin layout (no Graeco CSV exists)

Every SVG is written to be pasted INLINE into the deck HTML: no XML prolog, no
DOCTYPE, <title> first, ids prefixed per file (lat-, gre-, you-, mar-), and each
data cell is a <g data-tip="..."> so the deck's tooltip engine can target it.
Python stdlib only.
"""
import csv
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs-v3" / "images" / "slides" / "latin"
SLIDE = ROOT / "docs-v3" / "slides" / "42_slides_lesson_12b.html"

# palette
CARNELIAN = "#B31B1B"
INK = "#1f1f1f"
BLUE = "#dce8f8"
TAN = "#f8dcc0"
BERRY = "#e8c8da"
YELLOW = "#f8e2a0"
LAVENDER = "#b0a8d0"
NAVY = "#302050"
GRAY = "#f3f1ee"
DARKRED = "#580808"
FONT = "Lato,'Helvetica Neue',Arial,sans-serif"

ADD_FILL = {"A": BLUE, "B": TAN, "C": BERRY, "D": YELLOW}
GREEK = {"alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ"}
GREEK_ORDER = ["alpha", "beta", "gamma", "delta"]
ENT = {"&alpha;": "alpha", "&beta;": "beta", "&gamma;": "gamma", "&delta;": "delta"}


def esc(s):
    return html.escape(str(s), quote=True)


def read_csv(name):
    with open(ROOT / "workshops" / name, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def svg_open(prefix, w, h, title, desc):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
        f'aria-labelledby="{prefix}-t {prefix}-d" font-family="{FONT}">\n'
        f'<title id="{prefix}-t">{esc(title)}</title>\n'
        f'<desc id="{prefix}-d">{esc(desc)}</desc>\n'
    )


def txt(x, y, s, size=22, fill=INK, anchor="middle", weight="400", extra=""):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}"{extra}>{esc(s)}</text>'
    )


def legend_additives(prefix, y, x0=14):
    """One line: 'Additive' + four swatches A-D."""
    out = [f'<g id="{prefix}-legend">']
    out.append(txt(x0, y + 8, "Fill = additive", 22, INK, "start", "700"))
    x = x0 + 170
    for a in "ABCD":
        out.append(
            f'<rect x="{x}" y="{y - 16}" width="30" height="30" fill="{ADD_FILL[a]}" '
            f'stroke="{INK}" stroke-width="2"/>'
        )
        out.append(txt(x + 15, y + 8, a, 22, INK, "middle", "700"))
        x += 44
    out.append("</g>")
    return "\n".join(out)


# ---------------------------------------------------------------- latin 4x4
def build_latin():
    rows = read_csv("anova_latin_square.csv")
    drivers = list(dict.fromkeys(r["driver"] for r in rows))
    cars = list(dict.fromkeys(r["car"] for r in rows))
    cell = {(r["driver"], r["car"]): r for r in rows}
    W, X0, CW, CH, Y0 = 560, 96, 116, 88, 54
    H = Y0 + CH * len(drivers) + 56
    p = "lat"
    o = [svg_open(p, W, H, "Latin square of additives",
                  "A 4 by 4 Latin square: drivers I to IV by cars 1 to 4, each cell showing the "
                  "additive letter A to D and the measured pollution value. Each additive appears "
                  "once in every row and every column.")]
    # headers
    o.append(txt(X0 - 12, Y0 - 16, "Driver", 22, INK, "end", "700"))
    for j, c in enumerate(cars):
        o.append(txt(X0 + j * CW + CW / 2, Y0 - 16, f"Car {c}", 22, INK, "middle", "700"))
    for i, d in enumerate(drivers):
        y = Y0 + i * CH
        o.append(txt(X0 - 12, y + CH / 2 + 8, d, 24, INK, "end", "700"))
        for j, c in enumerate(cars):
            r = cell[(d, c)]
            x = X0 + j * CW
            tip = f"Driver {d} · Car {c} · Additive {r['additive']} · {r['y']} (pollution)"
            o.append(
                f'<g id="{p}-{d}-{c}" data-tip="{esc(tip)}">'
                f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="{ADD_FILL[r["additive"]]}" '
                f'stroke="{INK}" stroke-width="2"/>'
                + txt(x + CW / 2, y + 44, r["additive"], 40, INK, "middle", "700")
                + txt(x + CW / 2, y + 76, r["y"], 24, INK, "middle", "400")
                + "</g>"
            )
    o.append(legend_additives(p, Y0 + CH * len(drivers) + 36))
    o.append("</svg>\n")
    return "\n".join(o)


# --------------------------------------------------------------- graeco 4x4
def parse_graeco():
    """Read the Graeco-Latin layout out of the lesson 12b deck table."""
    src = SLIDE.read_text(encoding="utf-8")
    i = src.find("Graeco-Latin Squares</div>")
    if i < 0:
        sys.exit("FAIL slides_latin_squares: Graeco-Latin block not found in " + str(SLIDE))
    block = src[i:i + 4000]
    layout = []
    for tr in re.findall(r"<tr>(.*?)</tr>", block, flags=re.S):
        th = re.search(r"<th>([IV]+)</th>", tr)
        if not th:
            continue
        cells = re.findall(r"<em>([A-D])(&\w+;)</em>", tr)
        if len(cells) != 4 or any(g not in ENT for _, g in cells):
            sys.exit(f"FAIL slides_latin_squares: bad Graeco row {th.group(1)}")
        layout.append((th.group(1), [(a, ENT[g]) for a, g in cells]))
    if len(layout) != 4:
        sys.exit(f"FAIL slides_latin_squares: expected 4 Graeco rows, got {len(layout)}")
    return layout


def badge(cx, cy, g, prefix, r=16):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{NAVY}" stroke="{NAVY}" stroke-width="2"/>'
        + txt(cx, cy + 8, GREEK[g], 22, "#ffffff", "middle", "700")
    )


def build_graeco():
    layout = parse_graeco()
    W, X0, CW, CH, Y0 = 560, 96, 116, 88, 54
    H = Y0 + CH * 4 + 96
    p = "gre"
    o = [svg_open(p, W, H, "Graeco-Latin square of additives and days",
                  "A 4 by 4 Graeco-Latin square: drivers I to IV by cars 1 to 4. The large letter A to D "
                  "is the additive; the small round badge with a Greek letter alpha to delta is the day of "
                  "the test. Every additive and every day appears once in every row and column.")]
    o.append(txt(X0 - 12, Y0 - 16, "Driver", 22, INK, "end", "700"))
    for j in range(4):
        o.append(txt(X0 + j * CW + CW / 2, Y0 - 16, f"Car {j + 1}", 22, INK, "middle", "700"))
    for i, (d, cells) in enumerate(layout):
        y = Y0 + i * CH
        o.append(txt(X0 - 12, y + CH / 2 + 8, d, 24, INK, "end", "700"))
        for j, (a, g) in enumerate(cells):
            x = X0 + j * CW
            tip = f"Driver {d} · Car {j + 1} · Additive {a} · Day {GREEK[g]} ({g})"
            o.append(
                f'<g id="{p}-{d}-{j + 1}" data-tip="{esc(tip)}">'
                f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="{ADD_FILL[a]}" '
                f'stroke="{INK}" stroke-width="2"/>'
                + txt(x + 46, y + CH / 2 + 15, a, 40, INK, "middle", "700")
                + badge(x + CW - 24, y + 24, g, p)
                + "</g>"
            )
    ly = Y0 + CH * 4 + 36
    o.append(legend_additives(p, ly))
    # second legend line: badge = day
    o.append(f'<g id="{p}-legend2">'
             + badge(26, ly + 42, "alpha", p, 16)
             + txt(52, ly + 50, "Badge = day of test (α β γ δ)", 22, INK, "start")
             + "</g>")
    o.append("</svg>\n")
    return "\n".join(o)


# ---------------------------------------------------------------- youden 7x7
def build_youden():
    rows = read_csv("anova_youden.csv")
    blocks = sorted({int(r["block"]) for r in rows})
    treats = sorted({r["treatment"] for r in rows})
    cell = {(int(r["block"]), r["treatment"]): r for r in rows}
    W, X0, CW, CH, Y0 = 560, 98, 66, 62, 56
    H = Y0 + CH * len(blocks) + 104
    p = "you"
    o = [svg_open(p, W, H, "Youden square of seven treatments",
                  "A 7 by 7 Youden square: blocks 1 to 7 by treatments A to G. Each block holds 4 of the "
                  "7 treatments; each filled cell shows a Greek letter for the position in the block and "
                  "the wear value. Empty cells are hatched.")]
    o.append(
        f'<defs><pattern id="{p}-hatch" width="10" height="10" patternUnits="userSpaceOnUse" '
        f'patternTransform="rotate(45)"><rect width="10" height="10" fill="{GRAY}"/>'
        f'<line x1="0" y1="0" x2="0" y2="10" stroke="#c9c5c0" stroke-width="2"/></pattern></defs>'
    )
    o.append(txt(X0 - 10, Y0 - 16, "Block", 22, INK, "end", "700"))
    for j, t in enumerate(treats):
        o.append(txt(X0 + j * CW + CW / 2, Y0 - 16, t, 24, INK, "middle", "700"))
    for i, b in enumerate(blocks):
        y = Y0 + i * CH
        o.append(txt(X0 - 10, y + CH / 2 + 8, str(b), 24, INK, "end", "700"))
        for j, t in enumerate(treats):
            x = X0 + j * CW
            r = cell.get((b, t))
            if r is None:
                o.append(
                    f'<rect id="{p}-e{b}{t}" x="{x}" y="{y}" width="{CW}" height="{CH}" '
                    f'fill="url(#{p}-hatch)" stroke="{INK}" stroke-width="2"/>'
                )
                continue
            g = r["position"]
            tip = f"Block {b} · Treatment {t} · Position {GREEK[g]} · wear {r['wear']}"
            o.append(
                f'<g id="{p}-{b}{t}" data-tip="{esc(tip)}">'
                f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="{BLUE}" '
                f'stroke="{INK}" stroke-width="2"/>'
                f'<circle cx="{x + 18}" cy="{y + 18}" r="14" fill="{LAVENDER}" stroke="{NAVY}" stroke-width="2"/>'
                + txt(x + 18, y + 26, GREEK[g], 22, NAVY, "middle", "700")
                + txt(x + CW / 2, y + CH - 8, r["wear"], 22, INK, "middle", "400")
                + "</g>"
            )
    ly = Y0 + CH * len(blocks) + 34
    o.append(f'<g id="{p}-legend">'
             + txt(14, ly, "Each block holds 4 of the 7 treatments;", 22, INK, "start")
             + txt(14, ly + 30, "every pair of treatments shares a block twice.", 22, INK, "start")
             + txt(14, ly + 60, "Badge = position in block · hatched = absent.", 22, INK, "start")
             + "</g>")
    o.append("</svg>\n")
    return "\n".join(o)


# -------------------------------------------------------- martindale one cell
def arrow(x1, y1, x2, y2, p):
    return (
        f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{CARNELIAN}" stroke-width="3" '
        f'stroke-linecap="round" marker-end="url(#{p}-head)"/>'
    )


def build_martindale():
    r = read_csv("anova_martindale.csv")[0]  # first cell: replicate I, cycle C1, P1
    g = GREEK[r["emery"]]
    p = "mar"
    W, H = 560, 410
    cx0, cy0, cw, ch = 150, 144, 260, 176
    tip = (f"Replicate {r['replicate']} · Cycle {r['cycle']} · Position {r['position']} · "
           f"emery paper {g} · treatment {r['treatment']} · holder {r['holder']} · "
           f"wear {r['wear']} mg")
    # x anchors for the three symbols on the first line
    ax, tx, hx = 214, 284, 322
    o = [svg_open(p, W, H, "Anatomy of one Martindale cell",
                  f"One cell of the Martindale design, read as {g} {r['treatment']}{r['holder']} over "
                  f"{r['wear']}: emery paper {g}, treatment {r['treatment']}, holder {r['holder']}, "
                  f"wear {r['wear']} milligrams.")]
    o.append(
        f'<defs><marker id="{p}-head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" '
        f'markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{CARNELIAN}"/>'
        f'</marker></defs>'
    )
    o.append(
        f'<g id="{p}-cell" data-tip="{esc(tip)}">'
        f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>'
        + txt(ax, cy0 + 74, g, 56, NAVY, "middle", "700")
        + txt(tx, cy0 + 74, r["treatment"], 56, INK, "middle", "700")
        + txt(hx, cy0 + 74, r["holder"], 56, DARKRED, "middle", "700")
        + f'<line x1="{cx0 + 20}" y1="{cy0 + 92}" x2="{cx0 + cw - 20}" y2="{cy0 + 92}" stroke="{INK}" stroke-width="2"/>'
        + txt(cx0 + cw / 2, cy0 + 156, r["wear"], 60, INK, "middle", "700")
        + "</g>"
    )
    # top callouts
    o.append(txt(100, 44, f"emery paper {g}", 24, NAVY, "middle", "700"))
    o.append(arrow(112, 58, ax - 4, cy0 + 22, p))
    o.append(txt(290, 44, f"treatment {r['treatment']}", 24, INK, "middle", "700"))
    o.append(arrow(tx, 58, tx, cy0 + 22, p))
    o.append(txt(452, 44, f"holder {r['holder']}", 24, DARKRED, "middle", "700"))
    o.append(arrow(442, 58, hx + 6, cy0 + 22, p))
    # bottom callout
    o.append(txt(cx0 + cw / 2, 394, f"wear (mg) {r['wear']}", 24, INK, "middle", "700"))
    o.append(arrow(cx0 + cw / 2, 360, cx0 + cw / 2, cy0 + ch + 8, p))
    o.append("</svg>\n")
    return "\n".join(o)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    builds = {
        "latin_4x4.svg": build_latin,
        "graeco_4x4.svg": build_graeco,
        "youden_7x7.svg": build_youden,
        "martindale_cell.svg": build_martindale,
    }
    for name, fn in builds.items():
        s = fn()
        assert "<?xml" not in s and "<!DOCTYPE" not in s
        (OUT / name).write_text(s, encoding="utf-8")
        print(f"OK slides_latin_squares: wrote {name} ({s.count('data-tip=')} data-tip)")


if __name__ == "__main__":
    main()
