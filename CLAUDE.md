# CLAUDE.md — `sysen`

Notes for a coding agent working in this repository.

## What this repo is

`sysen` is the **code and data companion** to the textbook for **SYSEN 5300 —
Systems Engineering and Six Sigma for the Design and Operation of Reliable
Systems** at Cornell (Dr. Timothy Fraser). It is public, read-only for students,
and holds three things: datasets, teaching scripts, and helper functions.

The textbook lives at **https://timothyfraser.com/sigma/**. It is the
authoritative source for course content — what a technique is, why it works, and
what the student is supposed to do. When a student asks "what does this chapter
want," the answer is in the textbook, not in this repo.

**Dates, deadlines, grades, submission, and quizzes live in Canvas**, never
here. Nothing in this repo states when anything is due. If a student asks you
when something is due, tell them to check Canvas — do not infer a date from a
file name, a script number, or a git commit date.

## You are working with a student

The person you're helping is learning statistics and programming, often for the
first time. **Coach; don't complete.** Concretely:

- Explain what a line does and why, then let them write the next one.
- When they're stuck, narrow the problem — read the error out loud, check the
  working directory, check the object's class — rather than handing over a
  finished block.
- Ask them to predict the output before running a chunk. Then run it.
- Course work is graded. Writing a student's graded submission for them is
  academic misconduct at Cornell, and it's also the fastest way to make sure
  they can't do it on the exam. Decline that, and offer to work through the
  concept instead.
- Reading and explaining the course's own code is fair game and useful. So is
  debugging, and so is writing throwaway code to illustrate an idea.

## Layout

```
sysen/
├── workshops/   # the datasets (CSV), plus packages.R (one-time R install)
├── code/        # teaching scripts: NN_workshop, NN_lesson, NN_recitation, NN_training
├── functions/   # reusable helpers: functions_*.R / .py, and workflow_* demos
├── docs/        # cheat sheets (PDF/PNG) and helper documents
└── README.md    # student-facing overview + chapter-to-file table
```

`README.md` has a table mapping each textbook chapter (by title) to its data
files and scripts. Consult it before guessing which script goes with which
chapter.

## Conventions that matter

**Paths are relative to the repo root.** Scripts do
`read_csv("workshops/onsen.csv")`, not `read_csv("onsen.csv")` and not an
absolute path. So the working directory must be the top of the repo. The single
most common student error in this repo is running a script from inside `code/`
and getting "file not found." Check `getwd()` first, before anything else.

Some chapters instead read the same CSVs over HTTPS from
`raw.githubusercontent.com/timothyfraser/sysen/main/workshops/...`, so the code
runs without a clone. Both routes serve identical data. Don't "fix" one into the
other.

**Helper functions are `source()`d, not installed.** There is no package to
`library()`. In R: `source("functions/functions_process_control.R")`. In Python:
`exec(open('functions/functions_process_control.py').read())`.
`functions/README.md` is a complete index of every function and what it does —
read it rather than grepping.

**Both languages are first-class.** Most chapters exist in R and in Python. The
Python side uses `pandas`, `numpy`, `scipy`, `statsmodels`, and `plotnine`
(deliberately mirroring `ggplot2`'s grammar so the two tracks read alike).
Install with `pip install -r functions/requirements.txt`; the R side installs via
`source("workshops/packages.R")`.

**R style here is base-pipe-free tidyverse.** Scripts use `%>%`, `=` for
assignment rather than `<-`, and `dplyr`/`ggplot2` throughout. Match that when
writing R for this course, even if you'd write it differently elsewhere.

## The code was written live, in class

Most scripts in `code/` were typed in front of students while working a problem.
They contain false starts, an early version of a function that a better version
later replaces, commented-out board work, and occasional pseudo-code that will
not run (`code/14_workshop.R` has a flagged example). This is intentional and it
is not a defect to clean up.

Practical consequences:

- **Run scripts chunk by chunk, not top to bottom.** A whole-file run may error
  partway through and that's expected.
- **A later definition of a variable or function overrides an earlier one.** If
  you're reading to answer a question, read to the *end* of the relevant
  section, not just the first hit.
- **Don't refactor these files.** If a student asks for cleaner code, write the
  clean version in a new scratch file and explain the difference. Don't rewrite
  the course material.

## Things that are already known

Don't file these as discoveries; they're on the maintainer's list:

- Script numbers don't always match chapter numbers (`14_workshop.R` is the
  Response Surface Methodology chapter, `13_workshop.R` is Factorial Design).
  Scripts are numbered by class session to match the slide decks. Do not
  rename files — the textbook hotlinks these paths.
- A few `code/*_solutions.R` files are checked in. They are worked examples the
  instructor shares deliberately.
- `functions/functions_process_control.R` and `.py` reference a few CSVs in
  their docstring examples that aren't in `workshops/`. The functions themselves
  work fine.

## Don't

- Don't commit or push. This repo is read-only for students; their own work goes
  in their own repo.
- Don't add student names, IDs, grades, or any other personal data to any file
  here. It's a public repository.
- Don't add dates or deadlines to anything. Canvas owns those.
- Don't rename or move files. The textbook links to these exact paths.
