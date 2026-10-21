# FRegistryDuplicateId — C3 "first row of a duplicated id wins"

Seat `ChousaR26R.FRegistryDuplicateId`, round 26 attempt 1, author-lane advice only
(no outside judge / SHONEN claim). Judged on: calibration.

## Target identity

- Revision under test: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from
  `corpus/evidence/round26-measured-revision.json`); claim base `ba3333254dd337658a4f25e7a9471f9cf4e4567e`.
- Sandbox: `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FRegistryDuplicateId/tree` (rc=0).
- Digests in sandbox equal the revision file: `tools/research-gate.sh`
  `c2c813f1…43abc6`, `corpus/evidence/round26-registry-oracle.py` `6b2d135c…1f5d78`,
  `corpus/SOURCES.md` `8308e629…9aa9`.
- Rule under attack (`round26-claims.md:96`): "columns are located by header name;
  the first row of a duplicated id wins". Implementation: `tools/research-gate.sh:2433-2438`
  (`[[ -z ${META_REGISTRY_STATUS[$row_id]+x} ]]` guard). Oracle:
  `round26-registry-oracle.py` `records.setdefault(identifier, …)`.

## Commands

Each fixture has its own root at `/tmp/chousa-r26-falsify-FRegistryDuplicateId/w/<name>/`, containing
`SOURCES.md` and `corpus/knowledge/e.md`. The entry `e.md` is
`source: <ids>` / `verified-at: 2026-10-20 checked the row` / `recheck: 90d` / `## Claim`.
For each fixture:

```
bash tree/tools/research-gate.sh verify-metadata corpus/knowledge/e.md --root . --registry SOURCES.md
python3 tree/corpus/evidence/round26-registry-oracle.py corpus/knowledge/e.md --root . --registry SOURCES.md
```

Every command ran (no unrun check is reported). I did not run the selftest, the build, linting, a formatter, the 8 MiB probe, or `round26-registry-differential.sh`.

## Observed results: the duplicate rule itself

`P` = `corpus/knowledge/e.md`. The header is `| id | status | used-by |`.

| fixture | registry rows (in order) | gate rc / findings | oracle |
|---|---|---|---|
| A | S0999 mined P; S0999 queued P | 0, none (CLEAN) | [] |
| B | S0999 mined other.md; S0999 mined P | 1, META_SOURCE_USEDBY_MISSING | [USEDBY_MISSING] |
| C | S0999 mined P; S0999 mined other.md | 0, none | [] |
| D | S0999 queued P; S0999 mined P | 1, META_SOURCE_NOT_MINED | [NOT_MINED] |
| E | S0001 queued; S001 mined; cite S001 | 0, none | [] |
| E2 | same; cite S0001 | 1, META_SOURCE_NOT_MINED | [NOT_MINED] |
| F | S0999x queued; s0999 queued; S0999 mined | 0, none (invalid ids skipped) | [] |
| I | tab-padded S0999 queued; S0999 mined | 1, NOT_MINED | [NOT_MINED] |
| K | short row `\| S0999 \|`; S0999 mined | 1, NOT_MINED (empty status wins) | [NOT_MINED] |
| L | table1 S0999 mined; blank; table2 S0999 queued | 0, none (first table only) | [] |
| M | S0999 queued CRLF; S0999 mined | 1, NOT_MINED | [NOT_MINED] |
| N | S0999 empty status; S0999 mined | 1, NOT_MINED | [NOT_MINED] |
| O | header `id\|status\|used-by\|status`, row mined/…/queued | 0, none (first `status` column) | [] |
| Q | `\v`-padded S0999 queued; S0999 mined | 1, NOT_MINED | [NOT_MINED] |
| S | S0999 queued; inner `\|---\|`; S0999 mined | 1, NOT_MINED | [NOT_MINED] |

Every oracle run exited 0. Every gate exit matches its findings: 1 when there is a warning, 0 when clean.

**Verdict on the claim:** the first-duplicate rule is **not falsified**. In all 15
ordering, column, id-identity (`S001` and `S0001` are different string keys), CRLF,
whitespace, short-row and second-table fixtures, the gate's result matches the rule and
the oracle's findings.

### The controls can fail (QUALITY 17)

I made an isolated mutant at `/tmp/chousa-r26-falsify-FRegistryDuplicateId/mut/gate-lastwins.sh`
(sha256 `751d0451…e177c`). The only change from the target is deleting the guard
`&& [[ -z ${META_REGISTRY_STATUS[$row_id]+x} ]]`, which makes the last row win. Results:

- A: rc 1, NOT_MINED. The target gives 0.
- D: rc 0, CLEAN. The target gives 1, NOT_MINED. This is the same shape as selftest case
  `metadata-registry-duplicate-first-row` (want rc 1) and differential fixture `adv-duplicate.md`.
- B: rc 0, CLEAN. The target gives 1.
- C: rc 1, USEDBY_MISSING. The target gives 0.
- K: rc 0, CLEAN. The target gives 1.

So the existing duplicate control kills last-wins because of the rule itself, not because of a parse error. I infer the selftest would report a failure for the mutant [INFERENCE: I ran the fixture's shape through the CLI; I did not run the selftest].

## Findings (calibration)

**F1 — the oracle and gate disagree on which first row counts. The differential cannot see it.**
In four duplicate fixtures the first row's id cell (or status cell) contains an invisible byte, or the row has a doubled pipe:

| fixture | first row | gate | oracle |
|---|---|---|---|
| G | `S0999` + U+00A0 (NBSP), queued; then S0999 mined | rc 0, CLEAN (NBSP row skipped, second row wins) | [NOT_MINED] |
| G2 | S0999, `mined` + NBSP; then S0999 mined | rc 1, NOT_MINED | [] |
| H | `\|\| S0999 \| queued \| P \|`; then S0999 mined | rc 0, CLEAN (id cell is the empty first cell) | [NOT_MINED] |
| R | `S0999\x1c`, queued; then S0999 mined | rc 0, CLEAN | [NOT_MINED] |

- Cause [observed in the code]: the oracle uses Python `str.strip()`, which strips Unicode whitespace including NBSP and `\x1c`–`\x1f`. It also uses `text.strip("|")`, which removes every leading and trailing pipe. The gate trims C-locale `[:space:]` and removes one outer pipe.
- Adjudication [INFERENCE]: the contract does not define trimming. GFM trims only spaces and tabs, and treats `||` as an empty first cell. On that reading the gate is the spec-faithful side and the oracle over-normalizes.
- Calibration consequence: the "independent" oracle does not implement the same first-row identity. `REGISTRY_DIFF_AGREE` passes only because its 14 adversarial fixtures contain none of these shapes.
- G and R show a real bypass: a byte that looks the same on screen hides the first (queued) row, and a later mined duplicate silently approves the entry.
- The measured `corpus/SOURCES.md` has 39 S-id rows, no duplicate ids, and no NBSP, `\x1c`–`\x1f`, or `||` lines. So this changes no population result.

**F2 — repeated citations multiply findings; the differential collapses them to a set.**
- J: `source: S0999 and again S0999` against a queued row gives 2 NOT_MINED lines, `findings=2 drift=2`.
- J2: `S0999 S0999 S0999` with no row gives 3 ROW_MISSING lines, `findings=3 drift=3`.
- The oracle uses `set(SOURCE_ID_RE.findall(...))`, and the differential compares sets of finding ids, so the two tools can disagree on counts while the differential still reports agreement.
- Spec text "yields every token" (`claims.md:97`) permits one finding per occurrence, so this is not a falsification. But one defect inflates the drift tally n-fold, and no tool checks finding counts.

**F3 — a duplicate id is a contract violation that nothing reports.**
- `../CORPUS.md` Registry: an `id` is "the next unused; never reused".
- The preregistered rule resolves duplicates silently (first wins) and emits no finding: fixtures A and C are CLEAN even though the registry is invalid.
- Where order decides the result (A against D, C against B), a reader who sees only the second row reaches the opposite verdict. This is a scope gap, not a breach of the C3 spec. It should be named in the limits of `registry-link-r26.md`, or covered by a future `META_SOURCE_ROW_DUPLICATE` check.

**F4 — the inner-separator semantics differ (side observation, not duplicate-specific).**
- T: header, separator, then a second `|---|---|---|`, then S0999 mined.
- The gate gives rc 0, CLEAN, because the separator row is skipped. The oracle gives [ROW_MISSING], because it ends the table at the inner separator.
- In fixture S both tools agree only because the first-wins row comes before the separator.

## Remaining unknowns

- I did not run the differential, so its verdict on this revision is not reported here.
- Whether the gate or the oracle is canonical for NBSP and `||` needs a decision by the spec owner. The contract text does not settle it.

## Tools

No installs or updates.
