# R57W1CritC2Forge — attack on R57-C2 kill rule (forgeries in scratch)

Seat: critic (UFO-FSD), leaf, no subagents dispatched. Lane claim frozen at c2f914c5; counter
`corpus/evidence/round57/c2-count.py` copied/run only inside scratch. No lane/fleet/shokuknow
writes; no network. Tooling: nothing installed — used host python3 3.14.8, pdftotext 26.08.0
(counter's pinned version), git 2.x; `pacman` untouched per host guard.

Harness: scratch `/fast/scratch/hyaku/chousa-r57/R57W1CritC2Forge/` (mkdir -p; TMPDIR=$S;
PYTHONDONTWRITEBYTECODE=1), `git clone --shared chousa-shokunin $S/lane`, real working-tree
state (refetch.tsv, corpus/captures) synced into the clone; fixtures overlaid; counter run as
`python3 $S/lane/corpus/evidence/round57/c2-count.py --root $S/lane`. Junk raws built with the
counter's own `recipe_txt` so .txt files are recipe-consistent by construction. Fixture driver
imported the counter module read-only for `pinned_set`/`recipe_txt`/`key`. Scratch dir deleted
before yield (`rm -rf`, verified 0 remaining).

Pinned set re-derived from SET_REV 6656f077… inside the clone: 47 triples (matches SET_N).

## BASELINE (harness fidelity, not an attack)

Synced real state (working tree incl. other seats' live rows): rc=0
`SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS`
— identical to committed after-receipt e0e73e0. Harness reproduces the canonical measurement.

## (1) RECORD-ONLY — refetch.tsv 47 success rows, zero capture files

rc=1 `SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL`
Survives: a bare record confers no verdict (success rows satisfy neither REPRODUCED/DRIFTED nor the
UNREACHABLE failed-attempt rule). VERDICTS<47 as the item requires.

## (2) CAPTURE-ONLY — the 46 current byte-backed captures, refetch.tsv header only

rc=1 `SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL`
with 46/46 byte-backed triples noting `capture not the last successful attempt's bytes` (S105: no
bytes, no rows → MISSING). Survives: orphaned bytes give no verdict.

## (3) JUNK-PLUS — random-byte .raw×47 + recipe .txt + success rows naming junk shas

rc=1 `SET=47 VERDICTS=47/47 REPRODUCED=0 DRIFTED=47 UNREACHABLE=0 BYTE_BACKED=47 CONSISTENT=47/47 FLAGGED=0/47 C2=FAIL`
Exactly the claims' disclosed junk-forge shape and their JUNK control line. Survives via two
independent legs: REPRODUCED=0 < 5 (digest-bind holds — no preimage forge) and FLAGGED=0 < 47.

## (4) STALE-CAPTURE — disk bytes = earlier success, later success row names different bytes

Target S082 (ce16d57277fedfd4f0e7750e, REPRODUCED at baseline). Appended attempt-2 success row with
an unrelated sha256; disk left holding attempt-1 bytes. rc=1, per-triple line:
`CAPTURE S082 ce16d57277fedfd4f0e7750e pin=8e1f5bff76c1 MISSING capture not the last successful attempt's bytes`
`SET=47 VERDICTS=46/47 REPRODUCED=40 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=45 CONSISTENT=45/45 FLAGGED=0/0 C2=FAIL`
Survives: the stale triple gets no verdict, so VERDICTS<47.

## (5) FORGED-FLAG — DRIFTED triple with absent>0, flag line a/m vs counter's own counts

Same S082 converted to DRIFTED: junk raw+recipe txt on disk, appended success row naming the junk
shas; defined form holds none of its 2 pinned quotes → counter computes absent=2/2 (need_flag=1).

(a) lesson line `absent=1/2` (wrong a): rc=1
`SET=47 VERDICTS=47/47 REPRODUCED=40 DRIFTED=6 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/1 C2=FAIL`
Survives: mismatched a/m is not credited; FLAGGED<need_flag kills C2.

(b) lesson line `absent=2/2` (counter's own counts): rc=0
`SET=47 VERDICTS=47/47 REPRODUCED=40 DRIFTED=6 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=1/1 C2=PASS`
Survives per the item's letter — every other leg passes (REPRODUCED=40≥5, BYTE_BACKED=46≥32).
Calibration finding (reported, not patched): this is the claims' own disclosed gap made live —
DRIFTED is fetch-record-attested, not pin-bound, so swapping a REPRODUCED triple's committed bytes
to junk + extending refetch.tsv + emitting a count-matching FRESHNESS-FLAG prints C2=PASS. The
flag leg binds to nothing beyond the counter's own a/m; kill-rule integrity for DRIFTED rests on
the campaign actually running `capture-fetch.py`, which is outside counter scope by design.

## Notes

- Frozen predicate/targets/recipe unchallenged: all five forgeries fail or pass exactly where the
  frozen text and the pre-registered controls say they must; no counter, control or recipe edit
  proposed (frozen — findings only).
- Real-lane reads only (cp into scratch); no fleet-root or sibling-lane writes; lesson file absent
  in real lane at run time (fixtures create it inside the clone only).
- Siblings' live refetch rows/captures (S100/S103/S106 late successes, S134–S136 rc=28 retries)
  were present in the synced baseline; it still printed the committed 47/47 line.

VERDICT: attacked R57-C2's kill rule with five scratch forgeries (RECORD-ONLY, CAPTURE-ONLY,
JUNK-PLUS, STALE-CAPTURE, FORGED-FLAG wrong/match) — the frozen counter survived all five exactly
as specified; C2's only soft spot remains the claims-disclosed, record-attested DRIFTED leg.
