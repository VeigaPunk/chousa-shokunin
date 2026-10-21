# ResC3Clause: C3 filesystem-denylist clause against landed cb895a2

**Verdict: FALSIFIED (clause-scoped). C3 as frozen: partially falsified.**

The r26 failure class is closed at cb895a2. The landed predicate still refuses clean complete filesystem paths solely on their first-colon prefix. That contradicts the frozen wording "must inspect complete filesystem paths, not citation-anchor prefixes". Most of these refusals are inherited from base. One is new in r27: the claims canonical arm.

This is author-lane advice, not outside admission. Seat: `ChousaR27-2.ResC3Clause-16`, a read-only leaf. No installs or updates.

## Setup
- Sandbox: `/tmp/chousa-r27-residual-ResC3Clause/{base,dd,cb}`. Each is a `git archive` of 64eec5d, dd72641 and cb895a2. Exit 0.
- Gate digests:
  - base: `c2c813f1…abc6`
  - dd: `ca39d14d…2f84`
  - cb: `a6bc2855…2386` (matches the assignment)
- The dd→cb diff has no denylist line. `diff dd cb | grep -ciE 'deny|ptr_file_part'` prints 0. So the predicate under test is byte-identical in dd and cb.
- Mutant `mut/fullonly.sh` (sha256 `da72d82e…`) is cb with `is_denylist_fs_path` reduced to `is_denylist_path_value "$f"`, i.e. the prefix arm removed. Nothing else changed.
- Probe `fx/probe.sh` (sha256 `18f1bad7…`):
  - fresh synthetic root per case;
  - `env -i PATH LC_ALL=C CHOUSA_STRICT=0`;
  - three surfaces: `verify-metadata --registry`, a `verify-metadata` entry, and a `verify-claims` source.
  - Command: `bash fx/probe.sh mut/<g>.sh <g>` for g in base, dd, cb, fullonly. Each probe exits 0.
- Code under attack, from `tools/research-gate.sh@cb`:
  - `ptr_file_part` (573-576) is `${p%%:*}` after `norm_ptr`, which strips a leading and a trailing backtick.
  - `is_denylist_fs_path` (609-613) is "full path OR `ptr_file_part` prefix".
  - Filesystem callers: claims at 1139 and 1166, registry at 2394 and 2401, entry at 2613 and 2620.
  - The registry opens `"$canon"` of the complete argument (2396). No anchor is stripped before the open.

## Q1. Is the r26 class (an earlier colon hiding a denylisted complete path) closed at cb895a2? **Yes.**
I used 16 inputs:
- `a:b/.config/f.md`, `a:secret.env`, `synthetic:fixture.env`, `benign:x/credentials/f.md`, `a:b/x/oauth/f.md`;
- `a:b/.omp/f.md`, `a:b/.local/state/f.md`, `a:b/server.token.md`, `a:b/Cookies`, `a:b/chrome-profile/f.md`;
- `a:b:c/.config/f.md`, `a:op.env`, `a:b/Login Data`;
- symlink `plain.md -> a:b/.config/f.md` (canonical arm);
- root `x:y/` with `plain.md -> .config/f.md` (root-colon canonical);
- relative `a:b/.config/f.md` with cwd=root.

| surface | base | dd | cb | fullonly |
|---|---|---|---|---|
| registry, 16 inputs | 16 READ (rc0 `RESEARCH_GATE: CLEAN`) | 16 DENY | 16 DENY (rc2 `refused: denylist`) | 16 DENY |
| entry, 11 reachable | 11 READ (rc0 CLEAN) | 11 DENY | 11 DENY (rc1 `META_ENTRY_REFUSED … reason=denylist`) | 11 DENY |
| claims, 16 inputs | 16 READ (rc0 CLEAN) | 16 DENY | 16 DENY (rc1 `CLAIM_SOURCE_SESSION`) | 16 DENY |

- Five entry names do not end in `.md` (`a:secret.env`, `synthetic:fixture.env`, `a:op.env`, `a:b/Cookies`, `a:b/Login Data`). They exit rc2 with `metadata path is not a .md file or directory` before the reader runs, so no read happens on any gate.
- Decisive point: the full-path-only mutant keeps every Q1 refusal. The closure comes entirely from the complete-path arm. The prefix arm contributes nothing to closing the r26 class.
- Negative controls are READ rc0 on all four gates: `synthetic:ordinary.md`, `notes.env/f.md`, and `x:.config/f.md` (its component is `x:.config`). There is no over-refusal of plain colons.

