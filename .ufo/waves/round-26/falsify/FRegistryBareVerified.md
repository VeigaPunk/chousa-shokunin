# FRegistryBareVerified — C3 `META_VERIFIED_AT_BARE` relation/grammar attack

Seat `ChousaR26R.FRegistryBareVerified`. This is author-lane advice from one seat, not an outside judgement.
Target: the immutable revision `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from
`corpus/evidence/round26-measured-revision.json`). The claim base is `ba3333254dd337658a4f25e7a9471f9cf4e4567e`.
Sandbox: `/tmp/chousa-r26-falsify-FRegistryBareVerified/` (`tree/` = git archive of the target,
`base/` = base `tools/research-gate.sh`, `root/` = fixtures, `run.py` = matrix, `matrix.out` = raw output).

## Verdict

C3's two headline behaviors survive on the ASCII grammar: a date-only `verified-at:` warns, and
non-space checked text passes. All 30 fixtures matched the literal spec text (claims line 104–105:
"value after the leading date has no non-space text"), read with C-locale whitespace. Without
`--registry`, output is byte-identical to the base on the fixtures I compared.

**Calibration findings (none of them is a C3 spec violation by the gate):**

- **F1 — The gate and the oracle disagree, and the shipped probes cannot see it (calibration; medium).**
  The gate (`tools/research-gate.sh:2523-2528`, `local LC_ALL=C`, `[[:space:]]`) and the
  independent oracle (`corpus/evidence/round26-registry-oracle.py:17,142`, Python `str.strip()`
  and `^[ \t]*` before the date) split on 7 of 30 fixtures.
  - The gate says CLEAN (exit 0) but the oracle says BARE when the only thing after the date is:
    - a no-break space, U+00A0 (`p09`);
    - an ideographic space, U+3000 (`p10`);
    - unit separator `\x1f` (`p12`);
    - an indented continuation line containing only a no-break space (`p13`);
    - an em space, U+2003 (`p16`);
    - a next-line character, U+0085 (`p17`).
  - The gate says BARE but the oracle says nothing for `verified-at:\v2026-10-20` (`b11`): the gate
    accepts a vertical tab before the date; the oracle's `[ \t]*` does not.
  - Coverage: every `verified-at` value in `round26-registry-differential.sh` and
    `round26-measure.sh` is ASCII (`2026-10-21`, `… checked`, `… opened the source`, `%s`). So the
    differential's agreement is only shown for ASCII space and tab.
  - Effect: an entry whose `verified-at` shows only a date on screen passes C3 CLEAN. That
    contradicts `SKILL.md:483` ("says nothing nonblank about what was checked").
  - Zero-width space U+200B (`p11`) passes both the gate and the oracle; this is a shared gap.
  - The spec does not define "space", so neither side is falsified. But the oracle is not
    independent on this point.
- **F2 — The grammar checks that some text exists, not that it says what was checked (calibration; spec-literal).**
  These values pass CLEAN (exit 0) in both the gate and the oracle:
  - `2026-10-20x` (`p03`);
  - `2026-10-20 .` (`p04`);
  - `2026-10-20T12:00:00Z`, a timestamp with no description (`p05`);
  - `2026-10-2000`, where the extra `00` counts as "text" (`p06`).

  This satisfies the spec. But the claim's motivation (claims line 87: "nor that `verified-at:`
  says what was checked") and QUALITY 6 ("ISO date + what was checked") ask for more. The screen
  should be described as a non-blank-tail screen; any reading that it verifies content is unsupported.
- **F3 — Any header line after the date suppresses BARE (calibration; spec-literal, rule carried over from the base).**
  The verified-at value takes in every following non-blank, non-key line before the first `## `,
  indented or not. The base already did this (base `research-gate.sh:2396-2431`).
  - These all silence BARE in both the gate and the oracle: a date-only value followed by
    `# Entry title` (`p07`), by a fenced block (`p08`), or by a mis-cased `Source: elsewhere` (`p14`).
  - Claims line 97–98 states the continuation rule for keys, so this follows the spec. It is still
    a false-negative route.

No regression was found: no lost refusal, and no plain-output change.

## Matrix (gate exit / gate finding IDs / oracle finding IDs / agreement)

Registry: `| id | status | used-by |`, one row `S001 | mined |` listing all 30 entries.
Every entry is `source: S001 https://example.test/a anchor`, `verified-at:<case>`,
`recheck: 90d`, blank line, `## Claim`. That leaves BARE or UNDATED as the only possible finding.

