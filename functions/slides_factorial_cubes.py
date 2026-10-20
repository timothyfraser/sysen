# slides_factorial_cubes.py -------------------------------------------------
# Feeds: the factorial-design decks (Lesson 13 / Workshop 13): every cube
#   diagram of a 2^3 design. Python standard library only.
# Data: Box, Hunter & Hunter pilot plant 2^3 (T, C, K; yields in standard
#   order 60, 72, 54, 68, 52, 83, 45, 80) and a generic 2^3 design in A, B, C
#   (y1..y8 = 33, 63, 41, 57, 57, 51, 59, 53).
# Run from the top of the repo:  python3 functions/slides_factorial_cubes.py
# Writes (docs-v3/images/slides/factorial/):
#   cube_yields.svg, cube_T.svg, cube_C.svg, cube_K.svg, cube_TK.svg,
#   cube_three_way.svg, cube_contrast_{A,B,C,AB,AC,BC,ABC}.svg,
#   cube_full.svg, cube_half.svg
# Geometry (same for every cube): first factor left -> right, second factor
#   front -> back, third factor bottom -> top. Pilot: T, C, K. Generic: A, B, C.
import os

OUT = "docs-v3/images/slides/factorial"

RED, INK, WARM = "#B31B1B", "#1f1f1f", "#f3f1ee"
TAN_SOFT, BLUE_MID, BLUE_SOFT = "#f8dcc0", "#3880c0", "#dce8f8"
LAV, ROSE, NAVY, ROSE_INK = "#b0a8d0", "#d08080", "#302050", "#580808"
FONT = 'font-family="Lato, \'Helvetica Neue\', Arial, sans-serif"'
NUM = 'font-weight="700" style="font-variant-numeric:tabular-nums"'

W, H = 720, 570          # viewBox (shown at ~420 px wide: scale 0.58, so text >= 38)
X0, Y0 = 150, 410        # front-bottom-left corner
SX, SY = 280, 230        # first-factor width, third-factor height
DX, DY = 150, 110        # second-factor (depth) offset

PILOT_Y = [60, 72, 54, 68, 52, 83, 45, 80]
GENERIC_Y = [33, 63, 41, 57, 57, 51, 59, 53]


def pt(a, b, c):
    """Screen point of corner (a, b, c), each 0 (low) or 1 (high)."""
    return (X0 + a * SX + b * DX, Y0 - c * SY - b * DY)


def corners():
    """Corners in standard order: first factor fastest."""
    return [(i & 1, (i >> 1) & 1, (i >> 2) & 1) for i in range(8)]


EDGES = []
for i, (a, b, c) in enumerate(corners()):
    for axis in range(3):
        if (a, b, c)[axis] == 0:
            hi = [a, b, c]
            hi[axis] = 1
            EDGES.append(((a, b, c), tuple(hi), axis))

HIDDEN = (0, 1, 0)       # the back-bottom-left corner sits behind the cube


def face(axis, level):
    """Polygon of the face where factor `axis` is at `level`."""
    others = [k for k in range(3) if k != axis]
    pts = []
    for u, v in [(0, 0), (1, 0), (1, 1), (0, 1)]:
        p = [0, 0, 0]
        p[axis], p[others[0]], p[others[1]] = level, u, v
        pts.append(pt(*p))
    return " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)


class Fig:
    def __init__(self, name, title, height=H):
        self.name, self.title, self.h = name, title, height
        self.defs, self.body = [], []

    def add(self, s):
        self.body.append(s)

    def arrow_marker(self):
        mid = f"{self.name}-arr"
        self.defs.append(
            f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" '
            f'markerWidth="3.2" markerHeight="3.2" orient="auto">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker>')
        return mid

    def write(self):
        tid = f"{self.name}-title"
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {self.h}" '
               f'width="{W}" height="{self.h}" role="img" aria-labelledby="{tid}">',
               f'<title id="{tid}">{self.title}</title>',
               f'<rect width="{W}" height="{self.h}" fill="#ffffff"/>']
        if self.defs:
            out.append("<defs>" + "".join(self.defs) + "</defs>")
        out += self.body
        out.append("</svg>")
        path = os.path.join(OUT, self.name + ".svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out) + "\n")
        print("wrote", path)


def text(x, y, s, size=30, fill=INK, anchor="middle", bold=False, num=False, rot=None):
    w = NUM if num else ('font-weight="700"' if bold else 'font-weight="400"')
    r = f' transform="rotate({rot} {x:.0f} {y:.0f})"' if rot is not None else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" {FONT} font-size="{size}" {w} '
            f'text-anchor="{anchor}" dominant-baseline="central" fill="{fill}"{r}>{s}</text>')


