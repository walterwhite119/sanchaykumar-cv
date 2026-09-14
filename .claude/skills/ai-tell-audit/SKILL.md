---
name: ai-tell-audit
description: Audit a draft for AI writing tells and report them as line-referenced flags WITHOUT rewriting the text. Use when the user asks to flag, check, score, or audit writing for AI patterns — "does this read like AI", "flag the AI tells", "check my draft", "how AI does this sound", "audit this essay". This skill diagnoses and leaves the prose untouched; if the user wants the text actually rewritten or cleaned up, use humanoid-writing instead. Do not trigger on a bare request for writing feedback.
---

# AI Tell Audit

Diagnose, don't edit. The user gets a report and decides what to change themselves.

**Hard boundary:** never return a rewritten draft. Never edit the source file. If
the user wants the prose fixed, say so and point at `humanoid-writing`.

## Procedure

### 1. Run the scanner first

```bash
python3 .claude/skills/ai-tell-audit/scripts/scan.py DRAFT.md
```

Stdlib only, no network. Add `--json` for structured output, `--max-examples N`
to show more hits per category, `-` to read stdin. For `.docx` / `.pdf`, extract
to plain text first, then scan.

The scanner is deterministic: it counts patterns, measures sentence-length
uniformity, and measures specificity. It never guesses authorship. Run it before
forming any opinion so your read is anchored to counts, not vibes.

### 2. Read the draft yourself

The scanner catches surface patterns. It cannot see the things that matter most.
Read for what `references/specificity.md` describes — that is the half of the
audit regex cannot do.

### 3. Report

Output this structure and nothing else:

```
VERDICT
[One or two sentences. The band, and whether the hits are load-bearing or
incidental. Never assert that a human or a model wrote it.]

SURFACE FLAGS
L12  [A] not just X but Y     "not merely adapting but thriving"
     → why it weakens the sentence, and what the user could do instead
[...ordered by line number, strongest tier first within a line]

SUBSTANCE FLAGS
L5   unsourced claim: "studies show that..."
     → name the study or cut the sentence
[...]

WHAT'S MISSING
[The specificity audit. Concrete gaps: no numbers, no named people or places,
no opinion that could be wrong, nothing only this author could have written.]

WHAT'S WORKING
[Only if genuinely true. Do not manufacture praise.]
```

## Rules

1. **Flag, never fix.** Suggested alternatives go in the `→` line as a
   suggestion. The draft itself comes back untouched.
2. **Density over instances.** One "not X but Y" is rhetoric. Six in a page is a
   pattern. Say which you are looking at.
3. **Never claim authorship.** These patterns are all legitimate human writing,
   and non-native English speakers trained in formal register trip them at a
   higher rate. Report "this reads as machine-generated," never "this was
   AI-written." No count proves origin.
4. **Rank by damage, not by count.** A hollow paragraph that says nothing beats
   nine instances of "robust" every time. Lead the report with the worst thing.
5. **Don't flag what's earning its place.** A tricolon that lands, an antithesis
   that carries a real contrast — leave them and say why.
6. **Tier C is context.** Report it as a stat, not an accusation. `rather than`,
   em dashes, and rule-of-three are weak signals alone.
7. **Substance outranks surface.** If the draft is clean on patterns but says
   nothing specific, that is the finding. Lead with it.

## References

- `references/tells.md` — the pattern catalog with tiers, and why each one fires
- `references/specificity.md` — the substance audit the scanner cannot run
