---
name: slide-design
description: The DESIGN half of a SYSEN 5300 deck, in Tim's words from his 2026-10-20 phone reviews - the eight slide archetypes (Example with Show answer, Activity slide with the embedded activity page, Visual-helper "picture of the design" with tooltips, Image-right humanizing photo, Animation / Visualizer / Playground each on a full slide, Dataset / tools cards, Table slide, Section divider) with real markup, plus spacing and margins, code, numbering, replication, humour and photos (Unsplash view-before-use rule), and the two blind spots no gate catches. Use when someone says "slide design", "make the slides look like mine", "archetype", "Show answer", "activity slide", "image-right", "picture of the design", "Unsplash", or when running a per-deck design unit.
---

# slide-design

**Hygiene and fidelity are not here.** The faithful-port rules, the fidelity
map and the contact sheets are `specs/SLIDES.md` §7; the gates are §8 (the
instructor-side `slides-authoring` skill carries the same rules). Read those
first; this skill never restates them. Normative markup: `specs/SLIDES.md` §3
(archetype table + components) and §5.5 (answers and tooltips). The plan of
record is the course plan.

Tim, 2026-10-20: *"spacing, margins, card use, use of interesting, amusing
visuals, replication code, and also screenshots turned into graphs with
replication code."* Every class below exists in `docs-v3/assets/slides.css`
today; build nothing parallel (an engine change is a one-line request back to
the orchestrator).

## 1. The eight archetypes

| # | Archetype | When (Tim's words) | Markup |
|---|---|---|---|
| 1 | Example | every "Example N" / exercise: *"Show Answer on every example/exercise ... forever more"*; never an answer visible by default (*"I could have turned that into a think-pair-share"*) | `s-agenda s-example` + `.lang-pair` + `.answer[data-answer=output]` |
| 2 | Activity | the in-class activity: *"too much text ... a link and/or an embedded glimpse of that activity ... fill the white space"* | `s-agenda` + `data-activity` + `iframe.embed.embed--full` |
| 3 | Visual helper | a design or mechanism students must picture: *"visualize Greco-Latin and Youden squares ... a helper visual ... interactive tooltips"* | inline `svg.fig`, `data-tip` on every cell/node |
| 4 | Image-right | humanize a concept slide: *"approachable images ... industrial process ... people in the images, not always a white dude ... half the page on the right"* | `s-topbar` + `.cols--21.cols.middle`, `img[data-photo]` right |
| 5 | Animation / Visualizer / Playground | *"animation, visualizer, playground on separate slides, filling the page"* | `s-topbar` + `iframe.embed--full` of `labs/slide-<topic>.html?view=anim\|viz` |
| 6 | Dataset / tools | where students pick data: *"cards ... the CSVs supported in team boards ... a link to the team boards"* | `s-topbar s-cards` + `.cards.cards--2` > two `.card` |
| 7 | Table | any 2025 table or matrix: *"a little spacing between the tables"*; header *"enormous instead of a line break"* | `table.tbl` (+`.tbl--fit`), `th/td.num`, tints `t-b t-o t-p t-lav t-rose t-rd`, `.caption` |
| 8 | Section divider | between parts; `img.cutout` when the 2025 deck had a photo there | `s-section` + `hr.rule` + `img.cutout[data-photo]` |

