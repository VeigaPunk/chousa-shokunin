# R57W1CritC3Stray — attack on the STRAY_IDS leg and id regexes of c3-count.py

Seat: critic (leaf). Frozen claim: R57-C3 at lane commit fd95724d56a33a150cd2638fadd2ce1f3425e6c (c3-count.py frozen).
No lane/fleet writes; all runs against synthetic fixture roots via `c3-count.py --root` (git legs read the lane read-only).
Scratch: /fast/scratch/hyaku/chousa-r57/R57W1CritC3Stray (deleted on yield — see trap note at bottom).

## Target code (frozen, cited for the attack only)

- `corpus/evidence/round57/c3-count.py:85` — `ID_RE = re.compile(r"\bS\d{3,}\b")` (uppercase S, 3+ digits, word-bounded).
- `:272` — `stray = sorted({i for i in ID_RE.findall(entry) if i != "S127" and i not in bound_ids})` — scans the ENTRY only.
- `:284` — `ok = ... and not stray` — any stray token forces C3=FAIL; `STRAY_IDS` printed at `:281`.
- `bound_ids` (:248) = registry rows to which some Rk bound via the REFS loop; `EXCLUDED = {"S127","S128","S129"}` (:47) can never bind (candidate loop `:238` skips them), so S128/S129 can never enter `bound_ids`.

## Method

Built a synthetic fixture root (fabricated lane-owned captures, refetch rows, registry rows S901/S902/S131/S903
`mined 2026-10-27`, spans built by the lane's own `tools/build-spans.py`, entry/lesson with real quotes) that
makes every non-stray leg pass, so each mutation isolates the stray leg. Baseline:

```
$ python3 corpus/evidence/round57/c3-count.py --root $SCRATCH/fixture
BOUND=4/7 (min 4) R1:S901 R3:S902 R4:S131 R7:S903   SWEPT=3/3 R2 R5 R6
QUOTE_ROWS=9 IN_SPAN=9 IN_ENTRY=9 IN_LESSON=9 SHORT=9 CONTEXT=9 CAPTURE_BOUND=9
SUBSTANCE=PASS ANCHOR_BOUND=4/4 INFERENCE_GROUNDED=yes STRAY_IDS=-
C3=PASS   exit=0
```

Five entry mutations were run (each = baseline + one prose line); only the added line differs between runs.

## Isolated regex probes (python3, same pattern as :85)

```
'S128'->['S128']  'S1300'->['S1300']  's128'->[]  'S131'->['S131']  'S1271'->['S1271']
'S127'->['S127']  'XS128Y'->[]  'S1271X'->[]  'S12'->[]  '(S128)'->['S128']
search("see S1271 now") -> span (4,9) = 'S1271'   # never decomposes to S127: \b fails between '7' and '1'
```

## Findings

(1) `S128` in prose → stray → FAIL.  Case line added: `Note: S128 also discusses this clause in passing.`
    `STRAY_IDS=S128`, C3=FAIL, exit=1; every other print identical to baseline. Survives: the leg is live and
    catches any uppercase non-bound id, even though S128 is excluded only from BINDING, never from mention.
    Corroborated by the shipped controls (`controls/c3-controls.txt`: HELD `STRAY_IDS=S130`, CITER
    `STRAY_IDS=S130,S990` — both fail partly on this leg).

(2) `S1300` → stray → FAIL.  Added `Note: S1300 was consulted as a later index.`
    `STRAY_IDS=S1300`, C3=FAIL, exit=1. Survives: `\d{3,}` is greedy, matches the whole 4-digit token;
    the word boundary after the final digit holds; the whole token is then tested against the exemption.

(3) lowercase `s128` → NO match → **C3=PASS — hole (false PASS)**.  Added `Note: lowercase s128 was consulted...`
    Result: `STRAY_IDS=-`, C3=PASS, exit=0 — every leg identical to baseline. The frozen predicate sentence says
    "no `S###` token in the entry names a row other than S127 or a bound row"; a lowercase `s128` still names
    row S128 to any reader, but `ID_RE` is case-sensitive so the counter is blind to it. Coverage check of the
    other legs: the stray scan reads only the entry (:272); `tools/inference-ground.py` also uses
    `\bS\d{3,}\b` (its line 80) and I ran it directly on the mutated entry — exit 0 (it never looks at prose
    outside `#### Inference`); a second mutation putting `s128` as its own `#### Inference` bullet gave
    `INFERENCE_GROUNDED=no` (the bullet cites no id) yet `STRAY_IDS=-` still — the grounding rule catches it
    only incidentally, only inside Inference bullets, and only while it is the bullet's sole "cite" (a bullet
    citing S127 plus `s128` would pass both). So outside Inference prose, nothing catches it. Smallest safe
    correction (for any future re-freeze; NOT proposed as a change here): compile the leg's pattern with
    `re.IGNORECASE` while reporting the matched token verbatim. Reported, not patched, per the freeze rule.

(4) `S131` bound id in prose → fine → PASS.  Baseline already binds R4:S131 and cites `source: S131 — ...`;
    mutation added `The R4 binding comes from S131 in this fixture.` → `STRAY_IDS=-`, C3=PASS, exit=0.
    Survives: exemption is `bound_ids` membership (row actually bound through the REFS loop), not mere registry
    presence — a bound id may be mentioned anywhere in the entry, prose included.

(5) `S1271` → stray → FAIL.  Added `Cross-ref S1271 for a later draft revision.`
    `STRAY_IDS=S1271`, C3=FAIL, exit=1. Survives: the S127 allowance is exact-string (`i != "S127"`, :272) and
    the regex consumed the full token `S1271`, so a 4-digit neighbour of an allowed id is still stray. Direction
    is fail-closed (a false FAIL is possible only if S1271 names no registry row at all, in which case the entry
    gains nothing by mentioning it) — safe side for a counter.

## Notes on scope

- The leg scans the entry only; lesson/registry lowercase or uppercase mentions are outside the predicate's text
  ("in the entry") and were not attacked.
- `S12` (two digits) does not match :85 and is not an `S###` token — no predicate conflict.
- All six fixture runs are reproducible from `build_fixture.py` (scratch copy, deleted on yield); the frozen
  counter was never edited and no lane bytes were written.

## Hygiene

No tools installed or upgraded (none needed). Scratch dir removed via `trap 'rm -rf -- "$S"' EXIT` on shell exit;
fixture+mutations lived only under /fast/scratch/hyaku/chousa-r57/R57W1CritC3Stray. TMPDIR/PYTHONDONTWRITEBYTECODE
set for all runs. Only write: this report.

VERDICT: attacked the STRAY_IDS leg (`c3-count.py:85,:272,:284`) and its `\bS\d{3,}\b` id regexes with five
synthetic entry mutations against a fully-passing fixture — cases (1)(2)(4)(5) behave exactly per the frozen
predicate (survive); case (3) lowercase `s128` is a confirmed false-PASS hole the frozen counter cannot see,
reported per the freeze rule.
