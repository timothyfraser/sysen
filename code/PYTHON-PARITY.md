# PYTHON-PARITY — the Python scripts vs. their R twins and their chapters

**Ruling (Tim, 2026-09-14):** *"the sysen/code python NEEDS
to use the same general techniques as the textbook uses. The scripts are not
intended to be a replica of the textbook, but rather an extension, a bunch of
demos of the code techniques introduced in the textbook. But the sysen/code was
written before you updated the python textbook chapters, so there might be some
dissonance. Find the dissonance and fix it."*

Order of authority used throughout:

1. **The R twin is gospel.** Where a `.py` and its `.R` disagree about *what is
   demonstrated*, the R script wins.
2. **The chapter sets the technique.** Where a `.py` demonstrates the right
   thing by the wrong means, the rewritten chapter's means wins — course
   helpers from `functions/` wherever R uses a same-named function, `scipy` /
   `pandas` / `plotnine` for the rest.
3. **The script stays a script.** REPL-style, in-class working copy, false
   starts and blank teaching gaps preserved (`code/README.md`). No chapter
   prose was copied in.

Import idiom, matching the chapters exactly:

```python
import os, sys
sys.path.append(os.path.abspath('functions'))
from functions_distributions import ...
```

Chapter map (confirmed against the R twins' own headers, not guessed):

| Script | R twin header says | Chapter(s) |
|---|---|---|
| `01_workshop.py` | Coding in R | `coding-in-python.html` |
| `01_recitation.py` | Visualization with ggplot in R | `visualization-with-plotnine-in-python.html` |
| `02_workshop.py` | (no header) | `distributions-and-descriptive-statistics-in-python.html` |
| `02_recitation.py` | Distributions and Descriptive Statistics in R | `distributions-and-descriptive-statistics-in-python.html` |
| `03_lesson.py` | (no header; dplyr + writing functions) | `functions-in-python.html` |
| `03_workshop.py` | **Probability Functions in R** | `probability-functions-in-python.html` |
| `03_workshop_solutions.py` | **Probability Functions in R** | `probability-functions-in-python.html` |

---

## Totals

| Script | Raw stats calls before → after | Helper import lines after | Runs top-to-bottom |
|---|---|---|---|
| `01_recitation.py` | 0 → 0 | 0 (none needed) | PASS (before and after) |
| `01_workshop.py` | 0 → 0 | 0 (none needed) | PASS (before and after) |
| `02_recitation.py` | 0 → 0 | 0 (none needed) | PASS (before and after) |
| `02_workshop.py` | 0 → 0 | 2 | PASS (before and after) |
| `03_lesson.py` | 0 → 0 | 2 | PASS (before and after) |
| `03_workshop.py` | 0 → 0 | 2 | PASS (before and after) |
| `03_workshop_solutions.py` | 0 → 0 | 2 | PASS (before and after) |

The scripts were **already free of raw `scipy.stats` / `np.random` distribution
calls** — that half of the sweep was clean on arrival. The dissonance was not
raw calls; it was **three older techniques and one missing demo**:

* `sympy` symbolic calculus standing in for R's `mosaicCalc::antiD()`, where the
  rewritten chapter now uses `quad()` from `scipy.integrate`;
* the short-form `sys.path.append("functions")` where the chapters use
  `os.path.abspath`;
* two chapter headers naming the wrong chapter;
* `03_workshop.py` importing `density` / `tidy_density` / `approxfun` and then
  never using them, while its R twin demonstrates them.

---

## 1. `03_workshop.py` — Workshop 3, Probability Functions

| # | What | Kind | Action |
|---|---|---|---|
| 1 | R twin (L90–91, 99) demonstrates `dobs = obs %>% density() %>% approxfun()`, `dobs(50)`, and bare `dobs`. Python had **none of it** — the three helpers were imported and never called. | (a) R twin demonstrates, Python does not | ADDED `dobs = approxfun(tidy_density(density(obs)))`, `dobs(50)`, bare `dobs` |
| 2 | `x = sp.Symbol("x"); pobs = sp.lambdify(x, sp.integrate(d(x), x), "numpy")` as the `antiD()` stand-in. The rewritten chapter (ch3bpy-030) says plainly: *`quad()` from `scipy.integrate` computes the definite integral (PDF → CDF)* and never mentions `sympy`. | (c) technique the chapter no longer teaches | SWAPPED to a `pobs(x)` built on `quad(d, 0, xi)` |
| 3 | `import sympy as sp` — now unused. | dead import | REMOVED; `from scipy.integrate import quad` added |
| 4 | `sys.path.append("functions")` | idiom drift | SWAPPED to `import os, sys` + `sys.path.append(os.path.abspath('functions'))` |
| 5 | Header read `Chapter: Probability in Python`; the R twin reads `Chapter: Probability Functions in R`. | header wrong | FIXED to `Probability Functions in Python` |
| 6 | Comment `# (Run this script from the root of the sigma repo.)` — this is the **sysen** repo. | wrong repo named | FIXED |

**Numeric parity proven** (values identical to R's `mosaicCalc::antiD`):

```
pobs([1,2,3]) = [0.0015 0.006  0.0135]   R antiD expects [0.0015 0.006 0.0135]
p(50)         = [3.75]                    R expects 3.75
dobs(50)      = 0.011628303242027929
```

---

## 2. `03_workshop_solutions.py` — Workshop 3 solutions

| # | What | Kind | Action |
|---|---|---|---|
| 1 | Two `sp.lambdify(x, sp.integrate(d(x), x), "numpy")` sites (`p` and `pobs`), plus a header comment declaring *"sp.integrate() is our antiD(), sp.diff() is our D()"*. Chapter now teaches `quad()` for antiD and *"a small difference quotient of your own"* for D. | (c) technique the chapter no longer teaches | SWAPPED both to `quad()`; comment rewritten |
| 2 | R twin has no `D()` demo, but the chapter explicitly teaches the CDF→PDF direction, and the script's own removed comment promised it. | (a)/(c) | ADDED a 3-line `d2()` difference-quotient demo that recovers `d(50)` exactly (`d2(50) = 0.15`, `d(50) = 0.15`) |
| 3 | `import sympy as sp` | dead import | REMOVED; `quad` imported |
| 4 | `sys.path.append("functions")` | idiom drift | SWAPPED to the chapter idiom |
| 5 | Header `Chapter: Probability in Python` vs R twin's `Probability Functions in R` | header wrong | FIXED |
| 6 | `del` list did not include the new `d2` | housekeeping | UPDATED |

Everything else in this file was **already correct**: `rpois`, `ppois`, `hist`,
`dnorm`, `pnorm`, `qnorm`, `density`, `tidy_density`, `approxfun` are all course
helpers, matching the R twin line for line, including Exercise 7's `get_pobs()`.

---

## 3. `03_lesson.py` — Lesson 3, writing functions

| # | What | Kind | Action |
|---|---|---|---|
| 1 | `sys.path.append("functions")` | idiom drift | SWAPPED to `import os, sys` + `os.path.abspath` |
| 2 | Comment named the *sigma* repo | wrong repo | FIXED |

Otherwise clean and faithful: `pexp(2, rate=0.05)` next to the hand-written
`f(t, rate)` is exactly the R twin's teaching move, and the `lambda`-is-reserved
note is a genuine Python-only extension. The R twin's `f(t, lambda)` is renamed
`f(t, rate)` — correct, and it makes the script match `pexp()`'s own signature.

---

## 4. `02_workshop.py` — Workshop 2, Distributions

No changes needed. Already on the chapter import idiom
(`os.path.abspath('functions')`, `from functions_distributions import *`) and
already using `rnorm`, `rexp`, `hist` as helpers. R-twin parity is complete:
every R line has a Python counterpart, including R's commented-out
`# rpoisson()` stub, which the Python keeps as a comment pointing at `rpois()`.

One thing worth knowing rather than changing: R's `sd()` and pandas'
`.std()` both default to the *sample* standard deviation (n−1), so `mu` and
`sigma` match the R twin's numbers.

## 5. `02_recitation.py` — Recitation 2, Descriptive Statistics

No changes needed. Pure pandas descriptives, one-for-one with the R twin
(`sigma/mu`, `se = sigma/sqrt(n)`, the 1.96 interval, the cheese-supplier table,
the three-layer plotnine chart with `'"Mean"'` quoting). No R function in the
twin has a course-helper name, so there is nothing to swap. The `del la, mu,
sigma, n, se` stands in for R's `rm(list = ls())` and is correctly explained.

## 6. `01_workshop.py` — Workshop 1, Coding

No helper changes needed; the chapter is on the clean list and teaches no
distribution functions. The one `scipy` mention is a `# !pip install
scipy==1.16.3` line in the install block, not a call.

See CONFLICT C3 below for the R-twin content gap (positional indexing,
`bind_rows`, the deliberate errors) — reported, not acted on.

## 7. `01_recitation.py` — Recitation 1, Visualization

No changes needed. A faithful, complete twin of `01_recitation.R`, section for
section, through to the three themes at the end. Its deviations are all genuine
Python facts, correctly explained in comments: `seaborn.load_dataset('diamonds')`
for ggplot2's built-in data, `.sample(1000)` for `sample_n(1000)`,
`mcolors.CSS4_COLORS` for `colors()`, and the note that plotnine *raises* on a
doubly-specified aesthetic where ggplot2 silently prefers the static trait.

---

## CONFLICTS — for Tim, not decided here

**C1. `functions/requirements.txt` still calls `sympy` the `mosaicCalc`
stand-in.** Its comment reads *"symbolic calculus — stands in for R's mosaicCalc
(antiD / D)"*, and it pins `sympy==1.14.0`. The rewritten
`probability-functions-in-python.html` dropped `sympy` entirely in favour of
`scipy.integrate.quad`, and these scripts have now followed the chapter. So
`sympy` is currently pinned for a purpose nothing in the course uses.
`functions/` is outside this task's `owns:` list, so nothing was touched.
**Decision needed:** drop the `sympy` pin and its comment, or keep it.

**C2. `quad()` and `antiD()` are not the same object, and a sharp student will
see it.** R's `antiD()` returns an *indefinite* antiderivative (constant of
integration set to 0); `quad(d, 0, x)` returns a *definite* integral from 0.
For this workshop's `d(x) = 3x/1000` they agree to the last digit (verified
above), because `d(0) = 0`. They would **not** agree for a density that is
non-zero at 0 — the R answer would sit a constant above the Python one. The
chapter accepts this and so do the scripts. **Flagging it** because it is the
one place where "the R twin is gospel" and "the chapter sets the technique"
could later diverge on a different density.

