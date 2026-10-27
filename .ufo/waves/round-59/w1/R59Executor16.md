# R59Executor16 — round-58 frozen C1 counter: the positive verdict path does not exist

Seat: `R59Executor16` (executor, leaf). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin` (read-only for this seat). Lane tip at time of work: `af8c0a460d087cbfb8245fb9326608783ccc510b`. Scratch (removed before yield): `/fast/scratch/hyaku/chousa-r59/R59Executor16/`. No lane file other than this report was created or modified by this seat; `GIT_OPTIONAL_LOCKS=0 git status --porcelain` shows only the pre-existing untracked `?? .ufo/waves/round-59/` and `?? corpus/evidence/round59/`.

Frozen input (the only frozen predicate bytes that exist): `corpus/evidence/round58/c1-count.py`, sha256 `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`. The assignment's `corpus/evidence/round59/claims.md` **is absent** at the current tip (`ls: cannot access ... No such file or directory`), so no round-59 claim/counter is adjudicated here; evidence below is against the exact round-58 frozen bytes and the two round-59 control bytes that exist.

Axes: operability (assigned), calibration. This is a counter/control finding, not a builder finding. No live fetch, no install, no git/jj write, no spawn.

## Bottom line

F1: The frozen counter **cannot print `C1=PASS` for any builder**. Its aggregate requires uppercase `=PASS` on refusal legs that the same file always formats lowercase (`PASS = "pass"`). I ran the frozen bytes in place against a probe builder that satisfies every declared leg: all 11 legs printed pass, `BEFORE_FOREIGN=deleted`, exit 1, `REFUSE=0/7`, `C1=FAIL`. Changing exactly two case comparisons in a scratch copy of the same bytes, with the same probe and no other change, gives `REFUSE=7/7`, `C1=PASS`, exit 0. The frozen positive verdict path is unsatisfiable, so round-59's "positive verdict-path" milestone has no positive arm in round-58's counter to calibrate against.

F2: Because the aggregate is a constant, `REFUSE=0/7` carries no information. Two empirically different builder states — 7 true refusals (my probe) and 0 true refusals (lane base builder, per the frozen receipt) — print the identical `SUMMARY ... REFUSE=0/7` and `C1=FAIL`. Any `CONTROL_*=denied` line is equally uninformative: denial is indistinguishable from "the counter always fails".

F3: The positive path is also working-directory dependent. `BEFORE_BUILDER = HERE/"controls"/"build-spans-r55.py"`; the same counter bytes copied to another directory score `BEFORE_FOREIGN=absent` and fail even when the builder passes every leg.

F4: The two-token repair is **necessary but not sufficient**. With only the case fix, a probe that overwrites the foreign span file's bytes before refusing, and leaves an unlisted `spans/S999-1.txt` outside a 3-row manifest, still reaches `C1=PASS`, exit 0. The declared kill rules "changed foreign file" and the span-file set are printed but not enforced (`got`/`want` computed and unused).

F5: The gate is not wholly vacuous: after the case fix, a probe without the `--out` symlink guard is scored `SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)`, `REFUSE=6/7`, `C1=FAIL`. The defect is confined to (a) aggregation and (b) the unenforced legs.

## Arm 1 — frozen counter, exactly as committed, against a conforming probe

```
cd /fast/scratch/hyaku/chousa-r59/R59Executor16
TMPDIR=$PWD/tmpd python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py \
  --builder /fast/scratch/hyaku/chousa-r59/R59Executor16/probe-conforming.py \
  --work /fast/scratch/hyaku/chousa-r59/R59Executor16/work-frozen-inplace ; echo "EXIT=$?"
```
Output (stdout, stderr empty, `EXIT=1`):
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
C1=FAIL
```
Every declared leg printed `pass`, including all 7 refusal legs (`=pass(refused)`), and the aggregate still says `REFUSE=0/7`. The verdict token is not reachable.

Probe disclosure (calibration instrument, not a lane candidate): a self-contained builder that refuses before any write — `--out` symlink, cache entry symlink, non-regular cache entry via `lstat` (never opened), raw `st_size > 64 MiB`, `quotes.tsv` rows `> 100000`, entry column with `..`, and any existing `spans/S###-N.txt` not in the new plan (named in the message, never deleted); it derives the OLE form by importing the lane `tools/capture-text.py` read-only (`sys.dont_write_bytecode = True`, child launched with `-B` and `PYTHONDONTWRITEBYTECODE=1`), and writes `offset = max(0, find(quote)-80)` with span window `form[offset : offset+len(quote)+min(80,offset)+80]`, i.e. the window the frozen counter itself expects (deliberately isolating aggregation, not the separate offset<80 window divergence). No `__pycache__` appeared in `tools/` (newest entries predate the run: `build-spans…pyc` 14:21, `capture-text…pyc` 01:15; runs at 15:20+).

