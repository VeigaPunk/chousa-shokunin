# R95RevenPrior — prior-art reverse engineering for C1 novelty

Seat: R95RevenPrior. Assignment: is C1's capability new? Reverse-engineer the
lane's existing search/sweep machinery at base
`7b2373586fb70f0ead6446c671fcc8b546d3e687`, answer (1) whether any base
instrument re-executes a recorded search expression or compares a recorded hit
count/hit set (cite file:line either way), (2) the original intent of the r5
sweep re-run and whether `corpus/README.md:398-399` still describes base
accurately, (3) run `bash tools/research-gate.sh verify-sweeps
corpus/fixtures/search-rerun-r95.md --root ..` at carrier C
`d27e9891ba6d2bae8b1f6060f7c01bf13a1a6ea1` and explain WHY it is CLEAN.

Scratch: `/fast/scratch/hyaku/chousa-r95/R95RevenPrior` (clones `repo` at base,
`repoC` at C, probe dir; removed before yield). Lane reads only; no lane
mutation. Receipts copied to `.ufo/waves/round-95/w1/R95RevenPrior-*.txt`.

## (1) No base instrument re-executes a recorded search expression, and none
## compares a recorded hit count or hit set

Base `tools/` (18 files, no `search-rerun.py`):
absent-split.py, argv-witness.py, assimilate-rows.py, build-spans.py,
capture-fetch.py, capture-text.py, claims-audit-v2.py, claims-audit.py,
digest-in-tree.py, freeze-check.py, gate-records.py, inference-ground.py,
lane-preflight.py, mechanism-witness.py, quarantine-check.py,
quote-reopen.py, receipt-pin.py, store-record-audit.py.

Nearest candidate, `tools/research-gate.sh verify-sweeps`
(base file `repo/tools/research-gate.sh`):

- Header contract (file line 149): "re-run: any glob hit is SWEEP_CLAIM_FALSE
  naming the hit (zero hits verify)." Per-item output vocabulary (line 158):
  `hits=… observed=verified|hit|exempt|refused|invalid` — `hits` is the count
  of paths matched by glob expansion (`hits=${#hit_list[@]}`, line 3056) and
  `observed=verified` is assigned on `hits=0` (line 3072). It is the number
  of *files that exist at the named location*, never a count of *search
  expression matches*.
- The swept `where` cell is tokenized (`sweep_where_tokens`, lines 2750-2777):
  a whitespace-free value is split on commas/semicolons into a path set; a
  value containing whitespace is read as a command/description and only
  *structured words* survive (URLs, source ids, path/glob-shaped tokens);
  every other word — including any search expression — is ignored
  (cf. header lines 168-171: "its structured words (URLs, ids, path/glob-shaped
  tokens) are extracted, other words ignored — so an r1-style
  `test ! -f lib/ghost.md` cell names lib/ghost.md").
- Which sections `verify_sweeps` reads: `Sources` (line 2880), any
  `*reject*` heading (lines 2900-2956), `Sweeps` (lines 2959-2963) or, when
  Sweeps is absent, `Negatives` with a where-like column (lines 2965-2971),
  and `Claims` kind=negative for the resolution check (lines 3100+). There is
  no reference to a `## Searches` section anywhere in `tools/` or in the
  r5 fixtures (`grep -rn "## Searches"` over `tools/` + `sweeps-r5*` → no
  hits), and `## Searches` (§23 of the R95 record) is never read — section
  parsing is generic (`load_sections` lines 830-877, `table_rows` line 878) so
  the section is *loaded* into `SEC_BODY`, but `verify_sweeps` only ever
  `table_rows`-reads `Sources/Rejections*/Sweeps/Negatives/Claims`.
- No other base tool re-executes a recorded expression: the only
  subprocess-spawning tool is `digest-in-tree.py` (subprocess.Popen line 98,
  sha256 over committed blobs); `gate-records.py` line 11 states it "never
  runs a mutating git command" (in fact it never spawns a command at all);
  the grep calls in the gate use pinned GNU grep `-P` for quote/anchor
  occurrence (`grep -a -z -b -o -P`, lines 1968/1997 — occurrence location of
  a quoted span, not re-running a stored search expression), and
  `grep -c` counts rows/sections in gate output (lines 955, 3905-3925,
  3965-3966, 4275-4277, 4627+), never a filed hit count.
- README's own summary of the mode (base `corpus/README.md:190-191`):
  "verify-sweeps checks rejection reason/flip-condition presence and re-runs
  each named local sweep location set as a glob/existence test (r5)" — an
  existence verdict, not a search replay.

