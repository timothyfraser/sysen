# slides_workshop_10_art.py -- SVG cartoon for the accelerated-testing slide (stdlib only).
# Three parts sweat inside a 125 C oven while three engineers (varied skin, hair, dress)
# time them with stopwatches: "accelerated life testing" as a spectator sport.
# Run from the repo root:  python3 functions/slides_workshop_10_art.py
RED, NAVY, GOLD, BLUE, SOFT = "#B31B1B", "#302050", "#F2B705", "#3880c0", "#dce8f8"
W, H = 560, 640

def drop(x, y, s=1.0):
    return (f'<path d="M{x} {y} q{-9*s} {16*s} 0 {22*s} q{9*s} {-6*s} 0 {-22*s}z" fill="#8fc4f0" stroke="{NAVY}" stroke-width="2"/>')

def sweaty_face(cx, cy, mood):
    mouth = {"wobble": f'<path d="M{cx-9} {cy+14} q4.5 -6 9 0 q4.5 6 9 0" stroke="{NAVY}" stroke-width="3" fill="none" stroke-linecap="round"/>',
             "o":      f'<ellipse cx="{cx}" cy="{cy+15}" rx="6" ry="8" fill="{NAVY}"/>',
             "grit":   f'<rect x="{cx-11}" y="{cy+10}" width="22" height="10" rx="3" fill="#fff" stroke="{NAVY}" stroke-width="2.5"/><path d="M{cx-4} {cy+10} v10 M{cx+4} {cy+10} v10" stroke="{NAVY}" stroke-width="2"/>'}[mood]
    return (f'<circle cx="{cx-11}" cy="{cy}" r="6" fill="#fff" stroke="{NAVY}" stroke-width="2"/><circle cx="{cx+11}" cy="{cy}" r="6" fill="#fff" stroke="{NAVY}" stroke-width="2"/>'
            f'<circle cx="{cx-11}" cy="{cy+1}" r="2.6" fill="{NAVY}"/><circle cx="{cx+11}" cy="{cy+1}" r="2.6" fill="{NAVY}"/>'
            f'<path d="M{cx-18} {cy-11} l12 4 M{cx+18} {cy-11} l-12 4" stroke="{NAVY}" stroke-width="3" stroke-linecap="round"/>{mouth}')

def person(cx, skin, hair, shirt, style, label, y=470, watch_side=1):
    """Torso cartoon centred on cx with a raised stopwatch; bottom edge is y+170."""
    hairs = {
        "puffs":  f'<circle cx="{cx-30}" cy="{y-30}" r="19" fill="{hair}"/><circle cx="{cx+30}" cy="{y-30}" r="19" fill="{hair}"/><path d="M{cx-34} {y-4} a34 34 0 0 1 68 0 q-34 -22 -68 0z" fill="{hair}"/>',
        "hijab":  f'<path d="M{cx-44} {y+58} q-8 -112 44 -112 q52 0 44 112 q-44 -26 -88 0z" fill="{hair}"/><ellipse cx="{cx}" cy="{y+2}" rx="30" ry="33" fill="{skin}"/>',
        "glasses":f'<path d="M{cx-34} {y-6} a34 30 0 0 1 68 0 q-34 -12 -68 0z" fill="{hair}"/><rect x="{cx-27}" y="{y-8}" width="22" height="16" rx="5" fill="none" stroke="{NAVY}" stroke-width="3"/><rect x="{cx+5}" y="{y-8}" width="22" height="16" rx="5" fill="none" stroke="{NAVY}" stroke-width="3"/><path d="M{cx-5} {y} h10" stroke="{NAVY}" stroke-width="3"/>',
    }[style]
    face = '' if style == "hijab" else f'<circle cx="{cx}" cy="{y}" r="33" fill="{skin}"/>'
    body = f'<path d="M{cx-62} {y+170} q0 -110 62 -110 q62 0 62 110z" fill="{shirt}"/>'
    neck = f'<rect x="{cx-12}" y="{y+22}" width="24" height="36" rx="8" fill="{skin}"/>'
    eyes = (f'<circle cx="{cx-12}" cy="{y+2}" r="4" fill="#1f1f1f"/><circle cx="{cx+12}" cy="{y+2}" r="4" fill="#1f1f1f"/>'
            f'<path d="M{cx-9} {y+16} q9 8 18 0" stroke="#1f1f1f" stroke-width="3" fill="none" stroke-linecap="round"/>')
    sx = cx + watch_side * 66
    arm = f'<path d="M{cx+watch_side*46} {y+82} L{sx} {y+34}" stroke="{skin}" stroke-width="16" stroke-linecap="round"/>'
    watch = (f'<g data-tip="Stopwatch: logging the time to failure"><rect x="{sx-4}" y="{y-26}" width="8" height="8" fill="{NAVY}"/>'
             f'<circle cx="{sx}" cy="{y+4}" r="24" fill="#fff" stroke="{NAVY}" stroke-width="4"/>'
             f'<path d="M{sx} {y+4} V{y-10} M{sx} {y+4} l10 8" stroke="{RED}" stroke-width="3.5" stroke-linecap="round"/></g>'
             f'<circle cx="{sx}" cy="{y+34}" r="10" fill="{skin}"/>')
    return f'<g data-tip="{label}">{body}{neck}{face}{hairs}{eyes}{arm}{watch}</g>'

