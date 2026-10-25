# ConnectorSiblingScan — round 41

Attack: read-only scan of sibling lanes under `/home/vgpnk/Projects/shokunin` for tool-invocation pins and capture/drift gates in the mori census lineage; where chousa's `CAPTOOL` table could be reused; whether any sibling artifact contradicts the r41 mechanism. No production edits. No network. No installs.

Command (committed blobs, not worktree):

```text
git -C mori-shokunin rev-parse HEAD:tools/mori-census.sh
git -C chousa-shokunin rev-parse HEAD:tools/research-gate.sh
git -C tsukuroi-shokunin rev-parse HEAD:tools/probe-git-child-env-r31.py
git -C tsukuroi-shokunin rev-parse HEAD:tools/tsukuroi-census.sh
git grep -n -e --drift -e --pin HEAD -- tools   # each sibling lane
```

Output (this run):

```text
mori-shokunin     HEAD=d72ac1675352  tools/mori-census.sh blob=c7d952d6fabe
chousa-shokunin   HEAD=872bf3a35078  tools/research-gate.sh blob=ae10363a68ba
tsukuroi-shokunin HEAD=564db0b614b2  tools/probe-git-child-env-r31.py blob=953043991d8e
tsukuroi-shokunin HEAD=564db0b614b2  tools/tsukuroi-census.sh blob=10b6d47046c9
```

`git grep -- tools` for `--pin`/`--drift` outside chousa hits only `mori-shokunin/tools/mori-census.sh` (the lineage gate) and `souji-shokunin/tools/impl-35.sh` (plus impl-38/impl-47 `--drift` flags). Those souji flags are docs-vs-installed / reconcile drift, not a capture baseline. Census blob `c7d952d6fabe` was unchanged across a HEAD move `62a207f7521f` → `d72ac1675352` during the scan. Chousa `tools/research-gate.sh` was clean against `872bf3a35078`.

## Evidence

**Who runs a capture/drift gate.** The only sibling production gate in the mori r10 lineage is `mori-census.sh`. Chousa's committed gate says so: `tools/research-gate.sh:221-225` ("adapted from mori-shokunin r10") and the baseline stamp at `:4301` (`lineage: mori-shokunin r10 pin/drift`). Mori's contract is `--pin` writes one baseline, `--drift` writes nothing, volatile fields masked, `MORI_DRIFT: none` or named tokens (`mori-census.sh:170-213`, `:2920-3002`).

Other censuses are not that gate:

| lane | artifact | what it pins / drifts | CAPTOOL-shaped? |
|---|---|---|---|
| mori | `tools/mori-census.sh` `c7d952d6fabe` | `--pin`/`--drift`; seven bins default to bare names (`:314-320`) | no |
| tsukuroi | `tools/tsukuroi-census.sh` `10b6d47046c9` | `have()` is `command -v` (`:548`); no `--pin`/`--drift` | no |
| tsukuroi | `tools/probe-git-child-env-r31.py` `953043991d8e` | strace of 11 git-spawning tools; not a drift baseline | no |
| souji | `tools/souji-census.sh` `5aa8101cdcf2` | `command -v git/du/setsid` (`:3045-3047`); `--compare`, not `--pin` | no |
| souji | `tools/impl-35.sh:5`, impl-38, impl-47 | `--drift` = docs vs installed tools, or reconcile | no |
| fleet | `scripts/sources-census.sh` | SOURCES.md census; `date`/`realpath`/`gawk` by name; no pin/drift | no |
| tameshi | `tools/command-binding.py` | digest-pins declared receipts; does not resolve live PATH tools | no |

No sibling `tools/` tree contains `CAPTOOL`, a `GNU coreutils` `--version` probe, or `CAP_CHILD_PATH`. Lanes with an empty `tools/` at HEAD (audio, both game-dev, kagi, kake, kasegi, kengaku, kotoba, kumitate, lore, revenger, tabi) have nothing to reuse.

**Where the table would actually fit.** Mori's compared drift bytes still call two CAPTOOL names by PATH:

- `drift_normalize` (`:2776-2791`) runs bare `sed -E` (`:2779`). Both `--pin` (`:2923`) and `--drift` (`:2984`) take that stdout as the canonical block that is byte-compared (`:2990`). A `sed` that exits 0 without masking is chousa S3 on the ancestor: volatile counters become drift, or an empty canon trips `empty canonical block` (`:2973-2975`).
- `drift_report` (`:3000`) runs only when the bodies differ, then `LC_ALL=C sort -u` (`:2916`) orders `MORI_DRIFT` tokens. That is chousa S7 (sort fires only on drift reports). A reversing `sort` changes token order without changing the set.

`date` (`:383-384`) and `sha256sum | cut` (`:379`) also run at startup. They feed `pinned_ts` and `census_sha256`, which the header itself calls informational (`:2929`: "census_sha256 is informational (behavior, not revision, is compared)"). A hostile `cut` cannot flip `MORI_DRIFT`. Those two are the chousa r35/r37 hash-pipe class, and they are **not** `CAPTOOL_NAMES` rows. Chousa pins `sha256sum` with a separate `sha256_pin_bin` and deleted `cut` rather than adding it to the table (`research-gate.sh` comments at `:498-507`). Reusing CAPTOOL does not close mori's header pipe.

**Where the table must not be reused.** `MORI_*_BIN` defaults are bare names on purpose: `df pgrep journalctl jq tmux timeout git` (`:314-320`). Selftest points the overrides at absolute fixture dispatchers (`$bin/git` and siblings). A GNU-coreutils/`GNU sed` `--version` probe refuses `jq`, `git`, `journalctl`, `tmux`, and `pgrep` (procps). Tsukuroi's eleven git tools (`probe-git-child-env-r31.py:63-76`) are the same non-fit. `tsukuroi-census.sh` probes `pacman` / journal / systemd, not coreutils.