def draw_edges(fig, red_axes=(), arrow=None, r=40):
    """All twelve edges; edges along a red axis are carnelian arrows low -> high."""
    for lo, hi, axis in EDGES:
        (x1, y1), (x2, y2) = pt(*lo), pt(*hi)
        hidden = HIDDEN in (lo, hi)
        if axis in red_axes:
            dx, dy = x2 - x1, y2 - y1
            n = (dx * dx + dy * dy) ** 0.5
            ux, uy = dx / n, dy / n
            gap = r + 4
            fig.add(f'<line x1="{x1 + ux * gap:.1f}" y1="{y1 + uy * gap:.1f}" '
                    f'x2="{x2 - ux * (gap + 4):.1f}" y2="{y2 - uy * (gap + 4):.1f}" '
                    f'stroke="{RED}" stroke-width="7" stroke-linecap="round" '
                    f'marker-end="url(#{arrow})"/>')
        else:
            dash = ' stroke-dasharray="10 8"' if hidden else ""
            fig.add(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                    f'stroke="{INK}" stroke-width="{4 if hidden else 5}"{dash} '
                    f'stroke-opacity="{0.55 if hidden else 1}"/>')


def draw_values(fig, values, r=40, size=38, fill="#ffffff", ink=INK, ring=INK, keep=None):
    for i, (a, b, c) in enumerate(corners()):
        x, y = pt(a, b, c)
        on = keep is None or i in keep
        f, rg, ik = (fill, ring, ink) if on else ("#ffffff", "#b8b0b0", "#a09898")
        fig.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{f}" stroke="{rg}" '
                f'stroke-width="4"/>' + text(x, y + 1, values[i], size=size, fill=ik, num=True))


def draw_axes(fig, names, lows, highs, size=38, first_left=False):
    """Axis titles and level labels: first factor below, second along the
    right depth edge, third at the left. `size` is the label font size; the
    contrast cubes, drawn small in a 4+3 grid, pass a larger one.
    `first_left` puts the first factor's title at the left end of the
    bottom-front edge, beside its low mark, instead of centred under the
    edge (the contrast cubes carry their own name centred below)."""
    n1, n2, n3 = names
    # first factor: under the front-bottom edge
    y = Y0 + 66
    fig.add(text(pt(0, 0, 0)[0], y, lows[0], size=size, num=True))
    fig.add(text(pt(1, 0, 0)[0], y, highs[0], size=size, num=True))
    if first_left:
        fig.add(text(pt(0, 0, 0)[0] - 40, y, n1, size=size, fill=RED, bold=True, anchor="end"))
    else:
        fig.add(text((pt(0, 0, 0)[0] + pt(1, 0, 0)[0]) / 2, Y0 + 118, n1, size=size,
                     fill=RED, bold=True))
    # second factor: beside the bottom-right depth edge
    (xa, ya), (xb, yb) = pt(1, 0, 0), pt(1, 1, 0)
    fig.add(text(xa + 52, ya + 8, lows[1], size=size, anchor="start", num=True))
    fig.add(text(xb + 52, yb, highs[1], size=size, anchor="start", num=True))
    fig.add(text((xa + xb) / 2 + 65, (ya + yb) / 2 + 89, n2, size=size, fill=RED,
                 bold=True, anchor="middle", rot=-36))
    # third factor: left of the front-left vertical edge
    (xl, yl), (xh, yh) = pt(0, 0, 0), pt(0, 0, 1)
    fig.add(text(xl - 52, yl, lows[2], size=size, anchor="end", num=True))
    fig.add(text(xh - 52, yh, highs[2], size=size, anchor="end", num=True))
    fig.add(text(36, (yl + yh) / 2, n3, size=size, fill=RED, bold=True, rot=-90))


PILOT_AXES = (("Temperature T", "Concentration C", "Catalyst K"),
              ("160", "20", "A"), ("180", "40", "B"))
GEN_AXES = (("A", "B", "C"), ("&#8722;", "&#8722;", "&#8722;"), ("+", "+", "+"))


def tint(fig, axis, level, colour, opacity=0.9):
    fig.add(f'<polygon points="{face(axis, level)}" fill="{colour}" fill-opacity="{opacity}"/>')


def pilot_values():
    return [str(v) for v in PILOT_Y]


def cube_yields():
    f = Fig("cube_yields", "Pilot plant 2 cubed design: yields at the eight corners of the "
            "Temperature by Concentration by Catalyst cube")
    draw_axes(f, *PILOT_AXES)
    draw_edges(f)
    draw_values(f, pilot_values(), r=44, size=42)
    f.write()