### 1 Example - code visible, output behind Show answer
`data-answer="all"` (code hidden too) only when the task is "write the code
yourself". Wrapper carries the track (`data-lang`) so the toggle follows R | Python.
From `32_slides_lesson_13.html` (Example 4):
```html
<section class="slide s-agenda s-example">
  <div class="panel"><h1>Example 4</h1><div class="sub">Coding Three-Way Interaction Effects</div>
    <p>Estimate the three-way interaction of <strong>T</strong>, <strong>K</strong> and <strong>C</strong>.</p></div>
  <div class="side"><div class="lang-pair">
<pre data-lang="r"><span class="cm"># T x C effect at each K (A, B), then TCK</span>
c(tc("A"), tc("B"), (tc("B") - tc("A")) / 2)</pre>
<pre data-lang="py">print(tc("A"), tc("B"), (tc("B") - tc("A")) / 2)</pre>
<div class="answer" data-answer="output" data-lang="r" data-output><pre class="ocard">[1] 1.0 2.0 <b class="k">0.5</b></pre></div>
<div class="answer" data-answer="output" data-lang="py" data-output><pre class="ocard">1.0 2.0 <b class="k">0.5</b></pre></div>
  </div></div>
</section>
```
A chart beside the code: `.side.side--fig` (SLIDES.md §3 fit levers).

### 2 Activity - tagline + the page itself, never copied task text
The activity page is the single source of truth; dates live only in Canvas.
From `33_slides_workshop_13.html`:
```html
<section class="slide s-agenda" data-activity="explain-it-factorial-experiments">
  <div class="panel">
    <h1>Group Activity: Explain It</h1>
    <p>Factorial Experiments &middot; submit on Canvas</p>
  </div>
  <div class="side">
    <iframe class="embed embed--full" title="Activity: Explain It (Factorial Experiments)" loading="lazy" src="../activities/explain-it-factorial-experiments.html"></iframe>
  </div>
</section>
```

### 3 Visual helper - one picture of the design, a tip on every cell
Inline the SVG (an `<img>` cannot carry tips). Where one cell encodes several
things, add a nomenclature explainer ("How to read a cell"). From
`42_slides_lesson_12b.html` (Latin square, generated by
`functions/slides_latin_squares.py`):
```html
<svg class="fig" style="width:300px;height:auto" viewBox="0 0 560 462" role="img" aria-labelledby="lat-t lat-d">
  <title id="lat-t">4 x 4 Latin square of additives</title>
  <g id="lat-I-1" data-tip="Driver I · Car 1 · Additive A · 19 (pollution)">
    <rect x="96" y="54" width="116" height="88" fill="#dce8f8" stroke="#1f1f1f" stroke-width="2"/>
    <text x="154" y="98" font-size="40" text-anchor="middle">A</text></g>
  <!-- ... one <g data-tip> per cell -->
</svg>
```
HTML tables take tips too: `<td style="text-align:center" data-tip="Block 1 · Treatment B · Position α · wear 627"><span class="pill b">&alpha;</span> 627</td>`.
Ids and marker ids are document-global: prefix per SVG (`lat-`, `gre-`, `you-`).

### 4 Image-right - content left (~55-66%), one humanizing photo right
People in it, *"not always a white dude"*; source order: the deck's own 2025
photo bank → Tim's drop folder → Unsplash (§6 rule) → SVG cartoon. Built on
deck 32's "What is Factorial Design?" grid:
```html
<section class="slide s-topbar">
  <header class="topbar">Factorial Design</header>
  <div class="content"><div class="subhead">What is Factorial Design?</div>
    <div class="cols--21 cols middle">
      <div><ul class="tight"><li>select a fixed number of levels of each factor</li></ul></div>
      <div><img data-photo src="../images/slides/<deck-dir>/photo_<slug>.jpg" alt="what is actually in it">
        <div class="caption">Photo: &lt;name&gt; on Unsplash</div></div>
    </div></div>
</section>
```
No photo yet: leave `<!-- PHOTO SLOT: <what Tim should drop in> -->` in that column.

### 5 Animation / Visualizer / Playground - one per slide, full frame
Never two side by side; the frame wide enough to use the controls. From deck 32:
```html
<section class="slide s-topbar">
  <header class="topbar">Animation: factorial design</header>
  <div class="content">
    <iframe class="embed embed--full" title="Factorial design animation" loading="lazy"
      src="../labs/slide-factorial.html?view=anim&amp;topic=factorial&amp;v=20261020c"></iframe>
  </div>
</section>
```
Same slide again with `?view=viz`; the two playground slides (`lang=r`,
`lang=py`) stay as SLIDES.md §3 describes.

