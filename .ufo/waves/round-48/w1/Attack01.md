# Attack01 — held-out C1 precision probes (round 48)

**Verdict:** both correctly reasoned bullets were refused by the current tool with `INF_POLARITY_FLIP` (2/2). This is a small probe, not a frozen fixture or claim; no post-score predicate change is proposed.

## Method and evidence

Used only committed local fixture data: `corpus/fixtures/inference-ground-r47/spans.tsv`, `spans/S901-1.txt` (`the release ships a frozen pool of pages; no revision is recorded per sentence`), `spans/S902-1.txt` (`the archived copy is dated at build time; a placeholder value is not an archive link`), and `counts.json`. Scratch copies were placed under `/tmp/chousa-r48-attack01/{a,b}`. Each run used the current `tools/inference-ground.py` with the scratch entry, copied spans manifest and counts file; no network or installs.

## Held-out examples and observed results

1. **Negated-phrase scope; unlisted absence wording, different from round 47.** Correct inference: “Since `no revision is recorded` per sentence, the revision history remains undocumented for individual pages (`S901`).” The supported conclusion is that no per-sentence revision record exists; “undocumented” expresses the same absence without asserting revisions were recorded. The phrase occurs in the cited S901 span. Run: `python3 tools/inference-ground.py --entry /tmp/chousa-r48-attack01/a/probe.md --spans /tmp/chousa-r48-attack01/a/spans.tsv --counts /tmp/chousa-r48-attack01/a/counts.json --root /tmp/chousa-r48-attack01/a` → `GROUND ... tokens=1 grounded=1`; `FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revision'`; `GROUND: FAIL` (exit 1). Why: `revision` reuses the phrase's scope stem, while the phrase's explicit `no` is inside the grounding quote (removed from unquoted bullet words); no recognized negator remains within the tool's P1 window. `undocumented` is an unlisted absence expression.

2. **Affirmed phrase; neighboring-word binding.** Correct inference: “`the archived copy is dated at build` — not timestamps; the archive remains dated (`S902`).” The bullet affirms the archived copy's date as the source states; `not` contrasts timestamps, not the archive. The quoted phrase occurs in cited S902 span. Run: `python3 tools/inference-ground.py --entry /tmp/chousa-r48-attack01/b/probe.md --spans /tmp/chousa-r48-attack01/b/spans.tsv --counts /tmp/chousa-r48-attack01/b/counts.json --root /tmp/chousa-r48-attack01/b` → `GROUND ... tokens=1 grounded=1`; `FINDING INF_POLARITY_FLIP bullet=1 token='the archived copy is dated at build / archive'`; `GROUND: FAIL` (exit 1). Why: after removing the quote, `archive` matches the affirmed phrase's `archived` scope stem, and `not` is two words before it. P2 treats proximity as negation despite the local contrast binding `not` to `timestamps`.

These examples vary phrase polarity/scope and show the false-refusal mechanisms for an unlisted absence term and neighboring-word attachment. Neither reuses the held-out round-47 wording (`nonexistent`, `cannot ... revised`, nor the `not ... build date` construction). The span and count bytes were copied, not changed; entries are probe-only.

## Residual risk / verification gap

Two examples establish these two observed refusals only; they do not estimate a general false-refusal rate, cover every negator-distance boundary, or establish behavior on real-source material. No frozen fixtures, claims, or production files were changed.
