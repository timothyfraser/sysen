# `code` README

The R and Python scripts that go with the textbook chapters at
[timothyfraser.com/sigma](https://timothyfraser.com/sigma/).

## How files are named

```
NN[b]_<kind>[_<topic>][_solutions].<ext>
```

| Token | What it means |
|---|---|
| `NN` | **the class session number** — the number on the slide deck (`Workshop 11` → `11`), zero-padded. Not the textbook chapter number and not the calendar week. |
| `b` | a split session, where one session number carries two decks: `07b_workshop.R` goes with Lesson 7B. |
| `_workshop` | the main in-class coding session for that slot |
| `_lesson` | a shorter walkthrough of one technique |
| `_recitation` | extra practice, run in recitation |
| `_<topic>` | only when one session draws on two chapters and the names would otherwise collide (session 9: `09_workshop*` is maximum likelihood, `09_recitation*` is fault tree analysis) |
| `_solutions` | a worked answer key the instructor shares on purpose |
| `00_*`, `ZZ_*` | side topics and demos with no session of their own |
| `.R` / `.py` | the R track and the Python track. **A pair shares a basename**: `01_workshop.R` and `01_workshop.py` teach the same session, each in the style of its own textbook chapter. |
| directories | named, not numbered: `apps/` holds the Shiny dashboards, `plumber` APIs and parameterized report. A directory is not a session. |

Every script opens with the same four-line header: its own filename, the author,
the session slot and topic it belongs to, and the textbook chapter it pairs with,
by title.

## How to run them

**Run these from the repo root**, not from inside this folder — the scripts load
data with paths like `read_csv("workshops/onsen.csv")`.

**Run them chunk by chunk, not top to bottom.** Most were typed live in class,
so they include false starts, a first attempt that a better one later replaces,
and occasional pseudo-code that won't run. That's deliberate; the polished
version of each analysis is the textbook chapter.

The table in the top-level [`README.md`](../README.md) maps every chapter, by
title, to its scripts and data.
