# FDateRefused — round 26 attempt 1, C2 refused-entry / `--as-of` option attack

Seat `ChousaR26R.FDateRefused` (falsify, author-lane advice only; not an outside judge).
Axis judged: freshness (C2). Target: refused entries gain `due=refused freshness=refused`
only with `--as-of`, plus `--as-of` option validation.

## Revisions and sandbox

- Target `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from `corpus/evidence/round26-measured-revision.json`);
  claim base `ba3333254dd337658a4f25e7a9471f9cf4e4567e`. Lane HEAD observed = `0e9784bd…` at run time.
- Sandbox `/tmp/chousa-r26-falsify-FDateRefused/`: `tree/` = `git archive 0e9784bd… | tar -x` (rc0),
  `base/` = `git archive ba333325… | tar -x` (rc0).
- `tree/tools/research-gate.sh` sha256 `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`
  = `git show 0e9784bd…:tools/research-gate.sh | sha256sum` = the measured-revision pin (QUALITY 15).
  Base gate sha256 `985a63200ca4c5712806d8752ba27a8f3448b026f773659079e71ca602e56ef7`.
- Host: GNU bash 5.3.20, Python 3.14.8, `LANG=en_US.UTF-8`, `LC_ALL` unset. No tools installed or updated.

## Method

`attack.py` (sha256 `2bae6552…fbd5f`) writes fixtures as bytes and runs only
`bash <gate> verify-metadata …`; entry text is never executed. Expected values come
from spec v1 (`round26-claims.md:60-75`, 143-148) via Python `datetime`, written
before looking at the gate's date helpers. Each fixture is run three ways: base plain,
target plain, target `--as-of 2026-10-21`. The checks are:

- plain target == plain base (rc, stdout with only `ts=` masked, stderr);
- no plain META line has `due=` or `freshness=`;
- each refused as-of line == plain line with ` due=refused freshness=refused` inserted
  directly before ` verdict=drift`;
- non-refused lines == the oracle's `due`/`freshness`;
- the as-of findings minus `META_RECHECK_OVERDUE` == the plain findings, in order;
- the OVERDUE set == the oracle's, and no OVERDUE line names a refused entry;
- `METADATA_COMPLETE`, the summary line and the rc match.

Every refused fixture's header carries a past `recheck: 2000-01-02`. If a refused entry
leaked into date computation, it would print `due=2000-01-02 freshness=overdue`.

Refusal shapes:

- NUL after the header, and NUL as the first byte;
- a hardlink pair (multilink);
- a sparse 8,388,609-byte file (refused by size at stat, before any read; not the C1 probe);
- `.config/` and `credentials/` denylist paths;
- a symlink to a denylisted file;
- a `%q`-hostile basename (`r odd $(touch PWNED) \`id\` ;x=1.md`, NUL body);
- a mixed directory where refused entries sit next to overdue, current, date-past,
  event, unknown and boundary (due == as-of) entries;
- a single refused file path.

Composition: `--as-of` with `--registry tree/corpus/SOURCES.md` on the mixed and NUL
targets.

Option cases:

- `--as-of` before PATH;
- invalid values: `2026-02-29`, `2026-13-01`, `2026-10-21x`, `26-10-21`, `""`,
  `0000-01-01`, `2026-1-01`, fullwidth `２０２６-10-21`;
- a missing value;
- a valid leap day, `2028-02-29`;
- `--as-of` with `verify-chain`.

## Results (observed)

Command: `cd /tmp/chousa-r26-falsify-FDateRefused && python3 attack.py > attack.log 2>&1`.
It exits 1 with **TOTAL=162 FAIL=1** (161 PASS). attack.log sha256 is `9032e1c9…7e`.

**Held (refused arm, C2 claim as specified).** All of the following passed on every
refusal shape (nul, nulfirst, multilink, size, deny-config, deny-cred, symlink-deny,
oddname, mixed, single-file):

- plain==base, byte-identical;
- the refused as-of line is exactly
  `META entry=<b> source=refused verified_at=refused recheck=refused due=refused freshness=refused verdict=drift`;
- no OVERDUE finding for a refused entry, even with a past recheck in the header;
- finding sequence, `METADATA_COMPLETE` and summary unchanged except for oracle-predicted
  OVERDUE findings on non-refused entries. Base, plain and as-of rc were all 1.

The mixed directory's non-refused lines all matched the oracle:

| Entry | Due | Freshness |
|---|---|---|
| 90d from 2026-01-01 | 2026-04-01 | overdue |
| 2027-01-01 | 2027-01-01 | current |
| on-release | on-release | event |
| weekly | unknown | unknown |
| 1d from 2026-10-20 (boundary) | 2026-10-21 | current |
| 2026-10-20 | 2026-10-20 | overdue |

**Composition held.** With `--registry` added (both targets), refused lines keep their
fields, no `META_SOURCE_*` finding names a refused entry, and the as-of/no-as-of delta
is only the fields plus the predicted OVERDUE findings. Base rc there is 2, which is
expected: `--registry` is an unknown flag at base.

**Option checks held.** `--as-of` before PATH matched; `2028-02-29` was accepted. These
all gave rc 2 with no META output: `2026-02-29`, `2026-13-01`, `2026-10-21x`, `26-10-21`,
`""`, `0000-01-01`, `2026-1-01`, a missing value, and `--as-of` with another mode.
`PWNED` was never created.

