#!/usr/bin/env python3
"""Deterministic scan for AI writing tells. Stdlib only, no network, no deps.

Counts pattern hits with line numbers, measures sentence-length uniformity, and
measures specificity (numerals, named entities, hollow quantifiers).

The scanner counts. It does not judge. Density is evidence, not a verdict.

Usage:
    python3 scan.py draft.md
    python3 scan.py draft.md --json
    python3 scan.py a.md b.md --max-examples 4
"""

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Pattern catalog.  tier: A = strong tell, B = moderate, C = weak/context-bound.
# Each entry: (category, label, tier, regex)
# ---------------------------------------------------------------------------

PATTERNS = [
    # --- Negation-antithesis: the "not X but Y" family -------------------
    ("antithesis", "not just/only X but Y", "A",
     r"\bnot\s+(?:just|only|merely|simply)\b[^.?!\n]{0,80}?\bbut\b"),
    ("antithesis", "it's not X, it's Y", "A",
     r"\b(?:it|this|that)(?:'s|’s| is)\s+not\b[^.?!\n]{0,80}[,;.—–-]\s*(?:it|this|that)(?:'s|’s| is)\b"),
    ("antithesis", "X isn't about Y", "A",
     r"\b(?:isn't|isn’t|is not|aren't|aren’t|are not)\s+about\b"),
    ("antithesis", "not X but Y (bare)", "A",
     r"\bnot\s+(?:a|an|the)?\s?\w+\s*[,—–-]\s*but\s+(?:a|an|the)?\s?\w+"),
    ("antithesis", "not that X but Y", "A",
     r"\bnot\s+that\b[^.?!\n]{0,90}?\bbut\b"),
    ("antithesis", "em-dash antithesis", "B",
     r"\b[Nn]ot\s+\w+(?:\s+\w+)?\s*[\u2014\u2013]\s*\w+"),
    ("antithesis", "Less X, more Y", "A",
     r"\b[Ll]ess\s+\w+,\s+more\s+\w+"),
    ("antithesis", "No X. No Y.", "A",
     r"\bNo\s+\w+\.\s+No\s+\w+\."),
    ("antithesis", "where others X, this Y", "B",
     r"\bwhere\s+(?:others|most|many|everyone)\b[^.?!\n]{0,60}\bthis\b"),
    ("antithesis", "rather than", "C",
     r"\brather than\b"),
    ("antithesis", "more than just", "B",
     r"\bmore than (?:just|simply|merely)\b"),

    # --- Rhetorical machinery -------------------------------------------
    ("rhetoric", "question-as-pivot", "A",
     r"\b(?:The result|The catch|The problem|The reason|The upshot|The kicker|The best part|The twist|Why|So what|The difference|Sound familiar)\?"),
    ("rhetoric", "faux-punchy pivot", "A",
     r"\b(?:Here'?s the thing|The truth is|Here'?s why|And that'?s the point|That'?s not hyperbole|Let that sink in|But here'?s the (?:catch|thing|kicker))\b"),
    ("rhetoric", "trailing participial clause", "A",
     r",\s+(?:reflecting|highlighting|demonstrating|underscoring|showcasing|illustrating|emphasi[sz]ing|cementing|ensuring|allowing|enabling|helping|providing|offering|creating|driving|fostering|solidifying|marking|signal(?:l)?ing|paving)\b[^.?!\n]{0,120}[.?!]"),
    ("rhetoric", "whether you're X or Y", "A",
     r"\bwhether you(?:'re| are)\b[^.?!\n]{0,60}\bor\b"),
    ("rhetoric", "anaphora filler", "B",
     r"\b(\w+) (?:matters|counts)\.\s+\1?\s*(?:It|They)\b"),
    ("rhetoric", "rule of three (single-word list)", "C",
     r"\b\w{3,12}, \w{3,12},? and \w{3,12}\b"),

    # --- Dead phrases ----------------------------------------------------
    ("dead_phrase", "it is important/worth noting", "A",
     r"\bit(?:'s| is)\s+(?:important|worth|crucial|essential|key)\s+(?:to\s+)?(?:not(?:e|ing)|remember(?:ing)?|understand(?:ing)?|mention(?:ing)?)\b"),
    ("dead_phrase", "in today's ... world", "A",
     r"\bin today'?s\b"),
    ("dead_phrase", "plays a vital/key/pivotal role", "A",
     r"\bplays?\s+an?\s+(?:vital|key|crucial|pivotal|significant|important|central)\s+role\b"),
    ("dead_phrase", "testament to", "A",
     r"\b(?:stands as a |a |is a )testament to\b"),
    ("dead_phrase", "at the forefront of", "A", r"\bat the forefront of\b"),
    ("dead_phrase", "sits at the intersection of", "A", r"\bsits at the intersection of\b"),
    ("dead_phrase", "sheds light on", "A", r"\bshed(?:s|ding)? light on\b"),
    ("dead_phrase", "paving the way", "A", r"\bpav(?:e|es|ing) the way\b"),
    ("dead_phrase", "serves as a reminder", "A", r"\bserves? as a reminder\b"),
    ("dead_phrase", "in the realm/world of", "A", r"\bin the (?:realm|world|landscape|sphere) of\b"),
    ("dead_phrase", "when it comes to", "B", r"\bwhen it comes to\b"),
    ("dead_phrase", "it goes without saying", "A", r"\bit goes without saying\b"),
    ("dead_phrase", "needless to say", "A", r"\bneedless to say\b"),
    ("dead_phrase", "that being said", "B", r"\bthat being said\b"),
    ("dead_phrase", "with that in mind", "B", r"\bwith that in mind\b"),
    ("dead_phrase", "at the end of the day", "B", r"\bat the end of the day\b"),
    ("dead_phrase", "let's dive in / explore", "A",
     r"\blet'?s (?:dive|delve|explore|unpack|take a (?:closer )?look|jump)\b"),
    ("dead_phrase", "summary closer", "B",
     r"(?:^|[.\n]\s*)(?:In conclusion|In summary|To sum up|Overall|Ultimately|In essence|All in all)\b"),
    ("dead_phrase", "depends on your needs", "A",
     r"\bdepends (?:entirely )?on (?:your|the specific|individual)\b"),

    # --- Transitions -----------------------------------------------------
    ("transition", "Moreover/Furthermore/Additionally", "B",
     r"(?:^|[.\n]\s*)(?:Moreover|Furthermore|Additionally|In addition|Consequently|Nevertheless|Notably|Importantly|Crucially|Indeed)\b"),

    # --- Vocabulary ------------------------------------------------------
    ("vocabulary", "LLM-favored word", "B",
     r"\b(?:delve|delving|tapestry|multifaceted|meticulous(?:ly)?|pivotal|cornerstone|testament|harness(?:es|ing)?|leverag(?:e|es|ing)|robust(?:ness)?|comprehensive(?:ly)?|holistic(?:ally)?|seamless(?:ly)?|groundbreaking|invaluable|transformative|unprecedented|intricate|profound(?:ly)?|elevat(?:e|es|ing)|streamlin(?:e|es|ing)|embark(?:s|ing)?|resonat(?:e|es|ing)|spearhead(?:s|ing)?|bolster(?:s|ing)?|garner(?:s|ing|ed)?|myriad|plethora|vibrant|underscor(?:e|es|ing|ed)|showcas(?:e|es|ing|ed)|foster(?:s|ing|ed)?|encompass(?:es|ing|ed)?|empower(?:s|ing|ed)?|unlock(?:s|ing)?|navigat(?:e|es|ing)\s+the|cutting-edge|state-of-the-art|ever-(?:evolving|changing|growing)|fast-paced|game-?changer|treasure trove|wealth of|beacon of|deep dive)\b"),

    # --- Chatbot debris --------------------------------------------------
    ("debris", "assistant leftovers", "A",
     r"(?:As an AI(?:\s+language\s+model)?|I hope this helps|Great question|Certainly!|Of course!|Let me know if|Feel free to|As of my last (?:update|knowledge)|Here(?:'s| is) (?:a|the) (?:revised|updated|rewritten)|Would you like me to|In this (?:article|post|guide), (?:we|I)(?:'ll| will)|\[Insert|\[Author, Year\]|\[Your \w+ here\])"),
]

