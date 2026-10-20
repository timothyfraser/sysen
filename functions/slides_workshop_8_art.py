#!/usr/bin/env python3
"""Build the two inline-ready diagrams for the Recitation 12 (Monitoring &
Control Systems) deck and paste them into the deck between marker comments.

Run from the sigma root:   python3 functions/slides_workshop_8_art.py

Writes docs-v3/images/slides/workshop-8/{components,rest_api}.svg and replaces the
block between  <!-- ws8-components:begin --> ... <!-- ws8-components:end -->  and
<!-- ws8-rest:begin --> ... <!-- ws8-rest:end -->  in
docs-v3/slides/20_workshop_slides.html.

Every SVG is written to be pasted INLINE: no XML prolog, <title> first, ids
prefixed ws8-, and each node is a <g data-tip=".." data-tip-title=".."> so the
deck's tooltip engine can target it. Python stdlib only; palette from SLIDES.md.
"""
import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs-v3" / "images" / "slides" / "workshop-8"
SLIDE = ROOT / "docs-v3" / "slides" / "20_workshop_slides.html"

CARNELIAN = "#B31B1B"
INK = "#1f1f1f"
BLUE = "#dce8f8"
TAN = "#f8dcc0"
BERRY = "#e8c8da"
YELLOW = "#f8e2a0"
LAVENDER = "#b0a8d0"
GRAY = "#f3f1ee"
MUTED = "#5a5550"
FONT = "Lato,'Helvetica Neue',Arial,sans-serif"


def esc(s):
    return html.escape(str(s), quote=True)


def txt(x, y, s, size=26, fill=INK, anchor="middle", weight="400", extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{extra}>{esc(s)}</text>')


def node(nid, title, tip, body):
    return (f'<g id="{nid}" tabindex="0" data-tip-title="{esc(title)}" data-tip="{esc(tip)}">'
            f'{body}</g>')


def arrow(p, pts, color=CARNELIAN):
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="4" '
            f'stroke-linejoin="round" marker-end="url(#{p}-head)"/>')


def defs(p, color=CARNELIAN):
    return (f'<defs><marker id="{p}-head" viewBox="0 0 10 10" refX="8" refY="5" '
            f'markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="{color}"/></marker></defs>')


def box(x, y, w, h, fill, lines, size=28):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" '
           f'stroke="{INK}" stroke-width="2.5"/>']
    n = len(lines)
    y0 = y + h / 2 - (n - 1) * size * 0.6 + size * 0.35
    for i, ln in enumerate(lines):
        out.append(txt(x + w / 2, round(y0 + i * size * 1.2, 1), ln, size))
    return "".join(out)


