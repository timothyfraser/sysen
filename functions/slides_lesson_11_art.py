# slides_lesson_11_art.py -- SVG cartoons for Lesson 10 (stdlib only).
#   art_repeat_measure.svg : three people weigh the SAME apple and get three different readings (experimental error)
#   art_bikeshare.svg      : riders of different ages on bikeshare bikes, one under a rain cloud (trip generation)
# Run from the repo root:  python3 functions/slides_lesson_11_art.py
RED, NAVY, GOLD, PALE, BLUE, LAV = "#B31B1B", "#302050", "#F2B705", "#FFF3C4", "#a0c0f0", "#b0a8d0"
OUT = "docs-v3/images/slides/lesson-11/"

def head(cx, y, skin, hair, style, mood="smile"):
    hairs = {
        "short": f'<path d="M{cx-30} {y-6} a30 30 0 0 1 60 0 q-30 -20 -60 0z" fill="{hair}"/>',
        "bun":   f'<circle cx="{cx}" cy="{y-44}" r="13" fill="{hair}"/><path d="M{cx-31} {y-3} a31 31 0 0 1 62 0 q-31 -24 -62 0z" fill="{hair}"/>',
        "curly": "".join(f'<circle cx="{cx+dx}" cy="{y-dy}" r="13" fill="{hair}"/>' for dx, dy in [(-22, 12), (-10, 28), (6, 31), (20, 24), (28, 8)]),
        "bald":  f'<path d="M{cx-31} {y+2} q-4 -14 4 -18 M{cx+31} {y+2} q4 -14 -4 -18" stroke="{hair}" stroke-width="7" fill="none" stroke-linecap="round"/>',
        "long":  f'<path d="M{cx-32} {y+30} L{cx-32} {y-4} a32 32 0 0 1 64 0 L{cx+32} {y+30} q-8 -30 -32 -36 q-24 6 -32 36z" fill="{hair}"/>',
    }[style]
    mouth = {"smile": f'<path d="M{cx-10} {y+16} q10 8 20 0" stroke="#1f1f1f" stroke-width="3" fill="none" stroke-linecap="round"/>',
             "o":     f'<circle cx="{cx}" cy="{y+17}" r="5" fill="#1f1f1f"/>',
             "flat":  f'<path d="M{cx-9} {y+17} l18 -2" stroke="#1f1f1f" stroke-width="3" stroke-linecap="round"/>'}[mood]
    return (f'<circle cx="{cx}" cy="{y}" r="31" fill="{skin}"/>{hairs}'
            f'<circle cx="{cx-11}" cy="{y+1}" r="3.6" fill="#1f1f1f"/><circle cx="{cx+11}" cy="{y+1}" r="3.6" fill="#1f1f1f"/>{mouth}')

def standing(cx, skin, hair, shirt, style, mood, tip, reading, bubble_dx=0):
    y = 170
    return f'''<g data-tip="{tip}">
  <path d="M{cx-52} 330 q0 -112 52 -112 q52 0 52 112z" fill="{shirt}"/>
  <rect x="{cx-10}" y="{y+22}" width="20" height="34" rx="7" fill="{skin}"/>
  {head(cx, y, skin, hair, style, mood)}
  <rect x="{cx-58+bubble_dx}" y="62" width="116" height="40" rx="14" fill="#fff" stroke="{NAVY}" stroke-width="3"/>
  <path d="M{cx-8+bubble_dx} 101 l6 22 l10 -22z" fill="#fff" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>
  <rect x="{cx-7+bubble_dx}" y="98" width="16" height="6" fill="#fff"/>
  <text x="{cx+bubble_dx}" y="90" text-anchor="middle" font-family="'Source Sans 3', sans-serif" font-size="22" font-weight="700" fill="{RED}">{reading}</text>
</g>'''

