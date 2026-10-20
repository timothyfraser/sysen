# slides_recitation_9_tree.py
# Draws the textbook fault tree (gates G0-G6, basic events 1-8) used in
# Workshop 13 as an inline SVG with a data-tip on every gate and event.
# Standard library only. Usage:
#   python3 functions/slides_recitation_9_tree.py ft5 > tree.svg
# The argument is an id prefix: ids are document-global, so each copy of the
# tree on a deck needs its own prefix.
#
# The tree (read it top-down, as MOCUS does):
#   G0 = OR(1, G1, 2)      G1 = OR(G2, G3)
#   G2 = AND(G4, G5)       G3 = OR(3, G6)
#   G4 = OR(4, 5)          G5 = OR(6, 7)          G6 = OR(6, 8)
# Minimal cut sets: {1} {2} {3} {6} {8} {4,7} {5,7}

import sys

# Palette (sigma slide tokens, SLIDES.md section 4)
INK = "#2a1414"
RED_DARK = "#8f1414"
RED_TINT = "#fbecec"
RED_TINT2 = "#f2dada"
WHITE = "#ffffff"

BOX_W, BOX_H = 92, 44
GATE_H = 40
EV_R = 24

# name: (kind, x centre, y top, children, tip title, tip text)
GATES = {
    "G0": ("or", 300, 8, ["1", "G1", "2"], "G0 · TOP event · OR gate",
           "The system fails if event 1, event 2 or gate G1 occurs."),
    "G1": ("or", 300, 152, ["G2", "G3"], "G1 · OR gate",
           "Fails if G2 or G3 fails."),
    "G2": ("and", 170, 296, ["G4", "G5"], "G2 · AND gate",
           "Fails only if BOTH G4 and G5 fail: an AND gate adds events to a cut set."),
    "G3": ("or", 440, 296, ["3", "G6"], "G3 · OR gate",
           "Fails if event 3 or G6 occurs: an OR gate adds cut sets."),
    "G4": ("or", 90, 440, ["4", "5"], "G4 · OR gate", "Fails if event 4 or event 5 occurs."),
    "G5": ("or", 250, 440, ["6a", "7"], "G5 · OR gate", "Fails if event 6 or event 7 occurs."),
    "G6": ("or", 500, 440, ["6b", "8"], "G6 · OR gate", "Fails if event 6 or event 8 occurs."),
}

