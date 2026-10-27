# R57W2ReviewC2After — residual re-derivation of R57-C2 at HEAD

Seat: reviewer (leaf, no subagents). Scope: R57-C2 after-state only. Scratch `/fast/scratch/hyaku/chousa-r57/R57W2ReviewC2After/`
(TMPDIR=$PWD, PYTHONDONTWRITEBYTECODE=1; `git clone --shared` of the lane into `lane/`; deleted before yield). No lane writes
except this file; no network; no installs (python3 3.14.8, git, `pdftotext version 26.08.0` — the pinned preflight version — present).

Lane HEAD at run time: `3010e7537d163d9a76264a166d491214ecdaf45e` — **one commit past** the stated tip `1c9626e`
(`3010e75` = "round-57: W2 residual falsify call"). `git diff 1c9626e..HEAD` touches only `.ufo/...` files;
`git diff --stat 1c9626e..HEAD -- corpus/ tools/` prints nothing. C2 inputs are identical to the claimed tip.

## (1) Frozen diff — NOT literally empty, and correctly so

`git diff c2f914c53201a8f8ee4fef823b82681051d55592 HEAD -- corpus/evidence/round57/claims.md corpus/evidence/round57/c2-count.py corpus/evidence/round57/controls`
produces a diff — but it is exactly and only the later C3 freeze `fd95724d56a33a150cd2638fadd2ce1f3425e6c` (child of `c2f914c`:
`git log` shows `fd95724` directly atop `c2f914c`): claims.md `@@ -66,3 +66,62 @@` appends the `## R57-C3` section, and the
controls dir gains `build-c3-controls.py`, `c3-before.txt`, `c3-controls.txt`. That append is what claims.md's own protocol
requires ("each in its own lane commit before any of its data exists … corrections are appended below it"). Proof the C2
section is untouched: `git diff c2f914c5 HEAD -- claims.md | grep -c '^-'` → `1` (the `--- a/claims.md` header; zero deleted
content lines), and `git diff c2f914c5 HEAD -- corpus/evidence/round57/c2-count.py corpus/evidence/round57/controls/build-c2-controls.py corpus/evidence/round57/controls/c2-before.txt corpus/evidence/round57/controls/c2-controls.txt` → empty, exit 0.

Spec-text discrepancies (reported, none are claim defects): (a) the item's "must be empty" is false only because the spec
included `claims.md` and `controls/` — paths the C3 freeze legitimately appended to; C2's own bytes are frozen-clean.
(b) the goal's C3 freeze hash `fd95724d56a33a150cd2638fadd2ce1f3425e6c` does not resolve ("unknown revision"); the real
commit is `fd95724d56a33ad150cd2638fadd2ce1f3425e6c` (transposed `8f`/`d1` digits in the prompt). Frozen content unaffected.

## (2) Counter at HEAD, twice — identical to the e0e73e0 after-receipt

