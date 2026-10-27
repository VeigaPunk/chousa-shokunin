# R59Scout40 — offline source reconnaissance

## Bounded walk

- Read the frozen round-59 claims path recorded in lane context: `corpus/evidence/round59/claims.md` was not present at that path. The round-59 evidence directory currently exposes `census-start.txt` and `controls/c1-before.txt`; no alternate frozen claims file was established from this walk.
- `corpus/evidence/round59/census-start.txt` records validator exit 0 and five duplicate-URL warnings, all W04: S051, S053, S073, S074, S075. These are pre-existing census warnings, not proof that any URL's content or scope is invalid.
- `corpus/SOURCES.md` rows S051–S056 scope the prior HTML/head-boundary and Python network-transport references. S052 explicitly limits socket timeout semantics to each blocking operation rather than a whole-transfer deadline; S053 says `create_connection` resolves/traverses addresses itself, not that earlier address checks pin a connection. Those carefully scoped rows are relevant context, not current round-59 test evidence.
- The same registry records S073 as a correction to S070's `sha256sum` anchor, S074 as a rejected duplicate of S059's `hashlib` scope, and S075 as a locally captured `mktemp` manual. The census's duplicate warnings concern URL reuse across scopes, not necessarily duplicate claims; S074 itself demonstrates the distinction between genuine duplicate scope and a separate scope under one URL.
- `corpus/lessons/round-58.md` reports the prior positive-verdict-path defect: frozen C1's aggregate could not represent positive state, with `REFUSE=0/7`, despite safe/refusal legs reportedly passing. It says the round appropriately treated the claim as unprovable rather than rewriting frozen bytes and identified criterion 115 as a prospective positive-control requirement. It also states the fetch-scope L0 question remained open and no live fetch was performed.
- `corpus/evidence/round59/controls/c1-before.txt` is a direct before-capture for current calibration. Observed: `EMPTY_OK`, `REBUILD_OK`, `ESCAPE_ENTRY`, and `HELDOUT_OK` pass; FOREIGN and SYMLINK_OUT report `rc=0` despite expected refusal, and SYMLINK_OUT reports target-dir-written; SYMLINK_CACHE also reports `rc=0` despite expected refusal. FIFO_TXT and DEVZERO_TXT refuse but lack expected diagnostic tokens; FAT_RAW lacks expected `SIZE`; MANY_QUOTES returns `rc=0` rather than expected refusal. The summary is `OK=4/4 REFUSE=0/7`, with `BEFORE_FOREIGN=deleted`, `DENIED=0/0`, `C1=FAIL`, `EXIT=1`.

## Relevance and limits

**Observed:** the before-capture independently illustrates why the round-58 lesson's positive-control concern matters: the control's aggregate refusal denominator is zero, and multiple supposedly refused cases return success. It also captures a destructive foreign-file outcome and an external-target write. These are high-value falsification targets for interpreting any later positive verdict-path evidence.

**Inference:** these outcomes suggest the fixture/counter may be conflating refusal outcomes, diagnostic matching, and side effects; the capture alone does not identify which implementation or harness layer caused each failure. `DENIED=0/0` is not evidence of zero actual denials, given the zero denominator and the listed cases.

**Unresolved:** no after-capture or current-round final counter was available in the bounded walk; no claims body was available at the frozen path, so the exact predicates, pinned revision, and acceptance contract cannot be cross-checked here. No live external fetch was attempted; the fetch-scope ruling remains outside this offline reconnaissance.

## Evidence provenance

All findings above come from the lane-local artifacts named above, read offline. No source repository was modified, no external fetch was made, and no tool was installed. Confidence: high for the literal capture and registry statements; limited for causal interpretation and round-59 claim alignment.