Conclusion for C1's novelty sentence: the *capability* is new. Nothing at base
reads a `## Searches` table, executes its `expression` cell, or compares its
`hits`/`hit_set` cells; the claim's "nearest prior instrument" characterization
is accurate, and the gap (`search-rerun-record-r95.md`'s "execute half is
untouched", base README line 1108: "a record carrying the expression as run is
still not checkable") is as the recovery plan records it.

## (2) Intent of the r5 sweep re-run; README:398-399 still accurate at base

Original intent (`corpus/knowledge/sweeps-rejections-r5.md:32-44`, `:152-174`):
round 4 left kept rejections and negative sweeps unmeasured — a rejection
passed on a non-empty `reason`, a negative sweep on a non-empty `sweep` cell,
content never interpreted. Round 5 made them *verdict-bearing*: every
rejection needs reason AND flip-condition (else `SWEEP_REJECTION_INCOMPLETE`);
every negative sweep must name where it looked and local path sets are re-run
(glob hit ⇒ `SWEEP_CLAIM_FALSE`, zero hits verify); non-local sets stay
exempt-but-counted; naming nowhere drifts. The note is explicit and repeated
that the re-check is **location/existence only**: `:168-174` "The recorded
command is never executed, and its observed prose ('zero matches …') is never
compared… it cannot tell whether an empty location set is the right place to
have looked"; `:257-259` "The recorded command is never re-run … (design, not
debt): the re-check is a glob/existence test over the named locations."

README:398-399 (base, verbatim): "flip-condition presence is screened, not
quality (vacuity passes); the sweep re-run is a glob/existence check over the
named locations, never the recorded command; section absence is still r1's to
flag; and non-local sweeps stay exempt-but-counted." Every clause still
describes base exactly: re-verified this seat at base —
`verify-sweeps corpus/fixtures/sweeps-r5.md --root .` → `VERIFIED_SWEEPS=1/2
REJECTIONS_OK=3/3 RESEARCH_GATE: CLEAN` exit 0; `verify-sweeps
corpus/fixtures/sweeps-r5-broken.md --root .` → `SWEEP_REJECTION_INCOMPLETE` +
`SWEEP_CLAIM_FALSE`, `VERIFIED_SWEEPS=1/1 REJECTIONS_OK=0/1 RESEARCH_GATE:
DRIFT` exit 1 (`R95RevenPrior-sweep-base.txt`). The r5 note's open-items
residuals (vacuous flip passes; `VERIFIED_SWEEPS=0/0` CLEAN on a sectionless
record — `:251-256`) also still hold at base. No drift between the README
sentence and the base code.

## (3) Why `verify-sweeps` is CLEAN on `search-rerun-r95.md` at C

Command (from scratch `repoC`, carrier C `d27e9891…`):
`bash tools/research-gate.sh verify-sweeps corpus/fixtures/search-rerun-r95.md
--root ..` → exit 0, output (`R95RevenPrior-verify-sweeps-C.txt`):

```text
research-gate v2 — ts=… — mode=sweeps — record=corpus/fixtures/search-rerun-r95.md
VERIFIED_SWEEPS=0/0 REJECTIONS_OK=0/0
RESEARCH_GATE: CLEAN (sweeps=0 verified=0 exempt=0 hit=0 refused=0 invalid=0 rejections=0 rejections-ok=0 findings=0 drift=0)
```

Identical under `--root .` (`R95RevenPrior-verify-sweeps-C-rootdot.txt`).

Why, code path by code path (`verify_sweeps`, lines 2865-3136):

1. The record has no `## Sources` with declared pointers the mode needs, no
   `## Rejections`/`*reject*` heading (N_REJ=0), no `## Sweeps` section, and
   no `## Negatives` section. Its only `##` headings are `## As run` (§7) and
   `## Searches` (§23). The sweep-item loop finds SWEEP_ROWS empty
   (lines 2959-2971): `[[ -n ${SEC_BODY[Sweeps]+x} ]]` is false, so the
   `Negatives` fallback at line 2965 is not armed (line 2965's `&&` fails on
   `SEC_BODY[Negatives]` being unset), and the per-sweep loop never runs.
   N_SW therefore stays 0.
2. The negative-claim resolution loop (lines 3100+) reads `## Claims`, which
   the record does not have — skipped. No findings of any kind are emitted
   (FINDING_LINES stays empty), so ROLL never leaves CLEAN.
3. With N_SW=0, N_REJ=0 the CLEAN condition "verified+exempt = M and K = L
   and no finding drifts" is vacuously 0=0, 0=0 (header lines 163-165). The
   mode is *vacuously CLEAN on a record with no sweeps and no rejections* —
   the exact r5-note open item at `:251-253` ("A record with no `## Rejections`
   and no sweep rows at all closes `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=0/0`,
   CLEAN (measured)"). It does not read the `## Searches` section at all:
   lines 1364 (`table_rows Claims`), 1378/3093 (`table_rows Negatives`),
 1417/2665 (`table_rows Chain`), 1431 (`table_rows Rejections`),
 2959-2963/3071 (`table_rows Sweeps`), 1314/2887/3234 (`table_rows Sources`)
 have no `Searches` counterpart in the sweeps path (verified by grep: zero
 `Searches`/`expression`/`hit_set` reads in the sweeps region).

Corroborating probes (same C tree, scratch): a one-cell forgery of the R95
record (Q1's expression/hits replaced with `ZZZ`/999 — `R95RevenPrior-forged-f1.txt`)
also closes `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=0/0 RESEARCH_GATE: CLEAN` exit
0, and a nonsense record (`## Searches` with a junk table —
`R95RevenPrior-garbage.txt`) closes identically. For contrast, the r5 fixture
`corpus/fixtures/sweeps-r5.md` at C closes `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`
with two `SWEEP` and three `REJECTION` lines — the mode does work when given
its sections.

This confirms the C1 sentence's "accepts all 8 one-cell forgeries" arm — and
shows the reason is stronger than the sentence states: `verify-sweeps` accepts
*any* `## Searches` record, forged or not, trivially, because it never looks
at that section. The `PRIOR_ACCEPTED=8/8` arm of the battery is therefore not
evidence that a *similar* check was passed-and-missed; it is a vacuity
control — valuable as a do-nothing demonstration, but a reviewer should not
read it as the prior instrument having judged the searches and erred. The
honest reading, supported by (1) and (2): the new tool adds a section reader
and a re-execution the lane never had; the prior instrument is blind to the
record shape by design, and stays blind.

## Findings

- F1 (CONFIRMED, not a falsification): C1's novelty claim holds. No base
  instrument re-executes a recorded search expression or compares a recorded
  hit count/hit set. Citations: `tools/research-gate.sh:149,158,2750-2777,
  2865-3136,3056,3072`; `sweeps-rejections-r5.md:168-174,257-259`;
  `corpus/README.md:190-191,398-399`.
- F2 (HEDGE for the reviewer, not a falsification): `PRIOR_ACCEPTED=8/8` shows
  vacuity, not error. `verify-sweeps` returns `VERIFIED_SWEEPS=0/0 … CLEAN`
  exit 0 on the R95 record, on a forged copy, and on a junk `## Searches`
  record. The C1 sentence says the prior instrument "accepts all 8 one-cell
  forgeries the new tool refuses" — literally true, but the mechanism is that
  the prior instrument reads none of the record's sections, not that it
  judged the forgeries. Not a kill-rule hit (K2 is about the *new* tool
  accepting forgeries); flagged so the sentence is read at its true weight.
- F3 (NO FINDING): README:398-399 ("the sweep re-run is a glob/existence check
  over the named locations, never the recorded command") describes the base
  state accurately — re-measured at base (positive CLEAN 1/2+3/3, broken DRIFT
  with `SWEEP_REJECTION_INCOMPLETE` + `SWEEP_CLAIM_FALSE`) and confirmed in
  code (`sweep_glob_matches` 2845-2864 exists only as path existence/glob
  expansion; the tokeniser 2750-2777 discards expression text).

## Counter

| check | command | receipt | observed (line / exit) |
|---|---|---|---|
| base positive | `bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5.md --root .` @ base repo | `R95RevenPrior-sweep-base.txt` | `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3` / `RESEARCH_GATE: CLEAN`, exit 0 |
| base broken | `bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5-broken.md --root .` @ base repo | `R95RevenPrior-sweep-base.txt` | `FINDING SWEEP_REJECTION_INCOMPLETE` + `FINDING SWEEP_CLAIM_FALSE`, `RESEARCH_GATE: DRIFT`, exit 1 |
| C on R95 record | `bash tools/research-gate.sh verify-sweeps corpus/fixtures/search-rerun-r95.md --root ..` @ C repo | `R95RevenPrior-verify-sweeps-C.txt` | `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=0/0`, `RESEARCH_GATE: CLEAN (sweeps=0 … drift=0)`, exit 0 |
| C forgery blindness | same @ C, on forged copy (`R95RevenPrior-forged-f1.txt`) | — (same receipt line shape reproduced) | `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=0/0 RESEARCH_GATE: CLEAN`, exit 0 |
| C junk record | same @ C, on `R95RevenPrior-garbage.txt` | — | `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=0/0 RESEARCH_GATE: CLEAN`, exit 0 |

VERDICT: R95RevenPrior C1 held — no base instrument re-executes a recorded search expression or compares a recorded hit count or hit set, and verify-sweeps is CLEAN on the R95 record only vacuously (it never reads a ## Searches section).