**C3. `01_workshop.R` teaches six things `01_workshop.py` does not, and the
chapter does not teach them either.** The R twin demonstrates positional
indexing (`d[1,1]`, `d[3,]`, `d[,2]`), `bind_rows()` including the ragged-column
case, deleting a column (`d$weight2 = NULL`), `slice()`, the `filter()`
comparison family (`==`, `>=`, `<=`, `%in%`), and — deliberately — **three
errors that are the lesson** (`c("corgi","dalmatian") + 1`, and selecting a
column you just deleted), flagged in its own header. `coding-in-python.html`
teaches none of these; it mentions only `dfply`'s `select`/`mutate`/`summarize`.
Adding them would mean inventing content that no chapter backs, which the ruling
does not authorise. **Decision needed:** should `01_workshop.py` grow
`.iloc`/`.loc`, `pd.concat`, `.drop`, and a TypeError teaching moment — and
should `coding-in-python.html` gain them first?

**C4. `03_workshop.py` has blank teaching gaps that the R twin also has.** Both
files leave the plotting, simulation, and Exercise-4 sections empty on purpose —
they are filled live in class, and the `_solutions` twin has the answers. The
gaps were preserved. Confirming that is intended, because "align to the R twin"
could otherwise be read as "fill them in".

**C5. Helper Series-for-scalar rendering does not bite these seven scripts.**
Per the chapters' standing ruling the helpers return a `pandas.Series` even for
scalar input. In these scripts every helper result is either assigned, plotted,
or printed at the REPL, so students see a one-row Series where R printed a bare
number — a cosmetic difference already accepted course-wide. **No script prints
a different number than its R twin.** Noting it so nobody re-opens it.