## Contradiction (not smoothed)

Three committed contracts disagree on the child environment of a measured child. They are not the same surface, and the lineage stamp does not make them one mechanism.

1. **mori `git_cap`** (`c7d952d6fabe:578-594`): scrub is only `GIT_DIR` / `GIT_TRACE*` / `GIT_CONFIG*` via `env -u`. The comment states `PATH`, `HOME`, and every other variable stay inherited so fixture stubs and the live path keep working. `LD_PRELOAD` is therefore passed through. `GIT_CONFIG_NOSYSTEM` is unset, not forced on.
2. **chousa r41 capture child** (`ae10363a68ba:4071`, `:4153-4154`): `PATH` is replaced with `CAP_CHILD_PATH` (default `/usr/bin:/bin`) and the child env unsets `LD_PRELOAD` and `LD_LIBRARY_PATH`. `BASH_FUNC_*` is a named limit. This child is `bash verify-all`, not `git`.
3. **tsukuroi r31** (`953043991d8e:18-42`): control is `PATH=/usr/bin:/bin` with every `LD_*` removed. `loader-env` is a LEAK if any later execve still carries `LD_PRELOAD` / `LD_LIBRARY_PATH` / `PYTHONPATH`. `child-contract` is a LEAK if a git exec lacks `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_SYSTEM=/dev/null` (unset is the failure, not the fix).

So mori contradicts r41's loader half (inherit PATH and `LD_*` vs replace PATH and unset `LD_*`) and contradicts tsukuroi's git half (unset `GIT_CONFIG*` vs require the null-system triple). Tsukuroi does not contradict r41's frozen capture predicate: r41 never claims a git child, and both strip `LD_*` and pin a `/usr/bin:/bin` path. Copying r41's `-u LD_PRELOAD` into `git_cap` would falsify mori's own sentence at `:578-579`. Copying tsukuroi's `GIT_CONFIG_*=/dev/null` into r41's verify-all child would be a different claim than C1.

The baseline line `lineage: mori-shokunin r10` is attribution of the volatile-field compare, not evidence that the ancestor's invocation surface is pinned. Treating it as mechanism identity is the false reading.

## Proposed move

Reuse only the two CAPTOOL rows that sit on mori's **compared** drift path: `sed` in `drift_normalize` and `sort` in `drift_report`, with the existing absolute-path default (`/usr/bin` then `/bin`), GNU `--version` probe (`GNU sed` / `GNU coreutils`), and absolute-only override refusal.

Do not port `CAPTOOL_NAMES` onto `MORI_*_BIN`, onto tsukuroi's git tools, or onto souji's docs-drift flags. Do not copy `-u LD_PRELOAD` or `CAP_CHILD_PATH` into `git_cap`. Do not count `sha256sum|cut` or `date` as covered by that reuse: the header says they are outside the compare.

This is a boundary for a later mori edit. It is not a patch in this wave.

## Axes

- **Operability:** improved as a claim boundary. The two PATH calls that can change `MORI_DRIFT` bytes are the same class C1 just closed (`sed` mask, `sort` token order). Leaving the seven non-GNU bins bare avoids a pin that cannot pass its own probe.
- **Calibration:** not harmed. The move refuses the false join "lineage header ⇒ invocation surface already pinned" and refuses to score `sha256sum|cut` as a CAPTOOL gap on the drift compare.
- **Depth:** not harmed. No shared pin library (mori's census is a standalone script by its own git-scrub comments). One table, two call sites.

## Risks

- A GNU-only `sed` probe rejects a non-GNU `sed -E` that mori accepts today. That is a behavior change on the ancestor, not on chousa's counter.
- `sort` is unreachable on the `MORI_DRIFT: none` path (`drift_report` runs only after the bodies differ, `:2990-3000`). A none-only check would call the pin vacuous. Same limit chousa already names for S7.
- Porting the scrub from either r41 or tsukuroi into `git_cap` breaks the other contract. The three-way loader disagreement stays unresolved until a lane owns it; this move does not pick a winner.
- Mori HEAD moved during the scan. Cite blob `c7d952d6fabe`, not a floating worktree.

## Verification

Already exercised: the `git rev-parse` / `git show` / `git grep` lines above, against blobs `c7d952d6fabe`, `ae10363a68ba`, `953043991d8e`.

Not exercised (would be a mori-lane edit plus a live census): a PATH `sed` that `exit 0` on `mori-census.sh --drift` of a known-clean baseline must stop printing `MORI_DRIFT: none`; a reversing `sort` must change a multi-token `MORI_DRIFT` line; deleting only the `sed` wrapper must restore the first failure. Do not use `MORI_JQ_BIN` / `MORI_GIT_BIN` as the mutant — those are outside the proposed rows.

Verdict: **reuse is two names (`sed`, `sort`) on `mori-census.sh`'s compared drift path; the rest of CAPTOOL does not transfer; mori's inherit-PATH/`LD_*` contract contradicts r41's capture-child contract and tsukuroi's git-child contract, and the lineage stamp does not reconcile them.**

Artifact: `mori-shokunin` blob `c7d952d6fabe` (`tools/mori-census.sh`); `chousa-shokunin` blob `ae10363a68ba` (`tools/research-gate.sh`); `tsukuroi-shokunin` blob `953043991d8e` (`tools/probe-git-child-env-r31.py`).
