# tidyfault (Python)

A Python port of **tidyfault**, the R package for tidy fault tree analysis by
Timothy Fraser and Jingyao Tong (GPL-3; <https://github.com/timothyfraser/tidyfault>).
Pure Python: pandas and numpy only, no compiled code.

**Design rule: R is the reference.** Function names, argument names, column
names, column order, row order and return shapes match R. Where the two
disagree, the Python is the bug, with one deliberate exception listed below.
Every ported function is tested against output produced by R itself
(`tests/test_tidyfault_core.py`).

## Install and import

Nothing to install beyond `pandas` and `numpy`. From the repo root:

```python
import sys; sys.path.insert(0, "functions")
import tidyfault as tf

nodes, edges = tf.data.fakenodes, tf.data.fakeedges
gates = tf.curate(nodes, edges)          # R: curate(nodes = fakenodes, edges = fakeedges)
equation = tf.equate(gates)              # " ( ( (B *  (C + D) )  *  (A +  (B * C) ) ) ) "
f = tf.formulate(equation)               # function (A, B, C, D)
truth = tf.calculate(f)                  # 16-row truth table, failures first
tf.quantify_prob(f, [0.10, 0.20, 0.05, 0.15])   # 0.01285
tf.tabulate(["B*C", "A*B*D"], formula=f) # coverage 0.8 and 0.4
```

## The data model

A fault tree is two tables, exactly as in R:

| table | columns | meaning |
|---|---|---|
| `nodes` | `id`, `event`, `type` | one row per node; `type` is `top`, `and`, `or` or `not` (not a gate = basic event), a Categorical with R's factor levels in R's order |
| `edges` | `from`, `to` | one row per link, parent id to child id |

A basic event that feeds two branches appears twice in `nodes`, same `event`,
different `id`. `tf.validate_tree(nodes, edges)` (Python only) checks a tree
and names every problem it finds.

## R | Python

| R | Python | status |
|---|---|---|
| `curate(nodes, edges)` | `curate(nodes, edges)` | ported; tested against R on 7 trees |
| `equate(data)` | `equate(data)` | ported; tested against R on 7 trees (see deviation) |
| `formulate(formula)` | `formulate(formula)` returns a callable `Formula` | ported; arguments and printed body match R |
| `formalArgs(f)` | `formal_args(f)` | helper |
| `calculate(f)` | `calculate(f)` | ported; full truth tables match R row for row |
| `quantify_prob(f, newdata, truth_table)` | `quantify_prob(f, newdata, truth_table=None)` | ported (top-event probability); matches R to 1e-9 |
| `tabulate(data, formula, method, query)` | `tabulate(data, formula, method="mocus_rcpp", query=False)` | ported; matches R |
| `populate(binary_outcomes, event_probs)` | `populate(binary_outcomes, event_probs)` | ported; matches R |
| `gate(data, group, gate, size, res)` | `gate(data, group="id", gate="type", size=1, res=50)` | ported; polygons match R |
| `gate_and(size, res)`, `gate_or`, `gate_top` | same names | ported; coordinates match R to 1e-12 |
| `get_gate(x, y, gate, size, res)` | `get_gate(x, y, gate, size=1, res=50)` | ported |
| `data("fakenodes")` and the other 26 datasets | `tf.data.fakenodes`, `tf.load_data("fakenodes")` | all 27 bundled as CSV |
| `concentrate(data, method)` | | not yet |
| `mocus()`, `mocus_r()`, `mocus_rcpp()`, `mocus_cpp()` | | not yet (no Rcpp; pure Python planned) |
| `quantify(f, newdata, prob, fast)` | | not yet |
| `quantify_binary()`, `quantify_binary_fast()`, `quantify_prob_fast()` | | not yet |
| `simulate()` | | not yet |
| `illustrate()`, `plot()` | | not yet |

## Deliberate deviations from R

1. **`equate()` matches gate names as whole names.** R uses each gate name as a
   regex and matches it *anywhere* in a set. When one name sits inside another,
   R goes wrong. On the bundled `ai_nodes` tree, gate `T` matches inside basic
   event `TO`, and R's `equate()` never returns: the string grows until memory
   runs out. The port gives the intended equation, `" ( (AF + TO + RL)  + CWE) "`.
   That is what R produces once the top event is renamed. On every other bundled
   tree the two agree character for character.
2. **`equate()` refuses a cycle.** If gates reference each other in a loop,
   R loops forever. Python raises `ValueError` and names the loop.
3. **`formulate()` never calls `eval()`.** The equation is parsed by a small
   `+` / `*` / parentheses grammar, so a malformed or hostile string raises
   `ValueError` and is never executed. Argument order follows R's `sort()` under
   an English locale: case-insensitive, lowercase first on ties.
4. **`tabulate()` reads a `~` (NOT) prefix as "this event is 0"**, which is
   what R means. R's own `filter(~A == 0)` would error.

Whole-number columns in the datasets (ids, 0/1 indicators) load as `int64`. R
stores them as double, but the values are identical.

## Reference outputs

`reference/make_r_reference.R` sources the R functions straight from a
tidyfault checkout, runs them on every bundled tree and writes
`reference/r_reference.json`. The tests compare against that file. To
regenerate it:

```
cd functions/tidyfault/reference
Rscript make_r_reference.R <path-to-tidyfault-source> r_reference.json
```

`data/*.csv` were converted from the R package's `data/*.rda` with `pyreadr`.
