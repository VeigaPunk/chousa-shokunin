# R58ExecC1MutationFixture — round-58 C1 fixture-harness seat

**Lane** `/home/vgpnk/Projects/shokunin/chousa-shokunin` · **HEAD** `5da0a6375a554e1229492a8cb0b9695bd8e85456`
**Freeze** `9e73a031ab1ac3bac343de008850d7d87f9e5634` · **Claim base** `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`
**Scratch** (all artifacts; removed at yield) `/fast/scratch/hyaku/chousa-r58/R58ExecC1MutationFixture/`

## What I built

A scratch-only deterministic fixture harness for the C1 battery — 4 safe/rebuild legs (`EMPTY_OK
REBUILD_OK HELDOUT_OK ESCAPE_ENTRY`) + 8 refusal legs (`FOREIGN SYMLINK_OUT SYMLINK_CACHE FIFO_TXT
DEVZERO_TXT DEV_TXT FAT_RAW MANY_QUOTES`). It **independently reimplements** the leg semantics frozen in
`corpus/evidence/round58/c1-count.py` and never reads that counter at runtime. Scratch-only inputs: pinned
copies of `tools/capture-text.py` (sha `2c0140bc…2573`) and `captures/6dc68fd6b32ce9c8dfcebce8.raw` (sha
`6063a3af…df3`) plus scratch-local synthetic fixtures. No network, no `/tmp`, no lane mutation. Subject
`tools/build-spans-hardened-ref.py` (sha `2f0a0fa1…73e6`) is **my scratch reference implementation** of the
claims.md C1 semantics, so the battery has a subject satisfying every leg; scratch only, not a candidate.

```
$ python3 fixture_harness.py --builder tools/build-spans-hardened-ref.py --work .../work-ref2 --label REF2
[REF2] EMPTY_OK=pass            [REF2] REBUILD_OK=pass          [REF2] HELDOUT_OK=pass
[REF2] ESCAPE_ENTRY=pass(refused)
[REF2] FOREIGN=pass(refused)   [REF2] SYMLINK_OUT=pass(refused)  [REF2] SYMLINK_CACHE=pass(refused)
[REF2] FIFO_TXT=pass(refused)   [REF2] DEVZERO_TXT=pass(refused)  [REF2] DEV_TXT=pass(refused)
[REF2] FAT_RAW=pass(refused)    [REF2] MANY_QUOTES=pass(refused)  [REF2] SUMMARY SAFE=4/4 REFUSE=8/8
[REF2] HARNESS=PASS   EXIT=0
```
Exact run printed one leg per line, paired into columns here (no value changed); determinism: two identical runs →
byte-identical output (`diff d1.txt d2.txt` → IDENTICAL).

## Defect 1 (blocking) — the frozen counter can never print `C1=PASS`

`c1-count.py:51` defines `PASS = "pass"` (lowercase) and every refusal leg is emitted lowercase
(`expect_refuse` `:160`, `FOREIGN` `:223`, `SYMLINK_OUT` `:234`), but the verdict gate **`:391`** tests
`all(("=PASS" in l) for l in ref_legs)` — **uppercase**; `:399`'s `REFUSE=` summary has the same bug. So
`ref_pass` is `False` for *every* builder → verdict always `FAIL`, exit always 1 (safe legs survive only because
`:390` checks lowercase `"=pass"`). **C1 is unpassable as frozen.** My scratch reference passes all 7 frozen
refusal + 4 safe legs, yet:

```
$ python3 …/c1-count.py --builder tools/build-spans-hardened-ref.py --work .../work-decisive
EMPTY_OK=pass   REBUILD_OK=pass   HELDOUT_OK=pass   ESCAPE_ENTRY=pass(refused)
FOREIGN=pass(refused)   SYMLINK_OUT=pass(refused)   SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused)   DEVZERO_TXT=pass(refused)   FAT_RAW=pass(refused)   MANY_QUOTES=pass(refused)
BEFORE_FOREIGN=deleted   DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0    C1=FAIL    EXIT=1
```
`REFUSE=0/7` while seven refusal legs printed `=pass` — same bug. **Isolating proof this is the only blocker** (case fix on a **scratch copy only**; the lane file was never
edited — digest still `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` = the freeze-commit blob). Same command plus `--controls .../controls`:
the same 11 legs all pass, then `BEFORE_FOREIGN=deleted`, `CONTROL_REFUSEALL=denied`, `CONTROL_build-spans-r55=denied`,
`DENIED=2/2`, `SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=2/2`, `C1=PASS`, `EXIT=0`. The same case-fixed counter
still correctly FAILS the base builder (`FOREIGN=fail(rc=0, orphans deleted…)`, `C1=FAIL`), so the one-token change
(`"=PASS"`→`"=pass"` at `:391`,`:399`) restores discrimination rather than rubber-stamping. **Proposed patch, report-only
(not applied)**; amend-vs-re-freeze is the L1's call.

