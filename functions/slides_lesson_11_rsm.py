"""slides_lesson_11_rsm.py

Python twin of functions/slides_lesson_11_rsm.R, and the renderer of the
Lesson 11 RSM slides (two predicted-yum grids + one confidence-interval Example).

Run from the repo root, AFTER the R script has written its CSVs:
    Rscript functions/slides_lesson_11_rsm.R
    python functions/slides_lesson_11_rsm.py --fragment functions/slides_lesson_11_rsm_fragment.html

1. Refits m1 (yum ~ molasses + ginger) and m3 (second order with interaction)
   with statsmodels, predicts the same 16 x 16 grid and the same 95% CI, and
   asserts every number equals R's CSV to 0.01.
2. Reads workshops/slides_lesson_11_rsm_grid.csv and writes the slide markup:
   one inline svg.fig per model, a data-tip on every cell, the optimum outlined,
   one shared colour scale so the two slides are comparable.
"""
import argparse
import html

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA = "workshops/gingerbread_test1.csv"
GRID_CSV = "workshops/slides_lesson_11_rsm_grid.csv"
CI_CSV = "workshops/slides_lesson_11_rsm_ci.csv"
GH = "https://github.com/timothyfraser/sysen/blob/main/"

FORMULAS = {
    "m1": "yum ~ molasses + ginger",
    "m3": "yum ~ molasses * ginger + I(molasses**2) + I(ginger**2)",
}


# ---------------------------------------------------------------- the twin
def fit_and_check():
    cookies = pd.read_csv(DATA)
    models = {k: smf.ols(f, data=cookies).fit() for k, f in FORMULAS.items()}
    for k, m in models.items():
        print(k, m.params.round(3).to_dict(), "R2 =", round(m.rsquared, 5))
    assert round(models["m3"].rsquared, 3) == 0.335, models["m3"].rsquared

    myx = pd.DataFrame(
        [(round(mo, 2), round(gi, 1))
         for mo in np.arange(0.5, 1.25 + 1e-9, 0.05)
         for gi in np.arange(0.5, 2.0 + 1e-9, 0.1)],
        columns=["molasses", "ginger"])
    assert len(myx) == 256
    py = pd.concat([myx.assign(model=k, yhat=models[k].predict(myx)) for k in models]).reset_index(drop=True)

    r = pd.read_csv(GRID_CSV)
    both = r.merge(py, on=["model", "molasses", "ginger"], suffixes=("_r", "_py"))
    assert len(both) == 512, len(both)
    gap = (both.yhat_r - both.yhat_py).abs().max()
    assert gap < 0.01, f"grid differs from R by {gap}"
    print(f"grid: 512 cells match R (max gap {gap:.4f})")

    best = py.loc[py.groupby("model").yhat.idxmax()]
    print(best)

    best3 = r.loc[r[r.model == "m3"].yhat.idxmax(), ["molasses", "ginger"]].to_frame().T.astype(float)
    ci = models["m3"].get_prediction(best3).summary_frame(alpha=0.05)
    ci = ci[["mean", "mean_ci_lower", "mean_ci_upper"]]
    print(ci)
    rci = pd.read_csv(CI_CSV).iloc[0]
    for a, b in [("mean", "fit"), ("mean_ci_lower", "lwr"), ("mean_ci_upper", "upr")]:
        assert abs(ci[a].iloc[0] - rci[b]) < 0.01, (a, ci[a].iloc[0], rci[b])
    print("CI matches R to 0.01")
    return ci


# ---------------------------------------------------------------- the SVG
VIRIDIS = ["#440154", "#482878", "#3e4989", "#31688e", "#26828e",
           "#1f9e89", "#35b779", "#6ece58", "#b5de2b", "#fde725"]


def ramp(t):
    t = min(max(t, 0.0), 1.0) * (len(VIRIDIS) - 1)
    i = min(int(t), len(VIRIDIS) - 2)
    f = t - i
    a = [int(VIRIDIS[i][j:j + 2], 16) for j in (1, 3, 5)]
    b = [int(VIRIDIS[i + 1][j:j + 2], 16) for j in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * f):02x}" for x, y in zip(a, b))


def num(x, d):
    s = f"{x:.{d}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


