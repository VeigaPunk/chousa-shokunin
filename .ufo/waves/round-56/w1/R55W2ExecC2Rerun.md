# R55W2ExecC2Rerun — round-55 C2 after-state (executor / falsify)

Seat `R55W2ExecC2Rerun` (executor, leaf, no dispatch). Item: attack C2's after-state at lane commit
`29cfb12abd70f688b48c0d17f31e636f2d81104a` (the NMPA grey-literature field,
`corpus/knowledge/grey-literature-and-chinese-search-record-r40.md`, rows S124–S126). Predicate
`corpus/evidence/round55/claims.md` @ `1fc5d92b` R55-C2 is frozen, so findings are reported only.
Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, base `dba605de`, captures read-only from
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`; no network, no fetch, no
tool installed or upgraded (none needed). Scratch `/fast/scratch/hyaku/chousa-r56/R55W2ExecC2Rerun`.

## 0. What "at 29cfb12" means for this counter
```
$ git -C <lane> diff --name-only 29cfb12 HEAD | grep -v '^\.ufo'
LOG.md SCORECARD.md corpus/SOURCES.md corpus/evidence/round55/{c2-measure-after,c3-measure-after,census-end,wave-settled-r55}.txt
corpus/evidence/round56/** corpus/knowledge/grey-literature-field-china-r42.md corpus/lessons/{round-55,round-55-verifier-spotcheck,round-56}.md
$ git -C <lane> rev-parse 29cfb12:tools/build-spans.py → 072415ad… ; rev-parse HEAD:… → 072415ad…  (builder unchanged)
$ git -C <lane> status --porcelain corpus/evidence/round55 corpus/knowledge/grey-literature-and-chinese-search-record-r40.md \
      corpus/lessons/round-55.md tools/build-spans.py      → (empty)
```
`c2-count.py`, `spans.tsv`, `quotes.tsv`, the entry and the builder are byte-identical to 29cfb12;
`SOURCES.md` and `lessons/round-55.md` are not (round-56 rows, extra lesson lines) and the counter
reads both — so the state was scored twice: lane root (HEAD bytes) and a 29cfb12 archive copy
(`git archive 29cfb12 | tar -x -C $S/lane`, 243M) passed as `--root`. Both pass.

## 1–3. `c2-count.py` full, `--lane-only`, and the archive root
```
$ python3 corpus/evidence/round55/c2-count.py                 # exit 0, 0.38 s
ENTRIES=1/1 (min 1) REFUSED_ENTRIES=0     HELD_CITED=- HELD_BAD=0
BOUND=3/3 (min 2) REFUSED=0               BOUND_IDS=S124,S125,S126 GUIDELINE_BOUND=yes
REF_ID_UNBOUND=0                          NEW_GROUND=1/1
QUOTE_ROWS=19 ON_BOUND=19/19              SPAN_IDS=3/3 (min 3 each)
QUOTES_IN_SPAN=19/19  QUOTES_IN_ENTRY=19/19  QUOTES_IN_LESSON=19/19  QUOTE_SHORT=19/19  SPAN_CONTEXT=19/19
CAPTURE_BOUND=19/19   SUBSTANCE=PASS      ANCHOR_BOUND=3/3      INFERENCE_GROUNDED=1/1
QUARANTINE_VERDICTS=1/1 (S125)            QUARANTINE_BLOCKED_ADOPTED=0            C2=PASS
$ python3 corpus/evidence/round55/c2-count.py --lane-only      # exit 1 — predicate: never passes
(same lines except) CAPTURE_BOUND=skipped … C2=FAIL
$ python3 …/c2-count.py --root $S/lane       # runs 1, 2 and the lane-root repeat
QUARANTINE_VERDICTS=1/1 (S125) / QUARANTINE_BLOCKED_ADOPTED=0 / C2=PASS   exit=0 (×3)
```

## 4–6. build-spans `--check` from the copy, and the two held-out checkers
```
$ cd $S/lane && python3 tools/build-spans.py --quotes corpus/evidence/round55/quotes.tsv \
      --out corpus/evidence/round55 --check
SPANS_ROWS=19 STALE=0      # exit 0; copy spans.tsv sha256 aa73b1e42696a906… after the run == committed
# spans/ = 19 files both sides; $S/lane/tools/build-spans.py content sha256 1ed2650af28ea8e3… == committed
$ python3 corpus/evidence/round51/quote-substance-check.py corpus/evidence/round55/spans.tsv
IDS=3 QUOTES=19 FAILURES=0                                       # exit 0
$ python3 tools/inference-ground.py --entry corpus/knowledge/grey-literature-and-chinese-search-record-r40.md \
      --spans corpus/evidence/round55/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root .
GROUND entry=…grey-literature-and-chinese-search-record-r40.md section=1 bullets=3 tokens=8 grounded=8 ; GROUND: PASS  # exit 0
```

## 7. Independent re-derivation of all 19 rows (my script; not the builder, not the counter)
`$S/verify_c2.py` imports BASE `tools/capture-text.py` itself (`git show dba605de:…`), derives each
DEFINED form from the `.raw`/`.txt` capture, checks slice, offset, digest and containment:
```
ROWS=19  ROWS_BAD=0  exit 0
S124 key=bdff491a75c6abeda1d9c01d ole/zip offs=4545,4572,681,914,966,1002,0,0,0,5348,260  len(span)=101–212
     charN=4625,4652,761,994,1046,1082,4,22,33,5428,340   occ_in_form=1 each
S125 key=27d4865f201e99c1fed9f79b txt offs=162,291,700,871  charN=242,371,780,951   occ_in_form=1 each
S126 key=d663d66e2d39f868d84b1781 txt offs=1124,1244,697,2448 charN=1204,1324,777,2528 occ_in_form=1 each
```
Every span is exactly `form[offset:offset+len(span)]`, longer than its quote, quote at the recorded
`char N`; S124's 761/994/4625/4652 are the offsets the entry itself cites. Quote shape: max 139
chars / 19 whitespace words (limits 160 / 25), min 4 chars.

## 8. Controls rebuilt in scratch, scored against the committed receipt
```
$ python3 corpus/evidence/round55/controls/build-c2-controls.py $S/c2c      → "staged rewrite" exit 0
staged : BOUND=0/3 BOUND_IDS= REF_ID_UNBOUND=12 QUOTE_ROWS=0 CAPTURE_BOUND=0/0 SUBSTANCE=FAIL QUARANTINE_VERDICTS=0/1 C2=FAIL exit=1
rewrite: BOUND=2/3 BOUND_IDS=S124,S125 GUIDELINE_BOUND=yes REF_ID_UNBOUND=2 QUOTE_ROWS=0 ANCHOR_BOUND=0/2 C2=FAIL exit=1
$ diff (c2-controls.txt minus its comment/$ lines) scored.txt   → RECEIPT_MATCH=identical (44 lines each)
```

## 9. Probes: what the counter actually kills (each scored with `--root <probe tree>`)
- p1 non-reader forge: for all 11 S124 rows the span becomes the `.raw`'s UTF-16LE-decode window at
  its quote, offset rewritten to the decode position. Structurally perfect —
  `QUOTES_IN_SPAN=19/19 SPAN_CONTEXT=19/19` — but `CAPTURE_BOUND=8/19 ANCHOR_BOUND=2/3 C2=FAIL`
  exit 1. Measured why: every S124 quote IS findable in the decode (11/11) and **0/11** decode
  windows equal the form slice (form 13,718 chars vs decode 121,964).
- p2 offset drift: `spans/S126-4.txt` offset 2448→2449, span untouched → `CAPTURE_BOUND=18/19
  C2=FAIL`. `ANCHOR_BOUND` stayed 3/3: S126's anchor cell names only 777/1204/1324, so drift in its
  fourth quote is caught only by CAPTURE_BOUND.
- p3 digest forge: S124 `capture_sha256` zeroed → `CAPTURE_BOUND=8/19 C2=FAIL`.

## 10. Structural claims checked independently
```
$ grep -c "build.spans" corpus/evidence/round55/c2-count.py → 0     (separability: C1's builder never runs)
$ git grep -l -e 是否检索灰色文献 dba605de -- corpus/knowledge → (nothing) exit 1     (NEW_GROUND=1/1 is real)
$ grep -c 是否检索灰色文献 …r40.md → 5 ; grep -n "^source:" → S124/S125/S126 — <url> (one per bound document)
registry S124/S125/S126: 11 cells, [3]=B,B,A  [7]=mined [8]=2026-10-27 [10]=the entry (used-by)
lessons/round-55.md:63 `register S125 (round6) — gcpunion .doc — verdict: absent-as-written`
```

## 11. Findings (reported against the frozen predicate; nothing patched)
- F1 substance floor: `S124-8`'s quote is `（试行）`, 4 chars, and it passes
  `quote-substance-check.py` (MIN_CHARS=3, `corpus/evidence/round51/quote-substance-check.py:26`).
  So `QUOTES_IN_*=19/19` counts one row with no evidentiary content and `SUBSTANCE=PASS` is a floor,
  not entailment (the tool says so itself). The bind is not hollow — S124 carries 11 rows against a
  per-id minimum of 3 — but 19 rows ≠ 19 substantive quotes.
- F2 anchor coverage: ANCHOR_BOUND is satisfied by whichever `char N` a row names; S126 names 3 of
  4, so a self-consistent drift in the unnamed one survives it (p2). CAPTURE_BOUND ("the exact
  slice at the recorded offset") is the load-bearing clause.
- F3 depth: the `.doc` sidecar is the raw decoded as UTF-8 (`bdff491a….txt` starts `'��\x11ࡱ\x1a�…'`,
  garbage) and the UTF-16LE decode is reachable but wrong (§9): refused on content, not by a hook.
- F4: round-55's predicate does not require a quote to occur once in its form, but all 19 do
  (occ_in_form=1), so round-56's stronger uniqueness clause inherits no drift from this manifest.
## Evidence retained
The §0 `git status --porcelain` for the round-55 files, the entry and the builder is empty after
every run; all control/probe trees lived under `$S`; no lane file, registry, git/jj state, sibling
lane or `~/.local/bin` was written; no installs, no network. Scratch removed.

VERDICT: attacked round-55 C2's after-state at 29cfb12 (counter full + `--lane-only`, build-spans
`--check`, quote-substance, inference-ground, 19-row independent re-derivation, both controls
rebuilt) — it SURVIVES: `C2=PASS` exit 0 on the lane root and on the 29cfb12 archive root,
`--lane-only` FAIL, controls byte-identical to `c2-controls.txt`, and the three shortcuts
(UTF-16LE non-reader, offset drift, forged digest) each die on the named clause; F1/F2 are
calibration readings, not failures.
