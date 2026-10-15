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