CELL = 26
X0, Y0 = 110, 24            # top-left of the grid
N = 16


def svg_grid(g, model, lo, hi, prefix, title, formula, maxh=440):
    mol = sorted(g.molasses.unique())
    gin = sorted(g.ginger.unique())
    assert len(mol) == N and len(gin) == N
    best = g.loc[g.yhat.idxmax()]
    W, H = 900, 500
    out = [f'<svg class="fig" viewBox="0 0 {W} {H}" role="img" aria-labelledby="{prefix}-t" '
           f'style="width:100%;max-height:{maxh}px;display:block;margin:0 auto">',
           f'  <title id="{prefix}-t">{html.escape(title)}</title>',
           '  <defs><linearGradient id="' + prefix + '-ramp" x1="0" y1="1" x2="0" y2="0">'
           + "".join(f'<stop offset="{i / (len(VIRIDIS) - 1):.3f}" stop-color="{c}"/>'
                     for i, c in enumerate(VIRIDIS))
           + '</linearGradient></defs>']
    tested_m = {0.5, 0.75, 1.0, 1.25}
    tested_g = {0.5, 1.0, 1.5, 2.0}
    for _, r in g.iterrows():
        i = mol.index(r.molasses)
        j = gin.index(r.ginger)
        x = X0 + i * CELL
        y = Y0 + (N - 1 - j) * CELL
        m, gi, yh = num(r.molasses, 2), num(r.ginger, 1), f"{r.yhat:.1f}"
        tested = r.molasses in tested_m and round(r.ginger, 1) in tested_g
        lines = [f"Predicted yum: {yh}"]
        if tested:
            lines.append("A tested recipe (20 cookies baked)")
        lines.append(f"predict({model}, newdata = tibble(molasses = {m}, ginger = {gi}))")
        out.append(f'  <g data-tip-title="Molasses {m} cups · ginger {gi} tbsp" '
                   f'data-tip="{html.escape("|".join(lines))}" tabindex="0">'
                   f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                   f'fill="{ramp((r.yhat - lo) / (hi - lo))}"/>'
                   + (f'<circle cx="{x + CELL / 2}" cy="{y + CELL / 2}" r="3" fill="#ffffff" opacity="0.85"/>'
                      if tested else "")
                   + '</g>')
    # optimum
    bi, bj = mol.index(best.molasses), gin.index(best.ginger)
    bx, by = X0 + bi * CELL, Y0 + (N - 1 - bj) * CELL
    out.append(f'  <rect x="{bx}" y="{by}" width="{CELL}" height="{CELL}" fill="none" '
               f'stroke="#B31B1B" style="stroke:var(--red)" stroke-width="4" pointer-events="none"/>')
    side = X0 + N * CELL
    out.append(f'  <path d="M{bx + CELL + 2},{by + CELL / 2} L{side + 34},{by + CELL / 2}" stroke="#B31B1B" '
               f'style="stroke:var(--red)" stroke-width="2.5" fill="none"/>')
    out.append(f'  <text x="{side + 40}" y="{by + CELL / 2 - 4}" font-size="21" font-weight="700" '
               f'fill="#B31B1B" style="fill:var(--red)">best: {num(best.molasses, 2)} cups, '
               f'{num(best.ginger, 1)} tbsp</text>')
    out.append(f'  <text x="{side + 40}" y="{by + CELL / 2 + 20}" font-size="21" font-weight="700" '
               f'fill="#B31B1B" style="fill:var(--red)">predicted yum {best.yhat:.1f}</text>')
    # axes
    ink = 'fill="#2a1414" style="fill:var(--ink)"'
    muted = 'fill="#6b5b5b" style="fill:var(--muted)"'
    for v in sorted(tested_m):
        i = mol.index(v)
        out.append(f'  <text x="{X0 + i * CELL + CELL / 2}" y="{Y0 + N * CELL + 24}" font-size="18" '
                   f'text-anchor="middle" {ink}>{num(v, 2)}</text>')
    for v in sorted(tested_g):
        j = gin.index(v)
        out.append(f'  <text x="{X0 - 10}" y="{Y0 + (N - 1 - j) * CELL + CELL / 2 + 6}" font-size="18" '
                   f'text-anchor="end" {ink}>{num(v, 1)}</text>')
    out.append(f'  <text x="{X0 + N * CELL / 2}" y="{Y0 + N * CELL + 54}" font-size="20" '
               f'font-weight="700" text-anchor="middle" {ink}>Molasses (cups)</text>')
    cy = Y0 + N * CELL / 2
    out.append(f'  <text x="40" y="{cy}" font-size="20" font-weight="700" text-anchor="middle" '
               f'transform="rotate(-90 40 {cy})" {ink}>Ginger (tbsp)</text>')
    # legend
    for k, line in enumerate(formula):
        out.append(f'  <text x="{side + 40}" y="{Y0 + 18 + k * 26}" font-size="20" font-family="monospace" {ink}>'
                   f'{html.escape(line)}</text>')
    lx, ly, lh = side + 60, Y0 + 110, 190
    out.append(f'  <text x="{lx - 10}" y="{ly - 18}" font-size="19" font-weight="700" {ink}>Predicted yum</text>')
    out.append(f'  <rect x="{lx}" y="{ly}" width="24" height="{lh}" fill="url(#{prefix}-ramp)"/>')
    for v in np.linspace(lo, hi, 5):
        yy = ly + lh - (v - lo) / (hi - lo) * lh
        out.append(f'  <text x="{lx + 32}" y="{yy + 6}" font-size="17" {ink}>{v:.0f}</text>')
    out.append(f'  <circle cx="{lx + 6}" cy="{ly + lh + 30}" r="4" fill="#ffffff" stroke="#6b5b5b"/>'
               f'<text x="{lx + 18}" y="{ly + lh + 36}" font-size="17" {muted}>a tested recipe</text>')
    out.append('</svg>')
    return "\n".join(out)


