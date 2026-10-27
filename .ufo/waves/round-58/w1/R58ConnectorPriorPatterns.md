# R58ConnectorPriorPatterns — C1 counter and deletion history (rounds 49–57) against the frozen round-58 battery

Seat: R58ConnectorPriorPatterns (leaf, no subagents). Judged on operability. Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, HEAD `5da0a63`; freeze `9e73a03`; claim base `b13ca7b`.
Scope: cross-round pattern in C1 counter hardening and deletion hazards; whether `corpus/evidence/round58/c1-count.py` tests the prior lessons. Frozen files were read only. Probes ran on copies under `$S=/fast/scratch/hyaku/chousa-r58/R58ConnectorPriorPatterns/` (removed before yield). No install, no git/jj mutation, no live fetch. `tools/build-spans.py` is still the pinned r55 builder (`sha256 1ed2650a…`, same as `corpus/evidence/round58/controls/build-spans-r55.py`); no round-58 candidate exists to run.

## 1. Verified defect: the frozen counter cannot print `C1=PASS`

Every earlier C1 counter prints its verdict from a boolean: `round49/c1-count.py:397`, `round52:336`, `round53:376`, `round54:328`, `round55:476`, `round56/c1-gate.py:485`, `round56/c1-count.py:282`. Round 58 alone uses a case-mismatched token:
- `round58/c1-count.py:51` `PASS = "pass"`; refusal legs are built from it: `:160` `f"{name}={PASS}(refused)"`, `:223` (FOREIGN), `:234` (SYMLINK_OUT). They print `pass(refused)`.
- `:389-390` tests the ok legs with `"=pass"`. `:391` tests the refusal legs with `ref_pass = all(("=PASS" in l) for l in ref_legs)`, which never matches.
- `:399` (the summary count) also uses `'=PASS'`.

Runs (`$S/r58copy` = unmodified copy of `corpus/evidence/round58/`):
- **A** — `python3 -B $S/r58copy/c1-count.py --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py --work $S/runA --seed 7`
  ```
  EMPTY_OK=pass
  REBUILD_OK=pass
  FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
  SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
  SYMLINK_CACHE=fail(rc=0, expected refusal)
  FIFO_TXT=fail(rc=1, reason [...] absent in 'build-spans: refused S571: ...')
  DEVZERO_TXT=fail(rc=1, reason [...] absent in 'build-spans: refused S581: ...')
  FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: ...')
  MANY_QUOTES=fail(rc=0, expected refusal)
  ESCAPE_ENTRY=pass(refused)
  HELDOUT_OK=pass
  BEFORE_FOREIGN=deleted
  DENIED=0/0
  SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
  C1=FAIL   (EXIT=1)
  ```
  The lane receipt `corpus/evidence/round58/controls/c1-controls.txt` (commit `718e8d2`) shows the same `REFUSE=0/7 … C1=FAIL` and does not remark on it.
- **B** — same counter, builder `$S/forge.py` (27 lines, scratch). It delegates to the base builder, except that it refuses by basename of `--quotes`/`--out` (`quotes-few.tsv`, `out-link`, `quotes-9.tsv`, `quotes-7.tsv`, `quotes-8.tsv`, `quotes-5.tsv`, `quotes-many.tsv`) with the reason words the counter accepts. It writes nothing.
  ```
  EMPTY_OK=pass
  REBUILD_OK=pass
  FOREIGN=pass(refused)
  SYMLINK_OUT=pass(refused)
  SYMLINK_CACHE=pass(refused)
  FIFO_TXT=pass(refused)
  DEVZERO_TXT=pass(refused)
  FAT_RAW=pass(refused)
  MANY_QUOTES=pass(refused)
  ESCAPE_ENTRY=pass(refused)
  HELDOUT_OK=pass
  BEFORE_FOREIGN=deleted
  DENIED=0/0
  SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
  C1=FAIL   (EXIT=1)
  ```
  All seven refusal legs pass. The verdict still fails.
- **C** — `$S/r58fixed` is a scratch copy with one line changed: `:391` → `ref_pass = all(("=pass" in l) for l in ref_legs)`. The base builder gives `C1=FAIL` (EXIT=1). Forge B gives the same leg block as above, then `C1=PASS` (EXIT=0).

So: with the frozen counter as written, `C1=PASS` is unreachable for any builder. Once that one token is corrected, a 27-line name-keyed forge with no refusal logic passes the whole predicate. This is a probe of the counter, not a fix. The lane copy is unchanged.

