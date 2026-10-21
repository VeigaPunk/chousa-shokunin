# FC3AdjacentRealIds43 — attack on C3 control `adjacent-real-ids`

Seat `ChousaR27.FC3AdjacentRealIds43-11`, round 27 attempt 1, falsify wave.
Author-lane advice only; no outside admission.

- Target: `dd72641e574679c4f7882dd43de072b4c8892d6f` (master, lane
  `/home/vgpnk/Projects/shokunin/chousa-shokunin`).
- Gate: `tools/research-gate.sh` sha256
  `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84`
  (matches the assigned gate sha).
- Control: `corpus/evidence/round27-regressions.py:159`
  `('adjacent-real-ids', 'S001,S002', 1, 1)`; block `:139-160`, fixture/run
  helpers `:49-62`. Script sha256 `5afea7863f2b…a5df` (matches the landed
  `regressions.json`).
- Sandbox: `/tmp/chousa-r27-falsify-FC3AdjacentRealIds43`, created with
  `git archive dd72641… | tar -x`; pre-fix comparator from
  `git show 64eec5d:tools/research-gate.sh` (sha256 `c2c813f1b425…abc6`, the
  same base the r26 falsifier measured). No tool was installed or updated; no
  network, no host/live-process probe; every gate invocation used a synthetic
  temp fixture under the sandbox.
- Not run (owned by L1): the full `--selftest` and the 58-case regression
  script. Every measurement below is a single gate command or a sandbox mutant
  of it.

## Verdict

**FALSIFIED as a regression control; the fixture's semantics are not
falsified.** `adjacent-real-ids` is contract-derived and the landed gate
answers it correctly, but it does **not** discriminate the C3 repair it is
filed under: it passes on the pre-fix base gate and on a surgical revert of
`metadata_registry_check_source`, and it is never the unique catcher among the
seven persisted S-id controls. The C3 S-id block as a whole is also blind to a
tokenizer that splits only on comma/whitespace (7/7 controls pass; 31/93
declared-grammar inputs diverge).

## 1. Is the expectation derived from the declared contract, independent of gate code?

Yes, with one calibration caveat.

- `S001` in the fixture registry is `mined` with `used-by =
  corpus/knowledge/entry.md`, `S002` is `queued`. The expectation
  (rc 1, exactly one `META_SOURCE_NOT_MINED … source_id=S002`, exactly one
  `^FINDING META_SOURCE_` line) follows from the declared C3 contract —
  standalone ASCII S-ids, per-occurrence identity, exact root-relative
  used-by — plus the roll rule (warn ⇒ DRIFT). It is hand-encoded; nothing in
  the C3 block derives an expectation from gate source. The script reads the
  gate text only for the C1 helper extraction and the sha256.
- Independent corroboration of the single-occurrence shape: the persisted r26
  oracle `corpus/evidence/round26-registry-oracle.py` (a different
  implementation, lookaround grammar at `SOURCE_ID_RE`) on the same fixture
  returns `{"entry.md":["META_SOURCE_NOT_MINED"]}`, rc 0.
- Caveat (calibration): the review oracle for this exact row
  (`.ufo/waves/round-27/build/ReviewRegistryBoundary.md:15`) gives **both**
  ids `queued` and expects two findings. The persisted control weakened that to
  one finding by making `S001` mined-with-correct-used-by, so the control only
  asserts "`S002` is recognized exactly once and `S001` produces nothing"; it
  never asserts that the *first* id of an adjacent pair is recognized at all
  (a gate that dropped `S001` from `S001,S002` would still pass). The r26
  oracle cannot corroborate the multiplicity case `S002,S002 → 2` either: it
  is set-based (`source_ids = set(...)`, `findings: set`), so it reports one
  `META_SOURCE_NOT_MINED`.
- The expectation's rc and text format are gate-format-dependent (declared in
  earlier rounds' selftest expectations), but the semantics are not read back
  from this gate.

## 2. Does reverting/mutating the targeted production fix make the control fail?

No. The targeted fix is the rescan→token replacement in
`metadata_registry_check_source` (`tools/research-gate.sh:2499-2533`; mechanism
`C3_consumed_text_rescan` = 0 at target, 1 at base). Replaying the seven
persisted C3 S-id cases with the exact fixtures/patterns of
`round27-regressions.py:139-160` (`/tmp/.../obs.py`, one gate per case,
`CHOUSA_STRICT=0 LC_ALL=C`):

| variant | gate sha256 (short) | cases failing /7 | `adjacent-real-ids` |
|---|---|---|---|
| landed | ca39d14d | 0 | PASS (rc 1, S002 ×1) |
| base `64eec5d` (full pre-fix tree) | c2c813f1 | 4 | **PASS** |
| surgical revert of `metadata_registry_check_source` only (landed tree + base function body) | 81f88216 | 4 | **PASS** |
| whitespace-only tokenizer (`grep -oE '[^[:space:]]+'`) | 5676a4f1 | 2 | FAIL (rc 0, 0 findings) — also FAILS `two-real-occurrences` |
| comma+whitespace-only tokenizer (`tr ',' ' '` then line split) | adacdce9 | **0** | PASS |
| no-boundary tokenizer (`grep -oE 'S[0-9]{3,}'`) | 7af438ed | 5 | PASS |
| dedup (`sort -u`) | 0d87d3d2 | 1 | PASS — FAILS `two-real-occurrences` |
| first-token-only (`head -1`) | 0f493fd7 | 7 | FAIL — also caught by 6 others |
| last-token-only (`tail -1`) | b36c664c | 1 | PASS — FAILS `two-real-occurrences` |
| remove `local LC_ALL=C` from the function | 080ea398 | 0 | PASS |