**Entry-level Unicode digits held.** Fullwidth digits in an entry's `verified-at`/`recheck`
gave plain output identical to base, and with `--as-of` gave `due=unknown freshness=unknown`.
The `local LC_ALL=C` in `verify_metadata` protects that path.

### FALSIFIED — C2 option validation: a non-ASCII-digit `--as-of` exits 1, not 2

Spec v1 (`round26-claims.md:61`): "an absent or calendar-invalid value exits 2". Under
the host default locale (`en_US.UTF-8`), Bash `[0-9]` in `metadata_iso_date`
(`tools/research-gate.sh:2295`) matches non-ASCII decimal digits. The value then reaches
`$((10#…))` (`:2296-2298`), which fails. The call at top level (`:6297`) has no
`LC_ALL=C`, so `die_usage` never fires. `verify_metadata` then fails again at `:2550`,
and the process exits **1 with empty stdout** (no RESEARCH_GATE line). Exit 1 is the
DRIFT code, so callers read this as a drift result rather than a usage error. On a clean
target, the ASCII as-of gives rc 0 (CLEAN), but the fullwidth one gives rc 1.

Raw (`G=tree/tools/research-gate.sh`):

```
$ bash $G verify-metadata fx/nul --root fx --as-of '２０２６-10-21'; echo rc=$?
tree/tools/research-gate.sh: line 2297: 10#: invalid integer constant (error token is "10#")
tree/tools/research-gate.sh: line 2550: 10#: invalid integer constant (error token is "10#")
rc=1
$ bash $G verify-metadata fx/clean --root fx --as-of '２０２６-10-21'   -> same two lines, rc=1
$ bash $G verify-metadata fx/clean --root fx --as-of 2026-10-21       -> RESEARCH_GATE: CLEAN, rc=0
$ bash $G verify-metadata ../fx/nul --root ../fx --as-of '2026-10-2¹'
tools/research-gate.sh: line 2298: 10#2¹: arithmetic syntax error: invalid arithmetic operator (error token is "¹")
tools/research-gate.sh: line 2550: 10#2�: arithmetic syntax error: invalid arithmetic operator (error token is "�")
rc=1
```

Locale matrix (fx/nul target): every non-ASCII-digit value gave **rc 1** under the host
environment and `LC_ALL=en_US.UTF-8`, and **rc 2** (`--as-of must be a valid YYYY-MM-DD
date`) under `LC_ALL=C` and `LC_ALL=C.UTF-8`. The values tested were:

- fullwidth year, month or day (`２０２６-10-21`, `2026-１０-21`, `2026-10-２１`);
- Arabic-Indic `٢٠٢٦-١٠-٢١`;
- NKo `߂߀߂߆-10-21`;
- mathematical bold `𝟐𝟎𝟐𝟔-10-21`;
- superscripts `²026-10-21` and `2026-10-2¹`.

The selftest's only invalid-value case is ASCII `2026-02-30` (`:6083-6084`), so it
cannot see this. `round26-date-differential.sh` has no `LC_ALL`/`LANG` handling, and
every as-of value it generates is ASCII (`:69`, `:101`).

Scope: this is an option-validation defect in C2's new `--as-of` parser. It does not
affect the refused-entry arm or any ASCII date computation. The frozen 29 and the 6
controls use ASCII and are unaffected [INFERENCE: not re-run here; the probe's values
are ASCII by inspection]. One possible fix: `local LC_ALL=C` in `metadata_iso_date`, or
an ASCII-only class such as `[0123456789]`. That is a suggestion only; this seat made
no production edit.

## Independent failing controls (QUALITY 17, isolated sandbox mutants)

| Mutant | Change (vs tree gate) | Gate sha256 | Harness | Killed by |
|---|---|---|---|---|
| mutA | `:2622` → `freshness_fields=''` (refused fields dropped) | `4a47816f…9aee` | exit 1, FAIL=19 | `refused line …` checks on every refusal shape |
| mutB | `:2621` `if (( AS_OF_ARG_SET ))` → `if true` (un-gated) | `a616acef…1b` | exit 1 | `plain==base` and `plain has no due/freshness` |

Command: `GATE=$PWD/<mut>/tools/research-gate.sh python3 attack.py > <mut>.log`. The logs
are mutA.log (`3eec4efc…f6`) and mutB.log (`44d4241c…e1`). Both detectors fail on the
targeted arm, not on a parse error.

## Harness corrections (not gate defects)

The first two runs crashed in my own harness, and both were fixed before the final run:

1. A fixture filename contained `/`, which made a subdirectory. That run's "plain==base"
   failure was rc 2 at both base and tree, with the expected usage-text difference.
2. My `\S+` entry regex did not handle `%q`'s `\ ` escapes.

The final numbers above are from the corrected harness.

## Remaining unknowns

- `refuse=unreadable`, `stat` and `read` were not reached. An unreadable directory child
  dies earlier with `metadata entry unreadable` (`:2561`), and the other two need fd/proc
  faults. These three share the same code line (`:2618-2625`) as the exercised reasons.
- I did not run the selftest, the full build, linters, the C1 probe or the integrated
  verification.
