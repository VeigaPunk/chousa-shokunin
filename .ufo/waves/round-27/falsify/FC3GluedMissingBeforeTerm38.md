# FC3GluedMissingBeforeTerm38 — C3 `glued-missing-before-terminal`

**Verdict: HOLDS for the control as declared** (its expectation derives from the declared contract, and the targeted rescanning mutant is killed for the intended reason). **Coverage: FALSIFIED** — the control is not a liveness witness, and the C3 suite cannot see two same-class regressions (exact-three-digit width; unpinned locale). **Landed gate: no counterexample found** across 19 nearby synthetic inputs. This is author-lane advice, not an outside admission.

Axes: calibration (expectation vs. contract; does the kill hit the targeted mechanism), operability (ordinary gate output, no setup or parse failure), freshness (all runs on `dd72641e574679c4f7882dd43de072b4c8892d6f`; landed gate sha256 `ca39d14d…2f84`, matching the assignment; base is `64eec5d`, read-only `git show`, sha256 `c2c813f1…`; `round27-regressions.py` sha256 `5afea786…`).

Sandbox: `/tmp/chousa-r27-falsify-FC3GluedMissingBeforeTerm38` (archive of `dd72641e`). The lane's production files, index, and history were not changed. This report is the sole lane write.

## 1. Is the expectation derived from the contract, independent of gate code? — HOLDS

- Control: `corpus/evidence/round27-regressions.py:154` `('glued-missing-before-terminal', 'see S001S003 and S001', 0, 0)`. Assertions (`observe`, :31): exit 0, and `^FINDING META_SOURCE_` count 0 (plus an inert S002 pattern, see below).
- Contract: `round26-claims.md:132–141` (Spec-v1 correction): ids are `S` + three or more digits with **standalone ASCII alphanumeric/underscore boundaries**; `used-by` is an exact repo-relative path. `round27-claims.md:15` (C3): "standalone ASCII S-ids without invented or duplicate occurrences."
- Derivation: `S001S003` is one glued ASCII word, so it contributes no occurrence. The terminal `S001` is the only occurrence. Its row is `mined` with the exact backlink `corpus/knowledge/entry.md`. So the verdict is CLEAN, exit 0, with no `META_SOURCE_` finding. None of this consults gate code.
- The C3 expectations do not read gate text. Only the C1 usage-helper extraction (:40–50) does.
- Cosmetic: the first count at :163 (`source_id=S002` NOT_MINED) can never match this fixture because S002 is absent. The operative assertions are exit 0 and the `META_SOURCE_` count.

## 2. Targeted mutation — KILLED for the intended reason

The targeted mechanism is the historical `source_scan` rescanning in `metadata_registry_check_source()`. Prefix removal `${source_scan#*"$source_match"}` consumes the earlier ` S001` inside ` S001S003`, leaving `S003 and S001`, and the rescan then invents a standalone `S003`. The landed fix replaces this with one-pass tokenization, `grep -oE '[[:alnum:]_]+'` plus `^S[0-9]{3,}$` (landed 2499–2532).

`mut-revert.sh` is the landed gate with only that loop restored. The landed `local LC_ALL=C` (:2503) is kept.

```diff
2501c2501,2502
<   local source_id found_id=0 used_by token matched i
---
>   local source_id found_id=0 used_by token matched i source_match
>   local source_scan=$1 source_id_re='(^|[^[:alnum:]_])(S[0-9]{3,})([^[:alnum:]_]|$)'
2504,2505c2505,2507
<   while IFS= read -r source_id; do
<     [[ $source_id =~ ^S[0-9]{3,}$ ]] || continue
---
>   while [[ $source_scan =~ $source_id_re ]]; do
>     source_id=${BASH_REMATCH[2]}
>     source_match=${BASH_REMATCH[0]}
2529c2531,2532
<   done < <(printf '%s\n' "$source_value" | LC_ALL=C grep -oE '[[:alnum:]_]+' || true)
>     source_scan=${source_scan#*"$source_match"}
>   done
```

Single gate runs, control fixture (`entry.md`: `source: see S001S003 and S001`, verified 2026-01-02, recheck 90d). Registry: `S001 | mined | corpus/knowledge/entry.md`, `S002 | queued | —`. Argv: `bash GATE verify-metadata ENTRY --root ROOT --registry REG`, env `CHOUSA_STRICT=0 LC_ALL=C`, mirroring the harness `run()`.

