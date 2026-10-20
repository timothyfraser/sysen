# Slide charts: conventions and palettes

Scripts named `slides_*.R` / `slides_*.py` in this folder generate the charts
and numbers that sigma's HTML slide decks show. The deck standard is
`specs/SLIDES.md` (section 3 for components, section 4 for the palette).

## Conventions

- **R ggplot2 is the chart of record.** The Python twin reproduces the same
  numbers with pandas / scipy / statsmodels; plots in Python are optional.
- **Size:** `ggsave(width = 8, height = 5.2, dpi = 200, bg = "white")` unless
  the slide asks for another shape.
- **Theme:** `theme_minimal(base_size = 22)` or larger; Lato if installed,
  else sans. No chart title (the slide has one). Axis text >= 18 pt.
- **File names:** `gen_<what>.png` in `docs-v3/images/slides/<deck>/`. Never
  use `_eq_`, `_table_`, `_chart`, or the whole words example, solution, eq,
  eqs, lambda, chisq, kfactor, table, formula, calc in an image name: the deck
  audit treats those as screenshots.
- **Caption:** link the data and the code under the chart with `.src`, for
  example `Data: sysen/workshops/anova_coagulation.csv · Code: sysen/functions/slides_w12_anova.R`.
- **Numbers:** every number on a slide comes from the script's printed output.
- **Colours:** only the palette tokens below; no green.

## Palette (hex values of the `slides.css` tokens)

| Token | Hex | Token | Hex |
|---|---|---|---|
| red | `#B31B1B` | red-dark | `#8f1414` |
| ink | `#2a1414` | muted | `#8a6a6a` |
| tan `--o` | `#f0b068` | tan soft | `#f8dcc0` |
| tile tan `--peach-dk` | `#f0a880` | lavender | `#b0a8d0` |
| blue `--b` | `#a0c0f0` | blue soft / mid | `#dce8f8` / `#3880c0` |
| purple `--p` | `#8878c0` | purple soft / mid | `#e2ddf0` / `#6048a0` |
| yellow `--y` | `#f0c030` | yellow soft | `#f8e2a0` |
| rose | `#d08080` | navy-ink | `#302050` |

## Workshop 12 palettes (copy-paste)

Diets A-D (blood coagulation): soft fill per diet, strong partner for means
and ticks. Block-design tree: one tone per treatment.

```r
# R
diet_fill   = c(A = "#f0b068", B = "#8878c0", C = "#a0c0f0", D = "#d08080")
diet_strong = c(A = "#f0a880", B = "#6048a0", C = "#3880c0", D = "#B31B1B")
tree_tones  = c(A = "#f0c030", B = "#a0c0f0", C = "#8878c0", D = "#B31B1B")
grand_mean_colour = "#2a1414"
# usage: scale_fill_manual(values = diet_fill) + scale_colour_manual(values = diet_strong)
```

```python
# Python
DIET_FILL   = {"A": "#f0b068", "B": "#8878c0", "C": "#a0c0f0", "D": "#d08080"}
DIET_STRONG = {"A": "#f0a880", "B": "#6048a0", "C": "#3880c0", "D": "#B31B1B"}
TREE_TONES  = {"A": "#f0c030", "B": "#a0c0f0", "C": "#8878c0", "D": "#B31B1B"}
GRAND_MEAN_COLOUR = "#2a1414"
```

The matching HTML tints for tables use the same tones: `td.t-o` (A),
`td.t-p` (B), `td.t-b` (C), `td.t-rose` (D); see `specs/SLIDES.md`.

## Factorial design assets (Lesson 13 / Workshop 13)

| Script | Writes | Shows |
|---|---|---|
| `slides_factorial_cubes.py` (stdlib only) | `docs-v3/images/slides/factorial/cube_yields.svg`, `cube_T.svg`, `cube_C.svg`, `cube_K.svg`, `cube_TK.svg`, `cube_three_way.svg` | Pilot-plant 2^3 cube (T left-right, C front-back, K bottom-top); yields at corners; main-effect edges as red arrows, "-" face tan, "+" face soft blue; K = A / K = B faces tan / lavender |
| `slides_factorial_cubes.py` | `docs-v3/images/slides/factorial/cube_contrast_{A,B,C,AB,AC,BC,ABC}.svg` | BHH Fig 5.4 contrast cubes: filled corner = "+", open ring = "-" |
| `slides_factorial_cubes.py` | `docs-v3/images/slides/factorial/cube_full.svg`, `cube_half.svg` | Generic 2^3 (y1..y8 = 33, 63, 41, 57, 57, 51, 59, 53) and its ABC = + half fraction |
| `slides_factorial_pilot.R` / `.py` | `docs-v3/images/slides/lesson-13/gen_effects_lattes.png` / `gen_effects_lattes_py.png` | Lattes effects plot: one box per effect at its estimate, "estimate (SE)", diverging fill (blue mid / white / red) |
| `slides_factorial_replicates.R` / `.py` | `workshops/pilot_plant_replicates.csv` is read, nothing written | Replicate arithmetic: d, d^2/2, s^2 = 8, Var(effect) = 2, SE(effect) = 1.41 |