## 2. Cross-round pattern: counters forged through fixed inputs

Each round's counter was passed by a tool that read a fixed input (replay, literal string, digest, dir name, XML spelling, sibling file, or the record itself):

| round | lesson row | forge class | recorded fix | round-58 status |
|---|---|---|---|---|
| 49 | `corpus/lessons/round-49.md:21` | replay of golden outputs | perturbed-input leg, round 50 | no perturbed leg |
| 50 | `round-50.md:19` | `--selftest` compared as sets (duplicate line passed) | multiset compare | n/a (build-spans) |
| 51 | `round-51.md:15` | six literal DIFF lines recognised | nonce packages | n/a |
| 51 | `round-51.md:22` | work dirs named `s`, `d1`; tool keys on `--out` name | round-52 routed item, `round-52.md:25`: "make the next counter nonce-only with no fixed directory names" | **regressed** (below) |
| 52 | `round-52.md:16` | regex keyed to generator XML spelling | representation supplement | no representation leg |
| 53 | `round-53.md:19` | canned REAL by pinned digest | none in-round | HELDOUT_OK keyed on URL, capture key, 3 quotes |
| 54 | `round-54.md:17` (RW-1) | sibling HTML read, canned REAL by digest | supplement | same shape as 53 |
| 56 | `round-56.md:9` | alternating tool forges the kill rule | multiset / order | n/a (gate) |
| 57 | `round-57.md:97` | refetch record self-attested, C3 PASS | disclosed as limit | n/a |

The round-52 rule was implemented in round 56: `round56/c1-count.py:122` `w = self.work / secrets.token_hex(8)` per run. Round 58 reintroduces literal names. Every leg identity is a basename or URL the builder receives:
- output dirs: `out-empty` (`round58/c1-count.py:193`), `out-link` (:229), `out-9` (:247), `out-7` (:259), `out-8` (:274), `out-5` (:292), `out-many` (:303), `out-esc` (:311), `out-heldout` (:341), `out-before` (:351);
- quote files: `quotes-few.tsv` (:214), `quotes-9.tsv` (:245), and the rest of the `quotes-*.tsv` set;
- URLs: `https://fixture.example/doc1|7|8|9|5` (:186, :243, :255, :270, :285); seed default `7` (:168).
Only the parent `--work` is random (:174).

## 3. Deletion and containment hazards

**3a. Orphan unlink is old and was never tested by a counter.** `corpus/evidence/round49/build-spans.py:195` `p.unlink()` runs over `spans/S###-N.txt` not in the new file set, before the writes. The same loop is in the lane builder (`tools/build-spans.py:205`, unchanged since the r55 pin). Grep of round49–56 counters for foreign/orphan/S777 finds no build-spans leg (round55, round56, c1-gate contain none). `round49/c1-count.py:172` `dst.unlink()` belongs to `assimilate-rows`. The round-58 FOREIGN leg (`round58/c1-count.py:209–224`) is the first. Probe A shows the base deletes (`orphans deleted: foreign gone=True`).

**3b. Refusal legs do not measure partial writes.** The FOREIGN leg checks rc≠0, that `S777-1.txt` survives, and a reason substring. `expect_refuse(..., [])` at :250, :263, :278, :295, :306 forbids nothing. Probe E (`$S/partial.py`: on `quotes-many.tsv` it writes `spans.tsv` and `spans/S900-1.txt` into `--out`, then exits 1 with `SIZE ROWS CAP`; all other calls delegate):
```
python3 -B $S/r58copy/c1-count.py --builder $S/partial.py --work $S/runE2 --seed 7
MANY_QUOTES=pass(refused)
C1=FAIL   (EXIT=1)
```
`runE2/out-many/` holds `spans.tsv` and `spans/S900-1.txt`. `round58/claims.md:7` states "without partial writes"; this leg does not check it.

**3c. The counter deletes an existing `--work`.** `round58/c1-count.py:175-176` `if work.exists(): shutil.rmtree(work)`. Probe F (base builder, `--work $S/victim` holding `keep.txt`): `keep.txt present? no`. The frozen command says "fresh-absolute-dir", so only misuse triggers this. The round-56 counter refuses a non-empty `--work` (`round56/c1-count.py:161-162`, `usage: --work must be empty`); the guard was dropped in round 58. I did not run the counter against the lane.

**3d. Ok legs ignore the file set.** `got` (:120) and `want` (:122) are built and never compared. Probe D (`$S/extra.py`: base builder plus stray `spans/zz-extra.txt` on `out-empty`):
```
EMPTY_OK=pass
REBUILD_OK=pass
C1=FAIL   (EXIT=1)
```

