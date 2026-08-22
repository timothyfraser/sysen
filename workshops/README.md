# `workshops` README

This folder holds the **datasets** for the course. When a textbook chapter says
`read_csv("workshops/onsen.csv")`, this is the file it means.

Load them with a path relative to the **repo root**, not to this folder:

```r
library(readr)
onsen = read_csv("workshops/onsen.csv")
```

```python
import pandas as pd
onsen = pd.read_csv("workshops/onsen.csv")
```

If you get "file not found," you're almost certainly running from inside
`code/` instead of the top of the repo. Check `getwd()` in R.

Some chapters read the same files straight off the web, using
`https://raw.githubusercontent.com/timothyfraser/sysen/main/workshops/<file>.csv`.
Same data either way.

`packages.R` is the one non-data file here: run it once, at the start of the
term, to install the R packages the course uses.

The table in the top-level [`README.md`](../README.md) says which dataset goes
with which textbook chapter.