## Defect 2 — `expect_ok`'s span reconstruction is wrong near the form start

`:138` reconstructs the expected span as `form[offset : offset + len(quote) + min(CONTEXT, offset) +
CONTEXT]`, but the builder's rule (`tools/build-spans.py` ~`:146`) is `form[start : off + len(quote)+CONTEXT]`
with `start = max(0, off-CONTEXT)`. They agree only when `off >= 2*CONTEXT`; within 160 chars of the form start
the expected bytes are short by `off`. The counter's own fixture triggers this (`synth_quotes` picks `i =
rng.randrange(20, …)`):

```
$ python3 …/c1-count.py --builder tools/build-spans-hardened-ref.py --seed 35 --work .../work-seed35
EMPTY_OK=fail(spans/S502-1.txt span bytes)
SUMMARY OK=3/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0    C1=FAIL
```
The builder is **correct**; the counter mis-derives the expected span. Seed 7 doesn't hit it, but `--seed` is a
documented argument → live false-negative at any non-default seed. My harness uses the documented rule, passes at 35.

## Defects 3–7 — five more fixture defects, each independently weakening the battery

| # | location | frozen counter | my harness |
|---|---|---|---|
| 3 | `:232-236` | `expect_refuse("SYMLINK_OUT", proc, ["SYMLINK"], …)` then **overwrites** the result: `if not any(real.iterdir()): legs[-1] = f"SYMLINK_OUT={PASS}(refused)"` — reason class discarded; any refusal leaving the target dir empty passes | `SYMLINK_OUT=fail(reason-unnamed:'…: output path is not a directory\n')` |
| 4 | `:150-160` | `expect_refuse` checks rc, reason class and `forbidden_touch` but **never inspects `--out`** — a builder that refuses correctly yet writes a partial manifest first passes every refusal leg (claim: "refuses … **without partial writes**") | `SYMLINK_CACHE=fail(refused but wrote ['PARTIAL.txt', 'spans.tsv'] under --out)` etc. |
| 5 | `:344` | `HELDOUT_OK` passes `snapshot(work)` taken **after** the run, so `expect_ok`'s "nothing outside `--out` changed" check (`:142-146`) compares against a baseline already containing any stray write | `HELDOUT_OK=fail(wrote outside --out)` |
| 6 | `:271-280` | `DEVZERO_TXT` fixture is a **symlink** to `/dev/zero`, so a builder refusing symlinks but reading raw character devices is never caught | new `DEV_TXT` leg places a **direct** char device node (`mknod c 1 5`): `DEV_TXT=fail(reason-unnamed:…)` |
| 7 | `:212` | `REFUSEALL.py` makes `EMPTY_OK` fail, so `out-empty/spans/` never exists; `foreign.write_bytes(…)` raises an unhandled `FileNotFoundError` → abort, exit 1, **no `C1=` line**. The control "denies" by crashing, not by evaluating the predicate | scored on legs, no crash |

```
$ python3 …/c1-count.py --builder tools/build-spans-wrongreason-out.py --work .../work-wro
SYMLINK_OUT=pass(refused)                 # frozen counter: PASS (defect 3)
$ python3 …/c1-count.py --builder tools/build-spans-partialwrite-mutant.py --work .../work-pw-frozen
FOREIGN=pass(refused) … MANY_QUOTES=pass(refused)   # defect 4: wrote spans.tsv + PARTIAL.txt first
$ python3 …/c1-count.py --builder tools/build-spans-stray-mutant.py --work .../work-stray-frozen
EMPTY_OK=fail(write outside --out)    HELDOUT_OK=pass   # <-- defect 5: not detected
$ python3 …/c1-count.py --builder …/controls/REFUSEALL.py --work .../work-refuseall
Traceback (most recent call last):
  File "…/c1-count.py", line 212, in main
    foreign.write_bytes(b"foreign evidence bytes\n")
