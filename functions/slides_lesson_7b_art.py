# slides_lesson_7b_art.py -- SVG cartoon for the Lifetime Light Bulb Company slide (stdlib only).
# Three coworkers of different backgrounds look at a burnt-out bulb on a test bench, stopwatch beside it.
# Run from the repo root:  python3 functions/slides_lesson_7b_art.py
RED, NAVY, GOLD, PALE = "#B31B1B", "#302050", "#F2B705", "#FFF3C4"

def person(cx, skin, hair, shirt, hair_style, label):
    """A seated-torso cartoon person centred on cx; head circle, hair cap/bun/curls, shoulders."""
    y = 250
    hairs = {
        "short": f'<path d="M{cx-34} {y-8} a34 34 0 0 1 68 0 q-34 -22 -68 0z" fill="{hair}"/>',
        "bun":   f'<circle cx="{cx}" cy="{y-52}" r="16" fill="{hair}"/><path d="M{cx-35} {y-4} a35 35 0 0 1 70 0 q-35 -26 -70 0z" fill="{hair}"/>',
        "curly": "".join(f'<circle cx="{cx+dx}" cy="{y-dy}" r="15" fill="{hair}"/>' for dx, dy in
                         [(-26, 14), (-12, 32), (6, 36), (22, 28), (32, 10)]),
    }[hair_style]
    return f'''<g data-tip="{label}">
  <path d="M{cx-62} 400 q0 -92 62 -92 q62 0 62 92z" fill="{shirt}"/>
  <rect x="{cx-12}" y="{y+22}" width="24" height="34" rx="8" fill="{skin}"/>
  <circle cx="{cx}" cy="{y}" r="36" fill="{skin}"/>{hairs}
  <circle cx="{cx-13}" cy="{y+2}" r="4" fill="#1f1f1f"/><circle cx="{cx+13}" cy="{y+2}" r="4" fill="#1f1f1f"/>
  <path d="M{cx-12} {y+20} q12 -9 24 0" stroke="#1f1f1f" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M{cx-22} {y-12} l12 -4 M{cx+10} {y-16} l12 4" stroke="#1f1f1f" stroke-width="3" stroke-linecap="round"/>
</g>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 130 720 310" role="img" aria-labelledby="t d">
<title id="t">Three coworkers examine a burnt-out light bulb</title>
<desc id="d">A woman with a bun, a man with short hair and a person with curly hair look at a burnt-out bulb with a broken filament; a stopwatch beside it shows the elapsed time.</desc>
<rect y="130" width="720" height="310" rx="18" fill="#f6f1ee"/>
<rect x="0" y="372" width="720" height="68" fill="{NAVY}" opacity=".12"/>
{person(110, "#8D5524", "#2b1a10", RED, "curly", "Test engineer, curly hair")}
{person(250, "#F1C27D", "#4a2c17", NAVY, "bun", "Quality analyst, hair in a bun")}
{person(390, "#C68642", "#1f1f1f", "#7a7a86", "short", "Lab technician, short hair")}
<g data-tip="A burnt-out bulb: the filament snapped after 135 days on test">
  <rect x="548" y="318" width="64" height="30" rx="6" fill="#8a8a95"/>
  <rect x="552" y="338" width="56" height="8" fill="#6a6a75"/>
  <circle cx="580" cy="236" r="72" fill="{PALE}" stroke="{NAVY}" stroke-width="5"/>
  <path d="M556 306 L556 262 M604 306 L604 262" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/>
  <path d="M556 262 L568 230 M604 262 L592 230" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/>
  <path d="M568 230 l5 -8 M592 230 l-5 -8" stroke="{RED}" stroke-width="5" stroke-linecap="round"/>
  <path d="M566 190 l-16 -16 M580 184 l0 -24 M594 190 l16 -16" stroke="#8a8a95" stroke-width="4" stroke-linecap="round" stroke-dasharray="3 8"/>
</g>
<g data-tip="Stopwatch: time to failure is the data">
  <rect x="636" y="318" width="22" height="10" rx="3" fill="{NAVY}"/>
  <circle cx="647" cy="365" r="38" fill="#fff" stroke="{NAVY}" stroke-width="5"/>
  <path d="M647 365 L647 340 M647 365 L664 376" stroke="{RED}" stroke-width="5" stroke-linecap="round"/>
</g>
</svg>'''
open("docs-v3/images/slides/lesson-7b/art_bulb_team.svg", "w", encoding="utf-8").write(svg)
print("wrote art_bulb_team.svg")
