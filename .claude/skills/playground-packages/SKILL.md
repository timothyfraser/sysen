---
name: playground-packages
description: The one rule for R packages in sigma's in-browser playgrounds (webR). Heavy packages are never installed; they are base-R stand-ins defined once in docs-v3/assets/playground-live.js, and every R surface (chapter playgrounds, deck playgrounds, labs) shares that one shim and one install choke point. Load it before touching any playground, starter code, deck preset (packagesR), chapter pre-warm list, contract entry or tools/gen_contract.py allow-list that names an R package, and before adding a library() call to anything that runs in the browser.
---

# Playground packages (R / webR)

> **Load this when** you add or change: a playground starter, a deck preset in
> `docs-v3/assets/slide-playground.js` (`r:` starter, `packagesR`), a chapter's
> contract `packages` (the background pre-warm list), `WASM_SAFE_R` in
> `tools/gen_contract.py`, or any `library()` / `require()` / `pkg::` that a
> browser playground will run.

## Why this exists

On 2026-09-25 the recitation-5 deck took minutes to load. The SPC chapter's
pre-warm list (generated from `WASM_SAFE_R` in `tools/gen_contract.py`) named
`ggpubr` and `moments`. The pre-warm installed the **real** ggpubr, with about 50
dependencies, into the IndexedDB package cache that **every** playground on
the site shares. The `library()` shim then saw `requireNamespace("ggpubr")`
succeed and attached the real package, so the deck loaded the full package too.
Tim, 2026-09-25: *"We must not have these dumb things where we've fixed one
playground, but then the other playground still has the same issue."*

## The rule

1. **A heavy package gets a base-R stand-in, not an install.** The stand-in
   lives in `R_CALC_STANDIN` in `docs-v3/assets/playground-live.js`, and the
   package name goes into `R_NO_INSTALL` in the same file.
2. **There is one install choke point, and it refuses those names.**
   `installOneR()` in `playground-live.js` is where every install path ends:
   a Run's `library()` scan (`libRefsR`), a chapter's contract pre-warm list
   (`prewarmR`), a deck preset's `packagesR`, and the `install.packages()` shim.
   An `R_NO_INSTALL` name returns before it reaches `webr::install`.
3. **The shim always attaches the stand-in**, even when a real copy is in the
   cache. A real copy in a browser cache only ever got there by accident.
4. **A poisoned cache heals itself.** On boot, `bootR()` deletes any real copy
   of an `R_NO_INSTALL` package it finds in the persistent library.
5. **All R surfaces share this one shim.** Never write a per-surface install
   list, a per-deck workaround, or a second copy of a stand-in. If one surface
   needs a fix, the fix goes in `playground-live.js`, and every surface gets it.
6. **No install list may name a stand-in.** That covers deck `packagesR`, the
   contract `packages`, and `WASM_SAFE_R` in `tools/gen_contract.py`. Starters
   may `library(ggpubr)` etc.: the shim answers that call.

## Current stand-ins

| Package | Stand-in provides | Not provided |
|---|---|---|
| `mosaicCalc` | `D()` (symbolic derivative via `stats::D`) and `antiD()` | everything else in mosaic/mosaicCalc |
| `ggpubr` | `ggarrange()` (plots side by side or in a grid; `plotlist`, `ncol`, `nrow`, `widths`, `heights`) | every other ggpubr function |
| `moments` | `skewness()` and `kurtosis()` (both accept `na.rm`) | every other moments function |

When a student calls `library(<name>)`, the console says what the stand-in
provides, for example `[ ggpubr: this course stand-in provides ggarrange() only ]`.
`install.packages("<name>")` prints `course stand-in built into this playground
-- not installed; just call library()` and installs nothing. In RStudio the
real packages load as usual, because RStudio never runs this file.

## Adding a new stand-in (5 steps)

1. **Check that it is actually heavy.** Count its dependency tree in webR's
   index (`repo.r-wasm.org/bin/emscripten/contrib/<R version>/PACKAGES`). A
   light package with a webR build goes on `STARTER_ALLOW` in
   `tests/test_playground_packages.py` instead.
2. **Write the stand-in in base R**, inside `R_CALC_STANDIN` in
   `playground-live.js`. Implement only the functions the course uses, keep
   the helpers dot-prefixed, and assign into the `sigma:course-standins`
   environment the same way the existing `.sigma_standin_attach` branches do.
   Print a one-line notice that names exactly which functions it provides.
3. **Add the name to `R_NO_INSTALL`**, and to the name checks in the
   `library()` / `require()` shims in `R_CALC_STANDIN`.
4. **Take the name out of every install list**: deck `packagesR`, `WASM_SAFE_R`
   in `tools/gen_contract.py`, then regenerate the contract (`contract/chapters.json`
   and `docs-v3/assets/contract.js`). Add it to the test's expected stand-in
   set.
5. **Bump the cache token** (below), then run the test and do the browser check.

## Bumping the cache token

Every page must load the playground scripts at the current token, or a
student's browser keeps running the old shim.

1. `python -X utf8 -P tools/bump_cachebust.py <TOKEN>` rewrites every
   `assets/*.js|css?v=` in docs-v3 HTML **except the `labs/` tree**, and the
   `.js?v=` strings in `assets/sigma-shell.js`.
2. **Then bump these by hand, because the tool does not touch them:**
   - `docs-v3/labs/*.html`: every `assets/...?v=`, including
     `labs/slide-playground.html`'s `slide-playground.js?v=`.
   - `docs-v3/assets/slide-playground.js`: the
     `loadScript('../assets/playground-live.js?v=...')` string.
   - `docs-v3/slides/*.html`: the deck iframes'
     `slide-playground.html?preset=...&v=...` query.
3. Search for the old token afterwards. It should appear nowhere.

## Verify

- **Test:** `python -X utf8 -P -m pytest tests/test_playground_packages.py -q`
  checks the choke point, the shim, every install list, the contract, the
  starters, and that every playground script reference has the current token.
- **Browser check:** open a deck playground and the chapter in a fresh browser
  profile, with `navigator.webdriver` unset, because both surfaces keep the live runtime
  off under webdriver. Run the starter and read the network log. It must
  show **no** package-file fetch (`repo.r-wasm.org/bin/...`) for a stand-in or
  anything in its dependency tree. Also check the poisoning path: let the
  chapter's pre-warm finish, then open the deck in the same profile.
