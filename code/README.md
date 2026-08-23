# `code` — the scripts from class

This folder holds the R and Python **scripts** we work through in class. A
*script* is just a text file full of code, saved so you can run it again later;
its name ends in `.R` or `.py`.

You'll come here when a class session or a textbook chapter points you at a
file. You don't need to read the whole folder, and you never need to run every
file — open the one for the session you're on and leave the rest alone.

The tidy, written-out version of every analysis lives in the textbook at
[timothyfraser.com/sigma](https://timothyfraser.com/sigma/). What's in here is
the in-class working copy of the same material.

## How to run one of these

You'll do this in **Posit Cloud**, the browser version of R you set up in the
first workshop. Nothing to install.

1. Open the course project. In the **Files** window (bottom right), click the
   `code` folder, then click the file you want.
2. It opens in the **Scripts** window (upper left).
3. Highlight a line or two with your cursor, then press **CTRL** and **ENTER**
   simultaneously — or click the **Run** button above the script. (On a Mac, use
   the Mac equivalent, **Command** and **Return**.)
4. The result shows up in the **Console** (bottom left). Read it, then move down
   and run the next couple of lines.

The `.py` scripts work the same way, and it matters more there: they're written
REPL-style, so running one top to bottom prints almost nothing. Open an
interactive Python console and send a few lines at a time, exactly as you would
in R.

**Go a few lines at a time. Don't run the whole file top to bottom.** Most of
these scripts were typed live, in class, while working through a problem with
students. They read that way on purpose: false starts, a first attempt that a
better one replaces a few lines later, and the occasional bit of pseudo-code
that was only ever meant for the board. Running the file straight through will
throw errors that aren't your fault. Running it a few lines at a time is how
it's meant to be used — and it's how you actually see what each line does.

## If you get an error

Errors are normal. You will get them constantly, and so does everyone else,
including your instructor. Nearly all of them are one of three things:

- **`there is no package called ...`** or **`could not find function ...`** —
  the script needs a *package* (a bundle of extra commands someone else wrote
  and shared) that isn't installed yet. Run `workshops/packages.R` once, at the
  start of the term, and this goes away. That's normal, not something you broke.
- **`cannot open file 'workshops/onsen.csv'`** — R is looking in the wrong
  folder. [`workshops/README.md`](../workshops/README.md) has the one-click fix.
- **a missing parenthesis or quotation mark** — the most common error there is.
  Count your `(` against your `)`, and your `"` against your `"`.

If it's none of those, bring the error to recitation or office hours. Paste the
whole message; it usually says more than it looks like.

## R or Python?

Both tracks are first-class, and you only need one. Pick the language that fits
your background and stay with it.

A script and its twin in the other language **share a name**: `01_workshop.R`
and `01_workshop.py` are the same class session, each written in the style of
its own textbook chapter. Not every session has both twins.

## What the file names mean

The number at the front is the **class session number** — the number on the
slide deck that was up on screen. `11_workshop.R` is the code from Workshop 11.
It is not the textbook chapter number, and not the calendar week.

| Part of the name | What it means |
|---|---|
| `11_` | the class session number, zero-padded. `11_workshop.R` goes with Workshop 11. |
| `07b_` | a session split across two decks: `07b_workshop.R` goes with Lesson 7B. |
| `_workshop` | the main in-class coding session for that slot |
| `_lesson` | a shorter walkthrough of a single technique |
| `_recitation` | extra practice, worked in recitation |
| `_solutions` | a worked answer key, shared on purpose |
| `_<topic>` | added only when one session draws on two chapters and the names would collide (session 9: `09_workshop*` is maximum likelihood, `09_recitation*` is fault tree analysis) |
| `00_`, `ZZ_` | side topics and demos that don't belong to any one session |
| `.R` / `.py` | the R track and the Python track |
| `apps/` | a folder, not a session — the Shiny dashboards, `plumber` APIs, and parameterized report |

Every script opens with a short header naming itself, the author, the session it
belongs to, and the textbook chapter it pairs with. If you're not sure what a
file is for, read its first four lines.

## What the `_solutions` files are

A file ending in `_solutions` is a worked answer key — the same exercise with
the answers filled in. They're shared deliberately, so use them. The order that
actually teaches you something is: try it yourself, get stuck, *then* open the
solutions file and compare line by line. Reading the answer before you've tried
it feels efficient and teaches you almost nothing.

## Finding the file you want

The table in the top-level [`README.md`](../README.md) lists every textbook
chapter by title, with the scripts and datasets that go with it. That's the
fastest way in.

---

<sub>Maintainers: conventions for this folder are in [`CLAUDE.md`](../CLAUDE.md).</sub>