def components():
    p = "ws8c"
    W, H = 1090, 560
    o = [f'<svg class="fig" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-labelledby="{p}-t {p}-d" font-family="{FONT}">',
         f'<title id="{p}-t">Components of a monitoring system</title>',
         f'<desc id="{p}-d">A Sensor sends a Record Data message into a Database; an Extract Data '
         f'function turns it into a Table; a Process Data function computes quantities of interest '
         f'(Mean = 3, Do X); a Deliver Insights message reaches the User.</desc>',
         defs(p)]
    # column headers (what kind of thing each is)
    for x, s in [(90, "Sensor"), (290, "Message"), (530, "Database"), (750, "Function")]:
        o.append(txt(x, 46, s, 26, MUTED))
    for x, s in [(90, "User"), (290, "Message"), (530, "Quantities of Interest"), (750, "Function")]:
        o.append(txt(x, 534, s, 26, MUTED))
    # flow arrows first, nodes on top
    o.append(arrow(p, [(124, 150), (170, 150), (170, 150), (200, 150)]))
    o.append(arrow(p, [(380, 150), (470, 150)]))
    o.append(arrow(p, [(592, 150), (660, 150)]))
    o.append(arrow(p, [(840, 150), (921, 150), (921, 196)]))
    o.append(arrow(p, [(921, 342), (921, 400), (840, 400)]))
    o.append(arrow(p, [(660, 400), (610, 400)]))
    o.append(arrow(p, [(490, 400), (380, 400)]))
    o.append(arrow(p, [(200, 400), (130, 400)]))
    # 1 sensor
    o.append(node(f"{p}-sensor", "Sensor",
                  "Measures the real world: a counter, a thermometer, a click.|"
                  "Where every monitoring system starts.",
                  f'<circle cx="90" cy="150" r="34" fill="{CARNELIAN}"/>'
                  f'<path d="M34 120 Q20 150 34 180" fill="none" stroke="{CARNELIAN}" stroke-width="5" stroke-linecap="round"/>'
                  f'<path d="M48 126 Q38 150 48 174" fill="none" stroke="{CARNELIAN}" stroke-width="5" stroke-linecap="round"/>'))
    # 2 record data
    o.append(node(f"{p}-record", "Record Data (message)",
                  "The sensor sends its reading to the database.|"
                  "A message: one reading in, one row stored.",
                  box(200, 105, 180, 90, BLUE, ["Record", "Data"])))
    # 3 database cylinder
    db = (f'<path d="M472 112 V190 Q472 212 530 212 Q588 212 588 190 V112 Z" fill="{CARNELIAN}"/>'
          f'<ellipse cx="530" cy="112" rx="58" ry="20" fill="{CARNELIAN}" stroke="#fff" stroke-width="3"/>'
          f'<path d="M472 140 Q472 160 530 160 Q588 160 588 140" fill="none" stroke="#fff" stroke-width="4"/>'
          f'<path d="M472 170 Q472 190 530 190 Q588 190 588 170" fill="none" stroke="#fff" stroke-width="4"/>')
    o.append(node(f"{p}-db", "Database",
                  "Stores every recorded reading, in order.|"
                  "Nothing is processed yet: this is the raw record.", db))
    # 4 extract data
    o.append(node(f"{p}-extract", "Extract Data (function)",
                  "Queries the database for the rows you want.|"
                  "A function: asks for data, hands back a table.",
                  box(660, 105, 180, 90, TAN, ["Extract", "Data"])))
    # 5 table 3x3
    cells = "".join(
        f'<rect x="{862 + c * 42}" y="{200 + r * 46}" width="34" height="38" rx="5" fill="{CARNELIAN}"/>'
        for r in range(3) for c in range(3))
    o.append(node(f"{p}-table", "Table",
                  "The extracted data, as rows and columns.|"
                  "Queried data: ready to be processed.", cells))
    o.append(txt(998, 282, "Table", 26, MUTED, "start"))
    # 6 process data
    o.append(node(f"{p}-process", "Process Data (function)",
                  "Turns the table into numbers that matter.|"
                  "E.g. the mean, a control-chart signal, a rule: Do X.",
                  box(660, 355, 180, 90, TAN, ["Process", "Data"])))
    # 7 quantities of interest
    qoi = (f'<rect x="470" y="340" width="140" height="34" rx="6" fill="{CARNELIAN}"/>' + txt(540, 364, "Mean = 3", 20, "#fff") +
           f'<rect x="470" y="380" width="140" height="62" rx="6" fill="{CARNELIAN}"/>' + txt(540, 420, "Do X", 30, "#fff") +
           f'<rect x="470" y="448" width="140" height="28" rx="6" fill="{CARNELIAN}"/>' + txt(540, 468, "More info", 17, "#fff"))
    o.append(node(f"{p}-qoi", "Quantities of Interest (insights)",
                  "The answer the user needs, not the raw data.|"
                  "A statistic (Mean = 3), a decision (Do X), a link for more info.", qoi))
    # 8 deliver insights
    o.append(node(f"{p}-deliver", "Deliver Insights (message)",
                  "Sends the quantities of interest to a person.|"
                  "A message: an email, a dashboard, an alert.",
                  box(200, 355, 180, 90, BLUE, ["Deliver", "Insights"])))
    # 9 user
    user = (f'<circle cx="90" cy="368" r="24" fill="{CARNELIAN}"/>'
            f'<path d="M62 392 H118 V452 H62 Z" fill="{CARNELIAN}"/>'
            f'<path d="M62 398 L36 372 L46 364 L66 384 Z M118 398 L144 372 L134 364 L114 384 Z" fill="{CARNELIAN}"/>')
    o.append(node(f"{p}-user", "User",
                  "The person who acts on the insight.|"
                  "The whole system exists to give them one good decision.", user))
    o.append("</svg>")
    return "\n".join(o)