| case | verified-at payload | gate rc | gate | oracle | split |
|---|---|---|---|---|---|
| b01 | ` 2026-10-20` | 1 | VERIFIED_AT_BARE | BARE | agree |
| b02 | trailing spaces | 1 | BARE | BARE | agree |
| b03 | trailing tab | 1 | BARE | BARE | agree |
| b04 | CRLF file | 1 | BARE | BARE | agree |
| b05 | leading 4 spaces | 1 | BARE | BARE | agree |
| b06 | `verified-at:2026-10-20` | 1 | BARE | BARE | agree |
| b07 | `2026-13-45` | 1 | BARE | BARE | agree |
| b08 | trailing `\f` | 1 | BARE | BARE | agree |
| b09 | whitespace-only next line | 1 | BARE | BARE | agree |
| b10 | text, then duplicate key date-only (last wins) | 1 | BARE | BARE | agree |
| b11 | `\v` before date | 1 | BARE | — | **SPLIT** |
| p01 | `2026-10-20 checked the claim` | 0 | — | — | agree |
| p02 | date + indented `checked the claim` | 0 | — | — | agree |
| p03 | `2026-10-20x` | 0 | — | — | agree (F2) |
| p04 | `2026-10-20 .` | 0 | — | — | agree (F2) |
| p05 | `2026-10-20T12:00:00Z` | 0 | — | — | agree (F2) |
| p06 | `2026-10-2000` | 0 | — | — | agree (F2) |
| p07 | date + unindented `# Entry title` | 0 | — | — | agree (F3) |
| p08 | date + fenced block | 0 | — | — | agree (F3) |
| p09 | date + U+00A0 | 0 | — | BARE | **SPLIT** (F1) |
| p10 | date + U+3000 | 0 | — | BARE | **SPLIT** (F1) |
| p11 | date + U+200B | 0 | — | — | agree (shared gap) |
| p12 | date + `\x1f` | 0 | — | BARE | **SPLIT** (F1) |
| p13 | date + U+00A0-only next line | 0 | — | BARE | **SPLIT** (F1) |
| p14 | date + `Source: elsewhere` | 0 | — | — | agree (F3) |
| p15 | date-only, then duplicate key with text | 0 | — | — | agree |
| p16 | date + U+2003 | 0 | — | BARE | **SPLIT** (F1) |
| p17 | date + U+0085 | 0 | — | BARE | **SPLIT** (F1) |
| u01 | empty | 1 | VERIFIED_AT_UNDATED | — | agree (BARE correctly absent) |
| u02 | `20261020 checked` | 1 | VERIFIED_AT_UNDATED | — | agree |

Raw b01 output (registry mode; the timestamp header line is omitted):

```text
META entry=b01-date-only.md source=present verified_at=dated recheck=scheduled verdict=drift
FINDING META_VERIFIED_AT_BARE severity=warn surface=metadata obs=entry=b01-date-only.md key=verified-at has date only
METADATA_COMPLETE=1/1
RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)
```

p09 (no-break space) under the same flags: `verdict=clean`, `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)`, rc=0.

Controls:
- `NOREG b01`: no `--registry` gives rc 0 and no BARE.
- Locale: running with `LC_ALL`/`LANG` set to `C.UTF-8` or `en_US.UTF-8` does not change p09, p10 or b01, so F1 does not depend on the user's locale.
- Whole directory: gate rc 1, `bare_count 11`, `RESEARCH_GATE: DRIFT (entries=30 complete=28 findings=13 drift=13)`.
- Base comparison: plain `verify-metadata` (no flag, timestamp line dropped) was byte-identical between the target and the base for b01, p09, p07 and b11.

## Commands and exits (all run 2026-10-21)

- `git archive 0e9784bd… | tar -x -C …/tree`: exit 0. `sha256sum tree/tools/research-gate.sh` = `c2c813f1…abc6`, which matches the measured-revision input.
- `git archive ba333325… tools/research-gate.sh | tar -x -C …/base`: exit 0. Base sha256 = `985a6320…6ef7`.
- `python3 run.py | tee matrix.out`: exit 0, wall time 1.53 s. Python 3.14.8, GNU bash 5.3.20(1).
- Per-case runs: `bash tree/tools/research-gate.sh verify-metadata root/corpus/knowledge/<case>.md --root root [--registry root/registry.md]` (with `CHOUSA_*` unset), and `python3 tree/corpus/evidence/round26-registry-oracle.py <entry> --root root --registry root/registry.md` (exit 0 for every case).
- Not run: selftest, build, lint, formatter, `round26-measure.sh`, `round26-registry-differential.sh`, and the 8 MiB probe. None of these is claimed.

## Remaining unknowns

- Whether "space" in claims line 104–105 should mean ASCII or Unicode whitespace. The spec owner has to pick one, and then align either the gate or the oracle and add a non-ASCII fixture to the differential.
- How many real entries use F2 or F3 shapes was not measured. I did not grade the frozen population.

Tools installed or updated: none.
