# Round 81 — R81ExecRepro (fleet executor, reproducer)

Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Base `378fda82dc2cbcc555a0565052cc408121813cef` · prefreeze controls `f7929f877e6fd54f4dc5ce7f993da46bc7df43f9` ·
claims freeze `bb54e7f89da9ba4213aec9d976c13f3f4ba548fb` · candidate `7e2da96a0541946e796384d42fea18e09ede9e9f`.
Frozen predicate set read first: `corpus/evidence/round81/claims.md`.
Scratch `/fast/scratch/hyaku/chousa-r81/R81ExecRepro/` (created with `mkdir -p`, deleted before yield; every cited receipt was
copied into this output folder first). No network: my item names no re-open, so C1 K2 (live re-open) is out of my grant.
Tool installs: none. Lane/fleet git state: untouched (read-only `git show` / `git archive` / one `git clone` of the lane into
scratch; `git -C "$S/repo-prefreeze" rev-parse --show-toplevel` printed the clone, never the lane).

All receipts below are in `.ufo/waves/round-81/w1/R81ExecRepro/`.

---

## 1. Instrument identity — HELD (8/8)

Commands: `git -C <lane> show <rev>:<path> | sha256sum` for the three instruments and five fixtures at each of the three
revisions. Receipt: `a2-instrument-identity.txt`.

| instrument | sha256 | pin (claims.md) |
|---|---|---|
| `depth-r81.py` | `10c989c0a59f94d88e03b0972378fd178bc6ee62e55bb580998751c3f2daa1e9` | `10c989c0a59f94d88e03b0972378fd178bc6ee62e55bb580998751c3f2daa1e9` ✓ |
| `checklist-run.py` | `66ca8c97c597f4b4b538322654e98f1ca83ebdde3b5d44c2b5d0bd63f295bbc2` | `66ca8c97…295bbc2` ✓ |
| `run-controls.sh` | `c1942bb92fc4901efcc8e82a8679c1d776fc0061f012c39afd4ea331f27ea65c` | `c1942bb9…7ea65c` ✓ |
| item2-pass | `d9f1aa511e8b94c328982b05b6316022ab2c87a37a863817d8d0953a5eec959e` | `d9f1aa51…` ✓ |
| item2-fail | `5f9b89d1c011a094a7a384c88549735751add2a6c566ba9e72074dde33ad6f79` | `5f9b89d1…` ✓ |
| item4-pass | `64183e4789b7729b40043e018973ade6d03da9f610acc47fd9baf01bfbd8d682` | `64183e47…` ✓ |
| item4-fail | `b7a45309c6610cc0371f93d7b654f2074ad78732ca2d75d140a02a03e2b4135b` | `b7a45309…` ✓ |
| item5-fail | `bf53d570aa95af9a2b59c37c6be8547a8b88733b0cc77be676c005284227f3b0` | `bf53d570…` ✓ |

All eight hashes are identical at `f7929f87`, `bb54e7f8` and `7e2da96a`; the fixture pins are truncated to 8 hex chars in
claims.md and match on those prefixes. `tools/research-gate.sh` (the program the C2 Run lines execute) is
`d5d48128509f77edf161e4d8b10b833e6e00f822906460fa049f27d1244d41e2` at both base and candidate (`e1-attack-provenance.txt`).

## 2. BEFORE at base `378fda82` — reproduced exactly

Tree: `git -C <lane> archive 378fda82 | tar -x -C <scratch>/base` (19 436 files, `corpus/knowledge/` = 92 files).

| cmd | observed | rc | receipt |
|---|---|---|---|
| `python3 -B <lane>/corpus/evidence/round81/depth-r81.py --root <scratch>/base` | `DEPTH_R81 entries=0 fresh_rows=0 located_quotes=0` / `DEPTH_R81=FAIL` | **1** | `b1-depth-before-lanecopy.txt` |
| `python3 -B <lane>/corpus/evidence/round81/checklist-run.py --root <scratch>/base` | `CHECKLIST_RUN=3/6 DISCRIMINATE=0/3` / `CHECKLIST=FAIL` (items 2, 4, 5 `runnable=no … no-run-line`) | **1** | `b2-checklist-before-lanecopy.txt` |

Both equal the frozen expectation. The base tree carries no `corpus/evidence/round81/` at all, so a tree-copy run is
n/a at base (counters are introduced at prefreeze).

## 3. AFTER at candidate `7e2da96a` — predicate holds, both counters

Tree: `git archive 7e2da96a | tar -x -C <scratch>/cand` (19 479 files, `corpus/knowledge/` = 94).

| cmd | observed | rc | receipt |
|---|---|---|---|
| `python3 -B <lane>/corpus/evidence/round81/depth-r81.py --root <scratch>/cand` | `ENTRY citation-searching-tarcis-r81.md counted=yes reason=all-pass`; `ENTRY correction-retraction-status-r81.md counted=yes reason=all-pass`; `DEPTH_R81 entries=2 fresh_rows=5 located_quotes=14` / `DEPTH_R81=PASS` | **0** | `c1-depth-after-lanecopy.txt` |
| `python3 -B <lane>/corpus/evidence/round81/checklist-run.py --root <scratch>/cand` | items 2/4/5 `runnable=yes leg=pass`; `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3` / `CHECKLIST=PASS` | **0** | `c2-checklist-after-lanecopy.txt` |

