# slides_workshop_11_art.py -- SVG cartoon for the "Today's data" slide (stdlib only).
# Four neighbours of different backgrounds stand arm in arm in front of a row of houses,
# the sea behind them: X (damage) and Y (social capital) made into people.
# Run from the repo root:  python3 functions/slides_workshop_11_art.py
RED, NAVY, GOLD, SEA, FOAM = "#B31B1B", "#302050", "#F2B705", "#a0c0f0", "#eaf2fd"

def person(cx, skin, hair, shirt, style, label, y=372):
    """Torso cartoon centred on cx: head circle, hair/scarf, shoulders; the bottom edge is y+~150."""
    hairs = {
        "short": f'<path d="M{cx-34} {y-6} a34 34 0 0 1 68 0 q-34 -22 -68 0z" fill="{hair}"/>',
        "bun":   f'<circle cx="{cx}" cy="{y-50}" r="16" fill="{hair}"/><path d="M{cx-35} {y-2} a35 35 0 0 1 70 0 q-35 -26 -70 0z" fill="{hair}"/>',
        "curly": "".join(f'<circle cx="{cx+dx}" cy="{y-dy}" r="15" fill="{hair}"/>' for dx, dy in
                         [(-26, 14), (-12, 32), (6, 36), (22, 28), (32, 10)]),
        "scarf": f'<path d="M{cx-42} {y+26} a42 46 0 0 1 84 0 q0 30 -22 34 l-40 0 q-22 -4 -22 -34z" fill="{hair}"/>',
    }[style]
    face = f'<circle cx="{cx}" cy="{y}" r="33" fill="{skin}"/>'
    # a scarf frames the face: draw scarf first, then the face on top
    body = f'<path d="M{cx-60} {y+150} q0 -96 60 -96 q60 0 60 96z" fill="{shirt}"/>'
    neck = f'<rect x="{cx-12}" y="{y+22}" width="24" height="34" rx="8" fill="{skin}"/>'
    eyes = (f'<circle cx="{cx-12}" cy="{y+2}" r="4" fill="#1f1f1f"/><circle cx="{cx+12}" cy="{y+2}" r="4" fill="#1f1f1f"/>'
            f'<path d="M{cx-11} {y+16} q11 9 22 0" stroke="#1f1f1f" stroke-width="3" fill="none" stroke-linecap="round"/>')
    if style == "scarf":
        return f'<g data-tip="{label}">{body}{neck}{hairs}{face}{eyes}</g>'
    return f'<g data-tip="{label}">{body}{neck}{face}{hairs}{eyes}</g>'

def house(x, y, w, h, wall, roof, label, damaged=False):
    door = f'<rect x="{x+w/2-11}" y="{y+h-38}" width="22" height="38" rx="3" fill="{NAVY}"/>'
    win = f'<rect x="{x+10}" y="{y+22}" width="22" height="22" rx="3" fill="{FOAM}" stroke="{NAVY}" stroke-width="2"/>'
    crack = (f'<path d="M{x+w-26} {y+4} l8 18 l-10 12 l10 14" stroke="{NAVY}" stroke-width="3" fill="none" stroke-linecap="round"/>'
             if damaged else "")
    return (f'<g data-tip="{label}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{wall}" stroke="{NAVY}" stroke-width="3"/>'
            f'<path d="M{x-10} {y} L{x+w/2} {y-44} L{x+w+10} {y}z" fill="{roof}" stroke="{NAVY}" stroke-width="3"/>{door}{win}{crack}</g>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 540" role="img" aria-labelledby="t d">
<title id="t">Four neighbours stand arm in arm in front of coastal houses</title>
<desc id="d">A woman with curly hair, a man with short hair, a woman in a headscarf and a person with a bun stand side by side in front of a row of small houses; waves sit behind the houses on the left and a heart floats above the group.</desc>
<rect width="560" height="540" rx="18" fill="#f6f1ee"/>
<rect width="560" height="306" rx="18" fill="{FOAM}"/>
<g data-tip="The sea: the tsunami (X, damage) came from here">
  <path d="M0 306 V176 q60 -52 124 -4 q40 34 56 134z" fill="{SEA}"/>
  <path d="M0 176 q60 -52 124 -4 q22 18 36 50" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" stroke-dasharray="30 14"/>
</g>
{house(250, 214, 82, 92, "#fff3c4", RED, "A house the tsunami reached: damaged", True)}
{house(356, 204, 86, 102, "#dce8f8", NAVY, "A house that was not hit")}
{house(462, 218, 80, 88, "#fde0d4", "#7a7a86", "A house that was not hit")}
<rect y="306" width="560" height="234" fill="#e8dfd8"/>
<g data-tip="Social capital (Y): neighbours who know, trust and help each other">
  <path d="M0 40 C-60 0 -50 -50 -25 -50 C-10 -50 0 -40 0 -30 C0 -40 10 -50 25 -50 C50 -50 60 0 0 40z" transform="translate(300 92) scale(1.25)" fill="{RED}"/>
</g>
{person(85, "#8D5524", "#2b1a10", RED, "curly", "Neighbour with curly hair")}
{person(215, "#F1C27D", "#3a2414", NAVY, "short", "Neighbour with short hair")}
{person(345, "#C68642", "#5b6bb0", "#7a7a86", "scarf", "Neighbour in a headscarf")}
{person(475, "#5a3a22", "#1f1f1f", GOLD, "bun", "Neighbour with hair in a bun")}
</svg>'''
open("docs-v3/images/slides/workshop-11/art_neighbours.svg", "w", encoding="utf-8").write(svg)
print("wrote art_neighbours.svg")