heat = "".join(f'<path d="M{x} 36 q-10 -16 0 -30 q10 -14 0 -26" stroke="{RED}" stroke-width="4" fill="none" stroke-linecap="round" opacity=".55" transform="translate(0 22)"/>' for x in (150, 280, 410))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">Engineers time parts sweating in a hot oven</title>
<desc id="d">Three small electronic parts, a blue capacitor, a black chip and a grey resistor, sit on a rack inside a 125 degree oven, wide-eyed and sweating. Below, three engineers hold up stopwatches: a woman with afro puffs, a woman in a hijab and a man with glasses. One of them says the parts have 4,500 hours to fail, and counting.</desc>
<rect width="{W}" height="{H}" rx="18" fill="#f6f1ee"/>
{heat}
<g data-tip="The oven: 125 C stress, so failures arrive faster (that is the acceleration)">
  <rect x="50" y="62" width="460" height="288" rx="18" fill="#59596a" stroke="{NAVY}" stroke-width="4"/>
  <rect x="64" y="72" width="432" height="42" rx="8" fill="#3a3a48"/>
  <rect x="78" y="80" width="116" height="26" rx="5" fill="#1b1b24"/><text x="136" y="100" font-size="22" font-weight="700" text-anchor="middle" fill="#ff6a4a" font-family="monospace">125&#176;C</text>
  <circle cx="380" cy="93" r="14" fill="#d9d9e2" stroke="{NAVY}" stroke-width="3"/><path d="M380 93 l7 -8" stroke="{NAVY}" stroke-width="3"/>
  <circle cx="436" cy="93" r="14" fill="#d9d9e2" stroke="{NAVY}" stroke-width="3"/><path d="M436 93 l-7 -8" stroke="{NAVY}" stroke-width="3"/>
  <rect x="76" y="128" width="408" height="206" rx="12" fill="#f8c98a" stroke="{NAVY}" stroke-width="4"/>
  <rect x="86" y="138" width="388" height="186" rx="8" fill="#ffb25a" opacity=".55"/>
  <path d="M96 296 H464" stroke="#8a5a2a" stroke-width="5"/><path d="M96 306 H464" stroke="#8a5a2a" stroke-width="3" opacity=".5"/></g>
<g data-tip="Part 1, a capacitor: sweating (infant mortality candidate)">
  <rect x="116" y="212" width="64" height="84" rx="8" fill="{BLUE}" stroke="{NAVY}" stroke-width="3"/><ellipse cx="148" cy="212" rx="32" ry="8" fill="#6fa6d8" stroke="{NAVY}" stroke-width="3"/>
  {sweaty_face(148, 246, "wobble")}{drop(112, 232)}{drop(186, 248, .8)}</g>
<g data-tip="Part 2, a chip: gritting its teeth">
  <path d="M232 296 v14 M252 296 v14 M272 296 v14 M292 296 v14 M312 296 v14" stroke="#777" stroke-width="5" stroke-linecap="round"/>
  <rect x="222" y="226" width="100" height="72" rx="8" fill="#2f2f3a" stroke="{NAVY}" stroke-width="3"/>
  {sweaty_face(272, 252, "grit")}{drop(214, 250)}{drop(332, 244, .8)}{drop(300, 214, .7)}</g>
<g data-tip="Part 3, a resistor: please, just let it be Friday">
  <rect x="368" y="236" width="86" height="58" rx="22" fill="#d8c9a8" stroke="{NAVY}" stroke-width="3"/>
  <path d="M382 238 v54 M394 238 v54 M430 238 v54 M442 238 v54" stroke="{RED}" stroke-width="7"/>
  {sweaty_face(412, 258, "o")}
  <path d="M346 266 h22 M454 266 h20" stroke="#777" stroke-width="5" stroke-linecap="round"/>{drop(358, 220, .8)}{drop(466, 232)}</g>
<g data-tip="The caption of every life test: patience, but at 125 C">
  <path d="M270 392 L300 436 L330 392z" fill="#fff" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>
  <rect x="70" y="350" width="420" height="46" rx="12" fill="#fff" stroke="{NAVY}" stroke-width="3"/>
  <path d="M274 396 h52" stroke="#fff" stroke-width="5"/>
  <text x="280" y="381" font-size="22" font-weight="700" text-anchor="middle" fill="{NAVY}">Fail faster, please. We have lunch.</text></g>
{person(110, "#8d5a3b", "#1f1410", RED, "puffs", "Engineer with afro puffs, timing the capacitor", watch_side=1)}
{person(290, "#e0a878", "#302050", "#3880c0", "hijab", "Engineer in a hijab, timing the chip", watch_side=1)}
{person(450, "#f1c9a0", "#2b1a10", NAVY, "glasses", "Engineer with glasses, timing the resistor", watch_side=1)}
</svg>'''
open("docs-v3/images/slides/workshop-10/art_oven_stopwatch.svg", "w", encoding="utf-8").write(svg)
print("wrote art_oven_stopwatch.svg")