---

## Missing Python twins — reported, not acted on

33 of the 40 R scripts have no `.py` twin. By week/session:

| Session | R scripts with no Python twin |
|---|---|
| 04 | `04_workshop.R`, `04_workshop_solutions.R`, `04_recitation_solutions.R` |
| 05 | `05_workshop_solutions.R`, `05_recitation.R` |
| 06 | `06_recitation_solutions.R`, `06_workshop_extra.R` (+ its `.md`) |
| 07 | `07_lesson.R`, `07_recitation.R`, `07b_workshop.R` |
| 09 | `09_workshop.R`, `09_workshop_solutions.R`, `09_workshop_optim.R`, `09_recitation.R`, `09_recitation_solutions.R` |
| 10 | `10_lesson.R`, `10_workshop.R` |
| 11 | `11_workshop.R`, `11_workshop_exercises.R`, `11_recitation.R`, `11_recitation_rsm.R` |
| 12 | `12_lesson.R`, `12_workshop.R` |
| 13 | `13_lesson.R`, `13_workshop.R`, `13_examples.R` |
| no session (`00_`, `ZZ_`) | `00_api_queries.R`, `00_attribute_charts.R`, `00_demo.R`, `00_p_charts.R`, `00_practice_mle.R`, `00_why_distributions.R`, `ZZ_financial_analysis.R` |

`code/README.md` already tells students *"Not every session has both twins"*, so
this is a known state, not a break. The parity rule proven here — helper names
from `functions/`, `scipy` for the rest, R twin as gospel — would port to any of
them. Sessions 04, 05 and 07 are the closest to ready: their chapters
(`statistical-process-control`, `system-reliability`, `useful-life-distributions`)
are all swept and helper-clean. **Tim's call whether the rule extends to
scripts.**

---

<sub>Maintainers: this file is the audit for SIG.CODE.1. Conventions for this
folder are in [`README.md`](README.md).</sub>
