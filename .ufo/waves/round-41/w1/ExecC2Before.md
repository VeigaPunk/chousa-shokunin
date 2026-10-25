# ExecC2Before — C2 before-state replication (round 41, wave 1)

- seat: executor, leaf (id `ExecC2Before`); no subagent dispatch surface was used or needed
- date: 2026-10-24
- lane repo (read-only): `/home/vgpnk/Projects/shokunin/chousa-shokunin`
- pinned tree measured: `HEAD = 872bf3a3507875b382313f955d15960f9638256f`
  ("round-41 verifier spot-check (integrator, hyaku): non-author admit/reject")
- writes: this report only. No lane production file, lane git/jj state,
  `/home/vgpnk/Projects/shokunin/.ufo/state`, fleet repo, or sibling repo was modified.
  No network egress. No tool install or update (nothing needed; pacman untouched).
  No model alias was passed or hardcoded; the seat ran on its host-assigned route.

## Assigned attack

> In a copy of `/home/vgpnk/Projects/shokunin/chousa-shokunin` with
> `corpus/evidence/round41/w04-dispositions.tsv` removed, re-run `c2-count.py`;
> confirm `W04_DISPOSITIONED=0/4` and exit 1 — the committed
> `controls/c2-control-before.txt` must match.

## Pin inventory (measured, not inferred)