## Arm 2 — same counter bytes, copied: the positive path also depends on WHERE the counter sits

```
cp /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py ./c1-count-frozen.py
sha256sum c1-count-frozen.py   # 65da18bb… (identical to the lane file)
python3 -B c1-count-frozen.py --builder ./probe-conforming.py --work $PWD/work-frozen ; echo "EXIT=$?"
```
```
… HELDOUT_OK=pass
BEFORE_FOREIGN=absent
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=absent DENIED=0/0
C1=FAIL
EXIT=1
```
Same bytes, same builder, different directory: `BEFORE_FOREIGN` flips to `absent` because `BEFORE_BUILDER` is resolved as `HERE/controls/build-spans-r55.py`. A conforming builder is failed for the counter's location, not its behaviour.

## Arm 3 — two-token repair on a scratch copy: `C1=PASS` becomes reachable

```
diff -u c1-count-frozen.py c1-count-patched-pass.py
```
```
-    ref_pass = all(("=PASS" in l) for l in ref_legs)
+    ref_pass = all(("=pass" in l) for l in ref_legs)
...
-          f"REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)} "
+          f"REFUSE={sum('=pass' in l for l in ref_legs)}/{len(ref_legs)} "
```
(These are frozen lines 391 and 399; `PASS = "pass"` at line 52; refusal-leg emitters are 147/160/207/223/234 plus the literal lowercase at 315; `ok_pass` at 390 already compares `=pass`.)
```
python3 -B c1-count-patched-pass.py --builder ./probe-conforming.py --work $PWD/work-patched ; echo "EXIT=$?"
```
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
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
```
Identical leg lines, identical builder; only the aggregate tokens differ. Mechanism (frozen file, line numbers): `verdict = "PASS" if (ok_pass and ref_pass and integrity and denied_pass)` at 394; `ref_pass` at 391 is the conjunction over the 7 refusal legs; every one of those leg strings is produced with lowercase `pass`, so that conjunction is `False` for any builder output, and `REFUSE` at 399 sums the same uppercase token, i.e. always `0`.

## Arm 4 — after the repair, the positive verdict still admits the declared destructive/hygiene defects

Probe `probe-d6d8.py` = Arm 1 probe + two behaviours the counter declares but does not check: on the FOREIGN leg it overwrites the foreign file's bytes (`b"CORRUPTED foreign evidence bytes\n"`) and then refuses naming it (D6); and it always writes `spans/S999-1.txt`, unlisted (D8, where `expect_ok` builds `got`/`want` and never compares them).

```
python3 -B c1-count-patched-pass.py --builder ./probe-d6d8.py --work $PWD/work-d6d8 ; echo "EXIT=$?"
```
```
… FOREIGN=pass(refused) … HELDOUT_OK=pass
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
```
Fixture bytes after that PASS run (same `--work`):
```
$ ls work-d6d8/out-empty/spans
S501-1.txt  S502-1.txt  S503-1.txt  S777-1.txt  S999-1.txt
$ cat work-d6d8/out-empty/spans/S777-1.txt
CORRUPTED foreign evidence bytes
$ cat work-d6d8/out-empty/spans/S999-1.txt
unlisted span not in manifest
$ cut -f5 work-d6d8/out-empty/spans.tsv
span_file
spans/S501-1.txt
spans/S502-1.txt
spans/S503-1.txt
```
So a positive `C1=PASS` coexists with a foreign file whose bytes were destroyed and with an output file outside the manifest. The claim's kill rule ("changed/removed foreign file") is stated but unenforced; `FOREIGN` checks only `rc != 0`, existence, and a reason substring in the first 200 characters.

## Arm 5 — the gate does reject an enforced-leg defect (so F1–F4 are not "the counter checks nothing")

Same repaired counter, probe with only the `--out` symlink guard removed:
```
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SUMMARY OK=4/4 REFUSE=6/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

## Arm 6 — how a control is scored "denied" without being scored