```
$ python3 corpus/evidence/round57/c2-count.py   # run 1
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS
exit=0
$ python3 corpus/evidence/round57/c2-count.py   # run 2
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS
exit=0
```
Both lines are byte-identical to the summary inside the `e0e73e0` commit subject ("SET=47 VERDICTS=47/47 REPRODUCED=41
DRIFTED=5 (S083 S087 S113 S114 S121, absent=0) UNREACHABLE=1 (S105, 3 failed attempts >=600s apart) BYTE_BACKED=46
CONSISTENT=46/46 FLAGGED=0/0 C2=PASS"). Deterministic, exit 0.

## (3) Three controls on the scratch clone — all fail at the frozen profiles

```
$ python3 lane/corpus/evidence/round57/controls/build-c2-controls.py ctl   # lane = shared clone @3010e75
EMPTY
JUNK
ALLFAIL
$ python3 lane/corpus/evidence/round57/c2-count.py --root ctl/EMPTY
SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL   exit=1
$ python3 lane/corpus/evidence/round57/c2-count.py --root ctl/JUNK
SET=47 VERDICTS=47/47 REPRODUCED=0 DRIFTED=47 UNREACHABLE=0 BYTE_BACKED=47 CONSISTENT=47/47 FLAGGED=0/47 C2=FAIL   exit=1
$ python3 lane/corpus/evidence/round57/c2-count.py --root ctl/ALLFAIL
SET=47 VERDICTS=47/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=47 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL   exit=1
```
All three match `controls/c2-controls.txt` exactly; no control meets the target.

## (4) Wave-settled check

`python3 corpus/evidence/round55/wave-settled-check.py --round 57` → exit 2, "no fleet commit adds
`.ufo/reports/round-57/chousa.md`" (round report not yet filed — correct pre-filing mode). With `--before-filing`:
```
SETTLED w1 results=2026-10-27T06:11:09-03:00
WAVES=1 SETTLED=1     exit=0
```
`w1-results.json` was committed by `a8d4e7d` at 06:11:09, before any report can exist — satisfied. Note: `w2.ready.dispatched`
is still untracked (`git status` shows `??`); when committed, filing before a committed `w2-results.json` would trip this check.

## (5) store-record-audit at HEAD — expected FAIL, classes all named

```
$ python3 tools/store-record-audit.py
ORPHAN=3 ['53a92273a452a58f28368691', 'd473754a0cbf8d3095255d5a', 'd8b4f8f8829b813f16227893']
RECORD_ONLY=0
BYTES_STALE=0
STORE_BUT_RECORD_DENIES=2 ['d473754a0cbf8d3095255d5a', 'd8b4f8f8829b813f16227893']
STORE_RECORD_AUDIT=FAIL rows=144 keys=87      exit=1
```
The two record-denied keys = the spec's expected class: `d473754a`/`d8b4f8f8` (hnysfww wrap-up bytes, failure-only refetch
rows, named in `corpus/lessons/round-57.md:32` and `:46`). The third ORPHAN `53a92273` = the recordless NHC gazette PDF
committed by `b022b13`, reverse-identified by `R57W1RevOrphans`/`R57W1ExecStoreMap` (SonicState §63: "no refetch.tsv row,
bytes predate this round"). All three are pre-disclosed wave/lesson findings, not claim defects. `rows=144` + header = the
145-line `refetch.tsv` I counted.

## Residual legs I attacked (beyond the scripted five)

- **Independent re-derivation, no counter code**: my own script walks SET_REV manifests (12 `spans.tsv` carry
  `capture_sha256`) → `distinct_triples: 47`; recomputes verdicts from store bytes + refetch ledger →
  `REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 MISSING=0` — the counter's exact numbers.
- **DRIFTED honesty**: all five drifted triples still contain every pinned quote (`absent=0/{2,2,6,9,6}`) → `FLAGGED=0/0`
  is genuine, not flag-laundering; `corpus/lessons/round-57.md` carries zero FRESHNESS-FLAG lines.
- **D4 dormancy (w1 finding)**: zero non-chronological `fetched_utc` runs in the ledger → the file-order "last success"
  bug stays inactive.
- **S105 UNREACHABLE**: three `curl_rc=28` rows 08:06:12/08:30:12/08:33:48Z (span 1656s ≥ 600s); no `e3ca8f4f` file in
  `corpus/captures` — the wrap-up bytes were deliberately deleted so the frozen "no capture" leg could attest it
  (lesson :46 names this; the reproducible-bytes evidence survives in git history). Disclosed, pre-existing, unchanged.
- w1 attacks already named the standing gaps — C2Forge §5 (DRIFTED leg is record-attested, not pin-bound: junk-swap +
  matching flag passes by the frozen letter), C2Same D1–D4 — all confirmed dormant/accepted as designed; nothing new added.

## Findings

- F1 (spec text, not claim): the scripted "empty diff" cannot hold since the C3 freeze legitimately appends to the same
  three paths; C2's own files and every claims.md line are untouched (evidence §1).
- F2 (spec text): C3 freeze hash in the prompt is a transposed typo; real `fd95724d56a33ad…`.
- F3 (state): lane tip moved `1c9626e` → `3010e75` (W2 dispatch, `.ufo`-only); C2 unaffected.
- F4 (residual, disclosed): audit FAIL classes (ORPHAN=3, DENIES=2) and the S105 byte-deletion are standing, named
  disclosures — none reachable as a C2 falsifier.

VERDICT: attacked R57-C2's landed after-state at HEAD (freeze isolation, counter determinism ×2, all three controls on a
shared clone, wave-settled filing order, audit FAIL classes, plus a code-independent 47-triple re-derivation) — the claim
SURVIVES; the only falsifier-class items found are spec-text typos, not claim defects.
