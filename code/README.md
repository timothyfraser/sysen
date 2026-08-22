# `code` README

The R and Python scripts that go with the textbook chapters at
[timothyfraser.com/sigma](https://timothyfraser.com/sigma/).

File names follow `NN_<kind>.<ext>`:

| Suffix | What it is |
|---|---|
| `_workshop` | the main in-class coding session for that chapter |
| `_lesson` | a shorter walkthrough of one technique |
| `_recitation` | extra practice, usually run in recitation |
| `_training.py` | the Python track's version of a workshop |
| `_solutions` | a worked answer key the instructor shares on purpose |
| `00_*`, `ZZ_*` | side topics and demos with no chapter of their own |

**Run these from the repo root**, not from inside this folder — the scripts load
data with paths like `read_csv("workshops/onsen.csv")`.

**Run them chunk by chunk, not top to bottom.** Most were typed live in class,
so they include false starts, a first attempt that a better one later replaces,
and occasional pseudo-code that won't run. That's deliberate; the polished
version of each analysis is the textbook chapter.

The `NN` in a file name does not always match the chapter number. The table in
the top-level [`README.md`](../README.md) maps every chapter, by title, to its
scripts and data.
