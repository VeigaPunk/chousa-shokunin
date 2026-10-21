# FC3ReorderQueued31 — falsify attack on C3 control `reorder-queued`

Target revision: `dd72641e574679c4f7882dd43de072b4c8892d6f` (lane master).
Gate sha256 verified: `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84`
(`git show dd72641:tools/research-gate.sh | sha256sum`). Base gate for mutation
comparison: `git show 64eec5d:tools/research-gate.sh`, sha256
`c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`.
Sandbox: `/tmp/chousa-r27-falsify-FC3ReorderQueued31` (archive extract of the target
revision; all fixtures synthetic, temporary dirs). No tools installed; bash 5.3.20,
python 3.14.8 used. No LSP server applies to a shell script; grep/read located code,
every verdict below comes from executing the gate.

## Item attacked

`corpus/evidence/round27-regressions.py:137`

    ('reorder-queued', '| id | status | used-by |\nprose\n| id | note | used-by | status |\n|---|---|---|---|\n'
     f'| S001 | mined | {relative} | queued |\n', 1, 'META_SOURCE_NOT_MINED')

run through `observe()` (`:31-45`) as
`bash tools/research-gate.sh verify-metadata ENTRY --root ROOT --registry REGISTRY`.

**Verdict: HOLDS.** The expectation is contract-derived and independent of gate code;
the control fails on the base gate and on a revert of the exact production fix, for the
intended reason (wrong verdict, not parse/setup). Two adjacent limits are real but were
explicitly accepted as limits in the round-27 build record, so they do not falsify C3.
One control-sensitivity gap was found (partial revert of only `id_col` is invisible to
the whole C3 table block), with a concrete fixture that exposes it; the landed gate is
correct on that fixture.

## (1) Expectation derivation and independence

- The C3 block (`:121-200`) contains only literal fixtures, literal expected exit codes
  and literal finding strings. The gate source read at `:26` (`text = gate.read_text()`)
  is consumed by exactly one `re.search` (`:75`) in the C1 usage-helper extraction; no
  C3 expectation is computed from gate text, regex-extracted helpers, or exit probes of
  the gate.
- The semantic rule the case asserts — row status `queued` (i.e. not `mined`) for a cited
  standalone id must produce `META_SOURCE_NOT_MINED` and a drift verdict — exists
  independently in `corpus/evidence/round26-registry-oracle.py:130-136`
  (`if status != "mined": findings.add("META_SOURCE_NOT_MINED")`), a separate Python
  reader, not the gate.