# Substance probes: these measure what the writing is missing, not what it has.
SUBSTANCE = [
    ("vague_attribution", "unsourced appeal to authority",
     r"\b(?:studies (?:show|have shown|suggest|indicate)|research (?:shows|suggests|indicates|has shown)|experts? (?:say|agree|argue|believe)|it is (?:widely|generally|commonly) (?:recogni[sz]ed|accepted|believed|known|agreed)|many (?:believe|argue|would say)|some (?:argue|say|might say)|data shows|evidence suggests)\b"),
    ("hollow_quantifier", "quantity word with no quantity",
     r"\b(?:many|various|numerous|several|countless|a range of|a variety of|a number of|significant(?:ly)?|substantial(?:ly)?|considerable|a wide array of)\b"),
    ("hedge_stack", "stacked hedging",
     r"\b(?:may|might|could|can)\s+(?:potentially\s+|arguably\s+|possibly\s+)?(?:suggest|indicate|imply|help|serve|contribute|prove)\b"),
]

CODE_FENCE = re.compile(r"^\s*```")
MD_NOISE = re.compile(r"^\s*(?:[#>|]|[-*+]\s|\d+\.\s|!\[|\[!)")
WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")
SENT_SPLIT = re.compile(r"(?<=[.!?])[\"')\]]*\s+")
NUMERAL = re.compile(r"\b\d[\d,.]*\b")
PROPER = re.compile(r"\b[A-Z][a-z]{2,}\b")

