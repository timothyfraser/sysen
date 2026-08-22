---
name: glossary
description: The reference glossary of SYSEN 5300 terminology — reliability, probability, life distributions, SPC, capability, fault trees, acceleration models, regression, DOE, factorial design, and RSM — with the course's own definitions, its notation collisions, and the conflations students most often make. Use whenever a course term, symbol, or index needs defining, contrasting, or checking, so that what you say matches the textbook.
---

# Quality and Reliability Engineering Reference — SYSEN 5300

> ### ⌨️ Invocation: `/glossary`
> **Try:** "Use `/glossary` to explain why capability and stability are not the same thing."
> **Does:** Defines a term, contrasts two concepts you're confusing, and flags the mistake people usually make around them — grounded in the course's own wording.
> **Won't:** Do your analysis or answer a graded question. It sharpens the vocabulary; you do the thinking.

A reference glossary for **Systems Engineering and Six Sigma for the Design and
Operation of Reliable Systems** (Cornell). It defines the vocabulary used
across the textbook and flags the conceptual mistakes that vocabulary invites.
It is written for students and for the tools students use — a coding agent, a
study bot — so that everything speaks the same language as the chapters.

Use it as a **dictionary**, not a textbook. When an unfamiliar term shows up in
a chapter or a lecture, look it up here. When you are about to recommend a
method on your project, scan the mistakes list in section 13.

**Two things this glossary tries hard to do.** First, where a chapter defines a
term, the definition here agrees with that chapter rather than with the wider
literature. Second, where the textbook's own notation collides with itself —
and it does, in several load-bearing places — this glossary says so out loud
instead of quietly picking a side. Section 12 is nothing but those collisions,
and it is the section most likely to save you on an exam.

**A note on both tracks.** Every core idea here exists in R and in Python, and
both are fully supported. Concepts are written track-neutrally; where the two
languages genuinely differ in *vocabulary* rather than syntax, there is a
**Dual-track note**. Those notes are the places where a habit from one track
will actively mislead you in the other.

---

## Table of Contents