FileNotFoundError: [Errno 2] No such file or directory: '…/out-empty/spans/S777-1.txt'
EXIT=1
```

## Mutation matrix, "before" baseline, unrun, lane hygiene

All subjects are scratch files under `tools/`; `my harness` / `frozen counter`. 5/5 mutants killed; base
correctly fails; reference correctly passes. The frozen counter kills **0/5** (it fails them only via Defect
1's blanket `C1=FAIL`; after the case fix it still passes 3 of 5). The lane builder is still byte-identical to
the pinned R55 base (sha256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`), so **no C1
candidate builder has landed in the lane yet**:
- `build-spans-r55-base.py` (pinned R55, sha `1ed2650a…bf6`) — `HARNESS=FAIL` / reproduces the committed
  receipt `corpus/evidence/round58/controls/c1-before.txt` leg-for-leg (same 15 lines, same `C1=FAIL`, same
  `EXIT=1`): four safe legs pass, all seven refusal legs fail — `FOREIGN=fail(rc=0, orphans deleted: foreign
  gone=True)`, `SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)`, `SYMLINK_CACHE=fail(rc=0,
  expected refusal)`, `FIFO_TXT`/`DEVZERO_TXT` `=fail(rc=1, reason […] absent in '…no defined text form…')`,
  `FAT_RAW=fail(rc=1, reason ['SIZE'] absent in '…capture-text refused … ole-malformed…')`, `MANY_QUOTES=fail
  (rc=0, expected refusal)` — ending `SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0`.
- `build-spans-hardened-ref.py` (scratch reference) — `HARNESS=PASS` (4/4 safe, 8/8 refusal) / `C1=FAIL` (def. 1).
- `build-spans-stray-mutant.py` (writes outside `--out`) — `HARNESS=FAIL` / misses on HELDOUT_OK (def. 5).
- `build-spans-partialwrite-mutant.py` (writes, then refuses) — `HARNESS=FAIL` / misses entirely (def. 4).
- `build-spans-wrongreason-out.py` (refuses symlink w/o `SYMLINK`) — `HARNESS=FAIL` / scores it PASS (def. 3).
- `build-spans-char-dev-mutant.py` (allows raw char devices) — `HARNESS=FAIL` / scores it PASS (def. 6).

Unrun: `MANY_QUOTES` exact 100 000-row boundary not separately fuzzed (counter and reference both refuse at
`QUOTES_CAP + 1`). No live-target fetch attempted (round-42 egress-scope L0 remains open). C2 / S101 quote-set
binding out of scope; the pinned S101 capture was used only as a builder input for `HELDOUT_OK`, as the frozen
counter does. No tooling installed or updated (`RULES.md` read; pacman untouched). Lane hygiene: `git status
--porcelain` shows only the pre-existing untracked `.ufo/waves/round-58/`; I wrote **no** lane file except this
report; `c1-count.py` digest unchanged = freeze-commit blob; scratch removed at yield.

## Risks / blockers

- **Blocker for C1 scoring:** with `c1-count.py` as frozen, no builder produces `C1=PASS`, so any wave verdict
  recorded against the frozen counter is vacuous for the refusal legs. The L1 must amend (one-token case fix) or
  re-freeze before C1 can be measured. Defects 3–7 are independent, each individually weakening the battery.
- My reference encodes the claim as *I* read it; if the L1 reads a leg differently (e.g. requiring the token
  `FOREIGN` rather than the file name, or a specific `SIZE` token) it may need adjusting — a claim-reading question
  for the L1, not a counter defect. I do not judge C2 and assert no claim-verdict about C1's correctness; the L1
  integrates.

VERDICT: the concrete work/attack is the frozen C1 counter's ability to discriminate a hardened builder from
a base/mutant builder on the seven refusal legs plus the safe/rebuild legs; the attack is a builder satisfying
every frozen leg semantics while wrong on reason naming, partial writes, containment or device typing. The
frozen counter **falsifies** this discrimination — `C1=PASS` is unreachable for any builder
(`c1-count.py:391`/`:399` case mismatch), and with that fixed it still admits a wrong-reason refuser, a
partial-writing refuser and a char-device reader (`:232-236`, `:150-160`, `:344`, `DEVZERO_TXT` fixture). C1's
operability gate is therefore FALSIFIED as frozen; my scratch harness (8 refusal + 4 safe legs, 5/5 mutants
killed, reproducing the frozen `c1-before.txt` baseline leg-for-leg) shows it is achievable.
