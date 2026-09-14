# The specificity audit

The surface scan is the easy half. This is the half that matters.

Text can pass every pattern check and still read as machine-made, because the
real tell is not phrasing — it is **the absence of anything only this author
could have written.**

Run this by reading. No regex detects it.

---

## The six probes

### 1. Numbers
Are there any? Real ones — 4.7 cm, eleven years, 132 counts, October 2019 — not
"significant improvements" or "several years". A page of argument with zero
figures is either abstract by necessity or empty by default. Decide which.

*Scanner proxy:* `numerals_per_1k`. Below 4 is worth a look.

### 2. Named things
People, places, products, dates, titles. Generic actors ("organizations",
"teams", "users", "experts") are the default voice of text with no specific
referent behind it. Every generic actor is a question: which ones?

*Scanner proxy:* `proper_nouns_per_1k`. Below 10 is worth a look.

### 3. Falsifiable claims
Find one sentence that could be wrong. If every claim is hedged into safety
("can be", "may contribute to", "often plays a role"), the draft has no position
and cannot be argued with. That is not caution — it is absence.

### 4. Something that cost the author something
An admission, a failure, a changed mind, a number that came out badly, an
opinion that would annoy someone. Text that risks nothing reads as machine-made
even when every sentence is grammatical, because the balanced view is the
default output of a system optimized not to offend.

### 5. Sourcing
"Studies show", "research suggests", "experts agree", "it is widely recognized"
— every one is a claim with the citation removed. Flag each. Do not invent the
source, and do not guess at it.

### 6. Shape
Does every section run the same length? Every paragraph three-to-five sentences?
Every list three items? Real thinking is lumpy: the part the author cared about
runs long, the part they didn't gets a sentence. Mechanical evenness means the
structure came from a template, not from the argument.

---

## How to report it

Not "add more detail" — that is useless advice. Name the exact sentence and the
exact missing thing:

> L14 "Organizations report significant improvements"
> → which organizations, improvement in what, by how much? As written this
>   sentence is compatible with any result and asserts nothing.

---

## The order of operations

If the draft is **clean on patterns but empty on specificity**, lead the report
with that. A user who fixes forty surface flags and ships text that still says
nothing got worse advice than no advice.

If the draft is **heavy on patterns and rich on specificity**, say so plainly.
That is usually a human who writes in a formal register, or a draft where a
model helped with phrasing over real content. Neither is a problem to solve by
deleting em dashes.
