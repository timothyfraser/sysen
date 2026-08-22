# `sysen` — the code and data for SYSEN 5300

**Systems Engineering and Six Sigma for the Design and Operation of Reliable
Systems** · Cornell University · Dr. Timothy Fraser

Welcome. This is the **code and data companion** to the course textbook. The
textbook teaches; this **repository** — or *repo*, a shared folder of files that
everyone in the course gets a copy of — holds the scripts and the datasets those
chapters run on.

Plenty of people arrive in this course having never written a line of code.
That is expected, and the course is built for it. Get a copy of this once, read
the textbook alongside it, and run the code as you go.

## Quick links

| | |
|---|---|
| **Textbook** (start here) | [timothyfraser.com/sigma](https://timothyfraser.com/sigma/) |
| **Canvas** (deadlines, submission, grades, quizzes) | [Canvas](https://timothyfraser.com/sigma/canvas) |
| **This repo** | [github.com/timothyfraser/sysen](https://github.com/timothyfraser/sysen) |

> Two rules that save a lot of confusion. The textbook is authoritative for
> **content** — what to read, what to run, how a technique works. Canvas is
> authoritative for **dates, deadlines, grades, and quizzes**. You will not find
> a due date anywhere in this repo, and that is on purpose.

## What's in here

| Folder | What it holds |
|---|---|
| [`workshops/`](workshops) | The data. Every `read_csv("workshops/....csv")` you see in a chapter reads a file from this folder. |
| [`code/`](code) | The R and Python scripts from the workshops, lessons, and recitations — the live-coded version of what the chapters walk through. |
| [`functions/`](functions) | Helper functions written for this course (`functions_*.R`, `functions_*.py`), plus short `workflow_*` scripts showing how to call them. |
| [`docs/`](docs) | Cheat sheets for RStudio, `dplyr`, `ggplot2`, and `stringr`. |

Each of those folders has its own README explaining it in more detail. Read the
one for the folder you need; you can ignore the rest.

## Getting started

Three one-time steps, and then you're set for the term.

### 1. Get a copy of the repo

If you're using **Posit Cloud** — the browser version of R, which needs nothing
installed on your computer — the course project already has all of this in it.
Nothing to do here; go to step 2.

Otherwise, download it with `git`:

```sh
git clone https://github.com/timothyfraser/sysen.git
cd sysen
```

Chapters occasionally gain new data during the term. Pull those updates with:

```sh
cd sysen
git pull
```

You will never push anything back — this repo is read-only for students, so
there is nothing here you can break.

**Open the project, not just the file.** After you have a copy, double-click
`project.Rproj`. That tells R to treat the top of this folder as the place it
starts looking from, which is what every file path in every chapter assumes.
It's one click, and it heads off the single most common error of the first week.

### 2. Install what you need

**R** — run this once, from the top of the folder:

```r
source("workshops/packages.R")
```

A **package** is a bundle of extra commands that someone else wrote and shared.
That one line installs every package this course uses: the tidyverse, plus the
statistical and visualization packages. It takes a while the first time, so
start it and go get coffee. Warnings about packages built under a different
version of R are normal — ignore them.

**Python** — run this once:

```sh
pip install -r functions/requirements.txt
```

The Python track uses `pandas`, `numpy`, `scipy`, `statsmodels`, and `plotnine`
(the `ggplot2` grammar, in Python).

Both tracks are first-class, and you only need one. Most chapters exist in both
R and Python — pick the one that fits your background and stay with it.

### 3. Run code from the top of the repo

Scripts load data using paths written **relative to the top of this repo**:

```r
library(readr)
onsen = read_csv("workshops/onsen.csv")
```

```python
import pandas as pd
onsen = pd.read_csv("workshops/onsen.csv")
```

That path means "go into `workshops`, then take `onsen.csv`" — starting from the
top. So keep the top of the repo as the place R is looking from, which is
exactly what opening `project.Rproj` does for you.

If you see `No such file or directory` or `cannot open file`, that's the
giveaway that R is looking from somewhere else — usually from inside `code/`.
Type `getwd()` in the console and it will tell you where it currently is. This
is a normal thing to get wrong, not a sign that you broke something.

Some chapters skip the local file and read the same data straight off the web,
so the code runs anywhere:

```r
diamonds = read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/mydiamonds.csv")
```

Both routes give you the same numbers.

### 4. Use the helper functions

`functions/` holds functions written for this course — control chart math,
reliability functions, factorial effects, distribution helpers. Load one with
`source()` in R, or by executing the file in Python:

```r
source("functions/functions_process_control.R")
```

```python
exec(open('functions/functions_process_control.py').read())
```

[`functions/README.md`](functions/README.md) lists every function and what it
does.

## Where each chapter's code and data live

Chapters are listed by **title**, in textbook order. Not every chapter has a
script here — many are self-contained in the textbook — and the script numbers
do not always line up with the chapter numbers — scripts are numbered by
class session (lesson/workshop/recitation), matching the slide decks.

An R script and its Python twin **share a basename**: `01_workshop.R` and
`01_workshop.py` are the same session, each written in the style of its own
textbook chapter.

| Textbook chapter | Data in `workshops/` | Scripts in `code/` |
|---|---|---|
| Coding in R | — | `01_workshop.R` |
| Coding in Python | — | `01_workshop.py` |
| FMEA in R · FMEA in Python | — | — |
| Visualization with `ggplot` in R | — | `01_recitation.R` |
| Visualization with `plotnine` in Python | — | `01_recitation.py` |
| Distributions and Descriptive Statistics in R | `la_parishes.csv` | `02_workshop.R`, `02_recitation.R` |
| Distributions and Descriptive Statistics in Python | `la_parishes.csv` | `02_workshop.py`, `02_recitation.py` |
| Functions in R · Functions in Python | — | `03_lesson.R`, `03_lesson.py` |
| Probability in R | — | `03_workshop.R`, `03_workshop_solutions.R` |
| Probability in Python | — | `03_workshop.py`, `03_workshop_solutions.py` |
| Probability Functions in R | — | `03_workshop.R` |
| System Reliability in R | — | `04_workshop.R`, `04_workshop_solutions.R`, `04_recitation_solutions.R` |
| System Reliability in Python | — | — |
| Statistical Process Control in R | `onsen.csv` | `05_workshop_solutions.R`, `05_recitation.R` |
| Statistical Process Control in Python | `onsen.csv` | — |
| Indices and Confidence Intervals for Statistical Process Control in R | `onsen.csv` | `06_recitation_solutions.R`, `06_workshop_extra.R` |
| Indices and Confidence Intervals for Statistical Process Control in Python | `onsen.csv` | — |
| Useful Life Distributions (Exponential) | `masks.csv` | `07_lesson.R`, `07_recitation.R` |
| Statistical Techniques for Exponential Distributions in R | `masks.csv` | `07b_workshop.R` |
| Statistical Techniques for Exponential Distributions in Python | `masks.csv` | — |
| Useful Life Distributions (Weibull, Gamma, & Lognormal) in R | `crops.csv` | `09_workshop.R`, `09_workshop_optim.R`, `09_workshop_solutions.R` |
| Useful Life Distributions (Weibull, Gamma, & Lognormal) in Python | `crops.csv` | — |
| Fault Tree Analysis in R | `fault_tree_engine_nodes.csv`, `fault_tree_engine_edges.csv` (used by the textbook's interactive diagram) | `09_recitation.R`, `09_recitation_solutions.R` |
| Fault Tree Analysis in Python | — | — |
| Physical Acceleration Models | — | `10_workshop.R`, `10_lesson.R` |
| Physical Acceleration Models in Python | — | — |
| Bivariate Regression: Modeling Diamond Pricing | `mydiamonds.csv` | — |
| Bivariate Regression: Modeling Diamond Pricing in Python | `mydiamonds.csv` | — |
| Multivariate Regression: Modeling Effects of Disaster on Social Capital | `jp_matching_experiment.csv`, `japan_muni_elections.csv` | `11_workshop.R`, `11_workshop_exercises.R` |
| Multivariate Regression: Modeling Effects of Disaster on Social Capital in Python | `jp_matching_experiment.csv`, `japan_muni_elections.csv` | — |
| Design of Experiments in R | `donuts.csv` | `12_workshop.R`, `12_lesson.R` |
| Factorial Design and Interaction Effects in R | `lattes.csv` | `13_workshop.R`, `13_lesson.R`, `13_examples.R` |
| Factorial Design and Interaction Effects in Python | `lattes.csv` | — |
| Response Surface Methodology in R | `gingerbread_test1.csv`, `gingerbread_test2.csv`, `gingerbread_test3.csv` | `11_recitation.R`, `11_recitation_rsm.R` |
| Response Surface Methodology in Python | `gingerbread_test1.csv`, `gingerbread_test2.csv`, `gingerbread_test3.csv` | — |
| Appendix: `ggplot` tips | — | — |
| Appendix: `mermaid` Block Diagrams (Flowcharts) in R | — | — |
| Appendix: Using `fitdistr` to Fit Distribution Parameters | `crops.csv` | `00_practice_mle.R` |
| Appendix: Statistical Tables and Common Equations | `bn.csv`, `dn.csv`, `chisq.csv`, `k_lower.csv`, `k_upper.csv` | — |

Extras with no chapter of their own: `code/00_*` (demos and side topics),
`code/ZZ_financial_analysis.R` (financial impact analysis), and
`code/apps/` (Shiny dashboards, `plumber` APIs, and parameterized
reports).

## Cheat sheets

The course leans on a handful of R packages. When you get stuck, the package
documentation usually has an example that unsticks you — and for a fast lookup,
use a cheat sheet.

| Package | Purpose | Cheatsheet | Documentation |
|---|---|---|---|
| RStudio | the IDE itself | [Cheatsheet](https://rstudio.github.io/cheatsheets/rstudio-ide.pdf) | [Docs](https://docs.posit.co/ide/user/) |
| `dplyr` | data wrangling | [Cheatsheet](https://rstudio.github.io/cheatsheets/data-transformation.pdf) | [Docs](https://dplyr.tidyverse.org/) |
| `ggplot2` | data visualization | [Cheatsheet](https://rstudio.github.io/cheatsheets/data-visualization.pdf) | [Docs](https://ggplot2.tidyverse.org/) |
| `stringr` | working with text | [Cheatsheet](https://rstudio.github.io/cheatsheets/strings.pdf) | [Docs](https://stringr.tidyverse.org/) |
| `viridis` | color palettes | — | [Docs](https://sjmgarnier.github.io/viridis/) |
| `broom` | tidying model output | [Cheatsheet](https://pop.princeton.edu/sites/g/files/toruqf496/files/documents/2018May_Broom_0.pdf) | [Docs](https://broom.tidymodels.org/) |

Local copies of the RStudio, `dplyr`, `ggplot2`, and `stringr` cheat sheets live
in [`docs/`](docs) as PDFs and PNGs.

### cheatsheet: `RStudio` Interface

![`rstudio` interface](docs/cheatsheet_rstudio_1.png)

![`rstudio` interface](docs/cheatsheet_rstudio_2.png)

### cheatsheet: `dplyr` package

![`dplyr` package](docs/cheatsheet_dplyr_1.png)

![`dplyr` package](docs/cheatsheet_dplyr_2.png)

### cheatsheet: `ggplot2` package

![`ggplot` package](docs/cheatsheet_ggplot_1.png)

![`ggplot` package](docs/cheatsheet_ggplot_2.png)

## A note on how to use this code

Much of what's in `code/` was written **live, in class**, while working through
a problem with students. It reads that way on purpose: false starts, a first
attempt replaced by a better one, and the occasional line of pseudo-code written
on the board. That's what learning to code actually looks like.

So run these scripts **chunk by chunk**, not top to bottom. Read the comments,
run a few lines, look at what came back, then keep going. The polished, narrated
version of each analysis is the textbook chapter; these files are the working
session that produced it.

## License

See [LICENSE](LICENSE).
