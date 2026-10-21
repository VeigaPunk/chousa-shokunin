# FRegistryRegistryDeny — C3 `--registry` denied-path refusal (round 26 attempt 1, falsify)

Seat: `ChousaR26R.FRegistryRegistryDeny` (scout, leaf). Author-lane advice only; not an outside judge.

**Verdict: C3 registry denial is FALSIFIED for one input class.** A registry path that contains a
denylisted component (`/.config/`, `/.omp/`, `*.env`, `*credentials/*`, …) is opened, read and parsed
whenever a `:` appears anywhere earlier in the path. 16/16 colon-free deny shapes held (refused
before any `openat`), 6/6 colon shapes bypassed (rc=0, bytes read, table parsed to `CLEAN`).

## Identity

- Target: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from `corpus/evidence/round26-measured-revision.json`),
  `git archive` into `/tmp/chousa-r26-falsify-FRegistryRegistryDeny/tree`.
  `sha256 tools/research-gate.sh = c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`
  (equals the revision file's pinned input hash).
- Claim base: `ba3333254dd337658a4f25e7a9471f9cf4e4567e`, archived to `…/base`,
  `sha256 tools/research-gate.sh = 985a63200ca4c5712806d8752ba27a8f3448b026f773659079e71ca602e56ef7`.
- Lane HEAD observed at start: `0e9784bd52eca456b24d0bc40921480a47f91a2b`.
- Tools: GNU bash 5.3.20, strace 7.2 (`-f -qq -y -e trace=openat,read`). No installs or updates.
- Semantic navigation: no LSP device was available to this seat; symbol locations below are from
  literal text search plus reading the cited ranges (not semantic proof).

## Code under attack (observed)

- `tools/research-gate.sh:573-576` `ptr_file_part` returns `${p%%:*}` — everything before the first `:`
  (built to strip `path:line` citation anchors).
- `:595-606` `is_denylist_path` matches its globs against `ptr_file_part "$1"`, not the full path.
- `:2361-2407` `metadata_registry_load` calls `is_denylist_path` on the raw path, the `readlink -f`
  canon and the `/proc/$$/fd` canon. All three are filesystem paths, so all three are truncated at the
  first `:` before matching.
- The registry is loaded (`:2570-2571`) before any entry is opened, and only after `-e/-r/-f` stat tests.

## Harness

`/tmp/chousa-r26-falsify-FRegistryRegistryDeny/run.sh` (sandbox only). Fixed entry
`w/corpus/knowledge/e.md` (`source: S001`, dated+checked, `90d`); every registry fixture holds the
same valid table `| S001 | mined | corpus/knowledge/e.md |`, so a CLEAN exit 0 proves the protected
fixture's bytes were parsed. Each run:
`strace … bash GATE verify-metadata w/corpus/knowledge/e.md --root w --registry REG`, where
`open_prot`/`read_prot` = the protected fixture path appears in an `openat(` / `read(<path>)` trace line.
Command: `bash run.sh` → harness_rc=0; raw outputs in `…/out/*.out`, traces in `…/out/*.trace`.

| id | registry path (under `w/`) | rc | open | read | first gate line |
|---|---|---|---|---|---|
| P0 | `reg.md` (positive control) | 0 | yes | yes | `RESEARCH_GATE: CLEAN (entries=1 … findings=0 drift=0)` |
| D1 | `.config/reg.md` (absolute) | 2 | no | no | `research-gate: metadata registry refused: denylist` |
| D2 | `.config/reg.md` (relative, cwd=w) | 2 | no | no | same |
| D3 | `benign.md` → symlink to `.config/reg.md` | 2 | no | no | same |
| D4 | `cfg/reg.md`, `cfg` → symlink dir `.config` | 2 | no | no | same |
| D5–D6 | `.omp/reg.md`, `.local/state/reg.md` | 2 | no | no | same |
| D7–D8 | `secret.env`, `op.env` | 2 | no | no | same |
| D9–D10 | `x/credentials/reg.md`, `x/oauth/reg.md` | 2 | no | no | same |
| D11–D14 | `server.token.md`, `chrome-profile/reg.md`, `b/Cookies`, `b/Login Data` | 2 | no | no | same |
| D15–D16 | `.config/../.config/reg.md`, `./cfg/../.config/reg.md` | 2 | no | no | same |
| D19 | `/proc/self/fd/7` with `7<w/.config/reg.md` | 2 | — | no | same |
| D17 | `.config/none.md` (absent) | 2 | no | no | `metadata registry not found` |
| D18 | `.config` (directory) | 2 | no | no | `metadata registry is not a regular file` |
| H1 | `hl.md`, hardlink of `.config/reg.md` | 2 | yes | **no** | `metadata registry refused: multilink` |
| **B1** | `a:b/.config/reg.md` | **0** | yes | **yes** | `RESEARCH_GATE: CLEAN …` |
| **B2** | `a:secret.env` | **0** | yes | **yes** | same |
| **B3** | `m:x/credentials/reg.md` | **0** | yes | **yes** | same |
| **B4** | `plain.md` → symlink to `a:b/.config/reg.md` | **0** | yes | **yes** | same |
| **B5** | `run/user/1000/gvfs/sftp:host=h/home/u/.config/app/reg.md` | **0** | yes | **yes** | same |
| **B6** | `c:/.omp/agent/reg.md` | **0** | yes | **yes** | same |
| S1–S10 | `home/` + `.ssh/id_ed25519`, `.aws/credentials`, `.netrc`, `.git-credentials`, `.docker/config.json`, `.kube/config`, `.pgpass`, `.mozilla/firefox/p.default/logins.json`, `.gnupg/private-keys-v1.d/k.key`, `.local/share/keyrings/login.keyring` | 0 | yes | yes | `RESEARCH_GATE: CLEAN …` |

B1 trace excerpt (`out/B1.trace`):
`openat(…, "…/w/a:b/.config/reg.md", O_RDONLY) = 3` then
`read(0<…/w/a:b/.config/reg.md>, "| id | status | used-by |\n|---|-"..., 4096) = 81`.
D1-class traces contain zero lines naming the protected path (`grep -cF '.config/reg.md' out/D1.trace` → 0).

Non-table variant: `--registry e/a:b/.config/gh/hosts.yml` holding `oauth_token: FIXTURE-NOT-A-SECRET`
→ rc=2 `metadata registry has no table with id, status, and used-by columns`, but the trace shows
`read(0<…/a:b/.config/gh/hosts.yml>, "oauth_token: FIXTURE-NOT-A-SECRE"..., 4096) = 34`. An exit 2 here is
not a refusal: the bytes were already read.

## Mutation controls (QUALITY 17, sandbox copies only)

- **M1** `m1-nodeny.sh`: `sed -i -e '2375s/…is_denylist_path "$path" || is_denylist_path "$canon"…/if false; then/' -e '2382s/…|| is_denylist_path "$fdcanon"…/if [[ -z $fdcanon ]]; then/'`
  (diff: exactly lines 2375 and 2382). `GATE=m1-nodeny.sh bash run.sh`: D1, D3, D7 and D19 flip to
  rc=0 with read=yes; P0 is unchanged; H1 still refuses `multilink`. The harness therefore detects a
  lost registry denylist arm for that reason, not because of a parse error.
- **M2** `m2-fullpath.sh`: `sed -i '596s/f=$(ptr_file_part "$1")/f=$(norm_ptr "$1")/'` (diff: line 596
  only). `GATE=m2-fullpath.sh bash run.sh`: B1–B6 become rc=2 `refused: denylist` with open=no and read=no;
  P0, D1–D19 and H1 are identical to the unmutated target. The single cause is the `:` truncation in
  `ptr_file_part` used for filesystem paths. M2 is a diagnostic only. It also changes citation-pointer
  denylisting globally, so it is not a proposed patch.

## Findings

- **FRRD-1 — crit, falsifies C3 denial (registry).** `metadata_registry_load` does not refuse a
  denylisted path when a `:` comes earlier in the raw, canonical or fd-canonical path. It opens,
  reads and parses the bytes, and its findings depend on them (B1–B6 rc=0 CLEAN). The claim text
  ("read through the same fd-bound, size-capped, denylist/…-refusing reader") does not hold for this
  input class. Real paths with this shape include gvfs/sshfs mounts (`/run/user/<uid>/gvfs/sftp:host=…/home/<u>/.config/…`)
  and any project directory whose name contains a `:`. [INFERENCE] The real host has no such mount;
  only sandbox fixtures were exercised.
- **FRRD-2 — inherited, not introduced by r26.** The entry reader has the same bypass. With
  `e/.config/e.md` the run gives rc=1 and `source=refused … verdict=drift` at both target and base. With
  `e/a:b/.config/e.md` it gives rc=0 and `source=present verified_at=dated recheck=scheduled verdict=clean`
  at both target and base. C3 inherited the defect by reusing `is_denylist_path`. At base, `--registry`
  exits 2 `unknown flag: --registry`.
- **FRRD-3 — coverage gap (QUALITY 17).** The target selftest has 8 registry cases (missing-row,
  not-mined, used-by-path, verified-at-bare, no-token-id, positive-continuations,
  duplicate-first-row, refused-nul). None exercises a registry denylist, symlink, multilink, size or
  stat refusal. `round26-registry-oracle.py`, `round26-registry-differential.sh` and
  `round26-measure.sh` contain no deny or refusal case. [INFERENCE, selftest not run per the
  verification contract] With the M1 mutation applied, the selftest would still pass.
- **FRRD-4 — calibration/scope note, not a pattern defect.** Unlike entries (`*.md` required at
  `:2566-2567`), the registry accepts any regular file name. Credential-bearing files outside the
  denylist patterns (S1–S10: `.ssh`, `.aws/credentials`, `.netrc`, `.git-credentials`, `.docker`,
  `.kube`, `.pgpass`, Firefox `logins.json`, `.gnupg`, keyrings) are read and parsed. The C3 text
  promises only "denylist-refusing", so this matches the claim. Any wording of the form "refuses
  protected host files" would overclaim. The denylist scope (`:595-606`) is shared legacy.
- **FRRD-5 — low, spec-compliant.** Because `-e/-r/-f` run before the denylist (`:2370-2375`), an
  absent denylisted path reports `not found` (D17) while a present one reports `refused: denylist` (D1).
  Both exit 2, which is an existence oracle for protected paths. No bytes are read in either case.

## Held (observed)

The registry refuses before `openat` for every colon-free denylist shape, including absolute,
relative, symlinked-file, symlinked-directory, `..`-normalized and `/proc/self/fd/N` aliases (D1–D16,
D19). A hardlink alias is opened but refused `multilink` before any `read` (H1). Registry refusal
happens before any entry is opened, because the load at `:2571` precedes the entry loop.

## Not attacked

Bind-mount and namespace aliases; open-time races (for example, swapping in a FIFO after `-f`); the
size/stat/read refusal arms; composition with `--as-of`. No full selftest, build, lint, formatter or
8 MiB probe was run. No production file was edited.
