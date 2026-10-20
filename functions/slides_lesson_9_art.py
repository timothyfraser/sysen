# slides_lesson_9_art.py -- SVG cartoon for Lesson 12 (Weibull, Gamma & Lognormal), stdlib only.
#   art_bearing_bets.svg : three engineers place bets on which of four bearings on a test rig fails first
#                          (a series system fails at the FIRST failure: T = min(T1, ..., Tn))
# Run from the repo root:  python3 functions/slides_lesson_9_art.py
RED, NAVY, GOLD, PALE, BLUE = "#B31B1B", "#302050", "#F2B705", "#FFF3C4", "#a0c0f0"
OUT = "docs-v3/images/slides/lesson-9/"
FONT = "font-family=\"'Source Sans 3', sans-serif\""


def head(cx, y, skin, hair, style, mood="smile"):
    hairs = {
        "short": f'<path d="M{cx-30} {y-6} a30 30 0 0 1 60 0 q-30 -20 -60 0z" fill="{hair}"/>',
        "bun":   f'<circle cx="{cx}" cy="{y-44}" r="13" fill="{hair}"/><path d="M{cx-31} {y-3} a31 31 0 0 1 62 0 q-31 -24 -62 0z" fill="{hair}"/>',
        "curly": "".join(f'<circle cx="{cx+dx}" cy="{y-dy}" r="13" fill="{hair}"/>' for dx, dy in [(-22, 12), (-10, 28), (6, 31), (20, 24), (28, 8)]),
        "hijab": f'<path d="M{cx-38} {y+40} L{cx-38} {y-2} a38 38 0 0 1 76 0 L{cx+38} {y+40} q-38 14 -76 0z" fill="{hair}"/>',
    }[style]
    mouth = {"grin": f'<path d="M{cx-12} {y+13} q12 12 24 0z" fill="#1f1f1f"/>',
             "o":    f'<circle cx="{cx}" cy="{y+17}" r="5" fill="#1f1f1f"/>',
             "smile": f'<path d="M{cx-10} {y+16} q10 8 20 0" stroke="#1f1f1f" stroke-width="3" fill="none" stroke-linecap="round"/>'}[mood]
    face = f'<circle cx="{cx}" cy="{y}" r="31" fill="{skin}"/>'
    # a hijab sits behind the face; other hair styles sit on top of it
    layers = (hairs + face) if style == "hijab" else (face + hairs)
    return (layers + f'<circle cx="{cx-11}" cy="{y+1}" r="3.6" fill="#1f1f1f"/>'
            f'<circle cx="{cx+11}" cy="{y+1}" r="3.6" fill="#1f1f1f"/>{mouth}')


def bettor(cx, skin, hair, shirt, style, mood, pick, tip, cash):
    y = 200
    return f'''<g data-tip="{tip}">
  <path d="M{cx-52} 372 q0 -112 52 -112 q52 0 52 112z" fill="{shirt}"/>
  <rect x="{cx-10}" y="{y+22}" width="20" height="34" rx="7" fill="{skin}"/>
  {head(cx, y, skin, hair, style, mood)}
  <path d="M{cx+30} 300 q40 -10 46 -60" stroke="{shirt}" stroke-width="20" fill="none" stroke-linecap="round"/>
  <rect x="{cx+52}" y="200" width="56" height="40" rx="5" fill="#fff" stroke="{NAVY}" stroke-width="3" transform="rotate(-8 {cx+80} 220)"/>
  <text x="{cx+80}" y="227" text-anchor="middle" {FONT} font-size="20" font-weight="700" fill="{RED}" transform="rotate(-8 {cx+80} 220)">#{pick}</text>
  <text x="{cx}" y="400" text-anchor="middle" {FONT} font-size="17" font-weight="700" fill="{NAVY}">{cash}</text>
</g>'''


def bearing(x, n, smoke=False):
    s = (f'<path d="M{x-6} 432 q-14 -18 0 -34 q14 -16 0 -32" stroke="#9a9a9a" stroke-width="7" fill="none" stroke-linecap="round" opacity=".8"/>'
         if smoke else "")
    return f'''<g data-tip="Bearing #{n}{' (smoking: looks like the first failure)' if smoke else ''}">
  <circle cx="{x}" cy="470" r="30" fill="#c9c9d2" stroke="{NAVY}" stroke-width="4"/>
  <circle cx="{x}" cy="470" r="13" fill="#f6f1ee" stroke="{NAVY}" stroke-width="3"/>
  {''.join(f'<circle cx="{x+21*c}" cy="{470+21*s_}" r="4" fill="{NAVY}"/>' for c, s_ in [(1,0),(0,1),(-1,0),(0,-1),(.71,.71),(-.71,.71),(.71,-.71),(-.71,-.71)])}
  <text x="{x}" y="525" text-anchor="middle" {FONT} font-size="20" font-weight="700" fill="{NAVY}">#{n}</text>
  {s}
</g>'''


svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 20 640 520" role="img" aria-labelledby="t d">
<title id="t">Three engineers bet on which bearing fails first</title>
<desc id="d">A woman in a hijab, a curly-haired man and a woman with a bun each hold up a betting slip for a different bearing on a four-bearing test rig; a chalkboard reads "Which fails first? T = min(T1..T4)", and bearing #3 is already smoking.</desc>
<rect y="20" width="640" height="520" rx="18" fill="#f6f1ee"/>
<g data-tip="The betting board: a series system fails when its FIRST component fails">
  <rect x="150" y="34" width="340" height="96" rx="8" fill="{NAVY}"/>
  <rect x="150" y="34" width="340" height="96" rx="8" fill="none" stroke="#8a6a3a" stroke-width="7"/>
  <text x="320" y="72" text-anchor="middle" {FONT} font-size="26" font-weight="700" fill="#fff">Which fails first?</text>
  <text x="320" y="110" text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="24" fill="{GOLD}">T = min(T1, T2, T3, T4)</text>
</g>
{bettor(105, "#C68642", "#5a2e5a", RED, "hijab", "grin", 2, "Bets on #2: oldest batch", "$5")}
{bettor(300, "#8D5524", "#1f1f1f", "#7a7a86", "curly", "o", 3, "Bets on #3, and it is already smoking", "$5")}
{bettor(495, "#F1C27D", "#4a2c17", NAVY, "bun", "smile", 4, "Bets on #4: the m = 4 wear-out one", "$5")}
<rect x="40" y="430" width="560" height="14" rx="6" fill="{NAVY}" opacity=".25"/>
<rect x="60" y="470" width="520" height="8" fill="{NAVY}"/>
{bearing(150, 1)}{bearing(270, 2)}{bearing(390, 3, smoke=True)}{bearing(510, 4)}
</svg>'''

with open(OUT + "art_bearing_bets.svg", "w", encoding="utf-8") as fh:
    fh.write(svg)
print("wrote", OUT + "art_bearing_bets.svg")
