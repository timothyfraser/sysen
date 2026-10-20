# slides_recitation_11_art.py -- SVG cartoon for the "Iteration" divider (stdlib only).
# Three bakers of different backgrounds iterate on a gingerbread recipe: one tastes and
# scores ("yum 6/10 -> try more ginger"), one writes it down, one slides in the next batch.
# Run from the repo root:  python3 functions/slides_recitation_11_art.py
import pathlib
RED, NAVY, GOLD, BROWN, CREAM = "#B31B1B", "#302050", "#F2B705", "#8a5a34", "#fbf3ea"

def person(cx, skin, hair, shirt, style, label, y=250):
    hairs = {
        "short": f'<path d="M{cx-34} {y-6} a34 34 0 0 1 68 0 q-34 -22 -68 0z" fill="{hair}"/>',
        "bun":   f'<circle cx="{cx}" cy="{y-50}" r="16" fill="{hair}"/><path d="M{cx-35} {y-2} a35 35 0 0 1 70 0 q-35 -26 -70 0z" fill="{hair}"/>',
        "curly": "".join(f'<circle cx="{cx+dx}" cy="{y-dy}" r="15" fill="{hair}"/>' for dx, dy in
                         [(-26, 14), (-12, 32), (6, 36), (22, 28), (32, 10)]),
    }[style]
    hat = f'<rect x="{cx-32}" y="{y-66}" width="64" height="38" rx="14" fill="#fff" stroke="{NAVY}" stroke-width="3"/><rect x="{cx-36}" y="{y-36}" width="72" height="12" rx="5" fill="#fff" stroke="{NAVY}" stroke-width="3"/>' if style == "short" else ""
    body = f'<path d="M{cx-62} {y+170} q0 -110 62 -110 q62 0 62 110z" fill="{shirt}"/>'
    neck = f'<rect x="{cx-12}" y="{y+22}" width="24" height="34" rx="8" fill="{skin}"/>'
    face = f'<circle cx="{cx}" cy="{y}" r="33" fill="{skin}"/>'
    eyes = (f'<circle cx="{cx-12}" cy="{y+2}" r="4" fill="#1f1f1f"/><circle cx="{cx+12}" cy="{y+2}" r="4" fill="#1f1f1f"/>'
            f'<path d="M{cx-11} {y+16} q11 9 22 0" stroke="#1f1f1f" stroke-width="3" fill="none" stroke-linecap="round"/>')
    return f'<g data-tip="{label}">{body}{neck}{face}{hairs}{hat}{eyes}</g>'

def cookie(x, y, r=17):
    return (f'<g><circle cx="{x}" cy="{y-r*0.9}" r="{r*0.55}" fill="{BROWN}"/>'
            f'<rect x="{x-r*0.75}" y="{y-r*0.5}" width="{r*1.5}" height="{r*1.5}" rx="4" fill="{BROWN}"/>'
            f'<circle cx="{x-r*0.9}" cy="{y-r*0.2}" r="{r*0.4}" fill="{BROWN}"/><circle cx="{x+r*0.9}" cy="{y-r*0.2}" r="{r*0.4}" fill="{BROWN}"/>'
            f'<circle cx="{x}" cy="{y-r*0.95}" r="3" fill="{CREAM}"/><circle cx="{x-4}" cy="{y+r*0.3}" r="2.5" fill="{CREAM}"/><circle cx="{x+4}" cy="{y+r*0.3}" r="2.5" fill="{CREAM}"/></g>')

tray = lambda x, y, n: (f'<rect x="{x}" y="{y}" width="{n*46+16}" height="12" rx="5" fill="#c9c2bf" stroke="{NAVY}" stroke-width="2"/>'
                        + "".join(cookie(x + 30 + i * 46, y - 4) for i in range(n)))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 520" role="img" aria-labelledby="t d">
<title id="t">Three bakers iterate on a gingerbread recipe</title>
<desc id="d">A woman with curly hair tastes a cookie and holds up a sign reading yum 6 out of 10, a man in a chef hat slides a new tray of cookies from an oven, and a woman with a bun writes the result on a clipboard; trays of cookies sit on the counter.</desc>
<rect width="720" height="520" rx="22" fill="{CREAM}"/>
<rect y="378" width="720" height="142" rx="0" fill="#e9dfd6"/>
{person(130, "#8d5a3b", "#2a1a14", RED, "curly", "Baker 1: tastes batch 1 and scores it")}
{person(360, "#f1c9a5", "#5a3a22", NAVY, "short", "Baker 2: slides in batch 2 with more ginger")}
{person(590, "#c68a5e", "#1f1f1f", GOLD, "bun", "Baker 3: records every batch on the clipboard")}
<g data-tip="Taste score: yum 6 out of 10">
  <rect x="30" y="70" width="190" height="62" rx="12" fill="#fff" stroke="{NAVY}" stroke-width="3"/><path d="M110 132 l16 34 l14 -34z" fill="#fff" stroke="{NAVY}" stroke-width="3"/><rect x="108" y="128" width="34" height="8" fill="#fff"/>
  <text x="125" y="113" font-family="Lato,Arial,sans-serif" font-size="32" font-weight="700" text-anchor="middle" fill="{RED}">yum 6/10</text></g>
<g data-tip="Next batch: more ginger, then taste again">
  <rect x="400" y="20" width="200" height="62" rx="12" fill="#fff" stroke="{NAVY}" stroke-width="3"/><path d="M420 82 l-10 30 l36 -30z" fill="#fff" stroke="{NAVY}" stroke-width="3"/><rect x="418" y="78" width="30" height="8" fill="#fff"/>
  <text x="500" y="61" font-family="Lato,Arial,sans-serif" font-size="30" font-weight="700" text-anchor="middle" fill="{NAVY}">+ ginger?</text></g>
<g data-tip="Clipboard: molasses, ginger, yum for every batch">
  <rect x="640" y="330" width="62" height="84" rx="6" fill="#fff" stroke="{NAVY}" stroke-width="3"/>
  <rect x="660" y="322" width="22" height="14" rx="3" fill="{NAVY}"/>
  <path d="M650 358 h42 M650 374 h42 M650 390 h30" stroke="{NAVY}" stroke-width="3"/></g>
<g data-tip="Trays of cookies: batch 1, batch 2">{tray(36, 440, 5)}{tray(410, 440, 5)}</g>
<g data-tip="Counter"><rect x="0" y="446" width="720" height="14" fill="{NAVY}"/></g>
</svg>'''
out = pathlib.Path(__file__).resolve().parent.parent / "docs-v3/images/slides/recitation-11/art_bakers.svg"
out.write_text(svg, encoding="utf-8")
print("wrote", out)
