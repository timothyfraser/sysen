# slides_lesson_11_cycle.py ----------------------------------------------------
# Feeds: Lesson 10 slides, "Why DOE" (the experimental design cycle).
# Run from the top of the repo:  python functions/slides_lesson_11_cycle.py
# Prints: an inline <svg class="fig"> fragment (six steps on a ring, one
#   data-tip per step) that is pasted into the deck. Stdlib only.
import math

steps = [
  ("Plan the tests", "Choose factors, levels and runs before collecting anything|Randomize the run order"),
  ("Measure the output", "Run the experiment and record y for every run|Experimental error shows up here"),
  ("Identify significant factors", "ANOVA / t and F tests on each factor|Which X's actually move Y?"),
  ("Build your model", "Y = f(X1, X2, X3 ...)|Least squares regression on the significant factors"),
  ("Check your model", "Residuals, R², a confirmation run|Does it predict new data?"),
  ("Optimize", "Pick the factor settings that give the best Y|Then plan the next round of tests"),
]
fills = ["var(--b)", "var(--lav)", "var(--rose)", "var(--o)", "var(--b)", "var(--lav)"]
raw = ["#a0c0f0", "#c8b8e8", "#f0b0b8", "#f5c890", "#a0c0f0", "#c8b8e8"]
W, H, cx, cy, R = 900, 470, 450, 235, 175
bw, bh = 300, 58
out = []
out.append(f'<svg class="fig" viewBox="0 0 {W} {H}" role="img" aria-labelledby="dc-t" style="max-height:420px">')
out.append('  <title id="dc-t">The experimental design cycle: plan the tests, measure the output, identify significant factors, build your model, check your model, optimize, then plan again</title>')
out.append('  <defs><marker id="dc-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2a1414" style="fill:var(--ink)"/></marker></defs>')
pts = []
for i in range(6):
  a = -math.pi / 2 + i * 2 * math.pi / 6
  pts.append((cx + 1.55 * R * math.cos(a), cy + R * math.sin(a)))
# arrows between consecutive steps, drawn as arcs on the ring
for i in range(6):
  a0 = -math.pi / 2 + (i + 0.30) * 2 * math.pi / 6
  a1 = -math.pi / 2 + (i + 0.70) * 2 * math.pi / 6
  x0, y0 = cx + 1.55 * R * math.cos(a0), cy + R * math.sin(a0)
  x1, y1 = cx + 1.55 * R * math.cos(a1), cy + R * math.sin(a1)
  out.append(f'  <path d="M{x0:.1f},{y0:.1f} A{1.55*R:.0f},{R:.0f} 0 0 1 {x1:.1f},{y1:.1f}" fill="none" stroke="#2a1414" stroke-width="2.5" style="stroke:var(--ink)" marker-end="url(#dc-arrow)"/>')
for i, ((label, tip), (x, y)) in enumerate(zip(steps, pts)):
  out.append(f'  <g data-tip-title="{i+1}. {label}" data-tip="{tip}" tabindex="0">')
  out.append(f'    <rect x="{x-bw/2:.1f}" y="{y-bh/2:.1f}" width="{bw}" height="{bh}" rx="12" fill="{raw[i]}" style="fill:{fills[i]}"/>')
  out.append(f'    <text x="{x:.1f}" y="{y+8:.1f}" text-anchor="middle" font-size="23" font-weight="700" fill="#2a1414" style="fill:var(--ink)">{i+1}. {label}</text>')
  out.append('  </g>')
out.append(f'  <text x="{cx}" y="{cy-6}" text-anchor="middle" font-size="26" font-weight="700" fill="#B31B1B" style="fill:var(--red)">Y = f(X&#8321;, X&#8322;, X&#8323; ...)</text>')
out.append(f'  <text x="{cx}" y="{cy+26}" text-anchor="middle" font-size="19" fill="#6b5b5b" style="fill:var(--muted)">hover a step</text>')
out.append('</svg>')
print("\n".join(out))