### 6 Dataset / tools - two cards, links only, no paragraphs
From deck 33 (Team Boards deep link per dataset):
```html
<section class="slide s-topbar s-cards" data-activity="explain-it-factorial-experiments">
  <header class="topbar">Activity: Explain It (Factorial Experiments)</header>
  <div class="content"><div class="cards cards--2">
    <div class="card" style="align-items:flex-start;text-align:left"><div class="name">Pick one dataset</div>
      <div class="role">Plant Growth (2&times;2) &middot; <a href="https://connect.systems-apps.com/sysen5300-board/#/?problem=factorial-plants">Team Boards</a> &middot; <a href="https://github.com/timothyfraser/sysen/blob/main/workshops/plants.csv">CSV</a></div></div>
    <div class="card" style="align-items:flex-start;text-align:left"><div class="name">Your tools</div>
      <div class="role"><a href="https://github.com/timothyfraser/sysen/blob/main/functions/functions_factorial.R">functions_factorial.R</a> / <a href="https://github.com/timothyfraser/sysen/blob/main/functions/functions_factorial.py">.py</a></div></div>
  </div></div>
</section>
```

### 7 Table - HTML from a CSV, tints that mean something
Label columns centred or left, numeric columns `.num`, every table its own
`.caption` with `data · code` links; `tbl--fit` before any split. From deck 32:
```html
<table class="tbl tbl--fit">
  <thead><tr><th></th><th>Unblocked arrangement</th><th>Blocked<br>arrangement</th></tr></thead>
  <tbody>
    <tr><th>Comparing 2 entities</th><td class="t-lav">T-test</td><td class="t-b">Randomized blocking</td></tr>
    <tr><th>Comparing k entities</th><td class="t-b">ANOVA</td><td class="t-o"><mark class="hl o">Factorial design</mark></td></tr>
  </tbody>
</table>
<div class="caption">... <a href="https://github.com/timothyfraser/sysen/blob/main/workshops/anova_youden.csv">data</a> &middot; <a href="https://github.com/timothyfraser/sysen/blob/main/functions/slides_w12_latin.R">code</a></div>
```
Formulas beside a table: `.fcards > .fcard.fcard--tight`.

### 8 Section divider - with the 2025 photo as a cutout
From deck 32 (p6):
```html
<section class="slide s-section">
  <h1>Factorial Design and Enumeration</h1>
  <hr class="rule">
  <div class="sub">Lesson 9</div>
  <img class="cutout" data-photo style="max-width:44%;max-height:50%;bottom:140px;border-radius:12px"
       src="../images/slides/lesson-13/06_factory.jpg" alt="A Lego production line with minifigure workers">
</section>
```

Agenda with an aside: deck 32's merged "Today's lesson" (`s-agenda`, `.side`
split into a `.bubble` + the corgi photo with an in-flow `.caption`) is the
model for two housekeeping slides that should be one.

## 2. Spacing and margins

- Nothing starts under the footer band (the on-slide ‹ › buttons were removed 2026-10-20; navigation is keys, taps, swipe and mouse drag).
- Stacked blocks (two tables, table + text) 24-28 px apart: `style="margin-top:28px"` on the second.
- Captions in flow under their figure (`.caption` with `position:static`), never bottom-pinned onto the footer.
- A wide header before a ~400 px column gets `<br>`, a two-line header, not a giant column.
- One idea per slide; visible `p`/`li` >= 26 px (verify `c2`).
- Fit levers before splits: `.side--fig`, `.tbl--fit`, `.fcard--tight`, `.cols`.

## 3. Code

