# slides_workshop_9_art.py -- SVG cartoon for the "Why estimate parameters?" slide (stdlib only).
# Two engineers interrogate a failed capacitor under a desk lamp: failure data as a witness.
# Run from the repo root:  python3 functions/slides_workshop_9_art.py
RED, NAVY, GOLD, BLUE, SOFT = "#B31B1B", "#302050", "#F2B705", "#3880c0", "#dce8f8"

def person(cx, skin, hair, shirt, style, label, y=300):
    """Torso cartoon centred on cx: head circle, hair, shoulders; bottom edge is y+150."""
    hairs = {
        "bun":   f'<circle cx="{cx}" cy="{y-50}" r="16" fill="{hair}"/><path d="M{cx-35} {y-2} a35 35 0 0 1 70 0 q-35 -26 -70 0z" fill="{hair}"/>',
        "curly": "".join(f'<circle cx="{cx+dx}" cy="{y-dy}" r="15" fill="{hair}"/>' for dx, dy in
                         [(-26, 14), (-12, 32), (6, 36), (22, 28), (32, 10)]),
    }[style]
    face = f'<circle cx="{cx}" cy="{y}" r="33" fill="{skin}"/>'
    body = f'<path d="M{cx-60} {y+150} q0 -96 60 -96 q60 0 60 96z" fill="{shirt}"/>'
    neck = f'<rect x="{cx-12}" y="{y+22}" width="24" height="34" rx="8" fill="{skin}"/>'
    eyes = (f'<circle cx="{cx-12}" cy="{y+2}" r="4" fill="#1f1f1f"/><circle cx="{cx+12}" cy="{y+2}" r="4" fill="#1f1f1f"/>'
            f'<path d="M{cx-12} {y-10} l9 3 M{cx+12} {y-10} l-9 3" stroke="#1f1f1f" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M{cx-10} {y+20} h20" stroke="#1f1f1f" stroke-width="3" fill="none" stroke-linecap="round"/>')
    return f'<g data-tip="{label}">{body}{neck}{face}{hairs}{eyes}</g>'

def bubble(x, y, w, h, lines, tail_x, tail_y):
    """Speech bubble with a tail pointing at (tail_x, tail_y)."""
    tx = "".join(f'<text x="{x+w/2}" y="{y+30+i*28}" font-size="23" font-weight="700" text-anchor="middle" fill="{NAVY}">{t}</text>'
                 for i, t in enumerate(lines))
    return (f'<path d="M{x+w/2-14} {y+h-2} L{tail_x} {tail_y} L{x+w/2+16} {y+h-2}z" fill="#fff" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#fff" stroke="{NAVY}" stroke-width="3"/>'
            f'<path d="M{x+w/2-11} {y+h} h27" stroke="#fff" stroke-width="5"/>{tx}')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 540" role="img" aria-labelledby="t d">
<title id="t">Two engineers interrogate a failed capacitor under a desk lamp</title>
<desc id="d">A woman with a bun and a man with curly hair lean over a table. Between them sits a blue capacitor with crossed-out eyes and a scorched top. One engineer asks where it was at 2,920 hours; the capacitor asks for a lawyer.</desc>
<rect width="560" height="540" rx="18" fill="#f6f1ee"/>
<path d="M280 70 L150 430 H410z" fill="{GOLD}" opacity=".22"/>
<g data-tip="The interrogation lamp: every failure time is a clue"><path d="M280 0 V44" stroke="{NAVY}" stroke-width="4"/>
  <path d="M236 82 q44 -60 88 0z" fill="{RED}" stroke="{NAVY}" stroke-width="3"/><circle cx="280" cy="84" r="11" fill="{GOLD}" stroke="{NAVY}" stroke-width="3"/></g>
{person(88, "#C68642", "#2b1a10", RED, "bun", "Engineer with her hair in a bun, stern")}
{person(472, "#5a3a22", "#1f1f1f", NAVY, "curly", "Engineer with curly hair, stern")}
<rect x="0" y="420" width="560" height="120" rx="0" fill="#c9a77c"/><rect x="0" y="420" width="560" height="10" fill="#a98558"/>
<g data-tip="The suspect: a capacitor that failed early (shape m = 0.55 means infant mortality)">
  <path d="M258 420 v28 M302 420 v28" stroke="#555" stroke-width="6" stroke-linecap="round"/>
  <rect x="232" y="290" width="96" height="130" rx="10" fill="{BLUE}" stroke="{NAVY}" stroke-width="3"/>
  <ellipse cx="280" cy="290" rx="48" ry="12" fill="#6fa6d8" stroke="{NAVY}" stroke-width="3"/>
  <rect x="232" y="330" width="22" height="90" fill="#fff" opacity=".85"/><text x="243" y="394" font-size="22" font-weight="700" text-anchor="middle" fill="{NAVY}">&#8722;</text>
  <path d="M262 276 q-6 -22 10 -34 q-2 20 14 24 q6 -14 -4 -26 q22 12 12 38z" fill="#555" opacity=".8"/>
  <path d="M252 336 l22 22 M274 336 l-22 22 M286 336 l22 22 M308 336 l-22 22" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/>
  <path d="M258 392 q22 -14 44 0" stroke="{NAVY}" stroke-width="5" fill="none" stroke-linecap="round"/></g>
{bubble(14, 70, 232, 66, ["Where were you at", "2,920 hours?"], 120, 235)}
{bubble(318, 150, 228, 66, ["I want a lawyer.", ""], 310, 285)}
</svg>'''
open("docs-v3/images/slides/workshop-9/art_interrogation.svg", "w", encoding="utf-8").write(svg)
print("wrote art_interrogation.svg")