## Q2. Does the retained prefix arm violate the frozen clause's plain wording? **Yes.**
Frozen text, `corpus/evidence/round27-claims.md:15`: "Filesystem-path denylist checks must inspect complete filesystem paths, not citation-anchor prefixes; preserve existing citation-pointer semantics."

Landed counterexamples. In every row the complete path matches no denylist pattern, cb refuses, and fullonly reads it.

| input (complete path under a fresh root) | registry cb / fullonly | entry cb / fullonly | claims cb / fullonly | base |
|---|---|---|---|---|
| `k.env:1` | rc2 deny / rc0 CLEAN | n/a (not .md) | rc1 deny / rc0 | deny |
| `k.env:notes.md` | rc2 / rc0 | rc1 / rc0 | rc1 / rc0 | deny |
| `notes.env:v2/f.md` | rc2 / rc0 | rc1 / rc0 | rc1 / rc0 | deny |
| `metadata.env:1.md` | rc2 / rc0 | rc1 / rc0 | rc1 / rc0 | deny |
| `.env:1` | rc2 / rc0 | n/a | rc1 / rc0 | deny |
| `a/op.env:3` | rc2 / rc0 | n/a | rc1 / rc0 | deny |
| root dir `proj.env:2/`, file `corpus/f.md` | rc2 / rc0 | rc1 / rc0 | rc1 / rc0 | deny |
| `plain.md -> k.env:1` (canonical) | rc2 / rc0 | rc1 / rc0 | **rc1 / rc0** | registry and entry deny; **claims READ** |
| `` x.env` `` (trailing backtick) | rc2 / rc0 | n/a | deny / deny | deny |
| relative `` `.config/f.md `` | rc2 / rc0 | rc1 / rc0 | deny / deny | deny |

Totals: registry 10, entry 6, claims 8. These are refusals decided only by text before the first colon, or by backtick normalization, on a path the gate would otherwise open by its complete name.

Why "preserve existing citation-pointer semantics" does not cover them:
- These three surfaces open the complete name. The registry opens `$canon` (2396). Claims build `cand` from the whole `src` (1157-1165).
- A `:N` suffix on these surfaces is part of a file name, not an anchor.
- Citation-pointer callers are separate and untouched: `check_pointer` 660, `ptr_resolves_meta` 631, and `chain_ref_file` 1613 still use `is_denylist_path`.

Not inherited, new in r27:
- `claim_source_path` at base checks only `is_denylist_path "$src"` (base 1129). It has no canonical denylist arm.
- r27 added `is_denylist_fs_path "$canon"` at cb 1166. Its prefix arm refuses the claims alias `plain.md -> k.env:1`, which base reads (probe row `claims q3-alias-to-env1`: base READ rc0; dd and cb DENY rc1).
- So r27 extended citation-prefix refusal to a new complete canonical path. That runs directly against the clause, not merely an inherited residual.
- The landed gate's prefix arm on the root's canonical path means every registry, entry and claims file under a root whose path contains `X.env:` is refused. Example: root `proj.env:2/` above.

## Q3. Would dropping the prefix arm un-refuse anything base refused? **Yes. It is not a denylisted-path read.**
- Inputs base refuses that a full-path-only predicate would open: every Q2 row whose base column says deny.
  - Concrete synthetic names: `k.env:1`, `k.env:notes.md`, `notes.env:v2/f.md`, `metadata.env:1.md`, `.env:1`, `a/op.env:3`, root `proj.env:2/…`, `plain.md -> k.env:1` (registry and entry), `` x.env` ``, and relative `` `.config/f.md ``.
  - Surfaces: registry 10, entry 6, claims 7 (the claims alias is not base-refused).
