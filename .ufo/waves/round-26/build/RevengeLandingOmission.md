# R25-M15 landing-omission review — ChousaR26.RevengeLandingOmission-3
Axes: causal discrimination (falsifiable hypotheses), detection (pre/post byte pin), calibration (separate observation from inference).

## Evidence and divergence
- `corpus/lessons/round-25.md:248-263`: helper reported `landed c2a6e338…`; its gate blob was `63a39282…`, not measured `985a6320…`; other 10 measured blobs matched. Approved gate-only retry reported `c125d8bc…`, after which 11/11 matched; lesson says no helper-code change and cause unresolved.
- `corpus/evidence/round25-measured-revision.json:2-3,6-9,72-73`: pins `c125d8bc…`, all-match=true; records c2a6e338 as omitted checkpoint and stale gate SHA. This independently preserves the mismatch/recovery distinction, not its cause.
- `scripts/hyaku/jj-lane.sh:135-141`: `flock` serializes helper invocations per physical lane. It does not establish exclusion of unrelated processes editing files (inference from lock scope).
- `scripts/hyaku/jj-lane.sh:654-703`: named paths are tracked, `jj diff --summary` snapshots the requested files, then `jj commit ... -- fs_req`; no hash pin binds bytes measured earlier to candidate bytes. `:710-725` validates scope and pushes.
- `scripts/hyaku/jj-lane.sh:237-262`: `landed` is emitted only after `ls-remote` equals the local branch tip and the run's commit (or rewritten descendant) is accounted for. Thus a wrong printed remote hash is disfavored; the recorded c2a6e338 blob mismatch is the relevant failure.
- Read-only Git timestamp query: c2a6e338 committer `2026-10-21T05:52:11-03:00`; c125d8bc `05:53:19-03:00`; `merge-base --is-ancestor` succeeded. The 68-second retry gap dates the recovery but cannot identify a writer or snapshot event.

## Falsifiable causes (cause remains UNKNOWN)
- H1 — snapshot timing/cache: bytes changed after the helper's preflight `jj diff` snapshot or its commit snapshot retained older content. Prediction: an instrumented one-at-a-time replay with stable pre/post worktree SHA but old candidate blob implicates snapshot state; matching candidate blob on each snapshot falsifies this run-specific version. Helper ordering: `jj diff` at `:668`, commit at `:700-703`.
- H2 — concurrent editor: another writer replaced the gate between measurement and snapshot. Prediction: a repeated hash immediately before/after the helper differs, or a writer audit identifies a write in that interval; stable endpoints alone do not rule out a transient write-then-restore. The helper lock only excludes cooperating helper runs (`:135-141`).
- H3 — deterministic path/split handling: despite the gate being named, path-limited selection could have retained prior bytes. Prediction: replay with identical pinned bytes and exact gate-only path repeatedly yields old blob; repeated correct candidate bytes under identical conditions falsifies it. The successful gate-only retry with unchanged helper code weakens, but does not eliminate, this because the original request set differed.
- Wrong-revision reporting is a weaker alternative: `report_landed` verifies the remote tip and run-commit ancestry (`:237-262`); evidence explicitly compares the c2a6e338 gate blob. No evidence shows a mislabeled revision.

## Read-only pre/post check for L1
Use exact **leaf files** passed to the helper (all production/evidence paths, not only the gate); do not pass directories. Run from lane root; save the pre-pin outside the repo. Paths here must not contain tab/newline.

```bash
set -euo pipefail
PATHS=(tools/research-gate.sh corpus/SOURCES.md corpus/lessons/round-26.md) # replace with ALL requested files
PINS=/tmp/r26-pre.sha256
for p in "${PATHS[@]}"; do test -f "$p"; printf '%s\t%s\n' "$(sha256sum -- "$p" | cut -d' ' -f1)" "$p"; done > "$PINS"
# Now invoke the normal helper. Copy REV from its `landed <REV>` line.
REV=<landed-revision>; bad=0
while IFS=$'\t' read -r want p; do
  tree=$(sha256sum -- "$p" | cut -d' ' -f1)
  blob=$(git --no-optional-locks show "$REV:$p" | sha256sum | cut -d' ' -f1)
  printf '%s pre=%s worktree=%s commit=%s\n' "$p" "$want" "$tree" "$blob"
  [[ "$want" = "$tree" && "$want" = "$blob" ]] || bad=1
done < "$PINS"
exit "$bad"
```
The pre step pins bytes just before helper invocation; post requires committed blob = pre-pin = current worktree for every named file. Any difference fails closed; `pipefail` exposes a missing revision path. If post-run edits are intentional, compare commit to pre-pin as the landing verdict and report worktree drift separately. This check detects the stale-byte outcome, not its writer/cause; no test/replay was run in this seat.

Confidence: high on observed c2a6e338 mismatch and c125d8bc 11/11 recovery (lesson + JSON); low on causal attribution because there is no captured concurrent-writer timeline or per-snapshot hash. Git object-size probe was not informative: `git cat-file -s <64-hex SHA-256>` returned `Not a valid object name`.

VERDICT: Landing identity check caught and corrected the R25-M15 stale gate blob; cause remains unresolved. No installs.