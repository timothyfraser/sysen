# slides_recitation_9_symbols.py
# Draws the fault tree symbols table (Table 4.1 in the 2025 deck) as an
# inline SVG: seven symbols, each with its name and a data-tip.
# Standard library only. Usage:
#   python3 functions/slides_recitation_9_symbols.py sym > symbols.svg
# The argument is an id prefix (ids are document-global).

import sys

# Palette (sigma slide tokens, SLIDES.md section 4)
INK = "#2a1414"
RED_DARK = "#8f1414"
RED_TINT = "#fbecec"
RED_TINT2 = "#f2dada"
WHITE = "#ffffff"

CELL_W, CELL_H = 220, 140
CODE_URL = "https://github.com/timothyfraser/sysen/blob/main/functions/slides_recitation_9_symbols.py"
SY = 58  # y centre of the symbol inside a cell


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def or_gate(cx, cy):
    t, b = cy - 34, cy + 30
    return (f'<line x1="{cx}" y1="{t-14}" x2="{cx}" y2="{t+4}"/>'
            f'<path d="M{cx-34} {b} Q{cx-34} {t+16} {cx} {t} Q{cx+34} {t+16} {cx+34} {b} '
            f'Q{cx} {b-18} {cx-34} {b} Z" fill="{RED_TINT}"/>'
            f'<line x1="{cx-16}" y1="{b-6}" x2="{cx-16}" y2="{b+14}"/><line x1="{cx+16}" y1="{b-6}" x2="{cx+16}" y2="{b+14}"/>')


def and_gate(cx, cy):
    t, b = cy - 34, cy + 30
    return (f'<line x1="{cx}" y1="{t-14}" x2="{cx}" y2="{t}"/>'
            f'<path d="M{cx-34} {b} L{cx-34} {t+34} A34 34 0 0 1 {cx+34} {t+34} L{cx+34} {b} Z" fill="{RED_TINT2}"/>'
            f'<line x1="{cx-16}" y1="{b}" x2="{cx-16}" y2="{b+14}"/><line x1="{cx+16}" y1="{b}" x2="{cx+16}" y2="{b+14}"/>')


def basic(cx, cy):
    return f'<circle cx="{cx}" cy="{cy}" r="34" fill="{WHITE}" stroke="{RED_DARK}" stroke-width="3"/>'


def undeveloped(cx, cy):
    return f'<path d="M{cx} {cy-36} L{cx+52} {cy} L{cx} {cy+36} L{cx-52} {cy} Z" fill="{WHITE}"/>'


def comment(cx, cy):
    return f'<rect x="{cx-62}" y="{cy-30}" width="124" height="60" fill="{WHITE}"/>'


def transfer_out(cx, cy):
    # triangle, with the line entering from the side
    return (f'<path d="M{cx} {cy-34} L{cx+38} {cy+30} L{cx-38} {cy+30} Z" fill="{RED_TINT}"/>'
            f'<line x1="{cx+19}" y1="{cy-2}" x2="{cx+62}" y2="{cy-2}"/>')


def transfer_in(cx, cy):
    # triangle, with the line entering at the apex
    return (f'<line x1="{cx}" y1="{cy-52}" x2="{cx}" y2="{cy-34}"/>'
            f'<path d="M{cx} {cy-34} L{cx+38} {cy+30} L{cx-38} {cy+30} Z" fill="{RED_TINT}"/>')


# (key, name, drawer, tip)
SYMBOLS = [
    ("or", "OR gate", or_gate,
     "The output event occurs if at least one of the input events occurs."),
    ("and", "AND gate", and_gate,
     "The output event occurs only if all of the input events occur."),
    ("basic", "Basic event", basic,
     "A basic initiating fault (failure event) that needs no further development."),
    ("undev", "Undeveloped event", undeveloped,
     "An event not developed further, for lack of information or because it is not of sufficient consequence."),
    ("comment", "Comment rectangle", comment,
     "Supplementary information: a description of the event above it."),
    ("tout", "Transfer out", transfer_out,
     "The tree is developed further at the occurrence of the matching transfer-in symbol."),
    ("tin", "Transfer in", transfer_in,
     "This part of the tree is developed elsewhere, where the matching transfer-out symbol is."),
]


def build(prefix):
    cols, rows = 3, 3
    w, h = cols * CELL_W, rows * CELL_H
    out = [f'<svg class="fig" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{prefix}-t {prefix}-d">',
           f'<title id="{prefix}-t">Fault tree symbols</title>',
           f'<desc id="{prefix}-d">' + esc(" ".join(f"{n}: {t}" for _, n, _, t in SYMBOLS)) + "</desc>"]
    for i, (key, name, draw, tip) in enumerate(SYMBOLS):
        x0, y0 = (i % cols) * CELL_W, (i // cols) * CELL_H
        cx = x0 + CELL_W // 2
        out.append(f'<g id="{prefix}-{key}" tabindex="0" data-tip-title="{esc(name)}" data-tip="{esc(tip)}">'
                   f'<rect x="{x0+6}" y="{y0+6}" width="{CELL_W-12}" height="{CELL_H-12}" rx="10" '
                   f'fill="{WHITE}" stroke="{RED_TINT2}" stroke-width="2"/>'
                   f'<g stroke="{INK}" stroke-width="2.5" fill="none">{draw(cx, y0 + SY)}</g>'
                   f'<text x="{cx}" y="{y0+CELL_H-16}" font-size="21" text-anchor="middle" fill="{INK}">{esc(name)}</text></g>')
    # cells eight and nine: the hint
    x0, y0 = CELL_W, 2 * CELL_H
    out.append(f'<text x="{x0+CELL_W}" y="{y0+CELL_H//2+8}" font-size="24" font-style="italic" '
               f'text-anchor="middle" fill="{RED_DARK}">Hover a symbol</text>')
    out.append(f'<a href="{CODE_URL}"><text x="{x0+CELL_W}" y="{y0+CELL_H//2+44}" font-size="22" '
               f'text-decoration="underline" text-anchor="middle" fill="{RED_DARK}">code</text></a>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    print(build(sys.argv[1] if len(sys.argv) > 1 else "sym"))
