# `sysen` — SYSEN 5300 code and data

**Systems Engineering and Six Sigma for the Design and Operation of Reliable
Systems** · Cornell University · Dr. Timothy Fraser

This is the **code and data companion** to the course textbook. The textbook
teaches; this repo holds the scripts and the datasets those chapters run on.
Clone it once, `git pull` when a chapter says to, and run the code alongside the
reading.

## Quick links

| | |
|---|---|
| **Textbook** (start here) | [timothyfraser.com/sigma](https://timothyfraser.com/sigma/) |
| **Canvas** (deadlines, submission, grades, quizzes) | [canvas.cornell.edu/courses/88388](https://canvas.cornell.edu/courses/88388) |
| **This repo** | [github.com/timothyfraser/sysen](https://github.com/timothyfraser/sysen) |

> The textbook is authoritative for **content** — what to read, what to run, how
> a technique works. Canvas is authoritative for **dates, deadlines, grades, and
> quizzes**. You will not find a due date in this repo, and that is on purpose.

## What's in here

| Folder | What it holds |
|---|---|
| [`workshops/`](workshops) | The datasets. Every `read_csv("workshops/....csv")` in a textbook chapter reads a file from this folder. |
| [`code/`](code) | The R and Python scripts from the workshops, lessons, and recitations — the live-coded versions of what the chapters walk through. |
| [`functions/`](functions) | Reusable helper functions the course provides (`functions_*.R`, `functions_*.py`), plus short `workflow_*` scripts showing how to call them. |
| [`docs/`](docs) | Cheat sheets and helper documents for RStudio, `dplyr`, `ggplot2`, and `stringr`. |

## Getting started

### 1. Clone the repo

```sh
git clone https://github.com/timothyfraser/sysen.git
cd sysen
```

Pull updates as the term goes on:

```sh
cd sysen
git pull
```

You won't push to this repo — it's read-only for students.

If you use RStudio, open `project.Rproj` after cloning. That sets your working
directory to the repo root, which is what every path below assumes.

### 2. Install what you need

**R** — run this once, from the repo root:

```r
source("workshops/packages.R")
```

That installs the tidyverse plus the course's statistical and visualization
packages. It takes a while the first time.

**Python** — run this once:

```sh
pip install -r functions/requirements.txt
```

The Python track uses `pandas`, `numpy`, `scipy`, `statsmodels`, and `plotnine`
(the `ggplot2` grammar, in Python).

Both tracks are first-class. Most chapters exist in both R and Python; pick the
one that matches your background and stay on it.

### 3. Run code from the repo root

Scripts load data with paths **relative to the top of the repo**:

```r
library(readr)
onsen = read_csv("workshops/onsen.csv")
```

```python
import pandas as pd
onsen = pd.read_csv("workshops/onsen.csv")
```

So keep the repo root as your working directory. A "file not found" or "No such
file or directory" error almost always means you're sitting inside `code/`
instead of at the top. In R, `getwd()` tells you where you are.

Some chapters read the same CSVs straight off the web instead, so the code runs
without a clone:

```r
diamonds = read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/mydiamonds.csv")
```

Both routes give you the same data.

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
do not always line up with the chapter numbers (see
[`docs/RENAME-PROPOSAL.md`](docs/RENAME-PROPOSAL.md)).

| Textbook chapter | Data in `workshops/` | Scripts in `code/` |
|---|---|---|
| Coding in R | — | `01_workshop.R` |
| Coding in Python | — | `01_workshop.py`, `01_training.py` |
| FMEA in R · FMEA in Python | — | — |
| Visualization with `ggplot` in R | — | `01_recitation.R` |
| Visualization with `plotnine` in Python | — | — |
| Distributions and Descriptive Statistics in R | `la_parishes.csv` | `02_workshop.R`, `02_recitation.R` |
| Distributions and Descriptive Statistics in Python | `la_parishes.csv` | `02_training.py` |
| Functions in R · Functions in Python | — | `03_lesson.R` |
| Probability in R | — | `03_workshop.R`, `03_workshop_solutions.R` |
| Probability in Python | — | `03_training.py` |
| Probability Functions in R | — | `03_workshop.R` |
| System Reliability in R | — | `04_workshop.R`, `04_workshop_solutions.R`, `04_recitation_solutions.R` |
| System Reliability in Python | — | `04_training.py` |
| Statistical Process Control in R | `onsen.csv` | `05_workshop_solutions.R`, `05_recitation.R` |
| Statistical Process Control in Python | `onsen.csv` | `05_training.py` |
| Indices and Confidence Intervals for Statistical Process Control in R | `onsen.csv` | `06_recitation_solutions.R`, `06_workshop_extra.R` |
| Indices and Confidence Intervals for Statistical Process Control in Python | `onsen.csv` | `06_training.py` |
| Useful Life Distributions (Exponential) | `masks.csv` | `07_lesson.R`, `07_recitation.R` |
| Statistical Techniques for Exponential Distributions in R | `masks.csv` | `07_workshop.R` |
| Statistical Techniques for Exponential Distributions in Python | `masks.csv` | `07_training.py` |
| Useful Life Distributions (Weibull, Gamma, & Lognormal) in R | `crops.csv` | `08_workshop_solutions.R`, `08_lesson.R`, `08_recitation.R` |
| Useful Life Distributions (Weibull, Gamma, & Lognormal) in Python | `crops.csv` | `08_training.py` |
| Fault Tree Analysis in R | `fault_tree_engine_nodes.csv`, `fault_tree_engine_edges.csv` (used by the textbook's interactive diagram) | `09_workshop.R`, `09_lesson.R` |
| Fault Tree Analysis in Python | — | — |
| Physical Acceleration Models | — | `10_workshop.R`, `10_lesson.R` |
| Physical Acceleration Models in Python | — | `10_training.py` |
| Bivariate Regression: Modeling Diamond Pricing | `mydiamonds.csv` | — |
| Bivariate Regression: Modeling Diamond Pricing in Python | `mydiamonds.csv` | — |
| Multivariate Regression: Modeling Effects of Disaster on Social Capital | `jp_matching_experiment.csv`, `japan_muni_elections.csv` | `11_recitation.R`, `11_workshop_exercises.R` |
| Multivariate Regression: Modeling Effects of Disaster on Social Capital in Python | `jp_matching_experiment.csv`, `japan_muni_elections.csv` | — |
| Design of Experiments in R | `donuts.csv` | `12_workshop.R`, `12_lesson.R` |
| Factorial Design and Interaction Effects in R | `lattes.csv` | `13_workshop.R`, `13_lesson.R`, `13_examples.R` |
| Factorial Design and Interaction Effects in Python | `lattes.csv` | — |
| Response Surface Methodology in R | `gingerbread_test1.csv`, `gingerbread_test2.csv`, `gingerbread_test3.csv` | `14_workshop.R`, `11_recitation_rsm.R` |
| Response Surface Methodology in Python | `gingerbread_test1.csv`, `gingerbread_test2.csv`, `gingerbread_test3.csv` | — |
| Appendix: `ggplot` tips | — | — |
| Appendix: `mermaid` Block Diagrams (Flowcharts) in R | — | — |
| Appendix: Using `fitdistr` to Fit Distribution Parameters | `crops.csv` | `00_practice_mle.R` |
| Appendix: Statistical Tables and Common Equations | `bn.csv`, `dn.csv`, `chisq.csv`, `k_lower.csv`, `k_upper.csv` | — |

Extras with no chapter of their own: `code/00_*` (demos and side topics),
`code/ZZ_financial_analysis.R` (financial impact analysis), and
`code/15_workshop/` (Shiny dashboards, `plumber` APIs, and parameterized
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