# event id: (label, x centre, y centre, tip title, tip text)
EVENTS = {
    "1": ("1", 180, 174, "Event 1 · basic event",
          "On its own it fails G0: the minimal cut set {1}, a single point of failure."),
    "2": ("2", 420, 174, "Event 2 · basic event",
          "On its own it fails G0: the minimal cut set {2}, a single point of failure."),
    "3": ("3", 380, 462, "Event 3 · basic event",
          "Under G3, G1 and G0 (all OR gates): alone it is the minimal cut set {3}."),
    "4": ("4", 50, 606, "Event 4 · basic event",
          "Under G4, then the AND gate G2: it needs G5 too. Minimal cut set {4, 7}."),
    "5": ("5", 130, 606, "Event 5 · basic event",
          "Under G4, then the AND gate G2: it needs G5 too. Minimal cut set {5, 7}."),
    "6a": ("6", 210, 606, "Event 6 · repeated basic event",
           "Also appears under G6. There it alone fails the TOP event, so {6} is minimal and absorbs {4, 6} and {5, 6}."),
    "7": ("7", 290, 606, "Event 7 · basic event",
          "Under G5, then the AND gate G2: minimal cut sets {4, 7} and {5, 7}."),
    "6b": ("6", 460, 606, "Event 6 · repeated basic event",
           "Under G6, G3, G1 and G0 (all OR gates): alone it is the minimal cut set {6}."),
    "8": ("8", 540, 606, "Event 8 · basic event",
          "Under G6, G3, G1 and G0 (all OR gates): alone it is the minimal cut set {8}."),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def top_of(child):
    """y where a connector line meets a child (box top or circle top)."""
    if child in GATES:
        return GATES[child][2]
    return EVENTS[child][2] - EV_R


def x_of(child):
    return GATES[child][1] if child in GATES else EVENTS[child][1]


def gate_symbol(kind, cx, t):
    b = t + GATE_H
    if kind == "or":
        return (f'<path d="M{cx-20} {b} Q{cx-20} {t+12} {cx} {t} Q{cx+20} {t+12} {cx+20} {b} '
                f'Q{cx} {b-12} {cx-20} {b} Z" fill="{RED_TINT}" stroke="{INK}" stroke-width="2"/>')
    return (f'<path d="M{cx-20} {b} L{cx-20} {t+20} A20 20 0 0 1 {cx+20} {t+20} L{cx+20} {b} Z" '
            f'fill="{RED_TINT2}" stroke="{INK}" stroke-width="2"/>')


def build(prefix):
    out = [f'<svg class="fig" viewBox="0 0 600 640" role="img" aria-labelledby="{prefix}-t {prefix}-d">',
           f'<title id="{prefix}-t">Textbook fault tree: gates G0 to G6 over basic events 1 to 8</title>',
           f'<desc id="{prefix}-d">G0 is an OR gate over events 1 and 2 and gate G1. G1 is an OR over G2 and G3. '
           'G2 is an AND over G4 (OR of events 4 and 5) and G5 (OR of events 6 and 7). '
           'G3 is an OR over event 3 and G6 (OR of events 6 and 8). Minimal cut sets: 1, 2, 3, 6, 8, {4,7}, {5,7}.</desc>']
    # connectors first, so shapes sit on top
    lines = []
    for name, (kind, cx, y, kids, _, _) in GATES.items():
        gt = y + BOX_H + 8
        gb = gt + GATE_H
        lines.append(f'<line x1="{cx}" y1="{y+BOX_H}" x2="{cx}" y2="{gt}"/>')
        bus = gb + 12
        stem_top = gb - (12 if kind == "or" else 0)
        lines.append(f'<line x1="{cx}" y1="{stem_top}" x2="{cx}" y2="{bus}"/>')
        xs = [x_of(k) for k in kids]
        lines.append(f'<line x1="{min(xs)}" y1="{bus}" x2="{max(xs)}" y2="{bus}"/>')
        for k in kids:
            lines.append(f'<line x1="{x_of(k)}" y1="{bus}" x2="{x_of(k)}" y2="{top_of(k)}"/>')
    out.append(f'<g stroke="{INK}" stroke-width="2" fill="none">' + "".join(lines) + "</g>")
    for name, (kind, cx, y, kids, title, tip) in GATES.items():
        out.append(f'<g id="{prefix}-{name}" tabindex="0" data-tip-title="{esc(title)}" data-tip="{esc(tip)}">'
                   f'<rect x="{cx-BOX_W//2}" y="{y}" width="{BOX_W}" height="{BOX_H+8+GATE_H}" fill="{WHITE}" fill-opacity="0"/>'  # hit area: box + gap + gate
                   f'<rect x="{cx-BOX_W//2}" y="{y}" width="{BOX_W}" height="{BOX_H}" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>'
                   f'<text x="{cx}" y="{y+31}" font-size="24" text-anchor="middle" fill="{INK}">{name}</text>'
                   + gate_symbol(kind, cx, y + BOX_H + 8) + "</g>")
    for eid, (label, cx, cy, title, tip) in EVENTS.items():
        out.append(f'<g id="{prefix}-e{eid}" tabindex="0" data-tip-title="{esc(title)}" data-tip="{esc(tip)}">'
                   f'<circle cx="{cx}" cy="{cy}" r="{EV_R}" fill="{WHITE}" stroke="{RED_DARK}" stroke-width="2.5"/>'
                   f'<text x="{cx}" y="{cy+8}" font-size="24" text-anchor="middle" fill="{INK}">{label}</text></g>')
    out.append("</svg>")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Generic layout for the other trees on the deck. A node is
#   (kind, label lines, tip title, tip text, children)
# kind: "or" / "and" = event box over a gate symbol; "top" = box, single line
# down; "basic" = circle; "transfer" = triangle. Leaves get x slots left to
# right; a parent sits over the middle of its children.

FIRE = {
    "top": ("or", ["No signal from", "the start relay"], "TOP event · OR gate",
            "No signal from the start relay: the DC source fails, the detection system gives no signal, or the start relay fails open.",
            ["DC", "det", "SR"]),
    "DC": ("basic", ["DC"], "DC · basic event", "No current from the DC current source.", []),
    "det": ("and", ["No signal from", "detection system"], "Detection system · AND gate",
            "No signal only if ALL THREE detection systems (heat, smoke, manual) fail: they are redundant.",
            ["heat", "smoke", "man"]),
    "SR": ("basic", ["SR"], "SR · basic event", "Start relay fails in the open position.", []),
    "heat": ("or", ["Heat", "detection"], "Heat detection · OR gate",
             "No signal from the heat detection system: the pressure switch fails closed, or the fuse plugs are not activated.",
             ["PS1", "fuse"]),
    "smoke": ("or", ["Smoke", "detection"], "Smoke detection · OR gate",
              "No signal from the smoke detection system: at least 2 of 3 smoke detectors fail (transfer A), or the voting unit fails.",
              ["A", "VU"]),
    "man": ("or", ["Manual", "activation"], "Manual activation · OR gate",
            "No signal from the manual activation system: the manual switch fails, the pressure switch fails closed, or the operator fails to act.",
            ["MS", "PS2", "OP"]),
    "PS1": ("basic", ["PS"], "PS · basic event", "Pressure switch fails in closed position. It appears twice: also under manual activation.", []),
    "fuse": ("and", ["Fuse plugs", "not activated"], "Fuse plugs · AND gate",
             "Fuse plugs are not activated only if ALL FOUR fuse plugs fail to respond.",
             ["FP1", "FP2", "FP3", "FP4"]),
    "FP1": ("basic", ["FP1"], "FP1 · basic event", "Fuse plug 1 does not respond.", []),
    "FP2": ("basic", ["FP2"], "FP2 · basic event", "Fuse plug 2 does not respond.", []),
    "FP3": ("basic", ["FP3"], "FP3 · basic event", "Fuse plug 3 does not respond.", []),
    "FP4": ("basic", ["FP4"], "FP4 · basic event", "Fuse plug 4 does not respond.", []),
    "A": ("transfer", ["A"], "Transfer in A",
          "At least 2 of the 3 smoke detectors do not respond: developed on the next slide (an OR over three AND combinations of SD1, SD2, SD3).", []),
    "VU": ("basic", ["VU"], "VU · basic event", "Voting unit fails to raise a signal.", []),
    "MS": ("basic", ["MS"], "MS · basic event", "Manual switch fails to open.", []),
    "PS2": ("basic", ["PS"], "PS · basic event (repeated)", "Pressure switch fails in closed position. The same event as under heat detection.", []),
    "OP": ("basic", ["OP"], "OP · basic event", "Operator fails to take action.", []),
}

MOCUS1 = {
    "T": ("top", ["T"], "T · TOP event", "The top event. MOCUS starts here: write the top gate, G1, in row 1.", ["G1"]),
    "G1": ("and", ["G1"], "G1 · AND gate", "Both G2 and G3 must fail: replace G1 with G2, G3 on ONE row (comma).", ["G2", "G3"]),
    "G2": ("or", ["G2"], "G2 · OR gate", "Event 1 or event 2: replace G2 by two rows, one per input.", ["a1", "a2"]),
    "G3": ("or", ["G3"], "G3 · OR gate", "Event 1 or event 3: replace G3 by two rows, one per input.", ["b1", "b3"]),
    "a1": ("basic", ["1"], "Event 1 · repeated basic event", "Appears under G2 and G3: {1} alone fails both, so {1} is a minimal cut set.", []),
    "a2": ("basic", ["2"], "Event 2 · basic event", "Under G2 only: it needs event 3 from G3. Minimal cut set {2, 3}.", []),
    "b1": ("basic", ["1"], "Event 1 · repeated basic event", "The same event 1 as under G2: {1, 1} = {1} (a*a = a).", []),
    "b3": ("basic", ["3"], "Event 3 · basic event", "Under G3 only: it needs event 2 from G2. Minimal cut set {2, 3}.", []),
}

BULB = {
    "top": ("or", ["Light fails off"], "TOP event · OR gate",
            "The light fails off if ANY one of the five events occurs: five single-event cut sets A, B, C, D, E.",
            ["A", "B", "C", "D", "E"]),
    "A": ("basic", ["A"], "A · Bulb fails", "lambda = 1.0e-6 per hr, T = 2 hr, P = 1 - exp(-lambda T) = 2.0e-6", []),
    "B": ("basic", ["B"], "B · Switch A fails open", "lambda = 1.0e-7 per hr, T = 2 hr, P = 2.0e-7", []),
    "C": ("basic", ["C"], "C · Switch B fails open", "lambda = 1.0e-7 per hr, T = 2 hr, P = 2.0e-7", []),
    "D": ("basic", ["D"], "D · Battery fails", "lambda = 1.0e-8 per hr, T = 2 hr, P = 2.0e-8", []),
    "E": ("basic", ["E"], "E · Wire fails open", "lambda = 1.0e-9 per hr, T = 2 hr, P = 2.0e-9", []),
}

# name: (spec, root, title, desc, leaf spacing, level height, box width, font size)
TREES = {
    "fire": (FIRE, "top", "Fire detection system fault tree",
             "No signal from the start relay is an OR over DC, the detection system and SR. The detection system is an AND over "
             "heat detection (OR of PS and the fuse plugs, an AND of FP1 to FP4), smoke detection (OR of transfer A and VU) "
             "and manual activation (OR of MS, PS and OP).", 74, 128, 168, 22),
    "mocus1": (MOCUS1, "T", "MOCUS example 1 fault tree",
               "Top event T over AND gate G1, which has inputs G2 and G3. G2 is an OR of events 1 and 2; G3 is an OR of events 1 and 3.",
               96, 116, 80, 26),
    "bulb": (BULB, "top", "Light bulb fault tree",
             "Light fails off is an OR gate over five basic events: A bulb fails, B switch A fails open, C switch B fails open, "
             "D battery fails, E wire fails open.", 96, 150, 200, 24),
}


def layout(spec, root, dx, dy):
    pos, slot = {}, [0]

    def walk(n, depth):
        kids = spec[n][4]
        for k in kids:
            walk(k, depth + 1)
        if kids:
            x = (pos[kids[0]][0] + pos[kids[-1]][0]) / 2
        else:
            x = 40 + slot[0] * dx
            slot[0] += 1
        pos[n] = (x, 8 + depth * dy)
    walk(root, 0)
    return pos, slot[0]


def build_tree(name, prefix):
    spec, root, title, desc, dx, dy, bw, fs = TREES[name]
    pos, nleaf = layout(spec, root, dx, dy)
    bh = int(fs * 1.25 * max(len(v[1]) for v in spec.values() if v[0] in ("or", "and", "top"))) + 12
    gh, er = 36, 26
    W = int(80 + (nleaf - 1) * dx)
    H = int(max(y for _, y in pos.values()) + 2 * er + 12)
    if any(spec[n][0] in ("or", "and") and not spec[n][4] for n in spec):
        H += bh

    def top_y(n):
        return pos[n][1]

    lines, shapes = [], []
    for n, (kind, lab, tt, tip, kids) in spec.items():
        x, y = pos[n]
        x = round(x)
        if kind in ("or", "and", "top"):
            bot = y + bh
            if kind != "top":
                gt = bot + 6
                gb = gt + gh
                lines.append(f'<line x1="{x}" y1="{bot}" x2="{x}" y2="{gt}"/>')
                stem = gb - (10 if kind == "or" else 0)
            else:
                gb = stem = bot
            bus = max(gb + 12, (y + dy) - 14) if len(kids) > 1 else gb
            lines.append(f'<line x1="{x}" y1="{stem}" x2="{x}" y2="{bus}"/>')
            xs = [round(pos[k][0]) for k in kids]
            if len(xs) > 1:
                lines.append(f'<line x1="{min(xs)}" y1="{bus}" x2="{max(xs)}" y2="{bus}"/>')
            for k in kids:
                lines.append(f'<line x1="{round(pos[k][0])}" y1="{bus}" x2="{round(pos[k][0])}" y2="{top_y(k)}"/>')
            w = max(bw if kind != "top" else 80, 0)
            if len(lab) == 1 and len(lab[0]) <= 3:
                w = 80
            g = (f'<rect x="{x-w//2}" y="{y}" width="{w}" height="{bh}" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>')
            for i, t in enumerate(lab):
                ty = y + bh / 2 + fs * 0.36 + (i - (len(lab) - 1) / 2) * fs * 1.2
                g += f'<text x="{x}" y="{ty:.0f}" font-size="{fs}" text-anchor="middle" fill="{INK}">{esc(t)}</text>'
            if kind != "top":
                g += gate_symbol(kind, x, bot + 6)
            hit_h = bh + (6 + gh if kind != "top" else 0)
            g = f'<rect x="{x-w//2}" y="{y}" width="{w}" height="{hit_h}" fill="{WHITE}" fill-opacity="0"/>' + g
        elif kind == "basic":
            cy = y + er
            g = (f'<circle cx="{x}" cy="{cy}" r="{er}" fill="{WHITE}" stroke="{RED_DARK}" stroke-width="2.5"/>'
                 f'<text x="{x}" y="{cy + fs*0.36:.0f}" font-size="{fs if len(lab[0]) < 3 else fs - 4}" text-anchor="middle" fill="{INK}">{esc(lab[0])}</text>')
        else:  # transfer
            g = (f'<path d="M{x} {y} L{x+er+4} {y+2*er} L{x-er-4} {y+2*er} Z" fill="{RED_TINT}" stroke="{INK}" stroke-width="2"/>'
                 f'<text x="{x}" y="{y + 2*er - 8}" font-size="{fs}" text-anchor="middle" fill="{INK}">{esc(lab[0])}</text>')
        shapes.append(f'<g id="{prefix}-{n}" tabindex="0" data-tip-title="{esc(tt)}" data-tip="{esc(tip)}">{g}</g>')
    out = [f'<svg class="fig" viewBox="0 0 {W} {H}" role="img" aria-labelledby="{prefix}-t {prefix}-d">',
           f'<title id="{prefix}-t">{esc(title)}</title>', f'<desc id="{prefix}-d">{esc(desc)}</desc>',
           f'<g stroke="{INK}" stroke-width="2" fill="none">' + "".join(lines) + "</g>"] + shapes + ["</svg>"]
    return "\n".join(out)


if __name__ == "__main__":
    # python3 functions/slides_recitation_9_tree.py <prefix> [textbook|fire|mocus1|bulb]
    pre = sys.argv[1] if len(sys.argv) > 1 else "ft"
    which = sys.argv[2] if len(sys.argv) > 2 else "textbook"
    print(build(pre) if which == "textbook" else build_tree(which, pre))
