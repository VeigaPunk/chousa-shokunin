# CritC3Axis — C3 admission & axis naming (round 45, wave 2)

Seat: L1Chousa45.CritC3Axis (critic, leaf). Item: judge C3 for admission and
axis naming; test whether a junk-row commit can pass the default mode; test
whether the do-nothing control is a control the claimed work skips.
Measured on committed bytes at `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`
in `/tmp/chousa-r45-CritC3Axis/tree` (git archive); every counter run from
inside that tree. No lane writes; no fetch; scratch deleted at end.

## 1. Axis naming — holds

Round-prompt rule: name the axis by the surface the round changes; a
coverage/depth claim names the surface it moves and the command that would
show it unmoved.

- Surface moved: the two knowledge entries (`corpus/knowledge/evidence-archive-field-policy-r41.md`,
  `evidence-snapshot-coverage-r40.md`), their grounding artifacts
  (`corpus/evidence/round45/spans.tsv`, `spans/S082-1.txt`, `S082-2.txt`,
  `S083-1.txt`, `S083-2.txt`, `counts.json`), and three Registry rows
  S082/S083/S084 in `corpus/SOURCES.md`.
- Command that would show it unmoved: `python3 corpus/evidence/round45/c3-count.py`
  (default and `--lane-only`), both named in claims.md lines 91-92.
- 'depth' vs 'coverage': the round does have a coverage-side effect (three
  new Registry rows). But the substance the counter uniquely enforces is the
  capture-bound anchoring — each span sits at its recorded byte offset inside
  the sha256-pinned capture, and the seven counts are re-derived from the
  10 MB train.json capture. That is claim-vs-source verification at byte
  granularity (the lane's depth axis), not registry breadth. Feature
  check `CAPTURE_BOUND`/`COUNTS_REDERIVED` only run in default mode, and the
  claim itself names the lane-only blind spot — consistent with a depth
  claim. Verdict: **holds**.

## 2. Admission — mechanical predicate holds on the committed tree

Commands (verbatim, decisive output):

```
$ cd /tmp/chousa-r45-CritC3Axis/tree
$ python3 corpus/evidence/round45/c3-count.py
ENTRIES=2/2  CITES_BOUND=3/3  QUOTES_IN_SPAN=4/4  QUOTES_IN_ENTRY=4/4
COUNTS_IN_ENTRY=7/7  CAPTURE_BOUND=4/4  COUNTS_REDERIVED=7/7
C3=PASS   exit=0
$ python3 corpus/evidence/round45/c3-count.py --lane-only
ENTRIES=2/2  CITES_BOUND=3/3  QUOTES_IN_SPAN=4/4  QUOTES_IN_ENTRY=4/4
COUNTS_IN_ENTRY=7/7  CAPTURE_BOUND=skipped  COUNTS_REDERIVED=skipped
C3=PASS   exit=0
```

Independent spot-checks all hold: capture files exist with the recorded
sha256 (`8e1f5bff…` README, `a3ff65e0…` paper, `ae5eda7c…` train.json =
counts.json `capture_sha256`, `ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c`);
quote offsets match the entries' own "capture char" claims (README 1969 and
1027, paper 14575 and 120884, via `.find()` on captures); the four span
windows begin exactly 160 chars before each quote; Registry rows S082/S083/
S084 each carry URL, `mined`, and the citing entry in used-by. Kill rule
satisfied in both modes.

## 3. Junk-row forge — the default mode CAN be passed; "cheapest gate" claim is false

claims.md line 102-105 and c3-count.py docstring lines 20-24 state the
cheapest full-score forge is *entries + a self-consistent span manifest with
invented quotes*, refused by the default mode. That is wrong: the cheapest
forge is **junk entries reusing the committed real spans/counts** — it
passes both modes and touches only two files.

Reproduction (scratch clone of the committed tree; only the two entry bodies
replaced with no-claim junk; spans.tsv, spans/, counts.json, SOURCES.md
untouched):