def cube_main(letter, axis, full):
    f = Fig(f"cube_{letter}", f"Main effect of {full}: the four {letter} edges run from low to "
            f"high {letter}; the high face is blue, the low face tan; yields at the corners")
    arr = f.arrow_marker()
    if axis == 1:  # depth faces overlap: back face first
        tint(f, 1, 1, BLUE_SOFT)
        tint(f, 1, 0, TAN_SOFT, 0.75)
    else:
        tint(f, axis, 0, TAN_SOFT)
        tint(f, axis, 1, BLUE_SOFT)
    draw_axes(f, *PILOT_AXES)
    draw_edges(f, red_axes=(axis,), arrow=arr)
    draw_values(f, pilot_values())
    f.write()


def face_label(f, level, label, colour):
    pts = [pt(a, b, level) for a in (0, 1) for b in (0, 1)]
    cx = sum(p[0] for p in pts) / 4
    cy = sum(p[1] for p in pts) / 4
    f.add(text(cx, cy + 6, label, size=36, fill=colour, bold=True))


def cube_tk():
    f = Fig("cube_TK", "Two-way interaction T by K: the Catalyst A face (tan) and Catalyst B "
            "face (lavender) each carry two Temperature edges, low to high; yields at the corners")
    arr = f.arrow_marker()
    tint(f, 2, 0, TAN_SOFT)
    tint(f, 2, 1, LAV, 0.8)
    draw_axes(f, *PILOT_AXES)
    draw_edges(f, red_axes=(0,), arrow=arr)
    draw_values(f, pilot_values())
    f.write()


def cube_three_way():
    f = Fig("cube_three_way", "Three-way interaction: the Temperature by Concentration face at "
            "K = A (tan) and at K = B (lavender); yields at the corners")
    tint(f, 2, 0, TAN_SOFT)
    tint(f, 2, 1, LAV, 0.8)
    draw_axes(f, *PILOT_AXES)
    draw_edges(f)
    face_label(f, 0, "K = A", ROSE_INK)
    face_label(f, 1, "K = B", NAVY)
    draw_values(f, pilot_values())
    f.write()


def cube_contrast(label):
    idx = {"A": 0, "B": 1, "C": 2}
    f = Fig(f"cube_contrast_{label}", f"Contrast {label}: corners with a plus sign are filled, "
            f"corners with a minus sign are open rings", height=H + 50)
    draw_axes(f, *GEN_AXES, size=68, first_left=True)
    draw_edges(f)
    for a, b, c in corners():
        s = 1
        for ch in label:
            s *= 1 if (a, b, c)[idx[ch]] else -1
        x, y = pt(a, b, c)
        fill = INK if s > 0 else "#ffffff"
        f.add(f'<circle cx="{x}" cy="{y}" r="32" fill="{fill}" stroke="{INK}" stroke-width="5"/>')
    f.add(text(W / 2, Y0 + 150, label, size=80, fill=RED, bold=True))
    f.write()


def cube_full():
    f = Fig("cube_full", "Full 2 cubed design in A, B and C: all eight runs, y1 to y8 = "
            "33, 63, 41, 57, 57, 51, 59, 53")
    draw_axes(f, *GEN_AXES)
    draw_edges(f)
    draw_values(f, [str(v) for v in GENERIC_Y], r=40, size=38, fill=ROSE, ink=ROSE_INK,
                ring=ROSE_INK)
    f.write()


def cube_half():
    keep = [i for i, (a, b, c) in enumerate(corners())
            if (1 if a else -1) * (1 if b else -1) * (1 if c else -1) == 1]
    vals = ", ".join(f"y{i + 1} = {GENERIC_Y[i]}" for i in keep)
    f = Fig("cube_half", f"Half fraction with ABC = +: four runs kept ({vals}); the other "
            "four are dimmed")
    draw_axes(f, *GEN_AXES)
    draw_edges(f)
    vals_txt = [str(v) for v in GENERIC_Y]
    # dimmed runs first, kept runs on top and larger
    draw_values(f, vals_txt, r=36, size=34, keep=[])
    for i in keep:
        x, y = pt(*corners()[i])
        f.add(f'<circle cx="{x}" cy="{y}" r="46" fill="{ROSE}" stroke="{ROSE_INK}" '
              f'stroke-width="4"/>' + text(x, y + 1, vals_txt[i], size=42, fill=ROSE_INK, num=True))
    f.write()


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    cube_yields()
    cube_main("T", 0, "Temperature T")
    cube_main("C", 1, "Concentration C")
    cube_main("K", 2, "Catalyst K")
    cube_tk()
    cube_three_way()
    for lab in ["A", "B", "C", "AB", "AC", "BC", "ABC"]:
        cube_contrast(lab)
    cube_full()
    cube_half()