- The same fixture shape and expected finding were pre-registered in the build wave at
  `.ufo/waves/round-27/build/ReviewRegistryReorder.md:20` ("reordered-header false
  negative control ... expect exactly one `META_SOURCE_NOT_MINED` for S001 and a drift
  verdict").
- The persisted control deliberately strengthens that pre-registration: the review used
  the literal filler `note`, and the persisted row uses `mined` in the note cell. This
  matters. On the base gate the review-literal fixture
  `| S001 | note | REL | queued |` returns rc 1 with `META_SOURCE_NOT_MINED` (stale
  `status_col=1` reads `note`, also "not mined"), so it would have been vacuous; the
  persisted `mined` filler is what makes the base gate return CLEAN and the control
  discriminating. Measured: landed rc1/NOT_MINED, base rc1/NOT_MINED for the
  review-literal shape.
- Under-specification, minor: `reorder-queued` pins exit 1 + the finding substring +
  one verdict line, but no `^FINDING META_SOURCE_` count. A gate emitting both
  `META_SOURCE_NOT_MINED` and `META_SOURCE_USEDBY_MISSING` (both warn, still rc 1) would
  pass this case. The landed gate emits only NOT_MINED. `reorder-clean` (rc 0) does pin
  absence of extra warns through the exit code.

## (2) Mutation evidence — exact production-fix reverts

Production fix site (target gate `:2431-2435`, non-table branch of
`metadata_registry_load`):

    ((header_found)) && break
    header_candidate=0
    id_col=-1; status_col=-1; usedby_col=-1
    header_width=0

Sandbox mutants (byte-exact copies of the target gate with only the named lines changed;
`diff -u` inspected): `gate-m1-stale.sh` (all three index resets removed, width check
kept), `gate-m2-width.sh` (width equality at `:2466` removed), `gate-m3-both.sh`,
`gate-m4-id-only.sh`, `gate-m5-status-only.sh`, `gate-m6-usedby-only.sh`.

`observe()`-equivalent replication of the two reorder cases (rc, required substring,
verdict count):

| gate | reorder-queued expected `1 + NOT_MINED` | reorder-clean expected `0` |
|---|---|---|
| landed `tools/research-gate.sh` | PASS (rc1, NOT_MINED) | PASS (rc0) |
| base `gate-base.sh` | **FAIL** `exit 0 != 1; missing 'META_SOURCE_NOT_MINED'` | **FAIL** `exit 1 != 0` |
| m1 stale-state revert | **FAIL** same two reasons | **FAIL** `exit 1 != 0` |
| m2 width-check revert | PASS | PASS |
| m3 both reverts | **FAIL** same two reasons | **FAIL** `exit 1 != 0` |

Base/m1 output for the named case is a normal verdict (`RESEARCH_GATE: CLEAN ... findings=0`),
not a usage/parse error: the failure is the wrong verdict, exactly the stale-column
false negative the fix targets. Base output for `reorder-clean` is
`META_SOURCE_NOT_MINED` (stale `status_col=1` reads the note cell), i.e. the inverse
error pair. This is the intended failure mode.

Width revert does not affect `reorder-queued` (as expected; the width rule is pinned by
`delimiter-too-short`/`delimiter-too-long`, which go rc 2 -> rc 0 CLEAN on m2).

Partial reverts, replicated over the full 10-case C3 table block (`:132-146`):

| gate | C3 table block | note |
|---|---|---|
| landed | 10/10 pass | |
| base | 4/10 pass | fails header-break-blank, header-break-prose, reorder-clean, reorder-queued, delimiter-too-short, delimiter-too-long |
| m5 status-only revert | `reorder-queued` FAILS (rc0) | caught by the named control |
| m6 used-by-only revert | `reorder-queued` passes; `reorder-clean` FAILS (`META_SOURCE_USEDBY_MISSING`, rc1) | caught by the paired clean control |
| m4 id-only revert | **10/10 pass** | not caught by the persisted block |

## (3) Nearby same-class inputs

### 3a. Well-formed and break/aborted-candidate fuzz: no landed defect

Two independent expectation scripts in the sandbox (declared contract only: fresh named
`id`/`status`/`used-by` header, equal-width dash delimiter, first row per id wins,
ASCII `S[0-9]{3,}`, exact root-relative `used-by` with leading `./` normalized,
not-mined/missing-row/used-by warn rules):

- `fuzz.py`: 149 well-formed registries (all 6 header permutations, 0-2 extra columns,
  with/without outer pipes, alignment colons, 0-2 space indent, CRLF, status/used-by
  variants, duplicate-id first-wins, comma lists, repeated cited ids).
  `python3 fuzz.py tools/research-gate.sh` -> exit 0, `cases=149 mismatches=0`.
  Same suite on base -> also 0 mismatches (the fix does not change well-formed input).
- `fuzz_break.py`: 480 cases of prose/blank/aborted-header/partial-header/rowlike/two-
  aborted/fence-mention/heading prefixes followed by a fresh reordered table:
  landed exit 0, `cases=480 mismatches=0`; base exit 1 (`stopping at 10 mismatches / 118
  cases`) with ROW_MISSING false negatives on reordered fresh headers after prose.
- Landed behaviour on the build-record preservation fixture
  `HDR, blank, HDR, SEP, ROW` (`CriticRegistryGrammar.md` fixture list): rc 0, no
  findings, as required.

No counterexample was found where the landed gate produces a wrong verdict on input the
declared C3 contract covers.

### 3b. Adjacent limits (reproduced, already accepted as limits — not a falsification)

- **Fenced example first.** Registry: fenced 3-column table with
  `| S001 | queued | REL |`, then the real 3-column table with S001 `mined`. Landed:
  rc 1, `FINDING META_SOURCE_NOT_MINED` on a source that is mined in the real table.
  Same for a 4-space-indented (code) example. The registry reader has no fence/indent
  awareness.
- **Second table after a break.** First complete table has S001; prose; fresh 4-column
  table defines S002 `queued`. Entry cites S002. Landed: rc 1,
  `FINDING META_SOURCE_ROW_MISSING` (S002). The parser stops at the first non-pipe line
  after a header is accepted ("first-qualifying-table behaviour").
- A header-only first table (`HDR, SEP` with no rows) followed by prose and a complete
  table makes the later rows invisible: rc 1 ROW_MISSING.

Status: `.ufo/waves/round-27/build/CriticRegistryGrammar.md:27-31` records G1 fence and
G2 indent as **unchanged** "calibration (false positive)" limits that the C3 plan does
not fix, and `.ufo/waves/round-27/build/RevengerC3.md` states first-qualifying-table
behaviour and the post-acceptance termination are to be kept. These shapes are therefore
outside the declared C3 repair, and the `reorder-queued` control does not claim them.

### 3c. Control-sensitivity gap: `id_col`-only partial revert survives the whole block

Fixture (new; synthetic):

    | id | status | used-by |
    prose
    | note | id | status | used-by |
    |---|---|---|---|
    | x | S001 | queued | corpus/knowledge/entry.md |

Entry cites S001. Landed: rc 1, `META_SOURCE_NOT_MINED` (fresh header binds id at index
1). Base: rc 1, `META_SOURCE_ROW_MISSING` (stale `id_col=0` reads `x`). m4 (only the
`id_col=-1` reset reverted): rc 1, `META_SOURCE_ROW_MISSING`, i.e. indistinguishable
from base here and indistinguishable from the fix in every persisted C3 table case.
`fuzz_break.py gate-m4-id-only.sh` catches it (stopping at 10 mismatches / 122 cases),
as it does the status-only (10/122) and used-by-only (10/149) partials.

The landed gate is correct on this fixture; the gap is in control coverage: none of
`reorder-clean`, `reorder-queued`, `header-break-blank`/`-prose` moves the `id` column,
so a partial revert that leaves only `id_col` stale passes the C3 block. By static
inspection of the selftest registry fixtures (`tools/research-gate.sh:6395-6470`), none
of them moves `id` across a break either, so the same partial revert would not be
separated from the fix by the full selftest [INFERENCE — selftest not run].

## Author-lane advice

1. Add the 3c fixture as a C3 control (fresh header where `id` moves after a break,
   expected rc 1 + `META_SOURCE_NOT_MINED`). It costs one gate invocation and closes the
   only partial-revert blind spot found.
2. Tighten `reorder-queued` with `counts={r'^FINDING META_SOURCE_': 1}` so an extra warn
   (still rc 1) cannot ride along.
3. Keep the `mined` filler in the note cell; do not transcribe the review's literal
   `note` filler, which is vacuous against the base bug.
4. Leave fence/indent/second-table shapes as asserted limits (as the build record
   already does) rather than claiming them fixed.

## Limits of this review

- Single gate invocations and small mutants only; the full `--selftest`, the whole
  regression script, and the r26 differential were not run (L1 owns them). Selftest
  coverage statements are static inspection of the fixture list.
- All fixtures are synthetic temporary directories inside the sandbox; no host files,
  network, live processes, or lane production files were touched.
- The oracle scripts in the sandbox encode the declared contract as reconstructed from
  `round27-claims.md:15`, `ReviewRegistryReorder.md:19-22`, and
  `round26-registry-oracle.py`; ambiguous shapes (duplicate columns, malformed rows,
  fenced/indented tables, multi-table documents) were excluded from the mismatch count
  and reported as limits instead.