Run from the archived tree's own instrument copy (`python3 -B <scratch>/cand/corpus/evidence/round81/{depth-r81.py,checklist-run.py}
--root <scratch>/cand`), the output is **byte-identical** to the lane-copy run, stdout and rc (receipts
`c3-depth-after-treecopy.txt`, `c4-checklist-after-treecopy.txt`; `diff` of the two pipelines printed nothing). The only
difference between lane-copy and tree-copy is that the tree copy also takes its fixtures from the archived tree — which are
the pinned bytes (item 1 above).

Independent recomputation of the P2 fetch binding (`a6-c1-capture-bindings.txt`): for S203–S207 the `sha256(URL)[:24]`
capture key, the capture file's sha256, `refetch.tsv` `curl_rc=0`/`http=200`/`fetched_utc=2026-11-06T18:44:29Z–31Z` and the
`txt_sha256` column all agree (5/5 `MATCH`); each row is `mined`, `opened=2026-11-06`, `used_by` names its entry.
Novelty check (`a5-c1-novelty.txt`): `tarcis` = 0 files in the base knowledge set; `retract` = 0 files; the 16 base files
containing the word `erratum` use it in the lane's "round-N erratum" sense (e.g. `audit-r11.md` §6 erratum) and none is a
title about publication-erratum linking. S203–S208 are absent from the base registry and present at candidate
(`a4-c1-registry-and-set.txt`), S208 as `rejected` with its flip condition.

## 4. Control driver rerun from the prefreeze revision — 16/16 reproduce

**The instruction as literally worded cannot run.** `run-controls.sh` derives `LANE=$(cd "$(dirname "$0")/../../.." && pwd)`
and first does `git -C "$LANE" archive "$BASE"`; a `git archive` tree has no `.git`, so every `snap()` yields an empty tree
and the driver still exits 0 while emitting rc=2 receipts. Receipt: `d0-archive-driver-fails.txt` (observed
`fatal: not a git repository`, `DEPTH_R81 error: no corpus/SOURCES.md under --root`, `rc=2`). Reproduction therefore used a
git clone of the lane checked out at `f7929f87` (`git clone --no-hardlinks <lane> <scratch>/repo-prefreeze && git -C … checkout
f7929f87`; toplevel assertion printed the clone; `run-controls.sh` there is byte-identical to the pin, `c1942bb9…`).

```
HYAKU_SCRATCH=/fast/scratch/hyaku bash <scratch>/repo-prefreeze/corpus/evidence/round81/run-controls.sh \
  378fda82dc2cbcc555a0565052cc408121813cef <out>/controls-rerun
```

Driver rc = 0; all 16 controls returned their pinned rc (`k0` 1/1, `c1-pos` 0, f1–f7 1, `c2-pos` 0, g1/g2/g3/g5 1, g4 2).
`d-controls-diff-summary.txt`: after stripping `# cmd:` lines (the only line that differs — it names the clone rather than the
lane) **16/16 receipts are byte-identical** to `corpus/evidence/round81/controls/`, and so is the emitted
`c2-candidate-SKILL.md` (`cmp` clean).

**Does this make any control depend on uncommitted bytes? No.** `d1-uncommitted-dependency.txt`: for the six paths `snap()`
copies out of the working tree (`refetch.tsv` + five captures), worktree = candidate = prefreeze hashes, and
`git status --porcelain` on the relevant paths is empty. The dependence is on bytes **committed at prefreeze and candidate
but absent from base** (all five captures are missing at `378fda82`; `refetch.tsv` is 145 rows there vs 151). The k0 verdict
is not affected by that: `depth-r81.py` on the *pure* base archive prints the same `DEPTH_R81=FAIL`, rc=1 (§2).

## 5. Kill-rule probes

**C1 K2 (live re-open): n/a for this seat** — my item names no re-open and the egress table grants none.

**C1 K3 (decision-table row contradicted by its cited located quote): no firing found by reading.** Both counted entries'
decision tables were read against their located quotes. Entry 1's rows track rec 2/9/6/7/8 verbatim in substance; its last row
cites S208 (rejected, unreachable) and labels itself `lane inference`. Entry 2's rows track S205/S206/S207 in substance. Two
rows go *beyond* their quotes without contradicting them (entry 1 row 6 enumerates items the located fragment does not list;
entry 2 row 3 reads "a newer version exists" as "superseded wording"). Recorded as a reading, not as a K3 firing.