| Gate | rc | Output (key lines) | Harness-equivalent errors |
|---|---:|---|---|
| landed `ca39d14d…` | 0 | `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` | `[]` (passes) |
| base `64eec5d` (`c2c813f1…`) | 1 | `FINDING META_SOURCE_ROW_MISSING … source_id=S003 registry row missing`; `RESEARCH_GATE: DRIFT` | `['exit 1 != 0', "count '^FINDING META_SOURCE_': 1 != 0"]` |
| `mut-revert` | 1 | identical to base | `['exit 1 != 0', "count '^FINDING META_SOURCE_': 1 != 0"]` |

The failure is the invented occurrence `S003`, with the normal `META … source=present` and `METADATA_COMPLETE=1/1` lines present. It is not a usage, parse, or setup failure.

## 3. Neighbour and vacuity search

### 3a. Landed gate: 19 nearby inputs, none contract-inconsistent

Each row is one gate run on a synthetic fixture. "Contract" gives the reading from the round-26 ASCII-boundary text.

| Input (source value) | Locale env | rc | Findings | Contract reading |
|---|---|---:|---|---|
| `see S001S003 and S001` (control) | C | 0 | none | glued S003 invisible; OK |
| `see S001-S003 and S001` | C | 1 | ROW_MISSING S003 | hyphen is a boundary; OK |
| `see S001_S003 and S001` | C | 0 | none | underscore blocks; OK |
| `see S001S003 and S009` | C | 1 | ROW_MISSING S009 only | OK |
| `S001S003` (no standalone) | C | 0 | NO_ROW_ID info | OK |
| `see S001S0031 and S001` | C | 0 | none | glued 4-digit; OK |
| `see S003S001 and S001` | C | 0 | none | OK |
| `see S0031 and S001` / `see S001 S0031` | C | 1 | ROW_MISSING S0031 | 4-digit is a valid id; OK |
| `see s003 and S001` | C | 0 | none | lowercase not an id; OK |
| `see S001\u00a0S003 and S001` (NBSP) | C | 1 | ROW_MISSING S003 | non-ASCII is not a blocker; OK |
| `see éS003 and S001` | C and en_US.UTF-8 | 1 | ROW_MISSING S003 (both) | ASCII-only boundary reading; OK |
| `see S003é and S001` | en_US.UTF-8 | 1 | ROW_MISSING S003 | OK |
| `see S001S003 and S001` | en_US.UTF-8 | 0 | none | OK |
| `source: see S001S003` + `  S009` (continuation) | C | 1 | ROW_MISSING S009 | newline splits tokens; OK |
| `source: see S001` + `  S003S001` | C | 0 | none | OK |
| `source: S001` + fence `  S001S003 S009` | C | 1 | ROW_MISSING S009 | fenced continuation; OK |
| `source: S009` then `source: S001` | C | 0 | none | see 3c (S009 dropped) |
| no `source:` key, `--registry` | C | 1 | ABSENT warn + NO_ROW_ID info | see 3c |

Result: no landed-gate counterexample in the S-id class.

### 3b. Control vacuity and coverage gaps (counterexamples to the suite, not gate defects)

**V1. A dead registry check passes this control.** `mut-inert.sh` puts `return 0` at the top of `metadata_registry_check_source`. The control then returns rc 0, CLEAN, 0 findings, with error list `[]`, so it is vacuous as a liveness witness. Suite-level positives do catch the inert mutant: `adjacent-real-ids` (`S001,S002`) gives `['exit 0 != 1', "count …: 0 != 1"]`. The proposed same-fixture positive `see S001S003 and S009` gives 3 errors on the inert mutant and passes on landed (exactly one `source_id=S009`). The control alone does not prove the check ran.

**V2. Exact-three-digit width passes every C3 control.** `mut-exact3.sh` changes the id test at :2505 to `^S[0-9]{3}$`. It gives `see S0031 and S001` → rc 0, while landed gives rc 1 with `ROW_MISSING source_id=S0031`. `see S001 S0031` likewise gives rc 0. The control still passes under this mutant, since its glued case has no standalone four-digit id. The regression file has no standalone id of four or more digits (`grep -c 'S[0-9]\{4\}'` = 0). The spec requires "three or more" (`round26-claims.md:135`). Coverage gap.

**V3. The unpinned locale is invisible to C3 by construction.** `mut-nolocale.sh` removes three pins: `verify_metadata`'s `local LC_ALL=C` (landed :2564; already present at base :2539), the check-local `local LC_ALL=C` (:2502), and the inline `LC_ALL=C` on the grep (:2529).
- The harness exports `LC_ALL=C` to every gate run (`round27-regressions.py:28`, `run()` default `locale='C'` at :60). Every C3 registry call therefore runs in C. Under that environment `mut-nolocale` and landed are identical: both report `ROW_MISSING S003` for `see éS003 and S001`.
- Only the C2 date loop (:123) sets `en_US.UTF-8`. Its 12 single ascii-cli runs (6 per gate) are identical for landed and `mut-nolocale`, so they do not detect the unpinning either.
- Under inherited `en_US.UTF-8`: landed reports `ROW_MISSING S003` (rc 1). `mut-nolocale` returns rc 0, CLEAN, with no S003, which violates the ASCII-boundary text.