```
$ python3 corpus/evidence/round45/c3-count.py --root /tmp/chousa-r45-CritC3Axis/forge/tree
ENTRIES=2/2  CITES_BOUND=3/3  QUOTES_IN_SPAN=4/4  QUOTES_IN_ENTRY=4/4
COUNTS_IN_ENTRY=7/7  CAPTURE_BOUND=4/4  COUNTS_REDERIVED=7/7
C3=PASS   exit=0
```

The junk FIELD entry is 606 bytes: two `source:` lines plus the four quotes
pasted verbatim; the junk SNAP entry is 375 bytes: the source line plus the
seven count figures. No sentence asserts anything about AVeriTeC. The counter
never inspects entry content beyond presence of the quote strings (c3-count.py
lines 124-125) and count digits (lines 138-141); it cannot tell a grounded
inference from decorated junk. So the counter proves *provenance mechanics*
(quotes genuinely sit at those offsets in sha256-pinned captures), not that
the entries' inferences follow from them. The invented-quote forge is not the
cheapest; the pass-both-modes forge is, and the committed control suite
(`c3-control-forged-span.txt`) does not cover it.

## 4. Do-nothing control — reproducible and honest, but weak; the claimed work does not skip it

Reproduced verbatim on a clone with the round-45 evidence footprint removed
(entries, spans.tsv, spans/, counts.json):

```
ENTRIES=0/2  CITES_BOUND=0/3  QUOTES_IN_SPAN=0/4  QUOTES_IN_ENTRY=0/4
COUNTS_IN_ENTRY=0/7  CAPTURE_BOUND=0/4  COUNTS_REDERIVED=0/7
C3=FAIL   exit=1
```

Matches `controls/c3-control-do-nothing.txt`. It is scored at freeze and is
not skipped. But it is a baseline, not a discriminator: it fails by
construction (absence of every required artifact) and tells nothing about
whether the counter can detect partial or alternative work — that function is
served only by the forged-span control, which misses the junk-entry forge of
section 3. A *narrowed* do-nothing (delete only entries, keep spans) would
print `QUOTES_IN_SPAN=4/4 … C3=FAIL` — the control's all-zero output
corresponds to the round-44 tree, which is the right frame, but its
discriminating value is low.

## 5. Verdict: holds-narrowed

C3's mechanical admission holds on the committed tree (both modes, exit 0).
Axis naming 'depth' holds. Defect: the claim overstates the gate — "the
cheapest gate that would score full marks without the work" is junk entries
reusing the committed real spans, which passes **both** modes; the default
mode refuses invented quotes but not empty/detached entry prose. The
do-nothing control is genuine but tautological and does not cover the
cheapest forge.

## 6. Resolvable pointers

- claims.md (committed) lines 102-105: forged-span control claim — misses the
  junk-entry forge; line 100-101: do-nothing control (reproduced).
- c3-count.py lines 20-24: "cheapest gate" sentence — false; lines 112-131:
  span/capture loop never inspects entry semantics; lines 133-146: count loop
  only checks digit presence and re-derivation.
- Junk forge reproduction: `/tmp/chousa-r45-CritC3Axis/forge/tree`
  (deleted); decisive outputs above. Entry junk files sha256:
  `e21537c15659c9c26718e9490dc5b82821a5e4aa966846817111d5965b94621d` → junk
  `a3640fa99a0c2e39c96d69e28ff46c6cfb0d6b4e04167ad9cca44ed9dbb0ef8d`;
  `2e1973856c0e9101aadefb967100086ec37d8b024dfa42317a7d7beaf7e4bdcf` → junk
  `a8e5e26e8cd70c7d4dfdbd01b1d7c0b7698a2bae32da03df74ac1b885751de0e2`.
- Capture cross-check offsets: README quotes at chars 1969/1027; paper quotes
  at 14575/120884 (span offsets 1809/867/14415/120724, windows 160 chars).

Smallest safe correction (report only): narrow the claim to provenance
mechanics — "quotes bound at byte offsets in sha256-pinned captures" — and
replace the "cheapest gate" sentence with the junk-entry forge it actually
permits, or add a semantic-content check the counter cannot perform on bytes.
