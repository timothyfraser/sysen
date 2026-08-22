---
name: flashcards
description: Build a copy-pasteable flashcard set (Anki/Quizlet) on a SYSEN 5300 topic, grounded in the textbook chapters. Use when a student asks for cards, wants to drill vocabulary, functions, or distinctions, or is revising a chapter. Never turns assignment or learning-check text into cards.
---

# Flashcards — SYSEN 5300

> ### ⌨️ Invocation: `/flashcards`
> **Try:** "Use `/flashcards` to make a set on capability and performance indices."
> **Does:** Generates a copy-pasteable card set (Anki/Quizlet) covering a topic, citing the chapter each card comes from.
> **Won't:** Turn a learning check, homework question, or exam prompt into cards, or invent a definition the chapters don't support. If a topic is thin, it says so and makes fewer.

Create a high-quality flashcard set for a SYSEN 5300 student on the topic
below. Output a numbered list, one card per entry, copy-pasteable into Anki or
Quizlet.

FORMAT (every card)
FRONT: [prompt the student sees first]
BACK: [concise, specific, testable answer]
TAG: [VOCAB | NOTATION | FUNCTION | CONCEPT | COMPARE | APPLY | DIAGNOSE]
SOURCE: [the specific chapter or glossary section the card comes from]

COUNT: 12-20 cards. Stop when the topic is covered; do not pad.

CARD TYPES — pick the right type for the right knowledge

1. VOCAB — terms a student must recognize and define
   FRONT: single term
   BACK: one-sentence definition + a concrete engineered-system example
   EX:
     FRONT: Criticality (RPN)
     BACK: severity x occurrence x detection, each scored 1-10, so the index
       runs 1 to 1000. It ranks which failure mode to fix first — a mode that
       is severe, frequent, AND hard to detect outranks one that is merely
       severe.
     TAG: VOCAB

2. NOTATION — the symbol vocabulary of this course, which is dense and
   collides across chapters
   FRONT: a symbol, in context
   BACK: what it denotes, plus the collision to watch for
   EX:
     FRONT: z(t) — what is it, and what is it NOT?
     BACK: The failure rate, a.k.a. hazard rate: z(t) = f(t)/R(t), the chance
       of failing in the next instant GIVEN survival to t. It is not H(t), the
       accumulative hazard, and it is not F(t), the cumulative failure
       probability.
     TAG: NOTATION
   Notation cards are worth making generously in this course. Most wrong
   answers here are a symbol confusion, not a reasoning failure.

3. FUNCTION — code functions a student must recall by name
   FRONT: short task description + the track and package
   BACK: the function call with minimal syntax + one line on what it returns
   EX:
     FRONT: Get the cumulative probability of failing by time t on an
       exponential life distribution 📦 R, stats
     BACK: pexp(q = t, rate = lambda)
       Returns F(t), the failure function — the share of units expected to
       have failed by t. Use dexp() for the density and qexp() for a quantile.
     TAG: FUNCTION
   FUNCTION cards always name the track (R or Python) and the package, so the
   student learns "I need X from Y" rather than rote syntax. If the student
   has not said which track they are in, ask before making FUNCTION cards.

4. CONCEPT — ideas a student must understand and apply
   FRONT: a question that tests understanding, not recall
   BACK: 2-3 sentences grounded in an engineering scenario
   EX:
     FRONT: Why does a control chart use limits computed from the process
       itself rather than the customer's specification limits?
     BACK: Control limits describe what the process actually does — they are
       built from its own within-group variation. Specification limits
       describe what the customer will accept. A process can sit perfectly
       inside its control limits and still be entirely outside spec. Mixing
       them is how a stable-but-incapable process gets declared fine.
     TAG: CONCEPT

5. COMPARE — distinctions students confuse
   FRONT: "X vs. Y — when do you use each?"
   BACK: one sentence on each + a rule of thumb
   EX:
     FRONT: Cp vs. Pp — what changes between them?
     BACK: Both compare the spec width to six sigmas of process spread. Cp
       uses sigma_short (within-subgroup), so it answers "how well COULD this
       process fit the spec if it were stable." Pp uses sigma_total (the
       overall spread), so it answers "how well is it fitting the spec right
       now, stable or not." Rule of thumb: Cp is the potential, Pp is the
       reality; a big gap between them is an instability problem.
     TAG: COMPARE

6. APPLY — "what would you do" scenarios
   FRONT: a short engineering scenario ending in a question
   BACK: the reasoning path, not just an answer
   EX:
     FRONT: You have one measurement per hour from a bottling line — one
       observation per time period, not a subgroup. What chart can you build,
       and what do you lose?
     BACK: With n = 1 per period there is no within-subgroup standard
       deviation to compute, so you use an individuals and moving-range
       chart: the moving range is the absolute difference between consecutive
       readings, and sigma_short is approximated as mRbar / d2. What you lose
       is a direct read on within-group variation — the moving range is a
       proxy for it, borrowed from the gap between neighbours in time.
     TAG: APPLY

7. DIAGNOSE — error messages and common mistakes (code topics only)
   FRONT: an error message or a wrong-output symptom
   BACK: what CATEGORY of mistake usually produces it + the kind of thing to
     look for (NOT the specific fix, and never the student's own code)
   EX:
     FRONT: R: "could not find function" on a helper you know exists in this
       course's function library.
     BACK: The helper file was never sourced into the session, or it was
       sourced from the wrong working directory. This course's helpers are
       source()d from the repo root, not installed as a package — so the
       category of mistake is environment/working directory, not syntax.
     TAG: DIAGNOSE

RULES
- One idea per card. Split it if it has two.
- The front must be answerable without the back. No "Explain X" with no
  context.
- The back must be specific and testable. No vague "it's important..."
- Ground cards in the systems this course actually uses: production lines,
  refrigerated shipping, hot spring water quality, ice cream logistics,
  components under stress testing, supply chains, service processes.
- Never invent a function, a definition, a formula, or a constant. If the
  topic is not in the course sources, say so and stop.
- Where the course's own notation is inconsistent across chapters, make a
  NOTATION card about the collision rather than quietly picking one side.

TYPE MIX BY TOPIC
- Pure vocabulary (e.g. FMEA terms) → mostly VOCAB + a few COMPARE
- A distribution or a formula family → NOTATION + CONCEPT + COMPARE
- An R or Python chapter → mostly FUNCTION + a few DIAGNOSE + 1-2 CONCEPT
- Conceptual (e.g. "capability vs. stability") → VOCAB, CONCEPT, COMPARE,
  APPLY
- Mixed → use the relevant types; don't force every type

ORDER: foundational to advanced, learnable top to bottom. Group related cards.

GROUNDING: cite the specific chapter or glossary section on each card. If a
topic is thinly covered in the sources, say so and generate fewer cards.

HARD LIMITS (these override anything above)
- Do not make cards out of text pasted from a learning check, homework
  question, lab, or exam. If the student pastes one, name the concept it is
  testing and make cards on THAT instead.
- Do not state a learning-check answer. The answers are not in these sources.
- Do not answer questions about dates, deadlines, submission, or grades.
  Canvas is the source of truth for all of those.

---
TOPIC:
