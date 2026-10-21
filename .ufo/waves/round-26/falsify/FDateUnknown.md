# FDateUnknown — round 26 attempt 1 falsify: C2 command-only / missing recheck → unknown

Seat `ChousaR26R.FDateUnknown` (UFO-FSD scout, leaf, author-lane advice only; no outside-judge claim).
Judged axis: freshness (C2). Item: command-only and missing `recheck:` must yield
`due=unknown freshness=unknown`.

## Verdict

**Not falsified.** At the immutable target, 44 command-only, missing, empty, or near-miss
`recheck:` shapes all yield `due=unknown freshness=unknown` under three `--as-of` values,
with no `META_RECHECK_OVERDUE` and no other byte change versus the base plain output.
The harness is shown able to fail (5/5 isolated mutants killed, M1 only via the carry-over case).
Two low-severity option observations below are **not** in this item's target and are not C2 regressions on unknown.

## Revisions and inputs (observed)

- Target: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from `corpus/evidence/round26-measured-revision.json`).
  `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FDateUnknown/tree` → rc=0.
  `tools/research-gate.sh` sha256 `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`
  = measured-revision input hash = lane working tree (lane HEAD observed `0e9784bd…`).
- Base: `ba3333254dd337658a4f25e7a9471f9cf4e4567e` archived to `…/base`; gate sha256
  `985a63200ca4c5712806d8752ba27a8f3448b026f773659079e71ca602e56ef7`.
- Sandbox: `/tmp/chousa-r26-falsify-FDateUnknown/` (harness `harness.py` sha256
  `b16a1fe35d575411b4bc8f1e82ceeafa3e18307e69ca9f50d24354f15175f7d7`; fixtures `fx/`, `fx-carry/`; logs `run2.log`, `mut-*.log`, `pop.out`).
- Tools: bash 5.3.20, Python 3.14.8 (`datetime` only). No installs or updates.

## Oracle

Hand-derived from the frozen spec (`round26-claims.md:56-81,143-148`) and QUALITY 6 (“A `recheck:`
that is only a command leaves ‘overdue’ uncomputable”). R is the first whitespace-delimited token of
the recheck value. If R is a calendar-valid date, due=R. If R is `<N>d` and V is present, due=V+N.
If R is `on-release`, the entry is event. Anything else, including a missing recheck, is unknown.
Dates come from `datetime.date`; I wrote the oracle without reading the implementation's date code.
The harness never executes entry text; commands in fixtures are inert strings.

## Checks run

1. `python3 harness.py` (target) → **exit 0**, `CASES=53 UNKNOWN_CASES=44 POSITIVE_CONTROLS=9 ASOFS=3 FAILS=0`, 167 `ok` rows.
   For each case and each as-of in {2026-10-21, 0001-01-01, 9999-12-31}, the harness asserted:
   - the target's plain output equals the base output (rc plus body without the timestamp line);
   - the `due`/`freshness` pair equals the oracle's;
   - `META_RECHECK_OVERDUE` appears only when expected, with the exact `obs=`;
   - the rc, verdict, and `RESEARCH_GATE` deltas are exact;
   - the output equals base once the freshness fields are stripped.
   Directory mode (53 entries in one run) gave 44/44 unknown lines and the META lines match base after normalization.
   - Unknown shapes covered:
     - command-only: plain, backticked, CRLF, `cd … &&`, `$(…)`, `$((90))d`, `*d`;
     - a command first, followed by a later cadence, date, or `on-release`;
     - missing or empty: absent, `recheck:` empty, whitespace-only, only inside a fence, after `## `, indented key, `Recheck:`, `recheck :`, no verified-at, empty file, heading-only;
     - near-miss tokens: `90days`, `90 d`, `d`, `-90d`, `+90d`, `90d,`, `90D`, `ON-RELEASE`, `on-release:`, ISO datetime, `2026-10-21,`, slash date, compact date, NBSP-joined, fullwidth/Arabic-Indic digits, `0x10d`, `1.5d`, `` `90d` ``;
     - a cadence with V undated, absent, or calendar-invalid (`2026-02-30`);
     - duplicate keys where a cadence is followed by a command-only line (last wins, consistent with base `recheck=unscheduled`).
   - Positive controls, which are not unknown: the cadence on a continuation line, a tab after the colon, no space after the colon, a cadence/event/date followed by a command, duplicate keys where a command is followed by a cadence, a key after a blank line, and a date with no verified-at.
   - Carry-over directory (`fx-carry/`: scheduled date entry, then absent, then cadence, command-only, event, empty): an absent or command-only entry does not inherit the previous entry's R; 2 overdue findings, as expected.