**C2 K2 (item-text defect passes the landed Run line): FIRED for items 2 and 4.** Method: the harness extracts the landed
`Run:` line **verbatim** from the candidate tree's `SKILL.md`, replaces its first `<…>` placeholder with a record derived
from the frozen pass fixture by changing exactly one cell, and runs `bash -c` with cwd = the archived candidate tree — the same
mechanics `checklist-run.py` uses. Receipts: `c2-k2/*.txt` (command, record, cwd, full output, rc), summary
`c2-k2/attack-summary.txt`.

| variant | defect (item text) | rc | observed |
|---|---|---|---|
| item4 flip `-` | kept rejection, no flip-condition | **0** | `REJECTION id=R1 … reason=present flip=present observed=complete verdict=match` / `RESEARCH_GATE: CLEAN` |
| item4 flip `n/a` | same | **0** | `flip=present … verdict=match` / `CLEAN` |
| item4 flip `TBD` / `none` | same | **0** | `flip=present` / `CLEAN` |
| item4 reason `-` | kept rejection, no reason | **0** | `reason=present` / `CLEAN` |
| item4 flip `` (empty) — CONTROL | same | 1 | `SWEEP_REJECTION_INCOMPLETE … missing=flip` / `DRIFT` |
| item2 where `n/a` | negative claim, sweep names nowhere | **0** | `SWEEP id=W1 where=n/a looked=local hits=0 at=- observed=verified verdict=match` / `CLEAN` |
| item2 where `N/A`, `x/y` | same | **0** | `looked=local … verdict=match` / `CLEAN` |
| item2 where `S1` | sweep names a source id, no location | **0** | `looked=source-ids … observed=exempt verdict=exempt` / `CLEAN` |
| item2 where `` (empty) — CONTROL | same | 1 | `SWEEP_LOCATION_ABSENT` / `DRIFT` |

Mechanism, read in `tools/research-gate.sh`: `sweep_flip_cell`/the reason check accept **any non-empty cell** (`-`, `n/a`,
`TBD`, `none`, `?`, `...`, `—` all read `present`), and `sweep_token_class` classifies **any token containing `/`** as a local
path (`sweep_looks_path`), so `n/a` is expanded as a glob, matches nothing, and is counted `verified` — a sweep naming `n/a`
is reported as a verified zero-hit location. The frozen fixtures only exercise the *empty-cell* spelling of both defects, so
`CHECKLIST_RUN=6/6 DISCRIMINATE=3/3` is true while the Run lines do not produce their stated outcomes on the item-text defect
in these placeholder forms. Weaker, same family (not claimed as the rule's target): `where` = `external`, `https://…` →
`exempt` → CLEAN.

## 6. Findings

1. **C2 K2 firing (items 2 and 4).** Command, receipt and observed line per row in §5 / `c2-k2/*.txt`; rc=0 on records whose
   only defect is the one the item text names. The SKILL.md's own stated outcome for item 4 ("a kept `## Rejections` row
   without a reason or a flip-condition is `SWEEP_REJECTION_INCOMPLETE`, exit 1") is contradicted by rc=0 on `flip=n/a`.
   Adjudication is the L1's: the frozen rule says "an attack seat", and I am the reproducer seat — the measurement is mine,
   the role question is not.
2. **Instruction (d) is not executable as written** — the driver needs a git repo, not a `git archive` tree (§4); the
   reproduction used a clone checkout at the same revision with the same driver bytes.
3. **Controls depend on post-base committed bytes**, never on uncommitted ones; the k0 verdict is invariant to that (§4).
4. Everything else in the frozen set reproduces: identity 8/8, before 2/2, after 2/2 (and tree-copy identical), controls 16/16.

## 7. Risks and limits

- C1 K2 (live re-open) and the S203 PDF re-open are outside my grant; the C1 grounding rests on committed captures whose
  bindings I recomputed but did not re-fetch.
- The C2 attack uses records I authored; it measures the landed Run lines, not the lane's real records. A record with a real
  flip-condition in a dash-heavy table style is indistinguishable to the gate from one with `-` in the cell.
- The counter `checklist-run.py` is by design blind to this class (frozen fixtures only); the finding is against the C2
  claim's Run lines, not against the counter's arithmetic, which I reproduced exactly.

VERDICT: R81ExecRepro C1 held — depth-r81.py prints `DEPTH_R81=PASS` entries=2 fresh_rows=5 located_quotes=14 rc 0 at 7e2da96a and FAIL rc 1 at base, and no C1 kill rule fired on my surface (K2 not granted, no K3 contradiction found).
VERDICT: R81ExecRepro C2 fired — the predicate reproduces (`CHECKLIST_RUN=6/6 DISCRIMINATE=3/3` rc 0, controls 16/16 byte-identical) but kill rule K2 fires: the landed item-4 Run line exits 0 on a kept rejection whose flip_condition cell is `-`/`n/a`/`TBD`/`none`, and the landed item-2 Run line exits 0 on a sweep naming `n/a` (classified as a local glob, `hits=0`, `verified`), receipts `c2-k2/item4-flip-*.txt`, `c2-k2/item2-where-nxa.txt`.