- Why only these shapes: the patterns at 597-605 are monotone under prefix-to-full extension, except the suffix globs `*.env` and `*op.env`. Backtick stripping in `norm_ptr` is the second source. So the un-refused set is exactly "first-colon prefix (or backtick-trimmed text) ends in `.env`/`op.env`, or bare-starts `.config/` / `.omp/` / `.local/state/`, while the complete path does not match".
- None of these opens a file whose complete path or canonical target is denylisted. `k.env:1` is a different directory entry from `k.env`, and `` `.config `` is a different directory from `.config`. The raw, canonical and `/proc/$$/fd` arms keep full-path refusal (Q1: fullonly 43/43 DENY).
- Net: dropping the arm narrows a base refusal set. That is an over-refusal by name shape, which is a monotonicity tradeoff on the no-harm axis. It does not expose any path the denylist defines as secret.
- Suites on a cb tree with only the gate swapped to fullonly, run with `bash -c 'cd full; …'`:
  - `round27-regressions.py --gate tools/research-gate.sh`: rc1, `mismatches: 2`, `MISMATCH C3 legacy-env-anchor-refusal exit 0 != 2` and `MISMATCH C3 claims-legacy-env-anchor-refused missing 'FINDING CLAIM_SOURCE_SESSION'`.
  - `round27-falsify-controls.py --gate tools/research-gate.sh`: rc0 (26/26).
  - `bash tools/research-gate.sh --selftest` (UTF-8 locale inherited, LANG=en_US.UTF-8): rc1, `FAIL-case metadata-colon-anchor-denylist-compat … obs=entry=metadata.env:1.md reason=denylist`, `RESEARCH_GATE_SELFTEST: FAIL (1/215 cases)`.
  - The same three on cb: regressions rc0 (58/0), falsify-controls rc0 (26/0), selftest rc0 `PASS (215 cases, 0 skipped)`.
- The three checks that fail are exactly the prefix pins. `grep -c colon-anchor-denylist-compat` gives base 0, dd 1, cb 1, so the selftest pin is new at dd. Its provenance is the build-wave monotonicity decision, not the claim text:
  - `build/CriticPathScope.md` CX1 and control 5 ("Monotone guard: registry `w/k.env:1` still refused");
  - `build/ConnectFailures.md` ("the union is mandatory");
  - `corpus/lessons/round-27.md:91` ("accepted monotonicity constraint").

## Classification
- **Landed-gate counterexample (wrong behavior against the frozen text):**
  - the Q2 rows on all three surfaces;
  - the claims-canonical prefix refusal, which r27 newly introduced.
- **Inherited (base-identical):** the registry and entry Q2 rows, and the claims raw-source rows. Base refuses them by the same `ptr_file_part` prefix.
- **Control and coverage weaknesses:**
  - `legacy-env-anchor-refusal`, `claims-legacy-env-anchor-refused` and selftest `metadata-colon-anchor-denylist-compat` encode the prefix behavior the clause excludes. No persisted control asserts that a clean complete path like `k.env:notes.md` is read.
  - The refusal observation names the prefix, not the denied path. Claims `a:b/.config/f.md` emits `obs=path=<root>/a denied (not opened)`, a non-denylisted path (`claim_source_path` 1141/1168; same format at base).
  - Directory-mode `verify-metadata <dir>` did not descend into `a:b/.config/`, `k.env:1/` or `notes.env:v2/` subdirectories on any gate (rc0, `entries=1`). Nested colon directories are untested through directory mode.
- Report findings reproduced:
  - FC3ColonDeniedSuffix46 §3 (`reg.env:notes.md` family);
  - FC3PlainDeniedComponent44 C-A (`notes.env:v2/registry.md`);
  - FC3EntryColonDeniedCompon50 CX4 (`notes.env:v2/entry.md`, `cfg.env:notes.md`);
  - FC3LegacyEnvAnchorRefusal47 and FC3ClaimsLegacyEnvAnchorR57 (the control pins prefix behavior).
  - All reproduce unchanged at cb895a2.

## C3 verdict as frozen: **partially falsified**
- Verified parts:
  - The r26 failure class (FRegistryRegistryDeny) is closed on registry, entry and claims, including the raw, canonical, fd and root-colon arms.
  - Ordinary colons are allowed.
  - Citation-pointer callers are unchanged.
- Falsified part: "must inspect complete filesystem paths, not citation-anchor prefixes".
  - `is_denylist_fs_path` makes prefix-only refusals on complete filesystem paths across all three surfaces: 10, 6 and 8 synthetic inputs above.
  - r27 widened this to the claims canonical path.
  - The clause has no legacy or monotonicity exception, so the landed union cannot satisfy it as worded.
- I did not re-adjudicate the registry-header and S-id parts of C3 here.

## Smallest safe correction (judge's tradeoff; no claim redefinition)
- **Option 1.** Remove line 612 (the prefix arm). Retire or invert the three pinning checks together, and add positive read controls (`k.env:notes.md`, `notes.env:v2/f.md`, the claims alias to `k.env:1`).
  - The base-refused names listed in Q3 then become readable. That is a disclosed monotonicity narrowing with no denylisted path exposed.
- **Option 2.** Keep the union and record the C3 denylist clause as not met.
- Shipping the union while claiming the clause is verified is the one unsafe combination.
