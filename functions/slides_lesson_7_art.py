# slides_lesson_7_art.py -- SVG cartoon for Lesson 11 "When should we apply the Exponential Distribution?"
# (stdlib only). Three coworkers of different backgrounds study a whiteboard bathtub curve;
# a rubber duck floats along the flat useful-life period, which is where the exponential applies.
# Run from the sigma repo root:  python3 functions/slides_lesson_7_art.py
# Writes docs-v3/images/slides/lesson-7/art_bathtub_team.svg
RED, NAVY, GOLD, PALE = "#B31B1B", "#302050", "#F2B705", "#FFF3C4"
Y = 420  # head centre

def person(cx, skin, hair, shirt, style, label):
    hairs = {
        "curly": "".join(f'<circle cx="{cx+dx}" cy="{Y-dy}" r="15" fill="{hair}"/>' for dx, dy in
                         [(-26, 14), (-12, 32), (6, 36), (22, 28), (32, 10)]),
        "hijab": f'<path d="M{cx-44} {Y+44} q-6 -92 44 -92 q50 0 44 92 q-22 -18 -44 -18 q-22 0 -44 18z" fill="{hair}"/>'
                 f'<ellipse cx="{cx}" cy="{Y+2}" rx="31" ry="34" fill="{skin}"/>',
        "short": f'<path d="M{cx-34} {Y-8} a34 34 0 0 1 68 0 q-34 -22 -68 0z" fill="{hair}"/>',
    }[style]
    head = "" if style == "hijab" else f'<circle cx="{cx}" cy="{Y}" r="36" fill="{skin}"/>'
    glasses = (f'<circle cx="{cx-13}" cy="{Y+2}" r="10" fill="none" stroke="#1f1f1f" stroke-width="3"/>'
               f'<circle cx="{cx+13}" cy="{Y+2}" r="10" fill="none" stroke="#1f1f1f" stroke-width="3"/>'
               f'<path d="M{cx-3} {Y+2} h6" stroke="#1f1f1f" stroke-width="3"/>') if style == "short" else ""
    return f'''<g data-tip="{label}">
  <path d="M{cx-62} 560 q0 -92 62 -92 q62 0 62 92z" fill="{shirt}"/>
  <rect x="{cx-12}" y="{Y+22}" width="24" height="40" rx="8" fill="{skin}"/>
  {head}{hairs}
  <circle cx="{cx-13}" cy="{Y+2}" r="4" fill="#1f1f1f"/><circle cx="{cx+13}" cy="{Y+2}" r="4" fill="#1f1f1f"/>{glasses}
  <path d="M{cx-12} {Y+20} q12 9 24 0" stroke="#1f1f1f" stroke-width="3" fill="none" stroke-linecap="round"/>
</g>'''

# bathtub curve on the whiteboard (board spans x 50..430, y 50..300)
curve = "M70 80 C84 230 110 262 160 266 L330 266 C390 262 410 200 420 100"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 560" role="img" aria-labelledby="t d">
<title id="t">Three coworkers study a bathtub curve on a whiteboard</title>
<desc id="d">A whiteboard shows a bathtub-shaped failure rate curve with a yellow rubber duck floating along its flat bottom. In front of it, a person with curly hair, a person in a headscarf and a person with glasses look at it.</desc>
<rect width="480" height="560" rx="18" fill="#f6f1ee"/>
<g data-tip="Whiteboard: the bathtub curve of failure rate over time">
  <rect x="40" y="36" width="400" height="290" rx="10" fill="#fff" stroke="{NAVY}" stroke-width="6"/>
  <path d="M70 60 V292 H420" fill="none" stroke="#1f1f1f" stroke-width="3"/>
  <path d="{curve}" fill="none" stroke="{RED}" stroke-width="7" stroke-linecap="round"/>
  <path d="M160 70 V292 M330 70 V292" stroke="#999" stroke-width="2" stroke-dasharray="6 6"/>
  <text x="245" y="318" font-size="20" text-anchor="middle" fill="{NAVY}" font-family="sans-serif">useful life</text>
</g>
<g data-tip="A rubber duck, riding the flat part of the bathtub: constant failure rate, so exponential">
  <ellipse cx="245" cy="252" rx="34" ry="19" fill="{GOLD}"/>
  <circle cx="272" cy="226" r="16" fill="{GOLD}"/>
  <path d="M285 226 l16 4 l-16 6z" fill="#E8590C"/>
  <circle cx="276" cy="222" r="3" fill="#1f1f1f"/>
  <path d="M228 248 q14 -12 28 0" stroke="#d99a00" stroke-width="3" fill="none"/>
</g>
{person(90, "#8D5524", "#2b1a10", RED, "curly", "Test engineer, curly hair")}
{person(240, "#F1C27D", "#3b2a5a", NAVY, "hijab", "Reliability analyst, in a headscarf")}
{person(390, "#C68642", "#1f1f1f", "#7a7a86", "short", "Lab technician, glasses")}
</svg>'''
open("docs-v3/images/slides/lesson-7/art_bathtub_team.svg", "w", encoding="utf-8").write(svg)
print("wrote art_bathtub_team.svg")