| object | pin |
|---|---|
| lane HEAD | `872bf3a3507875b382313f955d15960f9638256f` |
| freeze commit (claims + counters + controls) | `b173b0943e647f7e3a365689df19debe40fd9dd2` |
| `corpus/SOURCES.md` @ HEAD | blob `d97529ec4b07903084d7c5b61ae8f24d69ecb9d3` |
| `corpus/SOURCES.md` @ freeze `b173b09` | blob `6a3d0765809da4e880154f163d7d73ea6753a9ea` |
| `corpus/evidence/round41/w04-dispositions.tsv` @ HEAD | blob `88be5ef34c33a31ed7ced27c3fabab196db465c5`, sha256 `2558bba41e54ae9f3c4fc48c89c95bbcf7c24acdbe6a592dcb72c41ff2dee7ca` |
| `.ufo/waves/round-41/controls/c2-control-before.txt` @ HEAD | blob `fa962f93e84ffbe6a4e36226c85e04f96c7ed0f6`, sha256 `0d90f683823648cc6901d072632612ba1c298b281f564cecf05d7b2f385f9803` |
| `corpus/evidence/round41/c2-count.py` @ freeze and @ HEAD | identical blob `86a112d1ab7ab1c0380e4724c90802f938ec965f`, sha256 `66bb31af0d199443c9a9c6f8bd9cf733f92e883306770ee7831559a34f4ccaa3` |
| census used by the counter (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`) | sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`; fleet blob `3f314620b2395eeb70d8405410132027dfe608e4` (outside the lane, not hash-pinned by the counter) |

Worktree `corpus/SOURCES.md` is byte-identical to HEAD (`git hash-object` = index = HEAD blob),
so the live census read committed bytes, not an in-flight sibling edit.

## Runs and exact output

### R1 — assigned attack: committed HEAD copied via `git archive`, TSV removed

```
rm -rf /tmp/exec-c2before-r41 && mkdir -p /tmp/exec-c2before-r41/copy
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive HEAD | tar -x -C /tmp/exec-c2before-r41/copy
rm -f /tmp/exec-c2before-r41/copy/corpus/evidence/round41/w04-dispositions.tsv
cd /tmp/exec-c2before-r41/copy && python3 corpus/evidence/round41/c2-count.py; echo "COUNTER_EXIT=$?"
```

```
W04_DISPOSITIONED=0/5
  FAIL S051: no disposition row
  FAIL S053: no disposition row
  FAIL S073: no disposition row
  FAIL S074: no disposition row
  FAIL S075: no disposition row
COUNTER_EXIT=1
```

`TSV_PRESENT_AFTER_RM=no`; stderr empty; `LANE` resolved to the copy
(`/tmp/exec-c2before-r41/copy`).

### R2 — committed control byte match

```
diff -u <(cat /tmp/exec-c2before-r41/c2-copy-before.txt; echo 'BEFORE_EXIT=1') \
        /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-41/controls/c2-control-before.txt
echo "DIFF_RC=$?"
```

No diff output; `DIFF_RC=0`. Control is 7 lines (5 FAIL lines + total line +
`BEFORE_EXIT=1`); counter stdout is the first 6. **Exact byte match.**

### R3 — positive control: committed TSV restored in a second copy

TSV bytes taken from `git show HEAD:corpus/evidence/round41/w04-dispositions.tsv`
(blob verified `88be5ef…`), then the counter re-run:

```
W04_DISPOSITIONED=5/5
WITH_TSV_EXIT=0
```

This matches `corpus/evidence/round41/measure-after-c2.txt` and shows the counter is
bidirectional, not stuck at 0.

### R4 — census at the pinned HEAD tree

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin chousa
```

rc 0, five W04 rows: `S051`, `S053`, `S073`, `S074`, `S075`. `n = 5`, not 4.

### R5 — census at the freeze commit, isolated root

`git archive b173b09` extracted under a private fleet root with the fleet
`shokunin.conf` copied in; `validate --root <private root> chousa`:

rc 0, four W04 rows: `S051`, `S053`, `S073`, `S074`. `S075` row count in
`SOURCES.md` at `b173b09` = 0 (blob `6a3d076…`). This is where the literal `0/4` comes from.

### R6 — committed counter inside the freeze tree (no TSV exists there)

```
W04_DISPOSITIONED=0/5   (FAIL S051 S053 S073 S074 S075)
FREEZE_TREE_COUNTER_EXIT=1
```

Despite the freeze tree having no S075 row, the counter prints `0/5`: `c2-count.py`
line 18 hardcodes `--root /home/vgpnk/Projects/shokunin` and
`CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`, so `<n>` follows
ambient fleet state, not the tree the counter file lives in.

### R7 — census against the stripped copy itself

A mirror root pointing `chousa-shokunin` at the stripped copy, with the fleet conf:
rc 0, five W04 rows (same ids as R4). The copy's committed `SOURCES.md` supports `n = 5`.

### R8 — auxiliary (not the assigned attack): extra-id kill rule

Fleet TSV + one bogus row `S999` → `W04_DISPOSITIONED=5/5`, `WARN S999: disposition
row without a census warning`, exit 0. `claims.md` says "a TSV naming ids not in the
census output … fails the counter", and the counter docstring says such a row "counts
as undispositioned"; the implementation only warns (`extra` list, no `bad` entry).
Flagged for the C2 critic/mutation seats; not counted in this report's verdict.

## Verdict

1. **Control-match clause: PASS.** The stripped-copy run prints `W04_DISPOSITIONED=0/5`
   and exits 1; stdout + `BEFORE_EXIT=1` is byte-identical to the committed
   `controls/c2-control-before.txt` (R2, rc 0).
2. **Literal expectation `0/4`: FALSIFIED.** The measured pinned tree yields
   `0/5`, because `S075` is a committed row at HEAD (blob `d97529e…`). Four is the
   count only at freeze commit `b173b09` (blob `6a3d076…`), where `S075` does not exist.
3. **C2 before-state at the measured revision: `0/5`, exit 1.** That is also the
   frozen claims' join-based form (`0/<n>`, `n` = census warnings at the measured
   revision), so the claim text is satisfied; the dispatch's `0/4` is stale relative
   to the landed tree and the control.

## Mechanism / provenance notes

- `S075` (mktemp row) was introduced by `1bd9001` ("… W04 dispositions (5/5); S075/S076 …"),
  one commit after the freeze commit that contains `c2-control-before.txt`. The control
  committed at `b173b09` already names `S075`, so it was generated from the pre-commit
  worktree that became `1bd9001`, not from `b173b09`'s committed bytes. It becomes
  exactly reproducible from `1bd9001` / HEAD onward; this is the only revision where
  the control and the tree agree.
- Consequently `0/4` is not reachable with the committed counter without editing the
  hardcoded census root or replacing the fleet root: a copy-based rerun always measures
  the live fleet lane. The copy test exercises the missing-TSV branch, not the copy's
  corpus; R7 covers the copy's corpus separately.
- `corpus/SOURCES.md` at both HEAD and `b173b09` is git-clean; no worktree-only
  content affected the counts (`git status` clean for that path; blob equality checked).

## Files changed

- `.ufo/waves/round-41/w1/ExecC2Before.md` (this report) — sole write.

No production files, counters, controls, TSV rows, receipts, git index, jj state, fleet
repo, or sibling repos were touched. Scratch evidence lives under
`/tmp/exec-c2before-r41/` (ephemeral; all decisive outputs are inlined above).

## Risks / blockers

- Do not "repair" the control to `0/4`: at the measured tree the control is correct and
  reproduces exactly. Editing it would make it non-reproducible.
- The counter is non-hermetic: its census invocation binds the absolute fleet root and
  an unpinned fleet script (`scripts/sources-census.sh`, sha256 above). A future change
  to that script or to the fleet lane silently changes `n` for any copy run.
- Auxiliary R8: the documented extra-id kill rule is not enforced (warn-only). This
  does not affect this before-state verdict but weakens C2's stated calibration.
- Blocker check: none. The assigned run was performed end-to-end; the only unmet part
  is the dispatch's literal `0/4`, which the data falsify rather than an environment gap.
