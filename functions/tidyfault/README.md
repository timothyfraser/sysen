# tidyfault (Python)

A Python port of **tidyfault**, the R package for tidy fault tree analysis by
Timothy Fraser and Jingyao Tong (GPL-3; <https://github.com/timothyfraser/tidyfault>).
Pure Python: pandas and numpy only, no compiled code.

**Design rule: R is the reference.** Function names, argument names, column
names, column order, row order and return shapes match R. Where the two
disagree, the Python is the bug, with the deliberate exceptions listed below.
Every ported function is tested against output produced by R itself
(`tests/test_tidyfault_core.py`, `tests/test_tidyfault_mocus.py`).

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
tf.concentrate(gates)                    # ["B*C", "A*B*D"], the minimal cut sets
tf.quantify(f, [True, True, True, False])            # True: the top event occurs
tf.quantify(f, [0.10, 0.20, 0.05, 0.15], prob=True)  # 0.01285
sim = tf.simulate(n_gates=3, n_basic=8, seed=1)      # {"nodes", "edges", "prob"}
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
| `mocus(data, method)` | `mocus(data, method="mocus_rcpp", top="or")` | ported, pure Python (no Rcpp); with `top="and"` the cut sets equal R's `mocus_r()` and `mocus_rcpp()` element for element on 6 trees (see deviation) |
| `mocus_r(data)`, `mocus_rcpp(data)`, `mocus_cpp(data)` | same names, plus `top="or"` | ported; one pure-Python queue algorithm behind all of them |
| `concentrate(data, method)` | `concentrate(data, method="mocus_rcpp", top="or")` | ported; with `top="and"` equals R on 6 trees for all three methods (see deviation) |
| `quantify(f, newdata, prob, fast)` | `quantify(f, newdata, prob=False, fast=True)` | ported; reproduces R on the `*_outcomes_binary` datasets and on 3 probability scenarios per tree to 1e-9 |
| `quantify_binary(f, newdata)` | `quantify_binary(f, newdata)` | ported; DataFrame in, bool array out; one scenario in, one bool out |
| `quantify_binary_fast()`, `quantify_prob_fast()` | same names | aliases of `quantify_binary()` and `quantify_prob()`; R's fast paths return the same values |
| `simulate(n_gates, n_basic, p_range, seed)` | `simulate(n_gates=3, n_basic=8, p_range=(0.01, 0.2), seed=None)` | ported; returns `{"nodes", "edges", "prob"}`, R's list shape; seeded draws differ from R's (see deviation) |
| `illustrate(nodes, edges, type, node_key, layout = "tree", size, scale_size, res)` | `illustrate(nodes, edges, type="nodes", node_key="id", layout="tree", size=0.25, scale_size=False, res=50)` returns a DataFrame or a dict of `nodes`/`edges`/`gates`(/`pairwise`) | ported (igraph Reingold-Tilford tree layout); coordinates match R to 1e-9 on 5 trees; only `layout="tree"` |

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
5. **`mocus()` and `concentrate()` read the top event as OR by default, as the
   equation does.** R disagrees with itself when the top event has several
   children: `curate()` and `equate()` join them with OR, but R's MOCUS
   expands the top event like an AND gate. Minimal tree: top event T with
   children A and B. `equate()` gives `" (A + B) "`, so A alone fails the
   system, yet R's `concentrate()` returns the single cut set `"A*B"`. The
   port's default, `top="or"`, gives `["A", "B"]`, cut sets that agree with
   `equate()`, `formulate()` and `calculate()`. `top="and"` reproduces R
   exactly, and the tests check both. Trees whose top event has one child
   (`fakenodes`, `breach_nodes`) give the same answer either way; `db_nodes`,
   `ai_nodes` and `security_nodes` do not (e.g. db: R gives four 6-event cut
   sets, the equation gives `AF`, `AUF`, `DC`, `NF`, `BF*SF`, `HF*MF`).
6. **`concentrate()` minimises by absorption, not `admisc::simplify()`.** MOCUS
   cut sets are products of plain basic events, so the minimal cut sets are
   the sets left after dropping duplicates and supersets. Output order follows
   admisc: fewer events first, then by sorted event position. Where R falls
   back to the unsimplified string (admisc's `'sols' not found` error), the
   port still returns minimal sets.
7. **`simulate(seed=)` draws from numpy, not R's random stream.** Same
   arguments, checks and return shape; a seed reproduces Python runs but not
   the tree R draws for the same seed.

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

The MOCUS, `concentrate()` and `quantify()` fixtures cover the minimal tree,
`fake`, `db`, `ai`, `security` and `breach`. `it_security` is skipped: R's
`concentrate()` does not finish on it in minutes. A full run takes about a
minute under R 4.5.2.

`data/*.csv` were converted from the R package's `data/*.rda` with `pyreadr`.
| `plot(x, ...)` (ggplot) | `plot(ill, ...)` returns a matplotlib `Figure`; `to_png(fig, path, dpi=300)` | ported; same shapes, viridis fills, labels and legend as R |