def rest():
    p = "ws8r"
    W, H = 1000, 560
    o = [f'<svg class="fig" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-labelledby="{p}-t {p}-d" font-family="{FONT}">',
         f'<title id="{p}-t">How a REST API call works</title>',
         f'<desc id="{p}-d">A client sends an HTTP verb and a URL to a server; the server replies '
         f'with JSON.</desc>',
         defs(p, INK)]
    o.append(txt(90, 40, "CLIENT", 30, INK, "middle", "700"))
    o.append(txt(910, 40, "SERVER", 30, INK, "middle", "700"))
    o.append(arrow(p, [(170, 130), (240, 130)], INK))
    o.append(arrow(p, [(700, 130), (790, 130)], INK))
    o.append(arrow(p, [(910, 250), (910, 420), (600, 440)], INK))
    o.append(arrow(p, [(400, 440), (90, 430), (90, 235)], INK))
    # client monitor
    o.append(node(f"{p}-client", "Client",
                  "The computer asking for something: your browser, an R script, a Python script.|"
                  "It starts every call.",
                  f'<rect x="20" y="70" width="140" height="110" rx="14" fill="none" stroke="#8a8a8a" stroke-width="10"/>'
                  f'<line x1="26" y1="150" x2="154" y2="150" stroke="#8a8a8a" stroke-width="8"/>'
                  f'<path d="M70 184 H110 L116 212 H64 Z" fill="#8a8a8a"/>'))
    # server stack
    srv = (f'<rect x="830" y="70" width="160" height="70" rx="22" fill="none" stroke="#8a8a8a" stroke-width="10"/>'
           f'<rect x="830" y="140" width="160" height="70" rx="22" fill="none" stroke="#8a8a8a" stroke-width="10"/>'
           f'<circle cx="935" cy="175" r="6" fill="#8a8a8a"/><circle cx="960" cy="175" r="6" fill="#8a8a8a"/>')
    o.append(node(f"{p}-server", "Server",
                  "The online 'listener' that waits to be pinged.|"
                  "Each function it offers lives at a URL address, an 'endpoint'.", srv))
    # HTTP verb
    o.append(node(f"{p}-http", "HTTP verb",
                  "What you want done.|GET: read | POST: create | PUT: replace | DELETE: remove",
                  f'<rect x="250" y="95" width="170" height="70" rx="14" fill="#c6efd2" stroke="{INK}" stroke-width="2.5"/>'
                  + txt(335, 142, "HTTP", 36)
                  + txt(262, 215, "GET", 26, INK, "start", extra=' font-family="monospace"')
                  + txt(262, 247, "POST", 26, INK, "start", extra=' font-family="monospace"')
                  + txt(262, 279, "DELETE", 26, INK, "start", extra=' font-family="monospace"')
                  + txt(262, 311, "PUT", 26, INK, "start", extra=' font-family="monospace"')))
    # URL
    o.append(node(f"{p}-url", "URL (endpoint)",
                  "Where to do it, written as a path.|/surveys is the whole collection; /surveys/123 is one survey.",
                  f'<rect x="480" y="95" width="170" height="70" rx="14" fill="{BLUE}" stroke="{INK}" stroke-width="2.5"/>'
                  + txt(565, 142, "URL", 36)
                  + txt(480, 215, "/surveys", 26, INK, "start", extra=' font-family="monospace"')
                  + txt(480, 247, "/surveys/123", 26, INK, "start", extra=' font-family="monospace"')
                  + txt(480, 279, "/surveys/123/resp …", 26, INK, "start", extra=' font-family="monospace"')))
    # JSON
    o.append(node(f"{p}-json", "JSON (the reply)",
                  "The server's answer: labelled values any language can read.|"
                  "Here: survey_id 123, score 9, a message, response_id 4.",
                  f'<rect x="410" y="405" width="180" height="70" rx="14" fill="{YELLOW}" stroke="{INK}" stroke-width="2.5"/>'
                  + txt(500, 452, "JSON", 36)
                  + txt(360, 512, '{ survey_id: 123, score: 9,', 22, INK, "start", extra=' font-family="monospace"')
                  + txt(360, 540, '  message: "amaze …", response_id: 4 }', 22, INK, "start", extra=' font-family="monospace"')))
    o.append("</svg>")
    return "\n".join(o)


def inject(src, key, svg):
    a, b = f"<!-- {key}:begin -->", f"<!-- {key}:end -->"
    i, j = src.find(a), src.find(b)
    if i < 0 or j < 0:
        sys.exit(f"FAIL slides_workshop_8_art: markers {key} not found in {SLIDE}")
    return src[:i + len(a)] + "\n" + svg + "\n" + src[j:]


def main():
    c, r = components(), rest()
    (OUT / "components.svg").write_text(c, encoding="utf-8")
    (OUT / "rest_api.svg").write_text(r, encoding="utf-8")
    src = SLIDE.read_text(encoding="utf-8")
    src = inject(src, "ws8-components", c)
    src = inject(src, "ws8-rest", r)
    SLIDE.write_text(src, encoding="utf-8")
    print("OK slides_workshop_8_art: components.svg, rest_api.svg written and injected")


if __name__ == "__main__":
    main()