def caption(extra=""):
    return ('      <div class="caption" style="position:static;margin-top:6px">Hover any cell: its recipe, '
            'predicted yum, and the predict() call' + extra + ' &middot; '
            f'<a href="{GH}workshops/slides_lesson_11_rsm_grid.csv">data</a> &middot; '
            f'<a href="{GH}functions/slides_lesson_11_rsm.R">code</a></div>')


def fragment(ci):
    g = pd.read_csv(GRID_CSV)
    lo, hi = np.floor(g.yhat.min()), np.ceil(g.yhat.max())
    g1, g3 = g[g.model == "m1"].reset_index(drop=True), g[g.model == "m3"].reset_index(drop=True)
    b1, b3 = g1.loc[g1.yhat.idxmax()], g3.loc[g3.yhat.idxmax()]
    w3 = g3.loc[g3.yhat.idxmin()]
    same = (b1.molasses, b1.ginger) == (b3.molasses, b3.ginger)
    r = pd.read_csv(CI_CSV).iloc[0]
    m, gi = num(r.molasses, 2), num(r.ginger, 1)

    if same:
        compare = (f"Same best corner, different shape: "
                   f"the basic model is nearly flat ({g1.yhat.min():.1f} to {g1.yhat.max():.1f}); this one dips "
                   f"near {num(w3.molasses, 2)} cups and reaches {b3.yhat:.1f} at that corner, not {b1.yhat:.1f}.")
    else:
        compare = (f"The best recipe moves from {num(b1.molasses, 2)} cups, {num(b1.ginger, 1)} tbsp "
                   f"to {num(b3.molasses, 2)} cups, {num(b3.ginger, 1)} tbsp.")

    s = []
    s.append("  <!-- RSM grid, basic model; inline svg.fig with a data-tip per cell, generated by "
             "functions/slides_lesson_11_rsm.py from workshops/slides_lesson_11_rsm_grid.csv -->")
    s.append('  <section class="slide s-topbar">\n    <header class="topbar">Response surface methodology</header>\n'
             '    <div class="content"><div class="subhead">The basic model\'s surface</div>')
    s.append(svg_grid(g1, "m1", lo, hi, "rsm1",
                      "Predicted yum from the basic model over 16 by 16 recipes; the best is "
                      f"{num(b1.molasses, 2)} cups of molasses and {num(b1.ginger, 1)} tbsp of ginger",
                      ["m1: yum ~ molasses + ginger"]))
    s.append(caption(" &middot; R&sup2; = %.3f" % smf.ols(FORMULAS["m1"], data=pd.read_csv(DATA)).fit().rsquared))
    s.append("    </div>\n  </section>\n")

    s.append("  <!-- RSM grid, second-order model with interaction; same colour scale as the basic model -->")
    s.append('  <section class="slide s-topbar">\n    <header class="topbar">Response surface methodology</header>\n'
             '    <div class="content"><div class="subhead">Second order with interaction</div>')
    s.append(svg_grid(g3, "m3", lo, hi, "rsm3",
                      "Predicted yum from the second-order model with interaction over 16 by 16 recipes; the best is "
                      f"{num(b3.molasses, 2)} cups of molasses and {num(b3.ginger, 1)} tbsp of ginger",
                      ["m3: yum ~ molasses * ginger", "  + I(molasses^2) + I(ginger^2)"], maxh=360))
    s.append(f'      <p style="margin:2px 0 0;text-align:center"><strong>{html.escape(compare)}</strong></p>')
    s.append(caption(" &middot; R&sup2; = 0.335"))
    s.append("    </div>\n  </section>\n")

    rf, rl, ru = f"{r.fit:.1f}", f"{r.lwr:.1f}", f"{r.upr:.1f}"
    pm, pl, pu = ci["mean"].iloc[0], ci["mean_ci_lower"].iloc[0], ci["mean_ci_upper"].iloc[0]
    pyout = html.escape(ci.to_string())
    interp = f"At {m} cups and {gi} tbsp, predicted yum is {rf} (95% CI {rl} to {ru})."
    s.append("  <!-- Example: predict with a 95% confidence interval (outputs from "
             "functions/slides_lesson_11_rsm.R and its Python twin) -->")
    s.append(f'''  <section class="slide s-agenda s-example">
    <div class="panel"><h1>Example</h1><div class="sub">Predict with a 95% confidence interval</div>
      <p>Predict <strong>yum</strong> at the second-order model's best recipe: {m} cups of molasses, {gi} tbsp of ginger.</p>
      <p>Ask <code>predict()</code> for a 95% confidence interval, not just the fitted value.</p></div>
    <div class="side"><div class="lang-pair">
<pre data-lang="r">library(dplyr)
library(readr)
cookies = read_csv("workshops/gingerbread_test1.csv")
m3 = lm(yum ~ molasses * ginger + I(molasses^2) + I(ginger^2),
         data = cookies)
best = tibble(molasses = {m}, ginger = {gi})
<span class="cm"># fit, lower and upper bound of the 95% CI</span>
predict(m3, newdata = best, se.fit = TRUE,
        interval = "confidence", level = 0.95) %&gt;%
  with(fit) %&gt;%
  as_tibble()</pre>
<pre data-lang="py">import pandas as pd
import statsmodels.formula.api as smf
cookies = pd.read_csv("workshops/gingerbread_test1.csv")
m3 = smf.ols("yum ~ molasses * ginger + I(molasses**2) + I(ginger**2)",
             data = cookies).fit()
best = pd.DataFrame({{"molasses": [{m}], "ginger": [{gi}]}})
<span class="cm"># alpha = 0.05 gives the 95% CI</span>
ci = m3.get_prediction(best).summary_frame(alpha = 0.05)
ci[["mean", "mean_ci_lower", "mean_ci_upper"]]</pre>
<div class="answer" data-answer="output" data-lang="r" data-output><pre class="ocard"># A tibble: 1 &times; 3
    fit   lwr   upr
  &lt;dbl&gt; &lt;dbl&gt; &lt;dbl&gt;
1  <b class="k">{rf}</b>  {rl}  {ru}</pre>
<p>{html.escape(interp)}</p></div>
<div class="answer" data-answer="output" data-lang="py" data-output><pre class="ocard">{pyout}</pre>
<p>{html.escape(interp)}</p></div>
    </div></div>
  </section>
''')
    return "\n".join(s)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fragment", action="append", default=[],
                    help="write the slide markup here (repeatable)")
    a = ap.parse_args()
    ci = fit_and_check()
    if a.fragment:
        text = fragment(ci)
        for p in a.fragment:
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            print("wrote", p)
