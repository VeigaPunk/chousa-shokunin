# ScribeSkillRows — round 63, wave w1 (scribe)

Draft: `.ufo/waves/round-63/w1/ScribeSkillRows/skill-rows.md` (three rows, placement noted in the file). Nothing under
`corpus/`, `tools/`, `SKILL.md` or `SCORECARD.md` was written. No git mutation, no network, no subagent.

## Findings

1. Three rows drafted, one per requested item, each placed after the last row of its table in `SKILL.md`:
   (a) Decision table after line 27 (`Pin a citation to a revision of a git artifact (r63)`), (b) Error patterns after
   line 53 (`a citation holds a branch name or a short hash where a commit is meant (r63)`), (c) Gates after line 153
   (`tools/lane-preflight.py (r63)`).
2. Two untraced claims, both in row (c): the battery command `python3 corpus/evidence/round63/c1-battery.py --tool
   tools/lane-preflight.py --fleet <fleet root> --work <dir>` with its `BATTERY=PASS` expectation, and the `tools/`
   directory prefix (the docstring writes `lane-preflight.py`). Both come from `corpus/evidence/round63/claims.md` C1,
   which is not one of the two sources the row was limited to; neither the candidate entry nor the reference docstring
   names the battery. The L1 must either admit `claims.md` as a source for battery and path, or ask for a row-level
   exception. I did not add a third source on my own.
3. Row (b) is only partly traceable. The entry says nothing that states a branch's resolution; its Limits mark the
   branch behaviour as `[INFERENCE]` (probe P02, P05, P06 observations, no page sentence). The row carries that
   marking and does not state a branch fact as established. A reader should not treat the branch half as evidence.
4. Pointer status: `corpus/knowledge/git-revision-identity-r63.md` does not exist yet
   (`ls corpus/knowledge | grep -c git-revision-identity-r63` → `0`). The rows (a) and (b) cite it, and SKILL.md's
   checklist requires resolvable pointers, so they must not land before the entry does.
5. Row (a) uses the entry's Q-quotes and Claims, and does not use the probe's `PROBE_FACTS` count. The entry's Limits say
   the probe's expected values are author-typed, so that count is not independent evidence and is not cited in any row.
6. Row (c) cites `ids\|none` escaped for the table, matching the existing `\|` convention in the Error-patterns table.
7. Scope limit: I read the candidate entry, the candidate rows (S142–S144) and the reference docstring. I did not open
   the probe output, the battery, or the counter; their outputs are not in any row except as the untraced battery
   expectation in point 2.

## Evidence (commands run, observed output)

- `sha256sum corpus/evidence/round63/claims.md` → `6c46b2cc193e1a44187777e6db98aec52278e37cc4f4b027efbe4365d24c70f5`
  (matches the frozen digest). `git -C <lane> rev-parse HEAD` → `c8bfcc65cb327b1a7da27fa39ef9a482a5b33cfb` (read only).
- Reads: `SKILL.md:13-100`, `SKILL.md:27:raw`, `SKILL.md:144-178`, `SKILL.md:153:raw` (table boundaries: lines 28, 54,
  154 are blank); `controls/c2-positive-entry.md` (31 lines, Q1–Q9, Claims 1–5, Limits); `controls/candidate-git-rows.txt`
  (rows S142–S144); `controls/pos-ref-preflight.py:1-36:raw` (usage, output, exit codes, G01–G08, write scope).
- `grep -c 'lane-preflight' SKILL.md` → `0` (no existing row; no duplicate).
- `grep -rl 'rev-parse' corpus/knowledge` → no output, exit `1` (no existing row covers the revision name).
- The lane's `.ufo/waves/round-63/w1/` existed; `ScribeSkillRows/` was created for the draft only.

## Traceability table (row → claim → source)

| row | claim | source |
|---|---|---|
| a | full 40-hex name; `^{commit}` check with `--verify` | entry Q1, Q7 |
| a | tag id differs from commit id; peel with `^{commit}` | entry Claim 1, Q3, Q8 |
| a | `<rev>:<path>` pins bytes, not the commit | entry Claim 3 |
| a | abbreviation/prefix as pin is wrong; candidate list via `--disambiguate` | entry Claims 2, 4, 5; Q6 |
| a | git version named with the reading | entry Limits |
| a | rows S142–S144 and the entry path | entry header `source:` line |
| b | prefix stops resolving after later objects | entry Claim 2; Q1, Q2, Q9 |
| b | default abbreviation length is configuration | entry Claim 4; Q5 |
| b | branch outside Q1 forms; branch behaviour `[INFERENCE]` | entry Q1; Limits |
| c | command line, flags | docstring line 4 |
| c | verdict map 0/1/2; ENV never a pass; summary line | docstring lines 9, 11–12 |
| c | gate ids G01–G08 and G01 census script search order | docstring lines 14–24 |
| c | write scope, no network | docstring line 26 |
| c | battery command and `BATTERY=PASS` | UNTRACED (claims.md C1) |
| c | `tools/` path prefix | UNTRACED (claims.md C1) |

## Verdict inputs

Rows: 3. Untraced claims: 2 (both in row c, see point 2). Row b's branch half is traced only to an `[INFERENCE]` limit.
Nothing installed, nothing upgraded (no tool install was needed for a read-only seat). Scratch directory
`/fast/scratch/hyaku/chousa-r63/ScribeSkillRows` was created empty and removed before yielding.

VERDICT: SKILL_ROWS=3 untraceable_claims=2