Frozen counter, builder `probe-null.py` (`import sys; sys.exit(0)`, writes nothing):
```
python3 -B <lane>/corpus/evidence/round58/c1-count.py --builder $PWD/probe-null.py --work $PWD/work-null ; echo "EXIT=$?"
EXIT=1
stdout: (empty)          # grep -c '^C1=' run-null.txt  -> 0
stderr: FileNotFoundError: .../work-null/out-empty/spans/S777-1.txt   (line 212)
```
The counter plants the foreign fixture unconditionally, assuming the EMPTY_OK builder created `out-empty/spans`. A builder that refuses everything (the `REFUSEALL.py` control shape) therefore produces **no `C1=` line at all**; the control loop scores a missing token as `denied`. That is the mechanism behind the round-58 receipt's `CONTROL_REFUSEALL=denied`, and it means deny-only controls cannot validate a positive path even after F1 is fixed.

## Calibration reading for round 59

- Round-58's C1 predicate, as frozen, has no positive state: the declared final verdict is unreachable for every possible builder (F1), so `REFUSE=0/7`/`C1=FAIL` cannot distinguish a conforming builder from a non-conforming one (F2). A round-59 positive control must be built against a counter that can emit its declared final token *for a conforming artifact* and must also be shown to reject a non-conforming artifact in the same run.
- My arms give the four readings such a control needs, on the two-token-repaired copy only: conforming → `PASS` (Arm 3); enforced-leg defect → `FAIL` (Arm 5); unenforced-leg defect → `PASS`, i.e. still unsound (Arm 4); control that never runs → **no verdict token** (Arm 6). Only the first two are currently satisfiable at once, and only after the repair.
- Ceremony/provenance note: the frozen receipt `corpus/evidence/round59/controls/c1-before.txt` is byte-identical to `corpus/evidence/round58/controls/c1-before.txt` (`diff` → identical). Its last line `EXIT=1` is **not** emitted by the counter (no `EXIT` string in `c1-count.py`); it was appended by a wrapper, so the receipt is not raw counter stdout.
- Secondary, not adjudicated: `python3 -B <lane>/corpus/evidence/round58/c2-count.py --root <lane> --work $PWD/work-c2` prints `C2=FAIL` with `ERROR ENTRY_MISSING / PROVENANCE_TRIO / S101_NOT_IN_SOURCE / REF_ID_UNBOUND / MANIFEST_MISSING / BUILDER_REBUILD_MISMATCH / CAPTURE_BOUND=0/12 / ANCHOR_BOUND=0/3 / ENTRY_QUOTES=0/12 / NEW_GROUND_FAIL` and `QUOTE_ROWS=0/12` (no `QUOTE_SET` error, i.e. the 12 frozen quotes are present). C2's positive path is unexercised on current lane bytes, not shown defective; note that its `NEW_GROUND` leg shells `git grep … b13ca7b5…` inside `--root`, so C2 cannot reach `PASS` outside a git worktree holding that commit — a positive-path precondition distinct from C1's.
- Observed boundary of the 3/10 operability axis, this seat only: the frozen gate's aggregate is not a verdict function of builder behaviour. I make no numeric score claim.

## Limits / what I did not establish

- I did not re-run the lane base builder (`tools/build-spans.py`, still the r55 pin `1ed2650a…`, unchanged this round) through the full battery. Its `MANY_QUOTES` leg materialises 100001 span files (~413 MB, per the round-58 audit); I cite the frozen receipt instead of regenerating that fixture. My probes refuse `MANY_QUOTES`, so no large tree was produced here (scratch peaked at 46 MB, mostly the 80 MiB sparse FAT_RAW fixture).
- Probe builders are mine and are described by their guards above; they are calibration instruments and must not be mistaken for a candidate lane builder. Their span window deliberately matches the counter's expectation, so nothing here re-litigates the separate `offset < 80` window divergence.
- Round-59 claims/counter bytes do not exist yet at the tip; if they land after this report, F1–F4 must be re-checked against the new digest rather than assumed.
- No LSP symbol work was applicable (byte-level counter audit); no source repositories were read.

## Recommendation to L1 (proposed in this report only; nothing applied)

1. Treat round-58 C1 as unprovable, not failed: the frozen bytes cannot yield `PASS`. Do not rewrite them.
2. A round-59 positive control needs, frozen before wave data: the exact counter digest; a conforming builder fixture that reaches the declared token; a same-run non-conforming arm that is denied; and at least one arm that exercises each kill rule it names (foreign bytes, unlisted span files) — currently those two are printed but not enforced.
3. Any receipt should be raw counter stdout with the exit code recorded separately, or its wrapper stated, so `EXIT=` lines are not misread as counter output.

---

Report path relative to lane root: `.ufo/waves/round-59/w1/R59Executor16.md`. Scratch `/fast/scratch/hyaku/chousa-r59/R59Executor16/` removed after this report was written; every command and output it depends on is quoted above.
