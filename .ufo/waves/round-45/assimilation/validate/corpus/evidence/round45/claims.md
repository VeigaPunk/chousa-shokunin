# Round 45 claims — frozen before scoring

author: chousa L1 (omp in-session L1, hyaku run 6)
date: 2026-10-25
round: 45 (attempt 1)
base: `d29bf47d94149a1b71581eeb0f36d9ff22d41da3`

No seat has scored these predicates. The construction checks that chose the
quotes and the counts are disclosed below; they are not seat scores, and the
predicates are not retuned after any seat scores.

Lowest scored non-retired axis: operability, 3/10. C1 works that axis.
No external fetch: the fetch-scope L0 `8d77e6c1` is still open. Freshness is
not a claim: every capture opened this round predates the round's launch.

Round tag (considerthese/2026-10-24.md, "Tag each round as research ground or
plumbing"): C1 and C2 are plumbing; C3 is research ground.

## C1 — operability (lowest scored non-retired axis, 3/10)

Routed from the round-44 closure, D5 (lesson mistakes 4 and 5).

Predicate R45-C1: tools/parent-lifetime.sh, run with a stub `kimi` first on
PATH, (a) exits 3 on a dispatch with zero tasks and still writes
`end ... n_spawned=0`; (b) exits 0 on a two-seat dispatch whose stub exits 0,
with `n_spawned=2 n_reaped=2`; (c) exits 3 on a two-seat dispatch whose stub
outlives `--timeout 1`, with both reap lines `exit_code=124`; (d) exits 2 when
a dispatch run omits `--timeout`; and (e) every receipt of (a)-(c) opens with
a start line carrying `timeout_s=<the value passed>`.

Counting command: `python3 corpus/evidence/round45/c1-count.py`

Target, one value: `CASES_MATCH=5/5`, `C1=PASS`, exit 0.

Do-nothing control (scored at freeze): the round-44 launcher, tool blob
`79ee8f2942802ee1d1771a7e5887a7a9a36cdb8b`, scores `CASES_MATCH=1/5`
(case b only), exit 1 — `controls/c1-control-r44-tool.txt`.

Kill rule: any case other than `ok`, or exit ≠ 0.

## C2 — calibration

Routed from the round-44 closure, D2. The SKILL.md Gates table is the lane's
own account of its gates; the committed tree is the observed state. The
counter counts the mismatches.

Predicate R45-C2: every committed gate entry point of the lane — each file
directly under tools/, and each corpus/evidence/round*/ file named
c<N>-count*.py, verify-receipts.py or errata-count.py — is named by its
repo-relative path inside a Gates row of SKILL.md, a Gates row being a line
of the `## Gates` section (up to the next `## ` heading) that starts with `|`,
carries at least 8 `|` separators and contains the word `exit`.

Counting command: `python3 corpus/evidence/round45/c2-count.py --list`

Target, one value: `UNREGISTERED=0`, `C2=PASS`, exit 0 (the counter
enumerates the full set; `ENTRY_POINTS` is whatever the measured tree holds,
this round's own counters included).

Before (scored at freeze): base tree `d29bf47d…` → `ENTRY_POINTS=51`,
`REGISTERED=25/51`, `UNREGISTERED=26`, exit 1 — `controls/c2-control-base.txt`.
The freeze tree adds this round's three counters, so its before is
`UNREGISTERED=29` once all three exist.

Cheapest forge (QUALITY 60): the bare paths pasted anywhere, or a one-cell
row. Refused by the row rule. A plausible row whose verdict map is wrong still
passes: a reader's check, named here.

Kill rule: `UNREGISTERED` ≠ 0, or exit ≠ 0.

## C3 — depth (sourced on rows opened this round; assimilation)

Theme, one: what an AVeriTeC archive field does and does not record. Two
staged entries, three rows, from `merge/chousa/`; re-grounded from the
campaign's on-disk capture cache (not committed in the campaign tree; the
lane commits the located spans, closing round-44 closure D1).

Predicate R45-C3: the two adopted entries
corpus/knowledge/evidence-archive-field-policy-r41.md and
corpus/knowledge/evidence-snapshot-coverage-r40.md exist; their three
`source:` lines bind lane ids S082, S083 and S084 to the AVeriTeC README, the
AVeriTeC v3 HTML paper and the AVeriTeC train.json URLs, each such Registry
row carrying that URL, status `mined` and the citing entry in used-by; the
four located quotes in corpus/evidence/round45/spans.tsv each sit in their
lane-committed span file and in the citing entry, and each span sits at its
recorded offset in the capture named sha256(url)[:24].txt whose sha256 is the
recorded one; the seven counts in corpus/evidence/round45/counts.json each
appear in the snapshot entry and are re-derived from the train.json capture
with the recorded sha256.

Counting commands: `python3 corpus/evidence/round45/c3-count.py` and
`python3 corpus/evidence/round45/c3-count.py --lane-only`

Target, one value each: default — `ENTRIES=2/2`, `CITES_BOUND=3/3`,
`QUOTES_IN_SPAN=4/4`, `QUOTES_IN_ENTRY=4/4`, `COUNTS_IN_ENTRY=7/7`,
`CAPTURE_BOUND=4/4`, `COUNTS_REDERIVED=7/7`, `C3=PASS`, exit 0; `--lane-only`
— the same first five values, the two capture-bound lines `skipped`,
`C3=PASS`, exit 0.

Do-nothing control (scored at freeze): the freeze tree, no entries →
`ENTRIES=0/2` … `C3=FAIL`, exit 1 — `controls/c3-control-do-nothing.txt`.
Forged-span control (scored at freeze): entries, rows and a self-consistent
span manifest with four invented quotes pass `--lane-only` (exit 0, the named
blind spot of lane-only mode) and fail the default (`CAPTURE_BOUND=0/4`,
`COUNTS_REDERIVED=0/7`, exit 1) — `controls/c3-control-forged-span.txt`.

Kill rule: any count short of its target in either mode, or exit ≠ 0.

## Construction checks (L1, before freeze; not seat scores)

- README capture `ce16d57277fedfd4f0e7750e.txt` (4771 bytes): "An
  archive.org link for the source url" at char 1969, "Where possible, an
  archive.org link to the original claim url" at char 1027, each once.
- Paper capture `412b146a2720ce6557268d05.txt`: "we cache all pages used as
  evidence in the internet archive" at char 14575; "Archive.org returns a 404
  page for these" at char 120884; `cached_source_url` and
  `cached_original_claim_url` occur 0 times; "Where possible" occurs once, in
  the annotator guideline on extractive answers.
- train.json capture `974299ae4b5f3bdb808b36a9.txt` (10184813 bytes, sha256
  `ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c`):
  records 3068; evidence answers carrying `cached_source_url` 6511, non-empty
  6510, empty 1; records carrying `cached_original_claim_url` 2531, non-empty
  1145, empty 1386 — the staged entry's figures, reproduced.