### 3c. Nearby observations, unspecified by the contract (landed = base; not C3 defects)

- Duplicate `source:` key: `source: S009` followed by `source: S001` gives rc 0, CLEAN. The later key overwrites `source_value` (landed :2690), so S009 is silently dropped. The contract is silent on duplicate keys, so this needs an owner decision, not a C3 fix.
- Absent `source:` key with `--registry`: both `META_SOURCE_ABSENT` (warn) and `META_SOURCE_NO_ROW_ID` (info) are emitted. Whether the info duplicate is intended is ambiguous.

## 4. Recommended controls (advice only; nothing applied)

- **R1.** Add a same-fixture positive to the glued-missing row: `see S001S003 and S009`, expecting exactly one `FINDING META_SOURCE_ROW_MISSING … source_id=S009` and zero `source_id=S003`. This kills the inert mutant (V1). It does not kill the rescan mutant, which is already killed by the glued row.
- **R2.** Add a UTF-8 registry control, `run('--registry', registry, locale='en_US.UTF-8')` on `see éS003 and S001`, expecting one `ROW_MISSING source_id=S003`. This kills V3. The expectation follows the literal ASCII-boundary text. If the owner intends Unicode letters to block, the spec must say so first.
- **R3.** Add a standalone four-digit fixture, `see S0031 and S001`, expecting one `ROW_MISSING source_id=S0031`. This kills V2.
- **R4.** Decide duplicate `source:` key handling and the absent-key double finding (3c). Both need a contract statement before any change.
- **R5 (cosmetic).** Make the first count in the glued-missing row reference an id that is actually in the fixture, or remove it.

## 5. Commands, exit codes, bounds

- Sandbox: `mkdir … && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e… | tar -x -C …` → exit 0. `git show 64eec5d…:tools/research-gate.sh > base-gate.sh` → exit 0.
- Mutants are sandbox copies edited with hashline edits: `mut-revert.sh`, `mut-inert.sh`, `mut-nolocale.sh`, `mut-exact3.sh`.
- Gate runs: about 45 single invocations, each `bash GATE verify-metadata …`, `timeout 120`. Observed rc values are in the tables above. No failure was a timeout.
- Not run: `--selftest`, the whole regression script, `mut-*` against the full suite. No network, no external targets, no host secret reads, no live-process inspection, no debugger, no subagents, no background jobs.
- Tools: none installed or updated. Runtimes in use: GNU bash 5.3.20(1)-release, Python 3.14.8, git 2.56.0, GNU grep 3.12-modified (`/usr/bin/grep`, which the gate children use). My tool shell's `grep` is a separate builtin and was not used for any gate run.

## Limits

- I replicated the harness's `observe()` error construction for single cases only; I did not execute the harness.
- Locale results depend on the host's installed `en_US.utf8` (present in `locale -a`).
- The non-ASCII adjacency reading follows the literal "ASCII alphanumeric/underscore boundaries" text. Nothing here says whether Unicode letters should block.
- No claim is made about parser, resource, or grammar safety beyond these inputs, nor about the other 57 controls or the full suite.

## Corrections (append-only, same attempt)

- Verdict paragraph and §3a: the landed nearby set is **20 inputs**, not 19. Two rows were omitted from the table: `see S001S003` (C, rc 0, `META_SOURCE_NO_ROW_ID` info only) and `see S03S001 and S001` (C, rc 0, no findings). Both are contract-consistent.
- §1: the C1 helper extraction that reads gate text is at `round27-regressions.py:74–77`, not :40–50. The C3 expectations do not read gate text.
- §2: the landed check-local `local LC_ALL=C` is at landed line **2502**. In `mut-revert.sh` it sits at 2503 because of the inserted line. The diff itself is unchanged.
- §4 R1 verified: `see S001S003 and S009` on `mut-revert` gives exactly one `ROW_MISSING source_id=S009` (rc 1), identical to landed. So R1 does not kill the rescan mutant; the glued row does.
- §5: about **60** single gate invocations, not 45. Return codes observed were 0, 1, and 2 (2 only for the C2 ascii-cli usage cases). None was a timeout (124).
- §2 table: the `mut-revert` row's "identical to base" means the same rc (1) and the same `FINDING META_SOURCE_ROW_MISSING … source_id=S003` line. The header line differs only by fixture path and timestamp, so the two outputs are not byte-identical.