| Rule | Detail |
|---|---|
| R first, R default | R `<pre>` before Python in every `.lang-pair`; the pill is the toggle, do not fight `localStorage` |
| Every chunk a pair | `.lang-pair` with `data-lang="r"` / `"py"`; Python follows that topic's Python chapter idiom |
| Comments kept | Tim's comments and blank lines from the 2025 source come back (`<span class="cm">`) |
| <= 12 lines visible | ~62 chars wide inside `s-example`; wrap long `c(...)` at 8 values |
| `=` never `<-` | house style; `%>%` pipe; `library()` one package at a time |
| Output in `.ocard` | inside the pair, inside `.answer` on Example slides, `b.k` marks the key statistic |

## 4. Numbering

- Title = slot + teaching week: **Lesson / Workshop / Recitation N**, lettered
  (8A / 8B) when one slot carries two decks. The deck-by-deck mapping is in
  the course plan.
- Change `<title>`, `data-deck-title`, title-slide `h1`, section `.sub` lines,
  agenda/bridge link text, activity kickers. **File names never change** (links,
  ratchet and registry are keyed on them).

## 5. Replication

| Thing | Comes from |
|---|---|
| Chart | `functions/slides_<deck>_<topic>.R` + `.py`, image `docs-v3/images/slides/<deck-dir>/gen_*.png`, caption `data · code`; palettes in `functions/README-slides.md` |
| Table | `workshops/*.csv`, every derived number recomputed by the script |
| Formula | `.fcards` (never an image) |
| Diagram | inline SVG from a generator script: `functions/slides_factorial_cubes.py`, `functions/slides_latin_squares.py` (stdlib, tips per cell) |
| Screenshot | becomes one of the above; the original goes to the Appendix with `data-appendix-reason` |

## 6. Humour and humanity

- **The funny image is content.** Reuse every photo the 2025 deck carried, at
  full size (`data-photo`), from `docs-v3/images/slides/<deck-dir>/`.
- Captions may joke: *"Figured you wouldn't mind me reusing this image again."*
- People in photos, and *"not always a white dude."*
- SVG cartoons are allowed: a generator `functions/slides_<deck>_art.py`,
  rendered and looked at like any image.
- One `<!-- PHOTO SLOT -->` per deck when nothing fits yet; Tim drops
  `photo_*.jpg` into the deck's image folder.
- **Unsplash is allowed, with Tim's rule, verbatim:**

  > "whenever you get a new image from unsplash, you MUST actually view it with
  > playwright - I've been burned by agents before who say they got a picture of
  > a dog and it turns out to be something totally unrelated, like a pencil."

  So: fetch candidates (`tools/fetch_image.py`) into the
  scratchpad, open **every** candidate in Playwright (or the Read tool), write
  one line per image saying what is actually in it, then copy the chosen one.
  An image never reaches a deck unseen. Caption **"Photo: <name> on Unsplash"**;
  list it in `docs-v3/images/CREDITS.md`.

## 7. The two blind spots

1. **Green gates are not fidelity or design.** Decks 42/32/33 passed
   `deck_audit` and `verify_slides` before Tim's phone review found eleven
   material problems. Contact sheets side by side + a screenshot of every
   changed slide, looked at (SLIDES.md §7 rule 10).
2. **Load probes must defeat `navigator.webdriver`.** The playgrounds skip
   their boot under automation, so a naive probe measures a deck that never
   boots (2026-10-20: Lesson 9 booted 3 webR + 4 Pyodide in a real browser).
   Launch with `--disable-blink-features=AutomationControlled` and
   `navigator.webdriver=false`; iframes get their address only near their
   slide (`data-sg-src`).

## 8. The unit prompt

The per-deck unit prompt lives in the course plan; paste it from there. A deck
unit's report shape: BEFORE/AFTER gate lines -> the map (or design map: one row
per slide, archetype -> verdict) -> slides changed, one line each -> not done
and why -> options for Tim. Every new image (Unsplash or SVG) is opened and
described in the report before it is placed.
