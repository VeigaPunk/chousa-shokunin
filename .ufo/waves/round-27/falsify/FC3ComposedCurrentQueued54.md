# FC3ComposedCurrentQueued54 — falsify attack on C3 control `composed-current-queued`

Target revision: `dd72641e574679c4f7882dd43de072b4c8892d6f` (lane master; read-only access).
Gate sha256 verified: `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches assignment).
Base for comparison: `64eec5d41c7cf7f17f5ce1e968e28b3769952596`, `tools/research-gate.sh` sha256 `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`.
Sandbox: `/tmp/chousa-r27-falsify-FC3ComposedCurrentQueued54` (`git archive` extract; `base-gate.sh`; `mut/T*.sh`; `drv/*.py`). All fixtures are synthetic temp roots. Lane access was read-only (`git show`, `git grep`, `git ls-tree`, `git log`, `git cat-file`, `git diff --stat`). No lane file was edited.

## Item attacked

`corpus/evidence/round27-regressions.py:206-209`

    registry.write_text(header + row.replace('mined', 'queued'))
    observe('C3', 'composed-current-queued', run('--registry', registry, '--as-of', '2026-10-21'), 1,
            ('due=2027-01-19 freshness=current',),
            counts={r'^FINDING META_SOURCE_NOT_MINED\b': 1, r'^RESEARCH_GATE: ': 1})

Fixture: entry `verified-at: 2026-10-21 checked synthetic fixture`, `recheck: 90d`; registry `| S001 | queued | corpus/knowledge/entry.md |`.

## Verdict: FALSIFIED (narrow scope)

- **Not a witness for any C1–C3 repair.** It passes identically on pre-repair base `64eec5d` (stdout byte-identical), and it stays green after reverting each C3 repair I could map to its inputs (header reset, S-id tokenizer, raw-path denylist).
- **Its own targeted check holds.** Reverting the NOT_MINED arm makes it fail for the intended reason, not a parse or setup error.
- **Same-class nearby inputs give wrong verdicts** on both base and landed. No independent control covers them.

Axis results:
- Operability: HOLDS. Replica on landed: `rc=1`, `errors=[]`. The recorded L1 entry for this control is `expected 1 / actual 1 / errors []`.
- Freshness: HOLDS. Recorded `script_sha256` `5afea786…` and `gate_sha256` `ca39d14d…` in `corpus/evidence/round27-regressions-after.json` match the sandbox files.
- Calibration: FALSIFIED (CE1–CE2 below; CE3 low).

## (1) Is the expectation derived from the declared contract, independent of gate code?

Mostly yes. One leg inherits gate code.
- `due=2027-01-19`: independent. Python `date(2026,10,21)+timedelta(90)` = `2027-01-19` (89d gives 01-18, 91d gives 01-20). The verified-at + cadence anchor is only implicit in `corpus/knowledge/metadata-screen-r25.md:11` ("when it is due again").
- `freshness=current`: independent. Strict `as-of > due` rule; as-of `2026-10-21` < due.
- NOT_MINED expected: contract. `corpus/QUALITY.md` criterion 6 requires the cited S### row to be `mined`.
- Count 1: one standalone occurrence in the source.
- **Exit 1 is gate-coupled.** Nothing declares NOT_MINED's severity. The gate sets `warn` (`tools/research-gate.sh:2511`), and the header (line 11) says warn|crit always drift. The exit-1 leg therefore inherits the gate's severity choice.

## (2) Revert or mutate the targeted fix — does the control fail for the intended reason?

No round-27 hunk touches the NOT_MINED arm. Landed `:2510` and base `:2484` are the same text (`elif [[ ${META_REGISTRY_STATUS[$source_id]} != mined ]]; then`). So the control targets pre-existing behavior, not a repair.

Method: replica `drv/cq_one.py` (same fixture state and `observe()` logic as lines 206–209, fresh temp root). Mutants are isolated copies edited with hashline `edit`. Each passes `bash -n`, and `diff` against landed shows only the intended region changed. Gate rc and control errors:

| variant | edit (landed line numbers) | gate rc | control errors | reading |
|---|---|---|---|---|
| landed | none | 1 | `[]` | pass |
| base `64eec5d` | none | 1 | `[]` | pass, identical stdout |
| T1 | NOT_MINED arm disabled (`:2510`) | 0 | `exit 0 != 1`; `NOT_MINED count 0 != 1` | fails, intended |
| T2 | due +1 day (`:2377`) | 1 | `missing 'due=2027-01-19 freshness=current'` | fails, arithmetic (pre-existing) |
| T3 | header-state reset removed (`CUT 2434.=2435`) | 1 | `[]` | not witnessed |
| T4 | base regex S-id loop restored (`:2501-2530`, 12 changed lines) | 1 | `[]` | not witnessed |
| T5 | raw-path denylist restored (`:2609`) | 1 | `[]` | not witnessed |
| T7 | freshness suppressed under drift (insert after `:2787`) | 1 | `missing 'due=…'` | fails, composition (pre-existing) |

- Reverting any round-27 repair (T3, T4, T5) leaves the control green. The only failing reverts are pre-existing behavior (T1, T2, T7).
- The control always runs `LC_ALL=C` (`run(..., locale='C')`, script line 60), so C2 locale changes cannot be observed by it. Its `90d`/`0090d` inputs also never reach the length bound that the C2 normalization change addressed.
- Grid check (`drv/matrix.py`): 143 composed cases (11 freshness × 5 registry × 3 sources, one gate command each). Landed 0 mismatches, base 0 mismatches, outputs line-identical. Grid sensitivity: T1 33 mismatches, T2 104, T7 122, T3 0, T4 0, T5 0. The family detects composition mutants but not the three C3 repairs.
- Not run: T6 (locale-pin removal). The control's forced `LC_ALL=C` makes it unobservable by construction.

## (3) Nearby counterexamples (same class: composed freshness × registry)

Each was run on landed and base. Results were identical unless noted.

**CE1 — calendar-invalid `verified-at` is clean. Calibration. Pre-existing. Pinned by the gate's own selftest.**
- Input: `verified-at: 2026-02-30 checked synthetic fixture`, `recheck: 90d`, `--as-of 2026-10-21`. Same with `2026-13-01` and `0000-01-01`.
- Result (landed and base): `rc=0`, `META … verified_at=dated recheck=scheduled due=unknown freshness=unknown verdict=clean`, no findings.
- Also with `recheck: 2026-12-31`: `rc=0`, `verified_at=dated`, `due=2026-12-31 freshness=current verdict=clean`.
- Contract: criterion 6 requires `verified-at:` to be an ISO date, and 2026-02-30 is not one. The gate's test is regex-only (`verified_state=dated`, `tools/research-gate.sh:2724`). A failed calendar check silently yields `freshness=unknown`, so a bad anchor can never be overdue and reads clean.
- The gate's selftest pins this as clean (`:6174-6182`). That is same-author, not independent. The regression suite has no such case.

**CE2 — non-ASCII-glued S-ids invent NOT_MINED. Calibration. Pre-existing. Contract-ambiguous.**
- Input: `source: éS001`, `source: S001é`, or `source: S001٢`, with registry S001 `queued`.
- Result: `rc=1`, `FINDING META_SOURCE_NOT_MINED`, identical under caller `LC_ALL=C` and `en_US.utf8`. `verify_metadata`'s `local LC_ALL=C` (`:2564`; base `:2539`) is inherited, so the boundary is byte-based in both.
- The gate's claim tokenizer treats non-ASCII as word characters (`tok_word_char`, `:1258`). Under that model S001 is not standalone and the finding is invented. A literal ASCII-only reading of "standalone ASCII S-ids" would make landed consistent. The gate's two tokenizers disagree, and the suite has no non-ASCII glue case (its glue cases are ASCII only).
- Grid: 187 ambiguous cases. ASCII model 0 mismatches (landed = base). Unicode model 99 mismatches on both, line-identical.

**CE3 — conflicting duplicate registry rows are order-dependent and silent. Low. Design-pinned.**
- `| S001 | mined |` then `| S001 | queued |`: landed = base, `rc=0` clean.
- Reverse order: `rc=1` NOT_MINED.
- First-row-wins is pinned by the gate's selftest (`:6272-6279`), so it is design. It still never flags the conflict.

## Commands and exit codes (key output)

- `git -C <lane> archive dd72641e… | tar -x -C <sandbox>`: exit 0. `sha256sum tools/research-gate.sh`: `ca39d14d…`.
- `git -C <lane> show 64eec5d…:tools/research-gate.sh > base-gate.sh`: sha `c2c813f1…`.
- `python3 drv/cq_one.py <gate>` (driver exit 0; gate rc in JSON): landed `rc=1 errors=[]`; base `rc=1 errors=[]`; mutant rows as in the table above.
- `bash -n mut/*.sh`: exit 0 each.
- `python3 drv/matrix.py <gate>` (exit 0): landed and base `cases=143 mismatches=0`; `--ambiguous --model ascii` `cases=187 mismatches=0` each; `--ambiguous --model unicode` `cases=187 mismatches=99` each. `diff` of landed vs base outputs: 0 differing lines in all three.
- Mutants via `matrix.py`: T1 33, T2 104, T3 0, T4 0, T5 0, T7 122 mismatches.
- `python3 drv/nearby.py <gate> [C|en_US.utf8]` and `python3 drv/dup.py <gate>`: outputs as in CE1–CE3.
- Recorded-evidence check (Python `hashlib` over the recorded JSON): hashes match, as stated above.

## Limits

- Did not run `--selftest` or `round27-regressions.py`; L1 owns those. The grids are ad hoc composed sampling, one gate command per case on synthetic temp roots.
- The replica does not reproduce the script's earlier alias or protected-file residue. Entry and registry state for this control are identical.
- The non-ASCII "standalone" contract is ambiguous (CE2 is labeled as such). CE1's severity is my judgment on criterion 6.
- I did not find a concrete ASCII input on which restored base S-id loop (T4) differs from landed. Neither this control nor the composed grid can see that difference.
- No known-unsafe long-token reproduction was run.
- Installs and updates: none. Toolchain used: GNU bash 5.3.20, Python 3.14.8, git 2.56.0 (system).

## Author-lane advice (not outside admission)

1. Do not cite `composed-current-queued` as a C3 repair witness. Either rename it as a composed guard for the pre-existing NOT_MINED arm, or add a base-failing sibling. Its sibling `reorder-queued` already fails at base and is a real repair witness.
2. Before deciding the contracts, add independent controls for CE1 and CE2. For CE1, decide whether an impossible `verified-at` is drift under criterion 6. For CE2, decide whether non-ASCII-adjacent tokens are standalone; then align the S-id tokenizer with `tok_word_char` or pin ASCII explicitly in the contract.
3. The 2026-02-30 "clean" pin at `:6174-6182` is a same-author expectation. Revisit it together with the CE1 decision.
4. Declare NOT_MINED's severity in the contract document. It is currently only in code.

## Appended corrections (append-only; written after the report above)

- Author-lane advice item 1 cites `reorder-queued` as "already fails at base". That statement comes from the FC3ReorderQueued31 report, not from this attack. It was not re-verified here.
- The composed control's only cadence is `90d`, supplied by `entry_text()`'s default `recheck`. The `0090d` input appears only in the matrix grid, not in this control. Section (2)'s note on leading-zero inputs should be read with that scope.
