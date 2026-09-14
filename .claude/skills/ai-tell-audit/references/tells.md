# Pattern catalog

Tiers describe **evidential strength**, not severity. A tier-A hit is one that
rarely appears in unedited human prose at this density. It is still not proof.

---

## Tier A — strong

### The negation-antithesis family

The single most overproduced LLM construction. Manufactures a contrast so a flat
statement feels like an insight.

| Form | Example |
|---|---|
| not just/only X but Y | "not merely adapting but thriving" |
| It's not X, it's Y | "It's not about surveillance, it's about trust" |
| X isn't about Y | "Leadership isn't about authority" |
| not that X but that Y | "not that the canon was complete but that it was a start" |
| Less X, more Y | "Less process, more shipping" |
| No X. No Y. Just Z. | "No meetings. No standups. Just work." |

**Why it fires:** the contrast is usually fake. The "not X" half is a straw
position nobody held, so deleting it loses nothing. Test: cut the negative half.
If the sentence still says the same thing, the antithesis was decoration.

**When to leave it:** when X is a position someone actually holds and the
sentence is correcting it. "Not partly right — right" earns its place because
the writer is retracting their own hedge.

### Rhetorical machinery

- **Question-as-pivot** — "The result? A more flexible workforce." Fires because
  it fakes suspense over a claim that needed none.
- **Faux-punchy pivot** — "Here's the thing:", "The truth is:", "Let that sink in"
- **Trailing participial clause** — "...report improvements, underscoring the
  value of investing in infrastructure." The clause adds no information; it
  gestures at significance. Almost always cuttable with zero loss.
- **Whether you're X or Y** — audience-flattering universalizer.

### Dead phrases

Phrases that consume words without adding meaning: "it is important to note",
"in today's fast-paced world", "plays a vital role", "stands as a testament to",
"at the forefront of", "sheds light on", "paving the way for", "in the realm of",
"let's dive in", "it goes without saying", "ultimately, it depends on your needs".

Test: delete it. If the sentence survives, it was dead.

### Chatbot debris

"As an AI language model", "I hope this helps", "Certainly!", "Great question",
"Here is a revised version", "[Insert citation here]", "In this article, we will".
Not a tell — a leak. Always a finding, never a judgment call.

---

## Tier B — moderate

- **Filler transitions** — Moreover, Furthermore, Additionally, Notably,
  Importantly, Consequently. Human writers use these; models use them to open
  every third paragraph. Count the rate, not the presence.
- **LLM-favored vocabulary** — delve, tapestry, cornerstone, testament,
  leverage, robust, comprehensive, holistic, seamless, transformative,
  unprecedented, intricate, elevate, streamline, embark, resonate, bolster,
  garner, myriad, plethora, underscore, showcase, foster, harness, empower,
  unlock, cutting-edge, ever-evolving, fast-paced, game-changer.
- **Em-dash antithesis** — "Not partly right — right." Common in good human
  writing; only meaningful in a cluster.
- **Stacked hedges** — "may potentially suggest that it is possible".

**Vocabulary caveat:** this list is a moving target. "Delve" was a 2023–24 tell.
Models shift with each release, and a checklist written against last year's
model catches last year's model. Treat vocabulary as supporting evidence only.

---

## Tier C — weak, report as stats only

- `rather than` — ordinary English
- Rule of three ("clear, concise, and compelling") — ordinary rhetoric
- Em-dash density — ordinary punctuation
- Uniform sentence length — real signal, but confounded by genre; technical
  and academic writing is legitimately uniform

Never lead a report with tier C. Never call a tier-C hit a tell on its own.

---

## Calibration

Weighted density per 1000 words (A=2, B=1, C=0.4):

| Band | Density | Reading |
|---|---|---|
| clean | < 8 | nothing above baseline |
| light | 8–20 | a few hits; normal for edited prose |
| moderate | 20–45 | noticeable clustering |
| heavy | ≥ 45 | well above human baseline |

Measured against the test corpus: heavily-patterned marketing prose scored 187;
a personal essay using antithesis deliberately scored 13.8; concrete lab notes
scored 0.0. Under 300 words the density is noisy — read the hits, not the band.

---

## What this catalog cannot do

1. **Prove authorship.** Every pattern here is legitimate human writing. The
   density is the signal and the density is probabilistic.
2. **Avoid punishing non-native speakers.** Writers trained in formal English
   instruction produce this balanced, signposted register naturally. This is the
   largest false-positive source and the reason rule 3 in SKILL.md exists.
3. **Stay current.** See the vocabulary caveat.
4. **See the real problem.** Scrubbing every pattern here yields laundered AI
   text, not human text. That is what `specificity.md` is for.
