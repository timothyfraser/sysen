#!/usr/bin/env python3
"""Two inline-ready SVGs for Recitation 11 (19_slides_recitation_7).

Run from the sigma root:   python3 functions/slides_recitation_7_art.py

Writes docs-v3/images/slides/recitation-7/{ci_diagram,test_team}.svg
  ci_diagram  the "confidence intervals around the true value" picture (slide 4),
              redrawn from the 2025 screenshot, a data-tip on every mark.
  test_team   a cartoon of a test team watching units on a rack (image-right slide).

Python stdlib only; no XML prolog, <title> first, ids prefixed (ci-, tt-).
Palette: specs/SLIDES.md section 4 (no green).
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs-v3" / "images" / "slides" / "recitation-7"
INK = "#2a1414"; RED = "#B31B1B"; REDT = "#fbecec"; MUTED = "#8a6a6a"
BLUE = "#a0c0f0"; BLUES = "#dce8f8"; BMID = "#3880c0"; PURP = "#8878c0"; PURS = "#e2ddf0"
YEL = "#f0c030"; YELS = "#f8e2a0"; TAN = "#f8dcc0"; ROSE = "#d08080"; LAV = "#b0a8d0"; NAVY = "#302050"
FONT = "Lato,'Helvetica Neue',Arial,sans-serif"
e = lambda s: html.escape(str(s), quote=True)


def svg(prefix, w, h, title, desc, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
            f'aria-labelledby="{prefix}-t {prefix}-d" font-family="{FONT}">\n'
            f'<title id="{prefix}-t">{e(title)}</title>\n<desc id="{prefix}-d">{e(desc)}</desc>\n{body}</svg>\n')


def lam_hat(x, y, size, fill=INK):
    """lambda with a hand-drawn hat (a combining circumflex renders badly in some fonts)."""
    w = size * 0.28
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-style="italic" text-anchor="middle" fill="{fill}">&#955;</text>'
            f'<path d="M{x-w} {y-size*0.78} L{x} {y-size*0.98} L{x+w} {y-size*0.78}" fill="none" stroke="{fill}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')


def ci_diagram():
    b = []
    cx, tx = 330, 392            # lambda-hat line, true-value line
    b.append(f'<g id="ci-formula" data-tip="Point estimator: lambda-hat = number of failures divided by total unit test hours">'
             f'{lam_hat(166, 66, 36)}<text x="204" y="66" font-size="30" fill="{INK}">=</text>'
             f'<text x="361" y="38" font-size="24" font-style="italic" text-anchor="middle" fill="{INK}"># of Failures</text>'
             f'<line x1="226" y1="52" x2="496" y2="52" stroke="{INK}" stroke-width="2"/>'
             f'<text x="361" y="84" font-size="24" font-style="italic" text-anchor="middle" fill="{INK}">total unit test hours</text>'
             f'<text x="330" y="130" font-size="26" text-anchor="middle" fill="{MUTED}">point estimator</text></g>')
    b.append(f'<g id="ci-est" data-tip="lambda-hat: the point estimate from one experiment. Every interval is built around it by multiplying with k factors.">'
             f'{lam_hat(cx, 196, 40)}'
             f'<line x1="{cx}" y1="206" x2="{cx}" y2="640" stroke="{INK}" stroke-width="3"/></g>')
    b.append(f'<g id="ci-true" data-tip="True value of lambda: fixed but unknown. A 95% CI is built to cover it 95% of the time.">'
             f'<line x1="{tx}" y1="236" x2="{tx}" y2="640" stroke="{RED}" stroke-width="2" stroke-dasharray="7 6"/>'
             f'<text x="{tx+12}" y="258" font-size="34" font-style="italic" fill="{RED}">&#955;</text>'
             f'<text x="{tx+42}" y="256" font-size="26" fill="{MUTED}">true value</text></g>')
    bars = [(1, 270, 560, 220, 480), (2, 270, 600, 275, 480), (3, 270, 640, 198, 458), (4, 270, 680, 220, 480)]
    ys = [300, 345, 390, 435]
    spans = [(220, 480), (275, 480), (198, 458), (220, 480)]
    for i, (y, (lo, hi)) in enumerate(zip(ys, spans), 1):
        b.append(f'<g id="ci-int{i}" data-tip="Experiment {i}: one 95% CI, from lambda-2.5 to lambda-97.5. It covers the true value of lambda.">'
                 f'<line x1="{lo}" y1="{y}" x2="{hi}" y2="{y}" stroke="{INK}" stroke-width="3"/>'
                 f'<circle cx="{lo}" cy="{y}" r="6" fill="{INK}"/><circle cx="{hi}" cy="{y}" r="6" fill="{INK}"/></g>')
    b.append(f'<g id="ci-dots" data-tip="...and so on: repeat the experiment many times and draw a new interval each time"><circle cx="{cx}" cy="480" r="4" fill="{MUTED}"/><circle cx="{cx}" cy="498" r="4" fill="{MUTED}"/><circle cx="{cx}" cy="516" r="4" fill="{MUTED}"/></g>')
    b.append(f'<g id="ci-int5" data-tip="Experiment N: the pattern repeats. About 95% of all such intervals cover the true value.">'
             f'<line x1="265" y1="560" x2="468" y2="560" stroke="{INK}" stroke-width="3"/>'
             f'<circle cx="265" cy="560" r="6" fill="{INK}"/><circle cx="468" cy="560" r="6" fill="{INK}"/></g>')
    b.append(f'<g id="ci-lo" data-tip="lambda-2.5: lower bound, the 2.5th percentile of the sampling distribution">'
             f'<text x="262" y="684" font-size="38" font-style="italic" text-anchor="middle" fill="{INK}">&#955;<tspan font-size="24" dy="8">2.5</tspan></text></g>')
    b.append(f'<g id="ci-hi" data-tip="lambda-97.5: upper bound, the 97.5th percentile of the sampling distribution">'
             f'<text x="470" y="684" font-size="38" font-style="italic" text-anchor="middle" fill="{INK}">&#955;<tspan font-size="24" dy="8">97.5</tspan></text></g>')
    return svg("ci", 640, 710, "Confidence intervals around the true value of lambda",
               "Lambda-hat equals the number of failures over total unit test hours. Several intervals from repeated experiments, each from lambda 2.5 to lambda 97.5, cross the dashed line at the true value.",
               "\n".join(b))


def person(px, base, skin, hair, shirt, style, tip, scale=1.0, glasses=False):
    """A standing figure; (px, base) = centre x and feet y. style: bun, short, curly, hijab, bald."""
    s = scale
    hx, hy = px, base - 188 * s
    out = [f'<g data-tip="{e(tip)}">']
    # legs
    out.append(f'<rect x="{px-26*s}" y="{base-78*s}" width="22" height="{78*s}" rx="6" fill="{NAVY}"/>')
    out.append(f'<rect x="{px+4*s}" y="{base-78*s}" width="22" height="{78*s}" rx="6" fill="{NAVY}"/>')
    # torso
    out.append(f'<rect x="{px-36*s}" y="{base-158*s}" width="{72*s}" height="{86*s}" rx="22" fill="{shirt}" stroke="{INK}" stroke-width="2"/>')
    # clipboard arm
    out.append(f'<rect x="{px-6*s}" y="{base-140*s}" width="{34*s}" height="{44*s}" rx="4" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    out.append(f'<line x1="{px+2*s}" y1="{base-126*s}" x2="{px+20*s}" y2="{base-126*s}" stroke="{MUTED}" stroke-width="2"/>')
    out.append(f'<line x1="{px+2*s}" y1="{base-114*s}" x2="{px+20*s}" y2="{base-114*s}" stroke="{MUTED}" stroke-width="2"/>')
    out.append(f'<circle cx="{px-34*s}" cy="{base-112*s}" r="11" fill="{skin}" stroke="{INK}" stroke-width="2"/>')
    # hair behind / hijab
    if style == "hijab":
        out.append(f'<path d="M{px-36*s} {hy+10*s} Q{px-38*s} {hy-40*s} {px} {hy-40*s} Q{px+38*s} {hy-40*s} {px+36*s} {hy+10*s} L{px+40*s} {hy+52*s} L{px-40*s} {hy+52*s} Z" fill="{hair}" stroke="{INK}" stroke-width="2"/>')
    if style == "curly":
        for dx, dy in [(-28, -14), (-14, -34), (6, -38), (24, -26), (30, -6), (-32, 4)]:
            out.append(f'<circle cx="{px+dx*s}" cy="{hy+dy*s}" r="{15*s}" fill="{hair}"/>')
    if style == "bun":
        out.append(f'<circle cx="{px}" cy="{hy-44*s}" r="{14*s}" fill="{hair}" stroke="{INK}" stroke-width="2"/>')
    # head
    out.append(f'<circle cx="{hx}" cy="{hy}" r="{32*s}" fill="{skin}" stroke="{INK}" stroke-width="2"/>')
    if style in ("short", "bun"):
        out.append(f'<path d="M{hx-32*s} {hy-4*s} Q{hx-30*s} {hy-38*s} {hx} {hy-36*s} Q{hx+30*s} {hy-38*s} {hx+32*s} {hy-4*s} Q{hx} {hy-22*s} {hx-32*s} {hy-4*s} Z" fill="{hair}"/>')
    if style == "hijab":
        out.append(f'<path d="M{hx-32*s} {hy-6*s} Q{hx} {hy-36*s} {hx+32*s} {hy-6*s} Q{hx+22*s} {hy-14*s} {hx} {hy-16*s} Q{hx-22*s} {hy-14*s} {hx-32*s} {hy-6*s} Z" fill="{hair}"/>')
    # eyes (looking left at the rack), smile
    for dx in (-12, 8):
        out.append(f'<circle cx="{hx+dx*s}" cy="{hy+2*s}" r="{4.5*s}" fill="#fff" stroke="{INK}" stroke-width="1.5"/><circle cx="{hx+(dx-2)*s}" cy="{hy+2*s}" r="{2.2*s}" fill="{INK}"/>')
    if glasses:
        out.append(f'<circle cx="{hx-12*s}" cy="{hy+2*s}" r="{9*s}" fill="none" stroke="{INK}" stroke-width="2"/><circle cx="{hx+8*s}" cy="{hy+2*s}" r="{9*s}" fill="none" stroke="{INK}" stroke-width="2"/><line x1="{hx-3*s}" y1="{hy+2*s}" x2="{hx-1*s}" y2="{hy+2*s}" stroke="{INK}" stroke-width="2"/>')
    out.append(f'<path d="M{hx-12*s} {hy+16*s} Q{hx-3*s} {hy+22*s} {hx+8*s} {hy+16*s}" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
    out.append('</g>')
    return "".join(out)


def unit(x, y, led, tip):
    return (f'<g data-tip="{e(tip)}"><rect x="{x}" y="{y}" width="52" height="40" rx="5" fill="{BLUES}" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="{x+8}" y="{y+8}" width="22" height="10" rx="2" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
            f'<circle cx="{x+40}" cy="{y+13}" r="5" fill="{led}" stroke="{INK}" stroke-width="1.5"/>'
            f'<line x1="{x+8}" y1="{y+28}" x2="{x+44}" y2="{y+28}" stroke="{BLUE}" stroke-width="3"/></g>')


def test_team():
    b = []
    b.append(f'<rect x="0" y="0" width="720" height="520" fill="{YELS}" opacity=".35"/>')
    b.append(f'<rect x="0" y="470" width="720" height="50" fill="{TAN}"/><line x1="0" y1="470" x2="720" y2="470" stroke="{INK}" stroke-width="2"/>')
    # rack
    b.append(f'<g id="tt-rack" data-tip="The test rack: units run powered on, hour after hour, until they fail or the test ends">'
             f'<rect x="30" y="86" width="360" height="384" rx="8" fill="#fff" stroke="{INK}" stroke-width="4"/>')
    for i, sy in enumerate((200, 310, 420)):
        b.append(f'<line x1="30" y1="{sy}" x2="390" y2="{sy}" stroke="{INK}" stroke-width="4"/>')
    b.append('</g>')
    for row, sy in enumerate((200, 310, 420)):
        for c in range(5):
            x = 48 + c * 68
            failed = (row == 1 and c == 3)
            led = RED if failed else BMID
            tip = ("Unit that just failed: this is failure number r. Time to record the hours and update the CI." if failed
                   else f"Unit on test, shelf {row+1}, slot {c+1}: still running, no failure yet")
            b.append(unit(x, sy - 42, led, tip))
    # smoke from failed unit
    fx = 48 + 3 * 68 + 26
    b.append(f'<g id="tt-smoke" data-tip="Smoke: one unit has failed (r = 1)"><circle cx="{fx}" cy="262" r="11" fill="#e6dcdc" stroke="{INK}" stroke-width="1.5"/>'
             f'<circle cx="{fx+12}" cy="242" r="14" fill="#e6dcdc" stroke="{INK}" stroke-width="1.5"/>'
             f'<circle cx="{fx-4}" cy="216" r="17" fill="#e6dcdc" stroke="{INK}" stroke-width="1.5"/></g>')
    # clock
    b.append(f'<g id="tt-clock" data-tip="Test clock: hours on test so far (T)"><rect x="96" y="22" width="248" height="52" rx="8" fill="{NAVY}" stroke="{INK}" stroke-width="3"/>'
             f'<text x="220" y="58" font-size="30" font-weight="700" text-anchor="middle" fill="{YELS}">T = 499 hrs</text></g>')
    # people
    b.append(person(462, 470, "#c68642", "#2a1414", PURS, "bun", "Test engineer with a clipboard, logging hours", 1.0, True))
    b.append(person(558, 470, "#f1c9a5", "#6b3b1f", ROSE, "hijab", "Reliability analyst, watching the rack", 1.0))
    b.append(person(648, 470, "#8d5524", "#2a1414", YELS, "curly", "Technician, ready to swap the failed unit", 0.92))
    # speech bubble
    b.append(f'<g id="tt-bubble" data-tip="Test teams spend most of their lives waiting for failure number r">'
             f'<path d="M436 30 h250 a14 14 0 0 1 14 14 v98 a14 14 0 0 1 -14 14 h-134 l-30 24 l8 -24 h-94 a14 14 0 0 1 -14 -14 v-98 a14 14 0 0 1 14 -14 z" fill="#fff" stroke="{INK}" stroke-width="3"/>'
             f'<text x="562" y="68" font-size="22" text-anchor="middle" fill="{INK}">Hour 499.</text>'
             f'<text x="562" y="96" font-size="22" text-anchor="middle" fill="{INK}">Please, one more</text>'
             f'<text x="562" y="124" font-size="22" text-anchor="middle" fill="{RED}" font-weight="700">failure for r...</text></g>')
    return svg("tt", 720, 520, "A test team watching units on a rack",
               "Three engineers with clipboards watch a rack of units under test. A clock reads 499 hours and one unit is smoking.",
               "\n".join(b))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (("ci_diagram", ci_diagram), ("test_team", test_team)):
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print("wrote", OUT / f"{name}.svg")