TIER_WEIGHT = {"A": 2.0, "B": 1.0, "C": 0.4}


def strip_code(text):
    """Blank out fenced code blocks so they do not skew counts (keeps line numbers)."""
    out, inside = [], False
    for line in text.split("\n"):
        if CODE_FENCE.match(line):
            inside = not inside
            out.append("")
            continue
        out.append("" if inside else line)
    return "\n".join(out)


def line_index(text):
    starts, pos = [0], 0
    for line in text.split("\n"):
        pos += len(line) + 1
        starts.append(pos)
    return starts


def line_of(starts, offset):
    lo, hi = 0, len(starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if starts[mid] <= offset:
            lo = mid
        else:
            hi = mid - 1
    return lo + 1


def snippet(text, start, end, pad=24):
    a = max(0, start - pad)
    b = min(len(text), end + pad)
    s = text[a:b].replace("\n", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return ("..." if a > 0 else "") + s + ("..." if b < len(text) else "")


def overlaps(span, taken):
    return any(span[0] < t[1] and t[0] < span[1] for t in taken)


def scan_patterns(text, starts, table):
    """Run a pattern table, dropping hits that overlap an earlier hit."""
    hits, taken = [], []
    for entry in table:
        category, label, tier, pattern = entry
        for m in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
            if m.start() == m.end() or overlaps(m.span(), taken):
                continue
            taken.append(m.span())
            hits.append({
                "category": category,
                "label": label,
                "tier": tier,
                "line": line_of(starts, m.start()),
                "match": re.sub(r"\s+", " ", m.group(0)).strip()[:90],
                "context": snippet(text, m.start(), m.end()),
            })
    hits.sort(key=lambda h: h["line"])
    return hits


def sentences_of(text):
    prose = [ln for ln in text.split("\n") if ln.strip() and not MD_NOISE.match(ln)]
    body = " ".join(prose)
    out = []
    for s in SENT_SPLIT.split(body):
        n = len(WORD.findall(s))
        if n >= 3:
            out.append((n, s.strip()))
    return out


def longest_uniform_run(lengths, tol=3):
    best = run = 1 if lengths else 0
    for i in range(1, len(lengths)):
        run = run + 1 if abs(lengths[i] - lengths[i - 1]) <= tol else 1
        best = max(best, run)
    return best


def analyze(path, text, max_examples):
    clean = strip_code(text)
    starts = line_index(clean)
    words = WORD.findall(clean)
    real_wc = len(words)
    wc = max(real_wc, 1)  # divisor guard only; report real_wc
    per_k = lambda n: round(n * 1000.0 / wc, 1)

    hits = scan_patterns(clean, starts, PATTERNS)
    substance_hits = scan_patterns(
        clean, starts, [(c, l, "S", p) for c, l, p in SUBSTANCE])

    weighted = sum(TIER_WEIGHT[h["tier"]] for h in hits)
    density = round(weighted * 1000.0 / wc, 1)

    sents = sentences_of(clean)
    lengths = [n for n, _ in sents]
    if len(lengths) >= 2:
        mean_len = round(statistics.mean(lengths), 1)
        sd = round(statistics.pstdev(lengths), 1)
        in_band = round(100.0 * sum(1 for n in lengths if 15 <= n <= 30) / len(lengths))
        run = longest_uniform_run(lengths)
    else:
        mean_len = sd = in_band = run = 0

    numerals = len(NUMERAL.findall(clean))
    propers = len(PROPER.findall(clean))
    em_dashes = clean.count("—")

    by_cat = {}
    for h in hits:
        by_cat.setdefault(h["category"], []).append(h)
    sub_by_cat = {}
    for h in substance_hits:
        sub_by_cat.setdefault(h["category"], []).append(h)

    return {
        "file": str(path),
        "words": real_wc,
        "sentences": len(lengths),
        "density": density,
        "band": band_for(density),
        "tier_counts": {t: sum(1 for h in hits if h["tier"] == t) for t in "ABC"},
        "sentence_stats": {
            "mean_words": mean_len,
            "stdev": sd,
            "pct_15_to_30_words": in_band,
            "longest_uniform_run": run,
        },
        "specificity": {
            "numerals": numerals,
            "numerals_per_1k": per_k(numerals),
            "proper_nouns": propers,
            "proper_nouns_per_1k": per_k(propers),
            "em_dashes": em_dashes,
            "em_dashes_per_1k": per_k(em_dashes),
            "vague_attributions": len(sub_by_cat.get("vague_attribution", [])),
            "hollow_quantifiers": len(sub_by_cat.get("hollow_quantifier", [])),
            "hedge_stacks": len(sub_by_cat.get("hedge_stack", [])),
        },
        "findings": {k: v[:max_examples] for k, v in by_cat.items()},
        "finding_counts": {k: len(v) for k, v in by_cat.items()},
        "substance_findings": {k: v[:max_examples] for k, v in sub_by_cat.items()},
        "total_hits": len(hits),
    }


def band_for(density):
    """Thresholds calibrated so skilled human prose using antithesis lands
    in 'light', not 'heavy'.  Short samples are noisy — see render()."""
    if density >= 45:
        return "heavy"
    if density >= 20:
        return "moderate"
    if density >= 8:
        return "light"
    return "clean"


BAND_NOTE = {
    "heavy": "Pattern density well above human baseline. Worth a full pass.",
    "moderate": "Noticeable clustering. Check whether the hits are load-bearing.",
    "light": "A few hits. Normal for edited prose; fix only what reads badly.",
    "clean": "Nothing above baseline. Judge substance instead of surface.",
}


def render(r, max_examples):
    L = []
    add = L.append
    add(f"AI-TELL AUDIT  —  {r['file']}")
    add("=" * 64)
    add(f"{r['words']} words, {r['sentences']} sentences, {r['total_hits']} pattern hits")
    add(f"Density: {r['density']} weighted hits / 1000 words  →  {r['band'].upper()}")
    add(f"  {BAND_NOTE[r['band']]}")
    if r["words"] < 300:
        add("  NOTE: under 300 words — density is noisy here. Read the hits, not the band.")
    tc = r["tier_counts"]
    add(f"  strong(A) {tc['A']}   moderate(B) {tc['B']}   weak(C) {tc['C']}")
    add("")

    add("SENTENCE RHYTHM")
    s = r["sentence_stats"]
    add(f"  mean length      {s['mean_words']} words")
    add(f"  variation (sd)   {s['stdev']}" + ("   <- low; uniform rhythm is a tell" if 0 < s["stdev"] < 6 else ""))
    add(f"  in 15-30 band    {s['pct_15_to_30_words']}%" + ("   <- most sentences the same size" if s["pct_15_to_30_words"] >= 70 else ""))
    add(f"  longest run of similar-length sentences: {s['longest_uniform_run']}" + ("   <- flat stretch" if s["longest_uniform_run"] >= 5 else ""))
    add("")

    add("SPECIFICITY  (the part surface editing cannot fix)")
    sp = r["specificity"]
    add(f"  numerals            {sp['numerals']}  ({sp['numerals_per_1k']}/1k)" + ("   <- almost no concrete figures" if sp["numerals_per_1k"] < 4 else ""))
    add(f"  proper nouns        {sp['proper_nouns']}  ({sp['proper_nouns_per_1k']}/1k)" + ("   <- few named things" if sp["proper_nouns_per_1k"] < 10 else ""))
    add(f"  vague attributions  {sp['vague_attributions']}" + ("   <- claims with no named source" if sp["vague_attributions"] else ""))
    add(f"  hollow quantifiers  {sp['hollow_quantifiers']}" + ("   <- 'many/several/significant' doing real work" if sp["hollow_quantifiers"] >= 5 else ""))
    add(f"  stacked hedges      {sp['hedge_stacks']}")
    add(f"  em dashes           {sp['em_dashes']}  ({sp['em_dashes_per_1k']}/1k)   [weak signal on its own]")
    add("")

    if r["findings"]:
        add("PATTERN HITS")
        for cat in sorted(r["findings"], key=lambda c: -r["finding_counts"][c]):
            shown, total = r["findings"][cat], r["finding_counts"][cat]
            add(f"\n  {cat.upper()}  ({total})")
            for h in shown:
                add(f"    L{h['line']}  [{h['tier']}] {h['label']}")
                add(f"          {h['context']}")
            if total > len(shown):
                add(f"    ... {total - len(shown)} more (raise --max-examples)")
        add("")

    if r["substance_findings"]:
        add("SUBSTANCE FLAGS")
        for cat, hs in r["substance_findings"].items():
            add(f"\n  {cat.upper()}")
            for h in hs:
                add(f"    L{h['line']}  {h['context']}")
        add("")

    add("-" * 64)
    add("The scanner counts; it does not judge. A hit is a question, not a verdict.")
    add("Every pattern here is also legitimate human writing. Density and")
    add("clustering carry the signal, and no count proves authorship.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Scan prose for AI writing tells.")
    ap.add_argument("files", nargs="+", help="text/markdown files, or - for stdin")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--max-examples", type=int, default=8,
                    help="examples shown per category (default 8)")
    args = ap.parse_args()

    results = []
    for f in args.files:
        if f == "-":
            results.append(analyze("<stdin>", sys.stdin.read(), args.max_examples))
            continue
        p = Path(f)
        if not p.is_file():
            print(f"skip: {f} is not a file", file=sys.stderr)
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            print(f"skip: {f}: {e}", file=sys.stderr)
            continue
        results.append(analyze(p, text, args.max_examples))

    if not results:
        print("no readable input", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(results if len(results) > 1 else results[0], indent=2))
    else:
        print("\n\n".join(render(r, args.max_examples) for r in results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