The revert fails for the intended reason in the sibling controls, not in this
one:

```
base: FAIL glued-before-terminal ; exit 1 != 0; count '^FINDING META_SOURCE_NOT_MINED\b[^\n]* source_id=S002(?: |$)': 1 != 0
base: FAIL glued-missing-before-terminal ; exit 1 != 0; count '^FINDING META_SOURCE_': 1 != 0
base: FAIL nonstandalone-duplicate ; count …: 2 != 1
base: FAIL glued-repeat-duplicate ; count …: 3 != 1
base: PASS adjacent-real-ids
base: PASS two-real-occurrences
base: PASS underscore-glued
```

`adjacent-real-ids` is blind to the defect by construction: the r26 trigger
precondition (`FRegistryIdBoundary.md:38-46`) is a standalone id at
end-of-value whose earlier literal `sep+id` occurrence sits inside a glued
token. `S001,S002` contains no glued run at all, so the rescan cannot misfire
on it and cannot be detected through it. No mutant in the table fails
`adjacent-real-ids` without also failing at least one other persisted control;
every mutant it catches (whitespace-only split) is also caught by
`two-real-occurrences`. It is redundant, not a detector.

## 3. Nearby same-class inputs: landed gate, and control vacuity

### 3a. Landed gate is correct on this class (no counterexample found)

A list-based reference implementing the declared grammar
`(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` with per-occurrence findings
was run against the landed gate on 93 synthetic source values
(`/tmp/.../fuzz.py`): the persisted control shape, `S001;S002`, `S001/S002`,
`S001|S002`, `(S001),(S002)`, `S001-S002`, `S001:S002`, tab/NBSP/U+3000
separators, `S0012`, `S0001`, `S001S002`, `_S001,S002_`, random glue strings.
Result: **93 cases, 0 diffs, exit 0**. Adjacent ids produce left-to-right
per-occurrence findings, e.g. both-queued `S001,S002` → 2 findings; `S003,S002`
with `S003` mined+exact-used-by → 1 finding (rc 1). Continuation-line and CRLF
forms of `S001,` + `S002` → one `NOT_MINED:S002`. 40 000 comma-adjacent
`S001` occurrences + terminal `S002` complete in 0.87 s wall with one finding
(the old quadratic rescan is gone).

### 3b. The control (and the block) is vacuous in a measurable way

- **Fix-vacuity:** table in §2 — base and surgical revert both PASS.
- **Block blindness (counterexample family):** mutant `adacdce9` replaces the
  tokenizer with "split on comma and whitespace only". All seven persisted
  S-id controls pass (0/7), yet the declared grammar requires `; : / | ( ) . -
  …` to be boundaries. The same mutant diverges from the independent reference
  on **31/93** inputs, e.g. `S001;S002`, `S001:S002`, `S001{S002}`,
  `(S001),(S002)` → the gate emits no S002 finding (rc 0) where the declared
  grammar requires `META_SOURCE_NOT_MINED:S002` (rc 1). No persisted C3 S-id
  control uses a non-comma, non-whitespace separator, so this class is
  unguarded; `adjacent-real-ids` hard-codes the comma and inherits the gap
  (this repeats the coverage gap the build scout already listed at
  `.ufo/waves/round-27/build/ScoutRegistryTokens.md`, item B "punctuation
  boundaries … currently only comma is covered").
- **Fixture weakness:** with `S001` mined and used-by-correct, the control's
  second count (`^FINDING META_SOURCE_` = 1) is also satisfied by a scanner
  that silently drops the first id of the pair; the reviewer's both-queued row
  (two findings) is not persisted anywhere.
- **Locale pin:** removing `local LC_ALL=C` from `metadata_registry_check_source`
  passes all seven controls (0/7), and is behaviorally inert in the landed
  design because the tokenizer carries `LC_ALL=C` in the child environment
  (measured identical output on `éS002`, `S002é`, U+FF0C and U+3000 separators
  under `LC_ALL=C.UTF-8`). Not a live defect — recorded so the “unpinned
  boundary” mechanism is not mistaken for a covered one.

## Limits

- Only the seven C3 S-id cases and single gate commands were replayed; the full
  selftest, the 58-case suite, and the differential drivers were not run (L1
  owns them). The base comparator is `64eec5d`, not the r26 measured revision.
- The reference implements the declared grammar as stated in the claims; it is
  not a semantic judge of whether the declared grammar itself is the right
  contract.
- Findings are limited to synthetic temp fixtures under
  `/tmp/chousa-r27-falsify-FC3AdjacentRealIds43`; no lane production file, lane
  git/jj state, fleet repo, or sibling lane was touched.
- No tool installs or updates; nothing to record in the tooling ledger.
