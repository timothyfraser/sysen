# CLAUDE.md — sysen

Course code and data for **SYSEN 5300**, *Systems Engineering and Six Sigma for
the Design and Operation of Reliable Systems* (Cornell). This repo is **public**
and it is one of exactly two things a student needs — the other is the textbook
website.

This file has two audiences. Read the one you are.

---

## If you are a student's agent

**What this repo is for.** Everything you need to do the R and Python work in
SYSEN 5300:

| | |
|---|---|
| `workshops/` | the datasets (`*.csv`) used in the weekly workshops, plus a few workshop scripts |
| `functions/` | reusable course functions (`functions_*.R`, `functions_*.py`) and the `workflow_*` scripts that demonstrate them |
| `code/` | the numbered workshop / recitation / training scripts, R and Python |
| `docs/` | cheat sheets (RStudio, `dplyr`, `ggplot2`, `stringr`) and helper materials |

**How it relates to the textbook.** The course book — *Sigma: Quality and
Reliability Engineering in R and Python* — is the website. The book explains the
concept; this repo holds the code and data you run alongside it. When a chapter
says "load `boots.csv`", that file is in `workshops/` here. Read the chapter,
run the code here.

**Ignore anything about instructor infrastructure.** You may see references in
the wider ecosystem to a private instructors repo, a Canvas permissions broker,
an AI grading pipeline, submodules, or deployment. **None of it is needed for
coursework, and none of it is accessible to you.** It is not a missing
prerequisite and it is not something to go find. If a task seems to require it,
the task is misread — the answer is in the book and in this repo.

**Working style here.** R uses `=` assignment and the `%>%` pipe, with packages
loaded individually (`library(dplyr)`, `library(ggplot2)` — not
`library(tidyverse)`). Python uses pandas + plotnine, matching the book's Python
chapters. Match the surrounding file rather than modernizing it.

---

## If you are an instructor's agent

- **This repo is nested as sigma's submodule** — the federation is
  `sysen_instructors` (private) ⊃ `sigma` (public) ⊃ `sysen` (public, here).
  From sigma, this is a gitlink at `sysen/`; bump it with
  `git submodule update --remote sysen` + commit, in sigma, deliberately.
- **Only `workshops/*.csv` and `functions/functions_*.py` may be mirrored** into
  sigma's `docs-v3/` (via sigma's `tools/sync_assets.py`). `code/` is **not**
  mirrored — it contains `*_solutions.*` files.
- **Never add solutions, answer keys, rubrics, exam content, rosters, grades, or
  student PII here.** This repo is public. Solved versions of assignments,
  grading configuration, and anything Canvas-adjacent belong in the private
  `sysen_instructors` repo. The `*_solutions.R` files already in `code/` are
  legacy worked examples that were published deliberately — that is not license
  to add more; when in doubt, it goes in the private repo.
- **No path, URL, or content referencing `sysen_instructors`** may be added
  here. The firewall runs in one direction only.

### Branches

- **`v2025`** — frozen snapshot of the 2025 state. Backup only; never
  force-push, rebase, or delete it.
- **`main`** — live. This is what students clone and what sigma's submodule
  pointer tracks.

Branch operations across the federation are sequenced in the private repo's
`docs/RUNBOOK-flip.md` and are Tim's call. Agents don't push, don't switch
branches, and don't commit here.