## 4. Lesson-named hazards the frozen battery does not reach

- **Zip inflation** (`round-52.md:19`, row 6: 1 MB deflated → 1 GiB text; `524,901`-byte package → `360,000,113` bytes). No zip leg: `grep -c -i 'zip\|inflat' round58/c1-count.py` → `0`. FAT_RAW (:282–295) tests raw file size only. The lane's inflation bound (`tools/capture-text.py:78` `MAX_PART = 256 MiB`) is not exercised by any frozen leg.
- **Duplicate-occurrence quote and zip branch** (`round-55.md:34`, named as uncovered by the round-55 counter). The battery forces unique quotes (:94–96, :331–335); no duplicate-occurrence leg exists. Round 56's battery mutates the gate, not the builder (`round56/claims.md:59`, "frozen mutants M1-M9 of G").
- **DENIED is off by default.** The frozen predicate command has no `--controls`, so `DENIED=0/0` (Probe A). The do-nothing clause binds only when a controls dir is passed (`:365`). The docstring (`:10`, `:169`) names NAIVE; the code (`:366`) checks only `REFUSEALL.py` and `build-spans-r55.py`; `controls/` has no NAIVE.
- **Crash instead of verdict.** First attempt at Probe E (builder that fails EMPTY_OK): `Traceback … File "…/r58copy/c1-count.py", line 212, in main … FileNotFoundError: …/runE/out-empty/spans/S777-1.txt`, EXIT=1, no `C1=` line. Denial by absence.

## 5. Does the frozen round-58 battery test the prior lessons?

| prior lesson | frozen R58 status |
|---|---|
| forge through fixed inputs (R49, R51, R52, R53, R54) | not tested; fixed names/URLs/seed (§2); Probes B and C |
| routed rule "nonce-only, no fixed directory names" (R52) | violated (§2) |
| counter defect hidden from its own legs (R50 row 19; R51 rows 5, 8) | new defect (§1): no leg checks the verdict token |
| orphan deletion (builder since r49) | tested for S777 only; any refusal reason words pass it (§3a) |
| partial writes on refusal | not tested (§3b) |
| `--work` containment (R56 guard) | removed; existing dir deleted (§3c) |
| inflation bound (R52 row 6) | not tested (§4) |
| duplicate-occurrence, zip branch (R55 line 34) | not tested (§4) |

## 6. Proposed patch (report only; not applied)
1. `:391` and `:399`: use one lowercase token form for all legs and the summary.
2. Per run: `secrets.token_hex(8)` for every output dir, quote file, and fixture host (`fixture-<hex>.example`); random seed when `--seed` is absent, printed in the receipt.
3. Refusal legs: snapshot `work` before and after; require no new or changed file under `out`, no `spans.tsv`, and no change outside `out`; FOREIGN bytes identical.
4. Ok legs: compare `set(got)` against `want` (the existing dead comparison).
5. Add legs: zip main part inflating past 256 MiB (refused, no partial output); duplicate-occurrence quote (refused); a basename-keyed forge control that must print `C1=FAIL`.
6. Wrap each leg so an exception still prints `C1=FAIL`; refuse a non-empty `--work`.
Verification if landed: rerun A, B, C, D, E, F and the new controls; expect A, B, D, E, F to show the stated defects on the frozen copy.

## 7. Checks not run / limits
- No round-58 candidate builder exists in the lane (`tools/build-spans.py` is the r55 pin); no candidate-level run.
- No C2 run. No lane file edited. No install, no pacman, no live fetch.
- Round-58 sibling seat reports (`R58ConnectorFrontier.md`, `R58ConnectorSiblingScope.md`) were not read; out of this seat's scope.
- Probe outputs are copied verbatim above; scratch is removed after this report.

VERDICT: falsified — the frozen C1 counter (`corpus/evidence/round58/c1-count.py`) does not test the round 49–57 forge and deletion lessons. Concrete attacks: (a) its verdict token is case-mismatched (`:51`/`:391`), so `C1=PASS` is unreachable (Probes A, B: seven `pass(refused)` legs, `REFUSE=0/7`, `C1=FAIL`); (b) with that single token corrected in a scratch copy, a 27-line basename-keyed forge with no refusal logic prints `C1=PASS` (Probe C). Also observed: `--work` deletion (§3c) and no partial-write check (§3b). The C1 verdict on the builder itself is not decided here.
