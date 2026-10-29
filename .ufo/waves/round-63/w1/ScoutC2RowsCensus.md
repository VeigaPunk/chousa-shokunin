# ScoutC2RowsCensus — round 63, wave w1 (C2 candidate rows vs the SOURCES.md contract)

Scope: validate `corpus/evidence/round63/controls/candidate-git-rows.txt` (rows S142–S144) against
`CORPUS.md` § SOURCES.md (contract v1) using the maintained `scripts/sources-census.sh validate`. Read-only on the lane;
scratch under `/fast/scratch/hyaku/chousa-r63/ScoutC2RowsCensus` (removed on exit). No network, no git writes, no
installs.

## Findings

1. **Column count.** All three rows have NF=13 (11 cells). Checked with `awk -F'|'`; the census E01 check is clean.
2. **Id collision.** Lane registry has 141 rows, max id S141. S142, S143, S144 are free (`grep -nE '^\|[[:space:]]*S14[2-4][[:space:]]*\|'`
   on the lane registry: no output). E02/E03 clean.
3. **Enums.** kind `docs`, `docs`, `own-work` (valid set); tier `A`, `A`, `B`; status `mined` ×3. E05/E06/E07 clean.
   E10 (community at A) not triggered.
4. **ISO dates.** `opened` = 2026-10-28 on all three (valid ISO, not in the future: `--today` default is UTC today,
   2026-10-29 on this host; also run with `--today 2026-10-28`, exit 0). E08 clean.
5. **Recheck cadence.** `on-release`, `on-release`, `180d`. `on-release` is symbolic (accepted by the `symbolic()` rule);
   `180d` matches `^[0-9]+d$`. E09 clean.
6. **used-by.** All three point to `corpus/knowledge/git-revision-identity-r63.md`, which does not exist in the lane at
   the freeze (created by landing). Without the entry the census reports E11 for S142, S143 and S144 (negative control,
   exit 1). With the candidate entry in the mirror, E11 clears (exit 0). So the rows are valid only together with the
   entry; they must land in the same commit.
7. **0–3 leading-space parser note.** Candidate rows are column-zero, so the note is not exercised by the file as shipped.
   Variants built with the rows indented:
   - 1 or 3 leading spaces: maintained `validate` exit 0, `census` FLEET rows = 144 (rows counted);
     frozen manual grep `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` counts 141 (column-zero only).
   - 4 leading spaces: maintained `validate` exit 0 with no E-line, `census` FLEET rows = 141 — the three rows are
     silently dropped (indented code by the parser's rule). No finding is raised.
   INFERENCE: this is a divergence between the frozen manual census and the maintained one, documented in the contract
   (the parser note says the frozen examples "remain unchanged"); it is not a defect in the candidate rows, which are
   column-zero. The silent-drop case at 4 spaces is a limit of the validator, not of the rows.
8. **Source column (not validated by census).** S142 and S143 name host files `/usr/share/man/man1/git-rev-parse.1.gz`
   and `/usr/share/man/man7/gitrevisions.7.gz`; both exist on this host (`ls -la`, Sep 28 14:57). S144 names
   `corpus/evidence/round63/git-revision-probe.txt`, which does not exist in the lane at the freeze (created by landing;
   the candidate output is at `controls/candidate-git-revision-probe.txt`). The census does not check the source column,
   so this passes the validator and is a landing-time obligation (INFERENCE from the claims file: the file is listed as
   created by the round).
9. **Warnings.** Lane baseline and mirror both list five pre-existing W04 warnings (S051, S053, S073, S074, S075 —
   same URL across scopes). The candidate rows add no W-line: S142–S144 carry no http(s) URL in the source cell, so no
   W04 is raised. The finding lists before and after are identical (`diff`).
10. **Harness pitfall (observed, not a row defect).** My first mirror copied only the new entry into a registry-only
    tree; `validate --file` resolves used-by relative to the registry's parent, so the census reported E11 for
    S001–S140 too (exit 1). A mirror must carry the full `corpus/` (as `run-c2-controls.py` does, ignoring
    captures/evidence/fixtures). The reported result below uses the full mirror.

## Evidence (commands and observed output)

- Row count before (lane) → after (mirror): `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → `141` → `144`.
- Validate, unmodified lane (`bash scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md`): `CENSUS_EXIT=0`,
  `file ok <lane>/corpus/SOURCES.md`, plus 5 W04 lines.
- Validate, mirror with candidate rows and entry (cwd = mirror): `CENSUS_EXIT=0`, `file ok <mirror>/corpus/SOURCES.md`;
  W04 lines identical to the lane (`IDENTICAL finding lists`).
- Validate, mirror with `--today 2026-10-28`: `CENSUS_EXIT=0`.
- Validate, mirror with entry removed: `E11 S142|S143|S144 missing used-by corpus/knowledge/git-revision-identity-r63.md`, `CENSUS_EXIT=1`.
- Census (non-validate), mirror: `FLEET rows 144`, `tier.A 112`, `tier.B 25`, `tier.C 7`, `tier.invalid 0`,
  `status.mined 118`, `status.queued 19`, `status.rejected 7`, `status.invalid 0`, `missing 0`, `CENSUS_EXIT=0`.
- Registry section: candidate rows at lines 152–154 of the mirror, all under `## Registry` (no E12).
- Leading-space variants (1, 3, 4 spaces): see finding 7.

Not run: `tools/lane-preflight.py`, `c2-count.py`, `run-c2-controls.py` (outside this item). No git, install or network
action taken; no tool installed or upgraded.

## Limits

- Validator checks structure, enums, dates, cadence and used-by paths only; it does not check that a `teaches` or
  `anchor` cell is true (entailment is out of scope here).
- The `opened` date (2026-10-28) is the claim's own statement; I did not re-open any source (read-only, no fetch).
- The 4-space silent drop is a property of the maintained parser as documented; I have not judged whether it should
  change (that would be a contract-version question).

VERDICT: CENSUS_EXIT=0 rows=141->144 findings=none