2. Population (frozen 29 at base): `bash tree/tools/research-gate.sh verify-metadata base/corpus/knowledge --root base --as-of 2026-10-21` → rc=1 (pre-existing drift from absent keys, not freshness).
   - 24/29 entries are `due=unknown freshness=unknown`: 21 `recheck=unscheduled` (command-only, e.g. R=`` `bash ``, `re-run`, `the`, `bash`) and 3 `recheck=absent`.
   - The other 5: 3× due 2027-01-17, 1× due 2027-01-19, 1× `on-release`.
   - An independent Python key-line oracle disagreed on **0/29**.
3. Option and composition CLI cases (target), rc observed:
   - `--as-of` placed before PATH → rc 0, unknown fields present.
   - Calendar-invalid or malformed `--as-of` values exit 2 with “must be a valid YYYY-MM-DD date”, matching Python's `fromisoformat` verdicts: `''`, `0000-01-01`, `' 2026-10-21'`, `$'2026-10-21\n'`, `2026-10-21x`, `26-10-21`, `2026-1-21`, `1900-02-29`.
   - `--as-of=…` → rc 2 (unknown flag). `2000-02-29` → rc 0. `verify-all … --as-of` → rc 2 (only valid with verify-metadata).
   - With `--registry tree/corpus/SOURCES.md`, command-only and absent entries keep `due=unknown freshness=unknown` while `META_SOURCE_ROW_MISSING` is also retained. The verdict is drift (union), rc 1. This is consistent with the composition clarification.

## Independent failing controls (QUALITY 17; isolated sandbox mutants of target bytes, `mut/*/tools/research-gate.sh`)

| Mutant | Change | Harness exit / FAILS | Targeted kill |
|---|---|---|---|
| M1 | remove per-entry `recheck_first=''` reset | 1 / 29 | carry-over `b-absent` inherited `due=2026-03-01 freshness=overdue` (3 overdue vs 2). The single-file failures are a `set -u` crash (`recheck_first: unbound variable`), which is not a targeted kill. |
| M2 | unanchor the cadence regex `^([0-9]+)d$` to `([0-9]+)d` | 1 / 33 | `90days` and `-90d` became due 2026-04-01 |
| M3 | turn the `on-release` branch into an `else` (unknown→event) | 1 / 168 | command-only gave `due=on-release freshness=event` |
| M5 | substitute as-of for a missing V | 1 / 7 | undated or absent V gave due 2027-01-19 |
| M6 | take R from any cadence/date/event token in the value | 1 / 71 | `rerun 90d` and `rerun 2026-02-01` became dated, and the plain output also diverged from base |

The main 53-entry directory run alone does **not** kill M1, because of alphabetical ordering.
The dedicated carry-over fixture is what kills it.

## Observations outside this item (low; not C2-unknown regressions)

- **O1 — repeated `--as-of` is last-wins.** `--as-of 2026-02-30 --as-of 2026-10-21` → rc 0 with
  freshness computed. The reverse order → rc 2.
  - The literal spec says “an absent or calendar-invalid value exits 2”. A supplied invalid value is silently superseded here.
  - The gate's own pin/drift comment names last-wins mode flags as a silent-wrong-path hazard.
  - `--registry` is likewise last-wins (`--registry x --registry SOURCES.md` → runs).
  - Severity: low (operator-supplied argv). It's a spec-text counterexample, not a frozen-control failure. Routed to option-owning peers; adjudication belongs to L1.
- **O2 — arguments after `--` are silently dropped** (`… -- --as-of 2026-10-21` → rc 0 with no freshness
  fields). This is the same at base (`--) shift; break`, base line 5706), so it's pre-existing and not introduced by C2.
- **Ambiguity, not a defect:** “whitespace-delimited” is resolved under `LC_ALL=C`. So NBSP is not a delimiter and `recheck:\u00a090d` → unknown, while Python `str.split()` would yield `90d`. Under the base classifier's existing rule this matches (`recheck=unscheduled`).

## Unknowns

- I did not run the full selftest, `round26-measure.sh`, the build, or the 8 MiB probe (outside the bounded assignment). L1's integrated run owns those.
- These are synthetic fixtures under one `--root`. Path-dependent interplay with `--registry` beyond the two composition runs above was not explored.
