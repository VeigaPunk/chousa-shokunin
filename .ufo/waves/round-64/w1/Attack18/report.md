# Attack18 — C3 startup assertions versus complete relocated tree

Axes: startup path accuracy; complete-tree relocation continuity; frozen-counter fidelity.
Recommendation only; no admission, integration, or production change.

## Findings, by severity

### High — frozen C3 relocation oracle expects the wrong path; its required 3/3 cannot hold

`corpus/evidence/round64/c3-count.py:86-92` creates `.../lane-copy/corpus/evidence/round65/FILE`, but computes `want = mirror.parent / needs[0]`, hence expects `.../lane-copy/corpus/evidence/corpus/SOURCES.md`. All three instruments derive `LANE = HERE.parents[2]`, correctly reporting `.../lane-copy/corpus/SOURCES.md` instead (battery lines 119-124; receipts lines 25-30; counter lines 34-39).

Bounded probes reproduced exactly the frozen relocation loop's filesystem layout and subprocess invocation for each unmodified instrument. All exited 2, stdout empty, stderr named the correct missing file; all three frozen `ok` expressions evaluated false. Representative command:

```text
/usr/bin/python -B /fast/scratch/hyaku/chousa-r64/Attack18/rel-c3-count.py/lane-copy/corpus/evidence/round65/c3-count.py
exit 2
stderr: c3-count: MISSING_LANE_FILE: /fast/scratch/hyaku/chousa-r64/Attack18/rel-c3-count.py/lane-copy/corpus/SOURCES.md
counter expects: /fast/scratch/hyaku/chousa-r64/Attack18/rel-c3-count.py/lane-copy/corpus/evidence/corpus/SOURCES.md
```

This is a **frozen claim/instrument failure**, not a supplemental weakness: claims.md:231-233 requires the unmodified counter to produce `RELOCATION_MATCH=3/3` and `C3=PASS`; line 100 makes any failed relocation fatal. [INFERENCE] Its full canonical run cannot meet that target with these frozen bytes, irrespective of the smoke/shift legs. I did not run the full counter or fabricate its final output. Preserve the frozen failure; any corrected oracle must have a distinct supplemental identity, not replace the claim's rule.

### Medium — frozen fixture is a same-depth rename, not its advertised extra-directory shift

`c3-count.py:86` changes `round64` to `round65` while retaining `lane-copy/corpus/evidence/<round>/FILE`. This is the same directory depth, contradicting claims.md:201-202 and 235-239's description of the exercised failure shape. Even correcting only the expected path would leave the advertised off-by-one coverage absent.

Independent controls actually placed each unchanged script at `lane-copy/corpus/evidence/round64/extra/FILE`. All exited 2, stdout empty, naming the exact derived `lane-copy/corpus/corpus/SOURCES.md`. Thus the startup guards work for the real depth shift; the defect is in the frozen counter's evidence construction, not demonstrated breakage of the guards.

## Complete relocated tree and assertion controls

Exported the complete committed lane using `git archive --format=tar bf40d99bda9eefdad3ed6276da077cfb24ba82f1` (exit 0; 298045440 bytes), into `.../Attack18/complete/deeper/renamed-lane`. This is a committed-tree export, not a git clone or current untracked/inherited-tree copy. Initial Python safe extraction rejected an archived absolute symlink; guarded retry preserved archived symlinks while refusing writes through external parents. No network or repository mutation.

For each instrument, executed `/usr/bin/python -B -c 'import runpy; d=runpy.run_path(PATH,run_name="startup_probe"); print("STARTUP_OK LANE="+str(d["LANE"]))'` (exact commands in receipt). This exercises import-time startup without invoking measurement main functions.

- All three complete-tree imports: exit 0, stderr empty; `STARTUP_OK LANE=.../complete/deeper/renamed-lane`.
- Temporarily removing only archived `corpus/SOURCES.md`: all three exit 2 with empty stdout and the exact removed path on stderr.
- Restoring SOURCES, temporarily removing archived `tools/lane-preflight.py`: battery and receipts exit 2 with empty stdout and the exact removed path on stderr.
- Each removed scratch file was restored before the next control; the entire scratch export was subsequently deleted.

The complete-tree behavior **supports**, rather than falsifies, the named limit at claims.md:237-239. Existence guards do not bind a complete tree to the original absolute location, and the claim explicitly discloses that. Do not report legitimate complete-tree relocation as a bypass.

## Byte provenance and scope

`git diff bf40d99bda9eefdad3ed6276da077cfb24ba82f1 -- corpus/evidence/round64/{c3-count.py,c1-battery-v3.py,run-receipts-v3.py}` (equivalent explicitly enumerated command): exit 0, no output. Independently read frozen bytes with `git show`; SHA-256 equality with working bytes held for all three. Prefixes match the freeze: battery `4b3f0b658bcd3bb6`, receipts `0f3cfae75f711f17`, counter `465a8c5efbb870f7`. Full hashes and all 14 bounded probe commands, stdout, stderr, and exits are in `Attack18/probe-receipt.json`.

C1's frozen E12/E13 independently drawn fixture-name mismatch remains an acknowledged frozen failure (assignment-provided observation; not rerun here). `c1-battery-supplement.py` is distinct post-freeze evidence and cannot repair the frozen C1 verdict. No finding here concerns that supplement or treats `ref-preflight-v3.py` as production.

## Residual risk and verification gaps

- `xd://lsp` is unavailable (`No such tool`); semantic references/definition/diagnostics could not be requested. Findings use direct source/path arithmetic plus execution, not grep as semantic proof.
- No full C3 smoke/shift measurement, C1 battery, source-admission spot-check, or unrelated runtime/identity/saturation/resume review was performed; those are outside this startup/depth item. `controls/c3-after.txt` was absent when read; no result was inferred from that absence.
- The counter's static selfcheck and shift verdict logic were not separately attacked. Missing BATTERY/SHiFT paths beyond the explicitly asserted set were not treated as failures of this narrowly frozen list.
- No frozen rules, counters, operator inputs, fleet/sibling files, or production files were edited. No git/jj mutations, commits, pushes, service changes, installs, or updates. Existing Python 3.14.8 and git were used; no installation channel applies.
- Scratch `/fast/scratch/hyaku/chousa-r64/Attack18` was removed before delivery; zero live clones.

## Self-evaluation

Accuracy 4/5: exact commands and raw receipts; full canonical output deliberately not claimed. Completeness 4/5: all listed startup guards and complete-tree case covered; full counter not exercised. Clarity 4/5: frozen failure separated from supported named limit. Actionability 4/5: exact offending expressions and correction boundary identified; frozen bytes intentionally untouched. Conciseness 4/5: raw outputs kept in JSON rather than repeated. Mean 4.0/5. Highest-value improvement for the integration owner is to retain the red frozen verdict and separately run any newly named corrected depth/oracle supplement. The user should agree with the explicitly bounded evidence, not infer full-round closure.
