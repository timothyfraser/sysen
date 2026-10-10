# `workshops` — the data

This is where the **data** lives. Every `.csv` file here is a spreadsheet of
numbers that a textbook chapter analyzes. When a chapter says
`read_csv("workshops/onsen.csv")`, this folder is the folder it means.

You'll rarely open these files by hand. You point your code at them and let R or
Python read them in for you.

## Reading a dataset in

```r
library(readr)
onsen = read_csv("workshops/onsen.csv")
```

```python
import pandas as pd
onsen = pd.read_csv("workshops/onsen.csv")
```

Look at the path: `workshops/onsen.csv`, not just `onsen.csv`. It's written that
way because your code runs from the **top of the project folder**, one level up
from here — so the way to reach this file from there is "go into `workshops`,
then take `onsen.csv`."

### Making that happen automatically

You don't have to arrange that by hand. Double-click **`project.Rproj`** in the
top folder, and R opens with the top folder already set as the place it starts
looking from. Every path in every chapter then works exactly as written, with
nothing for you to change. In Posit Cloud, opening the course project does the
same thing for you.

### If it says the file isn't there

`cannot open file 'workshops/onsen.csv'` or `No such file or directory` almost
always means R is looking from the wrong place — usually from inside `code/`
instead of from the top. Type `getwd()` in the Console: it prints the folder R
is currently looking from. If it ends in `/code`, that's your answer. Close the
project and reopen it with `project.Rproj`.

Nothing about this means you broke anything. It is the most common first-week
error in the course.

## Day one: `packages.R`

`packages.R` is the one file in here that isn't data. A **package** is a bundle
of extra commands that someone else wrote and shared; this course leans on a
couple dozen of them. `packages.R` installs the whole set in one go.

Run it **once**, at the start of the term, from the top of the project folder:

```r
source("workshops/packages.R")
```

It takes a while the first time — go get coffee. You may see warnings about
packages built under a different version of R; those are safe to ignore. After
this, you only ever need `library(...)` at the top of a script.

On the Python side, the one-time equivalent is:

```sh
pip install -r functions/requirements.txt
```

## Reading data straight off the web

Some chapters skip the local file entirely and read the same data from the
internet, so the code runs anywhere:

```r
diamonds = read_csv("https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/mydiamonds.csv")
```

Same numbers either way. Use whichever one the chapter shows you.

## Where the data came from

Most files here were collected or simulated for this course. The ones below come
from outside sources, so each carries a license and a citation.

| File | What it is | Source and license |
|---|---|---|
| `concrete.csv` | 1,030 concrete mixes: 8 recipe/age inputs (`cement`, `slag`, `ash`, `water`, `superplasticizer`, `coarse`, `fine` in kg/m³, and `age` in days) and `strength` (compressive strength, MPa). | I-Cheng Yeh (1998), *Concrete Compressive Strength* [Dataset], UCI Machine Learning Repository, <https://doi.org/10.24432/C5PK67>. Licensed CC BY 4.0. Column names shortened; values unchanged. |
| `castings_split.csv` | An **index only**: 7,283 rows (`file`, `label`, `split`) saying which casting photo goes in `train`, `valid` or `test`, and whether it is a `defect` or `ok`. 65 test photos that duplicate training photos are left out. | Built for this course from the Kaggle dataset "Casting product image data for quality inspection" (ravirajsinh45; photos from Pilot Technocast, Rajkot), <https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product>. The photos are licensed CC BY-NC-ND 4.0, so they are **not** in this repo and nobody here shares resized copies of them. You download them from Kaggle (free account) and run `code/prepare_castings.R` or `code/prepare_castings.py`, which shrinks them to 64 × 64 grayscale PNGs in `workshops/castings/`. That folder is created on your own computer and is never committed. |

## Which dataset goes with which chapter

The table in the top-level [`README.md`](../README.md) lists every chapter by
title, alongside its datasets and its scripts.

---

<sub>Maintainers: conventions for this folder are in [`CLAUDE.md`](../CLAUDE.md).</sub>