1. [Distributions and Descriptive Statistics](#1-distributions-and-descriptive-statistics)
2. [Probability and Probability Functions](#2-probability-and-probability-functions)
3. [FMEA and Block Diagrams](#3-fmea-and-block-diagrams)
4. [System Reliability](#4-system-reliability)
5. [The Failure-Rate Family of Functions](#5-the-failure-rate-family-of-functions)
6. [Life Distributions](#6-life-distributions)
7. [Fault Tree Analysis](#7-fault-tree-analysis)
8. [Physical Acceleration Models](#8-physical-acceleration-models)
9. [Statistical Process Control](#9-statistical-process-control)
10. [Process Capability and Performance](#10-process-capability-and-performance)
11. [Estimation, Fitting, and Uncertainty](#11-estimation-fitting-and-uncertainty)
12. [Comparing Groups: Experiments, ANOVA, and Regression](#12-comparing-groups-experiments-anova-and-regression)
13. [Factorial Design and Response Surface Methodology](#13-factorial-design-and-response-surface-methodology)
14. [Notation Collisions to Watch](#14-notation-collisions-to-watch)
15. [Common Terminology Mistakes](#15-common-terminology-mistakes)

---

## 1. Distributions and Descriptive Statistics

The atomic vocabulary. Everything downstream is built on it, and a loose grip
here shows up three chapters later as a misread index.

- **Distribution** — a vector's values stacked in order from lowest to highest
  to show the frequency of values. Any numeric vector can be expressed as one.
- **Histogram** — bars counting how many values fall in each bin. A *density
  plot* draws the same information as a smooth curve rather than blocks.
- **Density function** — the curve approximating a distribution. See §2 for
  what its height actually means.
- **The four traits of a distribution** — the course's organising frame:
  **size** (how many values), **location** (where it clumps), **spread** (how
  much values vary), and **shape** (e.g. bell curve). Nearly every descriptive
  statistic in the course is measuring one of these four.
- **Statistic** — "a single number that summarizes something about a sample."
  No magic. Statistics is the business of making them so we can make decisions
  under uncertainty.
- **Parameter vs. statistic** — a parameter describes a full **population**; a
  statistic describes a **sample**. The course notes that beyond this the terms
  are used largely interchangeably, but the distinction matters the moment you
  start estimating (§11).
- **Sample size (*n*)** — how many values you have. Size.
- **Mean, median, mode** — location. The mean is the balance point, the median
  the 50th percentile, the mode the most common value. The *relationship*
  between mean and median is a shape diagnostic: mean above median means
  right-skewed.
- **Percentile / quantile** — the value below which a given share of the
  distribution falls. The course's advice is worth internalising: with a
  quantile function you no longer need to remember min, max, range, or median
  — they are the 0th, 100th, and 50th percentiles.
- **Interquartile range (IQR)** — the 25th to 75th percentile span.
- **Standard deviation (σ)** — how much values vary from the mean *on average*.
  Spread.
- **Variance (σ²)** — the standard deviation squared. Accentuates large
  deviations.
- **Coefficient of variation (CV)** — the standard deviation as a share of the
  mean. Makes spread comparable across things measured in different units or
  at different scales.
- **Standard error (SE)** — the sample-size-adjusted standard deviation,
  σ/√n. It exists so that two samples of different sizes can be compared
  meaningfully. Later chapters use it constantly, and it always means the same
  thing: **the standard deviation of a sampling distribution** (§11).
- **Skewness** — shape: is the distribution leaning left or right?
- **Kurtosis** — shape: how heavy are the tails relative to a normal
  distribution?

**Dual-track note.** R's `sd()` and `var()` divide by *n − 1* by default;
NumPy's `np.std()` and `np.var()` divide by *n* unless you pass `ddof=1`. This
is not a style difference — it silently changes every standard error, control
limit, and capability index you compute downstream. The course's Python
chapters use pandas `.std()`, which does use *n − 1*, matching R. If you drop
to raw NumPy, set `ddof=1`.

---

## 2. Probability and Probability Functions

- **Probability** — "how often a specify event is expected to occur, given a
  sufficient number of times." (The typo is the chapter's; the definition is
  the one to use.)
- **Conditional probability** — the probability of two events happening
  together is the probability of the first, times the probability of the
  second *given that the first has already occurred*: P(AB) = P(A) × P(B|A).
  **If two events are interdependent, you multiply.**
- **Mutually exclusive** — two events that cannot both happen at once. **If
  two events are mutually exclusive, you add.** This add-versus-multiply pair
  is the whole of the course's probability arithmetic, and it reappears
  verbatim as the AND/OR rules of fault trees (§7) and the series/parallel
  rules of system reliability (§4).
- **Total probability** — for an event A mutually exclusive from each E_i:
  P(A) = Σ P(A|E_i) × P(E_i). Sum over every pathway.
- **Bayes' rule** — the probability of an outcome given a condition, expressed
  in terms of quantities you can actually measure:
  P(Outcome|Condition) = P(Outcome & Condition) / P(Condition).
  Its value is that it works when you have percentages rather than complete
  data.
  - **Prior** — the probability the outcome occurs, independent of anything
    else.
  - **Likelihood** — the probability the condition occurs, *given* the
    outcome. (Note: this is a different sense of "likelihood" from the one in
    §11. See §14.)
  - **Evidence** — the total probability that the condition does or does not
    occur. The denominator.
  - **Posterior** — the probability the outcome occurs *given* the condition.
    The thing you wanted.

### Probability functions

The course's framing: probability lets you measure, for any statistic, **how
extreme** it is. To do that you need something to compare against — either an
assumed hypothetical distribution, or a probability function built from the
observed data.

- **Probability density function (PDF)**, written *f(t)* or *d(t)* — "the
  function describing the probability (relative frequency) of any value in a
  distribution." For a vector *x*, it is a **curve** giving the probability
  (*y*) of each value across the range of *x*.
- **Cumulative distribution function (CDF)**, written *F(t)* — "the function
  describing the *cumulative* probability of each successive value in a
  distribution. Spans from 0 to 1." Answers *at most* questions.
- **Quantile function** — the inverse of the CDF: give it a percentile, it
  returns the raw value. Answers *what value sits at* questions.
- **Random generation** — draws a simulated sample from the distribution.
- **p-value** — the probability that a value **more extreme** than your
  statistic occurred.

**Hypothetical vs. observed probability functions.** A *hypothetical*
probability function assumes the population follows a known archetype (normal,
Poisson, gamma, exponential, Weibull) and computes from its formula. An
*observed* probability function is estimated from the data you actually have —
in this course by estimating a density and then turning that estimate into a
callable function, so you can ask about values you never observed. Both are
legitimate; they answer the same question from opposite directions.

**Dual-track note — the single most common cross-track error in this course.**
R names these four by prefix: `d` = density, `p` = cumulative, `q` = quantile,
`r` = random — `dexp`, `pexp`, `qexp`, `rexp`, and likewise `dnorm/pnorm/…`,
`dweibull/…`, `dgamma/…`. Python's SciPy names them by method on a
distribution object: `.pdf()`, `.cdf()`, `.ppf()` (percent-point function =
the quantile function), `.rvs()`. So R's `q` and SciPy's `ppf` are the same
thing, and R's `p` and SciPy's `cdf` are the same thing — but a reader who
maps `p` to `.pdf()` by the initial letter gets density where they wanted
cumulative probability, and the numbers look plausible enough to go unnoticed.

**Second dual-track trap: rate versus scale.** R's exponential and gamma
functions take a `rate` (λ). SciPy takes a `scale`, which is **1/λ**. The
course's Python chapters write this out explicitly — `expon.cdf(t,
scale=1/lambda)`, `gamma.cdf(t, a=k, scale=1/lambda)`. Pass λ where SciPy
wants a scale and you have silently inverted your failure rate. Similarly, R's
Weibull takes `shape` and `scale`; SciPy's `weibull_min` takes `c` for the
shape and `scale` for the scale — so the letter *c*, which means
**characteristic life** everywhere in this course's prose (§6), means
**shape** in the SciPy call signature.

---

## 3. FMEA and Block Diagrams

- **Failure Modes and Effects Analysis (FMEA)** — a structured walk through
  every way a system could fail, scoring each so you can rank what to fix
  first. Also a Six Sigma tool, and one of the method families available for a
  project.
- **Scope and resolution** — the deliberate choice of *which* failures you are
  analysing and at what grain. Set before scoring, not after.
- **Failure mode** — one specific way the system can fail.
- **Effect** — what that failure does downstream.
- **Severity** — how bad the effect is, scored 1 (none) to 10
  (hazardous/catastrophic).
- **Occurrence** — how often it happens, scored 1 (almost impossible) to 10
  (almost certain).
- **Detection** — how likely you are to catch it, scored 1 (almost certain to
  detect) to 10 (almost impossible to detect). **The scale runs backwards
  relative to intuition**: a high detection score is bad news, because it
  means the failure is hard to see coming.
- **Criticality**, a.k.a. **RPN (risk priority number)** — severity ×
  occurrence × detection, defined as "the *overall risk of each combination of
  severity and underlying conditions*." Runs 1 to 1000, because each input
  runs 1 to 10.
- Why the multiplication matters: a failure that is severe *and* frequent
  *and* invisible outranks one that is merely severe. The index is designed to
  surface exactly that combination.
- **Block diagram** — "shows how a series of components are connected in a
  social, physical, or technological system. Together, they visualize a
  *network*, where the blocks/components are *nodes* with lines, sometimes
  called *edges*, connecting them." Also just called a **flowchart**. FMEA
  leans on them heavily, and they are the visual ancestor of both the
  reliability block diagram (§4) and the fault tree (§7).
- **Subgraph** — a box drawn around a set of nodes in a diagram, to group them.

**A framing worth keeping.** The course's worked FMEA is deliberately
people-centric, "because it's important to remember that *people* are part of
our technological systems." An FMEA that only lists component failures has
usually missed the likeliest ones.

---

## 4. System Reliability

The question: **how likely is the system as a whole to survive, or fail, over
time?** The answer is always the probability arithmetic of §2 applied to a
structure.

- **Reliability analysis**, also called **survival analysis** — analysis where
  "our quantity of interest is the amount of time it takes to reach a
  particular outcome (eg. time to failure, time to death, time to market
  saturation)."
- **Lifetime distribution** — "the probability density function telling us how
  *frequently* each potential lifespan is expected to occur."
- **Component / node** — one element of the system. The course uses the
  network word *node* interchangeably.
- **Unlabelled node** — a node that is "just a junction for relationships," so
  it carries no probability of its own. Do not multiply one in.

### Series systems

"In a **series system**, we have a set of *n* components (sometimes called
*nodes* in a network), which get utilized *sequentially*. A domino train, for
example, is a series system. **It only takes 1 component to fail to stop the
entire system.** The overall reliability of a series system is defined as the
success of *every individual component* (A **AND** B **AND** C)."

R_S = Π R_i = R₁ × R₂ × … × R_n

Because every term is a probability below 1, **adding a component to a series
system always makes the system less reliable.** A series system is only as
good as its weakest link, and slightly worse than that.

### Parallel systems

"In a **parallel system** (a.k.a. *redundant* system), we have a set of *n*
components, but **only 1 component needs to function** in order for the system
to function… the success of *any individual component* (A **OR** B OR [A AND
B])." The course's image is a silverware drawer: you need one spoon, but you
keep several.

R_P = 1 − Π (1 − R_i) = 1 − Π F_i

Read that as: the system fails only if *everything* fails, so compute the
probability that they all fail and take the complement. **Adding a component
to a parallel system always makes the system more reliable.**

### Combined systems

"Most systems actually involve combining the probabilities of several
subsystems… we calculate the probabilities of each subsystem, then calculate
the overall probability of the final system. **The key is identifying exactly
which system is nested in which system.**"

The two named shapes are a **series system with a nested parallel system** and
a **parallel system with nested series systems**. They are not interchangeable
and they give very different answers from the same component reliabilities.
Draw the structure before you write the arithmetic — a structure error cannot
be recovered by careful algebra.

### Two rules used throughout

- **Multiplication rule** — the probability that *n* identical units each with
  reliability R(t) all survive past *t* is **R(t)ⁿ**.
- **Complement rule** — the probability that **at least one** of *n* units
  fails by time *t* is **1 − R(t)ⁿ**. (The chapter heading spells it
  "Compliment"; it means complement.)

### Renewal

- **Renewal** — the lag between a unit failing and being replaced.
- **Renewal rate** — "the mean number of failures per unit at time *t*."
  Obtained by combining failure and replacement probabilities with Bayes' rule
  (§2). **Careful:** the course writes the renewal rate as *r(t)*, the same
  symbol it uses elsewhere for the reliability function. See §14.

**Not covered in this course, despite being standard elsewhere:** *k*-out-of-*n*
systems, availability, and maintainability. If you find yourself needing
"availability," you are reaching outside the course's own toolkit — say so
rather than implying the textbook covers it.

---

## 5. The Failure-Rate Family of Functions

This is the most notation-dense material in the course, and the section
students most often get turned around in. All six functions describe the *same*
lifetime distribution from different angles, and each is derivable from the
others.

| Function | The course's name | Formula | Also equals | What it means |
|---|---|---|---|---|
| **F(t)** | Failure Function | 1 − e^(−λt) | 1 − e^(−H(t)) | CDF of lifespans: share failed **by** *t* |
| **R(t)** | Reliability Distribution | e^(−λt) | e^(−H(t)) | The remainder: share surviving **past** *t* |
| **f(t)** | Change in Failure Function | [F(t+Δt) − F(t)] / Δt | −R′(t) | The PDF: failures per unit time at *t* |
| **z(t)** | Failure Rate (Hazard Rate) | f(t) / R(t) | λ = 1/m | Chance of failing next instant **given survival to *t*** |
| **H(t)** | Accumulative Hazard Rate | −log(R(t)) | λt | Total risk accumulated from 0 to *t* |
| **AFR(t₁,t₂)** | Average Failure Rate | [H(t₂) − H(t₁)] / (t₂ − t₁) | — | Average failures per timestep between two times |

The relationships to hold onto:

- **R(t) = 1 − F(t).** Always, for every distribution. This is the one
  identity that never has an exception.
- **z(t) = f(t) / R(t).** The hazard rate is a *conditional* quantity — it is
  divided by the survivors. This is precisely what makes it different from
  f(t), and why "failure rate" and "probability of failure" are not synonyms.
- **H(t) = −log(R(t))**, and therefore **R(t) = e^(−H(t))**. The accumulative
  hazard is just the reliability function on a log scale.
- **The instantaneous hazard rate can rise or fall over time; the accumulative
  hazard only increases or stays constant.** It is a running total; totals do
  not go down.

Further terms in this family:

- **Mean time to fail (*m*, MTTF)** — "the mean of a lifespan distribution."
  For an exponential distribution, **λ = 1/m**, so the failure rate and the
  mean life are reciprocals. MTTF also equals the integral of the reliability
  function: ∫₀^∞ R(t) dt. That identity generalises to distributions where
  λ = 1/m does not.
- **Median time to fail (T₅₀)** — the value splitting the area under the
  density in half. For an exponential, T₅₀ = log(2)/λ ≈ 0.693/λ.
- **Modal time to fail** — the most common time to fail, the peak of the PDF.
  For an exponential this is *t = 0*, and the density only declines from
  there — which is worth pausing on, because it means the single most likely
  moment of failure for a memoryless part is immediately.
- **Conditional reliability (survival) function, R(x|t)** — the probability a
  unit survives an *additional x* given it has already reached age *t*:
  R(x|t) = R(x+t) / R(t).
- **Mean residual life (MRL, μ(t))** — "the average number of years the
  product is expected to survive *after* time *t*." For the exponential it is
  **constant** and equals the MTTF at every *t*; for a wear-out Weibull it
  shrinks as *t* grows.
- **AFR approximation** — when the probability at time *t* is below 0.10,
  AFR ≈ F(t)/T. Handy, and only valid in that small-probability regime.

### Units

Failure rates get very small very quickly, so the course rescales them:

- **Percent per thousand hours (%/K)** = 10⁵ × z(t)
- **Failure in Time (FIT) per thousand hours**, also called *parts per million
  per thousand hours*, **PPM/K** = 10⁹ × z(t), which equals 10⁴ × the rate in
  %/K.

These are units, not new quantities. A FIT figure is a hazard rate wearing
different clothes.

---

## 6. Life Distributions

- **Life distribution** — "the distribution of a vector of *n* products, whose
  values recording the amount of time it took for each product to fail. In
  other words, its **lifespan**."

### Exponential

- **The defining property:** "the failure rate λ remains **constant**… The
  probability that a product fails in the next hour of use is the same at
  t = 0, t = 100, or t = infinity. It doesn't worsen with time."
- **Lack of memory / memorylessness** — the name for that property. A part
  that has survived to *t* is, on average, **as good as new**. The course
  glosses it as the literal meaning of "if it is not broke, don't fix it."
- Parameter: **λ**, the rate. λ = 1/MTTF.
- **The 63.2% fact:** in an exponential distribution, the MTTF *always* sits
  at a cumulative probability of 1 − 1/e = 0.632. So the "mean" life is the
  point by which about 63% have already failed — not half. Half is T₅₀, and
  it is *earlier*.

**When it is the wrong model.** Anything that wears out, fatigues, corrodes,
or has infant-mortality defects violates memorylessness. Fitting an
exponential to it will not error; it will just quietly assume the thing never
ages.

### Weibull

The flexible one. "The exponential is a special case of Weibull distribution
where the failure rate λ is held constant such that *m* = 1. But in a usual
Weibull distribution, the failure rate can change over time. This makes it
very flexible, able to take on the shape of an exponential, gamma, or normal
distribution depending on the parameters."

- **Shape parameter *m*** — the parameter that decides the *behaviour* of the
  failure rate, quoted from the chapter:
  - ***m* = 1** → an exponential; constant failure rate.
  - ***m* = 2** → a **Rayleigh** distribution; the failure rate increases
    linearly.
  - ***m* < 1** → "the failure rate z(t) *decreases* over time, like the
    left-end (**infant-mortality**) of a bath-tub curve."
  - ***m* > 1** → "the failure rate z(t) *increases* over time, like the
    right-end (**wear-out**) of a bath-tub curve."
  - This single parameter is the course's whole story about how a thing ages.
    Reading it correctly is worth more than any other single skill in this
    chapter.
- **Characteristic life *c*** — "the time at which 63.2% of units will
  consistently have failed." It is the Weibull's scale parameter, and it
  replaces λ in the failure function: c = 1/λ.
- **Cumulative hazard:** H(t) = (λt)^m. If *m* = 1 this collapses to λt, the
  exponential case.
- **Failure function:** F(t) = 1 − e^(−(t/c)^m).
- **Failure rate:** z(t) = (m/c) × (t/c)^(m−1).
- **Solving for a missing parameter:** if any three of F(t), *m*, *t*, *c* are
  known, the fourth follows.
- **Weibull series systems** — in a series system of independent components,
  each Weibull with the *same* shape *m*, the system is also Weibull, with
  c_series = (Σ 1/c_i^m)^(−1/m).
- **Bath-tub curve** — the three-phase picture of a product's life: a
  decreasing infant-mortality phase, a flat useful-life phase, and an
  increasing wear-out phase. Note that the course *invokes* this curve as the
  intuition for the shape parameter but never formally defines it as its own
  object; the middle "useful life" phase is the exponential/memoryless regime.

### Gamma

- "The Gamma distribution is well suited to modeling products exposed to a
  **series of shocks** over time at a given rate over time."
- Parameters: **k** (shape — the number of shocks) and **λ** (the rate at which
  shocks arrive).
- **Gamma function Γ** — used to count "the total ways a series of shocks could
  have occurred"; Γ(k) = (k − 1)!.
- **Failure rate behaviour:** "Unlike the exponential, the gamma failure rate
  is *not* constant. What stays constant is the rate λ at which shocks
  *arrive*. For k > 1, the failure rate z(t) starts near zero and rises over
  time toward λ." The shape *k* controls how fast it climbs.
- MTTF = k/λ; Variance = k/λ².

### Lognormal

- "The log-normal distribution can be very useful, often in modeling
  semi-conductors, among other product."
- Parameterised in this course by **T₅₀** (the median) and **σ** — and the
  chapter is emphatic that "σ is really more of a **shape parameter** here
  than the standard deviation as we usually think of it."
- **Φ** — the CDF of the normal distribution. The lognormal CDF is written
  through it: F(t) = Φ( log(t/T₅₀) / σ ).
- **z-score** — a value expressed as a number of standard deviations from the
  mean; what Φ takes as its argument.
- **Inverse-Φ (Φ⁻¹)** — the normal quantile function.
- MTTF = T₅₀ × e^(σ²/2).

**A real trap the chapter flags.** Built-in lognormal functions in both
languages are parameterised by **meanlog** and **sdlog**, which are *not* T₅₀
and σ as this course uses them (meanlog is the log of the median). For Six
Sigma work the course deliberately writes its own lognormal functions in terms
of T₅₀ and σ. If you call a library lognormal directly with the course's
parameters, you will get a wrong answer that looks reasonable.

### Censoring

- **No censoring / complete sample** — every unit failed; you observed every
  lifespan.
- **Type I censoring**, a.k.a. **time-censored** — "experiment stops when time
  *t* reaches *limit*." You ran out of clock.
- **Type II censoring**, a.k.a. **failure-censored** — "experiment stops when
  the number of units failed reaches *limit*." You ran out of patience at a
  fixed failure count.
- Why it matters: the units that had **not** failed when you stopped still
  carry information — they tell you the lifespan exceeded the cutoff. Throwing
  them away biases every estimate downward. Both the λ estimator and the
  likelihood function (§11) have explicit terms for them.
- Note the course's vocabulary: it says *Type I / Type II / time-censored /
  failure-censored*. It does **not** use the phrase "right-censored," which is
  the standard term elsewhere.

---

## 7. Fault Tree Analysis

- **Fault tree** — "visual representation of boolean probability equations,
  typically depicting the sets of necessary events leading to system failure."
  Every fault tree can be written as a function: an equation for the
  probability of the top event.
- **Top event** — the big prominent failure you are modelling; the root of the
  tree. "A nuclear disaster, a missile launch," a widespread outbreak.
- **Intermediate event** — an event partway up the tree, produced by the
  events below it and feeding the events above it.
- **AND gate** — every sub-event must occur. **Multiply** the probabilities.
- **OR gate** — any sub-event suffices.
- **Boolean logic / boolean equation** — the algebra of ANDs and ORs that turns
  the picture into a number.
- **Edgelist and nodelist** — the course records a tree using network-science
  conventions: a **nodelist** of events (each with a unique `name`, an `event`
  label, and a `type` of `and`, `or`, `not`, or `top`) and an **edgelist** of
  `from`/`to` connections. The type `not` means **not a gate** — i.e. a leaf
  event — not logical negation. This trips people up.
  - The same event can appear in several places in one tree. When it does, it
    gets **different node names but the same event name**, so the graph stays
    well-formed while the logic stays honest.
- **Cutsets** — "all the possible sets of events which together trigger
  failure."
- **Minimal cutsets** — "the most reduced set of events which trigger
  failure." These are what you act on: the minimal cutsets name the smallest
  combinations that can take the system down, so they are your shortlist for
  redundancy or inspection.
- **MOCUS** — the top-down algorithm the course uses to derive cutsets. "It's
  pretty quick for small graphs, but gets exponentially longer the more nodes
  you add. (Especially with OR statements.) That's MOCUS's value as well as
  its tradeoff."
- **Coverage** — "the percentage of cutsets containing your minimal cutset out
  of all total cutsets leading to failure… basically a measure of the
  explanatory power of your cutsets."
- **Failure rates in a tree** — if you know each basic event's failure rate,
  you can evaluate the whole tree at any time *t* by feeding each event's F(t)
  into the boolean equation.
- **Simulating uncertainty** — the inputs to a fault tree are estimates. The
  course simulates variation in them (binomial draws for probabilities, normal
  draws for rates) and reads confidence intervals off the resulting
  distribution of top-event probabilities. This is often more informative than
  the point estimate, because it shows which input the answer is hostage to.

> **⚠ An inconsistency in the chapter, stated plainly.** The OR rule is
> presented two different ways. In some worked examples the OR gate is a
> **simple sum** of the branch probabilities; in the reusable `top_event()`
> function it is **1 − Π(1 − p)**, the complement form. These agree only when
> the probabilities are tiny. The complement form is the generally correct one
> — it is the parallel-system rule from §4 — and simple addition can exceed
> 1.0, which is your tell that something is wrong. If you are asked to
> reproduce a specific worked number, match the form that example used; if you
> are computing something real, use the complement form and say why.

**Vocabulary note.** The course says **"cutsets"** and **"minimal cutsets"**,
one word. It does *not* use the term "basic event" — its events are just
events, sub-events, or intermediate events.

---

## 8. Physical Acceleration Models

The problem: lab conditions are harsher than the field, so a life distribution
measured under stress is "always slightly *off* from the real, use-case life
distribution by a *specific factor*." These models convert one into the other.

- **Stress conditions (subscript *s*) vs. usage conditions (subscript *u*)** —
  lab versus field. Every quantity in this section carries one subscript or
  the other, and mixing them up inverts the answer.
- **Acceleration factor (AF, or A)** — the factor by which stress testing
  "accelerates the failure." Defined by f_u(t) = f_s(t) × AF, and computed as
  the ratio of the two densities.
- **The three conversion identities:**
  - F_u(t) = F_s(t/AF)
  - f_u(t) = f_s(t/AF) / AF
  - z_u(t) = z_s(t/AF) / AF
  — all following from the premise **t_u = t_s × AF**.
- **AF is generally not constant over time.** This is the thing to remember.
  "So, when we pick an AF, we're usually picking the AF corresponding to a
  specific parameter, like the characteristic life or median of a
  distribution."
- **Linear acceleration** — the working assumption that AF is a constant,
  linear relationship between f_u and f_s. It "requires us to choose a
  constant value of AF from *just 1 time-step*," so you pick a representative
  one — typically AF = T₅₀u / T₅₀s, or the equivalent ratio at the MTTF or the
  characteristic life. Naming *which* point you pinned it to is part of
  reporting the number honestly.

### The models

- **Arrhenius model (temperature)** — "a simple equation that models the impact
  of temperature on the log of lifespan." Fitted as a regression of log(c) on
  a **temperature factor**.
  - **Temperature factor (TF)** — a standardised unit, TF = 1/(k · T_Kelvin),
    where *k* is **Boltzmann's constant** (1/11605) and T_Kelvin = °C + 273.15.
  - **ΔH, the activation energy** — the model's *slope*: "the rate at which a
    temperature factor increase of 1 unit affects log(c)."
  - **A** — the model's intercept, exponentiated: A = e^(intercept).
- **Eyring model (multiple stressors)** — "derived from chemical reaction
  theory and quantum mechanics, which supposes that we can predict lifespan
  parameters pretty well if we know temperature *and* any other stresses, such
  as voltage." Fitted as a **multivariate** regression: instead of a line of
  best fit through two vectors, a *plane* through three.
- **Degradation model (time trends)** — for performance that decays with
  exposure rather than failing outright: Q_t = Q₀ × e^(−R(S)t), fitted as
  log(Y_t) = α + βX·t. Here β = −R, the degradation effect of the stressor.
  An **interaction term** enters when the degradation rate itself depends on
  another condition (e.g. how much voltage was applied).
- **Burn-in period** — deliberately running products for some hours before
  sale, so that "the defective products fail early on" and what remains is
  less likely to fail. It is infant mortality (§6, *m* < 1) exploited on
  purpose. Acceleration factors are what let you work out an ideal burn-in
  length, since a burn-in at stress conditions of t_b hours corresponds to
  a × t_b hours of normal use.
  - Post-burn-in failure is a **conditional probability**: you divide by the
    probability of having survived the burn-in.
- **Parsimony** — the course's stated rule of thumb: "seek to build the most
  *parsimonious* (simplest) model that explains the most variation."

**Not in this course:** the inverse power law, temperature-humidity models, and
the phrase "accelerated life testing" itself. The course's acceleration
toolkit is Arrhenius, Eyring, degradation, plus AF and burn-in.

---

## 9. Statistical Process Control

- **Statistical process control (SPC)** — "using statistics to (1) measure
  variation in product quality over time and (2) identify benchmarks to know
  when intervention is needed."
- **Process** — the thing producing output over time. In SPC you are always
  watching a process, not a static sample.
- **Subgroup** — a slice of the process, usually a time period, within which
  you have several measurements.
- **Subgroup size (n_w)** — how many observations per subgroup. It drives
  everything: which chart you can build, which constants you need, and how
  tight the limits are.

### The two families of statistics

The distinction the whole chapter rests on:

- **Within-group statistics** "measure quantities of interest within each
  subgroup." Also called **short-term** statistics. This is variation the
  process produces just by being itself.
- **Between-group statistics** "measure *total* quantities of interest for the
  overall process (eg. the overall *grand* mean, overall standard deviation)."

Named quantities:

- **x̄ (xbar)** — the within-group mean, one per subgroup.
- **x̄̄ (xbbar)** — the **grand mean**, the mean of the subgroup means.
- **r** — the within-group **range** (max − min). **Note: in SPC, *r* means
  range, not reliability.** See §14.
- **R̄ (rbar)** — the average range.
- **σ_short (sigma_s)** — the short-term variation parameter, computed as the
  square root of the mean of the within-group variances: √(mean(sd²)). The
  course's own explanation of *why*: "we're weakening the impact of any
  special cause variation so that our sigma is mostly representative of common
  cause (within-group) variation."
- **σ_total (sigma_t)** — the overall standard deviation of the raw data,
  ignoring subgroups.

**σ_short vs. σ_total is the load-bearing distinction of this entire unit.**
σ_short says how much the process wobbles *within* a subgroup. σ_total says
how much it wobbles overall, which includes any drift *between* subgroups. A
process that is drifting has σ_total > σ_short, and the gap between them is
the drift. Every index in §10 is one of these two divided into a spec width.

### Causes of variation

- **Common cause variation** — the ordinary, inherent variation the process
  produces all the time. It is what σ_short is built to capture.
- **Special cause variation** — variation from an assignable, external source:
  a new operator, a worn tool, a bad batch. It is what a control chart is
  built to detect.
- Note: the course uses both terms but never formally defines either in a
  standalone definition — they are introduced in the course of explaining why
  σ_short is computed the way it is. The distinction is still the point of the
  entire chapter, and a process described as **unstable** is one that "varies
  not just due to common causes."

### Control charts

- **Control limits** — bounds computed **from the process itself**, at ±3
  standard errors from the centre line. The course calls the pair "6-sigma
  control limits" because the band spans six standard errors end to end.
- **Centre line** — the grand mean (or R̄, or s̄, depending on the chart).

Charts the course actually covers:

- **Average (X̄) and standard deviation (S) chart** — the recommended pair.
  Quoted: "The preferred method for measuring within-group variability is the
  standard deviation, rather than the range, so we generally recommend (a)
  Average and Standard Deviation charts over (b) Average and Range charts."
- **Average (X̄) and range (R) chart** — the older pair, built with the D₃ and
  D₄ constants. Covered, but not recommended.
- **Individuals and moving range chart** — what you use when there is only one
  observation per period. "There's no way to calculate standard deviation for
  that — after all, there's no variation within each subgroup."
  - **Moving range (mR)** — the absolute difference between consecutive
    values. Absolute, because "ranges are always 0 to infinity."
  - **Average moving range (mR̄)** — the mean of those differences.
  - **The key approximation:** σ_short ≈ mR̄ / d₂.
  - **The lower control limit on a moving-range chart is always 0.** A range
    cannot be negative.

**Not covered in this course:** p, np, c, and u charts (attribute/count
charts); Western Electric or zone run rules; and the term "rational
subgrouping." The course also does not use the abbreviations UCL/LCL/CL — it
says "upper," "lower," and "control limits."

### The control-chart constants

These exist to recover σ_short when you cannot compute a standard deviation
directly — most often when the subgroup size is 1 and all you have is a moving
range.

- **d₂** — the *mean* of the range distribution for an archetypal normal
  distribution (mean 0, sd 1). Precisely: "in a distribution with a standard
  deviation of 1, the mean mR is d₂." That is what makes it a valid conversion
  factor from an observed average range into units of σ_short.
- **d₃** — the *standard deviation* of that same range distribution.
- **D₃, D₄** — multipliers giving the lower and upper control limits for the
  range: D₃ = 1 − 3(d₃/d₂), D₄ = 1 + 3(d₃/d₂). D₃ is bounded at 0.
- **C₄ (written `C4`; also `b2`)** — the mean standard deviation from an
  archetypal normal distribution.
- **B₃, B₄** — multipliers for the lower and upper 3-sigma limits on the
  standard deviation. B₃ is bounded at 0, since a standard deviation cannot be
  negative.
- **A₃** — a multiplier used in the standard-deviation chart's limits.

**Two things worth knowing about these constants in this course.** First, they
are obtained by **simulation**, not looked up in a table — the course
generates the archetypal distribution and measures it. Second, the course is
explicit that you often do not need them at all: "If you're working with full
data from your process, you can easily calculate σ_short right from the
empirical data, without ever needing to use d_x factors." They are a tool for
the data-poor case. (**A₂**, which appears in most other SPC texts, is not
introduced here.)

---

## 10. Process Capability and Performance

### The two questions

Quoted directly, because the phrasing is the definition:

- **Capability** — "does it meet required specifications?"
- **Stability** — "is production consistent and predictable?"

"A **capable** process delivers goods that can actually perform their
function, like a 20-foot ladder that is *actually* 20 feet. A **stable**
process delivers products with *consistent* and predictable traits (regardless
of whether those traits are *good*). We need to maximize **both**."

That parenthetical is the whole point. **A process can be perfectly stable and
completely incapable** — reliably making the wrong thing — and it can be
capable on average while being wildly unstable. They are independent axes, and
each has its own indices.

### Specification limits

"The specification limits are our **expected values** E_upper and E_lower, as
compared to our actual **observed values**, summarized by μ and σ." They come
from the customer, the market, or the regulator. They are **not** control
limits, which come from the process. Confusing the two is mistake #1 in §15.

### The four indices

| Index | Shape | Sided | Assumes | Formula | The question it answers |
|---|---|---|---|---|---|
| **C_p** | centered | 2-sided | stable | (E_up − E_low) / 6σ_short | How many times wider is the expected range than the observed range, **assuming it is stable**? |
| **C_pk** | uncentered | 1-sided | stable | \|E_limit − μ\| / 3σ_short | Same, for the left/right side, **assuming it is stable** |
| **P_p** | centered | 2-sided | not required | (E_up − E_low) / 6σ_total | How many times wider is the expected vs. observed range, **stable or not**? |
| **P_pk** | uncentered | 1-sided | not required | \|E_limit − μ\| / 3σ_total | Same, for the tail of interest, **stable or not** |

Reading the table as a system:

- **C vs. P is a σ choice.** The **capability** indices (C_p, C_pk) use
  **σ_short**, so they describe what the process *could* do if it were stable —
  its potential. The **process performance** indices (P_p, P_pk) use
  **σ_total**, so they describe what it *is* doing right now, drift included.
  A large gap between C_p and P_p is a diagnosis: the process has potential it
  is not realising because it is unstable.
- **The `k` suffix is a centering choice.** The plain indices (C_p, P_p)
  assume the distribution sits centred between the two limits and use the full
  spec width. The `k` indices are one-sided: they measure from the mean to
  **one** limit, and **always take the shorter tail** — the side you are
  closest to violating. So C_pk ≤ C_p always, and the two are equal only when
  the process is perfectly centred.
- **1.0 is the threshold.** At 1.0, the spec width exactly equals six sigmas
  of process spread. Below 1.0 the process does not fit inside its
  specification.
- **The identity:** P_p × C_pk = P_pk × C_p. Know any three and the fourth
  follows.

### Confidence intervals for the indices

An index is a statistic, so it has sampling error, and reporting one without an
interval overstates what you know. The course's pattern:

- **Degrees of freedom follow the σ.** Capability indices use
  v_short = k(n_w − 1); performance indices use v_total = n_w·k − 1, where *k*
  is the number of subgroups.
- **Centered (2-sided) indices** use the simple standard error
  estimate × √(1/(2v)).
- **Uncentered (1-sided) indices** add a term:
  estimate × √(1/(2v) + 1/(9n·estimate²)).
- Then the interval is estimate ± z·SE for a theoretical interval, or the
  2.5th and 97.5th percentiles of a bootstrap distribution.

**How to read one.** If the interval straddles 1.0, you cannot say the process
is capable — or that it isn't. If the whole interval sits below 1.0, you can
say with that confidence that the true index is below 1. That sentence is the
finding; the point estimate alone is not.

---

## 11. Estimation, Fitting, and Uncertainty

The machinery shared across the reliability and quality chapters.

### Sampling distributions

- **Sampling error** — "any statistic is really just 1 of the many possible
  values of statistics you could have gotten from your sample, had you taken
  just a slightly different random sample."
- **Sampling distribution** — "the latent distribution of 1000 statistics we
  could have gotten due to random sampling error." **Whenever you make a
  confidence interval, you are drawing from a sampling distribution.**
- **Null distribution** — the distribution of statistics you would get if the
  effect were *not* real. The course's clean split: **p-values describe null
  distributions; confidence intervals describe sampling distributions.** They
  are different objects answering different questions.
- **Standard error** — the standard deviation of a sampling distribution.
  (Same definition every time it appears in this course.)
- **Confidence interval** — the range you are some stated percent sure the
  true value lies in. A two-sided 95% interval "spans 95%, so it's got to
  start at 2.5% and end at 97.5%."

### Two ways to get an interval

- **Theoretical sampling distribution** — assume a shape (usually normal) and
  use a formula. "This is a big assumption."
- **Bootstrapped sampling distribution** — resample your own data *with
  replacement* many times, recompute the statistic each time, and read the
  percentiles off the resulting distribution. "Gaining accuracy at the expense
  of computational power." Works for *any* statistic, including all four
  capability indices.
- **Bootstrapped sample** — one such resample: "sometimes taking the same
  observation multiple times, sometimes leaving out some observations by
  chance."
- **Permutation test** — resampling **without** replacement, shuffling which
  group each observation belongs to. This "**breaks** any association between
  the outcome and our grouping variable, such that any statistic we get is
  purely due to chance" — which is exactly how you build a null distribution.

**Bootstrap vs. permutation, the distinction to hold.** Both resample, but for
opposite purposes. The **bootstrap** samples *with* replacement to approximate
the **sampling distribution** of your statistic → confidence intervals.
**Permutation** shuffles labels *without* replacement to approximate the
**null distribution** → p-values.

### Maximum likelihood estimation

- **MLE** — "a computational approach that will help us find the true (most
  likely) values for any parameter in any dataset. It's pretty robust if the
  number of failures is 'large' enough, where 'large' counts as > 10."
- **The three ingredients:** a sample; a **PDF**, which gives the probability
  of each observed value; and a **likelihood function**, which "tells us the
  probability of getting this EXACT sample, given the PDF values for each
  observed data point."
- **Likelihood** — the *product* of the densities of every observed point:
  LIK = Π f(t_i). Multiplication because it is a joint probability.
- **Log-likelihood** — the sum of the logged densities. Used for two reasons
  the course gives explicitly: the log of a tiny number is easier to read and
  compute, and the log of a product equals the sum of the logs.
- **The optimisation:** the best parameters are the ones that **maximise** the
  likelihood. Numerically, you search over candidate parameter values and keep
  the one with the greatest log-likelihood.
- **Censored likelihood** — with censoring, the likelihood is the product of
  the densities for the *r* units that failed, **times R(T_max)^(n−r)** for the
  *n − r* units that had not failed by the end. That second factor is how the
  survivors earn their keep. Drop it and you are pretending they failed at the
  cutoff.

**Dual-track note.** R maximises a log-likelihood by *flipping the sign scale*
on its minimiser (`optim(..., control = list(fnscale = -1))`); Python's
`scipy.optimize.minimize` has no such flag, so the Python chapters **return
the negative log-likelihood** and minimise that. Same idea, opposite sign
convention — and a sign error here does not crash, it just returns a confident
wrong parameter. Whichever track you are in, sanity-check the fitted parameter
against a crude estimate (for an exponential, 1/mean) before trusting it.

### Estimating a failure rate

- **λ̂ ("lambda-hat")** — the estimated failure rate. The hat marks it as an
  *estimate, subject to error*.
- **Complete sample:** λ̂ = (number of failures) / (total unit test hours).
- **With censoring:** λ̂ = r / (Σ t_i + (n − r)·t_z), where *r* is total
  failures, *n* is total units, Σt_i is total unit-hours among failures, and
  t_z is the last timestep recorded. The (n − r)t_z term is the survivors'
  contribution; with no censoring it is zero and the formula collapses to the
  simple one.
- **k factor** — the course's device for a confidence interval on λ̂: "we will
  **weight** λ̂ by a factor *k*, to get a slightly higher/slightly lower
  estimated failure rate that shows our confidence interval." It depends on
  (1) the total number of failures *r* and (2) the acceptable error α.
  - Under the hood it is a **chi-squared** quantile divided by 2r. The degrees
    of freedom depend on the censoring: **2r** for complete or Type II
    (failure-censored) data, **2(r + 1)** for time-censored data.
  - The course's own name for this is the *k* factor, not "the chi-squared
    interval," so use its word and mention the mechanism.
- **Planning an experiment** — solving the same relation for the unknown you
  need: minimum test time, or minimum sample size, to demonstrate a required
  failure rate. Note the course's warning: "Experiment planning by definition
  makes time-censored datasets," so use the df = 2(r + 1) form.

### Goodness of fit

- **Crosstabulation** — binning failures into equal time intervals and
  counting them, producing observed counts per bin (`r_obs`) alongside
  expected counts from a fitted model (`r_exp`).
- **Chi-squared (χ²)** — "the sum of ratios for each bin. Each ratio is the (1)
  squared difference between the observed and expected value over (2) the
  expected value. Ranges from 0 to infinity. The bigger (more positive) the
  statistic, the greater difference between the observed and expected data."
- **Degrees of freedom** — for this test, (number of bins − number of fitted
  parameters − 1). The course notes df "is the *mean* of the chi-squared
  distribution."
- **p-value** — "the probability of getting a value greater than or equal to
  (more extreme than) our observed chi-squared statistic."
- **Statistically significant** — "if our observed statistic is more extreme
  than most possible chi-squared statistics (eg. > 95% of the distribution),
  it's probably not due to chance."

**Note:** chi-squared is the *only* goodness-of-fit machinery this course
teaches for life distributions. QQ plots and probability plots — standard
elsewhere — do not appear.

---

## 12. Comparing Groups: Experiments, ANOVA, and Regression

### Experiments

- **Random assignment** — each unit is assigned to a condition by chance,
  holding everything else constant. It is what licenses a causal claim.
- **Control group** and **treatment group** — the baseline condition and the
  changed one.
- **Difference of means (d̄)** — the statistic: d̄ = x̄_treatment − x̄_control.
- **t-statistic** — "a standardized measure telling us *how extreme* is our
  statistic," computed as d̄ divided by its standard error. Its value is
  practical: it is cheap, where a permutation test needs thousands of
  resamples.
- **t distribution** — the null distribution the t-statistic is read against.
  Two-tailed, centred on 0, and **wider for small samples, narrower for large
  ones**, reflecting increasing precision as *n* grows.
- **Paired-sample (dependent) t-test** — when treatment and control have the
  same size and pair up observation by observation. Uses the standard
  deviation of the *differences*.
- **Unpaired-sample (independent) t-test** — when they don't. Uses each
  group's own standard deviation and size: σ = √(s₁²/n₁ + s₂²/n₂).
- **Equal vs. unequal variance** — an assumption you can make or refuse.
  Refusing costs you a much uglier degrees-of-freedom formula, which is why
  the course's remark is: with a computer, "it is no longer especially helpful
  to assume equal variances."

> **⚠ A practical trap the chapter flags emphatically.** When you hand a
> grouping variable to a t-test, **make it an ordered factor with the
> treatment group first**. Otherwise the software defaults to alphabetical
> order and silently computes control − treatment, flipping the sign of your
> effect.

### ANOVA

- **ANOVA (analysis of variance)** — tests differences in a numeric outcome
  between **three or more** groups. Practically, it "tries to ascertain how far
  apart three distributions are from each other."
- **Grand mean (x̄̄)** — the mean across all groups; the benchmark everything
  is measured against.
- **Total sum of squares (TSS)** — "the total variation in your data, using
  the grand mean as a benchmark."
- **Residual sum of squares (RSS)** — "how much deviation remains between your
  treatment group means and other values within each treatment group. This is
  the *unexplained error* in your model."
- **Explained sum of squares (ESS)** — "how much deviation *was explained* by
  your treatment group means." ESS = TSS − RSS.
- **Mean squares** — the sums of squares turned into averages so they are
  comparable: ESS/(k − 1) and RSS/(n − k), for *k* groups and *n* observations.
- **F-statistic** — "the ratio of the variation explained versus unexplained
  by your model." Ranges 0 to infinity. Small F: the model is barely better
  than a flat line at the intercept. Large F: it explains far more.
- **sigma / residual standard error** — the average prediction error. Falling
  sigma across models indicates better fit.

### Regression

- **Model** — "an equation approximating the relationship between two or more
  vectors of data. It's not the real thing — it's an approximation."
- **Line of best fit** — the line a regression draws through the data; the
  model *is* the equation of that line.
- **The model equation:** Y_observed = Alpha + X_observed × Beta + Error.
- **Alpha / intercept** — "the predicted value of the outcome if all
  predictors equal zero. Also called the Intercept, the point at which the
  line crosses the y-axis." The chapter's own caution: the intercept "might be
  nonsensical sometimes, like a negative price."
- **Beta / slope / coefficient** — "how much our outcome y increases by when
  our predictor x increases by 1."
- **Predicted value (Ŷ, `yhat`)** — what the model says for a given X. The
  course's prose word is **predicted values**, not "fitted values."
- **Residual / error** — "the difference between the observed outcome and the
  outcome predicted by the model." A regression finds the line that
  **minimises** these.
- **R-squared (R²)** — "the percentage of variation in the outcome that is
  explained by the model," ranging 0 to 1. Equivalently 1 − (RSS/TSS). The
  course's benchmarks: 1.00 perfect, 0.85 pretty great, 0.5 pretty good, 0.2
  not good but better than nothing, 0 nothing.
- **F-statistic (in regression)** — compares your model against the
  intercept-only baseline: does it explain more variation than a flat line?
- **Standard error (of a coefficient)** — the standard deviation of that
  coefficient's sampling distribution.
- **t-statistic (of a coefficient)** — "a standardized t-statistic measuring
  how extreme each estimate is, based on sample size and variance."
- **p-value** — "the probability that our alpha or beta coefficients were that
  large just due to chance."
- **Stars** — the shorthand: `***` p < 0.001, `**` p < 0.01, `*` p < 0.05, `.`
  p < 0.10.
- **Correlation (Pearson's r)** — the strength and direction of a relationship
  between two numeric variables, from −1 through 0 to +1. A pairwise
  description, with nothing controlled for.

### Multivariate regression

- **Outcome variable**, **explanatory variable**, **control variables** — the
  course's three labels for the roles in a model.
- **Controlling** — adding control variables to account for "alternative
  explanations for variation" in the outcome, which "**refines** our beta
  coefficient… getting us closer to the truth."
- **Plane / hyperplane of best fit** — with two predictors the model fits a
  *plane*; with more, a hyperplane. The line generalises.
- **Standardisation / z-scores** — rescaling variables so coefficients become
  comparable. "To compare the size of our beta coefficients, our variables
  must have the same units." A standardised beta reads: as the predictor
  increases by 1 **standard deviation**, the outcome changes by β **standard
  deviations**. Note: categorical variables are not rescaled and their
  coefficients cannot be compared to numeric ones this way.
- **Baseline (for a categorical predictor)** — the omitted category every
  other level is compared against. Every coefficient on a categorical variable
  is a difference *from the baseline*, and the intercept is the baseline's own
  value.
- **Log transformation** — used when the outcome is non-negative and
  right-skewed, as lifespans are. The course's reasoning in the acceleration
  chapter: "most useful life distributions involve exponential processes and
  lifespans are by nature non-negative, right-skewed variables. Taking
  log(outcome) adjusts for that and lets us plot a straight line of best fit."
- **Model-building strategy** — the course's recipe: start with the
  explanatory variable you care about plus the controls "without which the
  model isn't very valid," then add more controls to refine the estimate.
  Compare models on fit.

**Vocabulary note.** The course says "alternative explanations for variation";
it does not use the word **confounding**. It also uses **"direct effect"** and
**"one-way effect"** where most texts say "main effect."

---

## 13. Factorial Design and Response Surface Methodology

- **Factorial design** — an experiment that varies several factors at once, on
  purpose, so you can read off both individual effects and combined ones.
  "When you have a limited amount of time and/or resources, factorial-design
  experiments can be very cost-efficient." Structurally, each unit is randomly
  assigned a level of factor 1, then a level of factor 2, and so on, so every
  combination of conditions is represented.
- **Replicates** — the multiple observations made under each unique
  combination of treatment conditions. Without them you cannot separate an
  effect from noise.
- **Direct effect / one-way effect** — "how changing one factor affects the
  outcome… regardless of the other factors." The measured difference between
  the high level and the low level of a single factor.
- **Difference of grand means (d̄̄)** — the statistic for a direct effect: take
  the grand mean of the treatment groups, subtract the grand mean of the
  control groups. When a factor has three or more levels, one factor yields
  several d̄̄ statistics, not one.
  - Naming discipline the course insists on: **record the variable and the
    order of subtraction** (e.g. `b_a` = b − a). Half the confusion in
    factorial output is a forgotten sign convention.
- **Two-way interaction** — whether two factors "together affect the outcome
  differently than they do individually." Computed by comparing
  same-direction pairs (high-high + low-low) against opposite-direction pairs
  (high-low + low-high).
- **Three-way interaction** — whether a two-way interaction itself depends on a
  third factor. "A positive result means the interaction strengthens with the
  [third factor] change, and a negative result means it weakens."
- **Pooled variance / pooled standard error** — a single variance estimate
  applied across groups, weighted by each group's degrees of freedom. "In a
  factorial experiment, each combination of factors can vary a little due to
  random noise. This makes it hard to compare effects, so we want to use a
  pooled standard error that represents the average amount of noise across all
  groups before estimating treatment effects."
- **Reading an interaction plot** — plot the predicted outcome against one
  factor, with a separate line per level of the other. **Parallel lines mean
  no interaction; lines that cross or converge mean the effect of one factor
  depends on the other.**
- **Confidence vs. prediction intervals** — "confidence intervals are a little
  narrower, used in estimating effects you've already observed, while
  prediction intervals are a little wider, used for estimating predicted
  quantities that you naturally want a little more caution around."

### Response surface methodology

- **Response surface methodology (RSM)** — "using statistical models to predict
  an outcome (a.k.a. **response** variable) given a series of varying
  conditions. This lets us predict and visualize the **full range/surface** for
  that outcome."
- **Response variable** — the outcome being mapped.
- The three model forms the course builds, in order:
  - **First-order polynomial model:** Y = α + β₁X₁ + β₂X₂. Flat plane.
  - **Interaction model:** adds β₁₂X₁X₂. The plane can now twist.
  - **Second-order polynomial model with interaction:** adds β₁₁X₁² and
    β₂₂X₂². Now the surface can curve, which is what lets it find a peak or a
    valley rather than just a slope.
- **Contour plot** — the map of the fitted surface. "When we use *polynomial
  terms* in our model equation, we can map that plane almost perfectly to our
  observed data, creating more of a *contour* or *topographical* surface than
  a simple plane." Read it like a topographic map: closely spaced lines mean
  a steep response.
- **Study range** — the region you actually collected data in, distinct from
  the region the model will happily generate predictions for. Drawing the
  study range on your contour plot is how you keep yourself honest about
  extrapolation.
- **Canonical form** — "an abbreviation of your long model equation into a much
  more understandable, short form," Ŷ = Y_s + X₁² + X₂². It is not in the
  original units: it maps each raw value (lowercase x₁) to a standardised
  distance from the stationary point (uppercase X₁). Its use: "the canonical
  form of a model is like a shortcut for interpreting the shape of a contour
  plot."
- **Stationary point** — the point at which the canonical coordinates are
  zero; where the surface flattens out. Useful for identifying "key points
  after which increasing the amount of an ingredient will make no more
  difference."
- **Transforming variables** — log, logit, square, cube, roots. Worth knowing
  the course's honest framing: transformations often don't improve predictive
  accuracy but "might make our predictions more *realistic*" — e.g. logging an
  ingredient bounds it to positive values, because there is no such thing as
  negative ginger. "It's always a trade-off between predictive power and our
  ability to generate reasonable, useful quantities of interest."
- **Iterating** — RSM is sequential by design. You fit a surface, learn where
  to look, run more experiments there, and refit. New results that contradict
  your earlier predictions "are never a bad thing — because they get you
  closer to truth."

**Not in this course, despite being standard RSM vocabulary:** steepest
ascent, central composite design, "curvature" as a named diagnostic, coded
units (canonical form is the nearest equivalent), fractional factorial
designs, blocking, and center points. The course's own words are contour plot,
response surface, stationary point, canonical form, second-order polynomial.

---

## 14. Notation Collisions to Watch

The textbook reuses several letters for different quantities in different
chapters. These are not typos and they will not be fixed by reading more
carefully — you have to know they exist. This section is the highest-value
page in the glossary.

1. **`m` — mean time to fail vs. Weibull shape.** In the system reliability
   and failure-rate chapters, *m* is the **mean time to fail** (and λ = 1/m).
   In the Weibull material, *m* is the **shape parameter** that decides
   whether the failure rate rises or falls. Completely different quantities,
   one letter. Always check which chapter's context you are in.

2. **`c` — characteristic life vs. a shape argument.** In prose, *c* is the
   Weibull **characteristic life**, the time by which 63.2% have failed. In
   SciPy's `weibull_min`, the argument named `c` is the **shape**. Reading the
   course's Python code with the course's prose vocabulary in your head will
   invert the two.

3. **`r` / `R(t)` — range vs. reliability vs. renewal rate.** In SPC, `r` is
   the within-group **range** and `rbar` its average. In reliability, **R(t)**
   is the **reliability function**. And in the renewal material, *r(t)* is the
   **renewal rate** — the mean number of failures per unit at time *t*, which
   is close to the opposite of a survival probability.

4. **`f(t)` vs. `F(t)` — density vs. cumulative.** Lowercase *f(t)* is the
   **PDF**; uppercase *F(t)* is the **failure function / CDF**. The course's
   own prose occasionally calls a CDF "the failure function *f(t)*" in
   lowercase. When the text and the formula disagree, **trust the formula**: if
   it contains `1 − e^(−λt)` it is a CDF regardless of the letter in front of
   it.

5. **`z(t)` vs. `h(t)` vs. `H(t)` — hazard rate vs. cumulative hazard.** This
   course's standard symbol for the **instantaneous hazard rate** is **z(t)**.
   Most outside literature writes it *h(t)*, and the course does too in one
   place. Meanwhile **H(t)** (capital) is the **accumulative hazard**, a
   different quantity — a running total. And in the lognormal function set,
   the function *named* `h()` computes **H(t)**, the cumulative one. Rule of
   thumb: if it is a ratio f/R, it is the hazard rate; if it is −log(R), it is
   the cumulative hazard.

6. **`k` — three different things.** In the gamma distribution, *k* is the
   **shape** (the number of shocks). In failure-rate confidence intervals, the
   **k factor** is a chi-squared-derived multiplier. In SPC and ANOVA, *k* is
   the **number of subgroups or groups**. Also, Boltzmann's constant in the
   Arrhenius model is *k*.

7. **`σ` — standard deviation vs. lognormal shape vs. residual standard
   error.** Ordinarily σ is a standard deviation. In the **lognormal**, σ is
   explicitly "more of a shape parameter than the standard deviation as we
   usually think of it." In ANOVA and regression output, `sigma` means the
   **residual standard error**. And in SPC you must further distinguish
   **σ_short** from **σ_total**.

8. **`likelihood` — Bayes vs. MLE.** In **Bayes' rule**, the likelihood is
   P(condition | outcome), one term of a formula. In **maximum likelihood
   estimation**, the likelihood is the joint probability of your whole sample
   under a candidate parameter. Related ideas, different objects.

9. **`p` — the prefix vs. the p-value vs. a proportion.** In R, the `p`
   prefix means **cumulative probability** (`pexp`, `pnorm`). Elsewhere *p* is
   a **p-value**, and in regression *p* is the **number of parameters** in the
   F-statistic's degrees of freedom.

10. **`d` — density prefix vs. d̄ vs. d₂.** R's `d` prefix means **density**
    (`dexp`, `dnorm`). In experiments, **d̄** is the **difference of means**
    and **d̄̄** the difference of grand means. In SPC, **d₂** and **d₃** are
    control-chart constants derived from the range distribution.

---

## 15. Common Terminology Mistakes

The conflations that actually cost points. Watch for these in your own writing
before someone else does.

**1. Control limits are not specification limits.** Control limits come from
the **process** — ±3 standard errors computed from its own variation.
Specification limits come from the **customer, market, or regulator**. A
process can sit comfortably inside its control limits and be entirely outside
specification, which is the definition of a stable-but-incapable process. Every
control chart uses control limits; every capability index uses specification
limits. Never mix them into the same calculation.

**2. Capability is not stability.** Capability asks "does it meet required
specifications?" Stability asks "is production consistent and predictable?"
The course is explicit that a stable process may deliver consistent traits
"*regardless of whether those traits are good*." You need both, and each has
its own indices — capability indices for the first question, control charts
for the second.

**3. Common cause is not special cause.** Common cause variation is the
process's own ordinary noise; special cause variation comes from an
assignable, external source. σ_short is built specifically to capture the
former and downweight the latter. Saying "the process has high variation" is
not a finding — say *which kind*, because they have different remedies (redesign
the process versus find the assignable cause).

**4. σ_short is not σ_total.** σ_short is within-subgroup; σ_total is the
overall spread including drift between subgroups. Substituting one for the
other silently converts a capability index into a performance index (or vice
versa) and changes the meaning of your conclusion. If they differ a lot, that
gap *is* your instability finding — don't average it away.

**5. C_p, C_pk, P_p, and P_pk are four different claims.** C-versus-P is a σ
choice (short vs. total; potential vs. actual). The `k` suffix is a centering
choice (two-sided full width vs. one-sided shorter tail). Quoting "the
capability index" without saying which one is not a statement anyone can act
on.

**6. PDF, CDF, and quantile are three different questions.** The PDF gives the
relative frequency *at* a value. The CDF gives the cumulative probability *up
to* a value. The quantile function goes backwards: give it a percentile, it
returns the value. Getting these confused is the single most common
computational error in this course, and it is made much easier by R's `d`/`p`/`q`
prefixes not matching SciPy's `.pdf`/`.cdf`/`.ppf` names (§2).

**7. The failure rate is not the probability of failure.** z(t) = f(t)/R(t) is
**conditional on survival to t** — it is the chance of failing in the next
instant *given that you have made it this far*. F(t) is the unconditional
cumulative probability of having failed by *t*. A high hazard rate late in life
is entirely compatible with few units failing then, because few remain.

**8. The hazard rate is not the cumulative hazard.** z(t) can rise or fall over
time. H(t) is a running total, so it **only increases or stays constant**. If
your H(t) goes down, you have computed something else.

**9. MTTF is not the median, and it is not "the typical lifespan."** For an
exponential distribution the MTTF sits at the **63.2nd percentile**, not the
50th. The median is T₅₀ = log(2)/λ, and it is earlier. Meanwhile the *modal*
time to fail for an exponential is zero. Three perfectly good measures of
"typical," three different numbers.

**10. Memorylessness is a strong claim, not a default.** Choosing an
exponential distribution asserts that a component that has run for a year is as
good as new. For anything that wears out, that is false, and the model will not
warn you. If ageing matters, you want a Weibull and the shape parameter is the
whole point.

**11. Weibull shape *m* is not the mean time to fail *m*.** See §14 collision
#1. It is the same letter for the parameter that decides whether things get
*more* or *less* likely to fail over time — and for the average lifespan.

**12. Series and parallel are about logic, not layout.** Series means *every*
component must work (AND, multiply reliabilities); parallel means *any one*
suffices (OR, multiply the failure probabilities and take the complement).
Which one applies is a question about dependency, not about how the diagram is
drawn. Adding a component to a series system always makes it worse; adding one
in parallel always makes it better.

**13. A cutset is not a minimal cutset.** Cutsets are *all* the event
combinations that trigger the top event. Minimal cutsets are the *irreducible*
ones. The minimal cutsets are the actionable list; the full set is mostly
supersets of them.

**14. The OR-gate rule is not simple addition.** Adding branch probabilities
can exceed 1.0, which is your signal something is wrong. The general rule is
1 − Π(1 − p_i) — the same complement rule as a parallel system. Simple addition
is only a passable approximation when all the probabilities are very small.
(The chapter shows both; see the flag in §7.)

**15. The acceleration factor is not a constant of nature.** AF generally
varies over time. When you quote one number, you have pinned it to one
parameter — the median, the MTTF, the characteristic life. Say which. An AF
quoted without its anchor point is not reproducible.

**16. Stress conditions are not usage conditions.** Every quantity in the
acceleration chapter carries an *s* or *u* subscript for a reason. The whole
exercise is converting between them; losing track of which one you are in
inverts the answer.

**17. "Significant" is not "large," and it is not "important."** A p-value
tells you how extreme a statistic is relative to a null distribution. It says
nothing about the size of the effect or whether it matters to anyone. With a
big enough sample, a trivial effect is significant; with a small one, a large
effect may not be. Report the estimate and its interval, not just the stars.

**18. R-squared is not correctness.** R² is the share of variation explained.
A high R² on a model that omits the key control variable is a well-fitted
wrong answer, and a low R² can still contain a real, useful effect. It measures
fit, not validity.

**19. Correlation is not a controlled estimate.** Pearson's r describes two
variables with nothing held constant. A beta coefficient in a multivariate
model is an estimate *controlling for* the other variables in it. They answer
different questions and routinely have different signs.

**20. A direct effect is not an interaction.** A direct (one-way) effect is
what changing one factor does on average. An interaction is whether that
effect *depends on* another factor. "Machine B is better" and "Machine B is
better, but only with the oat milk" are different findings, and only the
second requires an interaction term. Parallel lines on an interaction plot mean
no interaction.

**21. Prediction inside the study range is not prediction outside it.** A
fitted response surface will cheerfully produce a value for ingredient
combinations you never tested. Draw the study range, and say when you are
extrapolating.

**22. Sampling error is not measurement error.** Sampling error is the
variation you get from having taken *this* sample rather than another one;
it shrinks as *n* grows and it is what confidence intervals describe.
Measurement error is your instrument being wrong; more data does not fix it.
A capability index computed on a broken gauge is precise and useless.

**23. Bootstrap and permutation are not interchangeable.** Bootstrap resamples
**with** replacement to approximate the **sampling distribution** → confidence
intervals. Permutation shuffles labels **without** replacement to approximate
the **null distribution** → p-values. Both are resampling; they answer
opposite questions.

**24. Censored data is not missing data.** A unit that had not failed when the
study stopped is not an absent observation — it is the information that its
lifespan exceeded the cutoff. Dropping it biases your failure rate upward.
Type I censoring means you ran out of time; Type II means you ran out of
failures.

**25. "Sigma" the metric is not "Six Sigma" the method.** σ is a standard
deviation — a number describing spread. **Six Sigma** is the improvement
methodology this course teaches: the DMAIC arc, FMEA, control charts,
capability analysis, designed experiments. And "six sigma" in "6-sigma control
limits" is a third thing again: the ±3-standard-error band that spans six
standard errors end to end. Three uses of one word in one course. Say which
you mean.

### Vocabulary precision

- **"Reliability" vs. "survival"** — the course treats reliability analysis and
  survival analysis as the same field with different disciplinary accents.
  R(t) is the reliability function; the *conditional* version R(x|t) is the one
  the course calls a survival function.
- **"Failure rate"** — ambiguous in this course, and worth pinning down every
  time. It usually means the **hazard rate z(t)**, but λ (a constant), F(t)
  (in some prose), and the AFR are all called "failure rate" somewhere in the
  chapters. Name the symbol.
- **"MTTF" vs. "MTBF"** — the course uses **mean time to fail (MTTF)**
  throughout. MTBF (mean time *between* failures, which presumes repair) does
  not appear. Don't import it.
- **"Characteristic life" vs. "MTTF"** — not synonyms. Characteristic life *c*
  is the 63.2nd percentile of a Weibull; MTTF is its mean, c·Γ(1 + 1/m). They
  coincide only when Γ(1 + 1/m) = 1.
- **"Criticality" vs. "severity"** — severity is one of the three inputs (how
  bad is the effect); criticality is the product of all three. A severe failure
  that never happens and is instantly detected has low criticality.
- **"Predicted values" vs. "fitted values"** — the course's prose word is
  **predicted values** (or `yhat`). Same object; use its word.
- **"Direct effect" / "one-way effect" vs. "main effect"** — the course says
  the first two. Most textbooks say "main effect." Same thing.
- **"Cutsets"** — one word, in this course's spelling.
- **"Alternative explanations"** — the course's phrase for what most texts call
  **confounding**.
- **"Stable" vs. "in control"** — the course says *stable* and describes points
  as "within range" or "comfortably within 3 standard deviations." It does not
  use the phrases "in control" and "out of control," and it does not teach the
  Western Electric run rules.