measure = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 40 640 380" role="img" aria-labelledby="t d">
<title id="t">Three people weigh the same apple and get three different readings</title>
<desc id="d">A woman with a bun reads 151.2 g, a bald man reads 150.6 g and a curly-haired person reads 151.9 g, all for one apple on one kitchen scale; a sticky note on the scale says "same apple!".</desc>
<rect y="40" width="640" height="380" rx="18" fill="#f6f1ee"/>
<rect x="0" y="330" width="640" height="90" fill="{NAVY}" opacity=".12"/>
{standing(110, "#F1C27D", "#4a2c17", NAVY, "bun", "smile", "Reading 1: 151.2 g", "151.2 g")}
{standing(320, "#8D5524", "#2b1a10", "#7a7a86", "bald", "o", "Reading 2: 150.6 g, same apple", "150.6 g")}
{standing(530, "#C68642", "#1f1f1f", RED, "curly", "flat", "Reading 3: 151.9 g, still the same apple", "151.9 g")}
<g data-tip="One apple, one scale: the spread between readings is experimental error">
  <rect x="250" y="352" width="140" height="44" rx="10" fill="#fff" stroke="{NAVY}" stroke-width="4"/>
  <rect x="285" y="362" width="70" height="22" rx="4" fill="{PALE}" stroke="{NAVY}" stroke-width="2"/><text x="320" y="379" text-anchor="middle" font-family="monospace" font-size="16" font-weight="700" fill="{RED}">???.? g</text>
  <circle cx="320" cy="328" r="26" fill="{RED}"/><path d="M320 304 q4 -12 12 -14" stroke="#5a3a1a" stroke-width="4" fill="none" stroke-linecap="round"/>
  <rect x="396" y="350" width="96" height="40" fill="{GOLD}" transform="rotate(6 444 370)"/>
  <text x="444" y="376" text-anchor="middle" font-family="'Source Sans 3', sans-serif" font-size="17" font-weight="700" fill="{NAVY}" transform="rotate(6 444 370)">same apple!</text>
</g>
</svg>'''

def rider(x, skin, hair, shirt, style, bike, tip, mood="smile"):
    by = 330
    return f'''<g data-tip="{tip}">
  <circle cx="{x-50}" cy="{by}" r="34" fill="none" stroke="{NAVY}" stroke-width="6"/>
  <circle cx="{x+60}" cy="{by}" r="34" fill="none" stroke="{NAVY}" stroke-width="6"/>
  <path d="M{x-50} {by} L{x-5} {by-50} L{x+40} {by-50} L{x+60} {by} M{x-5} {by-50} L{x+10} {by} L{x+40} {by-50} M{x+40} {by-50} l8 -26 l18 0" stroke="{bike}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="{x-24}" y="{by-62}" width="34" height="9" rx="4" fill="{NAVY}"/>
  <rect x="{x+44}" y="{by-90}" width="34" height="22" rx="4" fill="{bike}" opacity=".9"/>
  <path d="M{x-6} {by-60} L{x+8} {by-130} L{x+30} {by-128} L{x+56} {by-82}" stroke="{shirt}" stroke-width="26" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M{x-6} {by-60} L{x+18} {by-28} L{x+12} {by}" stroke="{NAVY}" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  {head(x+14, by-160, skin, hair, style, mood)}
</g>'''

bikes = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 40 680 360" role="img" aria-labelledby="t d">
<title id="t">Bikeshare riders of different ages; one rides under a rain cloud</title>
<desc id="d">An older bald rider in a red jacket and a young woman with long hair ride blue bikeshare bikes on a sunny side of the street; a third rider with curly hair pedals under a small grey rain cloud.</desc>
<rect y="40" width="680" height="360" rx="18" fill="#f6f1ee"/>
<rect x="0" y="364" width="680" height="36" fill="{NAVY}" opacity=".18"/>
<g data-tip="Sunny: more trips"><circle cx="90" cy="95" r="30" fill="{GOLD}"/>{"".join(f'<path d="M{90+44*c:.0f} {95+44*s:.0f} l{12*c:.0f} {12*s:.0f}" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/>' for c, s in [(1,0),(-1,0),(0,1),(0,-1),(.7,.7),(-.7,.7),(.7,-.7),(-.7,-.7)])}</g>
{rider(140, "#E0AC69", "#9a9a9a", RED, "bald", BLUE, "Weekend rider: a weekend changes the trip count")}
{rider(345, "#5C3A21", "#1f1f1f", LAV, "long", BLUE, "Weekday commuter")}
{rider(545, "#F1C27D", "#7a4a20", NAVY, "curly", BLUE, "Rain: fewer trips (the weather coefficient)", "flat")}
<g data-tip="Rain: fewer trips (the weather coefficient)">
  <path d="M500 96 a26 26 0 0 1 40 -20 a32 32 0 0 1 58 12 a22 22 0 0 1 -6 42 l-88 0 a18 18 0 0 1 -4 -34z" fill="#9a9aa6"/>
  {"".join(f'<path d="M{x} 142 l-6 16" stroke="{BLUE}" stroke-width="4" stroke-linecap="round"/>' for x in (518, 540, 562, 584))}
</g>
</svg>'''

open(OUT + "art_repeat_measure.svg", "w", encoding="utf-8").write(measure)
open(OUT + "art_bikeshare.svg", "w", encoding="utf-8").write(bikes)
print("wrote art_repeat_measure.svg, art_bikeshare.svg")
